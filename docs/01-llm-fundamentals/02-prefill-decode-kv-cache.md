# Prefill、Decode、KV Cache

如果你只把大模型理解成“输入一段文字，然后输出一段文字”，后面看推理服务会很容易卡住。
因为真正影响服务性能、成本和体验的，不是“这次调用有没有返回”，而是这次调用在模型内部经历了哪几个阶段。

在 LLM serving 里，最重要的第一组工程直觉就是：

- 输入不是一次性“变成答案”的
- 生成通常可以拆成 prefill 和 decode 两段
- KV cache 是 decode 能持续高效进行的关键状态
- 很多 serving 框架的优化，本质上都在围绕这三件事做管理

这一页先不追求公式和论文级细节，而是建立你后面读 vLLM、SGLang、prefix caching、batching、streaming 时最需要的系统直觉。

## 一次请求到底发生了什么

假设用户发来这样一条消息：

```text
请解释一下什么是 AI Gateway，并给一个简单例子。
```

模型不会像传统函数一样直接“算出一整段答案”。
更接近真实过程的是：

1. 先读取整段输入，把输入中的 token 转成模型可以继续推理的内部状态。
2. 再从第一个输出 token 开始，一个 token 一个 token 地生成。
3. 每生成一个新 token，模型都要基于“输入上下文 + 已经生成的 token”继续决定下一个 token。

这就自然分成了两个阶段：

| 阶段 | 做什么 | 更容易被什么影响 |
| --- | --- | --- |
| Prefill | 处理完整输入上下文，建立后续生成所需的状态 | 输入长度、batch 大小、prompt 复杂度 |
| Decode | 一个 token 一个 token 地继续生成输出 | 输出长度、KV cache、调度、并发请求数 |

你可以把 prefill 想成“读题”，decode 想成“边想边写答案”。
读题阶段一次性处理较长文本；写答案阶段每次只写一点，但会持续很多步。

## Prefill：读完整个输入

prefill 阶段处理的是 prompt 中已有的 token。

如果输入很短，例如一句简单问候，prefill 很轻。
如果输入包含长文档、历史对话、检索结果、工具输出或几千 token 的系统提示，prefill 就会变重。

这解释了一个很常见的现象：

> 明明只让模型回答一句话，为什么请求一开始等了很久？

很可能不是 decode 慢，而是 prefill 在处理很长的上下文。

在真实系统里，prefill 变重通常来自：

- 聊天历史没有裁剪
- RAG 检索塞入太多片段
- system prompt 过长
- 工具调用结果被完整塞回上下文
- 多轮对话不断把旧内容追加进去

这也是为什么上下文管理不是“产品提示词问题”，而是基础设施问题。
平台层、网关层、评测层都要知道：输入 token 越长，prefill 压力越大，首 token 等待越可能变长。

## Decode：一个 token 一个 token 生成

decode 阶段负责生成新 token。

假设模型要输出：

```text
AI Gateway 是位于应用和模型服务之间的一层平台组件。
```

它不是一次性吐出整句话，而是依次生成：

```text
AI
 Gateway
 是
 位于
 应用
 ...
```

每一步都要基于前面的上下文继续判断下一个 token。
所以 decode 的成本和输出长度强相关。

这解释了另一个常见现象：

> prompt 不长，但回答很长时，为什么总耗时还是很高？

这通常不是 prefill 问题，而是 decode 要走很多步。

对用户体验来说，decode 还决定了 streaming 的手感：

- 第一个 token 什么时候出来，影响“有没有反应”
- 后续 token 间隔是否稳定，影响“流式输出顺不顺”
- 输出很长时，总 decode 步数会决定请求持续时间

所以后面你看 [TTFT、ITL、吞吐](/01-llm-fundamentals/03-ttft-itl-throughput) 时，会发现这些指标几乎都能回到 prefill / decode 两段来理解。

## KV Cache：为什么不能每一步都从头算

如果 decode 每生成一个 token，都重新处理一遍完整上下文，那会非常浪费。

例如输入有 2000 个 token，模型已经生成了 100 个 token。
现在要生成第 101 个输出 token。
如果完全从头算，模型需要反复处理前面 2100 个 token 的历史。
下一步生成第 102 个 token，又要再处理 2101 个 token。

这显然不可接受。

KV cache 的作用，就是把前面 token 在 attention 中已经计算出的关键中间状态保存下来。
后续 decode 时，模型可以复用这些状态，不必每一步都把过去上下文完整重算。

你可以先把它理解成：

> KV cache 是模型为了继续生成而保存的“上下文计算状态”。

它带来的好处很直接：

- decode 阶段不需要每一步重算全部历史
- 长上下文续写变得可行
- streaming 输出可以更稳定

但它也带来代价：

- KV cache 会占显存
- 请求越多，占用越多
- 上下文越长，占用越多
- 输出越长，cache 也会继续增长

所以 KV cache 本质上是在用空间换时间。
这也是 LLM serving 和传统 HTTP 服务非常不同的地方：请求结束前，它不是无状态的。

## 为什么 KV Cache 会变成 serving 难题

如果只有一个用户、一个请求，KV cache 看起来只是一个内部优化。
但真实服务里同时有很多请求，每个请求的输入长度、输出长度、到达时间都不同。

这时候 serving 系统要回答很多问题：

- 哪些请求的 cache 还要留着
- cache 放在哪里
- 显存不够时如何淘汰或迁移
- 多个请求如何一起 batch
- streaming 请求能不能和非 streaming 请求共存
- 长上下文请求会不会拖慢短请求

