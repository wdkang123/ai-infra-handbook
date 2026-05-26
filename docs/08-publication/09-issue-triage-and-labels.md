# Issue 分类与标签策略

这页用于公开仓库的 issue triage。

好的 issue 分类不是为了看起来专业，而是让读者反馈、贡献任务、路线图和 PR 验收能接到一起。

如果 issue 没有分类、没有上下文、没有验收标准，维护者会很快被噪音淹没；如果分类过重，又会让第一次贡献的人不敢开始。所以这页采用一个轻量策略：先用 GitHub 默认标签，等协作真的变多后再扩展自定义标签。

## 默认原则

先用 GitHub 默认标签，等协作真的变多后再增加自定义标签。

原因很简单：新仓库默认通常已经有 `bug`、`documentation`、`enhancement`、`good first issue`、`help wanted`、`question` 等标签。

如果 issue template 或 Dependabot 配置引用不存在的标签，GitHub 会在 issue/PR 里留下 label not found 一类提示，反而增加维护噪音。

## Issue 分类的目标

每个 issue 最好能回答：

- 它属于哪类问题
- 影响哪条学习路径
- 需要改哪些页面或项目
- 完成后怎么验证
- 是否适合新贡献者
- 是否需要进入 roadmap

Issue 不是聊天记录的替代品，而是可维护任务的入口。

## 推荐标签

### 直接使用默认标签

| Label | 用途 | 适合的 issue |
| --- | --- | --- |
| `bug` | 可复现问题 | 命令失败、构建失败、链接错误、行为和文档不一致 |
| `documentation` | 文档与学习路径 | 概念解释、前后链接、证据说明、公开分享材料 |
| `enhancement` | 功能或学习体验增强 | 新 lab、新案例、新生成器、新迁移说明 |
| `good first issue` | 适合第一次贡献 | 范围小、验收清楚、不要求理解全部系统 |
| `help wanted` | 欢迎外部贡献 | 需要真实读者反馈、运行证据或领域经验 |
| `question` | 学习问题或设计讨论 | 需要澄清背景、适合转成 FAQ 的问题 |
| `duplicate` | 重复问题 | 已有同类 issue 或 PR |
| `invalid` | 不符合范围 | 无法复现、信息不足、和项目目标无关 |
| `wontfix` | 明确暂不处理 | 超出学习型项目边界或当前阶段不做 |

### 可选自定义标签

等你准备长期维护时，可以再创建：

| Label | 建议用途 |
| --- | --- |
| `lab` | hands-on lab 任务 |
| `evidence` | 示例输出、报告、manifest、截图和字段解释 |
| `feedback` | 共学、公开演示、读者体验反馈 |
| `case-study` | 工程复盘故事 |
| `ci` | GitHub Actions、Pages、构建链路 |
| `dependencies` | Dependabot、npm、pip、GitHub Actions 版本维护 |
| `python` | Python 项目、脚本、测试和 lint |

创建这些标签之前，不要在模板或 bot 配置中强制引用它们。

## 当前模板映射

仓库里的 issue templates 应该只引用已存在的默认标签。

| Template | 默认 labels | 说明 |
| --- | --- | --- |
| Bug report | `bug` | 要求复现步骤和脱敏输出 |
| Docs improvement | `documentation` | 处理解释、链接和学习路径问题 |
| Hands-on lab idea | `enhancement`, `documentation` | 新 lab 先按学习体验增强处理 |
| Evidence example | `documentation` | 如果已创建 `evidence`，可以再手动补 |
| Workshop feedback | `documentation` | 如果已创建 `feedback`，可以再手动补 |
| Learning question | `question` | 可沉淀到 FAQ、排障或路线图 |
| Roadmap task | `enhancement`, `help wanted` | 从 roadmap-pack 或维护复盘拆出的任务 |

## Triage 流程

收到 issue 后按这个顺序处理：

