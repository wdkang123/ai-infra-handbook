# TTFT、ITL、吞吐

性能讨论里最容易出问题的一句话是：

> 这个模型很快。

“快”到底是什么意思？
是用户多久看到第一个 token？是回答过程中 token 出得是否平滑？是系统一秒能处理多少 token？还是高并发下排队是否稳定？

AI Infra 里要把这些问题拆开看。
这页先建立三个核心指标：

- TTFT：Time To First Token
- ITL：Inter-Token Latency
- Throughput：吞吐

它们分别回答不同问题，也经常互相冲突。

## 三个指标分别看什么

| 指标 | 直觉 | 主要影响体验 |
| --- | --- | --- |
| TTFT | 多久开始说话 | 用户等待第一下响应 |
| ITL | 说话中间卡不卡 | streaming 是否顺滑 |
| Throughput | 总体产能有多高 | 系统能服务多少并发和 token |

如果把 LLM 响应想象成一次对话：

- TTFT 是对方沉默多久才开口。
- ITL 是对方开口以后说得是否断断续续。
- throughput 是整个服务大厅每分钟能接待多少人。

这三个问题都重要，但不能混为一谈。

## TTFT 是什么

TTFT 可以理解成：

> 从请求进入系统，到客户端看到第一个输出 token 的时间。

它特别影响用户体感。
如果 TTFT 很高，用户会觉得服务卡住了，即使后面 token 出得很快，第一印象也已经变差。

TTFT 通常由多段时间叠加：

| 阶段 | 可能贡献 |
| --- | --- |
| 客户端到网关 | 网络、TLS、客户端重试 |
| 网关处理 | 鉴权、限流、路由、cache、fallback |
| 服务排队 | 并发拥堵、batch 等待、调度策略 |
| prefill | 处理 prompt/context token |
| 第一次 decode | 生成第一个 token |
| streaming flush | 服务端把首个 chunk 发给客户端 |

所以 TTFT 不是单纯的“模型速度”。
它是端到端系统指标。

## 为什么长上下文会推高 TTFT

如果你读过 [Prefill、Decode 与 KV Cache](/01-llm-fundamentals/02-prefill-decode-kv-cache)，会知道模型生成前要先处理已有上下文。

这一步就是 prefill。
prompt token 越多，prefill 通常越重。

所以一种常见现象是：

- 用户当前输入很短
- 但历史对话、RAG 文档和 system prompt 很长
- `prompt_tokens` 很高
- 用户等很久才看到第一个 token

此时问题可能不是 decode 慢，而是 prefill 或排队慢。
如果你只看输出速度，就会误判。

## ITL 是什么

ITL 可以理解成：

> streaming 过程中，相邻两个输出 token 之间的时间间隔。

如果 TTFT 决定“多久开始说话”，ITL 决定“开始以后是否流畅”。

用户对 ITL 的感受很直接：

- 间隔稳定：回答像持续生成，体感顺。
- 间隔忽快忽慢：回答像卡顿。
- 间隔很长：用户会怀疑连接或服务出问题。

ITL 通常受这些因素影响：

- decode 阶段每步计算成本
- batch 调度
- 当前并发
- GPU 利用率
- 采样参数
- 输出长度
- streaming buffer 和网络 flush

注意，ITL 不是总耗时。
一个回答总共生成 1000 token，即使 ITL 很低，总时间仍然会长；一个回答只生成 20 token，即使 ITL 一般，用户也可能觉得可以接受。

## Throughput 是什么

throughput 关心的是系统总体产能。
在 LLM serving 中，它常见的表达方式包括：

- requests per second
- prompt tokens per second
- completion tokens per second
- total tokens per second
- concurrent running requests
- batch utilization

对平台来说，throughput 决定系统能承受多少流量、单位硬件成本能处理多少工作量。

但 throughput 不是单请求体验。
系统吞吐高，不代表每个用户都觉得快；单个用户体验好，也不代表系统总体资源利用率高。

## 三者为什么经常冲突

LLM serving 的很多优化，本质都是取舍。

### 更大的 batch 可能提高吞吐

batching 能让 GPU 更充分地工作。
但如果为了攒 batch 让请求等更久，TTFT 可能变差。

### 更激进的并发可能提高利用率

更多请求同时进入系统，可能让吞吐更高。
但调度、显存和 KV Cache 压力也会上升，导致 ITL 抖动或失败率变高。

### 更长上下文可能提高能力

更长 context 可以放入更多历史和检索材料。
但 prefill 成本增加，TTFT 和成本都会上升。

### 更长输出可能提升答案完整性

较大的 `max_tokens` 能让模型回答更完整。
但 completion token 增加会拉长总时间，也会占用 decode 资源。

