# 03. AI Gateway Platform

这一组讲的是“模型服务外面那层平台治理逻辑”。

如果 serving 层回答“模型怎么执行”，gateway 层回答的就是：

> 在一个组织或产品里，很多调用方、很多模型、很多供应商、很多策略同时存在时，调用大模型这件事怎样被统一管理？

初学时，gateway 很容易被看成“转发代理”。但真实系统里，它往往是 AI 平台最先长出来、也最容易变复杂的一层。它不负责模型内部推理，却负责让模型调用变得可控、可观测、可审计、可演进。

## 为什么需要 Gateway

如果只有一个 demo，业务代码可以直接调用模型服务。

但只要进入稍微真实一点的场景，就会出现这些问题：

- 多个业务方都要调用模型，鉴权怎么统一
- 不同模型供应商的接口不一样，调用方是否都要适配
- 模型名需要对外稳定，但内部目标可能变化
- 某个上游模型失败时，是否可以 fallback
- 请求量太高时，谁应该被限流
- 缓存命中是否能降低成本
- 每次请求出了问题，如何定位到调用方、模型、上游和失败原因
- streaming 中途失败时，客户端看到什么
- 成本、用量、错误率、延迟如何按维度统计

这些不是模型执行本身的问题，而是平台治理问题。

Gateway 的核心价值，就是把这些治理逻辑从业务代码和模型服务里抽出来。

## 更准确的心智模型：Gateway 是策略边界

把 gateway 理解成“代理”容易低估它。代理强调转发，策略边界强调决策。

一次请求进来时，gateway 至少在做三类判断：

1. 这个请求是否允许进入系统。
2. 这个请求应该进入哪个内部目标。
3. 这次调用的过程和结果应该如何被记录。

这三类判断分别对应安全、路由和观测。它们不一定都很复杂，但必须有明确位置。如果每个业务服务都自己做一套鉴权、模型映射、fallback、cache 和日志，系统短期可能能跑，长期会很难解释。

所以 gateway 的真正价值不是“让调用路径多一跳”，而是让治理逻辑有一个统一入口。统一入口意味着：

- 调用方看到稳定模型名，而不是每个内部后端的细节
- 平台可以在不改调用方代码的情况下调整上游目标
- 错误、fallback、cache、限流可以用统一字段记录
- 后续接入计费、审计、配额、灰度和 dashboard 时有落点

这也是为什么学习阶段要先把最小 gateway 做清楚。哪怕它现在只是 mock 上游，边界也应该像真实系统一样存在。

## Gateway 层负责什么

当前学习站里，gateway 重点覆盖这些能力：

- auth：谁能调用
- routing：请求应该去哪个内部目标
- rate limit：调用频率怎么控制
- fallback：主目标失败时是否有备用路径
- response cache：重复请求能否复用结果
- upstream health：如何判断上游健康
- streaming proxy：流式请求怎么转发
- request id：如何串联链路排查
- metrics：如何统计请求、错误、fallback、cache
- events：如何保留结构化运行证据

这些能力合起来，才是“平台”味道。单独一个反向代理并不能自动成为 AI Gateway。

## 一次请求里有哪些关键决策点

可以把 gateway 请求拆成几个检查点。

| 检查点 | 它回答什么 | 失败时常见信号 |
| --- | --- | --- |
| Auth | 调用方是谁，是否允许调用 | `401`、auth error event |
| Rate limit | 这个调用方现在是否超额 | `429`、rate limit counter |
| Model mapping | 外部模型名映射到哪个 target | unknown model、routing error |
| Cache lookup | 是否可以复用已有响应 | `x-cache`、cache event |
| Upstream call | 上游是否可达、是否成功 | `502`、upstream error |
| Fallback | 主路径失败后是否走备用目标 | `x-fallback-used`、fallback event |
| Stream proxy | chunk 如何被转发和收尾 | stream event、disconnect |
| Evidence write | 请求如何进入 metrics 和 events | request id、timeline |

读 gateway 代码时，不要只追“函数怎么调用”。更好的读法是追这些决策点：这个点在哪里做判断，判断结果如何影响后续路径，证据写在哪里。

