# 02. Inference Serving

> 本页解决：模型权重和 tokenizer 如何变成稳定、高效、可观测的模型服务。
> 读完能做：解释 `/v1/chat/completions`、`/v1/models`、streaming、metrics 和 request id 的 serving 契约。
> 关联代码：`projects/inference-service`、`projects/ai-gateway`。
> 验证命令：`curl -s http://localhost:8000/v1/models`。

这一组内容讲的是“模型服务本体”这一层。

更具体一点，它回答的是：

> 一个大模型已经有了权重和 tokenizer 之后，系统怎样把它稳定、高效、可观测地变成可调用服务？

这层离模型最近，也最容易被工具名词淹没。你会看到 vLLM、SGLang、Triton Inference Server、TensorRT-LLM、prefix caching、continuous batching、streaming、TTFT、ITL 等等。它们看起来像一串独立技术，但背后其实围绕同一个问题：如何在有限 GPU、显存、队列和延迟预算里，让很多请求同时生成 token。

![Inference Serving 执行层示意图](/images/articles/inference-serving-overview.jpg)

*图：Serving 层把权重、token、队列、缓存和流式输出组织成一个可调用、可观测、可替换的模型服务。*

## 先把 Serving 看成“执行契约”

一个 serving 服务对外至少要承诺几件事：

- 我支持哪些模型名
- 我接受什么请求格式
- 我如何返回普通响应和流式响应
- 我如何表达错误
- 我如何统计 usage
- 我如何暴露 health 和 metrics
- 我如何让上游追踪一次请求

内部是否使用 vLLM、SGLang、TensorRT-LLM 或 mock engine，可以逐步替换；但这些对外契约不能随便漂移。当前学习项目先把契约固定下来，就是为了后续替换真实后端时不重写整个系统。

所以读 serving 模块时，不要只问“真实模型在哪里”。更好的问题是：如果以后接入真实模型，哪些接口、错误语义、指标和事件应该保持稳定？

## Serving 层到底负责什么

Serving 层不是简单地“包一个 HTTP 接口”。真正的 serving 系统通常要处理：

- 模型加载和生命周期
- tokenizer 与请求预处理
- prefill / decode 执行调度
- KV Cache 管理
- batch 合并与拆分
- streaming 输出
- 错误映射
- metrics 与健康状态
- 模型列表和版本暴露
- 与 gateway 或上游平台的契约

当前仓库的 `projects/inference-service` 是学习型实现，所以它不会真的接 GPU 后端。但它保留了 serving 层对外最重要的形状：

- OpenAI-compatible 风格接口
- `/v1/chat/completions`
- `/v1/models`
- `/health`
- `/metrics`
- `/events`
- request id 传递
- streaming 与 non-streaming 两条路径
- mock engine 与 OpenAI-compatible engine 的边界

这让你可以先理解服务契约，再逐步想象内部替换成真实推理引擎。

## Serving 层的三条主线

这一章可以按三条主线理解。

### 1. 执行主线

执行主线关注模型如何生成 token。相关词包括 prefill、decode、KV Cache、batching、streaming、TTFT、ITL。

这条主线回答：

```text
一个请求如何占用模型执行资源？
为什么首 token 和后续 token 要分开观察？
为什么长上下文会改变资源压力？
```

### 2. 服务主线

服务主线关注模型如何被包装成稳定服务。相关词包括 OpenAI-compatible API、model list、health、metrics、error mapping、request id。

这条主线回答：

```text
上游系统如何可靠调用模型？
出错时如何知道发生了什么？
服务如何被 gateway 或监控系统理解？
```

### 3. 迁移主线

迁移主线关注从学习型 mock service 到真实 runtime 的路径。相关词包括 engine boundary、backend URL、runtime adapter、deployment stack。

这条主线回答：

```text
哪些代码只是学习替身？
哪些接口和证据边界应该保留？
真实 serving stack 接入时风险在哪里？
```

这三条线一起看，工具名词就不会那么散。

## Serving 和 Gateway 的边界

学习 AI Infra 时，一个常见混淆是把 serving 和 gateway 混成一层。

Serving 层更接近模型执行，关注：

- 模型能否加载
- 请求能否完成生成
- prefill/decode 如何调度
- GPU/显存是否扛得住
- 单模型服务的延迟、吞吐、错误

Gateway 层更接近平台治理，关注：

