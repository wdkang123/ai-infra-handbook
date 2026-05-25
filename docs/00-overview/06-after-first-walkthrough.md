# 第一次跑完之后学什么

## 为什么要有这一页

因为第一次 walkthrough 跑通之后，最常见的新问题就是：

- 我已经把四个项目串起来了一遍
- 也大概知道它们各自负责什么
- 那接下来应该往哪条线深入？

如果没有第二步路线，第一次实操很容易就停在“我跑过一次”。

## 最不建议的下一步是什么

第一次跑完之后，最不建议的是：

- 同时改四个项目
- 同时补很多功能
- 同时看很多目录

这样很容易重新陷入信息过载。

## 更稳的方式：选一条主线连续深入

更好的做法是：  
从四条主线里挑一条，连续深入两到三轮。

这样你会更快形成真正的系统直觉。

## 如果你更想理解“请求为什么会变成结果”

优先走推理服务主线：

1. [Prefill、Decode、KV Cache](/01-llm-fundamentals/02-prefill-decode-kv-cache)
2. [从请求到首个 Token](/01-llm-fundamentals/04-from-request-to-first-token)
3. [vLLM](/02-inference-serving/04-vllm)
4. [Streaming、Batching、Metrics](/02-inference-serving/09-streaming-batching-metrics)
5. 回看 [inference-service](/06-projects/01-inference-service)

这条线最适合你把“执行层”真的看懂。

## 如果你更想理解“平台层为什么存在”

优先走 gateway 主线：

1. [鉴权、路由、限流](/03-ai-gateway-platform/01-auth-routing-rate-limit)
2. [健康检查、Metrics、Request ID](/03-ai-gateway-platform/02-health-metrics-request-id)
3. [Streaming、错误路径、Upstream Health](/03-ai-gateway-platform/04-streaming-errors-upstream-health)
4. [平台层与模型服务层边界](/03-ai-gateway-platform/05-platform-vs-model-service)
5. [外部模型名与内部目标映射](/03-ai-gateway-platform/06-model-name-to-target-mapping)
6. 回看 [ai-gateway](/06-projects/02-ai-gateway)

这条线最适合你建立“入口治理”和“执行服务”分层。

## 如果你更想理解“质量怎么形成闭环”

优先走 eval / observability 主线：

1. [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
2. [Tracing、Metrics、Logs](/04-evaluation-observability/03-observability-traces-metrics-logs)
3. [LLM Evaluation](/04-evaluation-observability/05-llm-evaluation)
4. [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)
5. 回看 [eval-module](/06-projects/03-eval-module)

这条线会帮助你从“会跑命令”进到“会做判断”。

## 如果你更想理解“训练工程长什么样”

优先走 finetune 主线：

1. [LoRA、QLoRA、PEFT](/05-finetuning-training/01-lora-qlora-peft)
2. [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)
3. [数据集、Run、Checkpoint](/05-finetuning-training/04-datasets-runs-checkpoints)
4. [实验追踪、History、复现](/05-finetuning-training/06-experiment-tracking-history-reproducibility)
5. [什么时候该微调](/05-finetuning-training/07-when-to-finetune)
6. 回看 [finetune-demo](/06-projects/04-finetune-demo)

这条线最适合你形成“训练不只是命令，而是一组资产”的理解。

## 第一次跑完之后，怎么改代码最稳

这时最适合做的，不是大改，而是单点小改：

- 改一条 mock 文本
- 改一个限流阈值
- 改一个 eval 输出字段
- 改一个 finetune 指标

改完以后重跑，再看结果怎么变。

这会让你把：

- 文档
- 代码
- 输出结果

真正绑在一起。

## 这一页学完应该带走什么

第一次跑通只是起点。  
后面最重要的不是“继续同时看全部内容”，而是选一条主线连续深入，这样系统感才会真正长出来。
