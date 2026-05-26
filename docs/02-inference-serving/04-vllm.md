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
