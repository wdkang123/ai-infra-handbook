# GitHub 仓库设置建议

这页用于你第一次把仓库推到 GitHub 后做设置。  
它关注 GitHub 仓库页面本身，而不是本地代码。

## 1. About 区域

建议设置：

```text
Description:
AI Infra learning handbook with runnable Python scaffolds, hands-on labs, assessments, and a VitePress site.

Website:
https://wdkang123.github.io/ai-infra-handbook/

Topics:
ai-infrastructure
ai-infra
llm
inference
gateway
evaluation
finetuning
vitepress
python
learning
hands-on-labs
workshop
```

如果 Pages workflow 还没跑通，Website 可以先留空；跑通后再填上面的地址。

## 2. README 第一屏

公开前确认 README 第一屏能回答：

- 这是什么项目
- 它适合谁
- 它不是生产平台
- 从哪里开始学习
- 怎么运行本地文档站
- 怎么验证项目质量
- 使用什么许可证
- Node 版本是否由 `.nvmrc` 明确

如果读者必须翻很多屏才知道这些信息，README 还需要继续收敛。

公开仓库也应该避免把内部任务板、AI 协作提示词、临时交接文档、真实运行日志、模型权重和本机路径放进首个 commit。具体口径见 [公开仓库卫生规范](/08-publication/06-public-repo-hygiene)。

## 3. Pages 设置

进入：

```text
Settings -> Pages
```

Source 选择：

```text
GitHub Actions
```

然后到：

```text
Actions -> docs-pages -> Run workflow
```

第一次配置时手动运行一次。后续推送文档站相关改动到 `main` 或 `master` 时，workflow 也会自动发布。  
项目路径部署时，workflow 会自动设置 `VITEPRESS_BASE` 为 `/<仓库名>/`。

## 4. Branch Protection

等仓库稳定后，可以给默认分支添加保护规则。

建议最小规则：

- Require pull request before merging
- Require status checks to pass
- Require conversation resolution before merging

初期不需要一下子打开太多限制。  
这个仓库仍是学习项目，规则应该帮助维护质量，而不是挡住轻量贡献。

## 5. Dependabot

仓库已经提供 `.github/dependabot.yml`，覆盖：

- npm
- pip
- GitHub Actions

建议保留 weekly 节奏。这个项目不是生产服务，不需要过度频繁更新依赖；但公开仓库应该能及时看到文档站、Python 开发依赖和 CI action 的版本提醒。

## 6. Issue 分类

当前仓库已经有五类 issue template：

- Bug report
- Docs improvement
- Hands-on lab idea
- Evidence example
- Workshop feedback

建议在 GitHub 上配这些 labels：

| Label | 用途 |
| --- | --- |
| `bug` | 可复现问题 |
| `documentation` | 文档、学习路径、表达改进 |
| `enhancement` | 功能或学习体验增强 |
| `good first issue` | 适合第一次贡献 |
| `lab` | hands-on lab 相关任务 |
| `evidence` | 输出证据、manifest、报告样例相关任务 |
| `feedback` | 共学、公开演示和读者反馈 |
| `question` | 学习问题或设计讨论 |

## 7. 首批公开 issue

第一次公开后，可以创建几条路线图 issue。  
它们不一定马上做，但能告诉读者项目欢迎什么贡献。

更推荐的做法是先运行：

```bash
PYTHON=.venv/bin/python make roadmap-pack
```

然后从 [自动生成路线图包](/08-publication/05-generated-roadmap-pack) 里挑选首批 5 到 8 条。这样每条 issue 都能带上学习价值、建议文件、验收标准和验证命令。

建议首批 issue：

1. 补充更多 FAQ：收集第一次学习时的卡点
2. 继续补充更多真实运行截图或脱敏 sample artifact：让证据库更贴近读者机器上的输出
3. 收集第一批 workshop feedback：改进学习者工作簿、议程和公开演示脚本
4. 增加 eval judge adapter 示例：让 sample-level output 更接近真实评测
5. 增加 finetune resume / 多 checkpoint 选择示例：让训练资产链更完整
6. 增加真实 OpenAI-compatible serving 接入指南：保留 mock 路径，同时给进阶读者迁移方向

每条 issue 都建议包含：

- 学习价值
- 可能涉及的文件
- 验收命令
- 不希望引入的复杂度

## 8. Release 建议

如果你准备打第一个 release，可以用：

```text
v0.1.0-learning-site
```

Release notes 可以包含：

- VitePress 学习站
- 四个可运行学习项目
- hands-on labs
- 示例输出与证据库
- 共学与公开分享套件
- 学习自测
- 参考资料
- GitHub Pages workflow
- CI 和 smoke

发布前确认 [Publication Checklist](/08-publication/00-overview) 里的关键项已经完成。
