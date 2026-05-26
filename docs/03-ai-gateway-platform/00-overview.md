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

## 推荐阅读顺序

1. [鉴权、路由、限流](/03-ai-gateway-platform/01-auth-routing-rate-limit)
2. [健康检查、Metrics、Request ID](/03-ai-gateway-platform/02-health-metrics-request-id)
3. [Gateway、Router、Fallback、Cache](/03-ai-gateway-platform/03-gateway-router-fallback-cache)
4. [Streaming、错误路径、Upstream Health](/03-ai-gateway-platform/04-streaming-errors-upstream-health)
5. [平台层与模型服务层边界](/03-ai-gateway-platform/05-platform-vs-model-service)
6. [外部模型名与内部目标映射](/03-ai-gateway-platform/06-model-name-to-target-mapping)
7. [从 Demo Gateway 到真实平台](/03-ai-gateway-platform/07-from-demo-gateway-to-real-platform)

这个顺序先看最直接的平台控制，再看弹性与观测，最后回到系统边界和真实迁移。

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
