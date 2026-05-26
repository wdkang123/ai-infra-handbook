# GitHub 入口与协作地图

这页把网站和 GitHub 仓库之间的入口集中放在一起。

读者可以先在学习站按路线学习，也可以跳到 GitHub 看源码、提 issue、提交 PR 或查看自动检查状态。

一个公开学习项目如果只有网页，没有协作入口，就很难持续改进。反过来，如果只有 GitHub 仓库，没有清楚的学习路径，读者也很容易迷路。

这页的目标，就是把两者接起来。

## 三类访客入口

公开项目的入口要同时照顾三类人：

| 访客 | 他们最想知道 | 推荐入口 |
| --- | --- | --- |
| 第一次学习的人 | 这个项目适不适合我，从哪里开始 | 在线学习站、从 0 到 1 学习路径、第一次实操 |
| 准备贡献的人 | 有什么任务、怎么验证、PR 要写什么 | Issues、贡献指南、验证矩阵、PR 模板 |
| 关注项目状态的人 | 当前质量如何、Pages 是否可用、最近改了什么 | README、Actions、release notes、公开路线图 |

所以 GitHub 入口不应该只是一个仓库链接。
它应该让读者从“我想学”顺滑地走到“我能复现”，再走到“我能反馈或贡献”。

## 公开入口

