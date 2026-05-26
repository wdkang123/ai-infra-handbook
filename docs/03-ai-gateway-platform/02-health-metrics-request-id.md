# 健康检查、Metrics、Request ID

一个 AI Gateway 如果只会转发请求，它还不是一个真正有平台感的入口。
平台层除了“把请求送到下游”，还要持续回答三个问题：

1. 系统现在活着吗？
2. 最近整体状态怎么样？
3. 这一次请求到底经历了什么？

这三个问题分别对应：

- health check
- metrics
- request id + structured events

它们不是装饰功能，而是排障和维护的基本语言。

## 为什么不能只看“请求成功了”

一次请求返回 200，不代表系统真的健康。

例如：

- 主上游失败了，gateway 通过 fallback 返回了 200。
- cache 命中了，所以没有暴露下游已经不可用。
- 当前请求成功了，但最近 5 分钟 429 或 502 快速上升。
- 服务本身还活着，但某个 upstream model 已经探测失败。
- 用户拿到了响应，但后续无法通过 request id 复盘路径。

所以平台层需要多种信号，而不是只看 HTTP 状态码。

## 三类信号的分工

| 信号 | 主要回答 | 适合场景 |
| --- | --- | --- |
| `/health` | 当前服务和依赖是否可用 | 部署检查、负载均衡、上线前确认 |
| `/metrics` | 一段时间内整体趋势如何 | 监控、告警、容量判断 |
| `x-request-id` + `/events` | 单条请求经历了什么 | 排障、复盘、审计、教学演示 |

这三类信号互相补充。
缺任何一个，系统都会变得更难维护。

## Health Check：活着不等于健康

最简单的 `/health` 只会返回：

```json
{
  "status": "healthy"
}
```

这只能说明进程还在响应 HTTP。
但 gateway 的健康状态还应该关心下游服务。

当前仓库里的 `ai-gateway` 会对配置中的 upstream 做最小 health probe，然后返回：

- gateway 自己的 status
- gateway version
- `upstream_services`

如果某个 upstream 探测失败，gateway 顶层状态会变成 `degraded`。
这很重要，因为它把 `/health` 从“自我声明”推进成“依赖状态信号”。

## Health Check 不能证明什么

health check 很有用，但它不能证明所有事情。

| `/health` 能证明 | `/health` 不能证明 |
| --- | --- |
| 服务进程能响应 | 模型质量好不好 |
| 某些依赖当前可探测 | 每条请求都会成功 |
| upstream 大致可用 | 高并发下不会排队 |
| 部署后接口没完全挂 | token 成本是否合理 |

因此，health check 更像“生命体征”，不是完整诊断报告。

## Metrics：看趋势，而不是看单次请求

`/metrics` 解决的是另一个问题：一段时间内系统整体发生了什么。

对 gateway 来说，metrics 通常应该包含：

- 总请求数
- 成功请求数
- 鉴权失败数
- rate limit 命中数
- route not found 数
- upstream failure 数
- fallback attempts / successes
- cache hits / misses

对 inference-service 来说，metrics 通常应该包含：

- running requests
- total requests
- successful / failed requests
- prompt tokens total
- completion tokens total
- total tokens

这类数据适合做趋势判断。
例如“最近 10 分钟 502 上升”或“cache hit rate 突然下降”。

## Metrics 不能替代 Request ID

metrics 告诉你“整体发生了什么”，但通常不能告诉你“某一条请求为什么这样”。

例如你看到：

```text
gateway_upstream_failures_total 10
```

这说明上游失败增加了。
但它不能直接回答：

- 哪个用户请求失败了？
- 请求要的模型名是什么？
- 走的是哪个 upstream？
- 是否尝试 fallback？
- 最终返回了 502 还是 fallback 成功？

这些问题需要 request id 和事件 timeline。

## Request ID：把跨服务请求串起来

`x-request-id` 的价值在于：

> 给一条请求一个稳定名字，让它能穿过 gateway、inference-service、events、metrics 旁路和案例复盘。

当前仓库里，如果客户端没有传 `x-request-id`，服务会生成一个。
响应也会把它放回 header。

这样你就可以：

1. 从客户端响应 header 里拿到 `x-request-id`。
2. 去 gateway `/events/requests/{request_id}` 看入口层 timeline。
3. 去 inference `/events/requests/{request_id}` 看执行层 timeline。
4. 对照 `/metrics` 判断这是单点问题还是整体趋势。

这就是从“感觉慢/失败了”走向“可复盘”的关键。

## Structured Events：介于日志和指标之间

structured events 可以先理解成轻量事件日志。

它不像 metrics 那样只保留聚合数字，也不像原始日志那样完全自由文本。
它用结构化字段记录请求生命周期中的关键动作。

当前 gateway 会记录类似事件：

| 事件 | 说明 |
| --- | --- |
| `request_received` | gateway 收到请求 |
| `auth_failed` | 鉴权失败 |
| `rate_limited` | 被限流 |
| `route_not_found` | 找不到模型路由 |
| `cache_hit` / `cache_miss` | cache 是否命中 |
| `upstream_attempt` | 尝试访问某个上游 |
| `fallback_attempt` | 主上游失败后尝试 fallback |
| `fallback_success` | fallback 成功 |
| `upstream_error` | 上游错误 |
| `request_success` | 请求最终成功 |

