# Gateway 平台化加固

这一页说明 `ai-gateway` 如果要从学习型 gateway 继续走向真实平台，应该优先补什么。

当前 gateway 已经不是普通代理。
它有鉴权、路由、限流、fallback、cache、events、metrics 和 upstream health。

下一步不是把所有平台能力一次做满，而是把治理边界继续变厚，并让每个策略都可解释、可测试、可回滚。

## 当前应该保留的接口和 Header

迁移时优先保留：

```text
POST /v1/chat/completions
GET  /v1/models
GET  /health
GET  /metrics
GET  /events
GET  /events/summary
GET  /events/failures
GET  /events/requests
GET  /events/requests/{request_id}
```

优先保留这些 header：

```text
x-request-id
x-upstream-model
x-fallback-used
x-cache
```

这些接口和 header 是平台治理的观察面。
平台能力越复杂，越需要这些观察面保持稳定。

## 加固原则

一句话：

> 策略可以变复杂，但请求路径必须变得更可解释，而不是更神秘。

任何新增策略都应该能回答：

- 它为什么被命中？
- 它影响了哪个模型或租户？
- 它有没有改变 upstream？
- 它有没有触发 fallback？
- 它有没有改变成本或延迟？
- 它能不能在 request timeline 中看到？
- 它是否有测试覆盖？

如果不能回答这些问题，策略越多，平台越难维护。

## 第一阶段：把路由策略从配置示例变成策略对象

当前 `configs/models.yaml` 已经能表达：

- 外部模型名
- target model
- fallback chain

下一步可以逐步增加：

- weighted routing
- canary routing
- per-model timeout
- per-model retry budget
- per-model cache policy
- per-model cost metadata
- route decision reason

但不建议第一步就做复杂管理后台。
先让策略可测试、可读、可回滚。

### 路由策略的事件要求

一个更真实的 gateway 应该在 events 中解释路由：

```text
request_received
auth_passed
route_selected
upstream_attempt
fallback_attempt
request_success
```

当前项目已经有一部分事件。
后续可以把 route decision 继续补厚。

## 第二阶段：把限流从全局最小实现变成租户维度

真实 gateway 通常要区分：

- tenant
- API key
- model
- route
- time window
- request count
- token count
- concurrency

推荐演进路径：

1. token -> tenant id
2. tenant -> request budget
3. model -> per-model limit
4. prompt/completion tokens -> token budget
5. running requests -> concurrency budget

每一步都要保持：

- 未认证是 `401`
- 超限是 `429`
- 模型不存在是 `404`
- 上游失败是 `502`

不要让错误码语义混在一起。

## 第三阶段：把 fallback 变成有预算的恢复策略

当前 fallback 适合学习“主下游失败后切备用”。
真实平台要继续明确：

| 问题 | 为什么重要 |
| --- | --- |
| 哪些错误可 fallback | 4xx 通常不该盲目 fallback |
| 最多尝试几次 | 避免放大延迟和成本 |
| streaming 首 chunk 后是否允许 | 避免输出语义混乱 |
| fallback 是否改变质量 | 备用模型可能能力不同 |
| fallback 是否计入 release/eval | 发布判断要知道真实路径 |
| fallback 是否有预算 | 避免故障时成本失控 |

fallback 不是万能重试。
它是一种有边界的恢复策略。

## 第四阶段：把 cache 做成安全的成本治理能力

cache 的生产风险很高。

需要明确：

- cache key 是否包含 tenant/token？
- cache key 是否包含模型名和 target？
- system prompt 是否进入 key？
- temperature、max_tokens 等参数是否进入 key？
- cache TTL 是多少？
- cache 是否可按模型关闭？
- cache 命中是否会绕过权限变化？
- cached response 是否保留 request id？

当前项目已经覆盖 token 隔离和 TTL，这是很好的基础。
后续做更强 cache 时，第一优先级仍然是隔离和可解释。

## 第五阶段：接外部 tracing / logging backend

当前 `/events` 是内存结构化事件，适合学习。
真实平台应逐步接：

- structured logs
- distributed tracing
- request sampling
- trace id 和 request id 映射
- metrics dashboard
- alerting
- retention policy
- PII 脱敏
- audit storage

但即使接外部系统，也建议保留当前事件语义，方便学习者理解。

理想状态是：

