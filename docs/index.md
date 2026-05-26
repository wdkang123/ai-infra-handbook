---
layout: home

hero:
  name: "AI Infra Handbook"
  text: "一套能边学边跑的 AI Infra 学习站"
  tagline: "把概念、命令、服务状态页和最小可运行代码收成同一个入口。"
  actions:
    - theme: brand
      text: 从这里开始
      link: /00-overview/00-zero-to-one
    - theme: alt
      text: 进入学习路线
      link: /00-overview/02-learning-route
    - theme: alt
      text: 进入深度实战
      link: /07-hands-on-labs/00-overview
    - theme: alt
      text: 看案例复盘
      link: /11-case-studies/00-overview
    - theme: alt
      text: 看示例输出
      link: /13-output-gallery/00-overview
    - theme: alt
      text: 共学套件
      link: /14-workshop-kit/00-overview
    - theme: alt
      text: 看生产迁移
      link: /12-production-migration/00-overview
    - theme: alt
      text: 学习自测
      link: /10-assessments/00-overview

features:
  - title: 学习路径清楚
    details: 先看总论、再跑运行手册、再做第一次实操，不需要你自己在仓库里找顺序。
  - title: 四个项目能联动
    details: inference-service、ai-gateway、eval-module、finetune-demo 已有最小闭环。
  - title: 一边读一边跑
    details: 文档里保留了最重要的命令、浏览器地址和你应该观察到的结果。
  - title: 有实战验收
    details: 深度实战 lab 和学习自测会把概念、代码、命令、产物和验收标准串成可验证的任务。
  - title: 有工程案例
    details: 请求失败、模型发布、训练复现三个案例会把多项目能力串成可复盘的系统故事。
  - title: 有输出证据
    details: 示例输出与证据库会说明跑完命令后该看哪些 header、events、JSON 和 manifest。
  - title: 有共学套件
    details: 讲师指南、学习者工作簿、议程、评审模板和 GitHub 发布计划能支撑公开分享。
  - title: 有迁移路线
    details: 生产迁移章节会说明如何保留接口和观测，再逐步替换真实后端、策略、评测和训练。
---

<HomeLaunchPads />

<HomeGithubPanel />

<HomeCourseMatrix />

<HomeEvidenceFlow />

<HomePathExplorer />

<HomeSystemMap />

## 这个网站到底是什么

这个网站不是单纯的 AI Infra 概念笔记，也不是只放几个 demo 项目的代码说明。它更适合被理解成一套“学习型工程手册”：读者可以从系统分层开始，顺着最小可运行代码跑一遍，再用输出证据和案例复盘把理解落到实处。

这里刻意把文档、代码、验证命令、输出产物和公开协作流程放在同一个仓库里。原因很简单：AI Infra 的学习难点不只是概念多，而是概念经常和工程证据断开。很多人能说出 serving、gateway、eval、finetune，却不一定能回答：

- 一条请求失败时，先看 gateway 还是 inference？
- 一个模型分数提升时，为什么还不能直接发布？
- 一个训练 checkpoint 生成后，怎么证明它来自哪份数据？
- 一个项目准备公开时，怎么确认没有密钥、本机路径或个人痕迹？

这个网站希望训练的就是这些判断力。每一章都尽量把“概念是什么”继续推进到“怎么观察、怎么验证、怎么复盘、怎么继续扩展”。

## 三种读者怎么打开它

如果你是第一次系统学 AI Infra，不建议先从工具名开始。先走 [从 0 到 1 学习路径](/00-overview/00-zero-to-one)，把系统地图和最小运行链路跑通，再回头补 vLLM、SGLang、Triton、Eval、LoRA 这些专题。

如果你已经有后端或平台经验，建议直接从 [文档与代码怎么对应](/00-overview/05-docs-to-code-map) 和 [项目学习总览](/06-projects/00-projects-overview) 开始。重点不是看代码写得多复杂，而是看这个仓库如何把接口、事件、metrics、history、manifest 这些工程边界保留下来。

