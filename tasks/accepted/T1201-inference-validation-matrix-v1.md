# inference-service Validation Matrix v1

## Task ID: T1201
## Title: inference-service Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# inference-service Validation Matrix

本文档定义 inference-service 各 patch 的验收测试矩阵，对应 T1201 patch split。

## Validation Matrix

| ID | 端点 | 方法 | 场景 | 预期 HTTP | 验证命令 | 依赖 Patch |
|---|---|---|---|---|---|---|
| V01 | `/health` | GET | 引擎就绪 | 200 | `curl localhost:8000/health` | P1 |
| V02 | `/health` | GET | 引擎未初始化 | 200 | `curl localhost:8000/health`（返回 degraded） | P1 |
| V03 | `/metrics` | GET | Prometheus 格式 | 200 | `curl localhost:8000/metrics \| grep "^vllm_"` | P4 |
| V04 | `/v1/chat/completions` | POST | 基本推理 | 200 | `curl POST /v1/chat/completions ...` | P2 |
| V05 | `/v1/chat/completions` | POST | 带 system message | 200 | 同上 + system message | P2 |
| V06 | `/v1/chat/completions` | POST | 带 stop token | 200 | `curl ... "stop": ["5"]` | P2 |
| V07 | `/v1/chat/completions` | POST | 流式推理 | 200 + SSE | `curl -N ... "stream": true` | P3 |
| V08 | `/v1/chat/completions` | POST | 未知模型 | 404 | `curl ... "model": "nonexistent"` | P1 |
| V09 | `/v1/chat/completions` | POST | 空消息 | 422 | `curl ... "messages": []` | P1 |
| V10 | `/v1/chat/completions` | POST | temperature > 2.0 | 422 | `curl ... "temperature": 3.0` | P1 |
| V11 | `/v1/chat/completions` | POST | 缺 model 字段 | 422 | `curl ...`（无 model 字段） | P1 |

---

## V01-V02: /health 详细验证

```bash
# V01: 引擎就绪
curl -s http://localhost:8000/health | python -m json.tool
# 期望：
# {
#   "status": "healthy",
#   "engine": "vllm",
#   "model": "Qwen2.5-0.5B-Instruct",
#   "gpu_available": true
# }
```

**对应 fixture：** T1101 `health_all_systems_go.json`

---

## V03: /metrics 详细验证

```bash
# V03: Prometheus 格式
curl -s http://localhost:8000/metrics | grep -E "^vllm_|^inference_service_"
# 期望至少：
# vllm_num_requests_running 0
# vllm_num_tokens_total 0
# inference_service_requests_total 0
```

**对应 fixture：** T1101 `metrics_idle_state.txt`

---

## V04-V06: /v1/chat/completions 非流式详细验证

```bash
# V04: 基本推理
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen2.5-0.5B-Instruct",
    "messages": [{"role": "user", "content": "What is 2+2?"}]
  }' | python -m json.tool
# 期望：
# {
#   "id": "chatcmpl-*",
#   "object": "chat.completion",
#   "choices": [{"message": {"role": "assistant", "content": "4"}, "finish_reason": "stop"}],
#   "usage": {"prompt_tokens": *, "completion_tokens": *, "total_tokens": *}
# }
```

**对应 fixture：** T1101 `chat_basic_request.json`

---

## V07: 流式推理详细验证

```bash
# V07: SSE 流式
curl -N -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen2.5-0.5B-Instruct",
    "messages": [{"role": "user", "content": "Count to 3"}],
    "stream": true
  }' 2>/dev/null | head -10
# 期望：
# data: {"id":"chatcmpl-*","choices":[{"delta":{"role":"assistant","content":"1"},"finish_reason":null}]}
# ...
# data: [DONE]
```

**对应 fixture：** T1101 `sse_chat_sequence/sequence_a_short_answer.txt`

---

## V08-V11: 错误响应详细验证

```bash
# V08: 未知模型
curl -s -w "\n%{http_code}" -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "nonexistent", "messages": [{"role": "user", "content": "Hi"}]}'
# 期望 HTTP 404，body 含 "code": "404"

# V09: 空消息
curl -s -w "\n%{http_code}" -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "Qwen2.5-0.5B-Instruct", "messages": []}'
# 期望 HTTP 422

# V10: temperature 超限
curl -s -w "\n%{http_code}" -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "Qwen2.5-0.5B-Instruct", "messages": [{"role": "user", "content": "Hi"}], "temperature": 3.0}'
# 期望 HTTP 422
```

**对应 fixture：** T1101 `chat_unknown_model.json`、`chat_empty_messages.json`、`chat_temperature_invalid.json`

---

## pytest 测试覆盖

| Test | 覆盖 ID | 类 |
|---|---|---|
| `test_health_returns_200` | V01 | `TestHealth` |
| `test_health_never_returns_500` | V02 | `TestHealth` |
| `test_metrics_returns_prometheus_text` | V03 | `TestMetrics` |
| `test_metrics_content_type` | V03 | `TestMetrics` |
| `test_chat_basic_request` | V04 | `TestChatCompletions` |
| `test_chat_with_system_message` | V05 | `TestChatCompletions` |
| `test_chat_with_stop_token` | V06 | `TestChatCompletions` |
| `test_chat_streaming` | V07 | `TestChatCompletions` |
| `test_invalid_model_returns_404` | V08 | `TestErrorCases` |
| `test_empty_messages_returns_422` | V09 | `TestErrorCases` |
| `test_missing_model_field_returns_422` | V11 | `TestErrorCases` |
| `test_chat_temperature_validation` | V10 | `TestChatCompletions` |

---

Sources:
- T1001: test_api.py blueprint
- T1101: fixture assets
- T811: API contract

Risk of Staleness:
- API contract is stable; validation matrix follows T811 contract