1. 先判断它是 bug、docs、lab、evidence、feedback、question 还是 roadmap。
2. 如果是 bug，要求复现命令、实际输出和期望输出。
3. 如果是 docs，定位到具体页面和段落。
4. 如果是 lab 或 evidence，补上验收标准和关联页面。
5. 如果是 question，判断是否应该进入 FAQ 或排障手册。
6. 如果是 roadmap，确认它是否能被拆成 1 到 2 个 PR。
7. 给 issue 写清完成后怎么验证。

一个 issue 如果没有验收方式，不要急着标成 good first issue。

## 优先级口径

这个仓库不需要一开始创建很多 priority labels。

可以先在评论或 issue 描述中使用轻量口径：

| 级别 | 含义 |
| --- | --- |
| P0 | 影响公开安全、CI、Pages、README 开始路径或核心命令 |
| P1 | 影响主要学习路径、lab 验收、示例输出或生成器 |
| P2 | 局部解释、补充材料、样式和长期优化 |

P0 要尽快处理；P1 进入近期路线图；P2 可以合并到后续批量维护。

## Good First Issue 标准

适合第一次贡献的 issue 应该满足：

- 只改 1 到 3 个文件
- 不要求理解全部四个项目
- 验收命令明确
- 不涉及真实密钥、线上权限或复杂依赖升级
- 有清楚的关联页面
- 改完能看出学习价值

示例：

- 给 [常见排障手册](/09-reference/04-troubleshooting) 增加一个可复现问题
- 给某个 lab 补充“成功时应该看到什么”
- 给输出证据页补一个字段解释
- 给 FAQ 增加一个来自 workshop feedback 的问题
- 给某个自测题补一段参考答案

## 不适合 Good First Issue 的任务

这些任务不要轻易标 good first issue：

- 引入真实 serving backend
- 改 workflow 权限
- 大版本依赖升级
- 重构四个项目的共享接口
- 需要外部 API key 才能验证
- 没有明确验收方式的“优化体验”

它们可以是 roadmap 或 help wanted，但不适合第一次贡献。

## 关闭 issue 的标准

可以关闭的情况：

- 已经通过 PR 修复，并在评论里写明验证命令
- 重复 issue 已经链接到主 issue
- 需求超出学习型项目当前边界
- 反馈信息不足，维护者已经要求补充但长期没有回复
- 该问题已经被新的路线图 issue 覆盖

关闭时最好留下 1 到 2 句话，说明原因和替代入口。

## 和 PR 的关系

PR 应该至少关联一个 issue，或者在 PR 描述中说明为什么不需要 issue。

合并前重点看：

- issue 的学习价值是否被解决
- PR 是否更新了相关文档、导航或检查清单
- 是否跑过相应验证命令
- 新增页面是否出现在 sidebar
- 公开安全检查是否通过
- Changelog 是否需要记录

如果 PR 只是顺手改很多东西，但无法对应到 issue 或验证命令，先拆小。

## Issue 评论模板

维护者可以用：

```text
感谢反馈。这个 issue 我先归类为：

类型：
影响页面/项目：
建议验收：
建议验证命令：

如果你愿意提交 PR，建议先从这些文件开始：
-
```

这能让 issue 从“问题描述”变成“可执行任务”。

## 下一步

- 处理日常维护时看 [维护节奏与运营清单](/08-publication/08-maintainer-rhythm)。
- 拆路线图任务时看 [自动生成路线图包](/08-publication/05-generated-roadmap-pack)。
- 创建首批 release 和 issue 前看 [自动生成首发运营包](/08-publication/13-generated-launch-pack)。
- 写贡献说明时看 [贡献者协作手册](/14-workshop-kit/05-contribution-playbook)。

## 常见误区

### Label 越多越专业

不一定。标签越多，使用成本越高。先让默认标签跑起来。

### 所有问题都应该马上变成任务

不需要。有些问题更适合先进入 FAQ 或讨论。

### Good first issue 只是简单任务

它还必须有清楚验收和学习价值。

### 关闭 issue 就不用解释

公开项目里，关闭原因本身也是维护证据。
