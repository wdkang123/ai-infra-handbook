# 从请求到首个 Token

很多 AI Infra 术语之所以显得抽象，是因为它们被拆散了讲。

你看到：

- gateway
- auth
- routing
- prefill
- decode
- KV Cache
- TTFT
- streaming
- metrics
- request id

如果没有一条完整请求链路把它们串起来，这些词就像散在桌面上的零件。
这页要做的事，就是把“一次请求从进入系统到第一个 token 出现”完整走一遍。

读完以后，你应该能把慢请求、首 token 慢、streaming 卡顿、gateway fallback、token usage 和 request timeline 放到同一张图里理解。

## 先看最粗链路

一条 chat completion 请求，最粗可以拆成七段：

```text
client
  -> gateway
  -> route/auth/rate limit/cache
  -> inference-service
  -> prefill
  -> first decode step
  -> first token returned
```

如果继续生成，就进入后续 decode 和 streaming 阶段：

```text
first token
  -> decode next token
  -> stream chunk
  -> decode next token
  -> stream chunk
  -> done
```

所以“首个 token”不是模型内部某个孤立瞬间。
它是整条系统路径第一次对用户可见的结果。

## 为什么首个 token 特别重要

用户对 LLM 应用的第一感受，往往不是总耗时，而是：

> 它有没有开始回应？

如果用户等了 6 秒才看到第一个字，即使后面 2 秒输出完，也会觉得系统慢。
反过来，如果 1 秒内出现首 token，后面慢一点，体感可能还能接受。

这就是 TTFT 要单独讨论的原因。
它不是“总耗时”的替代指标，而是用户开始获得反馈的时间。

## 首 token 之前到底发生了什么

首 token 前通常已经经历了多层工作。

| 阶段 | 发生什么 | 可能造成什么问题 |
| --- | --- | --- |
| 客户端发起请求 | 准备 messages、model、参数、header | payload 过大、超时、重复请求 |
| Gateway 接入 | 生成或透传 `x-request-id` | 没有 request id 难以复盘 |
| 鉴权 | 检查 bearer token | 401、租户权限问题 |
| 限流 | 判断是否超过配额 | 429、峰值流量被拒绝 |
| 模型路由 | 外部模型名映射到内部目标 | 404、走错上游 |
| Cache 判断 | 命中则直接返回，未命中继续下游 | cache miss 增加等待 |
| Fallback 准备 | 主上游失败后可能切备用 | TTFT 变长但最终成功 |
| Inference 接收 | 执行层校验模型与消息 | 422、404、engine error |
| Prompt/token 处理 | messages 变成模型上下文 | prompt token 很大 |
| Prefill | 模型处理已有上下文 | 长上下文推高 TTFT |
| 首次 decode | 生成第一个 token | sampling、调度、KV Cache 状态影响 |
| Stream flush | 把首个 chunk 发给客户端 | buffer、网络、代理影响体感 |

这张表的重点是：TTFT 是端到端指标。
它可能卡在 gateway，也可能卡在 inference，也可能卡在模型 prefill。

## 一个具体慢请求场景

假设用户说：

> 我这次就问了一句话，为什么等这么久才开始回答？

从界面看，用户确实只输入了一句话。
但系统实际看到的可能是：

- system prompt 900 token
- 历史对话 7000 token
- RAG 检索片段 4000 token
- 当前问题 20 token
- JSON 输出格式要求 500 token

这次请求的 `prompt_tokens` 可能超过 12000。
用户当前输入短，不代表模型上下文短。

如果这条请求还经历了：

- cache miss
- 主上游 502
- fallback 到备用模型

那么用户看到首 token 之前，可能已经走完了一条很长的路径。
这就是为什么只看“用户输入长度”会误判。

## 普通响应和 Streaming 的差别

普通响应下，客户端通常要等完整答案生成后才收到结果。
这时用户看到的是总耗时。

streaming 下，服务端可以在 token 生成过程中不断返回 chunk。
这时你可以拆开观察：

- TTFT：首个 chunk 什么时候到
- ITL：后续 chunk 是否平滑
- total latency：全部结束花多久
- interruption：中途是否错误或断流

streaming 的价值不只是“看起来更丝滑”。
它改变了你观察系统的方式。

## 为什么 Gateway 也影响首 token

很多人会下意识把 TTFT 归因到模型。
但 gateway 也可能明显影响首 token。

例如：

- auth 依赖变慢
- rate limit 存储变慢
- router 查不到模型后重试
- cache 未命中
- 主上游失败后 fallback
- gateway 代理 streaming 时 buffer 不合理

