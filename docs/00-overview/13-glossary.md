# 术语索引

这页收集学习站里反复出现的关键词。

它不是百科全书，而是帮助你把术语和当前仓库里的代码、文档位置对上。

## 怎么使用这页

不要把术语表当成要背的清单。更好的用法是：

1. 阅读正文时遇到陌生词，先来这里确认它属于哪一层。
2. 看它对应的项目、文件或证据。
3. 回到原文继续读。
4. 如果这个词会影响实践，再去相关 lab 跑一次命令。

这个项目里的术语有一个特点：大多数词都不是纯概念，而是会落到接口、配置、输出证据或发布判断上。

例如：

```text
fallback
  -> gateway router
  -> x-fallback-used / events / metrics
  -> Gateway 韧性 Lab
```

如果你能把一个词从“定义”连到“代码和输出”，说明你已经不只是认识这个词，而是在理解它的工程位置。

## AI Infra

围绕大模型应用的工程基础设施。

在这个仓库里，AI Infra 被拆成四层：

- 推理服务层
- 平台治理层
- 评测质量层
- 训练资产层

对应阅读：

- [什么是 AI Infra](/00-overview/01-what-is-ai-infra)
- [四个项目怎么连成系统](/06-projects/06-end-to-end-system-map)

## Inference Service

模型服务本体，负责接收生成请求并返回结果。

当前对应项目：

- `projects/inference-service`

关键能力：

- `/health`
- `/metrics`
- `/v1/chat/completions`
- 普通响应
- streaming
- engine adapter

对应阅读：

- [inference-service](/06-projects/01-inference-service)

## AI Gateway

平台治理入口，负责把调用方请求变成受控的下游请求。

当前对应项目：

- `projects/ai-gateway`

关键能力：

- 鉴权
- 路由
- 限流
- request id
- upstream health
- fallback
- cache
- streaming proxy

对应阅读：

- [ai-gateway](/06-projects/02-ai-gateway)

## Token

模型处理文本时使用的基本单位。

工程里，token 通常影响：

- 成本
- 延迟
- 上下文长度
- throughput

对应阅读：

- [模型、Token、Context](/01-llm-fundamentals/01-model-token-context)

## Context

模型一次请求能看到的输入范围。

context 越长，不一定越好；它会影响显存、latency 和成本。

对应阅读：

- [模型、Token、Context](/01-llm-fundamentals/01-model-token-context)

## Prefill

模型处理已有上下文的阶段。

它通常影响首 token 之前的等待时间。

对应阅读：

- [Prefill、Decode、KV Cache](/01-llm-fundamentals/02-prefill-decode-kv-cache)

## Decode

模型逐个生成新 token 的阶段。

它通常影响持续输出速度，也就是 streaming 里的体感。

对应阅读：

- [Prefill、Decode、KV Cache](/01-llm-fundamentals/02-prefill-decode-kv-cache)

## KV Cache

模型在生成过程中复用中间状态的一种机制。

它影响：

- 长上下文性能
- 并发能力
- 显存占用
- prefix caching

对应阅读：

- [Prefill、Decode、KV Cache](/01-llm-fundamentals/02-prefill-decode-kv-cache)
- [Cache 与 Prefix Caching](/02-inference-serving/06-cache-prefix-caching)

## TTFT

Time To First Token，首 token 延迟。

它衡量用户多久能看到模型开始输出。

对应阅读：

- [TTFT、ITL、吞吐](/01-llm-fundamentals/03-ttft-itl-throughput)

## ITL

Inter Token Latency，token 间延迟。

它衡量模型持续生成时每个 token 之间的间隔。

对应阅读：

- [TTFT、ITL、吞吐](/01-llm-fundamentals/03-ttft-itl-throughput)

## Throughput

吞吐量，通常用来衡量系统单位时间处理多少请求或 token。

需要注意：低延迟和高吞吐经常存在取舍。

对应阅读：

- [TTFT、ITL、吞吐](/01-llm-fundamentals/03-ttft-itl-throughput)

## Streaming

模型结果以事件流形式逐步返回。

当前仓库里：

- inference-service 生成最小 SSE
- ai-gateway 透传 SSE
- 失败时会发结构化 SSE error

对应阅读：

- [Streaming、Batching、Metrics](/02-inference-serving/09-streaming-batching-metrics)
- [Streaming、错误路径、Upstream Health](/03-ai-gateway-platform/04-streaming-errors-upstream-health)

## SSE

