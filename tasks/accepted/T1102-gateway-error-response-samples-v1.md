# ai-gateway Error Response Samples v1

## Task ID: T1102
## Title: ai-gateway Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# ai-gateway Error Response Samples

本文档定义 ai-gateway 各场景错误响应 fixture，对应真实文件 `ai-gateway/tests/fixtures/error_responses/`。

## 错误响应格式（统一）

所有错误响应均遵循 OpenAI 错误格式：

```json
{
  "error": {
    "message": "<human-readable message>",
    "type": "<error_type>",
    "code": "<status_code_as_string>"
  }
}
```

---

## 401 — Authentication Error

### Missing Authorization Header

**对应文件：** `ai-gateway/tests/fixtures/error_responses/401_missing_auth.json`

```json
{
  "error": {
    "message": "Missing Authorization header",
    "type": "authentication_error",
    "code": "401"
  }
}
```

### Invalid API Key

**对应文件：** `ai-gateway/tests/fixtures/error_responses/401_invalid_key.json`

```json
{
  "error": {
    "message": "Invalid API key",
    "type": "authentication_error",
    "code": "401"
  }
}
```

### Wrong Auth Scheme

**对应文件：** `ai-gateway/tests/fixtures/error_responses/401_wrong_scheme.json`

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

## 404 — Model Not Found

### Unknown Model Name

**对应文件：** `ai-gateway/tests/fixtures/error_responses/404_model_not_found.json`

```json
{
  "error": {
    "message": "Model not found: unknown-model-xyz",
    "type": "invalid_request_error",
    "code": "404"
  }
}
```

请求示例：
```
POST /v1/chat/completions
{
  "model": "unknown-model-xyz",
  "messages": [{"role": "user", "content": "Hi"}]
}
```

---

## 422 — Validation Error

### Empty Messages

**对应文件：** `ai-gateway/tests/fixtures/error_responses/422_empty_messages.json`

```json
{
  "error": {
    "message": "messages must not be empty",
    "type": "invalid_request_error",
    "code": "validation_error"
  }
}
```

### Invalid Temperature

**对应文件：** `ai-gateway/tests/fixtures/error_responses/422_invalid_temperature.json`

```json
{
  "error": {
    "message": "temperature must be <= 2.0",
    "type": "invalid_request_error",
    "code": "validation_error"
  }
}
```

---

## 429 — Rate Limit Exceeded

**对应文件：** `ai-gateway/tests/fixtures/error_responses/429_rate_limit.json`

```json
{
  "error": {
    "message": "Rate limit exceeded",
    "type": "rate_limit_error",
    "code": "429"
  }
}
```

---

## 502 — Bad Gateway（Downstream Error）

### Downstream Inference Service Unavailable

**对应文件：** `ai-gateway/tests/fixtures/error_responses/502_downstream_unavailable.json`

```json
{
  "error": {
    "message": "Downstream inference service unavailable",
    "type": "server_error",
    "code": "502"
  }
}
```

### Downstream Engine Error

**对应文件：** `ai-gateway/tests/fixtures/error_responses/502_engine_error.json`

```json
{
  "error": {
    "message": "Inference engine error",
    "type": "server_error",
    "code": "502"
  }
}
```

---

## 500 — Internal Server Error

**对应文件：** `ai-gateway/tests/fixtures/error_responses/500_internal.json`

```json
{
  "error": {
    "message": "Internal server error",
    "type": "server_error",
    "code": "500"
  }
}
```

---

## Error Type Catalog

| HTTP Status | `type` 值 | 说明 |
|---|---|---|
| 401 | `authentication_error` | 鉴权失败 |
| 404 | `invalid_request_error` | 未知模型 |
| 422 | `invalid_request_error` | 请求校验失败 |
| 429 | `rate_limit_error` | 限流 |
| 500 | `server_error` | 服务器内部错误 |
| 502 | `server_error` | 下游不可用 |
| 503 | `server_error` | 服务不可用 |

---

Sources:
1. https://platform.openai.com/docs/guides/error-codes — OpenAI error codes
2. https://github.com/Portkey-AI/gateway — Portkey error format

Risk of Staleness:
- OpenAI error format is part of API spec; stable
