# Streaming、错误路径、Upstream Health

## 为什么平台层不只处理成功请求

很多人学 gateway 时，会先把注意力放在一条正常代理链路上：

- 请求进来
- 鉴权通过
- 路由成功
- 下游返回结果

这条路径当然重要，但真正让平台层变得像平台的，往往不是成功路径，而是边界路径：

- `stream=true` 时会发生什么
- 下游挂掉时怎么表现
- 鉴权失败、模型不存在、限流命中时要不要统一返回结构
- `/health` 到底是在说“我活着”，还是“我的下游也大致正常”
- 已经开始返回 streaming chunk 后，上游失败怎么表达

这些问题会直接决定系统是不是可运维。

## Streaming 为什么值得单独看

一旦进入 streaming，请求就不再只是一个简单的“收包再回包”流程。

非流式请求更像：

```text
client -> gateway -> upstream -> gateway -> client
```

Streaming 请求更像：

```text
client
  -> gateway
  -> upstream stream starts
  -> chunk 1
  -> chunk 2
  -> ...
  -> done or error
```

这时平台层至少要面对：

- 上游事件流怎么继续往外转
- 中途出错时如何结束流
- request id 和日志怎么对齐
- metrics 要记完整请求，还是记事件流过程
- structured events 要记录 attempt、fallback、success 还是 stream error
- 客户端已经收到部分内容后，还能不能改 HTTP status

所以 streaming 不是普通代理逻辑上加一个布尔值那么简单。

它会把“gateway 是不是只是透明代理”这个问题直接放大。

## 首 chunk 前和首 chunk 后为什么不同

当前 `ai-gateway` 的处理原则是：

- 如果首个 chunk 之前下游 `5xx` 失败，可以尝试 fallback。
- 如果所有候选都失败，或者已经开始输出后才失败，就在 SSE 中发出结构化 `error` 事件并结束流。

这个边界非常关键。

在首 chunk 之前，客户端还没有收到模型内容，gateway 可以更安全地切换备用上游。

在首 chunk 之后，客户端已经收到一部分主上游内容。如果这时再悄悄切换到备用模型，可能会出现：

- 前半段来自模型 A
- 后半段来自模型 B
- 风格和事实不一致
- 客户端无法判断回答来源

所以首 chunk 后的失败更适合清楚表达错误，而不是继续伪装成功。

## Streaming Error Event 的价值

Streaming error event 的价值是让客户端至少能拿到结构化失败对象，而不是只看到连接断开。

它能帮助客户端判断：

- 是上游失败
- 是所有 fallback 都失败
- 是 stream 中途错误
- request id 是什么
- 是否可以重试

这对真实产品很重要，因为 streaming UI 最怕“卡住但不知道为什么”。

## 当前仓库里为什么要做最小 streaming 透传

因为这非常适合学习。

如果一开始就做复杂重试、背压、取消传播、流控和连接池，你会很容易被实现细节淹没。

而现在这套最小 streaming 透传，正好能让你先看清楚：

- inference-service 可以流式吐结果
- ai-gateway 可以继续把这条流转发出去
- streaming 和普通 JSON 响应在系统组织上不同
- 错误路径要保留结构化语义
- fallback 不是任何时候都能安全发生

这已经足够建立第一层工程直觉。

## 错误路径为什么不是以后再补

平台层的职责之一，就是把失败变成可理解、可治理的系统行为。

学习阶段最值得先掌握的几类错误是：

| 状态 | 更可能说明 | 所在层 |
| --- | --- | --- |
| `401` | 入口不合法 | Gateway auth |
| `404` | 模型或目标不存在 | Gateway route 或 Serving model check |
| `429` | 调用方超过预算 | Gateway rate limit |
| `502` | 上游失败，平台拿不到正常结果 | Gateway upstream 或 Serving engine |
| streaming error event | 流式过程中失败 | Gateway / upstream stream |

这几类错误很有代表性，因为它们分别对应不同层次的问题：