## Gateway 不负责什么

边界同样重要。

Gateway 通常不负责：

- 真正执行模型推理
- 管理 KV Cache
- 做 continuous batching
- 优化 GPU kernel
- 保存训练 checkpoint
- 判断回答质量是否提升
- 替代评测系统做发布决策

它可以记录用量、延迟和失败，也可以对接 eval 或 billing，但它不是 serving runtime，也不是 evaluation harness。

一旦这个边界清楚，后面系统拆分会容易很多。

## 当前仓库如何体现 Gateway

`projects/ai-gateway` 是一个学习型 AI Gateway。它保留了平台层最关键的几种结构：

- Bearer token 鉴权
- 外部模型名到 upstream target 的映射
- 默认 fallback 配置
- 非流式与流式代理
- response cache
- upstream health 聚合
- `/v1/models`
- `/health`
- `/metrics`
- `/events`
- `/events/summary`
- `/events/failures`
- request timeline

它的目标不是把所有生产功能做满，而是让你看见 gateway 的骨架。

当你阅读代码时，可以把它想成一个“调用控制面”的最小模型：调用方不直接认识每个上游，而是通过 gateway 的统一契约进入系统。

## 当前实现最值得看的三个文件方向

第一次读 `ai-gateway` 时，可以按三个方向看，而不是从头到尾扫。

### 1. 入口契约

先看 server 如何暴露 OpenAI-compatible 风格的接口、health、metrics、events 和模型列表。入口契约决定了调用方能依赖什么，也决定后续替换内部实现时哪些外部行为不能随便破坏。

### 2. 路由和上游目标

再看外部模型名如何映射到内部 target。这个映射是 gateway 的核心边界之一。如果外部模型名和内部 target 直接绑死，后续做 fallback、canary、供应商迁移、成本治理都会很痛苦。

### 3. 事件和指标

最后看 events、summary、failures、timeline 和 metrics。它们让 gateway 不只是“转发成功或失败”，而是能解释每次请求发生了什么。公开学习项目尤其应该强调这点，因为读者需要看到证据才能建立直觉。

## 推荐阅读顺序

1. [鉴权、路由、限流](/03-ai-gateway-platform/01-auth-routing-rate-limit)
2. [健康检查、Metrics、Request ID](/03-ai-gateway-platform/02-health-metrics-request-id)
3. [Gateway、Router、Fallback、Cache](/03-ai-gateway-platform/03-gateway-router-fallback-cache)
4. [Streaming、错误路径、Upstream Health](/03-ai-gateway-platform/04-streaming-errors-upstream-health)
5. [平台层与模型服务层边界](/03-ai-gateway-platform/05-platform-vs-model-service)
6. [外部模型名与内部目标映射](/03-ai-gateway-platform/06-model-name-to-target-mapping)
7. [从 Demo Gateway 到真实平台](/03-ai-gateway-platform/07-from-demo-gateway-to-real-platform)

这个顺序先看最直接的平台控制，再看弹性与观测，最后回到系统边界和真实迁移。

## 读这一章时建议带着一个场景

只读概念容易觉得 gateway 很抽象。建议你带着这个场景读：

```text
一个业务方调用 gpt-like 模型。
外部模型名是 ai-infra-chat。
内部主 upstream 暂时不可用。
gateway 尝试 fallback。
最终用户拿到了 200 响应。
```

然后问：

- 这次请求是否真的健康？
- 哪个 header 能说明 fallback 发生过？
- metrics 是否记录了主 upstream 失败？
- events 里能不能看到 request id 和 target？
- 如果 fallback 目标质量更差，eval 如何发现？
- 如果 cache 命中，这次请求还应该算作上游成功吗？

这样读，gateway 就不再是“多一层服务”，而是系统风险和系统证据的交汇点。

## 一条请求经过 Gateway 时发生什么

可以把一次请求理解成下面这条链路：

```text
Client
  -> Auth
  -> Rate limit
  -> Model routing
  -> Cache lookup
  -> Upstream request
  -> Fallback decision
  -> Response or streaming events
  -> Metrics and structured events
```

