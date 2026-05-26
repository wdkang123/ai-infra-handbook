# Tracing、Metrics、Logs

Tracing、metrics、logs 经常被一起称为 observability。
但它们不是同一个东西。

如果你只看 metrics，你会知道“系统好像变差了”，但未必知道哪条请求出了问题。
如果你只看 logs，你会看到很多细节，但很难判断整体趋势。
如果你只看 traces，你能看到单次路径，但不一定知道这是不是普遍问题。

真正有用的可观测性，是三者一起工作。

## 三者分别回答什么

| 对象 | 主要回答 | 更适合看 |
| --- | --- | --- |
| Metrics | 最近整体状态如何 | 趋势、告警、容量、错误率 |
| Tracing | 某一条请求经过哪些环节 | 单次请求路径、耗时拆分 |
| Logs | 当时发生了哪些细节 | 原始错误、上下文、debug 信息 |

一句话：

- metrics 看整体。
- tracing 看路径。
- logs 看细节。

## Metrics：先发现系统不对

metrics 更像仪表盘。

对 AI Infra 来说，常见 metrics 包括：

- 请求数
- 成功数
- 失败数
- 运行中请求数
- prompt token 总量
- completion token 总量
- 429 / 502 数量
- fallback attempts
- cache hits / misses
- latency 分布
- TTFT / ITL
- tokens/sec

metrics 的价值是让你发现趋势：

- 错误率是不是上升？
- token 使用是不是异常？
- fallback 是否突然增多？
- 某个模型是否请求量暴涨？
- cache hit rate 是否下降？

但 metrics 通常不够解释单条请求为什么失败。

## Tracing：把一条请求拆成路径

tracing 回答的是：

> 这一条请求经过了哪些环节，每个环节发生了什么？

AI Infra 的请求经常跨多层：

```text
client
  -> ai-gateway
  -> inference-service
  -> model backend
  -> inference-service
  -> ai-gateway
  -> client
```

如果没有 tracing 或 request timeline，你只能猜：

- 是 gateway 慢？
- 是 inference 慢？
- 是上游模型慢？
- 是 fallback 了？
- 是 cache miss？
- 是 streaming 中途断了？

有 tracing 后，你可以沿一条 request id 查路径。

## Logs：找到具体细节

logs 更像现场记录。

它适合回答：

- 具体错误消息是什么？
- 哪个模型名没有命中？
- 哪个 upstream 返回了什么状态？
- 哪个 dataset record 校验失败？
- 哪个 export 缺少 adapter 文件？

Logs 的价值不在于越多越好，而在于：

- 结构化
- 可检索
- 能和 request id 对齐
- 不泄露敏感信息
- 能连接 metrics/traces

没有结构的海量日志，会让排障更难。

## 最好的配合顺序

一个实用顺序是：

1. 用 metrics 发现“哪里不对”。
2. 用 tracing 找“卡在哪一段”。
3. 用 logs 看“具体怎么坏的”。
4. 用 eval 判断“输出质量有没有退化”。

注意最后一步：observability 不等于 evaluation。
系统行为正常，不代表答案质量好。

## Observability 和 Evaluation 的边界

这两个概念关系很近，但不能混。

| 问题 | 更接近 |
| --- | --- |
| 请求有没有成功 | observability |
| 首 token 为什么慢 | observability |
| 上游是否 fallback | observability |
| 模型回答是否正确 | evaluation |
| 新模型是否退化 | evaluation |
| 输出格式是否符合任务 | evaluation |
| 退化请求在哪些样本 | evaluation + observability |

真实发布判断通常需要两者一起看：

- observability 说明系统怎么运行。
- evaluation 说明输出质量如何。

## 当前仓库怎么表达

当前仓库不是完整 observability 平台，但已经有最小观察面。

### Inference Service

```text
GET /health
GET /metrics
GET /events
GET /events/summary
GET /events/requests
GET /events/requests/{request_id}
```

重点信号：

- request received
- engine generate start
- stream start
- engine error
- request success
- prompt/completion token counters

### Gateway

```text
GET /health
GET /metrics
GET /events
GET /events/summary
GET /events/failures
GET /events/requests
GET /events/requests/{request_id}
```

重点信号：

- auth failed
- rate limited
- route not found
- cache hit/miss
- upstream attempt
- fallback attempt/success
- request success

这些 endpoint 不是生产级 tracing，但足够帮助学习者建立可观测性直觉。

## 一个具体排查场景

用户反馈：

> 刚才请求很慢，而且最后回答也不太对。

合理拆法：

### 先看 observability

1. 找 `x-request-id`。
2. 查 gateway timeline。
3. 看是否 cache miss、fallback、upstream error。
4. 查 inference timeline。
5. 看 prompt/completion token。
6. 看 metrics 是否整体异常。

### 再看 evaluation

1. 是否有同类样本退化？
2. candidate 和 baseline compare 是否通过？
3. sample analysis 中是否出现同类错误？
4. release recommendation 是否应该 block/review？

这样你不会把“系统慢”和“答案差”混成一个问题。

## 未来接真实 Observability 工具

后续可以接：

- OpenTelemetry
- Prometheus
- Grafana
- Loki / ELK
- Langfuse
- Phoenix
- 自研 dashboard

接工具时不要只看产品名。
要问它解决哪类问题：

- metrics？
- tracing？
- logs？
- eval traces？
- prompt/version tracking？
- dashboard？

工具越多，越需要保持概念分层。

## 常见误区

### “有 metrics 就够了”

不够。
metrics 适合看趋势，但不能解释单条请求细节。

### “Trace 是高级功能，后面再说”

不对。
就算没有完整 tracing 平台，也应该先保留 request id 和 timeline。

### “Logs 越多越好”

不是。
logs 要结构化、可检索、可关联，还要避免敏感信息泄露。

### “Observability 能判断模型质量”

不能完全判断。
它能说明系统行为，质量判断还需要 evaluation。

### “接了外部平台，本地 events 就没价值”

不建议这样想。
本地 events 是学习、测试和案例复盘的重要入口。

## 学完应该能回答

读完这一页后，你应该能回答：

1. metrics、tracing、logs 分别回答什么问题？
2. 为什么 request id 是跨层排障的主键？
3. Observability 和 evaluation 的边界是什么？
4. 当前仓库如何用 `/events/requests/{request_id}` 模拟最小 tracing？
5. 未来接 OpenTelemetry/Grafana/Langfuse 时应该先问什么？

## 继续阅读

- [健康检查、Metrics、Request ID](/03-ai-gateway-platform/02-health-metrics-request-id)
- [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
- [Benchmark 与生产质量不是一回事](/04-evaluation-observability/08-benchmark-vs-production-quality)
- [请求失败排查案例](/11-case-studies/01-request-incident-walkthrough)
