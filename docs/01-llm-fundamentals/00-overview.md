# 01. LLM Fundamentals

这一组内容解决的是一个很基础、但会反复影响后面所有工程判断的问题：

> 当我们说“把大模型接进系统”，系统里真正被处理、调度、缓存、计费、观测和评测的对象是什么？

很多学习资料会从 Transformer、Attention、论文结构开始讲。那些当然重要，但这个学习站的目标不是先训练你成为算法研究者，而是帮助你建立 AI Infra 工程直觉。所以这一章会刻意从工程侧切入：一次请求进来后，模型看见了什么，服务层做了什么，指标为什么这样定义，成本为什么这样产生。

如果这一章没站稳，后面的很多名词会很容易变成散点：

- vLLM / SGLang 为什么强调 prefill、decode、KV Cache
- gateway 为什么要关心 token、streaming、request id
- evaluation 为什么不能只看“回答看起来不错”
- finetune 为什么要记录 dataset、run、checkpoint 和 export
- observability 为什么要同时看指标、日志和 trace

这一章的价值，就是把这些后续章节背后的共同变量先讲清楚。

## 这一章不追求什么

这里不会把 LLM 基础讲成完整深度学习课程。你暂时不需要先掌握：

- Transformer 每一层矩阵乘法的推导
- Attention 的完整公式展开
- 分布式训练通信细节
- CUDA kernel 优化
- 论文级别的模型结构演进

这些内容后续当然可以继续学，但它们不是第一次读这个项目最紧迫的入口。

这里更关心几个工程问题：

- 请求进入系统后会被拆成什么单位
- context 为什么决定能力边界和成本边界
- prefill 和 decode 为什么会形成两种完全不同的负载
- KV Cache 为什么会影响显存、延迟和并发
- TTFT、ITL、throughput 为什么是 serving 里最常见的性能语言

换句话说，这一章不是让你背概念，而是让你之后看到代码、指标和工具时，知道它们为什么存在。

## 贯穿全站的几个基础变量

### Token 是共同计量单位

LLM 系统里最常见的工程错觉是：请求就是一次 HTTP 调用。

从 API 层看，这是对的。但从模型执行层看，真正被模型处理的是 token。prompt 会被 tokenize，输出会逐 token 生成，计费会按 token 统计，context window 会按 token 限制，缓存也围绕 token 序列生效。

所以你后面看任何 serving 或 gateway 设计，都要问：

- 输入 token 有多少
- 输出 token 有多少
- 是否需要 stream
- 是否有重复 prefix
- 是否会撑满 context
- 是否会导致某些请求占用太久

这比只看“请求数”更接近真实瓶颈。

### Context 是能力边界，也是成本边界

Context window 经常被介绍成“模型一次能看多少 token”。这只是第一层意思。

从工程角度看，context 还意味着：

- 更长输入会增加 prefill 计算
- 更长对话会占用更多 KV Cache
- 更长上下文会放大延迟和显存压力
- 更长 prompt 不一定带来更好回答
- prompt 模板设计会影响 cache 命中机会

所以真实系统不会只问“模型支持多长 context”。更常见的问题是：

- 当前业务是否真的需要这么长 context
- 哪些系统提示词可以稳定下来
- 哪些历史消息可以压缩或摘要
- 哪些文档应该进入 RAG，而不是全部塞进 prompt
- 超长输入失败时，用户看到的错误是否可理解

Context 是能力，也是账单和延迟。

### Prefill 与 Decode 是两段不同的工作

一次生成通常可以粗略拆成两段：

- prefill：处理已有输入上下文
- decode：逐步生成新 token

这两个阶段的压力不同。Prefill 更像一次性吃下输入上下文，decode 更像连续、小步、受前序状态影响地生成输出。

这解释了为什么 serving 系统会关心：

- 首 token 延迟，也就是 TTFT
- token 间延迟，也就是 ITL
- 输入长短对首 token 的影响
- 输出长短对请求占用时长的影响
- batch 调度为什么不能照搬普通 Web 服务思路

如果你只把 LLM 服务理解成“调用一次函数，返回一段文本”，就很难理解后面的性能优化。

### KV Cache 是状态，而不是普通缓存

KV Cache 容易被误解成“把回答缓存起来”。不对。

