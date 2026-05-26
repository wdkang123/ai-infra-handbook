# 学习站清单生成器

这一页说明如何用自动生成的学习站清单检查课程结构。

当文档越来越多时，只靠 sidebar 很难回答这些问题：

- 现在一共有多少页
- 每个章节有多少学习材料
- 哪些页面属于同一条学习主线
- 首页、实战、证据库、共学套件和发布资料是否能互相支撑
- 发到 GitHub 前，能不能快速给别人一份课程地图

`scripts/build_learning_inventory.py` 会扫描 `docs/`，把页面、章节、课程主线和维护信号汇总成 JSON / Markdown。

## 生成命令

在仓库根目录运行：

```bash
PYTHON=.venv/bin/python make docs-inventory
```

默认输出：

```text
.tmp/docs-inventory/learning_inventory.json
.tmp/docs-inventory/learning_inventory.md
```

这个目标会以 strict 模式运行。  
如果课程主线里登记的页面不存在，或者普通 Markdown 页面没有标题，命令会失败。

## JSON 结构

`learning_inventory.json` 的顶层结构是：

```text
report_type
generated_at
site
summary
quality_signals
make_targets
sections
course_tracks
```

重点字段：

| 字段 | 含义 | 用法 |
| --- | --- | --- |
| `summary.page_count` | 文档页总数 | 对齐首页统计和发布说明 |
| `summary.section_count` | 章节数量 | 判断课程结构是否继续膨胀 |
| `summary.course_track_count` | 课程主线数量 | 判断学习路径是否覆盖主要读者目标 |
| `summary.missing_track_route_count` | 主线缺失路由数量 | strict 模式应为 0 |
| `quality_signals` | labs、自测、案例、证据库、共学套件等页面数量 | 判断学习站是否只是概念文档，还是有练习和复盘材料 |
| `make_targets` | 根级 Makefile 目标 | 判断验证入口是否齐全 |
| `sections` | 按目录聚合的章节清单 | 查看每个模块的页面、链接和代码块数量 |
| `course_tracks` | 面向读者目标的学习路线 | 用于 README、共学带练和公开展示 |

## Markdown 结构

`learning_inventory.md` 更适合直接阅读或贴到 PR / issue：

- `Quality Signals`：学习体验是否完整
- `Sections`：每个章节的页数、链接数、代码块数和学习权重
- `Course Tracks`：7 条推荐学习主线
- `Section Pages`：每个页面的标题、路由和内容信号
- `Maintenance Notes`：维护时应该同步检查什么

## 课程主线

当前生成器内置 7 条主线：

| 主线 | 适合谁 | 典型入口 |
| --- | --- | --- |
| 从 0 到 1 主线 | 第一次接触 AI Infra 的读者 | [从 0 到 1 学习路径](/00-overview/00-zero-to-one) |
| 推理服务工程主线 | 想理解 token、streaming 和 metrics 的读者 | [推理服务总览](/02-inference-serving/00-overview) |
| 平台治理工程主线 | 想理解 gateway、鉴权、路由和失败语义的读者 | [AI Gateway Platform](/03-ai-gateway-platform/00-overview) |
| 评测发布判断主线 | 想理解 run、compare、leaderboard 和发布门禁的读者 | [评测与可观测性](/04-evaluation-observability/00-overview) |
| 训练资产复现主线 | 想理解 dataset、checkpoint、export 和 lineage 的读者 | [微调与训练](/05-finetuning-training/00-overview) |
| 公开分享与共学主线 | 准备发到 GitHub 或带别人学习的人 | [共学与公开分享套件](/14-workshop-kit/00-overview) |
| 生产迁移思维主线 | 想知道学习型系统如何继续变真实的人 | [生产迁移路线总览](/12-production-migration/00-overview) |

这些主线定义在 `scripts/build_learning_inventory.py` 的 `COURSE_TRACKS` 中。  
如果新增了更重要的学习路径，应该先改这里，再运行：

```bash
PYTHON=.venv/bin/python make docs-inventory
PYTHON=.venv/bin/python make docs-quality
```

## 什么时候使用

### 发布到 GitHub 前

运行：

```bash
PYTHON=.venv/bin/python make docs-inventory
PYTHON=.venv/bin/python make docs-quality
PYTHON=.venv/bin/python make infra-check
```

然后打开：

```text
.tmp/docs-inventory/learning_inventory.md
```

重点看：

- `Missing tracked routes` 是否为 0
- `Course Tracks` 是否覆盖新读者、工程读者和分享者
- `Quality Signals` 里 labs、自测、案例、证据库、共学套件是否还在
- `Sections` 是否出现明显失衡，例如某个模块只有 overview，没有深入页或练习页

### 做共学带练前

可以把 `Course Tracks` 作为选路材料：

- 新手走从 0 到 1 主线
- 工程读者按 serving / platform / eval / training 分组
- 带练者用公开分享与共学主线准备议程和工作簿
- 进阶读者用生产迁移主线讨论下一阶段

### 做内容维护时

如果新增了页面：

1. 把页面加入 VitePress sidebar
2. 如果它是主线关键页，把路由加入 `COURSE_TRACKS`
3. 更新 README 或相关 overview
4. 运行 `make docs-inventory`
5. 运行 `make docs-quality`

## 和证据包的关系

学习站清单回答的是：

> 这个学习网站有哪些内容，适合怎么走？

[自动生成证据包](/13-output-gallery/07-generated-evidence-packet) 回答的是：

> 这轮本地 smoke 到底跑出了哪些可复盘证据？

[发布摘要生成器](/09-reference/09-release-brief) 回答的是：

> 课程结构和运行证据合起来，当前是否适合公开展示？

[课程目录生成器](/09-reference/10-course-catalog) 回答的是：

> 这些页面如何组织成可以带练、可以自测、可以复盘的课程模块？

[自动生成共学包](/14-workshop-kit/07-generated-workshop-packet) 回答的是：

> 这些课程模块如何变成一次可执行、可交付、可复盘的共学活动？

[自动生成测评包](/10-assessments/06-generated-assessment-pack) 回答的是：

> 这些课程模块如何变成可以自测、可以评分、可以 PR review 的模块题目？

[自动生成路线图包](/08-publication/05-generated-roadmap-pack) 回答的是：

> 这些测评弱点和发布反馈如何变成可创建、可验收的 GitHub issue？

[自动生成首发运营包](/08-publication/13-generated-launch-pack) 回答的是：

> release notes、starter issues、默认标签和发布后检查表是否来自同一套可验证材料？

公开展示时可以一起使用：

1. 用 `learning_inventory.md` 说明课程结构
2. 用 `course_catalog.md` 说明课程模块和带练顺序
3. 用 `evidence_packet.md` 说明运行结果
4. 用 `release_brief.md` 判断发布状态
5. 用 `workshop_packet.md` 安排议程、模块、交付和复盘问题
6. 用 `assessment_pack.md` 安排模块题目、证据要求和评分标准
7. 用 `roadmap_pack.md` 整理首批 issue 种子和推荐 label
8. 用 `launch_pack.md` 复核 release notes、starter issues 和发布后检查表
9. 用 [共学与公开分享套件](/14-workshop-kit/00-overview) 组织学习者任务和反馈

这样项目就不只是“很多文档”，而是有结构、有路径、有运行证据、也有协作入口的学习站。
