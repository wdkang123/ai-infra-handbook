# GitHub 入口与协作地图

这页把网站和 GitHub 仓库之间的入口集中放在一起。
读者可以先在学习站按路线学习，也可以跳到 GitHub 看源码、提 issue、提交 PR 或查看自动检查状态。

## 公开入口

| 入口 | 链接 | 适合做什么 |
| --- | --- | --- |
| GitHub Profile | [wdkang123](https://github.com/wdkang123) | 查看维护者公开主页和其他项目 |
| Repository | [wdkang123/ai-infra-handbook](https://github.com/wdkang123/ai-infra-handbook) | 查看源码、README、提交记录和仓库文件 |
| Online Site | [AI Infra Handbook](https://wdkang123.github.io/ai-infra-handbook/) | 直接打开在线学习站 |
| Issues | [GitHub Issues](https://github.com/wdkang123/ai-infra-handbook/issues) | 提学习问题、反馈卡点、认领文档或路线图任务 |
| Pull Requests | [GitHub Pull Requests](https://github.com/wdkang123/ai-infra-handbook/pulls) | 提交文档、lab、案例、脚本或代码改进 |
| Actions | [GitHub Actions](https://github.com/wdkang123/ai-infra-handbook/actions) | 查看 CI、Pages 构建和发布验证记录 |

## 推荐跳转方式

如果你是第一次来：

1. 先读 [从 0 到 1 学习路径](/00-overview/00-zero-to-one)。
2. 跑完 [第一次实操演练](/00-overview/04-first-walkthrough)。
3. 对照 [示例输出与证据库](/13-output-gallery/00-overview) 判断结果。
4. 如果发现问题，再跳到 [Issues](https://github.com/wdkang123/ai-infra-handbook/issues) 反馈。

如果你准备贡献：

1. 先读 [贡献指南](https://github.com/wdkang123/ai-infra-handbook/blob/main/CONTRIBUTING.md)。
2. 根据 [Issue 分类与标签策略](/08-publication/09-issue-triage-and-labels) 选择任务类型。
3. 从 [首批公开 Issues 草稿](/08-publication/11-first-public-issues) 或 [自动生成首发运营包](/08-publication/13-generated-launch-pack) 里挑一个小任务。
4. 开 PR 前按 [验证矩阵](/09-reference/07-validation-matrix) 选择验证命令。

## 可以提什么 issue

首批最适合提这些问题：

- 新手不知道从哪里开始
- 某条命令在本地跑不通
- 某个输出字段看不懂
- 某个 lab 的验收标准不清楚
- 某个案例缺少失败路径或复盘解释
- 某个生产迁移方向需要更具体的例子

不要在公开 issue 中贴真实 API key、私有 endpoint、账号信息、带敏感 header 的日志或个人本机路径。
如果是安全问题，请先读 [Security Policy](https://github.com/wdkang123/ai-infra-handbook/blob/main/SECURITY.md)。

## 网站里的 GitHub 入口

现在网站里有三类 GitHub 入口：

- 顶部导航的 `GitHub` 会直接跳到仓库。
- 右上角 GitHub 图标会直接跳到仓库。
- 首页 `GitHub` 区块会列出 profile、repo、Issues、PR、Actions 和 Pages。

另外，文档页底部会出现 `在 GitHub 编辑此页`，方便读者直接跳到对应 Markdown 文件发起修改。

## 维护者视角

公开仓库的核心维护节奏可以这样理解：

1. 用学习站承接阅读和自学。
2. 用 Issues 承接问题、卡点和路线图任务。
3. 用 PR 承接具体改动。
4. 用 Actions 保证 CI、文档站和发布前检查不漂移。
5. 用 Pages 承接最终在线阅读体验。

这样网站和 GitHub 不是两套分散入口，而是一条完整的公开学习链路。
