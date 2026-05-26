# 维护节奏与运营清单

这页用于项目公开之后的日常维护。

公开学习站不是一次性上传完成，而是要持续把读者反馈、依赖更新、文档质量和路线图收进一个稳定节奏里。

维护的目标不是让项目每天都有大变化，而是让它一直保持：

- 能读
- 能跑
- 能查
- 能贡献
- 能安全公开

## 维护目标

维护时优先保护四件事：

| 目标 | 含义 |
| --- | --- |
| 学习路径稳定 | 第一次来的读者仍然知道从哪里开始 |
| 命令可复现 | README、Runbook、Labs 和证据页里的命令仍然能跑 |
| 公开信息安全 | 没有真实密钥、本机路径、私有 endpoint 或敏感日志 |
| 贡献边界清楚 | issue、PR、roadmap 和 release notes 都能说明验收方式 |

如果一次改动不能同时满足这些目标，先缩小范围。

## 每次 PR 前

每次改动准备提交前，先按改动类型选择检查：

| 改动类型 | 最小检查 | 额外检查 |
| --- | --- | --- |
| 文档小修 | `PYTHON=.venv/bin/python make docs-quality` | 如果改导航，再跑 `npm run docs:build` |
| README、发布、贡献文档 | `PYTHON=.venv/bin/python make public-check` | 检查 GitHub 页面入口是否仍准确 |
| 代码或脚本 | `PYTHON=.venv/bin/python make infra-check` | 涉及跨服务时跑 `make infra-smoke` |
| 依赖或 workflow | `PYTHON=.venv/bin/python make public-check` | npm 改动跑 `npm audit --omit=dev --audit-level=moderate` |
| 课程、共学、测评、路线图生成器 | `PYTHON=.venv/bin/python make infra-check` | 跑对应生成命令确认输出结构 |

PR 描述里至少记录：

- 这次改动解决哪个读者或维护者问题
- 影响哪些页面、脚本或项目
- 跑过哪些验证命令
- 有没有公开安全影响
- 是否需要更新 changelog

## 每周维护

每周做一次轻量维护，重点不是大改，而是清理积压和确认主线没有漂移。

| 项目 | 做什么 | 输出 |
| --- | --- | --- |
| Dependabot | 看是否有 npm、pip、GitHub Actions 更新 | 合并、手动升级或留下关闭原因 |
| Issues | 给新 issue 分类型、补验收标准 | 进入 backlog、good first issue 或关闭 |
| 文档入口 | 快速打开首页、README、学习路线、Runbook | 发现入口过期就优先修 |
| 反馈 | 汇总 workshop feedback、docs improvement、question | 变成 FAQ、lab 修正或 roadmap issue |
| 质量 | 至少跑一次 `public-check` | 确认公开安全和站点构建仍通过 |

推荐命令：

```bash
nvm use 22
PYTHON=.venv/bin/python make public-check
npm audit --omit=dev --audit-level=moderate
```

如果本周改过 smoke、证据库或共学材料，再补跑：

```bash
PYTHON=.venv/bin/python make infra-smoke
PYTHON=.venv/bin/python make infra-evidence
PYTHON=.venv/bin/python make release-brief
PYTHON=.venv/bin/python make workshop-packet
PYTHON=.venv/bin/python make assessment-pack
PYTHON=.venv/bin/python make roadmap-pack
PYTHON=.venv/bin/python make launch-pack
```

## 每月维护

每月适合做一次结构性复盘。

| 复盘问题 | 判断方式 |
| --- | --- |
| 新读者是否还能在 10 分钟内找到开始路径 | 看 README、首页、从 0 到 1、学习路线 |
| 最小运行路径是否仍然可靠 | 跑 `infra-smoke`，对照输出证据页 |
| 哪些问题重复出现 | 汇总 issue、workshop feedback、FAQ |
| 哪些页面变成只解释不验证 | 给页面补命令、输出或复盘问题 |
| 哪些路线图太大 | 拆成小 issue，并写清验收命令 |
| 哪些输出证据过期 | 重跑 smoke 或更新证据库 |
| 哪些页面最少被入口链接到 | 补导航、相关页或学习路径 |

