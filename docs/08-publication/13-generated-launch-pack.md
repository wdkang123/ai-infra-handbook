# 自动生成首发运营包

`launch-pack` 用来把发布摘要和路线图包合成一份首发运营包。
它解决的是公开发布前最后一公里的问题：release notes、首批 issues、发布后检查表和验证命令要来自同一套结构化材料，而不是散落在几篇手写文档里。

## 什么时候使用

适合在这些时机运行：

- 准备创建第一个 GitHub release
- 准备从路线图包挑选首批公开 issues
- 大改 README、发布文档、共学材料或验证链路之后
- 首发后 24 小时复盘 release、Pages、Actions 和 issue 池是否一致

它不会自动调用 GitHub API，也不会替你创建 release 或 issue。
它只生成可以人工确认的 JSON / Markdown 运营材料，适合公开仓库上线前做最后复核。

## 生成命令

完整发布前建议按这条链路跑：

```bash
nvm use
PYTHON=.venv/bin/python make public-check
PYTHON=.venv/bin/python make infra-smoke
PYTHON=.venv/bin/python make infra-evidence
PYTHON=.venv/bin/python make release-brief
PYTHON=.venv/bin/python make assessment-pack
PYTHON=.venv/bin/python make roadmap-pack
PYTHON=.venv/bin/python make launch-pack
npm audit --omit=dev --audit-level=moderate
```

如果前面的产物已经存在，也可以只运行：

```bash
PYTHON=.venv/bin/python make launch-pack
```

默认输出：

- `.tmp/launch/launch_pack.json`
- `.tmp/launch/launch_pack.md`

这两个文件位于临时目录，默认不会进入公开提交。
真正需要沉淀到仓库里的，是这页文档、发布手册、首批 issue 草稿和 release notes 草稿。

## 输入产物

`launch-pack` 读取两份上游产物：

| 输入 | 默认路径 | 作用 |
| --- | --- | --- |
| Release brief | `.tmp/release/release_brief.json` | 判断学习站、证据包和公开发布摘要是否 ready |
| Roadmap pack | `.tmp/roadmap/roadmap_pack.json` | 提供 issue seeds、学习价值、验收标准和验证命令 |

严格模式下，生成器会拒绝这些情况：

- release brief 缺失或 `report_type` 不正确
- release brief 不是 `ready`
- release brief 未标记 `ready_for_public_review`
- roadmap pack 缺失或 `report_type` 不正确
- roadmap pack 不是 `ready`
- roadmap pack 未标记 `ready_for_public_roadmap`
- roadmap pack 没有 issue seeds
- roadmap pack 的 summary 数量和实际 `issue_seeds` 数量不一致

这能避免你在材料还没准备好时误把半成品当成首发材料。

## 输出结构

JSON 产物主要包含：

| 字段 | 含义 |
| --- | --- |
| `summary` | launch readiness、release 标题、文档页数、issue 数量和标签模式 |
| `validation` | 每个上游产物是否满足公开首发条件 |
| `release_notes` | 可复制到 GitHub Releases 的标题、亮点、验证命令和边界说明 |
| `starter_issues` | 从路线图包挑出的首批 issue 候选 |
| `post_release_checklist` | 发布后 2 小时、24 小时、7 天、30 天的复盘动作 |
| `publication_flow` | 从自动产物到人工创建 release / issue 的流程说明 |
| `recommended_commands` | 建议在公开发布前记录的验证命令 |

Markdown 产物适合直接人工阅读和复核。
如果你要创建 GitHub release，可以先打开 `.tmp/launch/launch_pack.md`，再把 `Release Notes Draft` 按实际验证结果删改后复制到 GitHub。

## 标签规范化

路线图包里可能会出现 `lab`、`evidence`、`feedback` 等语义更强的标签。
但新仓库刚公开时，这些自定义 labels 通常还没有创建。

所以 `launch-pack` 会把首批 issue 的标签规范化为 GitHub 默认标签：

- `documentation`
- `enhancement`
- `good first issue`
- `help wanted`
- `question`
- 以及其他默认标签

示例：

| 路线图标签 | 首发 issue 标签 |
| --- | --- |
| `lab` | `documentation`, `enhancement` |
| `evidence` | `documentation` |
| `feedback` | `documentation`, `question` |
| 未识别自定义标签 | `enhancement` |

这样首批 issue 可以直接创建，不会因为引用未创建标签而增加维护噪音。
等贡献变多后，再按 [Issue 分类与标签策略](/08-publication/09-issue-triage-and-labels) 创建更细标签。

## 如何使用生成结果

推荐流程：

1. 运行 `PYTHON=.venv/bin/python make launch-pack`。
2. 打开 `.tmp/launch/launch_pack.md`。
3. 先看 `Validation`，确认所有字段都为 ready。
4. 从 `Release Notes Draft` 复制首版 release notes，并按当天实际验证结果删改。
5. 从 `Starter Issues` 挑 3 到 6 条创建到 GitHub。
6. 保留 issue 中的 learning value、suggested files、acceptance criteria 和 verification commands。
7. 发布后按 `Post-release Checklist` 做 2 小时、24 小时、7 天和 30 天复盘。

## 和其他发布材料的关系

- [发布摘要生成器](/09-reference/09-release-brief)：回答“当前学习站和运行证据是否能公开说明”。
- [自动生成测评包](/10-assessments/06-generated-assessment-pack)：回答“读者和 reviewer 能怎么自测和复盘”。
- [自动生成路线图包](/08-publication/05-generated-roadmap-pack)：回答“哪些卡点可以拆成 GitHub issue”。
- [首批公开 Issues 草稿](/08-publication/11-first-public-issues)：提供人工精修后的 issue 文案。
- [v0.1 Release Notes 草稿](/08-publication/12-v0-1-release-notes-draft)：提供人工精修后的 release 页面文案。
- `launch-pack`：把 release notes、starter issues、标签规范和发布后检查表集中成最后的运营包。

## 维护建议

每次公开发布前，优先更新上游结构化产物，再生成 launch pack。
不要只改 release notes 文案，因为那样很容易让验证命令、issue 池和实际站点状态发生漂移。

如果 launch pack 的 `launch_readiness` 是 `review`，先回到 release brief 或 roadmap pack 修输入。
只有当上游证据都清楚时，再去 GitHub 上创建 release 和 issue。
