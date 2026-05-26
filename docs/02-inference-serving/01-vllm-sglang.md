# vLLM 与 SGLang

vLLM 和 SGLang 经常被放在一起讨论，因为它们都站在“LLM 推理服务框架”这个位置上。
它们不是简单的 Python 包，也不是普通 HTTP wrapper，而是在试图回答同一个更难的问题：

> 当很多用户同时请求大模型时，系统如何高效、稳定、可观测地完成生成？

学习这两个框架时，不建议一开始就背功能表。
更好的方式是先抓住它们共同面对的基础问题，再理解它们各自更强调什么。

## 为什么 LLM Serving 不是包一层 HTTP

传统服务里，一个请求进来，业务函数执行，返回结果。
服务端主要关心：

- 路由
- 鉴权
- 数据库
- 缓存
- 日志
- 线程池或连接池

LLM serving 多了一层很特殊的复杂度：模型生成过程本身就很重。

一次请求不仅占用 CPU 和网络，还会占用：

- GPU 计算
- 显存
- KV cache
- 调度队列
- token 预算
- streaming 连接

更麻烦的是，请求之间的形态差异很大：

- 有的 prompt 很短
- 有的 prompt 很长
- 有的只生成十几个 token
- 有的要生成上千 token
- 有的要求 streaming
- 有的要求低延迟
- 有的可以为了吞吐多等一会儿

所以 LLM serving 框架的核心工作不是“把模型对象挂到 HTTP API 后面”。
真正难的是：

> 如何让不同长度、不同阶段、不同优先级的请求共享昂贵硬件，同时保持可接受的延迟和吞吐。

vLLM 和 SGLang 都是在这个问题空间里演化出来的。

## 先把两者放在同一张地图上

可以先用这张表建立分层直觉：

| 维度 | vLLM | SGLang |
| --- | --- | --- |
| 第一印象 | 高性能 LLM serving 引擎 | 生成程序与 serving 系统结合 |
| 学习重点 | KV cache、batching、OpenAI-compatible serving、吞吐和调度 | 生成流程表达、结构化调用、runtime 和 serving 协同 |
| 更容易联想到 | 把模型稳定高效地服务化 | 把复杂生成逻辑组织成可执行流程 |
| 不该误解为 | 只是一个 API server | 只是一个 prompt 编排库 |

这不是绝对边界。
两个项目都会不断演进，也都可能覆盖更多能力。
但对学习者来说，这个分层可以避免一开始就混乱。

## vLLM 更适合先理解成什么

vLLM 最适合先理解成：

> 围绕高吞吐、低延迟 LLM serving 做系统化优化的一条主线。

它常被提起，是因为它把很多原本很难自己实现的 serving 能力变得更容易落地。
学习 vLLM 时，最重要的是理解它为什么存在。

大模型推理服务会遇到几个硬问题：

1. KV cache 占用很大，管理不好会浪费显存。
2. 请求长度不一样，batching 很难做得稳定。
3. decode 是一步一步生成，调度粒度和传统 batch 推理不同。
4. 服务要兼容 OpenAI-style API，方便应用迁移。
5. 既要有吞吐，也要有可接受的首 token 延迟。

vLLM 的价值不是“有很多参数可以调”，而是它试图把这些问题组织成一个可用的 serving 引擎。

你可以带着几个问题去读 vLLM：

- 它如何处理 KV cache？
- 它如何把不同请求放到一起调度？
- 它如何暴露 OpenAI-compatible API？
- 它如何支持 streaming？
- 它如何让模型加载、服务启动和请求处理形成完整链路？

如果这些问题能回答清楚，你就已经抓住了 vLLM 的核心。

## SGLang 更适合先理解成什么

SGLang 可以先理解成：

> 更强调生成程序、推理执行和 serving runtime 协同的一条路线。

很多 LLM 应用不是简单的一问一答。
它们可能包含：

- 多轮推理
- 结构化输出
- 工具调用
- 多个模型调用组合
- 约束解码
- agent-like 流程
- 批量任务处理

