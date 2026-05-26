# Streaming、Batching、Metrics

推理服务不是“收到请求，调用模型，返回文本”这么简单。
一旦进入真实服务场景，你会同时面对三类问题：

- 用户希望尽快看到回答。
- 系统希望硬件不要空转。
- 维护者希望问题能被观察和解释。

这三类问题分别对应：

- streaming
- batching
- metrics

它们看似是三个主题，其实是同一个 serving 系统的三个侧面。

## 三者分别站在哪个视角

| 主题 | 主要视角 | 核心问题 |
| --- | --- | --- |
| Streaming | 用户体验和协议边界 | 结果能不能边生成边返回 |
| Batching | 执行效率和资源利用 | 多个请求如何一起组织执行 |
| Metrics | 运行状态和维护 | 服务整体是否健康、负载如何 |

如果只看 streaming，你容易只关注前端体感。
如果只看 batching，你容易只关注吞吐。
如果只看 metrics，你可能知道系统变差，却不知道用户怎么感知。

把三者放在一起，才更像在理解“服务”。

## Streaming：把生成过程暴露给用户

streaming 回答的是：

> 模型还在生成时，服务能不能把已经生成的部分先交给客户端？

在 chat 场景里，这通常表现为 Server-Sent Events 或类似 chunk 流。

它带来的直接变化是：

- 用户不用等完整回答结束。
- TTFT 变得可观察。
- 后续 token 的节奏变得可感知。
- 中途错误需要有协议表达。
- gateway 必须能正确透传流。

所以 streaming 不只是 UI 体验功能。
它会影响 API 设计、代理层实现、错误格式和测试方式。

## Streaming 不等于总耗时更短

这是一个常见误区。

streaming 让用户更早看到部分结果，但不一定让模型更快生成完整答案。

例如：

| 模式 | 首 token | 完整答案 |
| --- | --- | --- |
| 非 streaming | 用户看不到 | 8 秒后一次性返回 |
| streaming | 1 秒看到首 token | 8 秒后结束 |

总时间可能一样，但体感完全不同。
因此评估 streaming 时要同时看：

- TTFT
- ITL
- 总耗时
- 中途错误
- 客户端取消

## Streaming 的错误处理更难

普通 JSON 响应里，服务可以在返回前决定状态码和错误体。
streaming 一旦开始发送 chunk，就很难像普通响应那样“改状态码”。

这会带来几个工程问题：

- 上游开始输出后失败，gateway 怎么表达？
- fallback 是否只能发生在首 chunk 之前？
- 客户端如何区分正常结束和错误结束？
- metrics 应该如何记录部分成功？
- request timeline 如何记录流式中断？

当前 `ai-gateway` 的 stream fallback 就体现了这个边界：如果上游在首 chunk 前失败，还可以尝试 fallback；如果已经发出 chunk，再切换上游就会让输出语义变得混乱。

## Batching：把多个请求组织成高效执行

batching 回答的是：

> 多个请求如何一起执行，才能提高硬件利用率？

GPU 擅长并行计算。
如果每个请求都孤立执行，硬件可能无法被充分利用。

LLM serving 里的 batching 比普通模型服务更复杂，因为请求长度和生成进度不同：

- 有的请求 prompt 很长。
- 有的请求输出很短。
- 有的请求正在 prefill。
- 有的请求正在 decode。
- 有的请求已经结束。
- 有的请求刚刚进入队列。

因此，LLM batching 不只是“攒够 N 个请求一起跑”。
它还涉及调度、KV Cache、prefill/decode 分离、显存管理和公平性。

## Batching 为什么会影响体验

batching 通常有利于吞吐，但可能影响单请求体感。

例如，为了提高 batch utilization，系统可能让新请求等一小段时间。
这有助于整体吞吐，但会增加某些请求的 TTFT。

另一个例子是大请求和小请求混在一起。
如果调度不合理，小请求可能被长上下文请求拖慢。

所以 batching 的取舍是：

| 目标 | 可能收益 | 可能代价 |
| --- | --- | --- |
| 提高吞吐 | 更高 GPU 利用率、更低单位成本 | TTFT 可能上升 |
| 降低单请求等待 | 更好交互体验 | 硬件利用率可能下降 |
| 公平调度 | 避免小请求被饿死 | 调度复杂度上升 |
| 长上下文支持 | 能处理更复杂任务 | KV Cache 和显存压力上升 |

真实 serving runtime 的价值，很大一部分就在这些调度策略里。

## Metrics：让服务行为可观察