Server-Sent Events，一种服务端向客户端持续发送事件的 HTTP 传输方式。

当前仓库使用最小 `data: ...` 格式表达 streaming。

对应阅读：

- [Serving 可观测性 Lab](/07-hands-on-labs/01-serving-observability-lab)

## Request ID

跨服务追踪一条请求的标识。

当前仓库使用 `x-request-id`。

它不改变业务结果，但能帮助排查跨服务链路。

对应阅读：

- [健康检查、Metrics、Request ID](/03-ai-gateway-platform/02-health-metrics-request-id)

## OpenAI-compatible API

一种常见的大模型服务接口兼容形态。

在这个仓库里，它主要体现在：

- `/v1/chat/completions`
- `/v1/models`
- `messages`
- `model`
- `stream`
- usage 字段

OpenAI-compatible 不代表底层一定调用 OpenAI。它更像服务契约，后端可以是 mock engine、vLLM、SGLang 或其他兼容服务。

对应阅读：

- [inference-service](/06-projects/01-inference-service)
- [Serving 后端迁移](/12-production-migration/01-serving-backend-migration)

## Engine Adapter

模型执行后端的适配层。

它把统一的服务请求转换成某个具体 runtime 或上游服务能理解的调用。

当前仓库里，engine adapter 的价值是让学习者看到：

- 服务 API 可以稳定
- 后端执行层可以替换
- 上游错误需要映射
- streaming 和非 streaming 都要被处理

对应阅读：

- [概念到代码索引](/09-reference/02-concept-to-code-index)
- [从学习型服务到真实 Serving Stack](/02-inference-serving/10-from-learning-service-to-real-serving-stack)

## Upstream

gateway 或服务调用的下游依赖。

在 `ai-gateway` 里，upstream 通常指实际承接模型请求的 inference-service 或兼容模型服务。

upstream 状态会影响：

- `/health`
- `502`
- fallback
- events
- metrics

对应阅读：

- [Streaming、错误路径、Upstream Health](/03-ai-gateway-platform/04-streaming-errors-upstream-health)

## Health Check

健康检查接口。

当前仓库里：

- inference-service 的 `/health` 表示服务自身状态
- ai-gateway 的 `/health` 还会探测 upstream

对应阅读：

- [健康检查、Metrics、Request ID](/03-ai-gateway-platform/02-health-metrics-request-id)

## Metrics

机器可读的系统指标。

当前仓库里，metrics 用来观察：

- 请求数
- 成功数
- 失败数
- token 数
- cache 命中
- upstream failure

对应阅读：

- [Tracing、Metrics、Logs](/04-evaluation-observability/03-observability-traces-metrics-logs)

## Fallback

主路径失败时尝试备用路径。

当前 gateway 中：

- 普通请求可以在 5xx 后尝试备用模型
- streaming 只在首个 chunk 前允许 fallback
- 普通响应会通过 `x-upstream-model` / `x-fallback-used` 暴露 fallback 结果
- metrics 会记录 fallback attempts / successes

对应阅读：

- [Gateway、Router、Fallback、Cache](/03-ai-gateway-platform/03-gateway-router-fallback-cache)

## Rate Limit

入口限流。

它不是模型失败，而是 gateway 主动保护系统。

当前仓库里，限流失败会表现为：

- HTTP `429`
- rate limit 相关 event
- metrics 变化

对应阅读：

- [鉴权、路由、限流](/03-ai-gateway-platform/01-auth-routing-rate-limit)
- [Gateway 韧性 Lab](/07-hands-on-labs/02-gateway-resilience-lab)

## Response Cache

平台层缓存完整响应。

它不同于模型引擎里的 KV cache。  
当前 gateway 的 response cache 默认关闭，并按 token 和请求体隔离。

对应阅读：

- [Gateway 韧性 Lab](/07-hands-on-labs/02-gateway-resilience-lab)

## Event Timeline

一次请求在系统里留下的事件序列。

它适合回答：

- 请求什么时候进入 gateway
- 是否通过鉴权
- 选择了哪个 upstream
- 是否发生 fallback
- 是否命中 cache
- 最终成功还是失败

对应阅读：

- [失败症状到证据地图](/13-output-gallery/05-failure-evidence-map)
- [Serving 与 Gateway 输出证据](/13-output-gallery/01-serving-gateway-evidence)

## Run

一次评测运行。

它回答：某个模型在某个 task 上跑出了什么结果。

对应阅读：

- [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)

## Compare

一次评测对比。

它回答：candidate 相对 baseline 是 improved、regressed，还是 unchanged。

