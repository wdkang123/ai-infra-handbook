# 自动生成共学包

这一页说明如何生成 workshop packet。

前面几层自动产物分别解决不同问题：

- [学习站清单生成器](/09-reference/08-learning-inventory)：盘点站点章节、页面和课程主线
- [课程目录生成器](/09-reference/10-course-catalog)：把主线整理成可带练模块
- [自动生成证据包](/13-output-gallery/07-generated-evidence-packet)：汇总本轮 smoke 的运行证据
- [发布摘要生成器](/09-reference/09-release-brief)：判断当前是否适合公开展示

`scripts/build_workshop_packet.py` 会把课程目录和发布摘要合成一份共学包，面向讲师、带练者、学习小组组织者和准备公开分享的人。

如果你还需要把每个模块转成测评题、证据要求和评分标准，可以继续生成 [自动生成测评包](/10-assessments/06-generated-assessment-pack)。
如果你还需要把测评薄弱点和发布反馈转成首批 GitHub issue，可以继续生成 [自动生成路线图包](/08-publication/05-generated-roadmap-pack)。
如果你准备创建第一个 release 或首批 issue，可以继续生成 [自动生成首发运营包](/08-publication/13-generated-launch-pack)。

它回答的是：

> 如果要真的带别人学，这一轮该怎么安排议程、怎么拆模块、怎么要求学习者交付、怎么收集复盘问题？

## 生成命令

推荐在已经跑过 smoke 和发布摘要后运行：

```bash
PYTHON=.venv/bin/python make workshop-packet
```

默认输出：

```text
.tmp/workshop/workshop_packet.json
.tmp/workshop/workshop_packet.md
```

`make workshop-packet` 会先确保这些产物存在：

```text
.tmp/course-catalog/course_catalog.json
.tmp/release/release_brief.json
```

并以 strict 模式检查：

- 课程目录存在且 `ready_for_workshop` 为 `True`
- 发布摘要存在且 `release_readiness` 为 `ready`
- 发布摘要里的 `ready_for_public_review` 为 `True`
- 课程目录没有缺路由或缺主线

## JSON 结构

`workshop_packet.json` 的顶层结构是：

```text
report_type
generated_at
source_files
summary
validation
facilitation_principles
agenda_templates
module_cards
learner_deliverables
facilitator_checklist
recommended_commands
review_questions
```

重点字段：

| 字段 | 含义 | 用法 |
| --- | --- | --- |
| `summary.packet_readiness` | `ready` 或 `review` | 判断是否适合公开带练 |
| `agenda_templates` | 90 分钟、半天、两周三种议程 | 直接用于共学安排 |
| `module_cards` | 每个课程模块的学习卡片 | 分组学习、讲师备忘和学习者任务 |
| `learner_deliverables` | 学习者应该交付什么 | 避免共学只听不做 |
| `facilitator_checklist` | 讲师课前课后检查项 | 帮助公开分享保持稳定质量 |
| `review_questions` | 课后复盘问题 | 把反馈转成 issue、PR 或下一轮任务 |

## Markdown 结构

`workshop_packet.md` 更适合人读，可以直接放进：

- 共学活动 issue
- 公开分享准备稿
- PR 复盘说明
- 学习小组任务说明
- 讲师个人备忘

它包含：

- `Validation`：课程目录和发布摘要是否可用
- `Facilitation Principles`：带练时要保持的原则
- `Agenda Templates`：三种活动节奏
- `Module Cards`：每个模块的学习序列、任务、证据要求和讨论问题
- `Learner Deliverables`：学习者最小交付
- `Facilitator Checklist`：讲师检查项
- `Recommended Commands`：生成和发布前推荐命令
- `Review Questions`：课后复盘问题

## 三种默认议程

### 90 分钟快速共学

适合第一次线上分享或小范围试讲。

重点不是讲完整站，而是让学习者：

1. 理解项目定位
2. 选择一个模块
3. 看一份证据
4. 做一次短复盘
5. 留下一个后续问题

### 半天模块深挖

适合已经能本地运行，希望理解系统边界的学习小组。

可以把人分成 serving、gateway、eval、training 几组，每组完成：

- 一个核心问题
- 一个 lab 或证据页
- 一份输出解释
- 一个失败路径
- 一个后续 issue

### 两周共学节奏

适合准备持续共学、写系列文章或公开维护 GitHub 项目。

它把学习拆成：

1. 从 0 到 1 和系统地图
2. serving 与 gateway
3. eval 与 training
4. 案例、证据库和 capstone
5. 发布、共学包、发布摘要和反馈计划

## 模块卡片怎么用

每张模块卡片都会包含：

- 模块受众
- 学习目标
- 入口页面
- 学习序列
- 学习者任务
- 证据要求
- 讨论问题
- 讲师提示

使用方式：

1. 讲师从 `module_cards` 里选 1 到 2 个模块
2. 学习者按 `learning_sequence` 阅读入口和核心页
3. 学习者按 `learner_tasks` 跑命令或阅读产物
4. 学习者按 `evidence_expectations` 解释证据
5. 小组用 `discussion_prompts` 做复盘
6. 讲师把问题整理成 issue 或下一轮任务

## 和发布检查的关系

公开发布前可以跑：

```bash
PYTHON=.venv/bin/python make infra-release
```

现在它会覆盖：

```text
infra-format
docs-inventory
course-catalog
infra-check
infra-smoke
infra-evidence
release-brief
workshop-packet
assessment-pack
roadmap-pack
```

这意味着项目不只是“能构建、能测试、能生成证据”，还会检查：

- 课程是否能被组织成模块
- 共学包是否能生成
- 发布摘要是否允许公开带练
- 讲师是否能拿到一份结构化备忘
- 学习者是否能拿到模块题目、证据要求和评分标准
- 维护者是否能拿到首批 GitHub issue 种子和验收命令

## 和其他产物的关系

| 产物 | 回答的问题 | 适合谁看 |
| --- | --- | --- |
| `learning_inventory.md` | 站点有哪些页面和主线 | 维护者、新贡献者 |
| `course_catalog.md` | 内容如何组织成课程模块 | 讲师、学习者 |
| `evidence_packet.md` | 本轮运行留下了哪些证据 | 工程读者、PR reviewer |
| `release_brief.md` | 当前是否适合公开展示 | 发布者、维护者 |
| `workshop_packet.md` | 这次共学如何组织和复盘 | 讲师、组织者、学习小组 |
| `assessment_pack.md` | 每个模块怎么测、怎么评分 | 学习者、讲师、reviewer |
| `roadmap_pack.md` | 哪些改进可以变成 GitHub issue | 维护者、贡献者 |
| `launch_pack.md` | release notes、starter issues 和发布后检查表是否一致 | 发布者、维护者 |

这样，项目的公开学习闭环就更完整了：

1. 内容可盘点
2. 课程可分发
3. 证据可复盘
4. 发布可判断
5. 共学可执行
6. 测评可落地
7. 首发可复核
7. 路线图 issue 可创建
