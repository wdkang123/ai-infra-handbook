# 讲师与带练指南

这页给准备带别人学习这套项目的人用。

你不需要把每个细节都讲成课件。更好的方式是带读者建立三个能力：

1. 能看懂 AI Infra 的系统分层
2. 能把命令输出和系统行为对应起来
3. 能用证据说明一次请求、一次评测或一次训练产物发生了什么

## 带练前要准备什么

| 准备项 | 为什么重要 | 推荐入口 |
| --- | --- | --- |
| 环境检查 | 避免活动时间消耗在安装问题上 | [最小运行手册](/00-overview/03-runbook) |
| 系统地图 | 让读者先知道四个项目为什么分开 | [四个项目怎么连成系统](/06-projects/06-end-to-end-system-map) |
| 输出证据 | 让读者知道跑完命令后要看什么 | [示例输出与证据库](/13-output-gallery/00-overview) |
| 实操任务 | 让学习不是只听讲 | [深度实战总览](/07-hands-on-labs/00-overview) |
| 自测入口 | 让每个人能判断自己是否掌握 | [学习自测总览](/10-assessments/00-overview) |

建议在活动前发给参与者：

```text
请提前完成：
1. nvm use 22
2. npm install
3. PYTHON=.venv/bin/python make infra-dev-install
4. PYTHON=.venv/bin/python make infra-check
```

如果参与者不能提前安装，也可以把活动定位成“观察和讲解”，让他们先跟着看输出证据，课后再补本地运行。

## 带练时的主线

推荐按这条线讲：

1. 系统地图：四个项目分别站在哪一层
2. 请求链路：用户请求如何穿过 gateway 到 inference
3. 观测证据：request id、headers、events、metrics 分别说明什么
4. 评测闭环：run、comparison、leaderboard 如何支持发布判断
5. 训练资产：manifest、checkpoint、export lineage 为什么重要
6. 复盘表达：如何把一次操作讲成工程故事

这条线的优点是不会把读者淹没在工具名里。读者先看到系统行为，再回头理解 vLLM、SGLang、eval、finetune 这些概念会容易很多。

## 每一段怎么提问

### 系统地图

可以问：

- 如果没有 gateway，平台层会缺什么能力？
- inference-service 为什么不应该处理所有鉴权和限流？
- eval-module 为什么不应该只输出一个分数？
- finetune-demo 为什么要留下 manifest 和 history？

不要急着给结论。先让读者画出自己的四层图，再对照 [系统地图自测](/10-assessments/01-system-map-check)。

### 请求链路

可以问：

- 一个 `x-request-id` 应该出现在几个地方？
- 如果 gateway fallback 了，客户端应该看到什么 header？
- 如果 streaming 已经开始后上游失败，为什么不能简单改成普通 `502`？
- metrics 和 events 分别更适合回答什么问题？

配套页面：

- [Serving 与 Gateway 输出证据](/13-output-gallery/01-serving-gateway-evidence)
- [Gateway 韧性 Lab](/07-hands-on-labs/02-gateway-resilience-lab)

### 评测闭环

可以问：

- 为什么一个 eval run 需要保存 sample outputs？
- comparison 的 release recommendation 为什么比单次分数更适合做发布门禁？
- leaderboard 为什么要支持 backend、few-shot、task summary？
- 什么情况下 benchmark 结果不能直接代表生产质量？

配套页面：

- [Eval 报告证据](/13-output-gallery/02-eval-report-evidence)
- [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)

### 训练资产

可以问：

- checkpoint 和 export manifest 分别面向谁？
- dataset version 和 role stats 能降低什么风险？
- 如果 export lineage 断了，后续 eval 会遇到什么问题？
- 为什么训练结果要能被复现，而不是只看“跑完了”？

配套页面：

- [Finetune 产物证据](/13-output-gallery/03-finetune-artifact-evidence)
- [Finetune 复现资产 Lab](/07-hands-on-labs/04-finetune-reproducibility-lab)

## 时间控制建议

| 环节 | 90 分钟 | 半天 | 两周共学 |
| --- | --- | --- | --- |
| 系统总览 | 15 分钟 | 30 分钟 | 第 1 天 |
| 本地运行 | 20 分钟 | 45 分钟 | 第 2 到 3 天 |
| Serving/Gateway | 20 分钟 | 60 分钟 | 第 4 到 6 天 |
| Eval/Finetune | 20 分钟 | 75 分钟 | 第 7 到 10 天 |
| 证据复盘 | 10 分钟 | 45 分钟 | 第 11 到 12 天 |
| 答辩与反馈 | 5 分钟 | 45 分钟 | 第 13 到 14 天 |

如果时间很短，不要试图讲完所有页面。优先保证读者能跑通一条请求，并知道如何查证据。

## 常见带练风险

| 风险 | 表现 | 处理方式 |
| --- | --- | --- |
| 一上来讲太多概念 | 读者能听懂名词，但不知道怎么操作 | 回到 [第一次实操演练](/00-overview/04-first-walkthrough) |
| 只跑命令不看证据 | 命令绿了，但不知道系统行为 | 引导读 [示例输出与证据库](/13-output-gallery/00-overview) |
| 把 mock 当生产系统 | 误以为当前项目已经生产可用 | 引导读 [生产迁移路线总览](/12-production-migration/00-overview) |
| 讨论过早发散 | 话题跳到 GPU、Kubernetes、真实模型 | 先完成 [系统 Capstone 与验收 Rubric](/07-hands-on-labs/05-capstone-review-rubric) |

## 带练验收标准

一次带练结束时，参与者至少应该能完成：

1. 用自己的话解释四个项目的边界
2. 跑通一次 gateway 到 inference 的请求
3. 找到一次请求的 header、events、metrics
4. 解释一次 eval comparison 的发布建议
5. 解释一次 finetune export manifest 的来源
6. 用一页复盘说明自己看到了哪些证据

如果只能做到前三项，这次活动仍然有效。后面三项可以放到下一次。

## 带练后的跟进

活动结束后，不要只收“有没有跑通”。建议收三类反馈：

| 反馈 | 示例问题 | 用来改进什么 |
| --- | --- | --- |
| 卡点 | 哪一步最难判断对错？ | 改 [常见排障手册](/09-reference/04-troubleshooting) |
| 证据 | 哪个输出最能帮助你理解系统？ | 改 [示例输出与证据库](/13-output-gallery/00-overview) |
| 讲解 | 哪个概念听完仍然模糊？ | 改 [FAQ](/00-overview/10-faq) 或模块 overview |

这些反馈比泛泛的“文档是否清楚”更有用，因为它们能直接变成下一批 issue 或 PR。