对应阅读：

- [Eval 发布门禁 Lab](/07-hands-on-labs/03-eval-release-gate-lab)

## min_delta

评测比较中的最小有效差异阈值。

它用于避免把很小的 benchmark 波动误判成质量变化。

对应阅读：

- [eval-module](/06-projects/03-eval-module)

## LLM-as-Judge

用另一个模型来评价模型输出。

它适合开放式任务，但不能被当成绝对真理。

学习时要关注：

- judge prompt
- judge model
- judge reason
- 人工抽检
- 和 rule-based 指标是否冲突

对应阅读：

- [LLM Evaluation](/04-evaluation-observability/05-llm-evaluation)

## Leaderboard

评测结果的展示层。

它不等于评测本身。可信 leaderboard 应该能追溯到：

- run history
- result file
- sample outputs
- comparison report
- backend/few-shot/task 配置

对应阅读：

- [Benchmark、Arena、Leaderboard](/04-evaluation-observability/06-benchmark-arena-leaderboard)

## Bundle

一次运行或比较沉淀下来的文件集合。

它让结果可以被复盘，而不是只剩一个 JSON 分数。

对应阅读：

- [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)

## Dataset Registry

训练数据登记表。

它回答：

- 同一份数据是否被多次使用
- dataset sha 是否变化
- 训练方法和模型对应哪些数据
- 两份数据的差异在哪里

对应阅读：

- [数据集、Run、Checkpoint](/05-finetuning-training/04-datasets-runs-checkpoints)

## LoRA

一种常见的参数高效微调方法。

当前仓库用 mock 训练流程表达 LoRA 训练产物结构。

对应阅读：

- [LoRA、QLoRA、PEFT](/05-finetuning-training/01-lora-qlora-peft)

## QLoRA

结合量化加载和 LoRA 的微调方式。

当前 finetune-demo 会校验 QLoRA 配置中的 `load_in_4bit`。

对应阅读：

- [LoRA、QLoRA、PEFT](/05-finetuning-training/01-lora-qlora-peft)

## Checkpoint

训练过程中保存的中间产物。

当前仓库里，checkpoint 是 export adapter 的来源。

对应阅读：

- [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)

## Export

把训练 checkpoint 转成后续可以评测或部署的资产。

export 不只是复制文件。它应该记录：

- source checkpoint
- base model
- adapter hash
- export status
- lineage

对应阅读：

- [Finetune 产物证据](/13-output-gallery/03-finetune-artifact-evidence)

## Manifest

产物清单。

当前仓库里，manifest 用来记录：

- run 输出
- artifact 文件
- export 文件
- size
- sha256

对应阅读：

- [Finetune 复现资产 Lab](/07-hands-on-labs/04-finetune-reproducibility-lab)

## Artifact

一次运行留下的可复盘产物。

artifact 可以是：

- JSON
- Markdown
- manifest
- index
- sample outputs
- comparison report
- checkpoint metadata

artifact 的重点不是“文件很多”，而是让未来的人能解释当时发生了什么。

对应阅读：

- [产物与文件索引](/09-reference/03-artifacts-and-files)

## Smoke Test

端到端最小联调测试。

当前命令：

```bash
PYTHON=.venv/bin/python make infra-smoke
```

它验证四个项目的最小闭环仍然成立。

对应阅读：

- [质量与维护入口](/06-projects/07-quality-and-maintenance)

## public-check

公开发布前的综合检查入口。

它会把安全扫描、测试、文档质量和文档构建连起来跑，适合在准备提交、PR 或发布前执行。

当前推荐命令：

```bash
PYTHON=.venv/bin/python make public-check
```

如果 shell 找不到 `npm`，通常是 Node 环境没加载；先执行 `nvm use 22` 或用加载 nvm 的 shell 重跑。

对应阅读：

- [公开仓库卫生规范](/08-publication/06-public-repo-hygiene)

## VitePress

当前文档站使用的静态站点框架。

它负责：

- Markdown 渲染
- nav/sidebar
- 首页组件
- 本地 dev/preview
- 静态构建

对应阅读：

- [GitHub Pages 发布指南](/08-publication/01-github-pages)

## GitHub Pages

GitHub 提供的静态站点托管能力。

当前项目通过 GitHub Actions 构建 VitePress 并部署到 Pages。

它适合对外发布稳定批次，不适合替代本地调试。

对应阅读：

- [GitHub Pages 发布指南](/08-publication/01-github-pages)
