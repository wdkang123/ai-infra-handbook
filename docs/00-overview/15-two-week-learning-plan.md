# 两周学习计划

这页把课程大纲拆成一个可以执行的两周节奏。

它不是强制排期，而是帮你避免两个常见问题：

- 只读文档，不跑代码
- 只跑命令，不知道自己学会了什么

如果你时间更少，可以把两天压成一天。  
如果你希望讲给别人听，可以把每一天都加上 10 分钟复盘。

## 第 1 周：跑通系统地图

### Day 1：建立整体地图

阅读：

- [从 0 到 1 学习路径](/00-overview/00-zero-to-one)
- [什么是 AI Infra](/00-overview/01-what-is-ai-infra)
- [学习路线图](/00-overview/02-learning-route)
- [项目成熟度地图](/00-overview/14-project-maturity-map)

产出：

- 写下执行层、治理层、质量层、训练层各自解决什么问题
- 能解释为什么这不是一个单体 demo

验收：

- 完成 [系统地图自测](/10-assessments/01-system-map-check)

### Day 2：跑通最小环境

阅读：

- [最小运行手册](/00-overview/03-runbook)
- [第一次实操演练](/00-overview/04-first-walkthrough)

命令：

```bash
nvm use
PYTHON=.venv/bin/python make infra-check
```

产出：

- 确认文档构建和单元测试通过
- 记下四个项目的入口文件

### Day 3：理解推理服务

阅读：

- [模型、Token、Context](/01-llm-fundamentals/01-model-token-context)
- [从请求到首个 Token](/01-llm-fundamentals/04-from-request-to-first-token)
- [inference-service](/06-projects/01-inference-service)

动手：

- 启动 inference-service
- 发送普通请求和 streaming 请求
- 查看 `/metrics`、`/events`、`/events/requests`

产出：

- 能解释 request id、token usage、streaming event 的关系

### Day 4：理解平台治理

阅读：

- [鉴权、路由、限流](/03-ai-gateway-platform/01-auth-routing-rate-limit)
- [Gateway、Router、Fallback、Cache](/03-ai-gateway-platform/03-gateway-router-fallback-cache)
- [ai-gateway](/06-projects/02-ai-gateway)

动手：

- 发送正常 gateway 请求
- 触发 `401 / 404 / 429 / 502`
- 查看 `/events/failures`

产出：

- 能解释 gateway 为什么不是“多一层转发”

### Day 5：做前两组 Lab

完成：

- [Serving 可观测性 Lab](/07-hands-on-labs/01-serving-observability-lab)
- [Gateway 韧性 Lab](/07-hands-on-labs/02-gateway-resilience-lab)
- [Serving 与 Gateway 输出证据](/13-output-gallery/01-serving-gateway-evidence)
- [失败症状到证据地图](/13-output-gallery/05-failure-evidence-map)

验收：

```bash
PYTHON=.venv/bin/python make infra-smoke
```

产出：

- 写一段 200 字复盘：正常路径和失败路径分别留下了什么证据

## 第 2 周：建立质量和资产直觉

### Day 6：理解评测 run

阅读：

