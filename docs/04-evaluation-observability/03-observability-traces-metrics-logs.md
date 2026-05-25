# Tracing、Metrics、Logs

## 为什么这三件事要一起看

因为它们经常被统称为“可观测性”，但它们其实回答的是不同问题。

如果你只看 metrics，你会知道“系统变差了”；  
如果你只看 logs，你可能会看到很多细节，但很难形成整体视角；  
如果你只看 traces，你能看单次路径，但不一定知道整体趋势。

真正有用的 observability，通常是这三者一起存在。

## Tracing 在回答什么

tracing 回答的是：  
**这一条请求经过了哪些环节，每个环节花了多久。**

对于 AI Infra，这很重要，因为一条请求往往不是单段直线：

- 应用把请求打到 gateway
- gateway 做鉴权、路由、限流
- inference-service 执行模型请求
- 结果再返回上来

如果没有 trace，你只能猜卡在了哪。  
有 trace 以后，你才真正拥有“单次请求级”的视角。

## Metrics 在回答什么

metrics 回答的是：  
**整体系统最近是什么状态。**

比如：

- 请求数有没有上升
- 错误率有没有升高
- P99 latency 有没有抖动
- token 消耗是不是异常

所以 metrics 更像驾驶舱仪表盘。  
它不一定能告诉你为什么有问题，但能告诉你“现在是不是出问题了”。

## Logs 在回答什么

logs 回答的是：  
**当时到底发生了什么。**

它通常更原始、更细碎，但对排障特别重要。  
你可能会在 log 里看到：

- 原始错误消息
- 具体哪个模型名没有命中
- 哪个 request id 出了问题
- 某次转发为什么失败

所以 logs 常常是从 metrics 告警、trace 定位之后，最后下钻到具体细节的地方。

## 这三者最好的配合方式

一个很实用的理解顺序是：

1. 先用 metrics 发现“哪里不对”
2. 再用 tracing 看“卡在哪一段”
3. 最后用 logs 找“具体是怎么坏的”

这个顺序非常适合 AI Infra，因为它天然就是跨层系统。

## 在当前仓库里能对应到什么

当前仓库不是完整 observability 平台，但它已经把最小观察点做出来了：

- `inference-service` 和 `ai-gateway` 都有 `/metrics`
- gateway 和 inference 之间已经开始透传 `x-request-id`
- smoke 测试已经覆盖 health、metrics、streaming、request id 这些基础行为

也就是说，这套仓库已经能让你形成“可观测性不是另一个独立产品，而是系统本身的一部分”这个直觉。

## 学习时常见误区

### “有 metrics 就够了”

不够。  
metrics 很适合看趋势，但通常不够解释单次失败。

### “trace 只是高级功能，后面再说”

也不对。  
就算你现在不接完整 tracing 平台，也应该先理解 request id、span、链路边界这些概念。  
它们会直接影响你如何设计 gateway 和 inference 层。

### “logs 越多越好”

不是。  
logs 的价值在于可检索、可对齐、能和 request id 对上，而不是无穷无尽地堆文本。

## 这一章学完应该带走什么

你最应该带走的是这个结构：

- metrics 看整体
- tracing 看单次路径
- logs 看原始细节

把这个结构建立起来后，后面再看 Langfuse、OpenTelemetry、Phoenix、Grafana 这类工具时，你就不会只看到产品名，而能看到它们在系统里分别解决哪类问题。