月度复盘不一定要做 release，但建议更新：

- [公开路线图](/08-publication/03-public-roadmap)
- [常见问题 FAQ](/00-overview/10-faq)
- [常见排障手册](/09-reference/04-troubleshooting)
- [示例输出与证据库](/13-output-gallery/00-overview)
- [共学与公开分享套件](/14-workshop-kit/00-overview)

## 发布节奏

这个项目可以用轻量版本节奏，不需要复杂发布工程。

| 阶段 | 适合发布什么 |
| --- | --- |
| Patch | 文档修正、链接修复、依赖升级、模板修正 |
| Minor | 新 lab、新案例、新生成器、新的学习主线 |
| Milestone | 能支撑一次完整公开分享或学习小组复盘 |

每次 release notes 至少写清：

- 新增了什么学习价值
- 影响哪些入口
- 跑过哪些验证命令
- 是否有 breaking change
- 是否仍然是学习型项目而非生产平台

## 维护记录模板

可以在 issue、PR 或 release notes 中使用：

```text
维护范围：
-

读者影响：
-

验证：
- [ ] PYTHON=.venv/bin/python make public-check
- [ ] npm audit --omit=dev --audit-level=moderate
- [ ] GitHub Actions ci/docs-pages 通过
- [ ] GitHub Pages 返回 200

公开安全：
- [ ] 没有真实密钥、私有 endpoint、本机路径或敏感日志
- [ ] 示例输出已脱敏

后续 issue：
-
```

## 维护红线

这些情况要先停下来处理，不要继续合并：

- PR 中出现真实 API key、token、私钥、cookie、内部 URL
- 文档把学习型 mock 说成生产级能力
- 新页面没有入口，读者无法从导航找到
- issue 或 PR 没有可验证的完成标准
- 依赖升级后 CI 或 Pages 没有实际跑过
- 读者反馈反复指向同一个卡点，但路线图没有承接
- public-check 或 docs-quality 失败但仍准备发布

## 如何处理读者反馈

反馈不要只留在聊天里。

建议这样流转：

```text
读者反馈
  -> 判断是 question / bug / docs / lab / roadmap
  -> 建 issue 或补 FAQ
  -> 写清验收标准
  -> PR 修复
  -> 记录验证命令
  -> 必要时进入 release notes
```

如果一个问题被问了两次，就值得进入 FAQ 或排障手册。

如果一个 lab 被多人卡住，就值得补验收标准或示例输出。

## 如何处理依赖更新

Dependabot 和 dependency review 不要只看邮件。

处理时看：

- PR diff
- dependency type
- 是否安全修复
- 是否 major upgrade
- 本地 public-check
- GitHub Actions
- Pages 结果

更细规则见 [依赖维护与 Bot PR 处理](/08-publication/07-dependency-maintenance)。

## 下一步

- 如果你要处理公开反馈，继续看 [Issue 分类与标签策略](/08-publication/09-issue-triage-and-labels)。
- 如果你要处理 bot PR，继续看 [依赖维护与 Bot PR 处理](/08-publication/07-dependency-maintenance)。
- 如果你要规划后续任务，继续看 [自动生成路线图包](/08-publication/05-generated-roadmap-pack)。
- 如果你要复核 release 和首批 issue，继续看 [自动生成首发运营包](/08-publication/13-generated-launch-pack)。

## 常见误区

### 维护就是持续加新功能

不对。公开学习站更需要稳定入口、可靠命令和清楚证据。

### issue 越多越活跃

不一定。没有分类和验收标准的 issue 会增加维护噪音。

### release notes 只写新增内容

也要写验证、边界和是否仍是学习型项目。

### 依赖更新可以全自动合并

不要。依赖会影响读者本地运行路径和 GitHub Pages 构建。

### public-check 偶尔失败没关系

公开仓库不应该带着 public-check 失败继续发版。
