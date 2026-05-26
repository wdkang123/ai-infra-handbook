# 按目标选择学习路径

## 为什么这一页有用

不是每个人开始学 AI Infra 时，关注点都一样。

有人最想搞懂：

- 请求到底怎么变成结果
- 为什么 vLLM、SGLang、Triton 这些工具会出现
- streaming、batching、KV Cache 到底和普通后端服务有什么区别

有人更想搞懂：

- 平台层为什么存在
- gateway 和 inference-service 为什么要拆开
- fallback、cache、rate limit、request id 怎么形成治理能力

也有人更关心：

- 怎么做评测闭环
- 什么时候该微调
- 怎么把项目分享给别人一起学
- 怎么把仓库长期维护好

如果你已经知道自己更关心哪一类问题，这一页会比从头顺读更高效。

## 先判断你的学习目标

先选一个最像你的问题：

| 你最想解决的问题 | 推荐主线 |
| --- | --- |
| 我想知道请求怎么变成 token 和回答 | 推理服务主线 |
| 我想知道为什么需要 AI Gateway | 平台治理主线 |
| 我想知道模型输出怎么判断好坏 | 评测与发布判断主线 |
| 我想知道微调系统怎么组织 | 训练与微调主线 |
| 我想把项目分享给别人一起学 | 公开分享与共学主线 |
| 我想以后把 demo 迁移得更真实 | 生产迁移主线 |
| 我现在完全没方向 | 默认路线 |

选择主线不是永久选择。你可以先连续深入一条线，两三轮之后再切换。

## 如果你更想学推理服务

你最适合走这条线：

1. [什么是 AI Infra](/00-overview/01-what-is-ai-infra)
2. [模型、Token、Context](/01-llm-fundamentals/01-model-token-context)
3. [Prefill、Decode、KV Cache](/01-llm-fundamentals/02-prefill-decode-kv-cache)
4. [从请求到首个 Token](/01-llm-fundamentals/04-from-request-to-first-token)
5. [vLLM](/02-inference-serving/04-vllm)
6. [SGLang](/02-inference-serving/05-sglang)
7. [Cache 与 Prefix Caching](/02-inference-serving/06-cache-prefix-caching)
8. [Streaming、Batching、Metrics](/02-inference-serving/09-streaming-batching-metrics)
9. [inference-service](/06-projects/01-inference-service)
10. [Serving 与 Gateway 输出证据](/13-output-gallery/01-serving-gateway-evidence)

这条线会让你最快建立执行层直觉。

学完后你应该能回答：

- 为什么 token 是共同计量单位
- TTFT 和 ITL 为什么不同
- KV Cache 为什么影响显存和并发
- streaming 为什么会改变错误处理
- vLLM / SGLang 解决的是哪一层问题
- 当前 `inference-service` 哪些边界未来可以替换成真实后端

建议动手任务：

- 跑一次 inference-service 的 `/health`、`/v1/models`、`/v1/chat/completions`
- 触发一次 unknown model
- 查看 `/metrics` 和 `/events`
- 对照 [API Surface 速查](/09-reference/05-api-surface) 解释输出

## 如果你更想学平台层和网关

你最适合走这条线：

1. [学习路线图](/00-overview/02-learning-route)
2. [AI Gateway Platform](/03-ai-gateway-platform/00-overview)
3. [鉴权、路由、限流](/03-ai-gateway-platform/01-auth-routing-rate-limit)
4. [健康检查、Metrics、Request ID](/03-ai-gateway-platform/02-health-metrics-request-id)
5. [Gateway、Router、Fallback、Cache](/03-ai-gateway-platform/03-gateway-router-fallback-cache)
6. [Streaming、错误路径、Upstream Health](/03-ai-gateway-platform/04-streaming-errors-upstream-health)
7. [平台层与模型服务层边界](/03-ai-gateway-platform/05-platform-vs-model-service)
8. [外部模型名与内部目标映射](/03-ai-gateway-platform/06-model-name-to-target-mapping)
9. [ai-gateway](/06-projects/02-ai-gateway)
10. [失败症状到证据地图](/13-output-gallery/05-failure-evidence-map)

