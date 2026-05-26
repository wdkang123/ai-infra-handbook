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

## 先判断你现在卡在哪一类问题

很多人第一次跑完之后会说“感觉懂了一点，但不知道怎么继续”。这通常不是学习能力问题，而是问题没有分类。

可以先把自己的困惑放到下面四类里：

| 困惑类型 | 常见表现 | 下一步 |
| --- | --- | --- |
| 流程困惑 | 知道命令跑完了，但不知道每步在系统里代表什么 | 回到系统地图和请求链路 |
| 证据困惑 | 看到了 headers、events、manifest，但不知道怎么看 | 先读示例输出与证据库 |
| 边界困惑 | 不知道 gateway、serving、eval、finetune 为什么分开 | 选一条主线连续读三页 |
| 改动困惑 | 想动手，但不知道改哪里风险小 | 做一个单点小改动并复盘 |

这一步很重要。因为不同困惑需要不同解法。流程困惑靠路线图，证据困惑靠输出样例，边界困惑靠章节深读，改动困惑靠小实验。如果把它们混在一起，就会变成“我应该再看点什么”，最后又回到无目的浏览。

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

一个很小但有效的实验是：改一条 mock response 的 token 输出节奏，或者增加一个 events 字段，然后重新跑 serving lab。你不需要马上接真实 vLLM，只要能解释“输出变化在哪里被记录”，就已经从调用接口走向理解执行层。

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

这条线最适合做的实验是制造错误。比如用错误 token、unknown model、不可达 upstream、重复请求分别触发 auth、routing、fallback、cache 路径。Gateway 的学习价值不在“成功转发了一次”，而在你能解释失败为什么停在这一层。

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

这条线最适合做的实验是制造一个候选版本。哪怕只是改一个 mock 输出，也可以跑 baseline 和 candidate，再看 compare report 如何描述变化。你要训练的不是“分数怎么更高”，而是“一个变化如何被证据表达”。

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

这条线最适合做的实验是追溯资产。先从 export manifest 往前找 checkpoint，再找 run，再找 dataset。只要你能讲清这条链路，就会明白训练工程为什么不应该只留下一个目录或一个权重文件。

## 选主线时可以用这个判断

如果你暂时不知道选哪条线，可以按目标反推：

| 你想获得的能力 | 优先主线 | 典型产物 |
| --- | --- | --- |
| 能解释一次模型请求为什么慢 | 推理服务 | request timeline、streaming events |
| 能解释一次平台错误为什么发生 | Gateway | failure summary、request id、metrics |
| 能判断一个候选版本能不能发布 | Eval | compare report、sample analysis |
| 能解释一个训练产物从哪里来 | Finetune | run manifest、checkpoint index、export manifest |
| 能把项目讲给别人听 | 案例复盘 | 现象、证据、判断、下一步 |

不要用“哪条更高级”来选。四条线都重要，区别只在于你现在最想训练哪种工程判断。

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

这一轮不要急着评价代码好不好，也不要急着比较真实框架。先让系统在你脑子里从一堆目录变成一条路。

### 第二轮：解释

目标是解释每个输出的意义。

你需要开始看：

- headers
- metrics
- events
- run report
- manifest
- history

这一轮建议你每看到一个输出，都问两个问题：

- 它来自哪一层？
- 它能证明什么，不能证明什么？

比如 `x-request-id` 能帮助串联请求，但不能证明回答质量；`compare report` 能说明候选和基线的差异，但不能自动证明可以生产发布。把边界讲清楚，理解会稳很多。

### 第三轮：改动

目标是做一个小改动并验证。

你需要说明：

- 改了哪一层
- 为什么改
- 风险是什么
- 跑了什么验证
- 输出证据怎么变化

这三轮走完，学习会比单纯看文档深很多。

### 第四轮：讲述

如果你准备把项目放到 GitHub，建议再加一轮“讲述”。

讲述不是复述文档，而是把你的理解组织成一个别人能跟上的故事：

```text
我先跑通了哪条链路。
我重点选择了哪一层。
我做了哪个小改动。
这个改动让哪些输出发生变化。
这些输出说明了什么。
还有哪些地方只是学习型实现。
```

这轮会暴露很多隐藏问题。凡是你讲不清的地方，通常就是下一轮最值得补的页面、lab 或案例。

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

### 误区五：把学习路线当成考试路线

这套站点不是要求你按顺序背完所有章节。更好的方式是围绕一个真实问题反复来回：

```text
问题 -> 路线页 -> 项目页 -> 输出证据 -> 案例复盘 -> 小改动 -> 自测
```

这种来回会比线性阅读更接近真实工程学习。
