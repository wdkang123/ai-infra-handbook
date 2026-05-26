# 公开路线图

这页用于对外说明项目后续会怎么长。

路线图不是承诺日期，而是帮助读者和贡献者理解优先级：

- 当前项目已经做到什么
- 下一步最值得补什么
- 哪些方向暂时不做
- 什么样的贡献最适合进入仓库
- 每个阶段如何验收

公开学习项目的路线图不应该只写宏大方向。它更应该告诉读者：这个项目接下来会如何继续变得更可学、更可跑、更可复盘。

## 路线图的读法

这份路线图不是按日历承诺，而是按成熟度推进。

你可以这样理解：

| 问题 | 看哪一段 |
| --- | --- |
| 项目现在能不能公开 | 当前阶段 |
| 新读者体验先补什么 | Phase 1 |
| 代码怎么更接近真实工程 | Phase 2 |
| GitHub 上怎么长期维护 | Phase 3 |
| 什么时候接真实后端 | Phase 4 |
| 如何接住反馈 | Phase 5 |

如果你准备贡献，不要只看“可能方向”，更要看每个阶段的验收。验收标准决定了 issue 应该怎么拆。

## 如何使用路线图

如果准备把路线图拆成 GitHub issue，可以先运行：

```bash
PYTHON=.venv/bin/python make roadmap-pack
PYTHON=.venv/bin/python make launch-pack
```

然后从 `.tmp/roadmap/roadmap_pack.md` 或 `.tmp/launch/launch_pack.md` 选择 5 到 8 条首批 issue。

生成包会把学习价值、建议文件、验收标准和验证命令一起列出来，避免路线图停留在宽泛方向。

也可以先用 [首批公开 Issues 草稿](/08-publication/11-first-public-issues) 中已经整理好的任务作为首发 issue 池。

## 当前阶段

当前项目已经具备：

- VitePress 学习站
- AI Infra 主线文档
- 四个可运行学习项目
- 深度实战 labs
- CI 与 smoke
- GitHub 协作模板
- License、Code of Conduct、Changelog
- 发布检查清单
- 示例输出与证据库
- 共学与公开分享套件
- 学习自测与 Capstone
- 生产迁移路线
- 自动生成 learning inventory、course catalog、evidence packet、release brief、workshop packet、assessment pack、roadmap pack、launch pack
- GitHub Pages 发布链路
- public-check 公共安全与质量门禁

它已经适合开始公开分享和收集反馈。

但它仍然是学习型项目，不是生产平台。

## 路线图原则

### 先学习体验，再生产复杂度

项目的第一目标是帮助读者理解 AI Infra 主干边界。

所以路线图优先级不是“哪个功能最酷”，而是：

- 是否让读者更容易开始
- 是否让概念更容易落到代码
- 是否让输出更容易复盘
- 是否让贡献更容易验收

### 先证据，再展示

漂亮页面有价值，但更重要的是：

- run 是否可追溯
- compare 是否可解释
- fallback 是否可观察
- export 是否有 lineage
- public-check 是否能证明公开安全

展示应该建立在证据之上。

### 先小 issue，再大迁移

公开协作阶段，更适合拆小任务：

- 补一个字段解释
- 补一个 lab 验收标准
- 补一个失败案例
- 补一个自测题
- 补一个真实迁移注意事项

不要一开始就把 issue 写成“实现完整生产平台”。

## Phase 1：学习体验打磨

目标：让第一次来的读者更容易开始。

优先任务：

- 根据真实读者反馈补 FAQ
- 从 [自动生成路线图包](/08-publication/05-generated-roadmap-pack) 中选择 2 到 3 条 good first issue
- 从 [自动生成首发运营包](/08-publication/13-generated-launch-pack) 中复核首批 issue 的默认 labels 和验收命令
- 给每个 overview 增加“学完你能做什么”
- 给 lab 增加更多示例输出和证据包模板
- 根据共学反馈改进学习者工作簿、议程和公开演示材料
- 给常见报错增加排查页面
- 给术语索引增加更多交叉链接
- 根据两周学习计划补更多阶段性练习、示例输出和公开演示材料

验收：

- 新读者能在 10 分钟内找到开始路径
- 新读者能在 30 分钟内跑通最小 smoke 或知道如何分阶段跑
- 每个新增页面至少有一个上游入口和一个下一步入口
- docs-quality 通过

适合拆成 issue 的例子：

- 给某个 lab 增加一组成功/失败示例输出
- 给术语索引补 5 个跨章节高频词
- 给 troubleshooting 补一个真实报错路径
- 给 overview 增加“学完你能做什么”

## Phase 2：项目实现变得更真实

目标：在不牺牲学习可读性的前提下，让实现更接近真实工程。

优先任务：

- inference-service 继续细化真实 tokenizer / streaming usage
- ai-gateway 增加更细的 fallback 失败原因、重试预算和外部 tracing/logging backend
- eval-module 增加真实 judge adapter、更多 sample 聚合维度和更完整 leaderboard/dashboard 视图
- finetune-demo 增加 registry export、resume 策略和多 checkpoint 选择逻辑
- smoke 继续覆盖更多错误路径、header、metrics 和产物字段

