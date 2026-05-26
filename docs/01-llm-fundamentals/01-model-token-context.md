# 模型、Token、Context

这页是后面所有 AI Infra 内容的地基。

如果只从产品体验看，大模型像是在“读懂问题并回答”。
但从工程系统看，一次请求更接近这样：

1. 客户端把消息、参数和模型名发到服务端。
2. 服务端把消息转换成模型能处理的 token 序列。
3. 模型基于已有 token 预测下一个 token。
4. 新 token 被接回上下文，再继续预测下一个 token。
5. 服务端把 token 解码成人能读的文本，按普通响应或 streaming 返回。

这个视角一旦建立，后面的很多问题都会变得更清楚：为什么长上下文慢，为什么 token usage 是计费和限流基础，为什么 KV Cache 会占显存，为什么评测报告要保留 prompt/completion token，为什么 gateway 不能只按“请求次数”治理系统。

## 模型不是一个普通函数

在工程语境里，可以先把模型粗略理解成：

> 一个根据上下文预测下一个 token 的巨大函数。

这个说法不完整，但非常有用。它提醒我们三件事：

- 模型处理的不是原始自然语言，而是 token 序列。
- 模型不是一次性“吐出整段答案”，而是逐 token 生成。
- 模型每一步都依赖已经看过的上下文。

所以，当你看到一个 chat completion 接口时，不要只看成：

```text
question -> answer
```

更接近真实过程的是：

```text
messages -> tokens -> prefill -> decode token 1 -> decode token 2 -> ... -> text
```

这也是为什么 AI Infra 不是简单包一层 HTTP。
服务端要处理 token 统计、上下文长度、流式输出、缓存、排队、限流、错误复盘和成本治理。

## Token 到底是什么

token 不是“一个汉字”，也不是“一个英文单词”。
它是模型 tokenizer 切出来的最小处理单元。

不同模型的 tokenizer 可能不同，同一句话在不同模型里可能切成不同 token。
同一段文字里，中文、英文、数字、符号、空格、代码、JSON，也可能被切出完全不同的粒度。

因此，不要用字符数直接等价 token 数。
字符数只能粗略估计，真正的工程指标通常要看 token 数。

## 为什么 token 是工程里的核心单位

token 之所以重要，是因为它同时影响能力、成本和性能。

| 维度 | token 为什么重要 |
| --- | --- |
| 成本 | 很多模型 API 按输入 token 和输出 token 计费 |
| 延迟 | 输入 token 越多，prefill 越重；输出 token 越多，decode 越久 |
| 吞吐 | 系统最终处理的是 token 工作量，不只是请求数 |
| 显存 | 长上下文和 KV Cache 会增加显存压力 |
| 限流 | 只按 request 限流容易放过超长上下文请求 |
| 评测 | 不记录 token usage，很难比较不同 prompt 或模型的真实成本 |

这就是为什么你会在 OpenAI-compatible 响应里看到：

```json
{
  "usage": {
    "prompt_tokens": 128,
    "completion_tokens": 64,
    "total_tokens": 192
  }
}
```

这里的含义不是“顺手返回一个统计字段”，而是在告诉平台：

- 这次输入有多重
- 这次输出有多长
- 这次请求总体消耗了多少模型处理量

## Prompt Token 和 Completion Token

在一次 chat completion 中，可以先把 token 分成两类：

| 字段 | 含义 | 常见影响 |
| --- | --- | --- |
| `prompt_tokens` | 模型开始生成前已经看到的 token | prefill 延迟、上下文成本、KV Cache 初始占用 |
| `completion_tokens` | 模型实际生成出来的 token | decode 时长、streaming 输出长度、回答成本 |
| `total_tokens` | 二者之和 | 单次请求总体消耗 |

这三个字段经常能解释很多现象。

例如，一个用户说“模型怎么等了很久才开始回答”，你不能只看输出长度。
如果 `prompt_tokens` 很大，问题可能在 prefill；如果 `completion_tokens` 很大，问题可能是回答本身太长；如果两者都不大，则可能是排队、上游故障、网关重试或 batch 调度。

## Context 是什么

context 可以理解成：

> 模型这次生成时能够看到的全部 token 窗口。

在 chat 场景里，它通常包括：

- system prompt
- developer 或 policy instruction
- 历史 user / assistant 消息
- 当前 user 输入
- RAG 检索片段
- 工具调用结果
- 约束格式的 JSON schema 或输出说明

这些内容最后都会变成 prompt token，进入模型的上下文窗口。

所以 context 不是一个抽象概念，它会直接变成：

- 更长的输入 token
- 更重的 prefill
- 更大的 KV Cache
- 更高的费用
- 更容易触碰模型上下文长度上限

## 上下文窗口不是越大越好

很多初学者会自然地认为：上下文越大，模型知道的信息越多，所以一定更好。
真实工程里这只说对了一半。

更大的 context 确实能容纳更多历史、文档和工具结果，但它也带来几个问题：

