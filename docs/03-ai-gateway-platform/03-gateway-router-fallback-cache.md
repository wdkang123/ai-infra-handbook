# Gateway、Router、Fallback、Cache

## 为什么这一页要放在一起讲

Gateway、router、fallback、cache 经常在平台层混着出现，但它们不是同一件事。

如果你不把它们分开，后面很容易出现两种混乱：

- 把 router 误认为整个 gateway
- 把 fallback / cache 误认为只是附加优化

更好的理解方式是：

> 它们都属于平台层能力，但各自回答的问题不同。

可以先用一句话区分：

- Gateway 回答“统一入口在哪里”
- Router 回答“这条请求去哪里”
- Fallback 回答“主路径失败后怎么办”
- Cache 回答“哪些请求可以不再打到下游”

这四个能力叠在一起，才开始有平台层的味道。

## 一个请求穿过四层时发生了什么

先看一条看似普通的请求：

```json
{
  "model": "learning-chat",
  "messages": [
    {"role": "user", "content": "解释一下 KV Cache"}
  ],
  "stream": true
}
```

在业务方眼里，它只是一次模型调用。
在 gateway 里，它至少会经过四层判断：

```text
Gateway entrance
  -> Router decision
  -> Cache decision
  -> Upstream attempt
  -> Fallback decision if needed
```

每层都在回答不同问题：

| 层 | 关键问题 | 典型证据 |
| --- | --- | --- |
| Gateway | 谁在调用，是否允许进入 | `401`、auth event、request id |
| Router | 外部模型名对应哪个 target | `x-upstream-model`、route event |
| Cache | 是否能复用已有响应 | `x-cache`、cache hit/miss event |
| Fallback | 主路径失败后是否换候选 | `x-fallback-used`、fallback event |

如果你把这几层混成“转发”，排障时就会非常痛苦。
同样是一次成功响应，它可能是主路径成功，也可能是 cache hit，也可能是 fallback 成功。
这些路径对成本、质量和稳定性的含义完全不同。

## Gateway 在回答什么

Gateway 回答的是：

> 应用到底通过哪个统一入口来访问模型能力？

所以 gateway 往往要管：

- 入口协议
- 鉴权
- 模型名映射
- 请求转发
- 限流
- 健康检查
- metrics
- request id
- structured events
- cache / fallback 的外部语义

在当前仓库里，`ai-gateway` 就是这条主线的最小学习骨架。

它不负责真正执行模型推理，也不负责训练和评测。它的职责是让调用模型这件事被平台化治理。

## Router 在回答什么

Router 回答的是：

> 这条请求最终要发给哪个下游？

它经常只是 gateway 里的一部分，而不是完整平台本身。

你可以把它先理解成“决策器”，而不是“整个入口层”。

常见路由判断包括：

- 这个外部模型名映射到哪个内部 target
- 这个请求应不应该走备用模型
- 这个请求应不应该走测试版本
- 这个 token 或租户是否应该使用某个模型池
- 当前 upstream 是否健康
- 当前策略是否允许 fallback

当前项目的 router 不追求复杂策略，但已经保留了最重要的边界：外部模型名和内部上游目标不是同一个东西。

## 为什么外部模型名要和内部 target 解耦

如果调用方直接知道所有内部模型名，后续迁移会很痛苦。

例如你今天对外暴露：

```text
learning-chat
```

内部可以先指向 mock inference service，之后可以指向 vLLM、本地 SGLang、OpenAI-compatible upstream，甚至带 fallback 的 target 列表。

对调用方来说，外部模型名稳定；对平台来说，内部实现可以演进。

这就是 router 的价值。

## Fallback 在回答什么

Fallback 回答的是：

> 主要路径失败了以后怎么办？

它的价值不在“聪明切换”，而在“让平台在异常时仍然有可接受的退路”。

学习时你最应该理解的是：

- fallback 不是正常主路径
- fallback 是治理能力的一部分
- fallback 会影响稳定性、结果一致性和排障复杂度
- fallback 必须被记录

一个成熟平台不会把 fallback 当成“悄悄发生的小技巧”，而会把它当成明确的系统行为。

当前 gateway 会把 fallback 暴露成几类观察面：

- 单次响应里的 `x-upstream-model`
- 单次响应里的 `x-fallback-used`
- `/metrics` 里的 fallback attempts / successes
- `/events` 里的 `fallback_attempt` / `fallback_success`
- `/events/failures` 里的失败摘要

这样 fallback 不是静默发生，而是能被单次请求、最近事件和长期指标同时解释。

## Fallback 的风险

Fallback 不是越多越好。

它会引入几类风险：

| 风险 | 说明 |
| --- | --- |
| 质量不一致 | 备用模型可能回答风格或能力不同 |
| 成本变化 | 备用上游可能更贵 |
| 延迟增加 | 主路径失败后再尝试备用路径会增加耗时 |
| 问题被掩盖 | 用户成功拿到响应，但主 upstream 已经退化 |
| 复盘复杂 | 如果没有事件和 header，很难知道实际命中了谁 |

所以 fallback 的正确姿势不是“能 fallback 就行”，而是“fallback 可解释、可观测、可控制”。

## Fallback 什么时候不应该发生

Fallback 不是所有失败都能自动补救。
下面几类情况通常要谨慎：

| 场景 | 为什么谨慎 |
| --- | --- |
| 已经开始 streaming | 已输出内容属于主上游，再切换会造成语义混乱 |
| 请求有强一致要求 | 备用模型可能给出不同格式或不同事实判断 |
| 任务涉及安全边界 | 备用模型策略可能不同，不能无声切换 |
| 成本差异极大 | 主模型失败后切到昂贵模型可能造成预算失控 |
| eval / 发布评测 | fallback 会污染候选模型真实表现 |

