# 学习者工作簿

这页给学习者边学边记录用。

如果你只是阅读，很多概念会看起来都懂。真正有效的学习方式，是每一阶段都留下三个东西：

1. 我理解了什么
2. 我运行了什么
3. 我看到了什么证据

下面的模板可以直接复制到自己的笔记里。

## 怎么使用这份工作簿

这份工作簿不是让你写漂亮笔记，而是帮你把学习过程变成可复盘证据。

建议每次学习时只做三件事：

1. 写下本次目标。
2. 粘贴你实际运行过的命令和关键输出位置。
3. 用自己的话解释一个系统行为。

不要把工作簿写成页面摘要。比如“今天学习了 gateway 的鉴权、路由、限流”帮助不大；更好的记录是“我去掉 Authorization 后看到 401，gateway events 里出现 auth_failed，这说明鉴权在进入下游前完成”。后者能证明你把概念、命令和证据连起来了。

如果你准备把学习过程分享给别人，这份工作簿还可以作为博客、README、issue 和演示稿的原始材料。很多公开内容不是一次写出来的，而是从这种小的证据记录里长出来的。

## 学习者信息

```text
学习者：
日期：
机器环境：
Node 版本：
Python 版本：
当前目标：
```

## 每次学习前的 3 分钟准备

```text
今天我准备推进的模块：
我预计会运行的命令：
我预计会看到的证据：
我担心会卡住的点：
今天最多学习多久：
```

提前写这几行能防止学习发散。AI Infra 内容很容易一路点链接点下去，最后忘了今天到底想解决什么问题。

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

加深记录：

```text
如果用户问“这个仓库为什么要拆成四个项目”，我会这样回答：


如果把 gateway 和 inference 合并，会失去哪些清晰边界：


如果 eval 只输出一个分数，会缺少哪些判断信息：


如果 finetune 只留下 checkpoint，会缺少哪些复现信息：

```

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

加深记录：

```text
infra-check 验证了：

infra-smoke 验证了：

我能确认项目当前具备：

我还不能确认项目具备：

如果我要给别人演示，我会先展示哪一个输出：
```

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

加深记录：

```text
我看到的 request id：

gateway 中这条请求的关键事件：

inference 中这条请求的关键事件：

metrics 中哪些计数发生了变化：

如果这次请求改成 stream=true，我预计证据会有什么变化：

如果这次请求失败，我会如何分类：
- 鉴权失败：
- 路由失败：
- 下游失败：
- streaming 中途失败：
```

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

加深记录：

```text
baseline 与 candidate 是否来自同一个 task：

backend / few-shot / sample count 是否可比：

delta 是否超过 min_delta：

sample analysis 支持或反驳了什么结论：

release recommendation 的 reasons：

我的发布判断：

我会阻止发布的条件：
```

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

加深记录：

```text
dataset summary 里最重要的字段：

dataset version：

checkpoint index 指向：

export manifest 的 lineage：

run history 说明：

export history 说明：

如果别人要复现这次训练，还缺少：
```

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

加深记录：

```text
我会如何向一个新读者介绍这个项目：

我会如何向一个工程师介绍这个项目：

我会如何说明它不是生产平台：

我会如何说明它仍然值得学习：

我最想补强的一页文档或一个功能：
```

## 学习记录评分

| 级别 | 表现 |
| --- | --- |
| 1 | 只记录读了哪些页面 |
| 2 | 记录了命令和是否成功 |
| 3 | 记录了关键输出和证据位置 |
| 4 | 能用证据解释系统行为 |
| 5 | 能把失败、判断和下一步改进写成工程复盘 |

目标不是追求一次达到 5，而是每轮学习都比上一轮更能“用证据说话”。

## 一份合格记录长什么样

下面是一份简短但合格的记录示例：

```text
今天目标：
理解 gateway 如何把一条请求代理到 inference。

我运行了：
curl -i -s http://localhost:8080/v1/chat/completions ...

我看到：
响应里有 x-request-id，x-upstream-model，x-cache。
gateway /events/requests/{request_id} 里有 request_received、upstream_attempt、request_success。
inference /events/requests/{request_id} 里有 engine_start、request_success。

我的理解：
gateway 负责入口鉴权、模型名映射和代理；inference 负责模型服务接口和生成结果。
request id 把两层证据串起来，所以排障时不应该只看最终 body。

我还不确定：
streaming 已经开始后上游失败时，客户端会收到什么 error event。

下一步：
读 Gateway 韧性 Lab，并故意制造一次失败路径。
```

这份记录不长，但它有目标、命令、证据、理解、未确认问题和下一步。它比一整页概念摘抄更能帮助你继续学习。

## 每周复盘模板

如果你按两周计划学习，每周可以做一次汇总。

```text
本周我跑通过的链路：

本周我最理解的一个概念：

本周我最有价值的一份证据：

本周我遇到的一个失败：

我是怎么定位的：

我还需要补的前置知识：

下周最重要的目标：

可以变成 issue 或 PR 的改进：
```

每周复盘的重点不是写得完整，而是找出一个可继续推进的方向。只要你能把“我哪里不懂”变成“下一步看哪个文件、跑哪条命令、补哪页文档”，学习就没有停住。
