# Serving 与 Gateway 输出证据

## 这一页看什么

这一页整理 `inference-service` 和 `ai-gateway` 最重要的输出证据。

你不需要记住所有字段，但要能回答：

- 请求有没有真正进服务
- 请求有没有经过 gateway
- gateway 选择了哪个 upstream
- request id 是否贯穿
- streaming 是否按 SSE 结束
- metrics 和 events 是否能解释这次请求

## 服务健康证据

先看 inference-service：

```bash
curl -s http://localhost:8000/health
```

你应该关注：

| 字段 | 说明 |
| --- | --- |
| `status` | 服务是否认为自己可用 |
| `service` | 当前服务身份 |
| `engine_type` | 当前使用 mock 还是 OpenAI-compatible adapter |
| `models` | 当前暴露哪些模型 |

再看 gateway：

```bash
curl -s http://localhost:8080/health
```

你应该关注：

| 字段 | 说明 |
| --- | --- |
| `status` | gateway 顶层状态 |
| `upstream_services` | gateway 对下游服务的最小探测结果 |
| `models` | gateway 对外暴露的模型名 |

如果 gateway 是 `degraded`，优先看 `upstream_services`，不要直接猜 gateway 自己坏了。

## 普通请求证据

普通 completion 请求适合验证同步路径：

```bash
curl -i -X POST http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer dev-gateway-key-1" \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: demo_request_1" \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"hello"}]}'
```

重点看响应头：

| Header | 说明 |
| --- | --- |
| `x-request-id` | 请求 id 是否被保留或生成 |
| `x-upstream-model` | gateway 最终选择的上游模型 |
| `x-fallback-used` | 是否发生 fallback |
| `x-cache` | cache 状态，可能是 `bypass`、`hit`、`miss` |

重点看响应体：

| 字段 | 说明 |
| --- | --- |
| `id` | completion id |
| `model` | 返回结果对应的模型名 |
| `choices` | 生成内容 |
| `usage.prompt_tokens` | 输入 token 估算 |
| `usage.completion_tokens` | 输出 token 估算 |

这里的 token 是学习型估算，不是真实 tokenizer。它的价值是让你看到 usage 边界，而不是证明模型成本精确。

## Streaming 证据

Streaming 请求适合验证 SSE 路径：

```bash
curl -sN -X POST http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer dev-gateway-key-1" \
  -H "Content-Type: application/json" \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"stream"}],"stream":true}'
```

正常输出应该包含：

```text
data: {...}

data: [DONE]
```

你要关注两件事：

1. 是否按 `data:` 逐块输出
2. 是否以 `[DONE]` 结束

如果 streaming 中途失败，HTTP status 可能已经发出，错误更可能出现在 SSE event 里。这个边界可以配合 [Streaming、错误路径、Upstream Health](/03-ai-gateway-platform/04-streaming-errors-upstream-health) 理解。

## Metrics 证据

inference metrics：

```bash
curl -s http://localhost:8000/metrics
```

关注：

| 指标 | 说明 |
| --- | --- |
| `vllm_num_requests_total` | 请求数是否增加 |
| `vllm_prompt_tokens_total` | prompt token 是否累计 |
| `vllm_completion_tokens_total` | completion token 是否累计 |

gateway metrics：

```bash
curl -s http://localhost:8080/metrics
```

关注：

| 指标 | 说明 |
| --- | --- |
| `ai_gateway_requests_total` | gateway 请求数 |
| `ai_gateway_upstream_requests_total` | 上游请求数 |
| `ai_gateway_fallback_attempts_total` | fallback 尝试 |

metrics 适合回答“系统整体发生了多少事”，不适合回答“一条请求内部经历了什么”。单请求复盘要看 events。

## Events 证据

查 gateway 事件：

```bash
curl -s "http://localhost:8080/events?request_id=demo_request_1"
```

你应该能看到类似事件类型：

| event_type | 含义 |
| --- | --- |
| `request_received` | gateway 收到请求 |
| `upstream_attempt` | 尝试调用上游 |
| `fallback_attempt` | 尝试 fallback |
| `fallback_success` | fallback 成功 |
| `request_success` | 请求成功结束 |
| `auth_failed` | 鉴权失败 |
| `route_not_found` | 模型路由不存在 |
| `rate_limited` | 触发限流 |

如果你只想看聚合：

```bash
curl -s "http://localhost:8080/events/summary"
curl -s "http://localhost:8080/events/failures"
```

`summary` 适合看整体分布，`failures` 适合先判断失败大概来自鉴权、路由、限流还是上游。

## Request timeline 证据

单请求复盘时优先用：

```bash
curl -s "http://localhost:8080/events/requests/demo_request_1"
```

timeline 能把一条请求按时间串起来。

一条健康请求通常应该能解释：

1. 什么时候进入 gateway
2. 请求的外部模型名是什么
3. gateway 选择了哪个 upstream
4. 有没有 cache 或 fallback
5. 最后怎么结束

如果 timeline 缺失，先确认你是否传了 `X-Request-ID`，或者请求是否在事件保留窗口内。

## 常见错误怎么读

| 现象 | 优先看什么 | 可能含义 |
| --- | --- | --- |
| `401` | Authorization header | 没有 token 或 token 格式错误 |
| `404` | requested model | gateway 找不到模型路由 |
| `429` | rate limit event | 触发限流 |
| `502` | upstream attempt / inference error | 下游调用失败 |
| streaming 没有 `[DONE]` | SSE error event | 流式请求中途失败 |
| metrics 不变 | 是否真的打到对应服务 | 请求可能没经过这一层 |

## 复盘模板

```text
请求 id：
入口服务：
HTTP 状态：
关键 header：
metrics 是否变化：
timeline 中的关键 event：
这次请求证明了：
这次请求不能证明：
下一步要验证：
```

## 关联阅读

- [inference-service](/06-projects/01-inference-service)
- [ai-gateway](/06-projects/02-ai-gateway)
- [请求失败排查案例](/11-case-studies/01-request-incident-walkthrough)
- [API Surface 速查](/09-reference/05-api-surface)
