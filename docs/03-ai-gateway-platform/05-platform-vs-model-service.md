# 平台层与模型服务层边界

AI Infra 初学阶段最常见的混乱之一，是把 gateway 和 inference-service 混成一个东西。

表面上看，它们都和“调用模型”有关：

- gateway 收到 chat completion 请求。
- inference-service 也收到 chat completion 请求。
- 两边都有 `/health`。
- 两边都有 `/metrics`。
- 两边都可能返回错误。

但它们回答的是完全不同的问题。
如果这条边界不清楚，后续加多模型、评测、训练、观测、限流、fallback、成本治理时，系统很快会变成一团。

## 一句话区分

可以先这样记：

> Gateway 负责入口治理，Inference Service 负责推理执行。

再展开一点：

| 层 | 主要问题 | 典型能力 |
| --- | --- | --- |
| 平台层 / Gateway | 谁能调用、调用什么、怎么治理、怎么追踪 | auth、routing、rate limit、cache、fallback、request id、upstream health |
| 模型服务层 / Inference | 模型请求怎么执行、怎么产出结果、怎么暴露执行状态 | chat completion、streaming、engine adapter、token usage、serving metrics |

这不是为了画架构图好看，而是为了让职责可替换、可观察、可演进。

## 为什么不能都塞进模型服务

最开始做 demo 时，把鉴权、路由、模型调用都写在一个服务里很自然。
但系统稍微复杂一点，这种写法就会带来问题。

假设 inference-service 同时负责：

- 验证 API key
- 判断租户权限
- 做模型名映射
- 做 rate limit
- 做 response cache
- 做 fallback
- 执行模型请求
- 统计 token usage
- 暴露 engine metrics

短期能跑，长期会让服务职责变得非常混乱。
当你想换一个 serving backend，比如从 mock 换到 vLLM，再换到 SGLang，入口治理逻辑也会跟着被迫移动。

这会让“替换模型服务”变成“重写平台入口”。

## 为什么不能把 Gateway 当纯代理

另一种误区是：gateway 只是把请求转发给下游。

如果 gateway 只会转发，它确实很薄。
但 AI 平台层真正有价值的地方在于：

- 对外隐藏内部模型和 provider 变化
- 统一鉴权和配额
- 统一模型命名
- 统一错误格式
- 统一 request id
- 做 fallback 和 cache
- 记录跨服务事件
- 让评测、训练和发布流程能引用稳定模型入口

所以 gateway 不是“多此一举的转发层”。
它是把模型能力变成平台能力的入口。

## 边界的核心判断

判断一个功能应该放哪层，可以问三个问题。

### 1. 它是否和调用者身份有关？

如果答案是“是”，通常偏 gateway。

例如：

- API key 是否有效
- 某个 token 是否超过 quota
- 某个用户能否调用某个模型
- 是否要记录审计信息

这些是入口治理问题，不应该散落在每个模型服务里。

### 2. 它是否和具体模型执行有关？

如果答案是“是”，通常偏 inference-service。

例如：

- prompt 如何交给 engine
- streaming chunk 怎么生成
- prompt/completion token 怎么统计
- engine error 怎么映射
- 模型服务自身 metrics 怎么暴露

这些是执行层问题。

### 3. 如果换掉后端，它是否应该基本不变？

如果你从 mock serving 换到 vLLM，某个逻辑仍然应该保留，那它很可能属于 gateway 或平台周边。

例如：

- 外部模型名
- 鉴权
- 限流
- fallback 策略
- request id
- release gate 引用的模型入口

如果某个逻辑会随着 serving runtime 替换而变化，那它更可能属于 inference-service。

## 两层分别保留什么状态

| 信息 | 更适合在哪层 | 原因 |
| --- | --- | --- |
| API key / token | Gateway | 调用者身份属于入口治理 |
| 外部模型名 | Gateway | 对调用者稳定的 API 契约 |
| 内部 target model | Gateway 配置与 router | 平台决定实际去哪里 |
| prompt/completion tokens | Inference，Gateway 可汇总 | token 由执行层产生，平台可用于治理 |
| engine name | Inference | 执行后端细节 |
| upstream health | Gateway | 平台需要知道依赖状态 |
| request id | 两层都要 | 跨服务复盘主键 |
| fallback path | Gateway | 多上游治理问题 |
| streaming chunk | Inference 生成，Gateway 透传 | 执行和代理边界都要处理 |

这张表的价值是提醒你：边界不是抽象原则，它会落到每个字段和文件上。

## 一个具体例子：模型名不匹配

用户请求：

