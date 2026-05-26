# 从 Demo Gateway 到真实平台

当前 `ai-gateway` 已经不是一个普通代理。
它有鉴权、模型名映射、路由、限流、cache、fallback、streaming 透传、request id、upstream health、metrics 和 events。

但它也不是完整生产平台。
它还没有多租户管理平面、复杂 canary、生产级策略引擎、预算系统、外部 tracing 后端和完整审计。

这页要回答的是：

> 一个 demo gateway 怎么继续长成真实平台，而不失去学习项目最重要的清晰边界？

## 当前 Demo Gateway 已经表达了什么

当前 gateway 已经表达了平台层的核心骨架：

| 能力 | 当前作用 |
| --- | --- |
| Auth | 区分谁可以进入平台入口 |
| Routing | 把外部模型名映射到内部目标 |
| Rate limit | 让入口治理不只是转发 |
| Cache | 表达成本和重复请求治理 |
| Fallback | 表达上游失败后的恢复路径 |
| Streaming proxy | 表达流式响应的代理边界 |
| Upstream health | 表达 gateway 对依赖状态的观察 |
| Metrics | 表达整体趋势 |
| Events | 表达单条请求路径 |
| Request ID | 串起 gateway 和 inference |

这些能力已经足够让读者理解：gateway 是平台层，不是透明管道。

## 它还没有做满什么

真实平台通常还会继续扩展：

- tenant / organization / project 管理
- API key 生命周期
- per-tenant quota
- token budget
- per-model pricing
- weighted routing
- canary / shadow traffic
- retry budget
- policy engine
- audit log
- external tracing/logging backend
- dashboard 和告警
- config rollout / rollback
- secrets management

这些都重要，但不应该一开始全做。
学习项目要先把边界讲清楚，再逐步把能力变厚。

## 真实平台化的核心原则

一句话：

> 先让治理语义可解释，再让策略能力变复杂。

也就是说，不要急着做华丽控制台。
先确认每个策略能被测试、能被 request timeline 解释、能被 metrics 观察、能在出问题时回滚。

平台层最怕的是：策略越来越多，但没人知道一条请求为什么命中了某个策略。

## 推荐演进顺序

### 第一步：把模型路由策略变厚

当前 `configs/models.yaml` 已经能表达：

- 外部模型名
- target model
- fallback chain

下一步可以逐步扩展：

- per-model timeout
- per-model retry budget
- weighted routing
- canary target
- cache policy
- metadata for cost / owner

但要保持一个原则：每次路由决策都应该能在 events 中解释。

例如 timeline 中应该看得到：

```text
request_received
auth_passed
route_selected
upstream_attempt
fallback_attempt
request_success
```

当前项目还没有完整 `route_selected` 事件，但这是一个自然的演进方向。

### 第二步：把限流从全局变成租户维度

当前限流是学习型最小实现。
真实平台需要区分：

- tenant
- API key
- model
- route
- time window
- request budget
- token budget
- concurrency budget

建议逐步演进：

1. token -> tenant id
2. tenant -> request budget
3. model -> per-model budget
4. prompt/completion token -> token budget
5. concurrency -> running request guard

每一步都要保留 `401` 和 `429` 的清晰语义。

### 第三步：让 fallback 从“能切换”变成“有边界的恢复策略”

fallback 很容易被滥用。

真实平台要回答：

- 哪些错误允许 fallback？
- 4xx 是否应该 fallback？
- 5xx 是否都能 fallback？
- streaming 首 chunk 后能不能 fallback？
- fallback 后质量是否变化？
- fallback 是否应该进入 eval/release 记录？
- fallback 是否有次数和成本预算？

当前项目已经表达了一个重要边界：streaming 首 chunk 后 fallback 会变复杂。
后续应该继续把 fallback 做成可解释策略，而不是无限重试。

### 第四步：把 cache 做成安全的成本治理能力

cache 不是简单“相同请求返回相同响应”。
真实平台必须考虑：

- cache key 是否包含 tenant/token
- system prompt 是否进入 key
- model target 是否进入 key
- temperature 等参数是否进入 key
- cache TTL
- cache eviction
- cache 命中是否允许跨用户
- cached response 是否仍然符合当前权限

当前 gateway 已经测试 token 隔离和 TTL，这是很好的学习起点。
后续可以继续扩展 cache policy，但不要牺牲隔离边界。

### 第五步：接外部 observability 后端

当前 `/events` 是内存结构化事件。
它适合学习，但不是生产日志平台。

真实平台可以逐步接：

- structured logs
- OpenTelemetry traces
- Prometheus metrics
- dashboard
- alerting
- request sampling
- retention policy
- PII 脱敏

但迁移时要保留当前语义：

- request id 仍然是复盘主键
- events 仍然能解释 route/fallback/cache/error
- metrics 仍然能看整体趋势

不要接了外部系统，反而让学习者看不懂请求发生了什么。

## 当前仓库相关文件

重点看：

