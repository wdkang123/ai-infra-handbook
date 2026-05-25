# inference-service Stream SSE Samples v1

## Task ID: T1101
## Title: inference-service Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# inference-service Streaming SSE Samples

本文档定义 `/v1/chat/completions?stream=true` 场景下 SSE chunk 的完整序列样本，对应真实文件 `inference-service/tests/fixtures/sse_chat_sequence/`。

## Chunk 序列说明

每个 chunk：
- `Content-Type: text/event-stream`
- 每行以 `data: ` 开头
- JSON payload 后跟 `\n\n` 空行分隔符
- 最后一个 chunk 的 `choices[0].finish_reason` 为 `"stop"`
- 终止符为 `data: [DONE]\n\n`

---

## Sequence A: 短回答（3 tokens）

**对应文件：** `inference-service/tests/fixtures/sse_chat_sequence/sequence_a_short_answer.txt`

```
data: {"id":"chatcmpl-1704067200100","object":"chat.completion.chunk","created":1704067200,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{"role":"assistant","content":"4"},"finish_reason":null}]}

data: {"id":"chatcmpl-1704067200100","object":"chat.completion.chunk","created":1704067200,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```

---

## Sequence B: 多 token 回答

**对应文件：** `inference-service/tests/fixtures/sse_chat_sequence/sequence_b_multitoken.txt`

```
data: {"id":"chatcmpl-1704067200101","object":"chat.completion.chunk","created":1704067201,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{"role":"assistant","content":"The"},"finish_reason":null}]}

data: {"id":"chatcmpl-1704067200101","object":"chat.completion.chunk","created":1704067201,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{"content":" capital"},"finish_reason":null}]}

data: {"id":"chatcmpl-1704067200101","object":"chat.completion.chunk","created":1704067201,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{"content":" of"},"finish_reason":null}]}

data: {"id":"chatcmpl-1704067200101","object":"chat.completion.chunk","created":1704067201,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{"content":" France"},"finish_reason":null}]}

data: {"id":"chatcmpl-1704067200101","object":"chat.completion.chunk","created":1704067201,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```

---

## Sequence C: 带 system message 的流式

**对应文件：** `inference-service/tests/fixtures/sse_chat_sequence/sequence_c_with_system.txt`

```
data: {"id":"chatcmpl-1704067200102","object":"chat.completion.chunk","created":1704067202,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{"role":"assistant","content":"Paris"},"finish_reason":null}]}

data: {"id":"chatcmpl-1704067200102","object":"chat.completion.chunk","created":1704067202,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```

---

## Sequence D: streaming=false（非流式，不应出现 SSE）

**对应文件：** `inference-service/tests/fixtures/sse_chat_sequence/sequence_d_nonstreaming.json`

非流式请求返回普通 JSON，不返回 SSE：
```json
{
  "id": "chatcmpl-1704067200103",
  "object": "chat.completion",
  "created": 1704067203,
  "model": "Qwen2.5-0.5B-Instruct",
  "choices": [
    {
      "index": 0,
      "message": {"role": "assistant", "content": "Paris"},
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 18,
    "completion_tokens": 1,
    "total_tokens": 19
  }
}
```

---

## 字段规范

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | string | 格式 `chatcmpl-{timestamp_ms}` |
| `object` | string | 固定 `chat.completion.chunk` |
| `created` | int | Unix timestamp |
| `model` | string | 请求中的 model 值 |
| `choices[0].index` | int | 固定 `0` |
| `choices[0].delta` | object | `{content: string}` 或 `{}`（最后块） |
| `choices[0].delta.role` | string | 仅首块出现 `assistant` |
| `choices[0].finish_reason` | string \| null | 最后块为 `stop`，其余 `null` |

---

## SSE 格式要点

1. **每个 data line**：`data: ` + JSON 字符串 + `\n\n`
2. **空 delta**：最后 chunk 的 `delta` 为空对象 `{}`，此时 `finish_reason: "stop"`
3. **首块 role**：仅第一个 chunk 的 delta 包含 `role: "assistant"`，后续块仅含 `content`
4. **终止符**：`data: [DONE]\n\n`，无 JSON

---

Sources:
1. https://docs.vllm.ai/en/latest/serving/openai_compatibility_server.html — vLLM SSE format
2. https://platform.openai.com/docs/api-reference/chat/stream — OpenAI streaming

Risk of Staleness:
- SSE format is part of OpenAI API spec; stable since v1.0
