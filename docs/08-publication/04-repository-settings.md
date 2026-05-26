# GitHub 仓库设置建议

这页用于你第一次把仓库推到 GitHub 后做设置。  
它关注 GitHub 仓库页面本身，而不是本地代码。

## 设置优先级

第一次公开仓库时，不需要把 GitHub 所有开关一次开满。更稳妥的顺序是：

1. 先保证仓库描述、README、许可证、Pages 和 CI 能让读者正常进入。
2. 再配置 issue template、labels、Dependabot 和基础分支保护。
3. 等外部贡献变多后，再逐步加强 review、required checks 和贡献规范。

这个项目的目标是公开学习和共学，不是把规则堆到贡献者进不来。好的设置应该让读者更容易信任项目，也让维护者更容易守住质量底线。

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

About 区域还建议打开：

- Releases：用于 v0.1.0 这种阶段性发布
- Packages：默认不用，除非后续真的发布包
- Discussions：初期可以先不开，避免维护分散；有稳定社群后再考虑
- Wikis：建议关闭，知识应优先沉淀在 `docs/`
- Projects：如果开始公开路线图，可以开一个轻量项目板

Topics 不只是装饰。它会影响别人搜索和理解仓库定位，所以建议使用学习、AI Infra、VitePress、Python、hands-on 等准确标签，不要使用会暗示生产 SaaS 或托管平台的标签。

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

README 第一屏可以按这个顺序组织：

1. 一句话说明项目定位
2. 在线文档站入口
3. 本地运行最短路径
4. 内容地图或学习路径
5. 质量检查命令
6. 贡献和安全入口

如果 README 顶部塞满徽章、内部背景和过长愿景，第一次来的读者反而会不知道该点哪里。

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

如果第一次推送发生在 Pages source 设置完成之前，可能会看到 `build` job 成功、`deploy` job 失败。

这通常不是文档构建问题；在 Pages source 改成 `GitHub Actions` 后，重新运行 `docs-pages` workflow，或推送一次文档相关提交即可重新部署。

### Pages 发布节奏

Pages 会在推送到默认分支并命中文档相关路径时自动发布。
这对公开仓库是正常行为，但本地高频修改时不建议每改一点就推远端。

推荐节奏：

- 本地批量扩写、调样式、跑 `docs:build` 和 `docs-quality`
- 本地预览确认核心页面没有明显问题
- 攒成一个清晰版本后再提交和推送
- Pages 自动部署后只做线上验收，不把线上部署当调试工具

这样 GitHub Actions 历史会更干净，读者看到的站点也更稳定。

## 4. Branch Protection

等仓库稳定后，可以给默认分支添加保护规则。

建议最小规则：

- Require pull request before merging
- Require status checks to pass
- Require conversation resolution before merging

初期不需要一下子打开太多限制。  
这个仓库仍是学习项目，规则应该帮助维护质量，而不是挡住轻量贡献。

可以分三档推进：

| 阶段 | 建议规则 |
| --- | --- |
| 个人维护期 | 允许直接 push，但每次推送前本地跑 `public-check` |
| 公开协作初期 | 要求 PR、CI 通过、conversation resolved |
| 多贡献者阶段 | 增加 required review、限制 force push、保护 release 分支 |

如果你仍在大量本地打磨内容，可以先不把规则开得太重；准备接受外部贡献时再开启强一点的保护。

## 5. Dependabot

仓库已经提供 `.github/dependabot.yml`，覆盖：

- npm
- pip
- GitHub Actions

建议保留 weekly 节奏。这个项目不是生产服务，不需要过度频繁更新依赖；但公开仓库应该能及时看到文档站、Python 开发依赖和 CI action 的版本提醒。

处理 Dependabot PR 时建议看三件事：

- 它更新的是 npm、pip 还是 GitHub Actions
- CI 是否通过
- 更新是否影响 VitePress 构建、Python 检查或 Pages 部署

如果暂时不想合并，可以关闭或延后，但不要把“有 bot PR”理解成项目出问题。公开仓库收到依赖更新提醒是正常现象。

## 6. Issue 分类

当前仓库已经有七类 issue template：

- Bug report
- Docs improvement
- Hands-on lab idea
- Evidence example
- Workshop feedback
- Learning question
- Roadmap task

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

模板默认只引用 GitHub 默认 labels，避免新仓库因为不存在的 `evidence`、`feedback`、`lab` 等标签产生提示。等你真正创建这些自定义 labels 后，可以再手动补到 issue 或模板里。更完整的分类口径见 [Issue 分类与标签策略](/08-publication/09-issue-triage-and-labels)。

## 7. 首批公开 issue

第一次公开后，可以创建几条路线图 issue。  
它们不一定马上做，但能告诉读者项目欢迎什么贡献。

更推荐的做法是先运行：

```bash
PYTHON=.venv/bin/python make roadmap-pack
PYTHON=.venv/bin/python make launch-pack
```

然后从 [自动生成路线图包](/08-publication/05-generated-roadmap-pack) 或 [自动生成首发运营包](/08-publication/13-generated-launch-pack) 里挑选首批 5 到 8 条。这样每条 issue 都能带上学习价值、建议文件、验收标准和验证命令，并且首批标签默认不会引用新仓库里还不存在的自定义 labels。

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

## 8. Security 设置

公开仓库建议开启这些安全能力：

- Dependabot alerts
- Dependabot security updates
- Secret scanning alerts（如果账号/仓库权限支持）
- Private vulnerability reporting（如果后续接受外部安全反馈）

安全入口应该说明：

- 不要在公开 issue 贴密钥、token 或真实日志
- 安全问题优先通过 Security policy 或私下渠道报告
- 学习项目不处理真实用户数据
- 示例凭证必须是 placeholder

本地仍然要继续跑 `make public-check`。GitHub 的安全提醒是线上兜底，不应该替代本地检查。

## 9. Release 建议

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
如果需要更完整的 release notes 模板和发布后 24 小时检查清单，继续看 [v0.1 首发发布手册](/08-publication/10-v0-1-release-playbook)。

## 首发后 24 小时检查

仓库第一次公开后，建议在 24 小时内检查：

- README 顶部链接能打开
- Pages 首页返回 200
- Actions 没有持续失败
- Dependabot PR 是否需要处理
- issue template 是否能正常创建
- About Website 是否指向正确文档站
- 首批 issue 是否足够清楚
- 没有读者误解项目是生产平台

如果发现问题，优先修 README、首页、Pages、公开卫生和首批 issue。它们是新读者最先接触的入口。
