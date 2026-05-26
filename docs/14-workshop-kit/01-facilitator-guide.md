# 讲师与带练指南

这页给准备带别人学习这套项目的人用。

你不需要把每个细节都讲成课件。更好的方式是带读者建立三个能力：

1. 能看懂 AI Infra 的系统分层
2. 能把命令输出和系统行为对应起来
3. 能用证据说明一次请求、一次评测或一次训练产物发生了什么

带练这类工程项目时，最重要的不是把讲师变成“答案提供者”，而是把活动设计成“共同观察系统”。读者第一次接触 AI Infra 时，很容易被名词压住：KV Cache、Gateway、Rate Limit、Evaluation、LoRA、Manifest，每个词都像一个新坑。如果讲师只是一口气解释概念，听众短时间内会觉得很充实，但很难形成可复用能力。

更好的带练方式是围绕证据组织节奏：先让大家看到一条请求、一次失败、一次评测、一次训练产物，再回到概念解释为什么系统要这样设计。这样参与者不是被动听课，而是在学习“遇到一个 AI Infra 问题时，应该怎么定位、怎么验证、怎么表达结论”。

## 一次带练应该交付什么

一次好的带练结束后，最好不要只留下“大家听过一遍”的印象，而要留下可复用的学习资产。

至少包括：

- 一份参与者能继续使用的学习路径。
- 一组成功运行过的命令。
- 一条请求链路的证据。
- 一个评测或训练产物的复盘。
- 一份活动后的卡点清单。
- 一组可以变成 issue 的后续改进项。

如果你准备长期运营这个项目，这些资产会比单次讲解更重要。它们会慢慢变成 FAQ、案例、Lab、issue、release notes 和贡献者任务。

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

### 讲师自己要提前跑过什么

带练前建议讲师至少跑过这些命令，并保存关键输出：

```bash
PYTHON=.venv/bin/python make infra-check
PYTHON=.venv/bin/python make infra-smoke
PYTHON=.venv/bin/python make docs-quality
```

如果是公开分享或录制视频，再额外跑：

```bash
PYTHON=.venv/bin/python make public-check
npm run docs:build
```

这些命令不是为了展示“我机器上没问题”，而是为了建立讲师自己的信心：如果现场有人卡住，你知道正常输出大概长什么样，也知道应该去哪个文档页或哪个证据文件对照。

### 活动前发给参与者的说明

可以直接复制下面这段：

```text
这次活动不是普通概念讲座，而是一次 AI Infra 学习型项目带练。

请提前准备：
1. 安装 Node 22 和 Python 环境。
2. 克隆仓库并执行 infra-dev-install。
3. 如果不能本地运行，也可以只跟着观察讲师输出。

活动中我们会关注：
- 一条请求如何经过 gateway 和 inference。
- request id、events、metrics 如何帮助排障。
- eval compare 如何支持发布判断。
- finetune manifest 如何支持训练产物复现。

活动结束后请提交：
- 一条你能解释的证据。
- 一个你仍然模糊的问题。
- 一个你希望文档继续补充的点。
```

## 带练时的主线

推荐按这条线讲：

1. 系统地图：四个项目分别站在哪一层
2. 请求链路：用户请求如何穿过 gateway 到 inference
3. 观测证据：request id、headers、events、metrics 分别说明什么
4. 评测闭环：run、comparison、leaderboard 如何支持发布判断
5. 训练资产：manifest、checkpoint、export lineage 为什么重要
6. 复盘表达：如何把一次操作讲成工程故事

这条线的优点是不会把读者淹没在工具名里。读者先看到系统行为，再回头理解 vLLM、SGLang、eval、finetune 这些概念会容易很多。

## 90 分钟示例脚本

如果你只有 90 分钟，可以按下面节奏执行。

