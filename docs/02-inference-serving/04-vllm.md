# vLLM

vLLM 最适合先理解成：

> 面向 LLM serving 的执行框架。

它不是简单的“把模型包成 HTTP 服务”的工具，也不是只提供一个 OpenAI-compatible API。
它真正重要的地方，是把 LLM 在线推理里的几个核心难题放进同一套运行时里处理：

- KV Cache 如何管理
- 请求如何排队和调度
- prefill 和 decode 如何协同
- 多个请求如何动态 batching
- streaming 如何和吞吐共存
- OpenAI-compatible API 如何暴露给调用方

如果只把 vLLM 理解成“一个能 serve 模型的命令”，会漏掉它最值得学的部分。

## 先用一个真实问题理解 vLLM

假设你维护一个问答产品，最开始只有少量内部用户。
直接调用一个模型接口时，一切都看起来正常。

后来流量上来以后，你开始遇到这些现象：

- 第一个用户很快，多个用户同时来时首 token 明显变慢。
- 有些长文档请求会让短问题也跟着变慢。
- GPU 看起来很忙，但 tokens/sec 并不稳定。
- streaming 能返回，但用户感觉输出一阵一阵地卡。
- 上下文一长，显存压力比预期更早出现。

这时问题已经不是“HTTP 服务有没有写好”，而是模型执行层如何调度在线请求。
vLLM 的学习价值就在这里：它把这些现象放进同一个运行时问题里，让你能从 token、cache、batch 和 scheduler 的角度理解瓶颈。

所以读 vLLM 时，不要先问：

```text
启动命令是什么？
```

更好的问题是：

```text
当很多请求同时生成 token 时，它如何管理显存、队列、cache 和输出节奏？
```

## 它在系统里处在哪一层

可以把 vLLM 放在这里：

```text
client / app
  -> ai-gateway
  -> inference-service
  -> vLLM runtime
  -> GPU / model weights
```

在这张图里：

- gateway 解决入口治理：auth、routing、rate limit、fallback。
- inference-service 解决服务边界：API、events、metrics、request id。
- vLLM 解决执行层：调度、KV Cache、batching、模型生成。

这三层不是互相替代关系。

## 为什么 vLLM 在学习路径里很关键

vLLM 的学习价值不只是“它流行”。
它能帮助你把很多抽象词变成真实系统行为：

| 概念 | 在 vLLM 里更容易观察到什么 |
| --- | --- |
| KV Cache | 显存和并发为什么会被 cache 影响 |
| Prefill / Decode | 首 token 和后续 token 为什么不是同一种阶段 |
| Continuous batching | 在线请求为什么不是固定 batch size |
| Streaming | 体验和调度为什么要同时考虑 |
| Throughput | tokens/sec 为什么比 request count 更关键 |
| Prefix caching | 相同前缀为什么可能降低 prefill 成本 |

所以 vLLM 是学习 LLM serving 的好主线。

## PagedAttention 应该怎么理解

PagedAttention 不要先背成一个“优化名词”。
更好的理解是：

> vLLM 用分页思路管理 KV Cache，让长上下文和多并发请求的缓存管理更高效。

LLM 生成时，每个请求都要保存前文 token 的 key/value 状态。
如果缓存管理方式低效，显存会被浪费，并发和吞吐都会受影响。

PagedAttention 背后的学习直觉是：

- KV Cache 是 serving 的核心资源。
- cache 不是普通内存缓存，它占 GPU 显存。
- 长上下文请求会带来明显资源压力。
- cache 管理方式会影响并发、吞吐和延迟。

这比记住论文细节更重要。

## 运行时里真正难的是“正在生成的请求”

传统 API 服务处理请求时，常常可以把一次请求看成短暂的输入输出。
LLM serving 不一样。
一个请求在生成完成前会一直占用运行时状态：

- prompt 已经 prefill 过。
- KV cache 还在显存里。
- decode 还要继续很多步。
- streaming 连接还没有结束。
- scheduler 还要决定下一轮 token 生成时它是否进入 batch。

这意味着 vLLM 这样的运行时不是只处理“请求进来”和“响应出去”两个时刻，而是在很多 token iteration 之间不断做资源分配。

你可以把在线 LLM serving 想成一个持续变化的队列：

```text
新请求进入 -> prefill -> 进入 decode 队列 -> 每轮生成一些 token -> 结束或继续等待下一轮
```

每一轮里，运行时都要面对几个取舍：

| 取舍 | 影响 |
| --- | --- |
| 多放一些请求进 batch | 吞吐可能提高，但单请求等待可能变长 |
| 优先短请求 | 交互体验更好，但调度策略更复杂 |
| 接受长上下文 | 能力更强，但 KV Cache 压力上升 |
| 保留更多 cache | 复用机会更多，但显存更紧 |

这也是为什么 vLLM 不是普通 Web 框架里的一个 handler。
它更像模型执行层的交通系统。

## Continuous Batching 为什么重要

训练时的 batch 往往是固定的。
在线 serving 不是这样。

在线请求会不断进入和退出：

- 有的请求正在 prefill。
- 有的请求正在 decode。
- 有的请求刚刚开始。
- 有的请求已经结束。
- 有的请求输出很短。
- 有的请求输出很长。

Continuous batching 的核心直觉是：

> 在线推理要在 token 生成过程中动态组织 batch。

这会带来一个重要取舍：
更好的 batching 通常能提高吞吐，但也可能影响某些请求的 TTFT 或 ITL。

## OpenAI-compatible API 只是外壳

很多人第一次接触 vLLM，是通过类似：

```text
POST /v1/chat/completions
```

这很方便，但它只是外壳。

真正要理解的是：