- 谁能访问
- 请求路由到哪里
- 多模型或多供应商如何 fallback
- rate limit 和 quota 怎么做
- cache、auth、审计和租户隔离怎么做
- 对外模型名如何映射到内部目标

两层都可能暴露 `/metrics`，两层都可能记录 request id，但问题域不一样。Serving 是“模型怎么执行”，Gateway 是“平台怎么治理调用”。

## 为什么 LLM Serving 比普通模型服务更复杂

普通 CV / embedding / ranking 模型服务通常更像“输入一个 batch，输出一个 batch”。LLM 生成有几个额外难点：

### 输出长度不确定

一个请求可能生成 20 个 token，也可能生成 2000 个 token。输出长度越长，请求占用执行状态越久。

### 请求会边生成边返回

Streaming 不是简单地更快返回一次响应，而是把一次请求拆成连续事件流。服务端必须处理连接生命周期、上游错误、中途断开、metrics 归因等问题。

### Prefill 和 Decode 负载不同

输入很长会影响 prefill，输出很长会影响 decode。两个阶段的计算形态不同，所以调度策略也不同。

### KV Cache 会成为资源瓶颈

并发不只是抢 GPU 算力，也会抢 KV Cache 显存。长上下文、多并发、长输出会让显存压力变得非常真实。

### Batch 不是固定形状

LLM 请求不断进入、不断完成。Continuous batching 的意义，就是在动态请求流里尽量让硬件保持忙碌，同时控制单个用户的延迟体验。

这些问题解释了为什么 vLLM、SGLang、TensorRT-LLM 这类工具会存在，也解释了为什么“自己写一个简单 FastAPI 包模型”很快会遇到天花板。

## 一个具体场景：为什么 FastAPI 包模型不够

假设你用一个简单 HTTP 服务包住模型，刚开始只有一个用户，效果不错。后来出现这些变化：

- 用户输入越来越长
- 有人要求 streaming
- 并发从 1 个变成几十个
- 某些请求输出特别长
- 上游 gateway 需要稳定 request id
- 你需要区分用户取消和模型失败
- 你要知道 TTFT、ITL 和 token usage

这时问题就不再是“HTTP endpoint 能不能返回文本”。你需要管理队列、执行状态、stream 生命周期、错误语义、指标和资源。专业 serving runtime 的价值就在这里。

学习项目不会直接实现这些复杂调度，但它会先把外部契约和观测入口留下来，让你能看懂真实 runtime 应该接到哪里。

## 推荐阅读顺序

1. [vLLM 与 SGLang](/02-inference-serving/01-vllm-sglang)
2. [Triton 与 TensorRT-LLM](/02-inference-serving/02-triton-tensorrt-llm)
3. [服务选型与取舍](/02-inference-serving/03-serving-tradeoffs)
4. [vLLM](/02-inference-serving/04-vllm)
5. [SGLang](/02-inference-serving/05-sglang)
6. [Cache 与 Prefix Caching](/02-inference-serving/06-cache-prefix-caching)
7. [Triton Inference Server](/02-inference-serving/07-triton-inference-server)
8. [TensorRT-LLM](/02-inference-serving/08-tensorrt-llm)
9. [Streaming、Batching、Metrics](/02-inference-serving/09-streaming-batching-metrics)
10. [从学习型服务到真实 Serving Stack](/02-inference-serving/10-from-learning-service-to-real-serving-stack)

前 3 页先建立工具地图和选型直觉，后 5 页分别展开具体工具与机制，最后 2 页把流式、批处理、指标和迁移路径串起来。

## 本模块与项目代码怎么对应

配合阅读：

- [inference-service 项目页](/06-projects/01-inference-service)
- [API Surface](/09-reference/05-api-surface)
- [验证矩阵](/09-reference/07-validation-matrix)

你可以重点观察几条线：

### 请求入口

`/v1/chat/completions` 展示了模型服务最核心的契约：接收 model 和 messages，返回 completion 结构。

### 模型发现

`/v1/models` 让上游系统知道当前服务能提供哪些模型名。这是后续 gateway 做模型映射的基础。

### 健康与指标

`/health` 和 `/metrics` 不只是“方便看状态”。它们让上游平台可以判断服务是否可用、是否退化、是否需要 fallback。

### 事件流

`/events` 和 request timeline 让你看到请求执行历史。真实 serving 栈里，这类结构会演化成更完整的 tracing、logs 和 dashboard。

