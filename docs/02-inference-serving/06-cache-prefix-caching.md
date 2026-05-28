# Cache 与 Prefix Caching

Cache 在 LLM serving 里不是“锦上添花”。
它几乎会影响所有重要指标：

- TTFT
- ITL
- throughput
- 显存占用
- 并发能力
- 长上下文成本
- gateway 成本治理

如果你后面遇到这些问题：

- 为什么第二个请求更快？
- 为什么长上下文把并发打掉了？
- 为什么显存一下被吃满？
- 为什么 cache hit 后 TTFT 下降？
- 为什么 gateway cache 和 prefix cache 不是一回事？

很多时候最后都会回到 cache。

## 一个容易踩坑的场景

想象一个公开学习助手，每次请求都带同一段 system prompt：

```text
你是一个 AI Infra 学习助手，请用场景、机制、代码映射和误区解释问题。
```

如果请求结构稳定，serving runtime 可能复用这段公共前缀的计算状态。
如果团队后来为了排查方便，把动态 request id、当前时间、用户昵称都插到 prompt 最前面：

```text
request_id=...
current_time=...
user_name=...
你是一个 AI Infra 学习助手...
```

那么“公共前缀”就被打散了。
从业务代码看，只是多加了几个字段；从 serving 视角看，prefix caching 的命中可能明显下降。

这就是 Cache 章节最想建立的直觉：

> Prompt 结构、平台字段、用户隔离和 runtime cache 并不是互不相干的。

## 先分清三种 Cache

LLM 系统里常见的 cache 至少有三层。

| Cache 类型 | 所在层 | 复用什么 | 主要影响 |
| --- | --- | --- | --- |
| KV Cache | 模型执行层 | 已计算 token 的 key/value 状态 | decode 成本、显存 |
| Prefix Caching | serving runtime 层 | 共享前缀对应的 KV 状态 | prefill 成本、TTFT |
| Semantic / Response Cache | gateway/app 层 | 已生成响应或近似问题结果 | 成本、响应速度、上游压力 |

这三者都叫 cache，但语义完全不同。
学习时最容易混淆的就是把它们当成同一种东西。

## KV Cache 是什么

自回归模型每生成一个新 token，都要利用前面 token 的上下文。
如果每一步都从头计算整个历史，成本会非常高。

KV Cache 的作用是保存前文 token 的 key/value 状态，让后续 decode 不必重复计算全部历史。

它的关键点是：

- 它存在于模型执行过程里。
- 它和上下文长度强相关。
- 它占用显存。
- 它影响并发和长上下文能力。
- 它不是“返回内容缓存”。

所以 KV Cache 更像运行时状态，而不是应用层缓存。

## Prefix Caching 是什么

Prefix caching 关注的是：

> 多个请求共享相同前缀时，能不能复用这段前缀的 prefill 结果？

例如很多请求都包含同一个 system prompt：

```text
你是一个严谨的 AI Infra 学习助手。回答必须包含场景、机制、误区和仓库映射。
```

如果每次请求都重新 prefill 这段相同前缀，就会浪费。
prefix caching 想复用这段前缀对应的 KV 状态，从而减少重复 prefill。

它主要优化的是首 token 前的工作，也就是 TTFT 中和 prefill 相关的部分。

## Semantic / Response Cache 是什么

Semantic cache 或 response cache 更靠应用层或 gateway。

它关注的是：

> 这个问题是不是已经问过，能不能直接复用之前的回答？

这和 prefix caching 不同。

| 对比 | Prefix Caching | Semantic / Response Cache |
| --- | --- | --- |
| 复用对象 | 中间计算状态 | 最终响应 |
| 匹配条件 | token 前缀相同或可复用 | 问题相同或语义相似 |
| 所在层 | serving runtime | gateway/app |
| 主要风险 | 显存占用、命中率受 prompt 影响 | 越权、过期、错误复用 |
| 当前仓库表达 | 作为未来真实后端观察点 | gateway response cache |

