# Contributing

感谢你愿意改进这个 AI Infra 学习项目。

参与前请先阅读 [Code of Conduct](./CODE_OF_CONDUCT.md)。  
如果你要报告安全相关问题，请按 [Security Policy](./SECURITY.md) 的方式处理，不要在公开 issue 中贴真实密钥或敏感日志。

这个仓库的目标不是追求最大功能集合，而是帮助学习者在一个小而完整的系统里理解 AI Infra 的核心分层：

- inference-service：执行层
- ai-gateway：治理层
- eval-module：质量闭环层
- finetune-demo：训练资产层
- docs：学习网站、实战 lab、输出证据和共学套件

## 优先欢迎的贡献

最欢迎这些类型：

- 修正文档中容易误导初学者的表达
- 给概念页补对应代码入口
- 给项目页补失败路径、测试路径或观察点
- 给示例输出页补脱敏输出、字段解释和复盘提示
- 改进证据包生成器或自动证据汇总流程
- 改进学习站清单生成器、课程主线或内容盘点流程
- 改进课程目录生成器、学习模块、检查点或带练提示
- 改进发布摘要生成器或公开发布前门禁
- 改进共学包生成器、议程模板、模块卡片或学习者交付要求
- 改进测评包生成器、模块题目、证据要求或 rubric
- 改进路线图包生成器、issue 种子、推荐 label 或验收命令
- 给共学套件补学习者工作簿、带练议程或贡献任务
- 新增可独立完成的 hands-on lab
- 给已有行为补测试
- 把学习型 mock 实现替换成更真实但仍然可读的实现

暂时不建议这些类型：

- 一次性引入过重基础设施
- 为了“像生产系统”牺牲学习可读性
- 大范围重排文档目录但没有迁移导航
- 加入无法在本地或 CI 验证的功能

## 本地验证

第一次开发前：

```bash
PYTHON=.venv/bin/python make infra-dev-install
npm install
```

常规检查：

```bash
PYTHON=.venv/bin/python make infra-format
PYTHON=.venv/bin/python make public-check
```

`public-check` 会先扫描候选入库文件中的密钥、私钥、连接串、本机路径、个人痕迹和危险文件类型，再运行主要 lint、测试和文档站构建。

如果只改文档、导航或首页入口，也可以先跑更轻量的文档质量检查：

```bash
PYTHON=.venv/bin/python make docs-quality
```

改到跨服务链路时，再跑：

```bash
PYTHON=.venv/bin/python make infra-smoke
```

如果要整理本轮 smoke 输出或在 PR 里贴复盘证据，再跑：

```bash
PYTHON=.venv/bin/python make infra-evidence
```

如果改了课程结构、学习路径、首页入口或准备公开发布，再跑：

```bash
PYTHON=.venv/bin/python make docs-inventory
PYTHON=.venv/bin/python make course-catalog
```

如果改了发布流程、证据链路或准备贴 PR 复盘材料，再跑：

```bash
PYTHON=.venv/bin/python make release-brief
```

如果改了课程目录、发布摘要、共学套件或准备组织公开带练，再跑：

```bash
PYTHON=.venv/bin/python make workshop-packet
```

如果改了测评、自测、课程模块或准备做 PR review，再跑：

```bash
PYTHON=.venv/bin/python make assessment-pack
```

如果改了公开路线图、issue 种子或准备发布到 GitHub，再跑：

```bash
PYTHON=.venv/bin/python make roadmap-pack
```

如果改了 `tasks/` 或 `prompts/`，请额外确认其中没有个人路径、真实账号、私有 endpoint、真实 key、敏感日志或未脱敏研究材料。

## 文档贡献标准

新增或修改文档时，请尽量包含：

- 这页解决什么困惑
- 应该先读哪些前置内容
- 对应哪些代码文件
- 读者应该观察什么
- 学完后应该能回答什么问题

如果新增页面，请同步更新：

- `docs/.vitepress/config.mts`
- 相关 overview 页面
- 必要时更新 `README.md`
- 必要时更新 `scripts/build_learning_inventory.py` 里的课程主线
- 必要时更新 `scripts/build_course_catalog.py` 里的课程模块
- 必要时更新 `scripts/build_workshop_packet.py` 里的议程、模块卡片或交付要求
- 必要时更新 `scripts/build_assessment_pack.py` 里的题目、证据要求或评分标准
- 必要时更新 `scripts/build_roadmap_pack.py` 里的 issue 种子、label 或验收命令

并运行 `make docs-inventory`、`make course-catalog`、`make workshop-packet`、`make assessment-pack`、`make roadmap-pack` 和 `make docs-quality`，确认课程主线、课程模块、共学材料、测评材料、路线图 issue 种子、内链、heading 锚点、H1 结构、VitePress nav/sidebar 路由、首页配置与 Vue 组件链接和首页文档页统计没有漂移。

如果你不确定一类内容应该怎么写，可以先看：

- [内容写作规范](./docs/08-publication/02-content-style-guide.md)
- [示例输出与证据库](./docs/13-output-gallery/00-overview.md)
- [贡献者协作手册](./docs/14-workshop-kit/05-contribution-playbook.md)

## 代码贡献标准

新增代码时，请尽量保持：

- 行为边界清楚
- 测试覆盖失败路径
- 文档同步说明
- 不引入不必要的抽象
- 不破坏 `infra-check` 和 `infra-smoke`

如果改到用户可见行为，例如 API 返回、metrics、manifest、CLI 参数，请同时更新对应项目页。

## Pull Request 建议

一个好的 PR 通常包含：

- 为什么要改
- 改了什么
- 如何验证
- 是否影响学习路径或文档导航

如果只是修 typo，也可以保持很小的 PR。

## 发布相关文件

这个仓库已经提供了一组公开协作文件：

- `LICENSE`：MIT License
- `CODE_OF_CONDUCT.md`：讨论和协作行为准则
- `CHANGELOG.md`：面向学习者和贡献者的变化记录
- `PUBLICATION_CHECKLIST.md`：发布到 GitHub 前的检查清单
- `.github/ISSUE_TEMPLATE/evidence-example.yml`：收集脱敏输出和证据解释
- `.github/ISSUE_TEMPLATE/workshop-feedback.yml`：收集共学和公开演示反馈

如果你的贡献改变了学习路径、公开发布方式或重要项目行为，请同步更新这些文件中受影响的部分。

## 设计原则

这个项目最看重三件事：

1. 可学习：读者能看懂为什么这样设计
2. 可运行：命令能跑，结果能验证
3. 可迁移：学到的分层直觉能带到真实系统

只要贡献能加强这三点，就很适合这个仓库。
