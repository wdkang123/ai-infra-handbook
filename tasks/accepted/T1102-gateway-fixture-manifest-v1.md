# ai-gateway Fixture Manifest v1

## Task ID: T1102
## Title: ai-gateway Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# ai-gateway Fixture Manifest

本文档是 `ai-gateway` 全部 fixture 资产的索引清单，对应真实路径 `ai-gateway/tests/fixtures/` 和 `ai-gateway/configs/`。

## Fixture 文件清单

### Auth Fixtures

| 文件路径 | 场景 | 期望 HTTP |
|---|---|---|
| `tests/fixtures/auth/valid_bearer.yaml` | 有效 Bearer token | 透传 |
| `tests/fixtures/auth/missing_auth.yaml` | 缺少 Auth header | 401 |
| `tests/fixtures/auth/wrong_scheme_basic.yaml` | Basic scheme | 401 |
| `tests/fixtures/auth/wrong_scheme_token_only.yaml` | 无 Bearer prefix | 401 |
| `tests/fixtures/auth/invalid_api_key.yaml` | 无效 key | 401 |
| `tests/fixtures/auth/auth_disabled.yaml` | auth.enabled=false | 透传 |

### Routing Config Fixtures

| 文件路径 | 场景 |
|---|---|
| `configs/models.yaml` | 模型路由配置 |
| `configs/config.yaml` | 完整配置 |
| `configs/config.local.yaml` | 本地开发配置 |

### Error Response Fixtures

| 文件路径 | 场景 | HTTP |
|---|---|---|
| `tests/fixtures/error_responses/401_missing_auth.json` | 缺 auth | 401 |
| `tests/fixtures/error_responses/401_invalid_key.json` | 无效 key | 401 |
| `tests/fixtures/error_responses/401_wrong_scheme.json` | 错误 scheme | 401 |
| `tests/fixtures/error_responses/404_model_not_found.json` | 未知模型 | 404 |
| `tests/fixtures/error_responses/422_empty_messages.json` | 空消息 | 422 |
| `tests/fixtures/error_responses/422_invalid_temperature.json` | temperature 超限 | 422 |
| `tests/fixtures/error_responses/429_rate_limit.json` | 限流 | 429 |
| `tests/fixtures/error_responses/502_downstream_unavailable.json` | 下游不可用 | 502 |
| `tests/fixtures/error_responses/502_engine_error.json` | 引擎错误 | 502 |
| `tests/fixtures/error_responses/500_internal.json` | 内部错误 | 500 |

### Proxy Response Fixtures

| 文件路径 | 场景 |
|---|---|
| `tests/fixtures/proxy_responses/chat_completion_nonstreaming.json` | 非流式响应 |
| `tests/fixtures/proxy_responses/sse_chunk_01.txt` | 流式 chunk 样例 |
| `tests/fixtures/proxy_responses/chat_completion_with_usage.json` | 含 usage 字段 |
| `tests/fixtures/proxy_responses/model_name_mapping.yaml` | 路由模型名映射 |
| `tests/fixtures/proxy_responses/downstream_timeout_502.json` | 下游超时 |
| `tests/fixtures/proxy_responses/downstream_404.json` | 下游 404 透传 |

---

## 与 API Contract 对齐（T812）

| 契约点 | Fixture 覆盖 |
|---|---|
| `POST /v1/chat/completions` | proxy_responses/* |
| 鉴权 401 | auth/* (5 个场景) |
| 路由 404 | error_responses/404_model_not_found |
| 限流 429 | error_responses/429_rate_limit |
| 错误格式 | error_responses/* 全部 |

---

## 与 Starter Blueprint 对齐（T1002）

| Blueprint 要点 | Fixture 对应 |
|---|---|
| `verify_api_key()` auth bypass | `auth/auth_disabled.yaml` |
| `ChatCompletionsResponse` 未定义 → 改用 JSONResponse | proxy_responses 均为 JSON |
| `/v1/chat/completions` 路由 | `configs/models.yaml` |
| 错误格式 OpenAI style | error_responses/* |

---

Sources:
1. https://github.com/Portkey-AI/gateway
2. https://fastapi.tiangolo.com/tutorial/security/

Risk of Staleness:
- Bearer auth (RFC 6750) and OpenAI error format stable
