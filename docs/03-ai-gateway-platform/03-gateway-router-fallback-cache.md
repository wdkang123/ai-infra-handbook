# Gateway、Router、Fallback、Cache

## 为什么这一页要放在一起讲

因为这四个词经常在平台层混着出现，但它们并不是完全同一件事。

如果你不把它们分开，后面很容易出现两种常见混乱：

- 把 router 误认为整个 gateway
- 把 fallback / cache 误认为只是“附加优化”

更好的理解方式是：  
它们都属于平台层能力，但各自回答的问题不同。

## Gateway 在回答什么

gateway 回答的是“应用到底通过哪个统一入口来访问模型能力”。

所以 gateway 往往要管：

- 入口协议
- 鉴权
- 模型名映射
- 请求转发
- 限流
- 健康检查
- metrics / request id / structured events

在当前仓库里，`ai-gateway` 就是这条主线的最小学习骨架。

## Router 在回答什么

router 回答的是“这条请求最终要发给哪个下游”。

它经常只是 gateway 里的一部分，而不是完整平台本身。  
你可以把它先理解成“决策器”，而不是“整个入口层”。

常见路由判断包括：

- 这个外部模型名映射到哪个内部 target
- 这个请求应不应该走备用模型
- 这个请求应不应该走测试版本

## Fallback 在回答什么

fallback 回答的是“主要路径失败了以后怎么办”。

它的价值不在“聪明切换”，而在“让平台在异常时仍然有可接受的退路”。

学习时你最应该理解的是：

- fallback 不是正常主路径
- 它是治理能力的一部分
- 它会影响稳定性、结果一致性和排障复杂度

所以一个成熟平台不会把 fallback 当成“悄悄发生的小技巧”，而会把它当成明确的系统行为。

这也是为什么当前 gateway 会把 fallback 暴露成三类观察面：单次响应里的 `x-upstream-model` / `x-fallback-used`，`/metrics` 里的 fallback attempts / successes，以及 `/events` 里的 `fallback_attempt` / `fallback_success`。

## Cache 在平台层又是怎么回事

平台层说 cache，通常不是在说底层 KV cache。  
更常见的是：

- 请求级响应缓存
- semantic cache
- 某些高频 prompt 的复用层

这时它的价值更接近：

- 降低下游调用次数
- 降低成本
- 在某些重复问题场景里缩短响应时间

所以平台层 cache 和推理引擎里的 prefix caching 是两条不同层次的主线。

## 四者之间最容易混淆的边界

### 误区一：Gateway 就是 Router

不对。  
router 通常只是 gateway 的一个核心内部能力。

### 误区二：Fallback 只是路由策略的一种

部分成立，但不够完整。  
更准确地说，fallback 是路由体系里专门处理失败路径的那部分策略，它背后往往牵涉到可用性目标。

### 误区三：平台层 cache 和引擎层 cache 是同一回事

不是。  
一个更靠“减少外部请求或直接复用响应”，一个更靠“复用模型执行中的中间结果”。

## 在当前仓库里应该怎么学

当前仓库里的 `ai-gateway` 还没有把 fallback / semantic cache 做成生产级系统，但它已经把你最需要的学习骨架放好了：

- Bearer token 鉴权
- 模型名到上游的映射
- 限流
- request id 透传
- upstream health 探测
- stream proxy
- 普通请求 fallback
- 首 chunk 前的 streaming fallback
- fallback header 和 fallback metrics
- `/events` 结构化事件
- 默认关闭的非流式 TTL cache

也就是说，你现在已经能清楚看到 gateway 这个“外层壳”长什么样。  
后面再往里面加更复杂 router、canary、semantic cache，会容易很多。

## 推荐的学习顺序

1. 先把 gateway 当成统一入口
2. 再把 router 看成入口内部的决策器
3. 再看 fallback 如何处理失败路径
4. 最后再理解 cache 如何帮助成本和延迟治理

这样学，你就不会把所有“平台能力”都挤进一个抽象词里。
