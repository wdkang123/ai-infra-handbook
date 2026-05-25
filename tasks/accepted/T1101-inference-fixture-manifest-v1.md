# inference-service Fixture Manifest v1

## Task ID: T1101
## Title: inference-service Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# inference-service Fixture Manifest

本文档是 `inference-service` 全部 fixture 资产的索引清单，对应真实路径 `inference-service/tests/fixtures/` 和 `inference-service/configs/`。

## Fixture 文件清单

### Request / Response Fixtures

| 文件路径 | Fixture ID | 场景 |
|---|---|---|
| `tests/fixtures/health_all_systems_go.json` | F01 | /health — 引擎就绪 |
| `tests/fixtures/health_degraded.json` | F02 | /health — GPU 不可用 |
| `tests/fixtures/health_engine_not_ready.json` | F03 | /health — 引擎启动中 |
| `tests/fixtures/metrics_idle_state.txt` | F04 | /metrics — 空载 |
| `tests/fixtures/metrics_active_workload.txt` | F05 | /metrics — 活跃负载 |
| `tests/fixtures/metrics_with_errors.txt` | F06 | /metrics — 含错误统计 |
| `tests/fixtures/chat_basic_request.json` | F07 | POST /v1/chat/completions — 基本 |
| `tests/fixtures/chat_with_system_message.json` | F08 | POST /v1/chat/completions — 系统消息 |
| `tests/fixtures/chat_with_stop_token.json` | F09 | POST /v1/chat/completions — stop token |
| `tests/fixtures/chat_unknown_model.json` | F10 | POST /v1/chat/completions — 未知模型 404 |
| `tests/fixtures/chat_empty_messages.json` | F11 | POST /v1/chat/completions — 空消息 422 |
| `tests/fixtures/chat_missing_model.json` | F12 | POST /v1/chat/completions — 缺 model 422 |
| `tests/fixtures/chat_temperature_invalid.json` | F13 | POST /v1/chat/completions — temperature 超限 |
| `tests/fixtures/chat_streaming_request.json` | F14 | POST /v1/chat/completions — 流式请求体 |

### SSE Sequence Fixtures

| 文件路径 | 场景 |
|---|---|
| `tests/fixtures/sse_chat_sequence/sequence_a_short_answer.txt` | 3 token 短回答 |
| `tests/fixtures/sse_chat_sequence/sequence_b_multitoken.txt` | 多 token 回答 |
| `tests/fixtures/sse_chat_sequence/sequence_c_with_system.txt` | 带 system message 流式 |
| `tests/fixtures/sse_chat_sequence/sequence_d_nonstreaming.json` | 非流式响应（对比） |

### Config Examples

| 文件路径 | 场景 |
|---|---|
| `configs/.env.local` | 本地开发 .env |
| `configs/config.yaml` | 标准 config.yaml |
| `configs/config.local.yaml` | 本地开发用 config |
| `configs/config.smoke.yaml` | 冒烟测试用 config |

---

## 与 API Contract 对齐（T811）

| 契约点 | Fixture 覆盖 |
|---|---|
| `POST /v1/chat/completions` | F07~F14 |
| `GET /health` | F01~F03 |
| `GET /metrics` | F04~F06 |
| 错误格式 OpenAI 风格 | F10~F13 |
| SSE 终止符 `data: [DONE]` | SSE sequence files |

---

## 与 Starter Blueprint 对齐（T1001）

| Blueprint 要点 | Fixture 对应 |
|---|---|
| `/metrics` 需含 `vllm_*` | F04~F06 均含 |
| `finish_reason: stop` | F07~F09 |
| `role: assistant` | F07~F09, SSE sequences |
| temperature max 2.0 | F13 (invalid fixture) |
| 404 model_not_found | F10 |

---

## 依赖关系

- F01~F03 依赖 `HealthResponse` model（T1001 server.py）
- F04~F06 依赖 Prometheus client 输出格式
- F07~F14 依赖 `ChatCompletionsRequest` / `ChatCompletionsResponse` model（T1001 server.py）
- SSE sequences 依赖 `_stream_chat()` 实现（T1001 server.py）

---

Sources:
1. https://docs.vllm.ai/en/latest/serving/openai_compatibility_server.html
2. https://platform.openai.com/docs/api-reference/chat/create

Risk of Staleness:
- OpenAI API format stable; vLLM compatibility layer stable