### Engine 边界

mock engine 与 OpenAI-compatible engine 的边界提醒你：外部 API 契约可以先稳定，内部执行后端可以逐步替换。

## 读 `inference-service` 时可以这样走

第一次看代码时，建议按这个顺序：

1. 先找 server 入口，看路由有哪些。
2. 再看 request / response schema，看 API 契约是什么。
3. 再看 engine adapter，看执行后端被包在什么边界里。
4. 再看 streaming 路径，看普通响应和流式响应差异。
5. 最后看 metrics / events / timeline，看证据怎么落地。

这样你会先看到系统形状，再看内部细节。如果反过来先看 runtime 细节，很容易迷失在 mock 实现里。

## 读这一章时应该带着哪些问题

不要只问“哪个工具最快”。更好的问题是：

- 它解决的是执行层、服务托管层，还是平台治理层？
- 它主要优化 prefill、decode、cache、batching，还是部署管理？
- 它对输入长短、输出长短、并发形态有什么假设？
- 它如何暴露 metrics、health、model list 和错误？
- 它适合学习原型、单模型服务，还是多模型生产平台？
- 它和 gateway 的边界在哪里？

这些问题比简单排行榜更稳定。

## 学完这一章应该能做什么判断

学完后，你应该能比较清楚地判断：

- 为什么 OpenAI-compatible API 只是外壳，不是完整 serving 能力
- 为什么 vLLM/SGLang 更像 LLM runtime
- 为什么 Triton 更像通用模型服务托管层
- 为什么 TensorRT-LLM 更贴近 NVIDIA 优化执行栈
- 为什么 prefix caching 不是 response cache
- 为什么 streaming 会改变错误处理和 metrics 归因
- 为什么从 demo 迁移到真实 serving 时，要先保接口和观测

当这些判断形成后，你再看真实项目里的 serving 部署，就不会只看“启动命令是什么”，而会看系统边界是否清楚。

## 最小实践路线

建议按下面顺序动手：

1. 跑通 [第一次实操演练](/00-overview/04-first-walkthrough)。
2. 单独启动 `projects/inference-service`。
3. 分别调用 `/health`、`/v1/models`、`/v1/chat/completions`、`/metrics`。
4. 触发一次 unknown model，观察错误响应。
5. 触发一次 streaming 请求，观察事件输出。
6. 查看 request timeline，确认 request id 如何贯穿。
7. 回到本模块阅读 vLLM、SGLang、cache 和 metrics 页。

这样你会把抽象概念和真实接口连起来。

## 判断一个 Serving 方案时的检查表

以后你遇到一个真实 serving 方案，可以用这张表做第一轮判断：

| 问题 | 为什么重要 |
| --- | --- |
| 是否支持目标模型和 tokenizer | 决定能不能跑 |
| 是否支持 OpenAI-compatible API | 决定上游接入成本 |
| 是否暴露 health / metrics / model list | 决定能否被平台治理 |
| 是否支持 streaming | 决定交互体验和错误处理 |
| 是否有清楚的 request id / trace | 决定排障能力 |
| 是否能解释 TTFT / ITL / throughput | 决定性能分析能力 |
| 是否支持 prefix caching / batching | 决定吞吐和成本 |
| 是否容易回滚或替换 | 决定迁移风险 |

这个检查表比“哪个最快”更可靠。最快的方案如果不能观测、不能回滚、不能接入平台，也很难长期使用。

## 常见误区

### 误区一：Serving 就是 API Server

API Server 只是外层形状。真正难的是模型执行、调度、缓存、显存、streaming 和观测。

### 误区二：vLLM、SGLang、Triton、TensorRT-LLM 是同一类工具

它们有重叠，但站位不同。学习时要先分清执行 runtime、服务托管、优化库和平台治理。

### 误区三：只要模型能返回答案，Serving 就完成了

对学习 demo 可以这样开始；对真实系统，还要看并发、失败、延迟、指标、事件、回滚和版本。

### 误区四：吞吐越高就一定更适合线上

不一定。线上还要看 TTFT、ITL、尾延迟、失败率、成本、可运维性和团队熟悉度。

### 误区五：Gateway 可以替代 Serving 优化

Gateway 能做治理、路由、fallback 和 cache，但它不能替代模型执行层的调度和显存管理。
