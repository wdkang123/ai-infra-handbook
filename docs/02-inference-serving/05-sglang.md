# SGLang

SGLang 也属于 LLM serving runtime，但它值得学习的地方，不只是“也能跑模型”。

它更鲜明地提醒你：

- 生成过程可以被编排。
- 请求之间可能共享大量前缀。
- 结构化生成不是接口层小功能，而会影响运行时设计。
- prefill 和 decode 可以继续拆开看。

如果说 vLLM 很适合建立标准 LLM serving 直觉，那么 SGLang 很适合继续建立：

> 共享前缀 + 结构化生成 + 生成流程编排的系统直觉。

## 它在系统里处在哪一层

可以把 SGLang 放在这里：

```text
client / app
  -> ai-gateway
  -> inference-service
  -> SGLang runtime
  -> GPU / model weights
```

它和 vLLM 一样，主要属于推理执行层。
它不替代 gateway，也不替代 eval 或 finetune。

它回答的是：

- 生成请求如何被执行？
- 共享前缀如何被复用？
- 结构化生成如何被表达？
- runtime 如何协调 prefill/decode 和调度？

## 为什么它经常和 vLLM 一起比较

因为二者都站在 LLM serving runtime 这一层。

它们都关心：

- latency
- throughput
- batching
- KV Cache
- streaming
- OpenAI-compatible integration

但学习时不要只问“谁更快”。
更有价值的问题是：

- 它们分别把什么问题放在设计中心？
- 它们如何处理共享前缀？
- 它们如何表达结构化生成？
- 它们如何暴露可观察信号？

这样比较才不会停在排行榜思维。

## RadixAttention 应该怎么理解

SGLang 常被提到的一个点是 RadixAttention。

学习阶段可以先这样理解：

> 它让共享前缀复用在运行时里变得更自然。

很多真实请求不是完全随机的。
例如：

- 多个请求共享同一个 system prompt。
- 业务模板固定，只是用户输入变化。
- few-shot 示例大量复用。
- agent loop 中前文上下文高度重复。
- 评测时同一 prompt template 被反复使用。

如果 runtime 能更好识别和复用这些共享前缀，就可能降低重复 prefill 成本。

这和 [Cache 与 Prefix Caching](/02-inference-serving/06-cache-prefix-caching) 强相关。

## 结构化生成为什么重要

很多工程场景里，调用方不想要一段随意文本，而是想要稳定结构：

```json
{
  "decision": "promote",
  "reasons": ["accuracy improved", "no critical regression"],
  "risk_level": "low"
}
```

如果输出结构不稳定，后续系统就会失败：

- JSON parse 失败
- 字段缺失
- schema 不匹配
- downstream workflow 卡住

所以 structured output 不是“体验增强”，而是工程可靠性的一部分。

SGLang 的学习价值之一，就是让你更自然地把结构化生成和 runtime 结合起来看，而不是只当作 prompt trick。

## Prefill / Decode 分离的直觉

SGLang 相关讨论里，经常会看到 prefill/decode disaggregation 这类思路。

学习阶段不需要马上实现。
你只要先建立直觉：

- prefill 处理已有上下文，通常受 prompt length 影响。
- decode 逐 token 生成，通常受输出长度和调度影响。
- 两个阶段的资源形态不同。
- 真实系统可能把它们分开优化。

这会帮助你理解为什么“一次生成请求”内部也不是单一黑盒。

## SGLang 更适合哪些学习场景

你可以优先用 SGLang 思考这些场景：

| 场景 | 为什么适合 |
| --- | --- |
| 大量共享 system prompt | 前缀复用价值高 |
| agent / workflow | 生成流程有结构 |
| JSON / schema 输出 | 结构化生成很重要 |
| few-shot 模板反复使用 | 前缀高度重复 |
| 复杂推理编排 | 不只是单轮文本生成 |

这不意味着 SGLang 只适合 agent。
更准确地说，它让这些场景的运行时特征更容易被看见。

## 和当前仓库怎么对应

当前仓库没有直接嵌入 SGLang。
但它已经把理解 SGLang 需要的服务边界留出来：

- 普通响应
- streaming
- request id
- metrics
- events
- gateway 与 inference 分层
- engine adapter 边界

未来如果接 SGLang，更合理的路径是：

```text
inference-service engine adapter
  -> OpenAI-compatible SGLang backend
```

然后继续保留：

- `/v1/chat/completions`
- `/health`
- `/metrics`
- `/events`
- `x-request-id`
- usage 字段

这样真实 runtime 进入系统，但学习站的外壳和观测不丢。

## 一个最小实践场景

后续你真实试 SGLang 时，可以做两个小实验。

### 实验一：共享前缀

1. 准备一个很长的 system prompt。
2. 连续发送多个只改变 user message 的请求。
3. 观察整体延迟和 TTFT 是否出现趋势变化。
4. 对比没有共享前缀的请求。

目标不是得出严格 benchmark，而是感受前缀复用对服务行为的影响。

### 实验二：结构化输出

1. 设计一个固定 JSON schema。
2. 让模型输出严格 JSON。
3. 检查 parse 成功率。
4. 观察失败时如何通过 retry、guard 或 schema 约束处理。

目标是理解 structured output 为什么是工程问题。

## 常见误区

### “SGLang 就是更适合 Agent”

这句话有来源，但太窄。
它确实对生成流程编排和共享前缀更有存在感，但不只属于 agent。

### “RadixAttention 就等于 prefix caching”

不完全一样。
可以把它理解成更有利于前缀复用的一种运行时组织方式，而 prefix caching 是系统行为层看到的复用效果之一。

### “学 SGLang 要先学完所有 DSL”

不用。
先理解共享前缀、结构化生成和 prefill/decode 分离，再下钻接口更稳。

### “SGLang 和 vLLM 必须二选一”

学习阶段不需要这么看。
更重要的是理解它们各自强调的系统问题。

## 学完应该能回答

读完这一页后，你应该能回答：

1. SGLang 在系统里属于哪一层？
2. 为什么共享前缀是 LLM serving 的重要工作负载特征？
3. 结构化生成为什么不是简单 UI 或 prompt 小技巧？
4. Prefill/decode 分离能帮助你理解什么工程问题？
5. 当前仓库未来接 SGLang 时应该保留哪些边界？

## 继续阅读

- [vLLM](/02-inference-serving/04-vllm)
- [Cache 与 Prefix Caching](/02-inference-serving/06-cache-prefix-caching)
- [Streaming、Batching、Metrics](/02-inference-serving/09-streaming-batching-metrics)
- [Serving 后端迁移](/12-production-migration/01-serving-backend-migration)
