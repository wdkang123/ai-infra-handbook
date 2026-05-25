# 学习者工作簿

这页给学习者边学边记录用。

如果你只是阅读，很多概念会看起来都懂。真正有效的学习方式，是每一阶段都留下三个东西：

1. 我理解了什么
2. 我运行了什么
3. 我看到了什么证据

下面的模板可以直接复制到自己的笔记里。

## 学习者信息

```text
学习者：
日期：
机器环境：
Node 版本：
Python 版本：
当前目标：
```

## 阶段 1：系统地图

先读：

- [什么是 AI Infra](/00-overview/01-what-is-ai-infra)
- [四个项目怎么连成系统](/06-projects/06-end-to-end-system-map)

记录：

```text
我理解的四层结构：

1. inference-service：
2. ai-gateway：
3. eval-module：
4. finetune-demo：

我现在还不确定的问题：

-
-
-
```

自测：

- 我能解释 gateway 和 inference-service 的边界
- 我能解释 eval-module 为什么不是普通脚本
- 我能解释 finetune-demo 为什么需要 manifest 和 history

## 阶段 2：本地运行

先读：

- [最小运行手册](/00-overview/03-runbook)
- [第一次实操演练](/00-overview/04-first-walkthrough)

运行记录：

```text
安装命令：


启动命令：


检查命令：


遇到的问题：


解决方式：

```

证据记录：

```text
文档站地址：
inference health：
gateway health：
infra-check 结果：
infra-smoke 结果：
```

如果你不知道输出是否正确，对照：

- [Serving 与 Gateway 输出证据](/13-output-gallery/01-serving-gateway-evidence)
- [验证矩阵](/09-reference/07-validation-matrix)

## 阶段 3：请求链路

先读：

- [从请求到首个 Token](/01-llm-fundamentals/04-from-request-to-first-token)
- [健康检查、Metrics、Request ID](/03-ai-gateway-platform/02-health-metrics-request-id)

记录一次请求：

```text
请求入口：
请求模型：
request id：
是否经过 gateway：
是否命中 fallback：
是否命中 cache：
响应状态：
响应摘要：
```

证据位置：

```text
响应 header：
gateway /events：
gateway /events/summary：
gateway /events/requests/{request_id}：
inference /events：
inference /metrics：
```

复盘问题：

1. 这次请求经过了哪些组件？
2. 哪个证据能证明 request id 被贯穿？
3. 如果失败，我会先查 gateway 还是 inference？为什么？

## 阶段 4：评测与发布判断

先读：

- [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
- [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)
- [Eval 报告证据](/13-output-gallery/02-eval-report-evidence)

记录一次 eval：

```text
task：
model：
backend：
result file：
sample outputs：
sample analysis：
leaderboard：
comparison：
release recommendation：
```

复盘问题：

1. 这次评测的 baseline 和 candidate 是否可比？
2. 是否有指标提升但样本质量下降的情况？
3. release recommendation 为什么是这个结论？
4. 如果要上线，我还需要哪些生产证据？

## 阶段 5：训练与产物复现

先读：

- [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)
- [实验追踪、History、复现](/05-finetuning-training/06-experiment-tracking-history-reproducibility)
- [Finetune 产物证据](/13-output-gallery/03-finetune-artifact-evidence)

记录一次训练：

```text
base model：
dataset path：
dataset version：
training method：
output dir：
run manifest：
checkpoint index：
export manifest：
export history：
```

复盘问题：

1. 这次训练能否被别人复现？
2. dataset registry 里能看到哪些信息？
3. export manifest 能否追溯到 checkpoint？
4. 如果后续 eval 使用这个 adapter，要记录哪些来源？

## 阶段 6：端到端复盘

先读：

- [端到端复盘证据包](/13-output-gallery/04-end-to-end-review-packet)
- [系统 Capstone 与验收 Rubric](/07-hands-on-labs/05-capstone-review-rubric)
- [Capstone 答辩稿](/10-assessments/04-capstone-defense)

复盘模板：

```text
这次复盘的目标：

系统结构：

我跑通的链路：

关键命令：

关键证据：

一次失败或异常：

我如何定位：

我现在最清楚的概念：

我仍然模糊的概念：

下一步计划：
```

验收标准：

- 我能讲清四个项目的职责
- 我能解释一次请求的证据链
- 我能解释一次 eval 的发布判断
- 我能解释一次训练产物的 lineage
- 我能说明当前学习型实现和生产系统的差距

## 学习记录评分

| 级别 | 表现 |
| --- | --- |
| 1 | 只记录读了哪些页面 |
| 2 | 记录了命令和是否成功 |
| 3 | 记录了关键输出和证据位置 |
| 4 | 能用证据解释系统行为 |
| 5 | 能把失败、判断和下一步改进写成工程复盘 |

目标不是追求一次达到 5，而是每轮学习都比上一轮更能“用证据说话”。