```json
{
  "model": "gpt-learning",
  "messages": [...]
}
```

gateway 里可能配置：

```text
external name: gpt-learning
target model: Qwen/Qwen2.5-0.5B-Instruct
upstream: vllm-local
fallback: mock-backup
```

这时：

- 调用者只需要知道 `gpt-learning`。
- gateway 负责把它映射到内部候选目标。
- inference-service 只需要执行自己配置的目标模型。
- 如果主上游失败，gateway 可以 fallback。
- 响应 header 可以告诉你实际走了哪个 upstream。

如果没有这条边界，调用者就会被迫理解内部 target model、provider 地址和 fallback 细节。
这会让平台 API 很难稳定。

## 一个具体例子：请求失败

假设请求最终返回 502。

你需要分层排查：

1. Gateway 是否收到请求？
2. 鉴权是否通过？
3. 模型名是否匹配？
4. 是否被 rate limit？
5. 是否尝试 upstream？
6. upstream 是否返回 5xx？
7. 是否还有 fallback？
8. inference-service 是否记录 engine error？

如果平台层和模型服务层混在一起，排查路径就会模糊。
分层以后，你可以先看 gateway timeline，再看 inference timeline。

## 当前仓库怎么表达

### Gateway

相关文件：

```text
projects/ai-gateway/src/ai_gateway/server.py
projects/ai-gateway/src/ai_gateway/router.py
projects/ai-gateway/src/ai_gateway/runtime.py
projects/ai-gateway/configs/models.yaml
```

它表达：

- bearer token auth
- rate limit
- model routing
- fallback candidates
- response cache
- upstream health probe
- gateway metrics/events
- `x-request-id`
- `x-cache`
- `x-upstream-model`
- `x-fallback-used`

这些都是入口治理和平台抽象。

### Inference Service

相关文件：

```text
projects/inference-service/src/inference_service/server.py
projects/inference-service/src/inference_service/engines.py
projects/inference-service/src/inference_service/runtime.py
```

它表达：

- OpenAI-compatible chat completion
- normal / streaming response
- engine adapter
- model validation
- token usage
- inference metrics/events
- request timeline

这些都是推理执行和服务内部状态。

## 分层后如何演进

这条边界能带来很实际的演进能力。

### 替换模型服务

你可以把 `inference-service` 的 mock engine 替换成 vLLM、SGLang 或远程 OpenAI-compatible backend。
理想情况下，gateway 的 auth、routing、rate limit、request id、fallback 不应该重写。

### 增加多模型

gateway 可以增加更多外部模型名和内部 target。
inference-service 只负责执行它被配置的模型。

### 增加评测与发布门禁

eval-module 可以稳定地请求 gateway 暴露的模型名，而不是绑定某个临时下游地址。
这样发布判断更接近平台真实入口。

### 增加训练资产

finetune-demo 导出的 adapter 后续可以成为某个 target model 的来源。
gateway 仍然可以对外保留稳定模型名。

## 常见误区

### “模型服务顺手做鉴权也没问题”

可以做，但学习阶段最好先分开。
否则你会把入口治理和执行细节混在一起，后面迁移真实 serving backend 会更难。

### “Gateway 只要会转发就够了”

不够。
AI Gateway 的平台价值在于治理、抽象、观测和演进空间。

### “两层分开只是为了微服务”

不是。
即使单机学习项目，也需要职责边界。边界先清楚，未来拆不拆服务才有选择。

### “Inference 不需要 observability，Gateway 看得到就行”

不够。
gateway 能看到入口路径，但执行层的 token usage、engine error、streaming 状态仍然要在 inference 侧暴露。

### “Gateway 应该懂所有模型内部细节”

也不对。
gateway 应该理解平台治理需要的模型元信息，但不应该绑定具体 engine 内部实现。

## 学完应该能回答

读完这一页后，你应该能回答：

1. Gateway 和 inference-service 分别回答什么问题？
2. 为什么鉴权、限流、路由更适合放在平台层？
3. 为什么 token usage 和 engine metrics 更接近执行层？
4. 如果把 mock backend 换成 vLLM，哪些能力应该保持不变？
5. 当前仓库哪些文件表达了这条边界？

## 继续阅读

- [鉴权、路由、限流](/03-ai-gateway-platform/01-auth-routing-rate-limit)
- [外部模型名与内部目标映射](/03-ai-gateway-platform/06-model-name-to-target-mapping)
- [服务选型与取舍](/02-inference-serving/03-serving-tradeoffs)
- [从学习型 Gateway 到真实平台层](/03-ai-gateway-platform/07-from-demo-gateway-to-real-platform)