所以性能优化不是把一个数字拉满，而是先明确目标。

## 一个具体诊断场景

假设用户反馈：“网站上的 AI 回答很慢。”

你不应该马上说“换更快模型”或“加机器”。
更合理的拆法是：

1. 第一个 token 是否慢？
2. 第一个 token 出来后是否卡顿？
3. 只有单个用户慢，还是所有用户都慢？
4. 慢请求的 prompt token 是否明显更高？
5. gateway 是否发生了 fallback、cache miss 或 upstream retry？
6. `/metrics` 里的 running requests 是否很高？
7. `/events/requests/{request_id}` 的 timeline 显示卡在哪一层？

对应判断：

| 现象 | 更可能关注 |
| --- | --- |
| 首 token 很晚才出来 | TTFT、prefill、排队、网关处理 |
| 首 token 后断断续续 | ITL、decode、batch 调度、网络 flush |
| 高峰期整体变慢 | throughput、并发、资源利用率 |
| 长文档请求慢 | prompt token、context、prefill |
| 失败后才慢 | gateway fallback、上游重试 |

这样排查才不会把所有性能问题都归因到“模型慢”。

## 当前仓库怎么表达

当前仓库是学习型实现，没有真实 GPU scheduler，也不会提供生产级 latency histogram。
但它已经把观察性能的几个入口搭好了。

### `inference-service`

相关文件：

```text
projects/inference-service/src/inference_service/server.py
projects/inference-service/src/inference_service/runtime.py
projects/inference-service/src/inference_service/engines.py
```

你可以观察：

- `/v1/chat/completions` 是否普通响应或 streaming 响应
- `usage.prompt_tokens` 和 `usage.completion_tokens`
- `/metrics` 中的 request/token counters
- `/events` 中的 `request_received`、`engine_generate_start`、`request_success`
- `/events/requests/{request_id}` 的 timeline

这些信号虽然不等同于真实 TTFT/ITL，但它们让你建立“请求生命周期可观察”的习惯。

### `ai-gateway`

相关文件：

```text
projects/ai-gateway/src/ai_gateway/server.py
projects/ai-gateway/src/ai_gateway/runtime.py
```

你可以观察：

- 鉴权失败是否增加
- rate limit 是否触发
- cache hit / miss 是否变化
- fallback attempt / fallback success 是否出现
- `x-request-id` 是否贯穿
- `x-upstream-model` 是否说明实际走了哪个上游

如果 TTFT 变差，gateway 也可能是原因之一。
例如 cache miss 后访问慢上游、主上游失败后 fallback、或者限流前排队策略不合理。

## 该怎么设计指标

真实系统里，建议把指标分层：

| 层 | 应该看什么 |
| --- | --- |
| 客户端体验 | TTFT、总耗时、streaming 中断 |
| 网关层 | 鉴权、限流、路由、fallback、cache、upstream latency |
| 推理服务层 | queue time、prefill time、decode time、running requests |
| 模型运行时 | batch size、KV Cache、GPU utilization、tokens/sec |
| 业务层 | 成功率、用户取消率、成本、满意度 |

学习阶段不需要一次性实现所有指标。
但读文档和写代码时要知道：不同指标属于不同层。

## 常见误区

### “吞吐高就代表用户体验好”

不一定。
吞吐高可能来自更大的 batch，但用户可能等更久才看到第一个 token。

### “TTFT 高一定是模型慢”

不一定。
TTFT 包含网关、排队、prefill、首 token 生成和网络 flush。

### “Streaming 一定更快”

streaming 不一定让总耗时更短，它主要改善体感。
如果 TTFT 很高，用户仍然会先等很久。

### “只看 requests per second 就够了”

不够。
一个 20 token 请求和一个 20000 token 请求不是同一种负载。LLM 系统必须同时看 request 和 token。

### “平均值能代表性能”

平均值经常掩盖尾部问题。
真实系统通常还要看 p50、p95、p99、超时率和失败率。

## 学完应该能回答

读完这一页后，你应该能回答：

1. TTFT、ITL、throughput 分别描述什么？
2. 为什么优化吞吐可能伤害 TTFT？
3. 为什么长上下文请求首 token 可能更慢？
4. 如何用 request id、events 和 metrics 拆解一次“慢请求”？
5. 当前仓库有哪些入口能帮助你建立性能观察习惯？

## 继续阅读

- [模型、Token、Context](/01-llm-fundamentals/01-model-token-context)
- [Prefill、Decode 与 KV Cache](/01-llm-fundamentals/02-prefill-decode-kv-cache)
- [服务选型与取舍](/02-inference-serving/03-serving-tradeoffs)
- [请求失败排查案例](/11-case-studies/01-request-incident-walkthrough)
