# inference-service API Contract v1

## Task ID: T801
## Task Title: inference-service Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T301 MVP 设计，准备 inference-service 实施前包。

---

# inference-service API Contract v1

## 概述

本文档定义 inference-service 的 OpenAI 兼容 API 接口契约。

---

## 端点总览

| 端点 | 方法 | 说明 | MVP 必须 |
|------|------|------|---------|
| `/v1/chat/completions` | POST | 聊天补全 | 是 |
| `/v1/completions` | POST | 文本补全 | 是 |
| `/v1/models` | GET | 可用模型列表 | 是 |
| `/health` | GET | 健康检查 | 是 |
| `/metrics` | GET | Prometheus metrics | 是 |

---

## `POST /v1/chat/completions`

### 请求

```json
{
  "model": "string",
  "messages": [
    {
      "role": "system | user | assistant",
      "content": "string"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 256,
  "stream": false,
  "stop": null,
  "frequency_penalty": 0.0,
  "presence_penalty": 0.0,
  "top_p": 1.0
}
```

### 响应（非流式）

```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "Qwen2.5-0.5B-Instruct",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello!"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 5,
    "total_tokens": 15
  }
}
```

### 响应（流式）

```
data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","created":1234567890,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{"role":"assistant","content":"Hello"},"finish_reason":null}]}

data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","created":1234567890,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{"content":"!"},"finish_reason":null}]}

data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","created":1234567890,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```

来源：https://docs.vllm.ai/en/latest/getting_started/quickstart.html

---

## `POST /v1/completions`

### 请求

```json
{
  "model": "string",
  "prompt": "string",
  "temperature": 0.7,
  "max_tokens": 256,
  "stream": false,
  "stop": null,
  "n": 1,
  "frequency_penalty": 0.0,
  "presence_penalty": 0.0,
  "top_p": 1.0
}
```

### 响应

```json
{
  "id": "cmp-xxx",
  "object": "text_completion",
  "created": 1234567890,
  "model": "Qwen2.5-0.5B-Instruct",
  "choices": [
    {
      "index": 0,
      "text": "Hello!",
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 5,
    "completion_tokens": 5,
    "total_tokens": 10
  }
}
```

来源：https://docs.vllm.ai/en/latest/getting_started/quickstart.html

---

## `GET /v1/models`

### 响应

```json
{
  "object": "list",
  "data": [
    {
      "id": "Qwen2.5-0.5B-Instruct",
      "object": "model",
      "created": 1234567890,
      "owned_by": "inference-service"
    }
  ]
}
```

---

## `GET /health`

### 响应

```json
{
  "status": "healthy",
  "engine": "vllm",
  "model": "Qwen2.5-0.5B-Instruct",
  "gpu_available": true
}
```

来源：https://docs.vllm.ai/en/latest/serving/health_checks.html

---

## `GET /metrics`

### 响应（Prometheus 格式）

```
# HELP vllm_num_requests_running Number of requests currently running
# TYPE vllm_num_requests_running gauge
vllm_num_requests_running 0

# HELP vllm_num_tokens_total Total number of tokens processed
# TYPE vllm_num_tokens_total counter
vllm_num_tokens_total 12345

# HELP vllm_gpu_cache_usage GPU cache usage fraction
# TYPE vllm_gpu_cache_usage gauge
vllm_gpu_cache_usage 0.85
```

来源：https://docs.vllm.ai/en/latest/metrics.html

---

## 错误响应格式

```json
{
  "error": {
    "message": "Error message",
    "type": "invalid_request_error",
    "code": 400
  }
}
```

| HTTP 状态码 | 错误类型 |
|-------------|---------|
| 400 | invalid_request_error |
| 401 | authentication_error |
| 404 | not_found_error |
| 422 | validation_error |
| 500 | internal_error |
| 503 | service_unavailable |

---

## 与 OpenAI API 的兼容性说明

| 兼容性项 | 状态 | 说明 |
|---------|------|------|
| `/v1/chat/completions` | 兼容 | vLLM 内置支持 |
| `/v1/completions` | 兼容 | vLLM 内置支持 |
| `/v1/models` | 兼容 | 需要自行实现 |
| 流式输出 | 兼容 | vLLM SSE 支持 |
| Token 计算 | 兼容 | vLLM 内置 |

---

Sources:
1. https://docs.vllm.ai/en/latest/getting_started/quickstart.html — vLLM Quickstart
2. https://docs.vllm.ai/en/latest/serving/health_checks.html — vLLM Health Checks
3. https://docs.vllm.ai/en/latest/metrics.html — vLLM Metrics

Risk of Staleness:
- vLLM 版本更新可能改变 API 行为

Out of Scope Kept:
- 未写认证机制
- 未写多模型路由