验收：

- 每个新增行为都有测试
- 每个新增行为都有对应文档
- `infra-check` 和 `infra-smoke` 保持稳定
- 输出证据进入 [示例输出与证据库](/13-output-gallery/00-overview)

适合拆成 issue 的例子：

- 给 gateway fallback 增加更细 failure reason
- 给 eval sample analysis 增加新聚合字段
- 给 finetune checkpoint index 增加 best/latest 区分
- 给 smoke 增加一个失败路径证据断言

## Phase 3：公开站点运营

目标：让这个学习站可以长期维护。

优先任务：

- 持续确认 GitHub Pages 稳定发布
- README 保持在线站点链接和项目定位准确
- 准备或维护 `v0.1.0-learning-site` release notes
- 设置 repo description、topics 和 About website
- 创建 good first issue
- 创建 roadmap issue
- 用 workshop feedback issue template 收集第一批共学反馈
- 用 learning question 和 roadmap task issue template 收集学习问题与后续任务
- 定期根据反馈整理 FAQ

验收：

- GitHub Pages 能稳定发布
- 新 issue 能被归类到 docs、lab、bug、enhancement
- 贡献者能通过 CONTRIBUTING 快速开始
- 维护者能按 [维护节奏与运营清单](/08-publication/08-maintainer-rhythm) 处理反馈

适合拆成 issue 的例子：

- 首发后整理 5 个学习问题进 FAQ
- 根据 GitHub Pages 首发结果更新发布手册
- 把共学反馈模板里的高频问题转成 lab 改进
- 给 release notes 补一次真实验证记录

## Phase 4：真实后端接入

目标：保留学习型路径，同时提供更真实的接入方式。

可能方向：

- 接入本地 OpenAI-compatible vLLM
- 接入本地 SGLang
- 增加真实 eval runner 适配说明
- 增加真实 PEFT/LoRA 训练的迁移指南
- 增加外部 observability backend 的迁移说明

验收：

- mock 路径仍可跑
- 真实接入路径有清晰前置条件
- 失败时有明确排查文档
- 真实依赖不会破坏公开学习门槛

适合拆成 issue 的例子：

- 增加 OpenAI-compatible vLLM 接入说明
- 增加 SGLang adapter 迁移边界文档
- 增加真实 judge adapter 的最小接口说明
- 增加真实训练前置条件和失败排查清单

## Phase 5：更强的学习社区反馈闭环

目标：把真实读者反馈稳定转成项目改进。

可能方向：

- 周期性整理 learning question issue
- 把重复卡点转成 FAQ 和排障条目
- 把共学反馈转成 lab 改进
- 把 Capstone 中暴露的薄弱点转成自测题
- 把读者贡献的证据包整理进 output gallery

验收：

- 每月能看到反馈进入文档或 issue
- good first issue 不只是占位，而是有清楚验收
- release notes 能说明学习体验如何改善

适合拆成 issue 的例子：

- 每月整理一次 learning question issue
- 把重复报错合并进 troubleshooting
- 把读者提交的 evidence packet 脱敏后加入 output gallery
- 把 capstone 薄弱点转成 assessment 题目

## 暂不优先做什么

这些方向暂时不优先：

- 一上来做完整生产网关
- 引入复杂 Kubernetes 部署
- 做多云平台适配
- 做完整实验追踪平台
- 做完整用户系统
- 做需要真实密钥或私有资源才能跑通的默认路径

原因不是这些不重要，而是它们会让学习主线变散。

当前项目最重要的价值，仍然是让读者在小系统里看懂 AI Infra 的主干关系。

## 维护者如何更新路线图

每次大批量推进后，可以按这个顺序更新路线图：

1. 先跑 `make docs-inventory` 和 `make course-catalog`。
2. 看新增内容落在哪些主线。
3. 把已经完成的方向从“下一步”挪到“当前阶段”。
4. 把新暴露的问题转成 Phase 1 或 Phase 2 的小 issue。
5. 如果涉及公开发布，再跑 `make roadmap-pack` 和 `make launch-pack`。

路线图应该跟着证据变化，而不是凭感觉更新。

## 路线图 issue 应该怎么写

一个好的路线图 issue 应该包含：

```text
学习价值：
改动范围：
建议文件：
验收标准：
验证命令：
相关页面：
不做范围：
```

这样贡献者才知道如何开始，维护者也知道如何验收。

## 下一步

- 如果你要创建公开任务，看 [Issue 分类与标签策略](/08-publication/09-issue-triage-and-labels)。
- 如果你要复核首批 issues，看 [首批公开 Issues 草稿](/08-publication/11-first-public-issues)。
- 如果你要准备 release，看 [v0.1 首发发布手册](/08-publication/10-v0-1-release-playbook)。
- 如果你要持续维护，看 [维护节奏与运营清单](/08-publication/08-maintainer-rhythm)。
