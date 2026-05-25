# 课程目录生成器

这一页说明如何生成面向共学、公开分享和课程维护的 course catalog。

[学习站清单生成器](/09-reference/08-learning-inventory) 会回答：

> 这个站点一共有多少页面、多少章节、哪些页面属于哪条学习主线？

`scripts/build_course_catalog.py` 会进一步回答：

> 如果要把这些内容变成一套可带练的课程，每个学习模块应该如何组织入口、核心阅读、实验、自测、证据和迁移讨论？

它适合在这些场景使用：

- 准备把项目发到 GitHub，需要给读者一个清楚的课程目录
- 准备组织学习小组，需要给讲师和学习者分配路线
- 准备做公开演示，需要说明每个模块的学习目标和验收方式
- 新增了大量文档，需要检查课程主线是否还清晰

## 生成命令

在仓库根目录运行：

```bash
PYTHON=.venv/bin/python make course-catalog
```

默认输出：

```text
.tmp/course-catalog/course_catalog.json
.tmp/course-catalog/course_catalog.md
```

`make course-catalog` 会先运行：

```text
make docs-inventory
```

然后以 strict 模式生成课程目录。  
如果课程目录里登记的页面不存在，或者学习清单里缺少对应主线，命令会失败。

## JSON 结构

`course_catalog.json` 的顶层结构是：

```text
report_type
generated_at
source_inventory
summary
validation
program_outcomes
modules
recommended_commands
maintenance_notes
```

重点字段：

| 字段 | 含义 | 用法 |
| --- | --- | --- |
| `summary.module_count` | 课程模块数量 | 判断公开课程是否覆盖主要读者目标 |
| `summary.unique_route_count` | 课程目录覆盖的唯一页面数 | 判断核心课程入口是否足够聚焦 |
| `summary.estimated_study_blocks` | 估算学习块数量 | 帮助安排共学节奏 |
| `summary.ready_for_workshop` | 是否适合用于共学带练 | 发布或带练前的自动门禁 |
| `validation.missing_routes` | 课程目录缺失页面 | strict 模式必须为空 |
| `validation.missing_track_ids` | 学习清单缺失主线 | strict 模式必须为空 |
| `modules` | 每个学习模块的课程结构 | README、工作坊、公开演示和 PR 复盘都可以引用 |

## 课程模块

当前课程目录内置 7 个模块：

| 模块 | 适合谁 | 典型入口 | 验收重点 |
| --- | --- | --- | --- |
| 从 0 到 1 学习模块 | 第一次系统学习 AI Infra 的读者 | [从 0 到 1 学习路径](/00-overview/00-zero-to-one) | 能跑完第一轮本地实操并画出系统分层 |
| 推理服务工程模块 | 关注 token、streaming、metrics 的工程读者 | [推理服务总览](/02-inference-serving/00-overview) | 能用 request id、events 和 metrics 解释一次推理请求 |
| 平台治理工程模块 | 关注 gateway、鉴权、fallback、限流的读者 | [AI Gateway Platform](/03-ai-gateway-platform/00-overview) | 能复盘鉴权、路由、上游失败和 fallback 证据 |
| 评测发布判断模块 | 关注 run、compare、leaderboard、发布门禁的读者 | [评测与可观测性](/04-evaluation-observability/00-overview) | 能说明分数、样本分析和发布建议之间的关系 |
| 训练资产复现模块 | 关注 dataset、checkpoint、export、manifest 的读者 | [微调与训练](/05-finetuning-training/00-overview) | 能从训练输入追到导出产物并解释 lineage |
| 公开分享与共学模块 | 准备发 GitHub、带学习小组或公开展示的人 | [共学与公开分享套件](/14-workshop-kit/00-overview) | 能用课程目录、证据包和发布摘要组织复盘 |
| 生产迁移思维模块 | 想理解学习型系统如何继续变真实的人 | [生产迁移路线总览](/12-production-migration/00-overview) | 能识别接口、观测、数据和运维差距 |

每个模块会被拆成若干组：

- `建立地图`：先理解这条路线解决什么问题
- `核心阅读`：建立概念、边界和系统视角
- `运行与观察`：把本地命令跑起来并观察输出
- `动手练习`：进入 hands-on lab
- `证据输出`：知道哪些产物可以用于复盘
- `自测与答辩`：验证自己是否真的理解
- `公开分享`：面向 GitHub、学习小组和 PR review
- `生产迁移`：理解学习型实现和真实系统的差距

## Markdown 结构

`course_catalog.md` 更适合直接阅读或贴到 issue / PR：

- `Validation`：课程目录是否缺页面或缺主线
- `Program Outcomes`：整套课程希望读者最终具备什么能力
- `Modules`：每个模块的受众、目标、入口、页面组、检查点和讲师提示
- `Recommended Commands`：生成和发布前推荐命令
- `Maintenance Notes`：新增页面或主线后应该同步维护什么

## 什么时候使用

### 做公开课程介绍时

先运行：

```bash
PYTHON=.venv/bin/python make course-catalog
```

然后打开：

```text
.tmp/course-catalog/course_catalog.md
```

重点看：

- `Ready for workshop` 是否为 `True`
- 每个模块的 `Entry` 是否仍然是最适合新读者进入的页面
- 每个模块是否都有实验、自测或证据输出
- `Facilitator notes` 是否适合当前分享场景

### 做 GitHub 首发前

建议顺序：

```bash
PYTHON=.venv/bin/python make course-catalog
PYTHON=.venv/bin/python make release-brief
PYTHON=.venv/bin/python make workshop-packet
PYTHON=.venv/bin/python make assessment-pack
PYTHON=.venv/bin/python make roadmap-pack
PYTHON=.venv/bin/python make infra-release
```

这样可以同时确认：

- 课程目录完整
- 学习站清单完整
- 运行证据完整
- 发布摘要可用
- 共学包可用
- 测评包可用
- 路线图包可用

### 新增章节或大改学习路径时

如果新增的是普通参考页，只需要加入 VitePress sidebar 并运行 `make docs-quality`。

如果新增的是主线关键页，还应该：

1. 更新 `scripts/build_learning_inventory.py` 的 `COURSE_TRACKS`
2. 更新 `scripts/build_course_catalog.py` 的 `CATALOG_MODULES`
3. 运行 `make docs-inventory`
4. 运行 `make course-catalog`
5. 运行 `make docs-quality`

## 和其他自动产物的关系

| 产物 | 回答的问题 | 更适合谁看 |
| --- | --- | --- |
| `learning_inventory.md` | 学习站有哪些页面、章节和主线 | 维护者、新贡献者 |
| `course_catalog.md` | 这些内容如何组织成可带练课程 | 讲师、学习者、分享者 |
| `evidence_packet.md` | 本轮 smoke 跑出了哪些运行证据 | 工程读者、PR reviewer |
| `release_brief.md` | 当前是否适合公开发布或演示 | 发布者、维护者 |
| `workshop_packet.md` | 这次共学如何安排议程、模块、交付和复盘 | 讲师、组织者、学习小组 |
| `assessment_pack.md` | 每个模块如何出题、举证和评分 | 学习者、讲师、reviewer |
| `roadmap_pack.md` | 哪些改进可以变成首批 issue | 维护者、贡献者 |

七者合起来之后，这个项目的公开学习闭环会更完整：

1. 课程结构可盘点
2. 学习模块可分发
3. 运行证据可复盘
4. 发布状态可判断
5. 共学活动可执行
6. 模块测评可落地
7. 路线图 issue 可创建

这也是后续把项目传到 GitHub 时最值得保留的维护节奏。