inference-service 也会记录：

| 事件 | 说明 |
| --- | --- |
| `request_received` | 执行层收到请求 |
| `validation_failed` | 请求校验失败 |
| `model_not_found` | 模型名不匹配 |
| `engine_generate_start` | 引擎开始普通生成 |
| `engine_stream_start` | 引擎开始流式生成 |
| `engine_error` | 引擎错误 |
| `request_success` | 执行成功 |

这些事件让学习者可以看到一次请求在不同层发生了什么。

## 一条请求应该怎么查

假设用户说：“刚才那个请求失败了。”

你可以按这个顺序：

1. 找到响应 header 里的 `x-request-id`。
2. 查 gateway timeline。
3. 如果 gateway 走到 upstream，再查 inference timeline。
4. 看 gateway `/events/failures`，判断是否有同类失败。
5. 看 gateway `/metrics`，判断失败是偶发还是趋势。
6. 看 inference `/metrics`，判断执行层是否也有失败或 token 异常。

对应命令入口可以在 [命令速查](/09-reference/01-command-cheatsheet) 和 [API Surface](/09-reference/05-api-surface) 里找到。

## 一个具体排障场景

用户请求模型 `vllm-local`，返回 200，但回答速度变慢。

如果只看 200，你会觉得没问题。
但通过事件可能看到：

```text
request_received
cache_miss
upstream_attempt: primary
fallback_attempt: primary -> backup
upstream_attempt: backup
fallback_success
request_success
```

这说明请求成功不是因为主上游健康，而是 fallback 成功。
此时你应该继续看：

- `/health` 里 primary upstream 是否 degraded
- `/metrics` 里 fallback attempts 是否上升
- `/events/failures` 里失败 upstream 是否集中
- 相关 case study 是否有同类复盘

这就是为什么平台层不能只保留最终响应。

## 当前仓库怎么表达

### Gateway 入口

相关文件：

```text
projects/ai-gateway/src/ai_gateway/server.py
projects/ai-gateway/src/ai_gateway/runtime.py
projects/ai-gateway/src/ai_gateway/router.py
```

重点接口：

- `GET /health`
- `GET /metrics`
- `GET /events`
- `GET /events/summary`
- `GET /events/failures`
- `GET /events/requests`
- `GET /events/requests/{request_id}`
- `POST /v1/chat/completions`

重点 header：

- `x-request-id`
- `x-cache`
- `x-upstream-model`
- `x-fallback-used`

### Inference 入口

相关文件：

```text
projects/inference-service/src/inference_service/server.py
projects/inference-service/src/inference_service/runtime.py
```

重点接口：

- `GET /health`
- `GET /metrics`
- `GET /events`
- `GET /events/summary`
- `GET /events/requests`
- `GET /events/requests/{request_id}`
- `POST /v1/chat/completions`

重点字段：

- `usage.prompt_tokens`
- `usage.completion_tokens`
- `usage.total_tokens`
- `x-request-id`

## 学习阶段和生产系统的区别

当前 `/events` 是内存事件日志，适合学习，不是生产日志平台。
真实系统通常还会接：

- structured logs
- distributed tracing
- Prometheus / OpenTelemetry
- dashboard
- alerting
- retention policy
- tenant / user / org 维度
- PII 脱敏和访问控制

但学习阶段先把边界讲清楚更重要。
你要先知道 health、metrics、request id、events 分别解决什么问题，再去接更复杂的观测系统。

## 常见误区

### “有 `/health` 就够了”

不够。
`/health` 看当前可用性，不能解释趋势，也不能复盘单条请求。

### “metrics 越多越好”

不一定。
指标要能回答问题。没有命名规范、分层和排查路径的指标，会变成噪音。

### “request id 只是日志字段”

不是。
它是跨服务复盘的主键。没有它，gateway、inference、case study 和用户反馈很难串起来。

### “请求成功就不用看 events”

不一定。
成功请求也可能经历 fallback、cache hit、慢上游或重试。成功响应背后的路径同样重要。

## 学完应该能回答

读完这一页后，你应该能回答：

1. `/health`、`/metrics`、`x-request-id` 分别解决什么问题？
2. 为什么 health check 不能代表模型质量或请求体验？
3. 为什么 metrics 不能替代单条请求 timeline？
4. 一条 gateway 请求失败时，应该按什么顺序排查？
5. 当前仓库哪些接口和 header 能帮助你复盘请求？

## 继续阅读

- [鉴权、路由、限流](/03-ai-gateway-platform/01-auth-routing-rate-limit)
- [Gateway Router、Fallback 与 Cache](/03-ai-gateway-platform/03-gateway-router-fallback-cache)
- [请求失败排查案例](/11-case-studies/01-request-incident-walkthrough)
- [Gateway fallback/cache 复盘](/11-case-studies/04-gateway-fallback-cache-incident)