| 时间 | 环节 | 讲师动作 | 参与者动作 |
| --- | --- | --- | --- |
| 0-10 分钟 | 项目定位 | 说明这是学习型 AI Infra 手册，不是生产平台 | 写下自己最想理解的问题 |
| 10-20 分钟 | 系统地图 | 展示四个项目如何分层 | 画出自己的四层图 |
| 20-35 分钟 | 请求链路 | 演示 gateway 到 inference 的请求 | 记录 request id 和响应 header |
| 35-50 分钟 | 失败路径 | 演示 401 / 404 / 502 或 fallback | 判断失败属于哪一层 |
| 50-65 分钟 | Eval 判断 | 展示 run、compare、recommendation | 写下为什么不是只看分数 |
| 65-78 分钟 | Finetune 资产 | 展示 manifest、checkpoint、export lineage | 找出 dataset version 和 export manifest |
| 78-88 分钟 | 复盘 | 用模板写一段端到端说明 | 提交一个证据和一个问题 |
| 88-90 分钟 | 收尾 | 指向下一步页面和 issue | 选择后续学习任务 |

如果现场环境不可控，可以把本地运行压缩成演示，把更多时间给证据解释和复盘。比起让所有人现场装通，更重要的是让大家理解“跑通以后应该看什么”。

## 半天工作坊示例脚本

半天活动可以让参与者真正动手。

| 环节 | 建议时长 | 产出 |
| --- | --- | --- |
| 开场与系统地图 | 30 分钟 | 每人一张四层图 |
| 环境确认 | 30 分钟 | `infra-check` 结果 |
| 第一次实操 | 45 分钟 | gateway/inference 请求证据 |
| Gateway 韧性练习 | 45 分钟 | 失败路径复盘 |
| Eval 发布判断 | 45 分钟 | compare 报告说明 |
| Finetune 产物追踪 | 45 分钟 | manifest lineage 说明 |
| 小组复盘 | 30 分钟 | 每组一份证据驱动总结 |
| 后续 issue 拆解 | 15 分钟 | 3 到 5 个改进任务 |

半天工作坊要控制一个风险：参与者一旦遇到环境问题，很容易把全部时间都用在安装上。建议准备一份“观察模式”备用方案：无法本地运行的人仍然可以用讲师输出填写工作簿和复盘模板。

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

## 如何判断现场节奏是否健康

带练过程中可以观察几个信号：

| 信号 | 可能说明 | 调整方式 |
| --- | --- | --- |
| 大家只在复制命令 | 还没有理解命令验证什么 | 停下来对照输出证据 |
| 大家只问工具名 | 系统地图还不稳 | 回到四层结构 |
| 大家只问报错 | 环境问题压过学习目标 | 切换到观察模式 |
| 大家能主动提 request id、events、manifest | 证据意识开始形成 | 进入案例复盘 |
| 大家开始讨论生产差距 | 已经理解学习型边界 | 指向生产迁移章节 |

讲师不需要把所有问题当场解决。更好的方式是把问题分类：现场必须解决、可以课后补文档、适合变成 GitHub issue、适合留到下一次工作坊。

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

## 带练后的产物整理

活动结束后，建议讲师做一次 30 分钟整理，把现场素材变成仓库资产。

可以按下面清单做：

- 把重复出现的问题写进 FAQ 或 troubleshooting。
- 把一个典型失败路径写成 case study。
- 把讲解中临时画的系统图整理进 overview。
- 把参与者提出的好问题转成 issue。
- 把活动中最有代表性的证据补到 output gallery。
- 把无法现场解决的环境问题标成 follow-up。

这样项目会越带越厚，而不是每次活动都从零讲起。

## 带练后的跟进

活动结束后，不要只收“有没有跑通”。建议收三类反馈：

| 反馈 | 示例问题 | 用来改进什么 |
| --- | --- | --- |
| 卡点 | 哪一步最难判断对错？ | 改 [常见排障手册](/09-reference/04-troubleshooting) |
| 证据 | 哪个输出最能帮助你理解系统？ | 改 [示例输出与证据库](/13-output-gallery/00-overview) |
| 讲解 | 哪个概念听完仍然模糊？ | 改 [FAQ](/00-overview/10-faq) 或模块 overview |

这些反馈比泛泛的“文档是否清楚”更有用，因为它们能直接变成下一批 issue 或 PR。