每一步都可能改变系统行为。

Auth 失败时，请求不会进入上游。Rate limit 触发时，请求也不会占用模型服务。Cache 命中时，请求可能不需要走 upstream。主 upstream 失败时，fallback 可能让用户仍然得到成功响应。Streaming 中途失败时，系统需要决定如何向客户端表达错误，并如何记录这次事件。

这也是为什么 gateway 的测试要覆盖很多错误路径，而不能只测 happy path。

## 和 Serving 模块怎么连起来

Gateway 不应该替代 serving，但它要理解 serving 的契约。

例如：

- serving 暴露 `/v1/models`，gateway 才能知道可用模型
- serving 暴露 `/health`，gateway 才能做健康聚合
- serving 暴露 `/metrics`，平台才能观察下游状态
- serving 返回 request id，gateway 才能串联排查
- serving 支持 streaming，gateway 才需要处理流式代理

在这个仓库里，`inference-service` 和 `ai-gateway` 正好构成一条学习链路：先有模型服务，再有平台治理。

## 学完这一章应该能回答的问题

读完后，你应该能说明：

- 为什么业务方不一定应该直接调用模型服务
- 为什么外部模型名和内部上游目标要解耦
- fallback 什么时候有价值，什么时候会掩盖问题
- response cache 为什么和 prefix cache 不是一回事
- request id 为什么是排查链路的最低成本投资
- streaming proxy 的错误处理为什么比非流式更难
- gateway 为什么需要自己的 metrics 和 events
- 真实平台化时要补哪些治理能力

这些问题比“有没有一个代理层”更重要。

## 最小实践路线

建议你这样动手：

1. 启动 `inference-service`。
2. 启动 `ai-gateway` 指向 inference service。
3. 用正确 token 调一次 chat completion。
4. 用错误 token 触发 401。
5. 调一个 unknown model 触发模型路由错误。
6. 连续调相同请求，观察 cache header。
7. 模拟上游失败，观察 fallback 与 metrics。
8. 查看 `/events`、`/events/summary`、`/events/failures`。

这套实践能把“平台治理”从抽象词变成可观察行为。

## 学习型 Gateway 和生产 Gateway 差在哪里

当前仓库故意保留轻量实现，不把它说成生产平台。生产级 gateway 通常还需要：

| 能力 | 学习型实现关注 | 生产级还要补 |
| --- | --- | --- |
| 鉴权 | Bearer token 和错误语义 | 租户、密钥轮换、权限范围、审计 |
| 限流 | 最小频率控制 | 分布式限流、配额、突发预算 |
| 路由 | 外部模型名到 target | 灰度、权重、地区、成本、能力标签 |
| Fallback | 失败后备用路径 | 熔断、重试预算、质量风险评估 |
| Cache | 最小响应缓存 | 用户隔离、隐私、TTL 策略、失效机制 |
| 观测 | metrics、events、timeline | tracing backend、dashboard、告警 |
| 配置 | 静态或轻量配置 | 版本化配置、回滚、审批、变更记录 |

学习时不需要一次补满这些能力，但要知道缺口在哪里。知道缺口，才不会把 demo 误当生产系统。

## 常见误区

### 误区一：Gateway 只是 Nginx 转发

不够。AI Gateway 的关键是模型名映射、鉴权、限流、fallback、cache、用量、事件、审计和多上游治理。

### 误区二：Fallback 一定是好事

Fallback 能提高可用性，但也可能掩盖主路径退化，或者引入质量差异。它必须被 metrics 和 events 记录。

### 误区三：Cache 只要命中率高就好

Response cache 要考虑用户隔离、数据新鲜度、提示词敏感性和安全边界。高命中率不等于一定合理。

### 误区四：Gateway 不需要懂模型

Gateway 不执行模型，但需要理解模型调用的输入、输出、streaming、错误和用量结构，否则治理就会很粗糙。

### 误区五：平台越早做得越重越好

学习阶段应该先把边界和证据做清楚，再逐步加租户、配额、审计、计费、策略引擎和 dashboard。
