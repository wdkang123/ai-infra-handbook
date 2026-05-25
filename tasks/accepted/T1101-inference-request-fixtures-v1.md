# inference-service Request Fixtures v1

## Task ID: T1101
## Title: inference-service Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# inference-service Request Fixtures

本文档定义 `inference-service` 各端点的请求/响应 fixture，对应真实文件路径 `tests/fixtures/` 下将被 Codex 实现引用。

## 覆盖端点

- `GET  /health`
- `GET  /metrics`
- `POST /v1/chat/completions`（non-streaming + streaming）

---

## GET /health — 响应 fixture

### 正常响应（引擎就绪）

**对应文件：** `inference-service/tests/fixtures/health_all_systems_go.json`

```json
{
  "status": "healthy",
  "engine": "vllm",
  "model": "Qwen2.5-0.5B-Instruct",
  "gpu_available": true
}
```

### 正常响应（引擎未完全就绪，但服务仍可响应）

**对应文件：** `inference-service/tests/fixtures/health_degraded.json`

```json
{
  "status": "degraded",
  "engine": "vllm",
  "model": "Qwen2.5-0.5B-Instruct",
  "gpu_available": false
}
```

---

## GET /metrics — 响应 fixture

**对应文件：** `inference-service/tests/fixtures/metrics_idle_state.txt`

```
# HELP vllm_num_requests_running Currently running requests
# TYPE vllm_num_requests_running gauge
vllm_num_requests_running 0
# HELP vllm_num_tokens_total Total tokens generated
# TYPE vllm_num_tokens_total counter
vllm_num_tokens_total 128
# HELP vllm_avg_latency_ms Average inference latency
# TYPE vllm_avg_latency_ms gauge
vllm_avg_latency_ms 45.3
# HELP inference_service_requests_total Total chat completion requests
# TYPE inference_service_requests_total counter
inference_service_requests_total 12
# HELP inference_service_streaming_total Total streaming responses
# TYPE inference_service_streaming_total counter
inference_service_streaming_total 5
# HELP inference_service_errors_total Total errors by type
# TYPE inference_service_errors_total counter
inference_service_errors_total{model="unknown"} 2
```

---

## POST /v1/chat/completions — Non-streaming Fixtures

### Fixture 1: Basic Request

**对应文件：** `inference-service/tests/fixtures/chat_basic_request.json`

请求：
```json
{
  "model": "Qwen2.5-0.5B-Instruct",
  "messages": [
    {"role": "user", "content": "What is 2+2?"}
  ],
  "temperature": 0.7,
  "max_tokens": 256,
  "stream": false
}
```

响应（HTTP 200）：
```json
{
  "id": "chatcmpl-1704067200000",
  "object": "chat.completion",
  "created": 1704067200,
  "model": "Qwen2.5-0.5B-Instruct",
  "choices": [
    {
      "index": 0,
      "message": {"role": "assistant", "content": "4"},
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 1,
    "total_tokens": 13
  }
}
```

---

### Fixture 2: With System Message

**对应文件：** `inference-service/tests/fixtures/chat_with_system_message.json`

请求：
```json
{
  "model": "Qwen2.5-0.5B-Instruct",
  "messages": [
    {"role": "system", "content": "You are a helpful math assistant."},
    {"role": "user", "content": "What is 2+2?"}
  ],
  "temperature": 0.7,
  "max_tokens": 256,
  "stream": false
}
```

响应（HTTP 200）：
```json
{
  "id": "chatcmpl-1704067200001",
  "object": "chat.completion",
  "created": 1704067201,
  "model": "Qwen2.5-0.5B-Instruct",
  "choices": [
    {
      "index": 0,
      "message": {"role": "assistant", "content": "4"},
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 24,
    "completion_tokens": 1,
    "total_tokens": 25
  }
}
```

---

### Fixture 3: With Stop Token

**对应文件：** `inference-service/tests/fixtures/chat_with_stop_token.json`

请求：
```json
{
  "model": "Qwen2.5-0.5B-Instruct",
  "messages": [
    {"role": "user", "content": "Count to 5"}
  ],
  "temperature": 0.7,
  "max_tokens": 256,
  "stop": ["5"]
}
```

响应（HTTP 200）：
```json
{
  "id": "chatcmpl-1704067200002",
  "object": "chat.completion",
  "created": 1704067202,
  "model": "Qwen2.5-0.5B-Instruct",
  "choices": [
    {
      "index": 0,
      "message": {"role": "assistant", "content": "1, 2, 3, 4"},
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 8,
    "total_tokens": 18
  }
}
```

---

### Fixture 4: Invalid Model — Unknown Model

**对应文件：** `inference-service/tests/fixtures/chat_unknown_model.json`

请求：
```json
{
  "model": "nonexistent-model",
  "messages": [
    {"role": "user", "content": "Hi"}
  ]
}
```