这些问题就是推理服务框架真正复杂的地方。

所以当你听到 vLLM、PagedAttention、prefix caching、continuous batching 这些词时，不要只把它们当成“性能优化名词”。
它们背后共同面对的是：

> 如何在很多请求同时生成时，管理好 token、cache、显存和调度。

## Prefix Caching 和它有什么关系

prefix caching 是一个很容易和 KV cache 混在一起的概念。

可以先这样区分：

- KV cache：一次请求内部，为后续 decode 保存上下文状态
- Prefix caching：多个请求之间，如果前缀相同，尽量复用已经处理过的前缀

例如很多请求都共享同一段 system prompt：

```text
你是一个严格、可靠的 AI Infra 学习助手……
```

如果每个请求都重新 prefill 这段相同前缀，就会浪费。
prefix caching 的目标就是识别这种可复用部分，减少重复 prefill。

这在真实系统里很有价值，因为很多应用都有固定模板：

- 固定 system prompt
- 固定工具说明
- 固定输出格式要求
- 固定角色设定
- 固定安全策略提示词

但 prefix caching 也不是魔法。
如果前缀稍微变化、上下文拼接顺序不稳定，命中率就会下降。
这就是为什么 prompt 模板管理、gateway 请求规范和 serving cache 策略会互相影响。

## 和 Batching 的关系

batching 是把多个请求放在一起执行，提高硬件利用率。

但 LLM 的 batching 比普通模型服务更麻烦。
因为每个请求可能处在不同阶段：

- 有的请求还在 prefill
- 有的请求已经开始 decode
- 有的请求快结束
- 有的请求会生成很长
- 有的请求只生成几个 token

如果调度不好，就会出现：

- 长请求拖住短请求
- 显存被长上下文占满
- streaming 输出不稳定
- GPU 利用率不高
- 用户等待时间波动很大

所以现代 LLM serving 框架往往会做更细的调度。
你后面看到 continuous batching、iteration-level scheduling 这类说法时，可以先把它们放回这个问题：

> 怎么让不同阶段、不同长度的请求共享硬件，而不是互相拖垮？

## 如何判断慢在哪一段

学习阶段最重要的不是立刻会调优，而是开始形成分段排查能力。

当一个请求慢时，不要只问：

```text
模型为什么慢？
```

要拆成：

| 现象 | 更可能的问题 |
| --- | --- |
| 等很久才出现第一个 token | prefill 重、排队久、batch 调度慢 |
| 第一个 token 出来后，后续输出很慢 | decode 慢、并发高、cache/调度压力大 |
| 长上下文请求明显拖慢 | prefill 和 KV cache 占用压力大 |
| 短请求也波动很大 | batching、队列、限流或资源隔离问题 |
| streaming 一顿一顿 | decode 调度不稳定或下游传输链路有阻塞 |

这张表不是为了替代真实 profiler，而是让你从“感觉慢”进入“知道该看哪一段”。

## 和当前仓库怎么对应

当前仓库里的 `inference-service` 是学习型实现，不会真的加载大模型，也不会真的管理 GPU KV cache。
但它保留了几个很重要的接口形态：

- `/v1/chat/completions`
- `stream=true`
- `usage`
- `x-request-id`
- `/metrics`
- `/events`

这些接口让你可以先练习服务边界：

1. 一次请求如何进入服务
2. 请求 ID 如何贯穿
3. streaming 如何表现
4. usage 如何记录 token 数
5. metrics 和 events 如何帮助复盘

等你理解了 prefill / decode / KV cache，再回来看这个学习型服务，就能明白它为什么要保留这些字段。
它不是为了假装自己是完整 serving 引擎，而是为了给后续迁移到真实 vLLM / SGLang / TensorRT-LLM 留出接口位置。

## 常见误区

### 误区 1：只看总耗时

总耗时当然重要，但它太粗。
同样是 8 秒，一个请求可能是 prefill 等了 6 秒、decode 用了 2 秒；也可能是 prefill 0.5 秒、decode 7.5 秒。
两者的优化方向完全不同。

### 误区 2：以为上下文越长一定越好

长上下文能容纳更多信息，但它也会带来 prefill 成本和 KV cache 压力。
工程上经常要做取舍：该放进上下文的才放，不该放的要摘要、裁剪或外部存储。

### 误区 3：把 streaming 当成性能优化

streaming 不一定减少总计算量。
它更多改善的是用户感知：先看到第一个 token，体验会更好。
如果 decode 本身很慢，streaming 只能让用户更早看到进度，不能让模型凭空算得更少。

### 误区 4：忽略 cache 的资源成本

KV cache 提升 decode 效率，但会消耗显存。
高并发、长上下文、长输出叠加时，cache 可能成为主要资源压力。

## 学完这一页应该能回答

- 为什么一次生成要拆成 prefill 和 decode？
- 为什么输入长会影响首 token 等待？
- 为什么输出长会影响总耗时？
- KV cache 为什么是用空间换时间？
- prefix caching 和 KV cache 有什么区别？
- batching 为什么在 LLM serving 里更复杂？
- 当前学习型 `inference-service` 为什么保留 streaming、usage、metrics 和 events？

## 下一步

继续读：

- [TTFT、ITL、吞吐](/01-llm-fundamentals/03-ttft-itl-throughput)
- [从请求到首个 Token](/01-llm-fundamentals/04-from-request-to-first-token)
- [vLLM 与 SGLang](/02-inference-serving/01-vllm-sglang)
- [Cache 与 Prefix Caching](/02-inference-serving/06-cache-prefix-caching)