当前 `ai-gateway` 的 cache 是 response cache 学习实现，不是 prefix cache。

## Prefix Caching 优化什么

它主要优化 prefill 的重复成本。

假设两个请求：

```text
Request A = system prompt + few-shot examples + user question A
Request B = system prompt + few-shot examples + user question B
```

前面很长一段完全相同。
如果 runtime 能复用共享前缀，第二个请求就可能减少 prefill 开销。

这不会让 decode 本身 magically 变快。
它更可能降低首 token 等待。

## 为什么它是工作负载敏感优化

Prefix caching 不是打开就一定明显加速。

它依赖：

- 请求之间是否真的共享前缀
- 共享前缀是否足够长
- cache 是否还在
- 显存是否足够
- runtime 是否正确识别复用
- 其他瓶颈是否掩盖收益

如果请求完全随机、前缀都不同，prefix caching 命中率就低。

因此它不是魔法开关，而是和 workload、prompt 设计、服务调度都有关。

## Cache 的代价

Cache 不是免费的。

尤其 KV Cache / prefix cache 会占用 GPU 显存。
显存给了 cache，就不能给其他用途。

系统需要权衡：

- 留更多 cache，提升重复请求表现。
- 留更多空间给 batch，提高并发。
- 清理旧 cache，避免 OOM。
- 保留长前缀，提升共享 prompt 场景。
- 限制长上下文，保护系统稳定性。

所以 cache 策略本质上是资源管理策略。

## Prompt 设计会影响 Cache

这是学习 prefix caching 最有价值的直觉之一：

> Prompt 不是纯应用层文本，它会影响基础设施行为。

例如：

- system prompt 稳定，有利于共享前缀。
- 每次请求都在最前面插入动态时间戳，可能破坏共享前缀。
- few-shot 示例顺序稳定，有利于复用。
- RAG 文档每次都不同，prefix reuse 可能下降。
- 把用户专属信息放在最前面，可能让公共前缀变短。

所以 prompt 组织方式会影响 serving 性能。

## Cache Key 应该包含什么

平台层 response cache 最容易出事故的地方，不是“有没有缓存”，而是 cache key 设计不完整。

一个粗糙的 cache key 可能只看：

```text
model + messages
```

但真实系统里，影响响应语义的字段很多：

| 字段 | 为什么可能影响 cache |
| --- | --- |
| 调用方 / token / tenant | 防止跨用户复用敏感结果 |
| 外部模型名和内部 target | 同名模型迁移后结果可能不同 |
| system prompt | 指令改变会改变输出 |
| messages | 用户输入本体 |
| temperature / top_p | 采样参数影响随机性 |
| tools / response format | 输出协议可能不同 |
| safety / policy version | 策略变化会改变可返回内容 |
| adapter / prompt version | 微调或提示词版本影响结果 |

学习项目里的 cache 可以保持简化，但文档需要让读者知道：生产 cache 的难点往往在语义边界，而不是字典读写。

一个更稳的原则是：

> 只缓存你能解释其等价性的请求。

如果你无法清楚说明两个请求为什么“应该得到同一个结果”，就不要急着把它们放进同一个 cache key。

## Cache 失效比 Cache 命中更重要

很多人设计 cache 时只盯命中率。
但 AI 系统里更危险的是错误命中和过期复用。

你至少要考虑：

- 模型升级后旧缓存是否还有效。
- prompt 版本变化后是否应该清空。
- 用户权限变化后是否还能复用旧结果。
- 训练 adapter 替换后 cache key 是否包含版本。
- 安全策略更新后旧回答是否还允许返回。
- 评测或发布回滚后是否要隔离 cache。

因此 cache 需要和发布流程相连。
当模型、prompt、adapter、policy 或路由目标变化时，cache 也要能解释自己是否仍然有效。

