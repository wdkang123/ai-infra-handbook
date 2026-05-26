# 自动生成首发运营包

`launch-pack` 用来把发布摘要和路线图包合成一份首发运营包。
它解决的是公开发布前最后一公里的问题：release notes、首批 issues、发布后检查表和验证命令要来自同一套结构化材料，而不是散落在几篇手写文档里。

## 它在发布链路里的位置

首发前可以把自动产物想成一条流水线：

```text
docs inventory -> course catalog -> evidence packet -> release brief -> assessment pack -> roadmap pack -> launch pack
```

前面的产物回答“内容是否完整、证据是否齐全、课程是否能带练、问题能否拆成 issue”。
`launch-pack` 最后回答：

- 这次 release 应该怎么介绍
- 哪些 issue 适合作为首批公开任务
- 发布后 2 小时、24 小时、7 天和 30 天要检查什么
- 默认 GitHub labels 是否足够支撑首发

它不是自动发布工具，而是公开发布前的运营检查包。

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

## 生成前人工确认

运行前建议先确认：

- 本地没有准备提交的真实 `.env` 或密钥
- README、首页和发布总览已经是最新定位
- `release_brief.md` 不是过期产物
- `roadmap_pack.md` 的 issue seeds 确实来自当前内容缺口
- 你准备发布的是一个阶段性批次，而不是临时半成品

如果刚做过大规模内容扩写，最好先重新跑完整链路。否则 launch pack 可能还在引用旧的页面数量、旧的 issue seeds 或旧的 release readiness。

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

## validation 怎么读

`validation` 不是装饰字段，它决定这份 launch pack 是否适合拿去 GitHub 创建 release 和 issue。

| 信号 | 说明 | 处理 |
| --- | --- | --- |
| release brief 不是 ready | 发布摘要认为当前不适合公开复盘 | 回到 release brief 修缺失项 |
| roadmap pack 不是 ready | 路线图还不能稳定转成 issue | 回到 assessment 或 roadmap pack |
| issue seeds 为空 | 没有首批公开任务 | 补充路线图或手写首批 issue |
| ready_for_public_review 为 false | 公开定位或证据链不足 | 先修文档和证据 |
| ready_for_public_roadmap 为 false | issue 缺学习价值或验收 | 先修 issue seeds |

只有 validation 全部通过时，才建议把 release notes draft 和 starter issues 复制到 GitHub。

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

## Release notes 怎么改

生成的 release notes 是草稿，不应该原封不动粘贴。

人工精修时重点改：

- 把“本轮真实验证命令”补准确
- 删除当天没有验证过的夸张表述
- 明确说明这是学习型项目
- 把在线文档站、README 和首批 issue 链接补上
- 保留 known limitations，避免读者误解生产能力

一份好的 v0.1 release notes 应该让读者知道：

```text
我能在线读什么？
我能本地跑什么？
我能看到哪些证据？
我能从哪些 issue 开始贡献？
这个版本还不能做什么？
```

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

## Starter issues 怎么落地

从 launch pack 创建首批 issue 时，建议每条都保留这几块：

```text
## Learning value
这条 issue 能帮读者理解什么？

## Suggested files
- docs/...
- scripts/...

## Acceptance criteria
- ...

## Verification
- PYTHON=.venv/bin/python make docs-quality

## Out of scope
- 不引入生产级依赖
- 不提交真实密钥或大文件
```

首批 issue 不要太多。3 到 6 条通常更好：足够说明项目欢迎贡献，又不会制造一堆没人维护的任务。

## 如何使用生成结果

推荐流程：

1. 运行 `PYTHON=.venv/bin/python make launch-pack`。
2. 打开 `.tmp/launch/launch_pack.md`。
3. 先看 `Validation`，确认所有字段都为 ready。
4. 从 `Release Notes Draft` 复制首版 release notes，并按当天实际验证结果删改。
5. 从 `Starter Issues` 挑 3 到 6 条创建到 GitHub。
6. 保留 issue 中的 learning value、suggested files、acceptance criteria 和 verification commands。
7. 发布后按 `Post-release Checklist` 做 2 小时、24 小时、7 天和 30 天复盘。

## 发布后怎么用

launch pack 不是发布前用完就扔。

发布后可以用它做四件事：

- 2 小时内：确认 Pages、README、release、starter issues 都能打开
- 24 小时内：检查是否有 Dependabot、Actions 或读者反馈需要处理
- 7 天内：把第一批反馈转成 FAQ、lab、case 或 issue
- 30 天内：复盘哪些 starter issues 真正被点击、讨论或贡献

如果发现 release notes 和实际站点不一致，优先修公开入口。公开项目的第一印象不只来自代码，也来自你是否让读者知道当前状态。

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

## 常见误区

### 把 launch pack 当成自动发布

它不会创建 GitHub release，也不会替你开 issue。这样设计是有意的：首发运营材料必须经过人读，因为公开定位、措辞边界和首批 issue 质量都需要判断。

### 首批 issue 太大

新读者更适合做可完成的小任务。比如“补一个 fallback 输出字段解释”比“重构 gateway”更适合作为首批 issue。

### 只改 release notes 不改上游材料

如果发现 release notes 不准确，通常说明 release brief、roadmap pack 或文档本身需要更新。只改最终文案会让自动产物和真实状态分叉。