如果每次都把这些逻辑散落在业务代码里，系统会很难维护。
SGLang 的学习价值在于：它提醒你“生成过程本身也需要工程表达”。

也就是说，它不只关心模型能不能服务化，还关心复杂生成流程如何被描述、执行和优化。

学习 SGLang 时，可以重点看：

- 它如何表达一次生成任务
- 它如何组织多步生成流程
- 它的 runtime 如何执行这些流程
- 它和底层 serving / cache / batching 的关系是什么
- 它适合哪些比单次 chat completion 更复杂的场景

不要把它简单理解为“另一个 vLLM”。
更好的理解是：它和 vLLM 有重叠，但它强调的问题侧重点不完全一样。

## 两者共同面对的核心问题

无论 vLLM 还是 SGLang，最终都逃不开这几个基础问题。

### 1. Prefill 和 Decode 怎么调度

prefill 处理输入上下文，decode 逐 token 生成。
这两个阶段的性能特征不同。

一个 serving 系统要决定：

- prefill 请求和 decode 请求如何排队
- 长 prompt 是否会拖慢短 prompt
- decode 阶段如何持续补 batch
- streaming 请求是否要优先保证稳定输出

所以你看到的“调度策略”，背后往往是在平衡 prefill 和 decode。

### 2. KV Cache 怎么管理

KV cache 是 LLM serving 的关键资源。
它能加速 decode，但会消耗显存。

当并发增加时，系统要管理很多请求的 cache。
这不是普通缓存，因为它和模型生成状态绑定，不能随便丢。

好的 serving 框架会尽量减少 cache 浪费，让显存可以承载更多有效请求。

### 3. Batching 怎么做

LLM 的 batching 不是把一批图片丢进模型这么简单。
因为每个请求在不同时间到达，输入输出长度也不同。

如果 batch 粒度太粗，短请求会等长请求。
如果 batch 太碎，GPU 利用率又不高。

现代 serving 框架通常会更动态地组织 batch，让请求在 decode 过程中不断加入或退出。

### 4. Streaming 怎么保证体验

用户通常不愿意等完整答案生成完才看到结果。
streaming 能让第一个 token 更早出现，也能让长答案更有“正在进行”的感觉。

但 streaming 会让服务端连接保持更久，也让中间状态更复杂。
所以框架要同时处理：

- token 生成
- SSE 或类似流式协议
- 连接断开
- 错误事件
- 计费和 usage
- 请求追踪

这就是为什么当前仓库的 `inference-service` 即使是 mock，也保留了 `stream=true`。

## 什么时候优先关注 vLLM

如果你的目标是理解“如何把一个模型稳定挂成服务”，可以优先关注 vLLM 这条线。

典型问题是：

- 我要启动一个 OpenAI-compatible endpoint
- 我要服务多个并发请求
- 我要看吞吐和延迟
- 我要理解 KV cache 和 batching
- 我要把应用从 mock endpoint 切到真实模型服务

对应到本项目，你可以看：

- [从学习型服务到真实 Serving Stack](/02-inference-serving/10-from-learning-service-to-real-serving-stack)
- [Serving 后端迁移](/12-production-migration/01-serving-backend-migration)
- [inference-service 项目页](/06-projects/01-inference-service)

这里的重点是服务化、接口兼容、运行稳定和性能观测。

## 什么时候优先关注 SGLang

如果你的目标是理解“复杂生成流程如何被工程化表达”，可以优先关注 SGLang 这条线。

典型问题是：

- 一次任务不止一个 prompt
- 需要多步推理或多段输出
- 需要约束输出格式
- 需要把生成流程批量执行
- 需要把 prompt / tool / model call 组织成更清晰的程序

对应到本项目，SGLang 这条线更适合作为后续生产迁移和进阶专题。
当前仓库还没有直接实现 SGLang runtime，但你可以先从 `eval-module` 和案例复盘理解“生成结果如何被组织、比较和复盘”。