| 问题 | 说明 |
| --- | --- |
| 延迟变高 | prefill 要处理更多输入 token |
| 成本变高 | 输入 token 也要计费或占用推理资源 |
| 显存压力变大 | KV Cache 与上下文长度相关 |
| 噪声变多 | 放进来的内容不一定都对当前问题有帮助 |
| 评测变难 | prompt 改动会影响结果，比较时必须记录上下文条件 |

因此，AI Infra 里经常要做的不是“把所有东西塞进 context”，而是控制哪些信息值得进入 context。

这会牵出后续很多系统：

- RAG chunking 和 rerank
- 会话历史截断
- prompt compression
- prefix cache
- token budget
- gateway token quota
- eval prompt versioning

## 一个具体场景

假设你做了一个学习助手，用户连续问了 20 轮问题。
第 21 轮用户只输入了一句话：

```text
那这个和 KV Cache 有什么关系？
```

从产品界面看，这句话很短。
但模型实际看到的可能是：

- system prompt 800 token
- 历史 20 轮对话 8000 token
- 当前问题 15 token
- 你额外塞进去的参考文档 3000 token

于是这次请求虽然“用户输入很短”，但 `prompt_tokens` 可能超过 11000。
如果你只看字符长度或请求数，就会误判这次请求很轻；如果你看 token usage，就会知道它其实是一个重请求。

这就是 token 和 context 的工程价值：它们让你看到真实负载，而不是只看表面输入。

## 当前仓库怎么表达

当前仓库是学习型实现，不会接入真实 tokenizer，但它已经把 token/context 的工程位置留出来了。

### `inference-service`

相关入口：

```text
projects/inference-service/src/inference_service/server.py
projects/inference-service/src/inference_service/engines.py
projects/inference-service/src/inference_service/runtime.py
```

你可以重点看：

- chat completion 请求里的 `messages`
- 响应里的 `usage.prompt_tokens`
- 响应里的 `usage.completion_tokens`
- `/metrics` 里的 token 计数
- `/events` 里的 request 成功事件

当前实现用估算函数表达 token usage，不代表真实 tokenizer，但它表达了一个重要边界：服务层需要把“请求产生了多少 token 工作量”暴露出来。

### `ai-gateway`

相关入口：

```text
projects/ai-gateway/src/ai_gateway/server.py
projects/ai-gateway/src/ai_gateway/router.py
```

gateway 不直接生成 token，但它需要理解 token 相关信号的意义。
未来如果做更真实的平台治理，gateway 往往要基于 token 做：

- 配额
- 预算
- 限流
- 成本统计
- 模型路由策略

当前 gateway 先表达了请求入口治理、模型名映射、cache、fallback 和 request id。后续把 token quota 加进去时，也应该放在平台治理层理解，而不是只看成模型服务内部细节。

### `eval-module`

评测模块会在样本输出和报告里保留 token usage。
这很重要，因为一次评测的 accuracy 不是唯一结果。

如果两个模型分数相同，但一个模型平均 prompt 更长、输出更长、成本更高，发布判断就不一定相同。
所以评测结果需要连接到 token 和 artifact，而不是只留下一个分数。

## 如何观察

学习时可以按这个顺序观察：

1. 发一次 chat completion 请求。
2. 看响应 JSON 里的 `usage`。
3. 刷新 `/metrics`，看 prompt/completion token 计数是否增加。
4. 查 `/events/requests/{request_id}`，看这条请求是否能串起来。
5. 在 eval 报告里看样本级 token 使用情况。

这套观察顺序把“模型输出”变成了“可复盘的请求”。
后面学习性能、网关、评测和训练时，都应该保留这个习惯。

## 常见误区

### “用户输入短，请求就一定轻”

不一定。
用户输入只是当前轮消息，模型看到的是完整 context。历史对话、system prompt、检索文档和工具结果都可能让 prompt token 很大。

### “Token 只是计费用的”

不是。
token 同时影响延迟、吞吐、显存、缓存、评测和限流。

### “Context 越大越安全”

不一定。
更大的 context 可能带来更多噪声、更高成本和更慢响应。好的系统会管理上下文，而不是无脑扩展上下文。

### “模型返回文本，usage 不重要”

usage 是平台理解负载的关键字段。
没有 usage，你很难解释一次请求为什么慢、为什么贵、为什么吞吐下降。

## 学完应该能回答

读完这一页后，你应该能回答：

1. 为什么 LLM 系统常常按 token 而不是字符或请求数讨论成本？
2. `prompt_tokens` 和 `completion_tokens` 分别影响什么？
3. 为什么用户当前输入很短，实际请求仍然可能很重？
4. context 为什么既是能力边界，也是成本边界？
5. 当前仓库在哪里表达 token usage、metrics 和 request 复盘？

## 继续阅读

- [Prefill、Decode 与 KV Cache](/01-llm-fundamentals/02-prefill-decode-kv-cache)
- [TTFT、ITL、吞吐](/01-llm-fundamentals/03-ttft-itl-throughput)
- [Streaming、Batching、Metrics](/02-inference-serving/09-streaming-batching-metrics)
- [Serving / Gateway 输出证据](/13-output-gallery/01-serving-gateway-evidence)
