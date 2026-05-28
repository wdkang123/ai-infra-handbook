# 服务选型与取舍

推理服务选型最容易被问成一个过于简单的问题：

> vLLM、SGLang、Triton、TensorRT-LLM，到底哪个最好？

这个问题本身就有陷阱。
AI serving 不是买一个“最快框架”就结束，而是在模型、硬件、流量、延迟目标、团队能力和平台边界之间做取舍。

这页不追求给出唯一答案，而是帮你建立选型判断框架。
如果你能说清楚“为什么这个阶段选这个方案，以及牺牲了什么”，就比只背工具名更接近真实工程。

## 一个错误选型是怎么发生的

很多团队不是因为选了“差工具”失败，而是因为选型问题没有被说清楚。

例如团队只说：

```text
我们要上 vLLM，因为它快。
```

这句话少了很多关键信息：

- 快的是 TTFT、ITL、tokens/sec，还是部署速度？
- 当前瓶颈真的是模型执行层吗？
- gateway、eval、监控、回滚是否已经准备好？
- 目标流量是在线交互还是离线批处理？
- 团队是否能维护对应 GPU / runtime / deployment 栈？
- 如果真实后端挂了，公开学习路径是否还能跑？

选型不是工具投票，而是把目标、约束和证据写清楚。

更好的表达方式是：

```text
当前阶段目标是让读者理解真实 LLM runtime 的请求调度和 streaming 行为。
因此我们保留 mock 作为默认路径，把 vLLM 作为进阶后端接入。
我们接受进阶路径需要额外依赖，但不让它影响 CI 和第一次实操。
```

这种说法比“哪个最好”更接近工程决策。

## 先分清你在选哪一层

很多讨论会把不同层的东西混在一起比较。

| 层次 | 典型问题 | 示例 |
| --- | --- | --- |
| API / 服务入口 | 请求怎么进来、怎么返回、怎么鉴权 | FastAPI、OpenAI-compatible API |
| LLM serving runtime | 如何调度请求、管理 KV Cache、做 streaming | vLLM、SGLang |
| Inference server | 如何统一管理多个模型服务、部署和协议 | Triton Inference Server |
| Kernel / engine 优化 | 如何更充分使用 GPU、优化执行图和通信 | TensorRT-LLM |
| 平台治理 | 谁能调用、路由到哪里、限流、审计 | AI Gateway |

所以不要直接问“vLLM 和 Triton 谁好”。
更准确的问题是：你现在缺的是 LLM runtime、统一模型服务入口，还是底层执行优化？

## 取舍轴一：先跑起来还是先跑得极致

学习和原型阶段，最重要的是快速建立完整链路：

- 请求能进来
- 响应能返回
- streaming 能看见
- metrics 能变化
- request id 能串起来
- 失败路径能复盘

这时你更应该选容易理解、容易替换的方案。

生产高负载阶段，才会越来越关心：

- tokens/sec
- GPU 利用率
- KV Cache 命中和显存碎片
- batch 调度策略
- 多卡通信
- 模型并行
- 量化和 kernel 优化

这两类目标都合理，但顺序不同。
过早追求极致性能，容易让学习者还没理解边界，就被复杂部署和硬件细节淹没。

## 取舍轴也要分阶段

同一个项目在不同阶段，选型答案可能不同。

| 阶段 | 优先目标 | 更适合的策略 |
| --- | --- | --- |
| 教学入门 | 低门槛、可解释、可复现 | mock engine + 清晰接口 |
| 工程骨架 | request id、events、metrics、streaming | 学习型 inference-service |
| 真实后端试验 | 观察真实 prefill/decode/cache 行为 | OpenAI-compatible backend |
| 平台治理 | 多模型、限流、fallback、审计 | gateway 独立演进 |
| 性能优化 | tokens/sec、显存、batch、并发 | runtime / engine 深度调优 |

这张表的意思不是“必须按顺序做完”，而是提醒你：每一步的主目标不同，不要用下一阶段的标准否定当前阶段的设计。

学习站最需要避免的是两种极端：

- 永远停在 toy demo，不解释真实迁移路径。
- 过早接满生产复杂度，让读者第一步就跑不起来。

## 取舍轴二：体验优先还是吞吐优先

低延迟体验和高吞吐经常冲突。

如果你的业务更像在线聊天、代码补全、客服助手，用户会非常在意：

- TTFT
- streaming 是否平滑
- 中断和重试体验
- 高峰期是否稳定