响应（HTTP 404）：
```json
{
  "error": {
    "message": "Model not found: nonexistent-model",
    "type": "invalid_request_error",
    "code": "404"
  }
}
```

---

### Fixture 5: Empty Messages — Validation Error

**对应文件：** `inference-service/tests/fixtures/chat_empty_messages.json`

请求：
```json
{
  "model": "Qwen2.5-0.5B-Instruct",
  "messages": []
}
```

响应（HTTP 422）：
```json
{
  "error": {
    "message": "messages must not be empty",
    "type": "invalid_request_error",
    "code": "validation_error"
  }
}
```

---

### Fixture 6: Missing Model Field

**对应文件：** `inference-service/tests/fixtures/chat_missing_model.json`

请求：
```json
{
  "messages": [
    {"role": "user", "content": "Hi"}
  ]
}
```

响应（HTTP 422）：
```json
{
  "error": {
    "message": "field required",
    "type": "invalid_request_error",
    "code": "validation_error"
  }
}
```

---

### Fixture 7: Temperature Out of Range

**对应文件：** `inference-service/tests/fixtures/chat_temperature_invalid.json`

请求：
```json
{
  "model": "Qwen2.5-0.5B-Instruct",
  "messages": [{"role": "user", "content": "Hi"}],
  "temperature": 3.0
}
```

响应（HTTP 422）：
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

## Streaming Fixtures

### Fixture 8: Streaming Request

**对应文件：** `inference-service/tests/fixtures/chat_streaming_request.json`

请求：
```json
{
  "model": "Qwen2.5-0.5B-Instruct",
  "messages": [
    {"role": "user", "content": "Count to 3"}
  ],
  "stream": true,
  "max_tokens": 50
}
```

响应（HTTP 200, `Content-Type: text/event-stream`）：
每个 chunk 为一行 `data: {...}\n\n`，连续发送后以 `data: [DONE]\n\n` 结尾：
```
data: {"id":"chatcmpl-1704067200003","object":"chat.completion.chunk","created":1704067203,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{"role":"assistant","content":"1"},"finish_reason":null}]}

data: {"id":"chatcmpl-1704067200003","object":"chat.completion.chunk","created":1704067203,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{"content":","},"finish_reason":null}]}

data: {"id":"chatcmpl-1704067200003","object":"chat.completion.chunk","created":1704067203,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{"content":" 2"},"finish_reason":null}]}

data: {"id":"chatcmpl-1704067200003","object":"chat.completion.chunk","created":1704067203,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{"content":","},"finish_reason":null}]}

data: {"id":"chatcmpl-1704067200003","object":"chat.completion.chunk","created":1704067203,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{"content":" 3"},"finish_reason":null}]}

data: {"id":"chatcmpl-1704067200003","object":"chat.completion.chunk","created":1704067203,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```

---

## Fixture Catalog

| Fixture ID | 文件路径 | 场景 | HTTP |
|---|---|---|---|
| F01 | `tests/fixtures/health_all_systems_go.json` | /health 就绪 | 200 |
| F02 | `tests/fixtures/health_degraded.json` | /health 降级 | 200 |
| F03 | `tests/fixtures/metrics_idle_state.txt` | /metrics | 200 |
| F04 | `tests/fixtures/chat_basic_request.json` | 基本推理 | 200 |
| F05 | `tests/fixtures/chat_with_system_message.json` | 系统消息 | 200 |
| F06 | `tests/fixtures/chat_with_stop_token.json` | stop token | 200 |
| F07 | `tests/fixtures/chat_unknown_model.json` | 未知模型 | 404 |
| F08 | `tests/fixtures/chat_empty_messages.json` | 空消息 | 422 |
| F09 | `tests/fixtures/chat_missing_model.json` | 缺 model 字段 | 422 |
| F10 | `tests/fixtures/chat_temperature_invalid.json` | temperature 超限 | 422 |
| F11 | `tests/fixtures/chat_streaming_request.json` | 流式推理 | 200+SSE |

---

## 与 Starter Blueprint 契约对齐

| 字段 | Starter Blueprint (`T1001`) | 本 Fixture |
|---|---|---|
| `choices[0].message.role` | `"assistant"` | `"assistant"` |
| `finish_reason` | `"stop"` | `"stop"` |
| 错误格式 | OpenAI 风格 | OpenAI 风格 |
| SSE terminator | `data: [DONE]` | `data: [DONE]` |

---

Sources:
1. https://docs.vllm.ai/en/latest/serving/openai_compatibility_server.html — vLLM OpenAI compatibility
2. https://platform.openai.com/docs/api-reference/chat/create — OpenAI Chat API

Risk of Staleness:
- vLLM OpenAI compatibility layer is stable since v0.3; field names unlikely to change