metrics 回答的是：

> 最近这套服务整体处于什么状态？

对推理服务来说，最基本的 metrics 包括：

- 当前 running requests
- 总请求数
- 成功请求数
- 失败请求数
- prompt tokens total
- completion tokens total
- total tokens

更真实的 serving 系统还会继续看：

- TTFT 分布
- ITL 分布
- queue time
- prefill time
- decode time
- tokens/sec
- batch size
- GPU utilization
- KV Cache 使用率
- OOM / eviction / timeout

学习阶段不必一次性实现所有指标，但要知道这些指标分别回答什么问题。

## 三者如何一起解释一个问题

假设用户反馈：

> 最近回答开头很慢，但开始后输出还算顺。

你可以这样拆：

- streaming 告诉你：首 token 晚、后续 token 还可以。
- metrics 告诉你：running requests 是否高、prompt token 是否上升、失败率是否变化。
- batching 视角告诉你：是否为了吞吐让请求等 batch，或者长上下文请求占用了资源。

再结合 gateway events，你还可以看是否 cache miss、fallback 或上游健康变差。

这个例子说明：单独看任何一个词都不够。
用户体验、执行调度和运行指标需要放在一起。

## 当前仓库怎么表达

当前仓库没有真实 GPU batching scheduler，但已经表达了学习所需的边界。

### Inference Service

相关文件：

```text
projects/inference-service/src/inference_service/server.py
projects/inference-service/src/inference_service/runtime.py
projects/inference-service/src/inference_service/engines.py
```

它提供：

- 普通 chat completion
- streaming chat completion
- `/metrics`
- `/events`
- request timeline
- token usage 估算

你可以用它理解：服务层如何把响应、事件和指标暴露出来。

### Gateway

相关文件：

```text
projects/ai-gateway/src/ai_gateway/server.py
projects/ai-gateway/src/ai_gateway/router.py
projects/ai-gateway/src/ai_gateway/runtime.py
```

它提供：

- streaming 透传
- fallback-before-first-chunk 的边界
- cache hit/miss
- upstream health
- gateway metrics
- gateway events

你可以用它理解：代理层不是透明管道，streaming 会让边界更敏感。

## 学习时可以怎么观察

建议做三类实验：

### 1. 普通响应 vs Streaming

观察：

- 响应格式是否不同
- header 中 `x-request-id` 是否存在
- metrics 是否增加
- events timeline 是否记录 stream 标记

### 2. Cache / Fallback 对 Streaming 的影响

观察：

- 非 streaming 请求是否能 cache hit
- streaming 请求是否直接透传
- fallback 是否发生在首 chunk 前
- `x-fallback-used` 或 events 如何记录路径

### 3. Token Usage 对 Metrics 的影响

观察：

- `usage.prompt_tokens`
- `usage.completion_tokens`
- `/metrics` 中 token counters
- 不同 prompt 长度对计数的影响

这些实验能把概念直接接到当前仓库。

## 常见误区

### “Streaming 只是前端效果”

不止。
它会改变协议、代理、错误处理、测试和观测方式。

### “Batching 是框架内部黑盒，不用理解”

不对。
即使你不实现 scheduler，也必须理解它为什么影响 TTFT、ITL、吞吐和成本。

### “Metrics 部署后再补就行”

风险很大。
没有 metrics，你很难判断改动是让系统变好还是只是“还能跑”。

### “请求数就是负载”

LLM 里请求数不够。
一个短请求和一个长上下文请求，对系统压力完全不同，必须看 token 维度。

### “Streaming 成功就代表模型服务健康”

不一定。
streaming 可能中途失败，也可能首 chunk 很慢、后续平滑，或者首 chunk 快但后续卡顿。

## 学完应该能回答

读完这一页后，你应该能回答：

1. streaming 为什么既是体验问题，也是服务边界问题？
2. batching 为什么可能提高吞吐但伤害 TTFT？
3. metrics 为什么必须同时看 request 和 token？
4. streaming 中途失败为什么比普通响应更复杂？
5. 当前仓库如何用 inference-service 和 gateway 表达这三类问题？

## 继续阅读

- [从请求到首个 Token](/01-llm-fundamentals/04-from-request-to-first-token)
- [TTFT、ITL、吞吐](/01-llm-fundamentals/03-ttft-itl-throughput)
- [服务选型与取舍](/02-inference-serving/03-serving-tradeoffs)
- [Streaming、错误与上游健康](/03-ai-gateway-platform/04-streaming-errors-upstream-health)