如果你的业务更像离线批处理、批量总结、数据标注、评测跑分，系统会更在意：

- tokens/sec
- 单位 GPU 成本
- 批处理效率
- 长任务调度
- 失败后恢复

两种场景的“好服务”不是同一个标准。

| 场景 | 更关注 | 可能牺牲 |
| --- | --- | --- |
| 在线交互 | TTFT、ITL、稳定性 | 资源利用率可能没那么满 |
| 离线批量 | tokens/sec、成本、吞吐 | 单请求等待可能更长 |
| 内部评测 | 可复现、结果产物、任务队列 | 交互体感不是核心 |
| 多租户平台 | 隔离、限流、审计、路由 | 单服务简单性 |

## 取舍轴三：通用性还是硬件绑定

通用方案通常更容易：

- 本地学习
- 快速试错
- 换模型
- 换部署环境
- 让更多贡献者参与

但通用方案未必能榨干硬件性能。
当模型规模、流量和成本压力上来后，你可能需要更深的硬件绑定和执行优化。

这就是为什么很多团队会经历这样的路径：

1. 先用简单 mock 或轻量服务理解接口。
2. 接入 vLLM 之类 LLM runtime，建立真实 serving 能力。
3. 对特殊模型或高负载场景，引入更强的 engine / kernel 优化。
4. 用 gateway、observability、eval 和 release gate 管住平台。

这不是“前面的方案错了”，而是成熟度不同。

## 取舍轴四：单模型服务还是平台化多模型

一个模型服务只要回答：

- 这个模型能不能执行？
- 请求怎么生成？
- streaming 怎么返回？
- metrics 怎么暴露？

平台化多模型系统还要回答：

- 外部模型名如何映射到内部后端？
- 同一模型是否有多个候选上游？
- 某个上游失败时是否 fallback？
- 每个租户能用哪些模型？
- token budget 怎么算？
- 如何审计一次请求真实走了哪里？

所以推理服务选型不能脱离 gateway。
如果你只看模型服务层，很容易忽略平台治理复杂度。

## 取舍轴五：可观察性是否跟得上

很多 serving 方案刚接入时看起来“能返回答案”，但一出问题就不知道怎么查。

一个可维护的 serving 方案至少要能回答：

- 服务是否健康？
- 当前有多少请求？
- token 计数是否在变化？
- 哪些请求失败了？
- 一条请求是否能用 request id 串起来？
- streaming 是否中途断开？
- 上游模型实际是哪一个？
- fallback 或 cache 是否影响结果？

如果方案性能很好，但缺少这些观察入口，学习和维护都会很痛苦。

## 简化版选型矩阵

可以用下面这张矩阵做初步判断：

| 主要目标 | 更优先看 | 不要被什么带偏 |
| --- | --- | --- |
| 教学可运行 | 本地默认路径、mock、文档、测试 | 真实后端炫技 |
| 在线聊天 | TTFT、ITL、streaming、错误收尾 | 只看总 tokens/sec |
| 批量生成 | 吞吐、任务队列、失败重试 | 只看单请求延迟 |
| 多业务接入 | gateway、auth、routing、quota | 让业务直连后端 |
| 模型发布 | eval、compare、history、rollback | 只看 leaderboard |
| 成本优化 | token usage、cache、batch、模型分层 | 只看请求数 |
| 生产迁移 | 双路径、回滚、观测、CI | 一次性重写 |

矩阵不是替你做决定，而是防止你把问题问错。
如果目标是公开教学，默认路径就不能依赖昂贵硬件。
如果目标是高峰期成本，request count 就远远不够，必须看 token 和 batch。

## 一个具体选型例子

假设你要做一个公开学习网站的 AI Infra 示例项目。

你的目标不是马上服务百万 QPS，而是让读者理解：

- OpenAI-compatible API 长什么样
- request id 如何贯穿
- metrics 怎么观察
- gateway 和 inference-service 怎么分层
- eval 怎么从结果走到发布判断
- finetune 产物怎么沉淀成可追踪资产

此时最合理的做法不是一开始就把所有真实 serving stack 接满。
更合理的是先用学习型 `inference-service` 表达接口和边界，再逐步说明它如何迁移到 vLLM、SGLang、Triton 或 TensorRT-LLM。

这就是当前仓库的路线：先把学习路径和系统边界讲清楚，再为真实后端留迁移入口。

## 当前仓库怎么表达