这就是为什么 [健康检查、Metrics、Request ID](/03-ai-gateway-platform/02-health-metrics-request-id) 要单独讲。
没有 gateway 事件，你只能看到“模型服务最后有没有返回”，看不到入口层发生了什么。

## 为什么 Prefill 是首 token 的关键

从模型执行角度看，首 token 之前最重要的是 prefill。
prefill 要处理 prompt/context 中已经存在的 token。

这一步完成后，模型才开始 decode 第一个新 token。
因此：

- `prompt_tokens` 越大，prefill 通常越重。
- 历史上下文越长，TTFT 越可能上升。
- RAG 塞入无关长文档，会让首 token 变慢。
- prefix cache 命中时，某些重复前缀的 prefill 成本可能下降。

所以排查 TTFT 时，一定要先看 prompt/context，而不是只看 completion 长度。

## 当前仓库怎么表达

当前仓库不是生产级 serving stack，但已经把这条链路拆成可观察对象。

### Gateway 层

相关文件：

```text
projects/ai-gateway/src/ai_gateway/server.py
projects/ai-gateway/src/ai_gateway/router.py
projects/ai-gateway/src/ai_gateway/runtime.py
```

你可以观察：

- `x-request-id`
- `x-cache`
- `x-upstream-model`
- `x-fallback-used`
- `/events/requests/{request_id}`
- `/events/failures`
- `/metrics`

这些信号回答：请求在入口治理层发生了什么。

### Inference 层

相关文件：

```text
projects/inference-service/src/inference_service/server.py
projects/inference-service/src/inference_service/engines.py
projects/inference-service/src/inference_service/runtime.py
```

你可以观察：

- `usage.prompt_tokens`
- `usage.completion_tokens`
- `usage.total_tokens`
- 普通响应与 streaming 响应
- `/events/requests/{request_id}`
- `/metrics`

这些信号回答：请求在执行层如何被处理。

## 如何复盘一条首 token 慢的请求

学习时可以按这个顺序：

1. 从客户端响应 header 里拿到 `x-request-id`。
2. 查 gateway timeline，看是否 auth、rate limit、cache、fallback 或 upstream error。
3. 看 `x-cache`，判断是否命中 cache。
4. 看 `x-upstream-model` 和 `x-fallback-used`，确认真实上游。
5. 查 inference timeline，看 engine 是否开始生成、是否成功。
6. 看响应 usage，尤其是 `prompt_tokens`。
7. 看 `/metrics`，判断是单条请求慢，还是整体 running requests 或失败率异常。
8. 如果是 streaming，观察首 chunk 和后续 chunk 的间隔差异。

这个流程让“慢”变成可以定位的系统问题。

## 一条请求的简化心智模型

可以把端到端链路记成：

```text
入口治理时间
+ 排队/调度时间
+ prefill 时间
+ 首次 decode 时间
+ 首 chunk flush 时间
= TTFT
```

后续输出则更接近：

```text
多次 decode
+ 多次 stream flush
= 用户看到的生成节奏
```

这不是严格公式，但足够帮助你定位问题属于哪一类。

## 常见误区

### “TTFT 就是模型首 token 生成速度”

不完整。
TTFT 包含客户端、gateway、排队、prefill、decode 和网络 flush。

### “用户输入短，所以 prefill 一定短”

不一定。
模型看到的是完整 context，不只是当前输入。

### “Streaming 会让模型生成更快”

streaming 主要改善体感和可观察性，不一定降低总生成时间。

### “请求成功就说明路径正常”

不一定。
成功请求也可能经历 fallback、cache miss 或慢上游。

### “只看总耗时就够了”

不够。
总耗时不能区分首 token 慢和后续 token 慢，也不能解释 gateway 是否参与了问题。

## 学完应该能回答

读完这一页后，你应该能回答：

1. 首 token 之前通常经历哪些系统阶段？
2. 为什么 TTFT 不是单纯模型指标？
3. 为什么长上下文会推高首 token 等待？
4. gateway 的 cache、fallback、routing 为什么会影响体感延迟？
5. 当前仓库如何用 `x-request-id`、events、metrics 和 usage 复盘请求？

## 继续阅读

- [模型、Token、Context](/01-llm-fundamentals/01-model-token-context)
- [Prefill、Decode 与 KV Cache](/01-llm-fundamentals/02-prefill-decode-kv-cache)
- [TTFT、ITL、吞吐](/01-llm-fundamentals/03-ttft-itl-throughput)
- [请求失败排查案例](/11-case-studies/01-request-incident-walkthrough)
