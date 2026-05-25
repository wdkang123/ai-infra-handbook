# ai-gateway Auth Request Fixtures v1

## Task ID: T1102
## Title: ai-gateway Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# ai-gateway Auth Request Fixtures

本文档定义 ai-gateway 鉴权中间件的请求 fixture，对应真实文件 `ai-gateway/tests/fixtures/auth/`。

## 覆盖场景

1. Valid Bearer token
2. Missing Authorization header
3. Wrong auth scheme（e.g. Basic instead of Bearer）
4. Invalid API key

---

## Scenario 1: Valid Bearer Token

**对应文件：** `ai-gateway/tests/fixtures/auth/valid_bearer.yaml`

请求：
```yaml
headers:
  Authorization: "Bearer dev-gateway-key-1"
  Content-Type: "application/json"
method: "POST"
path: "/v1/chat/completions"
body_present: true
```

期望：
- 鉴权中间件返回 `"dev-gateway-key-1"`（已验证的 token 字符串）
- 请求继续传递到下游处理

---

## Scenario 2: Missing Authorization Header

**对应文件：** `ai-gateway/tests/fixtures/auth/missing_auth.yaml`

请求：
```yaml
headers:
  Content-Type: "application/json"
  # Authorization header 完全缺失
method: "POST"
path: "/v1/chat/completions"
body_present: true
```

期望响应（HTTP 401）：
```json
{
  "error": {
    "message": "Missing Authorization header",
    "type": "authentication_error",
    "code": "401"
  }
}
```

---

## Scenario 3: Wrong Auth Scheme（Basic instead of Bearer）

**对应文件：** `ai-gateway/tests/fixtures/auth/wrong_scheme_basic.yaml`

请求：
```yaml
headers:
  Authorization: "Basic dXNlcjpwYXNz"
  Content-Type: "application/json"
method: "POST"
path: "/v1/chat/completions"
body_present: true
```

期望响应（HTTP 401）：
```json
{
  "error": {
    "message": "Invalid Authorization header format. Expected: Bearer <key>",
    "type": "authentication_error",
    "code": "401"
  }
}
```

---

## Scenario 4: Wrong Auth Scheme（Token without Bearer prefix）

**对应文件：** `ai-gateway/tests/fixtures/auth/wrong_scheme_token_only.yaml`

请求：
```yaml
headers:
  Authorization: "dev-gateway-key-1"
  Content-Type: "application/json"
method: "POST"
path: "/v1/chat/completions"
body_present: true
```

期望响应（HTTP 401）：
```json
{
  "error": {
    "message": "Invalid Authorization header format. Expected: Bearer <key>",
    "type": "authentication_error",
    "code": "401"
  }
}
```

---

## Scenario 5: Invalid API Key

**对应文件：** `ai-gateway/tests/fixtures/auth/invalid_api_key.yaml`

请求：
```yaml
headers:
  Authorization: "Bearer invalid-key-xyz"
  Content-Type: "application/json"
method: "POST"
path: "/v1/chat/completions"
body_present: true
```

期望响应（HTTP 401）：
```json
{
  "error": {
    "message": "Invalid API key",
    "type": "authentication_error",
    "code": "401"
  }
}
```

---

## Scenario 6: Auth Disabled（config.auth.enabled=false）

**对应文件：** `ai-gateway/tests/fixtures/auth/auth_disabled.yaml`

请求：
```yaml
headers:
  # 无 Authorization header
  Content-Type: "application/json"
method: "POST"
path: "/v1/chat/completions"
body_present: true
config_override:
  auth:
    enabled: false
```

期望：
- 鉴权中间件返回 `None`（bypass）
- 请求继续传递到下游处理，即使没有 auth header

---

## Auth Config Shape

```yaml
# ai-gateway/configs/config.yaml
auth:
  enabled: true                    # false = skip auth entirely
  api_keys:                       # list of accepted Bearer tokens
    - "dev-gateway-key-1"
    - "dev-gateway-key-2"
  bypass_paths:                    # paths that skip auth
    - "/health"
    - "/metrics"
```

---

## Fixture Catalog

| 文件 | 场景 | 期望 HTTP |
|---|---|---|
| `auth/valid_bearer.yaml` | 有效 Bearer token | 透传（200/4xx取决于下游） |
| `auth/missing_auth.yaml` | 缺少 Auth header | 401 |
| `auth/wrong_scheme_basic.yaml` | Basic scheme | 401 |
| `auth/wrong_scheme_token_only.yaml` | 只有 token 无 Bearer | 401 |
| `auth/invalid_api_key.yaml` | 无效 key | 401 |
| `auth/auth_disabled.yaml` | auth.enabled=false | 透传 |

---

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey auth reference
2. https://fastapi.tiangolo.com/tutorial/security/ — FastAPI security

Risk of Staleness:
- Bearer token format is part of OAuth 2.0 spec (RFC 6750); stable
