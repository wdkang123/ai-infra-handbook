# 03. AI Gateway Platform

这一组讲的是“模型服务外面那层平台治理逻辑”。

也就是：

- 请求怎么进入系统
- 谁能调用
- 调哪个模型
- 频率怎么控
- 状态怎么观测
- 出问题时怎么定位

推荐阅读顺序：

1. [鉴权、路由、限流](/03-ai-gateway-platform/01-auth-routing-rate-limit)
2. [健康检查、Metrics、Request ID](/03-ai-gateway-platform/02-health-metrics-request-id)
3. [Gateway、Router、Fallback、Cache](/03-ai-gateway-platform/03-gateway-router-fallback-cache)
4. [Streaming、错误路径、Upstream Health](/03-ai-gateway-platform/04-streaming-errors-upstream-health)
5. [平台层与模型服务层边界](/03-ai-gateway-platform/05-platform-vs-model-service)
6. [外部模型名与内部目标映射](/03-ai-gateway-platform/06-model-name-to-target-mapping)
7. [从 Demo Gateway 到真实平台](/03-ai-gateway-platform/07-from-demo-gateway-to-real-platform)

如果你要看实际代码和接口，再同步配合：

- [ai-gateway 项目页](/06-projects/02-ai-gateway)
