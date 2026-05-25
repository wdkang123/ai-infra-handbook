# GitHub 发布计划

这页把“上传到 GitHub”拆成可执行的发布计划。

真正重要的不是第一次 push，而是让第一次来的读者、未来贡献者和你自己都能持续判断：这个项目现在能做什么，下一步该做什么。

## 发布前一周

发布前先完成这些检查：

| 检查项 | 目标 |
| --- | --- |
| README | 1 分钟内能说明项目定位、启动方式、学习路线 |
| 文档站 | 首页、nav、sidebar、搜索都能正常使用 |
| 质量命令 | `infra-check` 和 `infra-smoke` 能通过 |
| 发布清单 | [Publication Checklist](/08-publication/00-overview) 中关键项可解释 |
| 贡献入口 | CONTRIBUTING、issue template、PR template 已准备 |
| 安全检查 | 没有真实密钥、私有 endpoint、敏感日志 |
| 路线图 | 读者知道当前是学习型项目，也知道后续方向 |

推荐命令：

```bash
nvm use 22
npm install
PYTHON=.venv/bin/python make infra-format
PYTHON=.venv/bin/python make public-check
PYTHON=.venv/bin/python make docs-inventory
PYTHON=.venv/bin/python make course-catalog
PYTHON=.venv/bin/python make infra-smoke
PYTHON=.venv/bin/python make release-brief
PYTHON=.venv/bin/python make workshop-packet
PYTHON=.venv/bin/python make assessment-pack
PYTHON=.venv/bin/python make roadmap-pack
npm audit --omit=dev --audit-level=moderate
```

## 首发 README 应该回答什么

首发 README 不需要把所有内容讲完，但必须回答：

1. 这个项目是什么
2. 它适合谁
3. 它不是生产平台
4. 怎么启动文档站
5. 怎么跑质量检查
6. 从哪里开始学
7. 有哪些可运行项目
8. 怎么贡献或反馈

当前 README 已经覆盖这些方向，后续可以在真正部署线上站点后增加站点链接。

## GitHub 仓库设置建议

推荐设置：

| 设置 | 建议 |
| --- | --- |
| Description | AI Infra learning manual with runnable scaffolds |
| Website | GitHub Pages 或其他静态站地址 |
| Topics | `ai-infra`, `llm`, `inference`, `gateway`, `evaluation`, `finetuning`, `vitepress` |
| Issues | 开启 |
| Discussions | 如果准备做共学，可以开启 |
| Wiki | 暂时不需要，避免内容分散 |
| Projects | 可选，用于路线图 |
| Branch protection | 对 main 开启 PR 和 CI 要求 |

如果暂时只有你一个人维护，也建议保留 PR 流程，因为它会迫使每次改动写清楚验证结果。

## 首批 issue 建议

发布后可以预先放几类 issue，帮助读者理解贡献方向：

| Label | Issue 示例 |
| --- | --- |
| `good first issue` | 给某个 lab 增加常见失败说明 |
| `documentation` | 补充某个概念页的前置知识链接 |
| `evidence` | 给输出证据库增加一组实际运行截图或摘录 |
| `case-study` | 增加一个 gateway fallback 复盘案例 |
| `help wanted` | 改进 GitHub Pages 部署说明 |
| `question` | 收集学习者最常问的问题 |

注意：issue 应该小而清楚。不要开“完善文档”这种没有边界的任务。

## 首发后 30 天

| 时间 | 重点 | 具体动作 |
| --- | --- | --- |
| 第 1 到 3 天 | 确认可访问 | 检查 README、Pages、CI、链接 |
| 第 4 到 7 天 | 收第一批反馈 | 记录最常见的安装和阅读卡点 |
| 第 8 到 14 天 | 修学习路径 | 优先改首页、路线、runbook、FAQ |
| 第 15 到 21 天 | 补证据和案例 | 把反馈最多的输出做成证据页 |
| 第 22 到 30 天 | 整理路线图 | 把大想法拆成小 issue |

30 天内不要急着大改架构。公开学习项目早期最有价值的是把第一批读者的卡点转成稳定入口。

## 版本节奏

可以采用轻量版本节奏：

| 版本 | 目标 |
| --- | --- |
| `v0.1` | 文档站和最小可运行闭环可用 |
| `v0.2` | labs、assessments、case studies 更完整 |
| `v0.3` | 输出证据、共学模板、贡献流程完整 |
| `v0.4` | 引入更真实的后端或训练接入示例 |
| `v1.0` | 能稳定支撑公开课程或系列文章 |

版本号只是沟通工具，不要为了版本号本身增加复杂流程。

## 发布公告模板

```text
AI Infra Manual 发布了一个学习型版本。

它不是生产平台，而是一套能边学边跑的 AI Infra 学习站：

- 文档站：从总览、运行手册到两周学习计划
- 可运行项目：inference-service、ai-gateway、eval-module、finetune-demo
- 深度实战：Serving、Gateway、Eval、Finetune、Capstone
- 输出证据：跑完命令后知道该看什么
- 课程目录：按模块拆分共学、实验、自测和复盘
- 共学包：议程模板、模块卡片、学习者交付和复盘问题
- 测评包：模块题目、证据要求、rubric 和 Capstone review
- 路线图包：GitHub issue 种子、推荐 label、验收标准和验证命令
- 共学套件：带练、工作簿、复盘模板、贡献手册

适合想系统理解 LLM serving、gateway、eval、finetune 工程边界的人。
```

## 长期维护原则

1. 先稳定学习路径，再增加新技术名词
2. 每个新增能力都要有输出证据
3. 每个新增页面都要能被导航找到
4. 每个公开承诺都要能被本地命令验证
5. 不把学习型实现包装成生产能力

## 发布前最后一遍检查

发布前请跑：

```bash
PYTHON=.venv/bin/python make docs-inventory
PYTHON=.venv/bin/python make course-catalog
PYTHON=.venv/bin/python make public-check
PYTHON=.venv/bin/python make infra-smoke
PYTHON=.venv/bin/python make release-brief
PYTHON=.venv/bin/python make workshop-packet
PYTHON=.venv/bin/python make assessment-pack
PYTHON=.venv/bin/python make roadmap-pack
npm audit --omit=dev --audit-level=moderate
```

然后人工看一遍：

- [首页](/)
- [从 0 到 1 学习路径](/00-overview/00-zero-to-one)
- [示例输出与证据库](/13-output-gallery/00-overview)
- [学习站清单生成器](/09-reference/08-learning-inventory)
- [课程目录生成器](/09-reference/10-course-catalog)
- [发布摘要生成器](/09-reference/09-release-brief)
- [自动生成共学包](/14-workshop-kit/07-generated-workshop-packet)
- [自动生成测评包](/10-assessments/06-generated-assessment-pack)
- [自动生成路线图包](/08-publication/05-generated-roadmap-pack)
- [共学与公开分享套件](/14-workshop-kit/00-overview)
- [公开发布总览](/08-publication/00-overview)

这些入口能跑顺，首发体验就不会散。