KV Cache 保存的是模型在前文 token 上已经计算出的中间状态。它的作用是让模型在生成后续 token 时，不必反复重算所有历史上下文。

它带来的直觉是：

- 长上下文会占用更多显存状态
- 并发请求不是只抢算力，也抢显存
- streaming 请求会在一段时间内持续占用资源
- prefix caching 能优化一部分重复前缀场景
- cache 命中、淘汰和内存布局会成为 serving runtime 的核心能力

这也是为什么 vLLM、SGLang、TensorRT-LLM 这些工具不只是 HTTP server，它们都在处理模型执行过程中的状态管理问题。

## 推荐阅读顺序

1. [模型、Token、Context](/01-llm-fundamentals/01-model-token-context)
2. [Prefill、Decode、KV Cache](/01-llm-fundamentals/02-prefill-decode-kv-cache)
3. [TTFT、ITL、吞吐](/01-llm-fundamentals/03-ttft-itl-throughput)
4. [从请求到首个 Token](/01-llm-fundamentals/04-from-request-to-first-token)

这个顺序是有意设计的：

- 先知道模型处理什么
- 再知道生成过程分成哪些阶段
- 再知道指标如何对应阶段
- 最后把一次请求完整串起来

不要急着跳到工具页。工具页会更好看、更像工程，但工具背后的取舍都藏在这一章。

## 与当前仓库代码怎么对应

当前仓库里的 `projects/inference-service` 是一个学习型模型服务。它没有真的加载大模型权重，而是用 mock engine 模拟 OpenAI-compatible 的 chat completion 行为。

这不是偷懒，而是为了先让你看清楚接口和工程形状：

- 请求里有 model 和 messages
- 响应里有 completion id、message、usage
- streaming 会持续产生事件
- metrics 会记录请求和错误路径
- unknown model 会走明确错误
- engine error 会映射为上游失败

这些结构都和这一章的基础概念有关。

你可以把当前 mock service 看成一张低成本剖面图：它不会展示 GPU 内部细节，但会展示一个模型服务对外必须形成的契约。

## 学完这一章应该能回答的问题

读完这一组内容后，你不一定能手写推理引擎，但应该能解释：

- 为什么 token 数比字符数更重要
- 为什么长 prompt 会影响延迟和成本
- 为什么 TTFT 和 ITL 不是同一个指标
- 为什么 streaming 不等于“请求已经完成”
- 为什么 KV Cache 会让显存成为并发瓶颈
- 为什么 response cache 和 prefix cache 是不同层的东西
- 为什么模型服务的性能不能只用 QPS 描述

如果这些问题能说清楚，后面看 vLLM、SGLang、gateway、eval 和 finetune 时，就会更像在读一个连续系统，而不是在背一堆英文名词。

## 建议的学习方式

第一次读时，不建议一边读一边查太多论文。更好的方式是：

1. 先读完整章，建立词汇地图。
2. 跑一次 [第一次实操演练](/00-overview/04-first-walkthrough)，观察 mock service 的请求和响应。
3. 回来看 TTFT、ITL、usage、streaming 这些词。
4. 再进入 [Inference Serving](/02-inference-serving/00-overview) 模块。

如果你读到后面发现某个工具页突然变难，通常不是工具本身难，而是这里的基础变量还没变成直觉。那就回来重新看这一章。

## 常见误区

### 误区一：基础概念不重要，直接学工具更快

短期看好像更快，长期会变慢。因为工具的参数、指标和架构边界都在服务这些基础概念。

### 误区二：LLM 服务和普通 REST API 差不多

接口形式像，但资源模型很不一样。普通 API 多数请求很快释放资源，LLM 请求可能因为长输入、长输出和 streaming 长时间占用执行状态。

### 误区三：上下文越长越好

上下文越长，能力上限可能更高，但成本、延迟、失败面和噪声也会增加。好的系统会管理 context，而不是无限堆 context。

### 误区四：缓存就是缓存回答

LLM 系统里至少有 response cache、semantic cache、KV Cache、prefix caching 等不同层次。它们命中的对象、风险和收益完全不同。

### 误区五：吞吐越高体验越好

吞吐只描述系统整体处理能力。用户体验还会受到 TTFT、ITL、失败率、排队时间和输出长度影响。