如果你准备把它分享给别人，建议先读 [面向分享的学习方式](/00-overview/11-public-learning-guide)、[共学与公开分享套件](/14-workshop-kit/00-overview) 和 [公开发布总览](/08-publication/00-overview)。这条路线会更关注读者体验、证据包、issue、release notes 和维护节奏。

## 你应该怎样判断自己读懂了

不要用“我看了多少页面”判断进度。这个网站更推荐用证据判断学习进展。

一个比较可靠的标准是：

| 你能做到 | 说明你已经掌握了什么 |
| --- | --- |
| 画出四个项目的系统分层 | 你知道这不是四个孤立 demo |
| 跑通 gateway 到 inference 的请求 | 你理解最小请求链路 |
| 用 request id 找到 events timeline | 你开始有可观测性意识 |
| 解释一次 eval compare 的 release recommendation | 你理解质量判断不是单次分数 |
| 追溯一次 export manifest 到 dataset version | 你理解训练资产和复现 |
| 写出一次端到端复盘 | 你能把零散操作讲成工程故事 |

如果你能稳定做到这些，再继续看生产迁移章节、真实 serving 框架或更复杂的评测体系，就不会只是在堆名词。

## 现在最适合的打开方式

1. 先看 [从 0 到 1 学习路径](/00-overview/00-zero-to-one)
2. 再看 [什么是 AI Infra](/00-overview/01-what-is-ai-infra)
3. 接着看 [学习路线图](/00-overview/02-learning-route)
4. 如果你想按课程推进，看 [课程大纲](/00-overview/12-course-syllabus)
5. 如果你想知道当前项目已经到什么阶段，看 [项目成熟度地图](/00-overview/14-project-maturity-map)
6. 如果你想安排学习节奏，看 [两周学习计划](/00-overview/15-two-week-learning-plan)
7. 然后看 [最小运行手册](/00-overview/03-runbook)
8. 接着进入 [第一次实操演练](/00-overview/04-first-walkthrough)
9. 如果你已经跑通一轮，再看 [第一次跑完之后学什么](/00-overview/06-after-first-walkthrough)
10. 如果你想继续深入，进入 [深度实战总览](/07-hands-on-labs/00-overview)
11. 如果你想看完整工程故事，读 [案例复盘总览](/11-case-studies/00-overview)
12. 如果你想知道输出证据怎么看，读 [示例输出与证据库](/13-output-gallery/00-overview)
13. 如果你准备带别人学习或发到 GitHub，读 [共学与公开分享套件](/14-workshop-kit/00-overview)
14. 如果你想知道怎么继续变真实，看 [生产迁移路线总览](/12-production-migration/00-overview)
15. 如果你想检验自己是否真的理解，做 [学习自测](/10-assessments/00-overview)
16. 如果你需要查命令、查产物、排障，看 [参考资料总览](/09-reference/00-overview)
17. 如果你想检查自己学到哪了，看 [学习检查点](/00-overview/09-learning-checkpoints)

## 如果你已经知道自己更想学什么

