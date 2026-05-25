# 按目标选择学习路径

## 为什么这一页有用

因为不是每个人开始学 AI Infra 时，关注点都一样。

有人最想搞懂：

- 请求到底怎么变成结果

有人更想搞懂：

- 平台层为什么存在

也有人更关心：

- 怎么做评测闭环
- 什么时候该微调
- 怎么把项目分享给别人一起学

如果你已经知道自己更关心哪一类问题，这一页会比从头顺读更高效。

## 如果你更想学“推理服务”

你最适合走这条线：

1. [什么是 AI Infra](/00-overview/01-what-is-ai-infra)
2. [Prefill、Decode、KV Cache](/01-llm-fundamentals/02-prefill-decode-kv-cache)
3. [从请求到首个 Token](/01-llm-fundamentals/04-from-request-to-first-token)
4. [vLLM](/02-inference-serving/04-vllm)
5. [Streaming、Batching、Metrics](/02-inference-serving/09-streaming-batching-metrics)
6. [inference-service](/06-projects/01-inference-service)
7. [Serving 与 Gateway 输出证据](/13-output-gallery/01-serving-gateway-evidence)

这条线会让你最快建立“执行层”直觉。

## 如果你更想学“平台层和网关”

你最适合走这条线：

1. [学习路线图](/00-overview/02-learning-route)
2. [鉴权、路由、限流](/03-ai-gateway-platform/01-auth-routing-rate-limit)
3. [健康检查、Metrics、Request ID](/03-ai-gateway-platform/02-health-metrics-request-id)
4. [平台层与模型服务层边界](/03-ai-gateway-platform/05-platform-vs-model-service)
5. [外部模型名与内部目标映射](/03-ai-gateway-platform/06-model-name-to-target-mapping)
6. [ai-gateway](/06-projects/02-ai-gateway)
7. [失败症状到证据地图](/13-output-gallery/05-failure-evidence-map)

这条线会让你更快形成“治理层”和“执行层”的分层感。

## 如果你更想学“评测与发布判断”

你最适合走这条线：

1. [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
2. [Tracing、Metrics、Logs](/04-evaluation-observability/03-observability-traces-metrics-logs)
3. [LLM Evaluation](/04-evaluation-observability/05-llm-evaluation)
4. [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)
5. [Benchmark 与生产质量不是一回事](/04-evaluation-observability/08-benchmark-vs-production-quality)
6. [eval-module](/06-projects/03-eval-module)
7. [Eval 报告证据](/13-output-gallery/02-eval-report-evidence)

这条线最适合你建立“结果怎么变成判断”的思维。

## 如果你更想学“训练与微调”

你最适合走这条线：

1. [LoRA、QLoRA、PEFT](/05-finetuning-training/01-lora-qlora-peft)
2. [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)
3. [数据集、Run、Checkpoint](/05-finetuning-training/04-datasets-runs-checkpoints)
4. [什么时候该微调](/05-finetuning-training/07-when-to-finetune)
5. [从 Demo Training 到真实训练系统](/05-finetuning-training/08-from-demo-training-to-real-training-system)
6. [finetune-demo](/06-projects/04-finetune-demo)
7. [Finetune 产物证据](/13-output-gallery/03-finetune-artifact-evidence)

这条线最适合你建立“训练工程资产”直觉。

## 如果你更想做“公开分享和共学”

你最适合走这条线：

1. [面向分享的学习方式](/00-overview/11-public-learning-guide)
2. [共学与公开分享套件](/14-workshop-kit/00-overview)
3. [讲师与带练指南](/14-workshop-kit/01-facilitator-guide)
4. [学习者工作簿](/14-workshop-kit/02-learner-workbook)
5. [复盘与评审模板](/14-workshop-kit/04-review-templates)
6. [GitHub 发布计划](/14-workshop-kit/06-github-release-plan)
7. [公开发布验收 Lab](/07-hands-on-labs/06-public-release-readiness-lab)

这条线最适合你把个人学习项目整理成可以公开带练、收反馈和持续维护的学习站。

## 如果你还拿不准自己最该学哪条

最稳的还是走默认顺序：

1. [什么是 AI Infra](/00-overview/01-what-is-ai-infra)
2. [学习路线图](/00-overview/02-learning-route)
3. [最小运行手册](/00-overview/03-runbook)
4. [第一次实操演练](/00-overview/04-first-walkthrough)
5. [示例输出与证据库](/13-output-gallery/00-overview)
6. [学习者工作簿](/14-workshop-kit/02-learner-workbook)

跑完一轮之后，再回来看你最想深挖哪条线。

## 这一页学完应该带走什么

学习这套仓库，不一定非得所有内容按同一顺序推进。  
如果你已经知道自己的兴趣重点，可以直接选一条主线先深入。
