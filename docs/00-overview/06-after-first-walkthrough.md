# 第一次跑完之后学什么

## 为什么要有这一页

第一次 walkthrough 跑通之后，最常见的新问题是：

- 我已经把四个项目串起来了一遍
- 也大概知道它们各自负责什么
- 那接下来应该往哪条线深入？
- 我该继续读文档、改代码，还是做自测？

如果没有第二步路线，第一次实操很容易停在“我跑过一次”。这页就是帮你把第一次跑通，变成后续深入学习的起点。

## 最不建议的下一步

第一次跑完之后，最不建议的是：

- 同时改四个项目
- 同时补很多功能
- 同时看很多目录
- 一边看 serving，一边看 training，一边又想改 GitHub workflow

这样很容易重新陷入信息过载。

更稳的方式是：从四条主线里挑一条，连续深入两到三轮。

## 先做一次复盘

在选主线之前，建议先写下：

```text
我刚才跑通了哪些命令：
我看到了哪些输出：
我知道哪些输出是什么意思：
我还有哪些输出看不懂：
我最想继续理解哪一层：
```

如果你能写出来，说明第一次 walkthrough 没有白跑。

如果写不出来，先回看：

- [示例输出与证据库](/13-output-gallery/00-overview)
- [产物与文件索引](/09-reference/03-artifacts-and-files)
- [API Surface 速查](/09-reference/05-api-surface)

## 四条深入主线

### 主线一：理解“请求为什么会变成结果”

优先走推理服务主线：

1. [Prefill、Decode、KV Cache](/01-llm-fundamentals/02-prefill-decode-kv-cache)
2. [从请求到首个 Token](/01-llm-fundamentals/04-from-request-to-first-token)
3. [vLLM](/02-inference-serving/04-vllm)
4. [Cache 与 Prefix Caching](/02-inference-serving/06-cache-prefix-caching)
5. [Streaming、Batching、Metrics](/02-inference-serving/09-streaming-batching-metrics)
6. 回看 [inference-service](/06-projects/01-inference-service)

这条线最适合你把“执行层”真的看懂。

你应该能回答：

- TTFT 和 ITL 为什么不是一个指标
- streaming 为什么会改变错误处理
- mock engine 和真实 serving runtime 的边界在哪里
- metrics 和 events 如何证明请求发生过

### 主线二：理解“平台层为什么存在”

优先走 gateway 主线：

1. [鉴权、路由、限流](/03-ai-gateway-platform/01-auth-routing-rate-limit)
2. [健康检查、Metrics、Request ID](/03-ai-gateway-platform/02-health-metrics-request-id)
3. [Gateway、Router、Fallback、Cache](/03-ai-gateway-platform/03-gateway-router-fallback-cache)
4. [Streaming、错误路径、Upstream Health](/03-ai-gateway-platform/04-streaming-errors-upstream-health)
5. [平台层与模型服务层边界](/03-ai-gateway-platform/05-platform-vs-model-service)
6. [外部模型名与内部目标映射](/03-ai-gateway-platform/06-model-name-to-target-mapping)
7. 回看 [ai-gateway](/06-projects/02-ai-gateway)

这条线最适合你建立“入口治理”和“执行服务”分层。

你应该能回答：

- 为什么 gateway 不是普通 HTTP proxy
- `401 / 429 / 502` 分别更可能来自哪里
- fallback 成功为什么也需要记录
- request id 为什么是排障主线

### 主线三：理解“质量怎么形成闭环”

优先走 eval / observability 主线：

1. [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
2. [Benchmark、Leaderboard、Observability](/04-evaluation-observability/02-benchmark-leaderboard-observability)
3. [Tracing、Metrics、Logs](/04-evaluation-observability/03-observability-traces-metrics-logs)
4. [LLM Evaluation](/04-evaluation-observability/05-llm-evaluation)
5. [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)
6. [Benchmark 与生产质量不是一回事](/04-evaluation-observability/08-benchmark-vs-production-quality)
7. 回看 [eval-module](/06-projects/03-eval-module)

这条线会帮助你从“会跑命令”进到“会做判断”。

你应该能回答：

- 为什么 run 不是终点
- compare 为什么要校验 task
- leaderboard 为什么不能替代样本分析
- observability 如何帮助解释 eval 退化

### 主线四：理解“训练工程长什么样”

优先走 finetune 主线：

1. [LoRA、QLoRA、PEFT](/05-finetuning-training/01-lora-qlora-peft)
2. [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)
3. [Unsloth 与训练栈](/05-finetuning-training/03-unsloth-training-stack)
4. [数据集、Run、Checkpoint](/05-finetuning-training/04-datasets-runs-checkpoints)
5. [实验追踪、History、复现](/05-finetuning-training/06-experiment-tracking-history-reproducibility)
6. [什么时候该微调](/05-finetuning-training/07-when-to-finetune)
7. 回看 [finetune-demo](/06-projects/04-finetune-demo)

这条线最适合你形成“训练不只是命令，而是一组资产”的理解。

你应该能回答：

- dataset registry 解决什么问题
- checkpoint index 为什么重要
- export manifest 为什么需要 lineage
- 训练结果如何进入 eval

## 第一次跑完之后，怎么改代码最稳

这时最适合做的不是大改，而是单点小改：

- 改一条 mock 文本
- 改一个限流阈值
- 改一个 eval 输出字段
- 改一个 finetune 指标
- 给某个 events summary 增加一个聚合字段
- 给某个 manifest 增加一个可解释字段

改完以后重跑，再看结果怎么变。

这样你会把：

- 文档
- 代码
- 测试
- 输出结果
- 复盘证据

真正绑在一起。

## 推荐的三轮学习法

### 第一轮：跑通

目标是完成第一次 walkthrough。

你只需要知道：

- 项目能启动
- 命令能跑
- 输出在哪里
- 页面怎么互相链接

### 第二轮：解释

目标是解释每个输出的意义。

你需要开始看：

- headers
- metrics
- events
- run report
- manifest
- history

### 第三轮：改动

目标是做一个小改动并验证。

你需要说明：

- 改了哪一层
- 为什么改
- 风险是什么
- 跑了什么验证
- 输出证据怎么变化

这三轮走完，学习会比单纯看文档深很多。

## 什么时候做自测

如果你已经完成一次 walkthrough，可以开始做：

- [系统地图自测](/10-assessments/01-system-map-check)

如果你已经深入 serving/gateway，可以做：

- [Serving 与 Gateway 自测](/10-assessments/02-serving-gateway-quiz)

如果你已经深入 eval/finetune，可以做：

- [Eval 与 Finetune 自测](/10-assessments/03-eval-finetune-quiz)

如果你准备公开展示，可以做：

- [Capstone 答辩稿](/10-assessments/04-capstone-defense)

## 这一页学完应该带走什么

第一次跑通只是起点。

后面最重要的不是“继续同时看全部内容”，而是选一条主线连续深入。你要从“我跑过一次”走向：

- 我能解释一次请求
- 我能定位一次失败
- 我能比较一次 eval
- 我能追溯一次 export
- 我能设计一个小改动并验证

这时系统感才会真正长出来。

## 常见误区

### 误区一：第一次跑通后马上重构

太早。先做小改动，观察系统证据如何变化。

### 误区二：觉得自己必须一次学完所有模块

不需要。四条主线可以分轮推进。

### 误区三：只看文档，不看输出

这个项目的学习价值很大一部分在输出证据里。

### 误区四：只看输出，不回到系统图

输出必须放回系统层次里解释，否则很容易碎片化。
