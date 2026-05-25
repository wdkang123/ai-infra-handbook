# ai-gateway Validation Matrix v1

## Task ID: T1202
## Title: ai-gateway Implementation Map Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# ai-gateway Validation Matrix

本文档定义 ai-gateway 各 patch 的验收测试矩阵。

## Validation Matrix

| ID | 端点 | 方法 | 场景 | 预期 HTTP | 验证命令 | 依赖 Patch |
|---|---|---|---|---|---|---|
| G01 | `/health` | GET | 健康检查 | 200 | `curl localhost:8080/health` | P1 |
| G02 | `/v1/chat/completions` | POST | 有效 token + 已知模型 | 200 | `curl -H "Authorization: Bearer dev-gateway-key-1" ...` | P3 |
| G03 | `/v1/chat/completions` | POST | 无 token | 401 | `curl ...`（无 Auth header） | P2 |
| G04 | `/v1/chat/completions` | POST | 错误 scheme（Basic） | 401 | `curl -H "Authorization: Basic ..."` | P2 |
| G05 | `/v1/chat/completions` | POST | 错误 scheme（无 Bearer） | 401 | `curl -H "Authorization: dev-gateway-key-1"` | P2 |
| G06 | `/v1/chat/completions` | POST | 无效 key | 401 | `curl -H "Authorization: Bearer invalid-key-xyz"` | P2 |
| G07 | `/v1/chat/completions` | POST | 未知模型 | 404 | `curl ... "model": "unknown-model"` | P3 |
| G08 | `/v1/chat/completions` | POST | 空消息 | 422 | `curl ... "messages": []` | P1（FastAPI 校验） |
| G09 | `/v1/chat/completions` | POST | RPM 超限 | 429 | 61+ req/min | P4 |
| G10 | `/metrics` | GET | Prometheus 格式 | 200 | `curl localhost:8080/metrics` | P1 |

---

## G01: /health 详细验证

```bash
curl -s http://localhost:8080/health | python -m json.tool
# 期望：
# {
#   "status": "healthy",
#   "version": "0.1.0"
# }
```

---

## G02: 有效 token + 已知模型（代理）

```bash
curl -s -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dev-gateway-key-1" \
  -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "What is 2+2?"}]}' \
  | python -m json.tool
# 期望：200 + inference-service 响应
```

**对应 fixture：** T1102 `proxy_responses/chat_completion_nonstreaming.json`

---

## G03-G06: 鉴权错误

```bash
# G03: 无 token
curl -s -w "\n%{http_code}" -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}'
# 期望：401 + {"error": {"message": "Missing Authorization header", "type": "authentication_error", "code": "401"}}

# G04: 错误 scheme
curl -s -w "\n%{http_code}" -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic dXNlcjpwYXNz" \
  -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}'
# 期望：401 + {"error": {"message": "Invalid Authorization header format. Expected: Bearer <key>", "type": "authentication_error", "code": "401"}}

# G06: 无效 key
curl -s -w "\n%{http_code}" -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer invalid-key-xyz" \
  -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}'
# 期望：401 + {"error": {"message": "Invalid API key", "type": "authentication_error", "code": "401"}}
```

**对应 fixture：** T1102 `auth/missing_auth.yaml`、`auth/wrong_scheme_basic.yaml`、`auth/invalid_api_key.yaml`

---

## G07: 未知模型路由

```bash
curl -s -w "\n%{http_code}" -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dev-gateway-key-1" \
  -d '{"model": "nonexistent-model", "messages": [{"role": "user", "content": "Hi"}]}'
# 期望：404 + {"error": {"message": "Model not found: nonexistent-model", "type": "invalid_request_error", "code": "404"}}
```

**对应 fixture：** T1102 `error_responses/404_model_not_found.json`

---

## G09: 限流

```bash
# 快速发送 65 个请求
for i in {1..65}; do
  curl -s -o /dev/null -w "%{http_code}\n" \
    -X POST http://localhost:8080/v1/chat/completions \
    -H "Authorization: Bearer dev-gateway-key-1" \
    -H "Content-Type: application/json" \
    -d '{"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}'
done | grep "429" | head -1
# 期望：至少一个 429
```

**对应 fixture：** T1102 `error_responses/429_rate_limit.json`

---

## pytest 测试覆盖

| Test | 覆盖 ID |
|---|---|
| `test_health_returns_200` | G01 |
| `test_auth_valid_bearer` | G02 |
| `test_auth_missing_token` | G03 |
| `test_auth_wrong_scheme` | G04 |
| `test_auth_invalid_key` | G06 |
| `test_proxy_known_model` | G02/G07 |
| `test_proxy_unknown_model` | G07 |
| `test_empty_messages` | G08 |
| `test_rate_limit_exceeded` | G09 |
| `test_metrics_endpoint` | G10 |

---

Sources:
- T1002: server.py, auth middleware blueprints
- T1102: all fixture files
- T812: API contract

Risk of Staleness:
- API contract is stable; validation matrix follows T812 contract