### `inference-service` 是学习入口

相关文件：

```text
projects/inference-service/src/inference_service/server.py
projects/inference-service/src/inference_service/engines.py
projects/inference-service/src/inference_service/runtime.py
```

它表达的是：

- `/v1/chat/completions`
- streaming 响应
- `usage` token 字段
- `/health`
- `/metrics`
- `/events`
- request timeline

它不是生产级 vLLM 替代品。
它的价值在于让读者先理解服务接口、观测入口和错误边界。

### `ai-gateway` 是平台边界

相关文件：

```text
projects/ai-gateway/src/ai_gateway/server.py
projects/ai-gateway/src/ai_gateway/router.py
projects/ai-gateway/configs/models.yaml
```

它表达的是：

- auth
- routing
- rate limit
- response cache
- fallback
- upstream health
- request id
- gateway metrics/events

如果以后把后端换成 vLLM 或 SGLang，gateway 的核心职责不应该消失。
它仍然应该负责入口治理，而不是让业务方直接绑死某个模型服务地址。

### 生产迁移页给后续路径

继续阅读时，可以看：

- [从学习型服务到真实 Serving Stack](/02-inference-serving/10-from-learning-service-to-real-serving-stack)
- [Serving Backend 迁移路线](/12-production-migration/01-serving-backend-migration)
- [Gateway 平台化加固路线](/12-production-migration/02-gateway-platform-hardening)

这些页面的作用是告诉你：当前项目不是终点，而是一个能逐步替换内部实现的学习骨架。

## 常见选型误区

### “哪个框架 benchmark 高就选哪个”

benchmark 很重要，但不能单独决定。
你还要看模型支持、部署复杂度、可观察性、团队熟悉度、故障处理和平台集成。

### “学习项目不用考虑边界”

正好相反。
学习项目更应该把边界讲清楚，因为边界是后续迁移的地图。

### “先把 gateway 和 inference 合成一个服务更简单”

短期可能简单，长期会模糊职责。
当你加鉴权、限流、多模型、fallback、eval 和审计时，混在一起会更难解释。

### “吞吐指标能代表所有性能”

不能。
在线交互还要看 TTFT 和 ITL；平台还要看错误率、fallback、cache、排队和成本。

### “选了一个方案就不能变”

好的架构应该允许替换后端。
外部接口、模型名、观测字段和发布流程越稳定，内部 runtime 越容易迭代。

## 选型时可以问的十个问题

1. 这是在线交互还是离线批量？
2. 当前最痛的是 TTFT、ITL、吞吐、成本还是稳定性？
3. 模型规模和上下文长度是什么量级？
4. 是否需要多模型、多租户、多上游？
5. 是否需要 OpenAI-compatible API？
6. streaming 是否是硬需求？
7. 失败时是否需要 fallback？
8. metrics、events、request id 是否能支撑排查？
9. 团队是否能维护对应部署和硬件栈？
10. 未来替换 serving backend 时，gateway 和 eval 是否能基本不动？

这些问题比“哪个最好”更接近真实选型。

## 可以写进 Issue 的选型模板

后续如果要在 GitHub 上讨论某个 serving 后端，可以直接用这个模板：

```text
选型目标：
候选方案：
当前瓶颈：
预期收益：
主要代价：
依赖变化：
默认学习路径是否受影响：
需要新增的指标：
需要新增的测试：
回滚方式：
文档更新：
```

这样选型讨论就不会停留在“我觉得某工具更好”。
它会自然连接到公开仓库维护所需的测试、文档和回滚。

## 学完应该能回答

读完这一页后，你应该能回答：

1. 为什么 vLLM、SGLang、Triton、TensorRT-LLM 不总是在同一层比较？
2. 为什么在线交互和离线批量的 serving 目标不同？
3. 为什么学习项目先保持清晰边界比一开始追求极致性能更重要？
4. 当前仓库的 `inference-service` 和 `ai-gateway` 分别表达什么边界？
5. 如果未来接入真实 vLLM，哪些外部能力应该保持稳定？

## 继续阅读

- [vLLM 与 SGLang](/02-inference-serving/01-vllm-sglang)
- [Triton 与 TensorRT-LLM](/02-inference-serving/02-triton-tensorrt-llm)
- [TTFT、ITL、吞吐](/01-llm-fundamentals/03-ttft-itl-throughput)
- [平台层与模型服务层边界](/03-ai-gateway-platform/05-platform-vs-model-service)