```text
projects/ai-gateway/src/ai_gateway/server.py
projects/ai-gateway/src/ai_gateway/router.py
projects/ai-gateway/src/ai_gateway/runtime.py
projects/ai-gateway/src/ai_gateway/config.py
projects/ai-gateway/configs/models.yaml
projects/ai-gateway/tests/test_proxy.py
```

其中：

- `server.py` 表达平台入口和事件记录。
- `router.py` 表达模型路由和 upstream 调用。
- `runtime.py` 表达 metrics、rate limiter、cache、events。
- `models.yaml` 表达模型名到 target/fallback 的配置边界。
- tests 表达平台语义的保护网。

## 一个具体演进场景

假设你想新增 canary：

```text
ai-infra-chat
  -> 95% stable target
  -> 5% candidate target
```

不要第一步就做管理后台。
更稳的步骤是：

1. 在配置中表达 candidate target。
2. 在 router 中选择 target。
3. 在 events 中记录 selected target 和 reason。
4. 在 response header 中保留实际 upstream。
5. 在 metrics 中聚合 stable/candidate 请求数。
6. 在 eval 里对 candidate target 做 run/compare。
7. 在 case study 或 output gallery 中记录证据。

这样 canary 不是一个神秘开关，而是一个可观察、可回滚、可评测的策略。

## 平台化风险清单

| 风险 | 表现 | 防线 |
| --- | --- | --- |
| 策略不可解释 | 不知道请求为什么走到某个上游 | request timeline 记录 route decision |
| fallback 掩盖问题 | 用户得到 200，但主上游长期失败 | header、events、metrics 都记录 fallback |
| cache 越权 | 不同 token 命中同一缓存 | cache key 保留 token/tenant 隔离 |
| 限流误伤 | 大量正常请求被 429 | tenant/model 维度指标和事件 |
| 成本失控 | 长上下文请求绕过预算 | token budget + usage 统计 |
| 观测断裂 | 只能看到最后 502 | request id 贯穿 gateway 和 inference |
| 配置不可回滚 | 策略改坏后难恢复 | config version 和发布记录 |

## 验收清单

平台化改动至少确认：

- [ ] `401 / 404 / 429 / 502` 语义不混乱
- [ ] `/v1/models` 仍然说明 target model 和 fallback metadata
- [ ] `/health` 仍然反映 upstream 状态
- [ ] `/events/failures` 能聚合失败状态码和失败 upstream
- [ ] `/events/requests/{request_id}` 能看见 cache / upstream / fallback / terminal event
- [ ] `x-request-id`、`x-upstream-model`、`x-fallback-used`、`x-cache` 仍然存在
- [ ] cache 仍然按 token 或 tenant 隔离
- [ ] `PYTHON=.venv/bin/python make gateway-test` 通过
- [ ] `PYTHON=.venv/bin/python make infra-smoke` 通过

## 文档同步点

如果 gateway 能力继续扩展，需要同步更新：

- [ai-gateway](/06-projects/02-ai-gateway)
- [API Surface 速查](/09-reference/05-api-surface)
- [CLI Surface 速查](/09-reference/06-cli-surface)
- [验证矩阵](/09-reference/07-validation-matrix)
- [Gateway 韧性 Lab](/07-hands-on-labs/02-gateway-resilience-lab)
- [请求失败排查案例](/11-case-studies/01-request-incident-walkthrough)
- [Gateway fallback/cache 复盘](/11-case-studies/04-gateway-fallback-cache-incident)

## 常见误区

### “真实平台第一步是做控制台”

不一定。
控制台只是管理界面，真正核心是策略语义、观测和回滚。

### “Gateway 只要转发稳定就够了”

不够。
平台层要治理身份、模型、成本、失败、观测和发布路径。

### “Fallback 越多越可靠”

不一定。
fallback 可能掩盖质量变化、成本变化和主上游问题，必须有预算和观测。

### “Cache 命中越高越好”

不一定。
如果 cache key 边界错了，高命中率可能意味着越权或脏数据。

### “接外部 tracing 后本地 events 可以删掉”

不建议。
学习项目里本地 events 是理解请求路径的重要入口，生产迁移也应该保留同样语义。

## 学完应该能回答

读完这一页后，你应该能回答：

1. 当前 `ai-gateway` 已经表达了哪些平台层骨架？
2. 为什么真实平台化不应该从复杂控制台开始？
3. fallback、cache、rate limit 分别有哪些生产风险？
4. canary 或 weighted routing 应该如何接入 events、metrics 和 eval？
5. Gateway 平台化改动应该如何验收？

## 继续阅读

- [Gateway 平台化加固](/12-production-migration/02-gateway-platform-hardening)
- [外部模型名与内部目标映射](/03-ai-gateway-platform/06-model-name-to-target-mapping)
- [健康检查、Metrics、Request ID](/03-ai-gateway-platform/02-health-metrics-request-id)
- [验证矩阵](/09-reference/07-validation-matrix)
