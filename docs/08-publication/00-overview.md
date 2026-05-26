# 公开发布总览

这一组页面帮助你把学习站从“本地可用”推进到“可以公开分享”。

公开分享时，读者最关心的不只是代码能不能跑，还包括：

- 我从哪里开始
- 这套内容适不适合我
- 当前项目已经做到什么程度
- 跑完命令后能不能看懂输出证据
- 如果想带别人学习，有没有可复用的共学材料
- 网站能不能在线访问
- 我发现问题后怎么反馈
- 我想贡献内容时按什么标准来

## 发布前最重要的十件事

### 1. 本地质量通过

发布前至少确认：

```bash
PYTHON=.venv/bin/python make infra-format
PYTHON=.venv/bin/python make public-check
PYTHON=.venv/bin/python make infra-smoke
```

### 2. 文档站能构建

```bash
nvm use
PYTHON=.venv/bin/python make docs-inventory
PYTHON=.venv/bin/python make course-catalog
PYTHON=.venv/bin/python make docs-quality
npm run docs:build
```

如果这一步失败，GitHub Pages 也大概率会失败。

`docs-inventory` 会生成学习站清单，帮助你在发布前确认章节、页面、课程主线和维护信号没有漂移。
`course-catalog` 会生成可带练课程目录，帮助你确认每条主线都有入口、阅读、实验、证据和自测。
`docs-quality` 会先检查 Markdown 本地链接、heading 锚点、H1 结构、VitePress nav/sidebar 路由、首页配置与 Vue 组件链接、README 关键入口和首页文档页统计，能提前发现很多“构建能过但读者会迷路”的问题。

如果你已经跑过 `infra-smoke`，可以继续运行：

```bash
PYTHON=.venv/bin/python make release-brief
PYTHON=.venv/bin/python make workshop-packet
PYTHON=.venv/bin/python make assessment-pack
PYTHON=.venv/bin/python make roadmap-pack
PYTHON=.venv/bin/python make launch-pack
```

`release-brief` 会把学习站清单和运行证据合成一份公开发布摘要。  
`workshop-packet` 会继续把课程目录和发布摘要合成议程、模块卡片、学习者交付和复盘问题，方便你直接组织共学或公开演示。
`assessment-pack` 会把课程目录和共学包合成模块题目、证据要求、rubric 和 Capstone review，方便读者自测或 reviewer 复盘。
`roadmap-pack` 会把发布摘要和测评包合成首批 GitHub issue 种子，方便把 FAQ、证据库、迁移指南和模块深挖任务拆成可贡献的小任务。
`launch-pack` 会把发布摘要和路线图包合成首发运营包，方便统一 release notes、starter issues、默认标签规范和发布后复盘清单。

### 3. README 能独立解释项目

很多人第一次只会看 GitHub README。  
所以 README 至少要说明：

- 这个项目是什么
- 怎么启动文档站
- 怎么跑检查
- 推荐学习顺序
- 示例输出和复盘证据入口
- 项目成熟度和学习型边界
- 当前不是生产系统

### 4. 许可证要明确

当前仓库已经提供 MIT License。  
如果你后续想把代码和文档拆成不同许可证，可以在 README 中额外说明。

常见选择包括：

- MIT：宽松，适合代码和示例
- Apache-2.0：宽松，并包含专利授权条款
- CC BY 4.0：常用于文档内容

### 5. GitHub 仓库外壳要完整

公开后，读者不只看代码，也会看仓库是否便于参与。

建议确认：

- About description 清楚
- Topics 能帮助搜索
- Website 指向在线文档站
- License、Code of Conduct、Security、Changelog 都可见
- Issue templates 和 PR template 已经存在

### 6. 共学材料能支撑分享

如果你希望这个项目不只是放到 GitHub，而是真的能帮助更多人学习，需要准备：

- 讲师或带练者怎么组织一次学习
- 学习者如何记录命令、证据和复盘
- 学习小组可以采用什么议程
- PR、issue、案例和证据如何保持同一标准
- 首发后 30 天如何收集反馈和继续迭代

这些内容集中在 [共学与公开分享套件](/14-workshop-kit/00-overview)。

### 7. 依赖维护流程要清楚

公开仓库上线后，Dependabot、dependency review、CI 和 Pages workflow 会持续产生反馈。
发布前需要确认：

- Dependabot 覆盖 npm、pip 和 GitHub Actions
- 依赖 PR 有本地检查和 CI 检查路径
- Actions 升级后会确认对应 workflow 实际通过
- 维护者知道如何判断 bot 邮件、关闭 PR 和手动补丁之间的关系
- v0.1 release notes 能说明学习价值、验证命令和项目边界

具体流程见 [依赖维护与 Bot PR 处理](/08-publication/07-dependency-maintenance)。

### 8. 维护节奏要可持续

公开项目最怕“首发很完整，后面无人整理”。
发布后应该明确：

- 每次 PR 前跑什么检查
- 每周如何处理 Dependabot、issue 和读者反馈
- 每月如何复盘学习路径、FAQ、证据库和路线图
- 什么情况必须先停下来处理公开安全问题