- API 请求如何进入 scheduler
- prompt 如何进入 prefill
- 生成过程如何进入 decode
- streaming chunk 如何返回
- usage 如何统计
- metrics 如何暴露
- 错误如何映射

所以学习 vLLM 时，不要停在“接口像 OpenAI”。
接口相似只是集成入口，运行时行为才是重点。

## 接入 vLLM 时应该保留哪些证据

如果未来把当前项目接到真实 vLLM 后端，最重要的不是让第一条请求成功，而是保留足够证据解释每条请求。

至少要保住这几类证据：

| 证据 | 为什么重要 |
| --- | --- |
| request id | 串起 gateway、inference-service 和 vLLM backend |
| model / served model name | 确认外部模型名最终落到了哪个执行目标 |
| prompt / completion token usage | 用于成本、限流和 eval 分析 |
| TTFT / queue / prefill / decode 信号 | 拆解“慢”到底慢在哪一段 |
| streaming start / end / error | 判断用户体感和协议边界 |
| backend error type | 区分连接失败、模型不存在、超时、OOM、运行时错误 |

如果只看到一段文本结果，而没有这些证据，真实后端接入以后会很难排障。

一个学习项目尤其要保留这些字段，因为读者需要看到“为什么这样设计”，而不是只看到“它能返回”。

## vLLM 和 Gateway 的关系

vLLM 不替代 gateway。

vLLM 更关注：

- 模型如何执行
- GPU 如何利用
- KV Cache 如何管理
- 请求如何 batching

gateway 更关注：

- 谁能调用
- 调用哪个外部模型名
- 是否超限
- 是否 cache/fallback
- 是否记录审计和 request timeline

真实系统里，常见关系是：

```text
业务应用 -> AI Gateway -> vLLM / inference backend
```

所以“用了 vLLM 是否还需要 gateway”的答案通常是：需要，只是职责不同。

## vLLM 和当前仓库怎么对应

当前仓库没有把 vLLM 直接嵌进默认路径。
这是刻意控制复杂度。

当前 `inference-service` 先表达：

- API 外壳
- request id
- usage
- metrics
- events
- streaming
- engine adapter

这些边界稳定后，vLLM 可以作为真实后端进入：

```text
inference-service engine adapter
  -> OpenAI-compatible vLLM backend
```

相关页面：

- [从学习型服务到真实 Serving Stack](/02-inference-serving/10-from-learning-service-to-real-serving-stack)
- [Serving 后端迁移](/12-production-migration/01-serving-backend-migration)

## 一个最小实践场景

学习 vLLM 时，不建议一开始追求所有高级参数。
更适合先做一个小实验：

1. 启动一个 vLLM OpenAI-compatible 服务。
2. 发送一条普通 chat completion。
3. 发送一条 `stream=true` 请求。
4. 观察首 token 等待和后续输出节奏。
5. 看 metrics 中 request/token 变化。
6. 构造共享 system prompt，观察 prefix caching 相关行为。

这个实验的目标不是跑出漂亮 benchmark，而是把 serving 行为看见。

## 应该观察哪些指标

学习阶段可以先观察：

| 指标 | 说明 |
| --- | --- |
| TTFT | 首 token 等待，常受 prefill、排队和 gateway 影响 |
| ITL | token 间隔，反映 decode 和调度流畅度 |
| prompt tokens | 输入上下文大小 |
| completion tokens | 输出长度 |
| running requests | 当前服务压力 |
| tokens/sec | 吞吐 |
| cache 相关指标 | prefix/KV cache 是否影响性能 |

不要只看 request per second。
LLM 负载必须看 token。

## 什么情况下不该急着优化 vLLM

vLLM 很重要，但不是所有问题都应该立刻归因到 vLLM。

如果你看到系统变慢，先确认：

| 现象 | 先看哪里 |
| --- | --- |
| 401、404、429 变多 | gateway 鉴权、路由、限流 |
| cache miss 变多 | gateway cache key、请求差异、TTL |
| 首 token 前等待很久 | gateway timeline、queue time、prefill token |
| 首 token 很快但后续卡 | decode、batch 调度、stream flush |
| 回答质量下降 | eval run、sample analysis、模型或 prompt 变更 |
| 只有某个业务方慢 | tenant quota、prompt 结构、上下文长度 |

换 runtime 或调参数之前，先用证据确认瓶颈在哪一层。
这也是本学习站反复强调 gateway、events、metrics、eval 的原因。
Serving runtime 是核心层，但它不是唯一层。

## 常见误区

### “vLLM 就是更快的模型推理”

太窄。
vLLM 的价值是把高效 serving 组织起来，包括调度、cache、batching、streaming 和 API。

### “用了 vLLM 就不用自己做服务边界”

不对。
你仍然需要考虑 gateway、错误格式、request id、metrics、eval 和发布流程。

### “vLLM 学完就等于 serving 学完”

不够。
还要理解 SGLang、Triton、TensorRT-LLM、gateway、observability 和 eval。

### “OpenAI-compatible API 一样，行为就一样”

不一定。
不同 runtime 的调度、cache、错误和指标语义可能不同。

## 学完应该能回答

读完这一页后，你应该能回答：

1. vLLM 在 AI Infra 系统里属于哪一层？
2. PagedAttention 为什么和 KV Cache 管理有关？
3. Continuous batching 为什么不是训练里的固定 batch size？
4. vLLM 和 gateway 为什么不是二选一？
5. 当前仓库如何为未来接入 vLLM 保留边界？

## 继续阅读

- [SGLang](/02-inference-serving/05-sglang)
- [Cache 与 Prefix Caching](/02-inference-serving/06-cache-prefix-caching)
- [Serving 后端迁移](/12-production-migration/01-serving-backend-migration)
- [TTFT、ITL、吞吐](/01-llm-fundamentals/03-ttft-itl-throughput)