## 一个简单类比

可以用这样一个不完全精确但有用的类比：

- vLLM 更像“把模型高效稳定地开成服务”
- SGLang 更像“把复杂生成过程写成更可执行、可优化的程序”

如果你要做的是“给应用提供一个兼容接口”，vLLM 的问题会更靠前。
如果你要做的是“把复杂 LLM 工作流组织起来”，SGLang 的问题会更靠前。

但真实系统里两者并不一定互斥。
一个团队可能同时需要：

- 高效的 serving backend
- 清晰的生成流程表达
- 平台层 gateway
- 评测和观测
- 发布门禁

这也是为什么本学习站把它们放在 AI Infra 的整体地图里，而不是孤立比较。

## 不要陷入“谁更好”的浅比较

新手很容易问：

```text
vLLM 和 SGLang 到底哪个更好？
```

这个问题通常太粗。
更好的问题是：

| 你真正关心什么 | 更应该看什么 |
| --- | --- |
| OpenAI-compatible serving 是否容易启动 | API server、模型加载、部署文档 |
| 高并发下吞吐如何 | batching、KV cache、调度和 benchmark |
| 首 token 延迟如何 | prefill、队列、调度策略 |
| 复杂生成流程怎么组织 | 生成程序表达、runtime、约束和工具调用 |
| 线上怎么观测 | metrics、events、trace、日志和 request id |
| 出问题怎么回滚 | gateway 路由、fallback、版本管理 |

比较框架时，一定要带着场景。
没有场景的比较，最后只会变成功能清单背诵。

## 和 Gateway 的关系

vLLM 或 SGLang 这类 serving backend 通常不应该直接承担所有平台职责。

真实系统里，经常会在前面加一层 gateway：

```text
Client -> AI Gateway -> Serving Backend -> Model
```

gateway 负责：

- 鉴权
- 外部模型名映射
- 限流
- fallback
- cache
- request id
- 日志和事件

serving backend 负责：

- 模型加载
- 推理执行
- KV cache
- batching
- streaming
- token usage

这就是 [AI Gateway Platform](/03-ai-gateway-platform/00-overview) 和 [Inference Serving](/02-inference-serving/00-overview) 要分成两章的原因。
它们不是重复，而是不同层。

## 和当前仓库怎么对应

当前 `projects/inference-service` 是学习型服务，不是真正的 vLLM 或 SGLang。
但它刻意保留了真实迁移需要的接口形态：

- `/v1/models`
- `/v1/chat/completions`
- `stream=true`
- `usage`
- `/metrics`
- `/events`
- `x-request-id`
- OpenAI-compatible engine adapter

你可以先用它理解：

1. 应用如何调用模型服务
2. gateway 如何代理它
3. streaming 如何被转发
4. metrics 和 events 如何记录
5. 后续如何替换成真实 OpenAI-compatible backend

等你切到真实 vLLM / SGLang endpoint 时，学习型服务可以逐步退到“接口契约样板”的位置。

## 学完这一页应该能回答

- 为什么 LLM serving 不是简单包一层 HTTP？
- vLLM 更强调哪类 serving 问题？
- SGLang 更强调哪类生成流程问题？
- 两者共同面对哪些 prefill、decode、cache、batching 难题？
- 为什么比较框架前必须先有场景？
- serving backend 和 AI Gateway 应该怎么分工？
- 当前仓库的 `inference-service` 为什么要保留 OpenAI-compatible 接口？

## 下一步

继续读：

- [Prefill、Decode、KV Cache](/01-llm-fundamentals/02-prefill-decode-kv-cache)
- [服务选型与取舍](/02-inference-serving/03-serving-tradeoffs)
- [vLLM](/02-inference-serving/04-vllm)
- [SGLang](/02-inference-serving/05-sglang)
- [从学习型服务到真实 Serving Stack](/02-inference-serving/10-from-learning-service-to-real-serving-stack)
