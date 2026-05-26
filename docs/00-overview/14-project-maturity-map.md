# 项目成熟度地图

这页回答一个很实际的问题：

> 这个仓库现在到底到什么地步了？

简短结论是：

> 它已经从零散 demo 推进到可以公开学习、可以本地运行、可以持续迭代的阶段，但还不是生产级 AI 平台。

这个判断很重要。它既避免低估项目价值，也避免把学习型实现包装成生产能力。

## 先给当前评分

按学习项目成熟度看，当前大致是：

```text
Level 1 内容可读：已达到
Level 2 本地可跑：已达到
Level 3 证据可复盘：已明显进入
Level 4 生产可用：未达到，也不是当前默认目标
```

所以对外表达时可以说：

```text
这是一个已经具备公开学习价值的 AI Infra Handbook，
包含可运行 scaffold、质量检查、证据包和共学材料；
它不是生产平台，但可以作为理解生产 AI Infra 的学习底座。
```

## 当前阶段判断

| 维度 | 当前状态 | 可以怎么使用 |
| --- | --- | --- |
| 学习站 | 已经可用 | 适合作为公开课程入口、个人学习路线、分享材料 |
| 四项目代码 | 已形成最小闭环 | 适合读代码、跑命令、做 lab、观察系统行为 |
| 联调验证 | 已覆盖 smoke | 适合每轮改动后确认主链路没有断 |
| 观测与产物 | 已有结构化事件、索引和 manifest | 适合学习 request lifecycle、eval history、训练资产化 |
| 输出证据 | 已有示例输出与证据库 | 适合读者跑完命令后判断结果、整理复盘和做公开演示 |
| 共学组织 | 已有带练指南、工作簿、议程、评审模板、发布计划和自动生成包 | 适合组织学习小组、公开分享、模块测评和开放贡献 |
| 发布准备 | 已有 GitHub Pages、CI、协作模板和 checklist | 适合上传 GitHub 后继续收反馈 |
| 生产能力 | 仍是学习型实现 | 不适合直接作为生产网关、训练平台或评测平台上线 |

## 成熟度分层

可以把当前项目分成四个成熟度层级。

### Level 1：内容可读

这一层要求：

- 读者知道项目是什么
- 文档能解释核心概念
- 页面之间有导航
- README 能提供起点

当前项目已经达到，并且正在继续把核心页从提纲扩写成教程。

### Level 2：本地可跑

这一层要求：

- 有可运行项目
- 有 runbook
- 有 tests
- 有 smoke
- 有示例输出

当前项目已经达到。四个项目能通过本地检查形成最小闭环。

### Level 3：证据可复盘

这一层要求：

- 请求有 request id、events、timeline
- eval 有 run、compare、history、leaderboard
- finetune 有 dataset、checkpoint、export lineage
- 公开发布有 public-check、Actions、Pages

当前项目已经较明显进入这一层。

### Level 4：生产可用

这一层要求：

- 真实 serving backend
- 生产级 gateway 策略
- 外部 observability backend
- 真实 judge / dashboard
- 真实训练与 artifact store
- 多租户、权限、成本、SLO、回滚

当前项目还没有达到，也不应该假装已经达到。

## 从 Level 3 到 Level 4 差什么

差距主要不是“再多写几页”，而是这些系统能力：

| 方向 | 当前学习实现 | 生产化需要 |
| --- | --- | --- |
| Serving | mock/adapter 边界 | 真实 runtime、容量、SLO、回滚 |
| Gateway | 最小治理逻辑 | 多租户、配额、策略、审计 |
| Observability | 本地 events/metrics | tracing/log backend、告警、dashboard |
| Evaluation | run/compare 骨架 | 真实 judge、人工复核、线上反馈闭环 |
| Finetune | mock 资产链 | 真实训练、artifact store、模型 registry |
| Security | public-check | 完整 secret 管理、权限、合规流程 |

这些方向可以逐步迁移，但不应该一次塞进默认学习路径。

## 已经具备的能力

### 文档站主干已经成型

现在文档不是散页，而是围绕几条主线组织：

- 总览与学习路线
- LLM 基础概念
- 推理服务
- AI Gateway 平台层
- 评测与可观测性
- 微调训练
- 四个可运行项目
- hands-on labs
- 示例输出与证据库
- 共学与公开分享套件
- 学习自测
- 发布与参考资料

这意味着它已经可以作为学习网站使用，而不只是仓库 README 的附属说明。

### 四个项目已经能串成系统

当前系统分成四层：

| 层 | 项目 | 主要回答的问题 |
| --- | --- | --- |
| 执行层 | `inference-service` | 请求如何进入模型服务、如何响应、如何暴露 metrics/events |
| 治理层 | `ai-gateway` | 请求如何鉴权、路由、限流、fallback、追踪失败 |
| 质量层 | `eval-module` | 结果如何被记录、比较、聚合和转化为发布判断 |
| 训练层 | `finetune-demo` | 训练如何留下可复现资产、checkpoint、export lineage |

这四层不是为了模拟完整生产系统，而是为了让学习者看见 AI Infra 的主干边界。

