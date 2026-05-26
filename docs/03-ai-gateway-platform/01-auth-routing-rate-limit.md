# 鉴权、路由、限流

AI Gateway 最容易被低估。
很多人第一次看到 gateway，会以为它只是“把请求转发到模型服务”的代理层。
如果只是这样，那确实没什么值得专门学。

但真实 AI Infra 里的 gateway 不是普通透明代理。
它站在应用和模型服务之间，负责把“可以调用模型”这件事变成一个可治理、可观测、可演进的平台能力。

最基础的三件事就是：

- 鉴权：谁可以进来
- 路由：这条请求应该去哪
- 限流：这条请求现在能不能被接受

这三件事看起来朴素，但它们决定了后面所有平台能力的边界。

## 为什么平台层不能只做转发

假设没有 gateway，应用直接调用模型服务：

```text
Client -> Inference Service
```

短期看很简单。
但只要系统开始变大，问题会马上出现：

- 每个应用都要自己保存模型服务地址
- 每个应用都要自己处理 API key
- 模型升级时所有应用都要改配置
- 想做限流时没有统一入口
- 想统计谁用了多少 token 很困难
- 想 fallback 到另一个模型没有统一策略
- 想屏蔽某个不稳定后端很麻烦
- 想做审计和追踪缺少统一 request id

所以平台层的价值不是“多加一跳”，而是把模型调用从散落在各应用里的点状逻辑，收敛成统一治理面。

更合理的结构是：

```text
Client -> AI Gateway -> Inference Service / Serving Backend
```

这样应用只知道外部模型名和统一 API。
至于背后到底是 mock 服务、vLLM、SGLang、Triton 还是第三方模型供应商，可以由 gateway 和平台配置逐步演进。

## 鉴权：谁可以进来

鉴权先解决的是“这是不是一个合法请求”。
它不是只有安全意义，也是在保护昂贵的模型资源。

LLM 请求的成本通常比普通接口高得多。
一个恶意或错误配置的客户端，可能在短时间内消耗大量 token、GPU 时间或供应商额度。
所以入口鉴权是 AI 平台的第一道边界。

最小形态可能只是：

```http
Authorization: Bearer local-dev-token
```

生产形态可能会更复杂：

- 用户 token
- 服务间 token
- API key
- OAuth / OIDC
- 租户身份
- 项目或 workspace 身份
- 内部系统签名

但无论形态如何，核心问题都是：

> 请求者是谁，它是否有资格调用这个模型或这类能力？

## 鉴权不只是判断 token 对不对

很多初学者会把鉴权理解成：

```text
token 正确 -> 放行
token 错误 -> 拒绝
```

这是第一步，但平台层通常还要继续判断：

- 这个用户能不能调用这个模型
- 这个用户能不能使用 streaming
- 这个用户有没有更高上下文长度额度
- 这个用户属于哪个租户
- 这个请求是否应该计入某个项目预算
- 这个 token 是否已经被禁用

也就是说，鉴权后面往往会接授权、配额和审计。

学习阶段不需要一开始实现完整权限系统。
但你要知道：gateway 放在模型服务前面，是为了让这些能力有地方生长。

## 路由：外部模型名不等于内部后端

路由解决的是：

> 用户请求的模型名，最后应该落到哪个执行目标？

例如客户端请求：

```json
{
  "model": "ai-infra-chat",
  "messages": [
    {"role": "user", "content": "解释一下 AI Gateway"}
  ]
}
```

但内部真实后端可能是：

```text
http://localhost:8000/v1
Qwen/Qwen2.5-0.5B-Instruct
```

也可能是：

```text
https://internal-vllm.example/v1
meta-llama/...
```

也可能根据环境、用户、灰度策略发生变化。

这就是为什么 gateway 层常常会维护一张映射：

| 外部模型名 | 内部目标 | 用途 |
| --- | --- | --- |
| `ai-infra-chat` | mock learning service | 本地学习和测试 |
| `fast-chat` | 小模型 serving backend | 低成本快速响应 |
| `strong-chat` | 大模型 backend | 高质量任务 |
| `eval-candidate` | 候选模型 | 发布前评测 |

外部模型名是平台契约。
内部目标是实现细节。

把这两者分开，平台才有演进空间。

## 路由为什么是平台职责

如果没有 gateway，应用会直接写死后端地址。
一旦模型升级、后端迁移或做灰度发布，所有应用都要跟着改。

有了 gateway，应用只依赖稳定外部名称。
平台可以在内部做：

- 模型版本切换
- A/B 测试
- 按租户路由
- 按任务类型路由
- 按成本路由
- 按地域路由
- fallback 路由
- 灰度发布

这就是模型平台和单个模型服务的区别。

模型服务负责把某个模型跑起来。
gateway 负责把很多模型能力组织成可治理的产品入口。

## 限流：为什么不能无限接请求

限流的核心不是“故意卡用户”，而是保护系统稳定性。

LLM 服务的资源通常很贵，也更容易被长请求拖慢：

- 长 prompt 会增加 prefill 压力
- 长输出会增加 decode 时间
- 并发请求会争抢 GPU 和 KV cache
- streaming 会保持连接
- 外部模型供应商可能有速率和额度限制

如果没有限流，系统可能出现：

- 单个用户打满服务
- 少数长请求拖慢所有人
- 供应商额度被异常消耗
- GPU 队列堆积
- 错误率上升
- 延迟雪崩

所以限流是平台对可用性的保护。

## 限流不只是一种算法

学习时常见的限流实现是内存计数：

```text
每个 token / user / IP 在固定窗口内最多 N 次请求
```

这足够理解基础思想。