- 身份
- 路由
- 治理
- 下游可用性
- 流式传输状态

如果错误路径没有被明确设计，系统就只能在失败时给出模糊信号。

## Upstream Health 到底表达什么

这是最容易被简化错的地方。

一个服务自己的 `/health` 可以很简单：

> 进程活着、配置加载了、路由注册了。

但 gateway 的 `/health` 如果要更有意义，就不能只说“我自己活着”。

它还应该尽量知道：

- 我依赖的下游是不是活着
- 如果下游死了，我是 `healthy`、`degraded` 还是 `unhealthy`
- 哪些 upstream 影响了整体状态
- 当前是否还有可用 fallback

当前仓库里已经把这件事做到最小真实探测：gateway 会探测 upstream health，并在失败时把顶层状态降成 `degraded`。

这一步很有学习价值，因为它让你看到：

- 平台层健康状态通常不是单机进程概念
- 它会天然带有依赖传播
- health payload 的状态语义比单纯 HTTP 200 更重要

## Health、Metrics、Events 的关系

这三者不是替代关系。

| 面向 | 主要回答 |
| --- | --- |
| `/health` | 当前是否大致可用 |
| `/metrics` | 一段时间内发生了多少请求、失败、fallback、cache |
| `/events` | 最近具体发生了哪些结构化事件 |

例如：

- `/health` 告诉你 upstream degraded
- `/metrics` 告诉你 upstream failures 增多
- `/events/failures` 告诉你具体失败状态和模型分布
- request timeline 告诉你某条请求经历了什么

排障时不要只看一个面。

## 当前仓库里怎么对照看

如果你想把这一章和代码对应起来，最值得看：

- `projects/ai-gateway/src/ai_gateway/server.py`
- `projects/ai-gateway/src/ai_gateway/router.py`
- `projects/ai-gateway/tests/test_proxy.py`
- `scripts/integration_smoke_test.sh`

你会看到这里不是在做“花哨网关”，而是在把学习最重要的边界落成可观察行为。

重点看这些测试路径：

- health reflects unhealthy upstream
- missing auth returns 401
- rate limit returns 429
- upstream failure returns 502
- stream proxy success
- stream proxy fallback before first chunk
- stream proxy emits error after first chunk
- metrics reflect error paths

测试名称本身就是学习地图。

## 实操观察建议

可以按下面顺序观察：

1. 正常调用 gateway。
2. 记录 `x-request-id`。
3. 触发无认证请求，看 `401`。
4. 触发 unknown model，看 `404`。
5. 触发 rate limit，看 `429`。
6. 模拟 upstream failure，看 `502` 或 fallback。
7. 发 streaming 请求，观察 SSE chunk。
8. 查看 `/events/failures`。
9. 查看 `/events/requests/{request_id}`。

这条路径会让你看到平台层不是只有转发，还有失败治理。

## 学习时常见误区

### Streaming 只是响应格式不同

不够准确。

它通常会牵动代理方式、错误处理、日志、指标和排障方式。

### 错误路径只是补测试用的

不对。

平台层真正的价值之一，就是把失败清楚地表达出来，而不是让失败变成混乱。

### Health 只要 200 就行

也不对。

200 只是传输层面，health payload 的结构和状态语义同样重要。

### Fallback 可以解决所有 upstream 问题

不能。

Fallback 能提高可用性，但不能替代主路径修复，也不能保证质量一致。

### Stream 开始后还可以随便换模型

不建议。

首 chunk 后切换模型会让一个回答混合多个来源，排障和用户体验都会变差。

## 这一章学完应该带走什么

平台层真正的成熟度，很多时候不是看它正常代理时多顺，而是看：

- streaming 时是否还能保持边界清晰
- 失败时是否给出可理解路径
- 健康状态是否包含对下游依赖的最小真实判断
- metrics 和 events 是否能解释失败

这些能力会让 gateway 从“代理”变成“平台入口”。
