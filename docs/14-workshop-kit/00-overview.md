# 共学与公开分享套件

这一组页面面向准备把项目分享给别人、带学习小组、做公开演示或开放贡献的人。

前面的章节已经回答了“学什么、怎么跑、怎么看输出、如何验收”。这里补上另一层：

- 怎么把一套个人学习材料组织成可复用的共学活动
- 怎么让新读者在第一次进入仓库时知道该交付什么
- 怎么让贡献者知道哪些内容值得补、补到什么程度算合格
- 怎么把 GitHub 发布从一次上传，变成持续迭代的学习项目

## 这一章解决什么问题

公开学习项目最容易卡在三个地方：

1. 页面很多，但第一次来的读者不知道该怎么走
2. 能跑通命令，但不知道怎么记录过程和复盘证据
3. 想让别人贡献内容，但没有统一的模板和验收标准

所以这一章不再继续堆 AI Infra 概念，而是把学习组织方式、带练节奏、输出模板、贡献规则和发布节奏收成一组可以直接复用的材料。

## 推荐阅读顺序

| 页面 | 适合谁 | 你会得到什么 |
| --- | --- | --- |
| [讲师与带练指南](/14-workshop-kit/01-facilitator-guide) | 想带别人学习的人 | 课前准备、节奏控制、提问方式、验收方式 |
| [学习者工作簿](/14-workshop-kit/02-learner-workbook) | 自学者和学习小组成员 | 每一阶段要记录的问题、命令、证据和复盘 |
| [学习小组议程](/14-workshop-kit/03-study-group-agenda) | 想组织共学的人 | 90 分钟、半天、两周三种活动节奏 |
| [复盘与评审模板](/14-workshop-kit/04-review-templates) | 准备公开展示的人 | 复盘包、演示稿、PR 说明、issue 记录模板 |
| [贡献者协作手册](/14-workshop-kit/05-contribution-playbook) | 准备开放贡献的人 | 新页面、新 lab、新案例、新证据的贡献标准 |
| [GitHub 发布计划](/14-workshop-kit/06-github-release-plan) | 准备上线仓库的人 | 首发前、首发后 30 天、长期维护节奏 |
| [自动生成共学包](/14-workshop-kit/07-generated-workshop-packet) | 准备直接带练的人 | 议程模板、模块卡片、学习者交付和复盘问题 |
| [自动生成测评包](/10-assessments/06-generated-assessment-pack) | 准备测评或复盘的人 | 模块题目、证据要求、rubric 和 Capstone review |
| [自动生成路线图包](/08-publication/05-generated-roadmap-pack) | 准备开放贡献的人 | GitHub issue 种子、推荐 label、验收标准和验证命令 |
| [自动生成首发运营包](/08-publication/13-generated-launch-pack) | 准备创建 release 的人 | release notes、starter issues、默认标签规范和发布后检查表 |
| [课程目录生成器](/09-reference/10-course-catalog) | 准备带练或拆班学习的人 | 7 个可分发模块、检查点和讲师提示 |

## 它和其他章节怎么配合

| 你要做的事 | 先看 | 再看 |
| --- | --- | --- |
| 带别人从零跑通 | [从 0 到 1 学习路径](/00-overview/00-zero-to-one) | [讲师与带练指南](/14-workshop-kit/01-facilitator-guide) |
| 按模块拆分共学 | [课程目录生成器](/09-reference/10-course-catalog) | [学习小组议程](/14-workshop-kit/03-study-group-agenda) |
| 生成讲师备忘和学习者任务 | [自动生成共学包](/14-workshop-kit/07-generated-workshop-packet) | [复盘与评审模板](/14-workshop-kit/04-review-templates) |
| 生成模块题目和评分标准 | [自动生成测评包](/10-assessments/06-generated-assessment-pack) | [参考答案与讲解](/10-assessments/05-answer-key) |
| 生成首批 issue 种子 | [自动生成路线图包](/08-publication/05-generated-roadmap-pack) | [GitHub 发布计划](/14-workshop-kit/06-github-release-plan) |
| 生成首发 release 运营材料 | [自动生成首发运营包](/08-publication/13-generated-launch-pack) | [v0.1 首发发布手册](/08-publication/10-v0-1-release-playbook) |
| 组织一次线上共学 | [两周学习计划](/00-overview/15-two-week-learning-plan) | [学习小组议程](/14-workshop-kit/03-study-group-agenda) |
| 让读者边跑边记录 | [第一次实操演练](/00-overview/04-first-walkthrough) | [学习者工作簿](/14-workshop-kit/02-learner-workbook) |
| 做一次公开演示 | [公开演示脚本](/13-output-gallery/06-public-demo-script) | [复盘与评审模板](/14-workshop-kit/04-review-templates) |
| 开放外部贡献 | [内容写作规范](/08-publication/02-content-style-guide) | [贡献者协作手册](/14-workshop-kit/05-contribution-playbook) |
| 正式发到 GitHub | [公开发布总览](/08-publication/00-overview) | [GitHub 发布计划](/14-workshop-kit/06-github-release-plan) |