但真实 AI Gateway 里的限流可能有很多维度：

| 维度 | 例子 |
| --- | --- |
| 请求次数 | 每分钟最多 60 次 |
| token 数 | 每天最多 100 万 input + output token |
| 并发数 | 同时最多 5 个 streaming 请求 |
| 模型级别 | 大模型额度更严格 |
| 租户级别 | 不同 workspace 不同预算 |
| 优先级 | 内部评测任务低峰运行 |
| 成本 | 超过预算后降级或拒绝 |

这也是 AI Gateway 和普通 API Gateway 的差异之一：token、模型和生成长度会变成限流对象。

## 鉴权、路由、限流如何串起来

一次请求进入 gateway 后，大致可以这样理解：

```text
1. 解析 request id
2. 检查 Authorization
3. 识别调用者身份
4. 检查调用者是否能使用目标模型
5. 根据外部模型名找到内部 target
6. 检查限流和配额
7. 转发到 downstream serving backend
8. 记录响应、错误、token usage 和事件
```

这不是唯一实现，但顺序很有代表性。

其中任何一步失败，都应该有清楚的错误语义：

| 失败点 | 常见状态码 | 含义 |
| --- | --- | --- |
| 没有认证信息 | 401 | 请求者身份不合法 |
| 模型名不存在 | 404 | 外部模型名无法路由 |
| 超过频率或配额 | 429 | 当前请求被限流 |
| 下游服务失败 | 502 | gateway 到 backend 的路径失败 |

当前仓库里的 `ai-gateway` 就保留了这些基础错误路径。
它不是完整平台，但已经能让你练习平台边界。

## 和 fallback / cache 的关系

鉴权、路由、限流是入口治理的基础。
后面更复杂的 gateway 能力会长在它们之上。

例如 fallback：

```text
首选模型失败 -> 尝试备用模型
```

如果没有路由表，就不知道备用模型是谁。
如果没有鉴权，就不知道这个用户是否允许使用备用模型。
如果没有限流，就可能在失败重试时放大流量。

再比如 response cache：

```text
相同请求 -> 命中缓存 -> 不打下游模型
```

如果没有鉴权，缓存可能跨用户泄漏。
如果没有路由，缓存 key 很难包含正确模型目标。
如果没有限流，缓存未命中时仍可能打爆后端。

所以不要把这些能力割裂看。
gateway 是一个整体治理层。

## 和当前仓库怎么对应

当前 `projects/ai-gateway` 已经提供了最小学习实现：

- Bearer token 鉴权
- 外部模型名到下游目标的映射
- `/v1/models`
- `/v1/chat/completions`
- streaming 透传
- rate limit
- fallback 示例
- response cache
- `/metrics`
- `/events`
- `/events/failures`
- `/events/requests/{request_id}`
- `x-request-id`
- `x-upstream-model`
- `x-fallback-used`
- `x-cache`

你可以把它当成一个小型平台层标本。
它不追求生产完整性，但它把最关键的学习观察点留下来了。

读代码时可以重点看：

- `projects/ai-gateway/src/ai_gateway/config.py`
- `projects/ai-gateway/configs/models.yaml`
- `projects/ai-gateway/src/ai_gateway/proxy.py`
- `projects/ai-gateway/tests/test_proxy.py`

这些文件会把“鉴权、路由、限流不是抽象词”变成具体代码。

## 一个学习任务

你可以用这个顺序练习：

1. 启动 inference-service 和 ai-gateway。
2. 不带 Authorization 调用 gateway，观察 401。
3. 带错误模型名调用，观察 404。
4. 快速连续请求，观察 429 或 metrics 变化。
5. 正常请求，记录 `x-request-id`。
6. 用 request id 查询 events timeline。
7. 对照 [Gateway 韧性 Lab](/07-hands-on-labs/02-gateway-resilience-lab) 复盘。

这个练习的价值不在于请求是否成功，而在于你能解释每个失败语义来自 gateway 的哪一层判断。

## 常见误区

### 误区 1：把 gateway 当成 Nginx 反向代理

反向代理只是基础形态。
AI Gateway 还要处理模型名、token、配额、fallback、usage、events 和发布治理。

### 误区 2：把鉴权留给模型服务

模型服务可以有自己的保护，但平台统一鉴权最好放在入口层。
否则每个后端都要重复实现，并且策略很难一致。

### 误区 3：路由只是 URL 转发

路由不仅是 URL。
它还包含外部模型名、内部模型名、fallback、灰度、租户策略和版本管理。

### 误区 4：限流只按请求数

LLM 场景里，请求数不够。
一个请求可能只有 20 token，也可能有 20000 token。
真实系统经常要把 token、并发、模型成本和租户预算一起考虑。

## 学完这一页应该能回答

- 为什么 AI Gateway 不能只是透明转发？
- 鉴权、授权、配额之间是什么关系？
- 外部模型名为什么不应该直接等于内部后端？
- 限流为什么是保护稳定性，而不是单纯限制用户？
- 401、404、429、502 分别更可能来自 gateway 的哪一层？
- 当前仓库的 `ai-gateway` 哪些文件对应这些能力？

## 下一步

继续读：

- [健康检查、Metrics、Request ID](/03-ai-gateway-platform/02-health-metrics-request-id)
- [Gateway、Router、Fallback、Cache](/03-ai-gateway-platform/03-gateway-router-fallback-cache)
- [Streaming、错误路径、Upstream Health](/03-ai-gateway-platform/04-streaming-errors-upstream-health)
- [从 Demo Gateway 到真实平台](/03-ai-gateway-platform/07-from-demo-gateway-to-real-platform)