### 验证闭环已经比较完整

当前有多类验证：

```bash
PYTHON=.venv/bin/python make docs-quality
PYTHON=.venv/bin/python make public-check
PYTHON=.venv/bin/python make infra-format
PYTHON=.venv/bin/python make infra-test
PYTHON=.venv/bin/python make infra-check
PYTHON=.venv/bin/python make infra-smoke
PYTHON=.venv/bin/python make infra-evidence
PYTHON=.venv/bin/python make release-brief
PYTHON=.venv/bin/python make workshop-packet
PYTHON=.venv/bin/python make assessment-pack
PYTHON=.venv/bin/python make roadmap-pack
PYTHON=.venv/bin/python make launch-pack
```

这让项目可以继续大步迭代，而不是每次都靠人工感觉判断有没有改坏。

### 证据闭环已经形成

项目已经有：

- HTTP headers
- metrics
- events
- request timeline
- run history
- comparison index
- leaderboard
- dataset registry
- checkpoint index
- export manifest
- evidence packet

这些证据让读者可以从“命令成功了”继续追问：

- 成功路径留下了什么证据？
- 失败路径如何被记录？
- 一次 run 能否被复盘？
- 一个 export 能否追溯回训练和数据？

## 还没有做到什么

为了保持学习可读性，当前仍然刻意保留了一些边界：

- inference-service 默认仍是 mock/学习型 engine
- gateway 没有接入完整生产级策略引擎、分布式限流或外部 tracing backend
- eval-module 还没有真实 judge adapter 和完整 dashboard
- finetune-demo 还没有执行真实 GPU 训练、resume 策略和多 checkpoint 选择
- 文档中还可以继续增加更多真实接入迁移说明、案例和示例输出

这些不是缺陷清单，而是下一阶段的成长方向。

## 适合现在怎么用

### 如果你是第一次学习

1. 看 [课程大纲](/00-overview/12-course-syllabus)。
2. 按 [两周学习计划](/00-overview/15-two-week-learning-plan) 推进。
3. 跑 [第一次实操演练](/00-overview/04-first-walkthrough)。
4. 做至少两个 [hands-on labs](/07-hands-on-labs/00-overview)。
5. 对照 [示例输出与证据库](/13-output-gallery/00-overview) 看懂输出证据。
6. 用 [学习者工作簿](/14-workshop-kit/02-learner-workbook) 记录命令、证据和卡点。
7. 用 [学习自测](/10-assessments/00-overview) 检查自己是否真的理解。

### 如果你准备公开分享

1. 看 [面向分享的学习方式](/00-overview/11-public-learning-guide)。
2. 看 [共学与公开分享套件](/14-workshop-kit/00-overview)。
3. 做 [系统 Capstone 与验收 Rubric](/07-hands-on-labs/05-capstone-review-rubric)。
4. 做 [公开发布验收 Lab](/07-hands-on-labs/06-public-release-readiness-lab)。
5. 整理 [端到端复盘证据包](/13-output-gallery/04-end-to-end-review-packet)。
6. 生成 [自动生成共学包](/14-workshop-kit/07-generated-workshop-packet)。
7. 生成 [自动生成测评包](/10-assessments/06-generated-assessment-pack)。
8. 生成 [自动生成路线图包](/08-publication/05-generated-roadmap-pack)。
9. 生成 [自动生成首发运营包](/08-publication/13-generated-launch-pack)。
10. 对照 [GitHub 发布计划](/14-workshop-kit/06-github-release-plan) 做首发前检查。

### 如果你准备继续开发

先不要四层同时改。

建议选择一条线：

- serving 后端迁移
- gateway 策略加固
- eval judge/dashboard
- finetune 真实训练
- docs / evidence / workshop 体验

每条线都要写清：

- 改动边界
- 新增证据
- 新增测试
- 文档更新
- 验证命令

## 成熟度自检

你可以用下面问题判断项目是否继续变稳：

```text
新读者能否 10 分钟找到起点？
本地是否还能跑 public-check？
核心 pages 是否不是空提纲？
每个项目是否有明确的正常路径和失败路径？
新增输出是否进入证据库？
新增行为是否有测试？
公开仓库是否没有敏感信息？
GitHub Pages 是否仍然 200？
```

如果这些问题越来越容易回答，项目成熟度就在提升。

## 怎么判断下一步优先级

每次继续推进时，可以按这个顺序选：

1. 读者是否还会卡在入口。
2. 核心章节是否还像提纲。
3. 命令跑完后是否知道看什么证据。
4. 失败后是否知道查哪一层。
5. 公开发布后是否能接住反馈。
6. 是否有一条真实迁移路线能解释边界。

当前阶段最值得继续做的，仍然是内容深度、证据解释、lab 可执行性和公开协作入口。

## 一句话结论

当前项目已经到了可以公开作为学习网站使用的阶段。

下一阶段的重点不是再堆页面，而是继续提升深度：更多真实接入、更清晰的失败案例、更完整的示例输出，以及更强的项目级复盘和共学反馈闭环。
