# Root Integration Smoke Expected Output v1

## Task ID: T1105
## Title: Root Integration Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# Root Integration Smoke Expected Output

本文档定义 `scripts/integration_smoke_test.sh` 各测试项的预期输出，对应真实文件 `ai-infra/tests/fixtures/smoke_expected/`。

## Smoke Test ID Map

| Test ID | 场景 | 对应 Script Function |
|---|---|---|
| IT-01b | Direct inference-service | `test_it01_direct()` |
| IT-01 | Gateway → Inference proxy | `test_it01()` |
| IT-02 | Streaming | `test_it02()` |
| IT-03 | Health both | `test_it03()` |
| IT-04 | Auth — no token | `test_it04()` |
| IT-05 | Auth — invalid token | `test_it05()` |
| IT-06 | Unknown model | `test_it06()` |
| IT-07 | Metrics endpoints | `test_it07()` |

---

## IT-01b: Direct inference-service — Expected

**对应文件：** `ai-infra/tests/fixtures/smoke_expected/it01b_expected.json`

执行：
```bash
curl -s -w "\n%{http_code}" -X POST "${INFERENCE_URL}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{"model": "Qwen2.5-0.5B-Instruct", "messages": [{"role": "user", "content": "What is 2+2?"}]}'
```

预期：
- HTTP 200
- JSON body 含 `"choices"` 数组
- `choices[0].message.role == "assistant"`
- `choices[0].finish_reason == "stop"`

```json
{
  "id": "chatcmpl-*",
  "object": "chat.completion",
  "created": 1704067200,
  "model": "Qwen2.5-0.5B-Instruct",
  "choices": [
    {
      "index": 0,
      "message": {"role": "assistant", "content": "*"},
      "finish_reason": "stop"
    }
  ],
  "usage": {"prompt_tokens": 12, "completion_tokens": 1, "total_tokens": 13}
}
```

---

## IT-01: Gateway → Inference — Expected

**对应文件：** `ai-infra/tests/fixtures/smoke_expected/it01_expected.json`

执行：
```bash
curl -s -w "\n%{http_code}" -X POST "${GATEWAY_URL}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AUTH_KEY}" \
  -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "What is 2+2?"}]}'
```

预期：
- HTTP 200
- JSON body 含 `"choices"` 数组
- `model` 字段为 `"vllm-local"`（ai-gateway 透传）

---

## IT-02: Streaming — Expected

**对应文件：** `ai-infra/tests/fixtures/smoke_expected/it02_expected.txt`

执行：
```bash
curl -s -X POST "${INFERENCE_URL}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{"model": "Qwen2.5-0.5B-Instruct", "messages": [{"role": "user", "content": "Count to 3"}], "stream": true}' \
  | head -5
```

预期输出：
```
data: {"id":"chatcmpl-*","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"role":"assistant","content":"*"},"finish_reason":null}]}

data: {"id":"chatcmpl-*","object":"chat.completion.chunk","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```

验证：
- `grep -q "data:"` → pass
- `Content-Type` 含 `text/event-stream`

---

## IT-03: Health Both — Expected

**对应文件：** `ai-infra/tests/fixtures/smoke_expected/it03_expected.json`

```bash
curl -s http://localhost:8000/health
curl -s http://localhost:8080/health
```

预期：
```json
{"status": "healthy", "engine": "vllm", "model": "Qwen2.5-0.5B-Instruct", "gpu_available": true}
{"status": "healthy", "version": "0.1.0"}
```

---

## IT-04: No Auth Token — Expected

**对应文件：** `ai-infra/tests/fixtures/smoke_expected/it04_expected.json`

```bash
curl -s -w "\n%{http_code}" -X POST "${GATEWAY_URL}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}'
```

预期：
- HTTP 401
```json
{"error": {"message": "Missing Authorization header", "type": "authentication_error", "code": "401"}}
```

---

## IT-05: Invalid Token — Expected

**对应文件：** `ai-infra/tests/fixtures/smoke_expected/it05_expected.json`

```bash
curl -s -w "\n%{http_code}" -X POST "${GATEWAY_URL}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer invalid-key-xyz" \
  -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}'
```

预期：
- HTTP 401
```json
{"error": {"message": "Invalid API key", "type": "authentication_error", "code": "401"}}
```

---

## IT-06: Unknown Model — Expected

**对应文件：** `ai-infra/tests/fixtures/smoke_expected/it06_expected.json`

```bash
curl -s -w "\n%{http_code}" -X POST "${GATEWAY_URL}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AUTH_KEY}" \
  -d '{"model": "unknown-model-xyz", "messages": [{"role": "user", "content": "Hi"}]}'
```

预期：
- HTTP 404
```json
{"error": {"message": "Model not found: unknown-model-xyz", "type": "invalid_request_error", "code": "404"}}
```

---

## IT-07: Metrics — Expected

**对应文件：** `ai-infra/tests/fixtures/smoke_expected/it07_expected.txt`

```bash
curl -s http://localhost:8000/metrics | grep "vllm_"
curl -s http://localhost:8080/metrics | grep "ai_gateway_"
```

预期 inference-service `/metrics` 输出包含：
```
vllm_num_requests_running 0
vllm_num_tokens_total 0
inference_service_requests_total 0
```

预期 ai-gateway `/metrics` 输出包含：
```
ai_gateway_requests_total 0
```

---

## Smoke Summary Output（预期格式）

**对应文件：** `ai-infra/tests/fixtures/smoke_expected/summary_expected.txt`

```
[PASS]  IT-01b: inference-service direct returned 200
[PASS]  IT-01: Gateway proxy returned 200
[PASS]  IT-02: Streaming response contains SSE data
[PASS]  IT-03: inference-service /health returned 200
[PASS]  IT-03: ai-gateway /health returned 200
[PASS]  IT-04: No token → 401
[PASS]  IT-05: Invalid token → 401
[PASS]  IT-06: Unknown model → 404
[PASS]  IT-07: inference-service /metrics contains vllm_ metrics
[PASS]  IT-07: ai-gateway /metrics contains ai_gateway_ metrics

==========================================
Smoke Test Summary: 10 passed, 0 failed
==========================================
```

---

Sources:
1. https://docs.vllm.ai/en/latest/serving/openai_compatibility_server.html
2. https://github.com/Portkey-AI/gateway

Risk of Staleness:
- OpenAI API format stable; aligns with T811/T812 contracts