这也是为什么本项目把 cache、gateway、eval 和 production migration 放在同一个学习体系里：它们最终都会汇合到“系统变化如何被治理”这个问题。

## 当前仓库怎么对应

当前仓库还没有真实接入 vLLM/SGLang 的 prefix caching。
但它已经把观察路径留出来：

### Inference Service

```text
projects/inference-service/src/inference_service/server.py
projects/inference-service/src/inference_service/runtime.py
projects/inference-service/src/inference_service/engines.py
```

它提供：

- request id
- usage
- metrics
- events
- streaming
- engine adapter

这些是未来观察真实 cache 行为的外壳。

### Gateway

```text
projects/ai-gateway/src/ai_gateway/server.py
projects/ai-gateway/src/ai_gateway/runtime.py
```

它表达的是 response cache：

- `x-cache`
- cache hit/miss events
- token 隔离
- TTL
- eviction

这和 prefix caching 不同，但同样是成本治理的一部分。

## 最小实践建议

以后接真实后端后，可以做一个简单实验：

1. 准备一个长且稳定的 system prompt。
2. 连续发两条只改变 user message 的请求。
3. 记录 TTFT、总耗时、prompt token、cache 指标。
4. 再构造每次前缀都不同的请求作为对照。
5. 比较两组趋势。

目标不是严谨 benchmark，而是确认你能看见“共享前缀改变服务行为”。

## 排查 Cache 问题时的证据顺序

当你怀疑 cache 影响系统行为时，可以按这个顺序查：

1. 看响应 header：`x-cache` 是 hit 还是 miss。
2. 看 gateway events：是否记录 cache lookup、hit、miss、store。
3. 看 request id：同一请求是否真的没有进入下游。
4. 看模型和 target：cache 是否跨目标复用。
5. 看 token / tenant：cache 是否按调用方隔离。
6. 看 TTL 和 eviction：结果是否过期或被淘汰。
7. 看 eval 或 sample：缓存复用后质量是否仍然可接受。

这套顺序能帮助你区分几类问题：

| 现象 | 可能原因 |
| --- | --- |
| 本该 hit 却 miss | key 不稳定、prompt 动态字段过多、TTL 太短 |
| 本该 miss 却 hit | key 缺字段、版本未纳入、隔离不足 |
| hit 后质量变差 | 旧结果过期、模型或策略已变 |
| cache 降低成本但事故变多 | 只追命中率，没有发布联动和审计 |

## 常见误区

### “KV Cache 等于 Prefix Caching”

不等于。
KV Cache 是底层状态，prefix caching 是围绕共享前缀复用 KV 状态的策略。

### “Gateway cache 等于 prefix cache”

不等于。
gateway cache 复用最终响应，prefix cache 复用中间计算。

### “Cache 命中越多越好”

不一定。
cache 占资源，也可能带来隔离和过期风险。

### “只要开启 prefix caching 就会明显变快”

不一定。
它依赖工作负载和前缀复用比例。

### “Prompt 设计和基础设施无关”

不对。
prompt 的稳定性和结构会影响 prefix caching 命中。

## 学完应该能回答

读完这一页后，你应该能回答：

1. KV Cache、Prefix Caching、Response Cache 分别复用什么？
2. Prefix caching 主要优化 prefill 还是 decode？
3. 为什么 cache 会带来显存和并发取舍？
4. 为什么 prompt 组织方式会影响 cache 命中？
5. 当前仓库的 gateway cache 和未来真实后端 prefix cache 有什么不同？

## 继续阅读

- [Prefill、Decode 与 KV Cache](/01-llm-fundamentals/02-prefill-decode-kv-cache)
- [vLLM](/02-inference-serving/04-vllm)
- [SGLang](/02-inference-serving/05-sglang)
- [Gateway Router、Fallback 与 Cache](/03-ai-gateway-platform/03-gateway-router-fallback-cache)
