# Gateway 平台化加固

这一页说明 `ai-gateway` 如果要从学习型 gateway 继续走向真实平台，应该优先补什么。

当前 gateway 已经不是普通代理：它有鉴权、路由、限流、fallback、cache、events、metrics 和 upstream health。  
下一步不是把所有平台能力一次做满，而是把治理边界继续变厚。

## 当前边界

当前应该保留：

- `POST /v1/chat/completions`
- `GET /v1/models`
- `GET /health`
- `GET /metrics`
- `GET /events`
- `GET /events/failures`
- `GET /events/requests/{request_id}`
- `x-request-id`
- `x-upstream-model`
- `x-fallback-used`
- `x-cache`

这些接口和 header 是后续平台能力的观察面。

## 加固顺序

### 第一步：把路由策略从“配置示例”变成“策略对象”

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

但要避免一开始就做复杂管理后台。先让策略可测试、可读、可回滚。

### 第二步：把限流从全局最小实现变成租户维度

真实 gateway 通常要区分：

- tenant
- API key
- model
- route
- time window

学习项目里可以先扩展成：

- token -> tenant id
- tenant -> request budget
- model -> per-model limit

迁移时必须继续保留 `401 / 429` 的清晰语义。

### 第三步：把 fallback 变成有预算的恢复策略

当前 fallback 适合学习“主下游失败后切备用”。  
更真实时要补：

- 哪些错误可 fallback
- fallback 最多尝试几次
- 是否允许 streaming 首 chunk 后 fallback
- fallback 是否改变模型质量
- fallback 是否进入 release / eval 记录

fallback 不是万能重试。它必须有边界。

### 第四步：接外部 tracing / logging backend

当前 `/events` 是内存结构化事件，适合学习。  
真实平台应逐步接：

- structured logs
- distributed tracing
- request sampling
- trace id 和 request id 映射
- dashboard 和告警

但即使接外部系统，也建议保留当前事件语义，方便学习者理解。

## 风险清单

| 风险 | 表现 | 防线 |
| --- | --- | --- |
| 策略变复杂 | 出错时不知道命中哪条规则 | request timeline 记录 route decision |
| fallback 滥用 | 质量波动被掩盖 | header、events、metrics 都记录 fallback |
| cache 越权 | 不同 token 命中同一缓存 | cache key 保留 token 隔离 |
| 限流误伤 | 正常请求被大量 `429` | tenant / model 维度指标 |
| tracing 缺失 | 只能看最后错误 | request id 贯穿 gateway 和 inference |

## 验收清单

- [ ] `401 / 404 / 429 / 502` 语义不混乱
- [ ] `/v1/models` 仍然能说明 target model 和 fallback metadata
- [ ] `/events/failures` 能聚合失败状态码和失败 upstream
- [ ] `/events/requests/{request_id}` 能看见 route / fallback / terminal event
- [ ] fallback headers 仍然存在
- [ ] cache 仍然按 token 隔离
- [ ] `gateway-test` 通过
- [ ] `infra-smoke` 通过

## 应该更新的文档

- [ai-gateway](/06-projects/02-ai-gateway)
- [API Surface 速查](/09-reference/05-api-surface)
- [验证矩阵](/09-reference/07-validation-matrix)
- [Gateway 韧性 Lab](/07-hands-on-labs/02-gateway-resilience-lab)
- [请求失败排查案例](/11-case-studies/01-request-incident-walkthrough)

## 一句话结论

Gateway 平台化的关键，不是立刻做完整控制台，而是把路由、限流、fallback、cache 和 tracing 的语义变得可解释、可测试、可回滚。
