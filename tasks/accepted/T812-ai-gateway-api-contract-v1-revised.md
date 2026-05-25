# ai-gateway API Contract v1 (Revised)

## Task ID: T812
## Task Title: ai-gateway API Contract Tighten
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T802-review.md，把 `/v1/completions`、`/v1/models` 从 MVP 必须降级为可选。

---

# ai-gateway API Contract v1 (Revised)

## 概述

本文档定义 ai-gateway 的代理 API 接口契约。

---

## 端点总览

| 端点 | 方法 | 说明 | MVP 必须 |
|------|------|------|---------|
| `/v1/chat/completions` | POST | 聊天补全代理 | **是** |
| `/v1/completions` | POST | 文本补全代理 | 否（后续扩展） |
| `/v1/models` | GET | 可用模型列表 | 否（后续扩展） |
| `/health` | GET | Gateway 健康状态 | **是** |
| `/metrics` | GET | Prometheus metrics | **是** |

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

### 请求头

| 头部 | 必须 | 说明 |
|------|------|------|
| `Authorization` | 是 | `Bearer <api_key>` |
| `Content-Type` | 是 | `application/json` |

### 响应

透传下游 inference-service 的响应，格式与 `/v1/chat/completions` 一致。

### 错误响应

| HTTP 状态码 | 错误类型 | 说明 |
|-------------|---------|------|
| 400 | `invalid_request_error` | 请求格式错误 |
| 401 | `authentication_error` | API Key 无效 |
| 404 | `not_found_error` | 模型未配置 |
| 422 | `validation_error` | 参数验证失败 |
| 429 | `rate_limit_error` | 超出限流 |
| 500 | `internal_error` | Gateway 内部错误 |
| 502 | `bad_gateway` | 下游服务不可用 |
| 503 | `service_unavailable` | Gateway 不可用 |

---

## `POST /v1/completions`（后续扩展）

> MVP 阶段不需要实现，后续按需扩展。

### 请求

```json
{
  "model": "string",
  "prompt": "string",
  "temperature": 0.7,
  "max_tokens": 256,
  "stream": false,
  "n": 1,
  "stop": null,
  "frequency_penalty": 0.0,
  "presence_penalty": 0.0,
  "top_p": 1.0
}
```

### 请求头

同 `/v1/chat/completions`。

---

## `GET /v1/models`（后续扩展）

> MVP 阶段不需要实现，后续按需扩展。

### 响应

透传下游 inference-service 的 `/v1/models` 响应，或聚合多个下游的模型列表。

```json
{
  "object": "list",
  "data": [
    {
      "id": "Qwen2.5-0.5B-Instruct",
      "object": "model",
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
  "version": "0.1.0",
  "upstream_services": {
    "vllm-local": "healthy"
  }
}
```

---

## `GET /metrics`

### 响应（Prometheus 格式）

```
# HELP ai_gateway_requests_total Total number of requests
# TYPE ai_gateway_requests_total counter
ai_gateway_requests_total{model="vllm-local",status="200"} 1234

# HELP ai_gateway_request_duration_seconds Request duration
# TYPE ai_gateway_request_duration_seconds histogram
ai_gateway_request_duration_seconds_bucket{model="vllm-local",le="1.0"} 1000

# HELP ai_gateway_tokens_total Total tokens processed
# TYPE ai_gateway_tokens_total counter
ai_gateway_tokens_total{model="vllm-local"} 567890
```

---

## 请求转发行为

### 路由匹配

| 请求 model 参数 | 路由到下游 |
|---------------|-----------|
| `vllm-local` | `http://localhost:8000/v1` |
| `openai-gpt4` | `https://api.openai.com/v1` |
| 未配置 model | 返回 404 |

### Header 转发

| Header | 处理方式 |
|--------|---------|
| `Authorization` | 转发到下游（如下游需要） |
| `Content-Type` | 转发 |
| `X-Request-ID` | 生成并传递 |
| `X-RateLimit-*` | 返回限流信息 |

### Body 转发

- 直接透传，不修改 body
- 移除下游不支持的参数（如 `user`）

---

## 与 OpenAI API 的兼容性说明

| 兼容性项 | 状态 | 说明 |
|---------|------|------|
| `/v1/chat/completions` | 兼容 | 透传，MVP 核心 |
| `/v1/completions` | 兼容（可选） | 透传，后续扩展 |
| `/v1/models` | 兼容（可选） | 透传或聚合，后续扩展 |
| 流式输出 | 兼容 | SSE 透传 |
| Token 计算 | 部分 | 返回下游的 usage |

---

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway
2. https://github.com/BerriAI/litellm — LiteLLM
3. https://docs.litellm.ai/docs/proxy_router — LiteLLM Router

Risk of Staleness:
- 下游 API 变化可能需要调整转发逻辑

Out of Scope Kept:
- 未写多租户路由
- 未写成本感知路由