- 更想理解请求怎么变成结果：看 [推理服务](/02-inference-serving/00-overview)
- 更想理解平台治理：看 [AI Gateway Platform](/03-ai-gateway-platform/00-overview)
- 更想理解评测与发布判断：看 [Evaluation Observability](/04-evaluation-observability/00-overview)
- 更想理解训练与微调：看 [Finetuning Training](/05-finetuning-training/00-overview)
- 更想按任务练习：看 [深度实战总览](/07-hands-on-labs/00-overview)
- 更想看工程复盘：看 [案例复盘总览](/11-case-studies/00-overview)
- 更想知道输出证据怎么看：看 [示例输出与证据库](/13-output-gallery/00-overview)
- 更想带别人学习或做公开分享：看 [共学与公开分享套件](/14-workshop-kit/00-overview)
- 更想规划真实迁移：看 [生产迁移路线总览](/12-production-migration/00-overview)
- 想检验自己是否真的掌握：看 [学习自测总览](/10-assessments/00-overview)
- 想快速查命令：看 [命令速查](/09-reference/01-command-cheatsheet)
- 想快速查接口：看 [API Surface 速查](/09-reference/05-api-surface)
- 想快速查 CLI：看 [CLI Surface 速查](/09-reference/06-cli-surface)
- 想知道改完跑什么：看 [验证矩阵](/09-reference/07-validation-matrix)
- 想生成课程结构盘点：看 [学习站清单生成器](/09-reference/08-learning-inventory)
- 想生成公开发布摘要：看 [发布摘要生成器](/09-reference/09-release-brief)
- 想生成可带练课程目录：看 [课程目录生成器](/09-reference/10-course-catalog)
- 想生成共学议程和模块卡片：看 [自动生成共学包](/14-workshop-kit/07-generated-workshop-packet)
- 想生成模块题目和评分标准：看 [自动生成测评包](/10-assessments/06-generated-assessment-pack)
- 想生成首批 GitHub issue 种子：看 [自动生成路线图包](/08-publication/05-generated-roadmap-pack)
- 想生成 release notes、首批 issue 和发布后检查表：看 [自动生成首发运营包](/08-publication/13-generated-launch-pack)
- 想定位卡点：看 [常见排障手册](/09-reference/04-troubleshooting)
- 想快速查词：看 [术语索引](/00-overview/13-glossary)
- 如果还拿不准：看 [按目标选择学习路径](/00-overview/07-choose-your-path)
- 如果你卡在“到底该怎么学才算有效”：看 [常见问题 FAQ](/00-overview/10-faq)

## 如果你准备把它分享给别人

建议先读 [面向分享的学习方式](/00-overview/11-public-learning-guide)，再打开 [共学与公开分享套件](/14-workshop-kit/00-overview)、[自动生成共学包](/14-workshop-kit/07-generated-workshop-packet)、[自动生成测评包](/10-assessments/06-generated-assessment-pack)、[自动生成路线图包](/08-publication/05-generated-roadmap-pack) 和 [自动生成首发运营包](/08-publication/13-generated-launch-pack)，完成 [系统 Capstone 与验收 Rubric](/07-hands-on-labs/05-capstone-review-rubric) 和 [公开发布验收 Lab](/07-hands-on-labs/06-public-release-readiness-lab)，最后用 [Capstone 答辩稿](/10-assessments/04-capstone-defense) 做一次公开展示前的自测。

如果你准备发布到 GitHub 或部署在线站点，再看 [公开发布总览](/08-publication/00-overview)、[GitHub Pages 发布指南](/08-publication/01-github-pages)、[GitHub 仓库设置建议](/08-publication/04-repository-settings)、[维护节奏与运营清单](/08-publication/08-maintainer-rhythm)、[Issue 分类与标签策略](/08-publication/09-issue-triage-and-labels)、[v0.1 首发发布手册](/08-publication/10-v0-1-release-playbook)、[首批公开 Issues 草稿](/08-publication/11-first-public-issues)、[v0.1 Release Notes 草稿](/08-publication/12-v0-1-release-notes-draft)、[自动生成首发运营包](/08-publication/13-generated-launch-pack) 和 [GitHub 入口与协作地图](/08-publication/14-github-entrypoints)。

这样你不仅能把项目跑起来，还能讲清楚：

- 这套系统分成哪几层
- 每一层为什么存在
- 失败路径如何表现
- 当前学习型实现和生产级系统差在哪里

## 推荐的第一份学习产出

如果你今天只想做一件能沉淀下来的事，建议写一份很短的“第一次端到端记录”。

可以直接用这个格式：

```text
我今天跑通的链路：
我使用的命令：
我看到的请求证据：
我看到的评测或训练产物：
我能解释的系统行为：
我还不能解释的问题：
下一次我会继续验证：
```

这份记录不需要写得像正式博客。它的价值是把你的学习从“我大概看懂了”变成“我能指出证据在哪里”。等你后面想写 README、博客、GitHub issue 或共学材料时，这些小记录会比临时回忆可靠得多。

## 本地怎么启动这个学习站

```bash
nvm use
npm install
npm run docs:dev
```

`nvm use` 会读取仓库里的 `.nvmrc`，当前推荐 Node 22。

启动后直接打开：

- `http://localhost:5173`

如果你想打成静态站：

```bash
npm run docs:build
npm run docs:preview
```