所以 fallback 策略需要有开关、范围和证据。
它可以用于提升可用性，但不能变成掩盖系统退化的黑箱。

## Cache 在平台层又是怎么回事

平台层说 cache，通常不是在说底层 KV Cache。

更常见的是：

- 请求级 response cache
- semantic cache
- 某些高频 prompt 的复用层

它的价值更接近：

- 降低下游调用次数
- 降低成本
- 在重复问题场景里缩短响应时间
- 减少上游波动对用户的影响

平台层 cache 和推理引擎里的 prefix caching 是两条不同层次的主线。

| 类型 | 所在层 | 缓存对象 | 主要收益 | 主要风险 |
| --- | --- | --- | --- | --- |
| Response cache | Gateway | 完整响应 | 降低请求成本 | 用户隔离、过期、敏感内容 |
| Semantic cache | Gateway / App | 语义相近请求结果 | 复用相似问题 | 误命中、质量不可控 |
| Prefix caching | Serving runtime | 共享 prompt 前缀的 KV 状态 | 降低 prefill 成本 | 显存管理、prefix 稳定性 |
| KV Cache | Serving runtime | 单次生成上下文状态 | 加速 decode | 显存压力 |

把这些 cache 混起来，会导致设计判断出错。

## 当前仓库里的 Cache 如何理解

当前 `ai-gateway` 的 cache 更接近 response cache。

它关心的是：

- 相同 token / 请求是否能复用响应
- cache 是否过期
- cache 是否按 token 隔离
- cache 满时如何淘汰
- response header 如何显示命中状态

它不是在做 prefix caching，也不是在优化模型执行内部状态。

所以读这页时要记住：Gateway cache 是平台治理能力，不是推理 runtime 优化。

## 四者之间最容易混淆的边界

### Gateway 就是 Router

不对。

Router 通常只是 gateway 的一个核心内部能力。Gateway 还要处理 auth、rate limit、cache、fallback、health、metrics、events 等问题。

### Fallback 只是路由策略的一种

部分成立，但不够完整。

更准确地说，fallback 是路由体系里专门处理失败路径的策略，它背后牵涉可用性目标、质量风险和排障复杂度。

### 平台层 cache 和引擎层 cache 是同一回事

不是。

一个更靠减少外部请求或直接复用响应，一个更靠复用模型执行中的中间结果。

### Cache 命中率越高越好

不一定。

如果 cache 没有用户隔离、过期策略和可解释 header，高命中率也可能代表错误复用。

### Fallback 成功就说明系统健康

不一定。

Fallback 成功只能说明用户拿到了响应，不能说明主路径健康。主路径退化仍然应该进入 metrics 和 events。

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

也就是说，你现在已经能清楚看到 gateway 这个外层壳长什么样。

后面再往里面加更复杂 router、canary、semantic cache，会容易很多。

## 设计 Router 时最重要的不是策略多

Router 很容易被做成一个复杂配置中心。
但学习阶段最重要的不是策略数量，而是每个决策是否可解释。

一个可维护的 router 至少应该回答：

- 这个外部模型名当前有哪些候选 target？
- 候选 target 的顺序为什么是这样？
- 哪些 target 是主路径，哪些是 fallback？
- 这个调用方是否允许访问这些 target？
- target 健康状态如何影响决策？
- 决策结果是否写入 header、metrics 或 events？

如果路由策略很复杂，却不能解释“为什么这条请求去了这个上游”，平台会很快变成黑箱。

所以 router 的第一目标不是聪明，而是可审计。

## 推荐的学习顺序

1. 先把 gateway 当成统一入口。
2. 再把 router 看成入口内部的决策器。
3. 再看 fallback 如何处理失败路径。
4. 再看 cache 如何帮助成本和延迟治理。
5. 最后把 headers、metrics、events 放在一起复盘。

这样学，你就不会把所有平台能力都挤进一个抽象词里。

## 实操观察

建议你至少观察这些信号：

- 成功请求是否带 `x-request-id`
- 成功请求是否带 `x-upstream-model`
- fallback 时 `x-fallback-used` 是否变化
- cache 命中时 `x-cache` 是否变化
- `/metrics` 是否出现 fallback / cache 相关计数
- `/events` 是否能看到请求、失败、fallback
- `/events/failures` 是否能聚合失败状态

如果这些信号都能解释，你对 gateway 的平台能力就不只是知道名词了。

## 小型设计练习

读完这一页，可以尝试设计一个最小模型路由表：

```yaml
models:
  - name: learning-chat
    primary: mock-inference
    fallbacks:
      - mock-inference-backup
    cache:
      enabled: true
      ttl_seconds: 60
```

然后回答：

- `learning-chat` 是外部模型名还是内部模型名？
- `mock-inference` 的健康状态从哪里来？
- 如果 primary 返回 500，fallback 是否允许？
- 如果请求是 streaming，fallback 的边界在哪里？
- cache key 是否包含调用方 token？
- 响应 header 要暴露哪些决策结果？
- metrics 里要记录哪些计数？

这个练习不需要你马上实现复杂系统。
它的价值是训练你把平台策略写成可解释契约。

## 这一章学完应该带走什么

Gateway 是统一入口，router 是决策器，fallback 是失败路径策略，cache 是成本和延迟治理能力。

它们都属于平台层，但解决的问题不同。

真正有用的平台设计，不是把这些能力堆上去，而是让每个能力都有清楚边界、可观察证据和失败语义。