- [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
- [LLM Evaluation](/04-evaluation-observability/05-llm-evaluation)
- [eval-module](/06-projects/03-eval-module)

动手：

- 跑一次 eval run
- 查看 `result.json`、`sample_outputs.json`、`sample_summary.json`、`sample_analysis.json`

产出：

- 能解释 sample output、sample summary、sample analysis 的区别

### Day 7：理解发布判断

阅读：

- [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)
- [Benchmark 与生产质量不是一回事](/04-evaluation-observability/08-benchmark-vs-production-quality)

动手：

- 跑一次 compare
- 生成 leaderboard
- 生成 run index 和 comparison index

产出：

- 能解释 `release_recommendation` 为什么只是门禁建议

### Day 8：理解训练资产

阅读：

- [LoRA、QLoRA、PEFT](/05-finetuning-training/01-lora-qlora-peft)
- [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)
- [finetune-demo](/06-projects/04-finetune-demo)

动手：

- 跑一次 mock train
- 查看 run manifest、dataset summary、checkpoint index、artifacts manifest

产出：

- 能解释为什么 checkpoint 只是资产目录的一部分

### Day 9：理解 export 和复现

阅读：

- [实验追踪、History、复现](/05-finetuning-training/06-experiment-tracking-history-reproducibility)
- [从 Demo Training 到真实训练系统](/05-finetuning-training/08-from-demo-training-to-real-training-system)

动手：

- 跑一次 export
- 生成 run index、dataset registry report、export index

产出：

- 能从 export manifest 追溯回训练 run 和 dataset

### Day 10：做后两组 Lab

完成：

- [Eval 发布门禁 Lab](/07-hands-on-labs/03-eval-release-gate-lab)
- [Finetune 复现资产 Lab](/07-hands-on-labs/04-finetune-reproducibility-lab)
- [Eval 报告证据](/13-output-gallery/02-eval-report-evidence)
- [Finetune 产物证据](/13-output-gallery/03-finetune-artifact-evidence)

验收：

```bash
PYTHON=.venv/bin/python make infra-check
PYTHON=.venv/bin/python make infra-smoke
```

产出：

- 写一段 300 字复盘：一个模型迭代如何经过 train、eval、gateway 发布判断

## 最后 4 天：准备分享

### Day 11：做 Capstone

阅读：

- [案例复盘总览](/11-case-studies/00-overview)
- 至少选择一个案例完整读完
- [端到端复盘证据包](/13-output-gallery/04-end-to-end-review-packet)

完成：

- [系统 Capstone 与验收 Rubric](/07-hands-on-labs/05-capstone-review-rubric)
- [Capstone 答辩稿](/10-assessments/04-capstone-defense)

产出：

- 一份 5 分钟讲解稿
- 一张系统图
- 一组验证命令
- 一段基于案例的工程复盘
- 一份能公开分享的输出证据包

### Day 12：做发布前验收

完成：

- [公开发布验收 Lab](/07-hands-on-labs/06-public-release-readiness-lab)
- [公开发布总览](/08-publication/00-overview)
- [GitHub 仓库设置建议](/08-publication/04-repository-settings)
- [公开演示脚本](/13-output-gallery/06-public-demo-script)

命令：

```bash
PYTHON=.venv/bin/python make docs-inventory
PYTHON=.venv/bin/python make course-catalog
npm run docs:build
PYTHON=.venv/bin/python make infra-check
PYTHON=.venv/bin/python make infra-smoke
PYTHON=.venv/bin/python make release-brief
PYTHON=.venv/bin/python make workshop-packet
PYTHON=.venv/bin/python make assessment-pack
PYTHON=.venv/bin/python make roadmap-pack
PYTHON=.venv/bin/python make launch-pack
npm audit --omit=dev --audit-level=moderate
```

产出：

- 确认 README、导航、文档、代码和 smoke 状态一致
- 生成一份可分享的学习站清单
- 生成一份可带练的课程目录
- 生成一份可公开复盘的发布摘要
- 生成一份可直接组织共学的共学包
- 生成一份可用于模块自测和评分的测评包
- 生成一份可整理首批 GitHub issue 的路线图包
- 生成一份可复核 release notes、starter issues 和发布后检查表的首发运营包
- 整理一段 GitHub 项目介绍

### Day 13：整理共学材料

阅读：

- [共学与公开分享套件](/14-workshop-kit/00-overview)
- [讲师与带练指南](/14-workshop-kit/01-facilitator-guide)
- [学习者工作簿](/14-workshop-kit/02-learner-workbook)
- [复盘与评审模板](/14-workshop-kit/04-review-templates)
- [自动生成共学包](/14-workshop-kit/07-generated-workshop-packet)
- [自动生成测评包](/10-assessments/06-generated-assessment-pack)
- [自动生成路线图包](/08-publication/05-generated-roadmap-pack)
- [自动生成首发运营包](/08-publication/13-generated-launch-pack)

完成：

- 把 Day 1 到 Day 12 的命令、证据和卡点整理进工作簿
- 用评审模板写一份 5 分钟公开展示稿
- 选出最适合 first-time contributor 的 3 个任务

产出：

- 一份可分享的学习者工作簿
- 一份公开演示复盘模板
- 一份自动生成的共学包
- 一份自动生成的测评包
- 一份自动生成的路线图包
- 一份自动生成的首发运营包
- 一组可直接筛选成 issue 的贡献任务

### Day 14：制定 GitHub 首发计划

阅读：

- [贡献者协作手册](/14-workshop-kit/05-contribution-playbook)
- [GitHub 发布计划](/14-workshop-kit/06-github-release-plan)
- [自动生成首发运营包](/08-publication/13-generated-launch-pack)

完成：

- 对照首发前一周检查项确认状态
- 设计 README 首发介绍
- 准备首批 issue 和 label
- 确认 GitHub Pages、CI、issue templates 和 PR template 的使用方式

产出：

- 一份首发检查记录
- 一份发布公告草稿
- 一份发布后 30 天迭代计划

## 每天的复盘模板

```text
今天学的是哪一层：

我跑了什么命令：

我看到了什么产物或指标：

正常路径是什么：

失败路径是什么：

我现在还能说不清的问题：

下一步要回看的页面或代码：
```

这份计划真正想训练的不是记住每个名词，而是形成一种习惯：每学一个概念，都能找到对应代码、对应命令、对应产物和对应验收。
