# v0.1 首发发布手册

这页用于准备第一个公开 release。
它不是要求你马上打 tag，而是把 v0.1 需要说清楚的范围、验证、发布说明和后续维护动作提前整理好。

## v0.1 的定位

建议第一个 release 命名为：

```text
v0.1.0-learning-site
```

这个版本应该表达三件事：

| 维度 | v0.1 应该承诺什么 | v0.1 不应该承诺什么 |
| --- | --- | --- |
| 学习内容 | 有结构化学习路线、模块页、labs、案例、自测和共学材料 | 覆盖所有 AI Infra 主题 |
| 可运行代码 | 四个学习型项目能跑通最小闭环 | 等价于生产 serving、gateway、eval 或 training 平台 |
| 公开维护 | CI、Pages、模板、安全检查和维护文档齐全 | 已经有成熟社区治理 |

v0.1 的目标是让新读者可以开始系统学习，让维护者可以持续接住反馈。

## 发布前门禁

发布前建议先跑：

```bash
nvm use
PYTHON=.venv/bin/python make public-check
PYTHON=.venv/bin/python make infra-smoke
PYTHON=.venv/bin/python make infra-evidence
PYTHON=.venv/bin/python make release-brief
PYTHON=.venv/bin/python make workshop-packet
PYTHON=.venv/bin/python make assessment-pack
PYTHON=.venv/bin/python make roadmap-pack
npm audit --omit=dev --audit-level=moderate
```

如果你只是在小范围改文档，`public-check` 已经足够。
但打 release 之前，建议跑完整链路，因为 release notes 需要能说明“这套学习站不仅能看，还能跑、能复盘、能组织共学、能拆路线图”。

## 人工检查清单

自动检查通过之后，再人工打开这些入口：

- [首页](/)
- [从 0 到 1 学习路径](/00-overview/00-zero-to-one)
- [学习路线图](/00-overview/02-learning-route)
- [最小运行手册](/00-overview/03-runbook)
- [第一次实操演练](/00-overview/04-first-walkthrough)
- [案例复盘总览](/11-case-studies/00-overview)
- [示例输出与证据库](/13-output-gallery/00-overview)
- [共学与公开分享套件](/14-workshop-kit/00-overview)
- [公开发布总览](/08-publication/00-overview)
- [维护节奏与运营清单](/08-publication/08-maintainer-rhythm)

重点看：

- 新读者是否知道第一步该做什么
- README 和首页是否没有互相矛盾
- 文档站里的核心入口是否都能从导航找到
- release 说明是否没有把学习型实现包装成生产系统
- GitHub Pages 是否返回 200

## Release Notes 模板

可以直接把下面这段作为 v0.1 release notes 的起点：

```text
AI Infra Handbook v0.1.0-learning-site

这是一个学习型首发版本，用于系统学习 AI Infra 的主干工程路径。

包含：
- VitePress 文档站与 GitHub Pages 发布流程
- 从 0 到 1 学习路径、课程大纲、两周学习计划和术语索引
- 四个可运行学习项目：inference-service、ai-gateway、eval-module、finetune-demo
- Hands-on labs：Serving、Gateway、Eval、Finetune、Capstone 和公开发布验收
- 案例复盘：请求失败、模型发布判断、训练产物复现、Gateway fallback/cache、Eval 退化阻断
- 示例输出与证据库：HTTP header、events、eval report、finetune manifest、失败证据和公开演示脚本
- 自动生成产物：learning inventory、course catalog、evidence packet、release brief、workshop packet、assessment pack、roadmap pack
- 公开协作材料：issue templates、PR template、贡献指南、安全说明、维护节奏和 issue triage

验证：
- PYTHON=.venv/bin/python make public-check
- PYTHON=.venv/bin/python make infra-smoke
- PYTHON=.venv/bin/python make release-brief
- PYTHON=.venv/bin/python make workshop-packet
- PYTHON=.venv/bin/python make assessment-pack
- PYTHON=.venv/bin/python make roadmap-pack
- npm audit --omit=dev --audit-level=moderate

边界：
- 这是学习项目，不是生产平台
- 默认路径使用 mock / local scaffold，便于读者复现
- 真实 serving、gateway、eval 和 training 接入请参考生产迁移章节
```

## 首发后 24 小时

发布后第一天不要急着继续大改。先确认：

| 检查 | 目标 |
| --- | --- |
| README | GitHub 第一屏能解释项目定位 |
| Pages | 在线站点能访问，核心入口能打开 |
| Actions | `ci`、`docs-pages`、Dependabot 相关检查没有失败 |
| Issues | 模板可用，没有引用不存在的 labels |
| Release | release notes 能说明验证命令和学习边界 |

如果收到第一批反馈，优先把它们归类成：

- FAQ
- 排障条目
- lab 验收补充
- 示例输出补充
- 路线图 issue

## 首发后 7 天

第一周最值得做的是收集真实卡点。
不要先追求新功能，先回答：

- 哪个入口最常被问
- 哪条命令最容易失败
- 哪个概念读者最难理解
- 哪个 lab 的“成功标准”不够清楚
- 哪类输出证据最需要补截图或字段解释

这些反馈应该回流到：

- [常见问题 FAQ](/00-overview/10-faq)
- [常见排障手册](/09-reference/04-troubleshooting)
- [示例输出与证据库](/13-output-gallery/00-overview)
- [Issue 分类与标签策略](/08-publication/09-issue-triage-and-labels)
- [自动生成路线图包](/08-publication/05-generated-roadmap-pack)

## 是否现在就创建 GitHub release

可以，但不必急。
比较稳的做法是：

1. 先让 `main` 上的 CI 和 Pages 连续通过。
2. 确认 README、站点首页和发布总览都已经指向在线站点。
3. 从这页复制 release notes，按实际验证结果删改。
4. 在 GitHub Releases 页面创建 `v0.1.0-learning-site`。
5. 发布后把 release 链接补回 README 或 Changelog。

如果你还没有创建首批 roadmap issues，也可以先不打 release，先把 issue 池整理出来。

## 下一步

- 如果要创建公开任务，看 [Issue 分类与标签策略](/08-publication/09-issue-triage-and-labels)。
- 如果要从自动产物挑任务，看 [自动生成路线图包](/08-publication/05-generated-roadmap-pack)。
- 如果要持续维护，看 [维护节奏与运营清单](/08-publication/08-maintainer-rhythm)。
