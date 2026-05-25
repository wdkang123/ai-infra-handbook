# 健康检查、Metrics、Request ID

## 为什么平台层不只关心“能不能转发”

一个请求能成功，不代表平台层状态就真的清楚。  
平台还需要知道：

- 下游现在是不是活着
- 最近失败有没有变多
- 这条请求跨了哪些服务

## 健康检查

`/health` 最开始常常只是“服务自己说自己活着”。  
但平台层更进一步，它还应该尽量知道下游是不是活着。

所以当前仓库里的 gateway 已经开始做最小 upstream health probe。  
这一步虽然还很轻，但它把 `/health` 从静态声明推进成了一个真实信号。

## Metrics

`/metrics` 更像“长期看系统状态”的窗口。  
如果 `/health` 更适合快速判断活不活，那 metrics 更适合回答：

- 最近请求量有多少
- 认证失败有没有变多
- 上游失败有没有变多
- fallback 有没有变多，成功 fallback 占多少

这就是为什么健康检查和 metrics 不能互相替代。

## Structured Events

`/events` 处在 header 和 metrics 中间。

header 适合回答“这一次响应最终是什么状态”。  
metrics 适合回答“一段时间内整体趋势如何”。  
structured events 适合回答“最近这几条请求分别经历了哪些关键动作”。

当前 gateway 会记录 `request_received`、`auth_failed`、`rate_limited`、`route_not_found`、`cache_hit`、`cache_miss`、`upstream_attempt`、`fallback_attempt`、`fallback_success`、`request_success` 等事件，并支持按 `event_type`、`request_id`、`requested_model`、`upstream_model` 过滤。`/events/summary` 会把最近事件聚合成计数，帮助你快速看事件类型、请求模型和上游模型分布。`/events/failures` 会专门聚合失败相关事件、状态码、失败上游和 failed request 数量。`/events/requests` 会先列出最近请求 timeline 索引，`/events/requests/{request_id}` 再把一条请求的事件串成 timeline，适合回看路由、fallback 和终止事件。学习时可以先把它看成最小事件日志，而不是生产级日志平台。

## Request ID

`x-request-id` 不是业务输出的一部分，但对跨服务排查非常重要。  
它的意义在于：你终于能把“一条请求”在不同层里串起来看。

学习阶段先建立这个习惯非常值，因为以后系统一复杂：

- streaming
- 多服务
- 多模型
- 重试

都会让“到底是哪条请求出的问题”变得更难。