- 本地 `/events` 仍能演示请求路径。
- 外部 tracing 能做长期存储和跨服务视图。
- 两者都用 request id 或 trace id 串起来。

## 第六阶段：引入配置版本与回滚

平台问题经常不是代码 bug，而是策略配置改错。

真实 gateway 应该逐步记录：

- config version
- route policy version
- cache policy version
- quota policy version
- release/change reason
- operator / automation source
- rollback target

这能帮助你回答：

> 今天 14:30 开始 429 上升，是不是某个限流配置发布导致的？

没有配置版本，平台排障会变成猜测。

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

迁移时常改：

- `models.yaml`：路由和 fallback 配置。
- `router.py`：候选 upstream、转发、health probe。
- `runtime.py`：rate limit、cache、metrics/events。
- `server.py`：API 入口和事件记录。
- tests：保护平台语义。

## 风险清单

| 风险 | 表现 | 防线 |
| --- | --- | --- |
| 策略变复杂 | 出错时不知道命中哪条规则 | request timeline 记录 route decision |
| fallback 滥用 | 质量波动被 200 掩盖 | header、events、metrics 都记录 fallback |
| cache 越权 | 不同 token 命中同一缓存 | cache key 保留 token/tenant 隔离 |
| 限流误伤 | 正常请求被大量 `429` | tenant/model 维度指标 |
| 成本失控 | 长上下文请求绕过治理 | token budget 和 usage 统计 |
| tracing 缺失 | 只能看最后错误 | request id 贯穿 gateway 和 inference |
| 配置漂移 | 不知道哪次策略改坏 | config version 和 rollback |

## 验收清单

Gateway 平台化改动至少确认：

- [ ] `401 / 404 / 429 / 502` 语义不混乱
- [ ] `/v1/models` 仍然能说明 target model 和 fallback metadata
- [ ] `/health` 仍然能反映 upstream 状态
- [ ] `/events/failures` 能聚合失败状态码和失败 upstream
- [ ] `/events/requests/{request_id}` 能看见 cache / upstream / fallback / terminal event
- [ ] fallback headers 仍然存在
- [ ] cache 仍然按 token 或 tenant 隔离
- [ ] route/fallback/cache 关键路径有测试
- [ ] `PYTHON=.venv/bin/python make gateway-test` 通过
- [ ] `PYTHON=.venv/bin/python make infra-smoke` 通过

## 应该更新的文档

- [ai-gateway](/06-projects/02-ai-gateway)
- [API Surface 速查](/09-reference/05-api-surface)
- [CLI Surface 速查](/09-reference/06-cli-surface)
- [验证矩阵](/09-reference/07-validation-matrix)
- [Gateway 韧性 Lab](/07-hands-on-labs/02-gateway-resilience-lab)
- [请求失败排查案例](/11-case-studies/01-request-incident-walkthrough)
- [Gateway fallback/cache 复盘](/11-case-studies/04-gateway-fallback-cache-incident)

## 常见误区

### “平台化就是做控制台”

不完整。
控制台是表层，核心是策略、观测、审计、回滚和测试。

### “Fallback 越多越稳定”

不一定。
fallback 可能掩盖主上游故障，也可能改变质量和成本。

### “Cache 命中率越高越好”

不一定。
如果隔离边界错了，高命中率可能是安全问题。

### “限流只按 request count 就够了”

LLM 场景不够。
长 prompt 和长 completion 的成本差异很大，token budget 很重要。

### “接入 tracing 后本地 events 就没用了”

不建议这样想。
本地 events 是学习、测试和案例复盘的轻量入口。

## 学完应该能回答

读完这一页后，你应该能回答：

1. Gateway 平台化时哪些接口和 header 最应该保留？
2. 为什么新增策略必须进入 request timeline？
3. fallback、cache、rate limit 分别有哪些生产风险？
4. 为什么配置版本和回滚是平台能力的一部分？
5. Gateway 加固后应该跑哪些检查？

## 继续阅读

- [从 Demo Gateway 到真实平台](/03-ai-gateway-platform/07-from-demo-gateway-to-real-platform)
- [平台层与模型服务层边界](/03-ai-gateway-platform/05-platform-vs-model-service)
- [外部模型名与内部目标映射](/03-ai-gateway-platform/06-model-name-to-target-mapping)
- [验证矩阵](/09-reference/07-validation-matrix)
