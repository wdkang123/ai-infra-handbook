# ai-gateway Proxy Response Samples v1

## Task ID: T1102
## Title: ai-gateway Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# ai-gateway Proxy Response Samples

本文档定义 ai-gateway 作为代理向下游 inference-service 转发后收到的响应样本，对应真实文件 `ai-gateway/tests/fixtures/proxy_responses/`。

## 代理行为说明

- ai-gateway 将收到的 `/v1/chat/completions` 请求透传到下游 `http://localhost:8000/v1/chat/completions`
- 响应结构与 inference-service 的 `ChatCompletionsResponse` 完全一致
- 流式响应时，ai-gateway 直接透传 SSE chunks，不修改 content

---

## Non-streaming Proxy Response

**对应文件：** `ai-gateway/tests/fixtures/proxy_responses/chat_completion_nonstreaming.json`

```json
{
  "id": "chatcmpl-1704067200100",
  "object": "chat.completion",
  "created": 1704067200,
  "model": "vllm-local",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "The capital of France is Paris."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 22,
    "completion_tokens": 8,
    "total_tokens": 30
  }
}
```

**流向：** `Client → [ai-gateway] → [inference-service] → [ai-gateway] → Client`

---

## Streaming Proxy Response（单个 chunk 透传）

**对应文件：** `ai-gateway/tests/fixtures/proxy_responses/sse_chunk_01.txt`

ai-gateway 收到的下游 SSE chunk，透传给 Client：

```
data: {"id":"chatcmpl-1704067200101","object":"chat.completion.chunk","created":1704067201,"model":"vllm-local","choices":[{"index":0,"delta":{"role":"assistant","content":"Paris"},"finish_reason":null}]}

data: {"id":"chatcmpl-1704067200101","object":"chat.completion.chunk","created":1704067201,"model":"vllm-local","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```

ai-gateway 在流式场景下的处理：
1. 设置 `X-Forwarded-For` / `X-Forwarded-Host` headers
2. 不修改 chunk 内容
3. 直接 `StreamingResponse` 透传

---

## Proxy Request to Downstream（转发时修改的字段）

ai-gateway 会在转发时对请求 body 做少量修改：

**Original from Client → ai-gateway：**
```json
{
  "model": "vllm-local",
  "messages": [{"role": "user", "content": "What is 2+2?"}],
  "temperature": 0.7
}
```

**Forwarded by ai-gateway → downstream：**
```json
{
  "model": "Qwen2.5-0.5B-Instruct",
  "messages": [{"role": "user", "content": "What is 2+2?"}],
  "temperature": 0.7
}
```

说明：
- `model` 字段会被路由配置中的 downstream 模型名替换（`vllm-local` → `Qwen2.5-0.5B-Instruct`）
- 其他字段原样透传

**对应文件：** `ai-gateway/tests/fixtures/proxy_responses/model_name_mapping.yaml`

```yaml
# routing: upstream model name → downstream model name
upstream_to_downstream_model:
  "vllm-local": "Qwen2.5-0.5B-Instruct"
  "llama3-8b": "meta-llama/Llama-3-8b"
```

---

## Proxy Response with Usage Info

**对应文件：** `ai-gateway/tests/fixtures/proxy_responses/chat_completion_with_usage.json`

```json
{
  "id": "chatcmpl-1704067200102",
  "object": "chat.completion",
  "created": 1704067202,
  "model": "vllm-local",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "4"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 1,
    "total_tokens": 13
  },
  "service_tier": "standard"
}
```

---

## Downstream Timeout Response

**对应文件：** `ai-gateway/tests/fixtures/proxy_responses/downstream_timeout_502.json`

当 downstream 超过 `timeout_ms` 无响应时：

```json
{
  "error": {
    "message": "Downstream inference service unavailable",
    "type": "server_error",
    "code": "502"
  }
}
```

---

## Downstream 404 Passthrough

**对应文件：** `ai-gateway/tests/fixtures/proxy_responses/downstream_404.json`

当 downstream 返回 404（未知模型）时，ai-gateway 透传：

```json
{
  "error": {
    "message": "Model not found: unknown-model",
    "type": "invalid_request_error",
    "code": "404"
  }
}
```

---

## Headers 处理

| Header | 处理方式 |
|---|---|
| `Authorization` | 保留，用于鉴权后透传到下游 |
| `Content-Type` | 保留 |
| `X-Forwarded-For` | 新增，记录原始 client IP |
| `X-Forwarded-Host` | 新增，记录原始 host |
| `X-Gateway-Request-Id` | 新增，追踪 ID |
| `X-RateLimit-Remaining` | 新增，速率限制剩余量（若启用） |

---

## 与 inference-service 契约对齐

ai-gateway 的 proxy response 格式与 `inference-service` 的 `ChatCompletionsResponse` 完全一致，对齐 T811 API contract。

| 字段 | 一致性 |
|---|---|
| `choices[0].message.role` | ✅ 一致 `"assistant"` |
| `choices[0].finish_reason` | ✅ 一致 `"stop"` |
| `usage` 结构 | ✅ 一致 |
| SSE chunk 格式 | ✅ 一致 |

---

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey proxy behavior
2. https://docs.vllm.ai/en/latest/serving/openai_compatibility_server.html

Risk of Staleness:
- Proxy passthrough behavior is project-internal; follows OpenAI API spec