具体节奏见 [维护节奏与运营清单](/08-publication/08-maintainer-rhythm)。

### 9. Issue 分类要低噪音

Issue template 和 bot 配置不要引用仓库里不存在的 labels。
初期优先使用 GitHub 默认标签，例如 `bug`、`documentation`、`enhancement`、`good first issue`、`help wanted`、`question`。等贡献真的变多后，再创建 `lab`、`evidence`、`feedback`、`ci`、`dependencies` 等自定义标签。

具体分类见 [Issue 分类与标签策略](/08-publication/09-issue-triage-and-labels)。

### 10. 首发 release 和首批 issues 要说明边界

如果准备创建第一个 GitHub release，不要只写“initial release”。
应该说明：

- 当前版本能帮助读者学什么
- 包含哪些可运行项目、labs、案例和自动产物
- 跑过哪些验证命令
- 仍然是学习型项目，不是生产平台
- 发布后 24 小时和 7 天怎么接反馈
- 首批 issues 的学习价值、验收标准和验证命令是什么

具体模板见 [v0.1 首发发布手册](/08-publication/10-v0-1-release-playbook)、[首批公开 Issues 草稿](/08-publication/11-first-public-issues)、[v0.1 Release Notes 草稿](/08-publication/12-v0-1-release-notes-draft) 和 [自动生成首发运营包](/08-publication/13-generated-launch-pack)。

## 当前已经准备好的材料

仓库已经有：

- `README.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `CHANGELOG.md`
- `LICENSE`
- `PUBLICATION_CHECKLIST.md`
- GitHub issue templates
- Learning question 与 roadmap task issue templates
- Pull request template
- 首批公开 issues 草稿
- v0.1 release notes 草稿
- 首发运营包生成器
- GitHub 入口与协作地图
- CI workflow
- Dependency review workflow
- Dependabot weekly grouped updates
- 支持手动触发和文档相关 push 自动发布的 GitHub Pages workflow

## 推荐发布顺序

1. 创建 GitHub repo
2. 推送代码
3. 设置 About、topics 和默认分支
4. 确认 CI 通过
5. 配置 GitHub Pages 为 GitHub Actions
6. 手动运行一次 docs-pages workflow，确认 Pages 配置可用
7. 把在线站点链接补到 README
8. 根据 [v0.1 首发发布手册](/08-publication/10-v0-1-release-playbook)、[v0.1 Release Notes 草稿](/08-publication/12-v0-1-release-notes-draft) 和 [自动生成首发运营包](/08-publication/13-generated-launch-pack) 准备首个 release notes
9. 根据 [GitHub 发布计划](/14-workshop-kit/06-github-release-plan)、[首批公开 Issues 草稿](/08-publication/11-first-public-issues) 和 [自动生成首发运营包](/08-publication/13-generated-launch-pack) 创建第一批 roadmap issues
10. 用 [自动生成路线图包](/08-publication/05-generated-roadmap-pack) 和 [自动生成首发运营包](/08-publication/13-generated-launch-pack) 持续补充 good first issue、docs、lab 和 evidence 任务

## 发布后优先收集什么反馈

不要一开始只问“你觉得怎么样”。  
更好的问题是：

- 你在哪一步卡住了
- 哪个词不懂
- 哪条命令没跑通
- 哪个 lab 的验收标准不清楚
- 你最想继续深入哪条线

这些反馈能直接变成文档和 lab 的改进。

## 继续阅读

- [GitHub Pages 发布指南](/08-publication/01-github-pages)
- [内容写作规范](/08-publication/02-content-style-guide)
- [公开路线图](/08-publication/03-public-roadmap)
- [GitHub 仓库设置建议](/08-publication/04-repository-settings)
- [自动生成路线图包](/08-publication/05-generated-roadmap-pack)
- [公开仓库卫生规范](/08-publication/06-public-repo-hygiene)
- [依赖维护与 Bot PR 处理](/08-publication/07-dependency-maintenance)
- [维护节奏与运营清单](/08-publication/08-maintainer-rhythm)
- [Issue 分类与标签策略](/08-publication/09-issue-triage-and-labels)
- [v0.1 首发发布手册](/08-publication/10-v0-1-release-playbook)
- [首批公开 Issues 草稿](/08-publication/11-first-public-issues)
- [v0.1 Release Notes 草稿](/08-publication/12-v0-1-release-notes-draft)
- [自动生成首发运营包](/08-publication/13-generated-launch-pack)
- [GitHub 入口与协作地图](/08-publication/14-github-entrypoints)
- [项目成熟度地图](/00-overview/14-project-maturity-map)
- [公开发布验收 Lab](/07-hands-on-labs/06-public-release-readiness-lab)
- [示例输出与证据库](/13-output-gallery/00-overview)
- [学习站清单生成器](/09-reference/08-learning-inventory)
- [课程目录生成器](/09-reference/10-course-catalog)
- [发布摘要生成器](/09-reference/09-release-brief)
- [自动生成共学包](/14-workshop-kit/07-generated-workshop-packet)
- [自动生成测评包](/10-assessments/06-generated-assessment-pack)
- [共学与公开分享套件](/14-workshop-kit/00-overview)