| 入口 | 链接 | 适合做什么 |
| --- | --- | --- |
| GitHub Profile | [wdkang123](https://github.com/wdkang123) | 查看维护者公开主页和其他项目 |
| Repository | [wdkang123/ai-infra-handbook](https://github.com/wdkang123/ai-infra-handbook) | 查看源码、README、提交记录和仓库文件 |
| Online Site | [AI Infra Handbook](https://wdkang123.github.io/ai-infra-handbook/) | 直接打开在线学习站 |
| Issues | [GitHub Issues](https://github.com/wdkang123/ai-infra-handbook/issues) | 提学习问题、反馈卡点、认领文档或路线图任务 |
| Pull Requests | [GitHub Pull Requests](https://github.com/wdkang123/ai-infra-handbook/pulls) | 提交文档、lab、案例、脚本或代码改进 |
| Actions | [GitHub Actions](https://github.com/wdkang123/ai-infra-handbook/actions) | 查看 CI、Pages 构建和发布验证记录 |

## 第一次来的读者怎么走

如果你是第一次来，不建议直接钻进文件目录。

推荐顺序：

1. 打开 [AI Infra Handbook](https://wdkang123.github.io/ai-infra-handbook/)。
2. 先读 [从 0 到 1 学习路径](/00-overview/00-zero-to-one)。
3. 跑完 [第一次实操演练](/00-overview/04-first-walkthrough)。
4. 对照 [示例输出与证据库](/13-output-gallery/00-overview) 判断结果。
5. 做 [系统地图自测](/10-assessments/01-system-map-check)。
6. 如果发现问题，再跳到 [Issues](https://github.com/wdkang123/ai-infra-handbook/issues) 反馈。

这样读者先有学习路线，再进入 GitHub 协作，会比直接看源码轻松很多。

## 准备贡献的人怎么走

如果你准备贡献：

1. 先读 [贡献指南](https://github.com/wdkang123/ai-infra-handbook/blob/main/CONTRIBUTING.md)。
2. 根据 [Issue 分类与标签策略](/08-publication/09-issue-triage-and-labels) 选择任务类型。
3. 从 [首批公开 Issues 草稿](/08-publication/11-first-public-issues) 或 [自动生成首发运营包](/08-publication/13-generated-launch-pack) 里挑一个小任务。
4. 开 PR 前按 [验证矩阵](/09-reference/07-validation-matrix) 选择验证命令。
5. 在 PR 描述里写清楚文档影响、学习影响、验证命令和输出证据。

贡献不一定要从代码开始。这个项目很适合这些贡献：

- 改进某个章节解释
- 给 lab 增加失败路径
- 补一个案例复盘
- 改进 API/CLI 参考页
- 增加自测题或答案讲解
- 补一条生产迁移注意事项
- 修复文档内链或错字
- 增加 smoke 覆盖

对公开学习站来说，好的解释和好的复盘同样重要。

## GitHub Profile 区块怎么用

站点里加入维护者 GitHub 信息时，不需要写成个人简历。
更好的方式是把它当成公开协作入口：

- Profile 链接帮助读者确认维护者身份和其他公开项目。
- Repository 链接帮助读者回到源码、README、issue templates 和历史提交。
- Issues / PR 链接帮助读者把问题转成可追踪任务。
- Actions 链接帮助读者看到公开验证记录。

首页和本页都可以放这些入口，但要避免重复成“链接墙”。
读者在首页看到的是项目可信度和行动入口；在这页看到的是协作路径和使用规则。

## 可以提什么 Issue

首批最适合提这些问题：

- 新手不知道从哪里开始
- 某条命令在本地跑不通
- 某个输出字段看不懂
- 某个 lab 的验收标准不清楚
- 某个案例缺少失败路径或复盘解释
- 某个生产迁移方向需要更具体的例子
- 某个自测题缺少参考答案
- 某个章节读完之后仍然无法连接到代码

Issue 最好包含：

- 你读到哪一页
- 你跑了什么命令
- 你看到什么输出
- 你期望看到什么解释
- 你是否愿意补一个 PR

这样维护者能更快判断问题类型。

### 一个好的 Issue 示例

```text
标题：Serving 可观测性 Lab 中 events timeline 的观察点不够清楚

页面：/07-hands-on-labs/01-serving-observability-lab
我跑的命令：curl -s http://localhost:8000/events/requests/req_lab_serving_json_1
我看到的输出：能看到 request_started 和 request_success，但不确定每个字段代表哪一层
我期望补充：解释 timeline 里 model、status、duration、event_type 的含义
我愿意贡献：可以补一段字段说明和一个复盘模板
```

这个 issue 有页面、命令、输出、困惑和可贡献方向，维护者很容易判断它是不是文档缺口。

## 不应该贴什么

不要在公开 issue 中贴：

- 真实 API key
- 私有 endpoint
- 账号信息
- 带敏感 header 的日志
- 个人本机路径
- 公司内部模型名或业务数据
- 没脱敏的请求样本

如果是安全问题，请先读 [Security Policy](https://github.com/wdkang123/ai-infra-handbook/blob/main/SECURITY.md)。

公开项目的协作质量，很大程度取决于大家是否能保留足够上下文，同时避免泄露敏感信息。

## 网站里的 GitHub 入口

现在网站里有几类 GitHub 入口：

- 顶部导航的 `GitHub` 会直接跳到仓库。
- 右上角 GitHub 图标会直接跳到仓库。
- 首页 `GitHub` 区块会列出 profile、repo、Issues、PR、Actions 和 Pages。
- 文档页底部会出现 `在 GitHub 编辑此页`，方便读者直接跳到对应 Markdown 文件发起修改。
- 发布与协作章节会指向 issue templates、PR template、release playbook 和维护节奏。

这些入口的目的不是堆链接，而是让读者能从学习、反馈、贡献、发布检查之间自然切换。

## 维护者视角

公开仓库的核心维护节奏可以这样理解：

1. 用学习站承接阅读和自学。
2. 用 Issues 承接问题、卡点和路线图任务。
3. 用 PR 承接具体改动。
4. 用 Actions 保证 CI、文档站和发布前检查不漂移。
5. 用 Pages 承接最终在线阅读体验。
6. 用 release notes 和 launch pack 记录公开迭代。

这样网站和 GitHub 不是两套分散入口，而是一条完整的公开学习链路。

## 从反馈到 PR 的路径

一个很健康的协作路径是：

```text
读者卡住
  -> 提 learning question issue
  -> 维护者确认是否是文档缺口
  -> 转成 roadmap task 或 good first issue
  -> 贡献者提交 PR
  -> Actions 验证
  -> Pages 更新
  -> Changelog 记录变化
```

这个流程能避免“反馈散在聊天里”，也能让公开项目积累真实学习证据。

## PR 前检查

提交 PR 前，至少确认：

- 这次改动属于文档、脚本、项目代码还是发布配置
- 按 [验证矩阵](/09-reference/07-validation-matrix) 跑了对应命令
- 没有真实密钥、私有 endpoint 或个人路径
- 如果改了教程，内链没有断
- 如果改了 API/CLI，参考页同步更新
- 如果改了输出产物，证据库或 artifacts 索引同步更新
- PR 描述里写清楚验证结果

如果准备公网发布，优先跑：

```bash
PYTHON=.venv/bin/python make public-check
```

### 一个好的 PR 描述示例

```text
## 改动
- 扩写 Serving 可观测性 Lab 的事件观察点
- 增加 request timeline 复盘模板

## 学习影响
- 读者能区分 metrics 和 events 的作用
- 读者能把 x-request-id 串到 request timeline

## 验证
- PYTHON=.venv/bin/python make docs-quality
- npm run docs:build

## 安全检查
- 没有新增密钥、私有 endpoint 或个人路径
```

PR 描述的目标不是写得很长，而是让维护者能快速判断：改了什么、为什么改、怎么验证、是否适合公开。

## GitHub Actions 怎么看

Actions 页面主要看两类 workflow：

- `ci`
- `docs-pages`

`ci` 说明项目检查、测试和质量门禁是否通过。

`docs-pages` 说明文档站是否能构建并发布到 GitHub Pages。

如果 Actions 失败，不要只看红叉。要点开失败 job，找到：

- 哪条命令失败
- 是测试失败、构建失败、依赖失败还是权限失败
- 是否和本次改动有关
- 本地是否能复现

相关页面：

- [验证矩阵](/09-reference/07-validation-matrix)
- [常见排障手册](/09-reference/04-troubleshooting)
- [GitHub Pages 发布](/08-publication/01-github-pages)

## 适合首批贡献的任务

如果你想帮忙，但不知道从哪里开始，可以优先考虑：

| 类型 | 示例 |
| --- | --- |
| 文档解释 | 把某个短章节补成带场景、机制、误区的教程 |
| 输出证据 | 给某个命令补 sample output 和解释 |
| Lab 改进 | 给 lab 增加失败路径和验收标准 |
| 自测题 | 增加题目、参考答案或评分标准 |
| 案例复盘 | 把一次真实排障写成 case study |
| 迁移说明 | 补某个真实工具接入时的边界和风险 |
| 安全卫生 | 改进公开仓库检查和脱敏说明 |

这类任务通常比大规模重构更适合公开协作。

## 常见误区

### 误区一：GitHub 入口只是外链集合

不是。它应该把学习、反馈、贡献、验证和发布连接起来。

### 误区二：只有代码贡献才有价值

对学习站来说，解释、案例、证据、测试和排障路径同样重要。

### 误区三：Issue 写得越短越好

太短会缺上下文。好的 issue 应该包含页面、命令、输出、预期和是否愿意贡献。

### 误区四：Actions 失败只要重跑

不要急着重跑。先判断失败类型和是否与本次改动有关。

### 误区五：公开仓库可以先发再慢慢查安全

公开前必须查。密钥、私有 endpoint、个人路径和敏感日志一旦上传，后续处理成本会很高。