## 共学版本的核心产物

如果你要把这个项目变成可以分享的学习站，建议至少准备这几类产物：

| 产物 | 作用 | 对应页面 |
| --- | --- | --- |
| 学习路线 | 让新读者知道顺序 | [学习路线图](/00-overview/02-learning-route) |
| 课程目录 | 让组织者按模块分发任务 | [课程目录生成器](/09-reference/10-course-catalog) |
| 共学包 | 让讲师直接拿到议程、模块卡片和交付要求 | [自动生成共学包](/14-workshop-kit/07-generated-workshop-packet) |
| 测评包 | 让讲师和 reviewer 看到题目、证据要求和评分标准 | [自动生成测评包](/10-assessments/06-generated-assessment-pack) |
| 路线图包 | 让维护者把反馈和薄弱点拆成 issue | [自动生成路线图包](/08-publication/05-generated-roadmap-pack) |
| 首发运营包 | 让维护者统一 release notes、starter issues 和发布后检查表 | [自动生成首发运营包](/08-publication/13-generated-launch-pack) |
| 实操记录 | 证明读者真的跑过 | [学习者工作簿](/14-workshop-kit/02-learner-workbook) |
| 输出证据 | 证明命令和系统行为对得上 | [示例输出与证据库](/13-output-gallery/00-overview) |
| 复盘模板 | 把零散命令变成工程故事 | [复盘与评审模板](/14-workshop-kit/04-review-templates) |
| 贡献规则 | 让后续迭代不失控 | [贡献者协作手册](/14-workshop-kit/05-contribution-playbook) |

## 什么算共学准备好了

不是页面数量越多越好，而是第一次来的读者能独立回答：

1. 我应该先读哪一页
2. 我应该跑哪几个命令
3. 跑完以后应该看到什么
4. 如果失败，我该查哪一类证据
5. 我能交付什么学习产物
6. 我想贡献时应该从哪里开始

当这六个问题都有明确入口时，项目就已经从“个人笔记”往“公开学习站”迈了一大步。

## 最小共学流程

一次最小共学可以这样安排：

1. 读 [什么是 AI Infra](/00-overview/01-what-is-ai-infra)，统一系统地图
2. 跑 [最小运行手册](/00-overview/03-runbook)，确认环境可用
3. 做 [第一次实操演练](/00-overview/04-first-walkthrough)，打通四个项目
4. 用 [示例输出与证据库](/13-output-gallery/00-overview)，对照输出证据
5. 填 [学习者工作簿](/14-workshop-kit/02-learner-workbook)，留下个人复盘
6. 生成 [自动生成共学包](/14-workshop-kit/07-generated-workshop-packet)，整理讲师备忘和交付要求
7. 生成 [自动生成测评包](/10-assessments/06-generated-assessment-pack)，准备模块题目和评分标准
8. 生成 [自动生成路线图包](/08-publication/05-generated-roadmap-pack)，筛选首批 issue 种子
9. 生成 [自动生成首发运营包](/08-publication/13-generated-launch-pack)，复核 release notes、starter issues 和发布后检查表
10. 做 [系统 Capstone 与验收 Rubric](/07-hands-on-labs/05-capstone-review-rubric)，完成一次端到端讲解

## 下一步

- 如果你要带别人学，继续看 [讲师与带练指南](/14-workshop-kit/01-facilitator-guide)
- 如果你是学习者，继续看 [学习者工作簿](/14-workshop-kit/02-learner-workbook)
- 如果你准备发到 GitHub，继续看 [GitHub 发布计划](/14-workshop-kit/06-github-release-plan)