这条线会让你形成治理层和执行层的分层感。

学完后你应该能回答：

- Gateway 为什么不是普通 HTTP proxy
- `401 / 404 / 429 / 502` 更可能来自哪一层
- fallback 成功为什么也要记录
- response cache 为什么要隔离
- `x-request-id` 如何连接 response、events 和 timeline
- 外部模型名和内部 target 为什么要解耦

建议动手任务：

- 用正确 token 调一次 gateway
- 用错误 token 触发 `401`
- 调 unknown model 触发 `404`
- 观察 `x-cache`、`x-upstream-model`、`x-fallback-used`
- 查看 gateway `/events/failures`

## 如果你更想学评测与发布判断

你最适合走这条线：

1. [Evaluation Observability](/04-evaluation-observability/00-overview)
2. [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
3. [Benchmark、Leaderboard、Observability](/04-evaluation-observability/02-benchmark-leaderboard-observability)
4. [Tracing、Metrics、Logs](/04-evaluation-observability/03-observability-traces-metrics-logs)
5. [评测工具与展示面](/04-evaluation-observability/04-evaluation-tools-and-surfaces)
6. [LLM Evaluation](/04-evaluation-observability/05-llm-evaluation)
7. [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)
8. [Benchmark 与生产质量不是一回事](/04-evaluation-observability/08-benchmark-vs-production-quality)
9. [eval-module](/06-projects/03-eval-module)
10. [Eval 报告证据](/13-output-gallery/02-eval-report-evidence)

这条线最适合你建立“结果怎么变成判断”的思维。

学完后你应该能回答：

- run 为什么不是终点
- compare 为什么要校验 task
- min_delta 为什么会影响 recommendation
- leaderboard 为什么不能替代样本分析
- observability 如何帮助解释 eval 退化
- 发布判断为什么要同时看质量、延迟、成本和稳定性

建议动手任务：

- 跑一次 eval
- 生成 compare report
- 查看 run history 和 leaderboard
- 写一段 promote / review / reject 的发布判断

## 如果你更想学训练与微调

你最适合走这条线：

1. [Finetuning Training](/05-finetuning-training/00-overview)
2. [LoRA、QLoRA、PEFT](/05-finetuning-training/01-lora-qlora-peft)
3. [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)
4. [Unsloth 与训练栈](/05-finetuning-training/03-unsloth-training-stack)
5. [数据集、Run、Checkpoint](/05-finetuning-training/04-datasets-runs-checkpoints)
6. [SFT、DPO 与训练目标](/05-finetuning-training/05-sft-dpo-and-training-objectives)
7. [实验追踪、History、复现](/05-finetuning-training/06-experiment-tracking-history-reproducibility)
8. [什么时候该微调](/05-finetuning-training/07-when-to-finetune)
9. [从 Demo Training 到真实训练系统](/05-finetuning-training/08-from-demo-training-to-real-training-system)
10. [finetune-demo](/06-projects/04-finetune-demo)
11. [Finetune 产物证据](/13-output-gallery/03-finetune-artifact-evidence)

这条线最适合你建立训练工程资产直觉。

学完后你应该能回答：

- 微调什么时候不是第一选择
- dataset registry 解决什么问题
- checkpoint index 为什么重要
- export manifest 为什么需要 lineage
- training run 和 eval run 如何连接
- Unsloth、PEFT、TRL、Transformers 分别更像哪一层工具

建议动手任务：

- 查看 sample dataset
- 跑一次 train
- 查看 run state 和 checkpoint index
- 跑一次 export
- 查看 export manifest 和 export history
- 用 dataset diff 理解数据变化

## 如果你更想做公开分享和共学

你最适合走这条线：

1. [面向分享的学习方式](/00-overview/11-public-learning-guide)
2. [共学与公开分享套件](/14-workshop-kit/00-overview)
3. [讲师与带练指南](/14-workshop-kit/01-facilitator-guide)
4. [学习者工作簿](/14-workshop-kit/02-learner-workbook)
5. [学习小组议程](/14-workshop-kit/03-study-group-agenda)
6. [复盘与评审模板](/14-workshop-kit/04-review-templates)
7. [贡献者协作手册](/14-workshop-kit/05-contribution-playbook)
8. [GitHub 发布计划](/14-workshop-kit/06-github-release-plan)
9. [公开发布验收 Lab](/07-hands-on-labs/06-public-release-readiness-lab)
10. [GitHub 入口与协作地图](/08-publication/14-github-entrypoints)

这条线最适合你把个人学习项目整理成可以公开带练、收反馈和持续维护的学习站。

学完后你应该能回答：

- 新读者应该从哪里开始
- 共学活动要交付什么
- 讲师如何判断学员是否跑对
- issue 和 PR 应该如何承接学习反馈
- 公开发布前要做哪些安全和质量检查

建议动手任务：

- 用学习者工作簿记录一次 walkthrough
- 准备一次 90 分钟导览
- 写一份 Capstone 展示提纲
- 生成首发运营包并检查 starter issues

## 如果你更想做生产迁移

你最适合走这条线：

1. [生产迁移路线总览](/12-production-migration/00-overview)
2. [Serving 后端迁移](/12-production-migration/01-serving-backend-migration)
3. [Gateway 平台化加固](/12-production-migration/02-gateway-platform-hardening)
4. [Eval 评测系统迁移](/12-production-migration/03-eval-judge-dashboard-migration)
5. [Finetune 真实训练迁移](/12-production-migration/04-finetune-real-training-migration)
6. [验证矩阵](/09-reference/07-validation-matrix)
7. [示例输出与证据库](/13-output-gallery/00-overview)

这条线适合你思考“当前学习系统如何一步步变真实”。

学完后你应该能回答：

- 哪些接口不能轻易变
- 哪些内部实现可以替换
- 每一步迁移要保留哪些证据
- 为什么不能一口气同时替换四层
- 真实依赖如何不破坏公开学习体验

## 如果你还拿不准自己最该学哪条

最稳的还是走默认顺序：

1. [什么是 AI Infra](/00-overview/01-what-is-ai-infra)
2. [学习路线图](/00-overview/02-learning-route)
3. [最小运行手册](/00-overview/03-runbook)
4. [第一次实操演练](/00-overview/04-first-walkthrough)
5. [第一次跑完之后学什么](/00-overview/06-after-first-walkthrough)
6. [示例输出与证据库](/13-output-gallery/00-overview)
7. [学习者工作簿](/14-workshop-kit/02-learner-workbook)

跑完一轮之后，再回来看你最想深挖哪条线。

## 怎么判断自己选对了

选对路线的感觉通常是：

- 你能连续读三四页而不频繁迷路
- 你能把一个概念连接到项目文件或输出证据
- 你能提出一个小改动
- 你知道改完应该跑什么验证

如果你读着读着发现每页都像新世界，说明可以回到总览页或第一次 walkthrough 重新补系统地图。

## 常见误区

### 误区一：必须按目录顺序学

不必。目录顺序适合完整学习，但按目标选择路线更适合已有方向的读者。

### 误区二：选了主线就不能切换

可以切换，但建议每条线至少连续深入几页，不要每十分钟换一次。

### 误区三：只选自己熟悉的线

熟悉的线容易给成就感，但不熟悉的边界往往更能补系统短板。

### 误区四：只读不跑

每条线都应该至少配一个动手任务，否则很容易停留在概念层。

## 这一页学完应该带走什么

学习这套仓库，不一定非得所有内容按同一顺序推进。

如果你已经知道自己的兴趣重点，可以直接选一条主线先深入；如果还不确定，就先跑默认路线，用输出证据帮你找到下一步。
