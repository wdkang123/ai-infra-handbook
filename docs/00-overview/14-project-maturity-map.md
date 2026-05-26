# 项目成熟度地图

这页回答一个很实际的问题：

> 这个仓库现在到底到什么地步了？

简单说：它已经从“零散 demo”推进到“可以公开学习、可以本地运行、可以持续迭代”的阶段，但还不是生产级 AI 平台。

## 当前阶段判断

| 维度 | 当前状态 | 可以怎么使用 |
| --- | --- | --- |
| 学习站 | 已经可用 | 适合作为公开课程入口、个人学习路线、分享材料 |
| 四项目代码 | 已形成最小闭环 | 适合读代码、跑命令、做 lab、观察系统行为 |
| 联调验证 | 已覆盖 smoke | 适合每轮改动后确认主链路没有断 |
| 观测与产物 | 已有结构化事件、索引和 manifest | 适合学习 request lifecycle、eval history、训练资产化 |
| 输出证据 | 已有示例输出与证据库 | 适合读者跑完命令后判断结果、整理复盘和做公开演示 |
| 共学组织 | 已有带练指南、学习者工作簿、议程、评审模板、发布计划、自动共学包和自动测评包 | 适合组织学习小组、公开分享、模块测评和开放贡献 |
| 发布准备 | 已有 GitHub Pages、CI、协作模板和 checklist | 适合上传 GitHub 后继续收反馈 |
| 生产能力 | 仍是学习型实现 | 不适合直接作为生产网关、训练平台或评测平台上线 |

## 已经具备的能力

### 1. 文档站主干已经成型

现在文档不是散页，而是围绕几条主线组织：

- 总览与学习路线
- LLM 基础概念
- 推理服务
- AI gateway 平台层
- 评测与可观测性
- 微调训练
- 四个可运行项目
- hands-on labs
- 示例输出与证据库
- 共学与公开分享套件
- 学习自测
- 发布与参考资料

这意味着它已经可以作为“学习网站”使用，而不只是仓库 README 的附属说明。

### 2. 四个项目已经能串成系统

当前系统分成四层：

| 层 | 项目 | 主要回答的问题 |
| --- | --- | --- |
| 执行层 | `inference-service` | 请求如何进入模型服务、如何响应、如何暴露 metrics/events |
| 治理层 | `ai-gateway` | 请求如何鉴权、路由、限流、fallback、追踪失败 |
| 质量层 | `eval-module` | 结果如何被记录、比较、聚合和转化为发布判断 |
| 训练层 | `finetune-demo` | 训练如何留下可复现资产、checkpoint、export lineage |

这四层不是为了模拟完整生产系统，而是为了让学习者能看见 AI Infra 的主干边界。

### 3. 验证闭环已经比较完整

当前有四类验证：

```bash
PYTHON=.venv/bin/python make infra-format
PYTHON=.venv/bin/python make docs-inventory
PYTHON=.venv/bin/python make course-catalog
PYTHON=.venv/bin/python make infra-test
PYTHON=.venv/bin/python make infra-check
PYTHON=.venv/bin/python make infra-smoke
PYTHON=.venv/bin/python make release-brief
PYTHON=.venv/bin/python make workshop-packet
PYTHON=.venv/bin/python make assessment-pack
PYTHON=.venv/bin/python make roadmap-pack
PYTHON=.venv/bin/python make launch-pack
```

其中：

- `infra-format` 检查格式与 lint
- `docs-inventory` 生成学习站章节、页面和课程主线清单
- `course-catalog` 把课程主线整理成可带练模块、检查点和讲师提示
- `infra-test` 跑四个项目的单元测试
- `infra-check` 同时覆盖 lint、测试和文档构建
- `infra-smoke` 打通 gateway、inference、eval、finetune 的端到端学习链路
- `release-brief` 把课程结构和运行证据合成发布前摘要
- `workshop-packet` 把课程目录和发布摘要合成共学议程、模块卡片、学习者交付和复盘问题
- `assessment-pack` 把课程目录和共学包合成模块题目、证据要求、rubric 和 Capstone review
- `roadmap-pack` 把发布摘要和测评包合成 GitHub issue 种子、推荐 label 和验收命令
- `launch-pack` 把发布摘要和路线图包合成 release notes、starter issues、默认标签和发布后检查表

这让项目可以继续大步迭代，而不是每次都靠人工感觉判断有没有改坏。

## 最近一轮增强了什么

最近几轮主要把“可观测、可复盘、可教学”补厚了：

- inference/gateway 有结构化事件、事件摘要、request timeline 和 request index
- gateway 增加 `/events/failures`，可以按状态码、失败事件、upstream 聚合失败
- eval 增加 run index、comparison index、leaderboard、sample summary、sample analysis
- finetune 增加 dataset registry、dataset diff、export index、run index、checkpoint index
- 文档新增示例输出与证据库，把 header、events、JSON report、manifest 和失败症状整理成可复盘材料
- 文档新增共学与公开分享套件，把带练、工作簿、议程、评审模板、贡献协作和 GitHub 首发计划整理成可复用材料
- smoke 覆盖更多 header、metrics、错误路径、索引文件和产物字段

这些能力让读者可以从“命令成功了”继续追问：

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
- 文档中还可以继续增加示例输出、截图和真实接入迁移说明

这些不是缺陷清单，而是下一阶段的成长方向。

## 适合现在怎么用

如果你是第一次学习：

1. 看 [课程大纲](/00-overview/12-course-syllabus)
2. 按 [两周学习计划](/00-overview/15-two-week-learning-plan) 推进
3. 跑 [第一次实操演练](/00-overview/04-first-walkthrough)
4. 做至少两个 [hands-on labs](/07-hands-on-labs/00-overview)
5. 对照 [示例输出与证据库](/13-output-gallery/00-overview) 看懂输出证据
6. 用 [学习者工作簿](/14-workshop-kit/02-learner-workbook) 记录命令、证据和卡点
7. 用 [学习自测](/10-assessments/00-overview) 检查自己是否真的理解

如果你准备公开分享：

1. 看 [面向分享的学习方式](/00-overview/11-public-learning-guide)
2. 看 [共学与公开分享套件](/14-workshop-kit/00-overview)
3. 做 [系统 Capstone 与验收 Rubric](/07-hands-on-labs/05-capstone-review-rubric)
4. 做 [公开发布验收 Lab](/07-hands-on-labs/06-public-release-readiness-lab)
5. 整理 [端到端复盘证据包](/13-output-gallery/04-end-to-end-review-packet)
6. 生成 [自动生成共学包](/14-workshop-kit/07-generated-workshop-packet)
7. 生成 [自动生成测评包](/10-assessments/06-generated-assessment-pack)
8. 生成 [自动生成路线图包](/08-publication/05-generated-roadmap-pack)
9. 生成 [自动生成首发运营包](/08-publication/13-generated-launch-pack)
10. 对照 [GitHub 发布计划](/14-workshop-kit/06-github-release-plan) 做首发前检查

## 一句话结论

当前项目已经到了“可以公开作为学习网站使用”的阶段。  
下一阶段的重点不是再堆页面，而是继续提升深度：更多真实接入、更清晰的失败案例、更完整的示例输出，以及更强的项目级复盘和共学反馈闭环。
