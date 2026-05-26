# Issue 分类与标签策略

这页用于公开仓库的 issue triage。  
好的 issue 分类不是为了看起来专业，而是让读者反馈、贡献任务、路线图和 PR 验收能接到一起。

## 默认原则

先用 GitHub 默认标签，等协作真的变多后再增加自定义标签。

原因很简单：新仓库默认通常已经有 `bug`、`documentation`、`enhancement`、`good first issue`、`help wanted`、`question` 等标签。  
如果 issue template 或 Dependabot 配置引用不存在的标签，GitHub 会在 issue/PR 里留下“label not found”一类提示，反而增加维护噪音。

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
7. 给 issue 写清“完成后怎么验证”。

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

示例：

- 给 [常见排障手册](/09-reference/04-troubleshooting) 增加一个可复现问题
- 给某个 lab 补充“成功时应该看到什么”
- 给输出证据页补一个字段解释
- 给 FAQ 增加一个来自 workshop feedback 的问题

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

如果 PR 只是“顺手改很多东西”，但无法对应到 issue 或验证命令，先拆小。

## 下一步

- 处理日常维护时看 [维护节奏与运营清单](/08-publication/08-maintainer-rhythm)。
- 拆路线图任务时看 [自动生成路线图包](/08-publication/05-generated-roadmap-pack)。
- 创建首批 release 和 issue 前看 [自动生成首发运营包](/08-publication/13-generated-launch-pack)。
- 写贡献说明时看 [贡献者协作手册](/14-workshop-kit/05-contribution-playbook)。
