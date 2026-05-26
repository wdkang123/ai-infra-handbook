# 自动生成测评包

这一页说明如何生成 assessment pack。

前面的自动产物已经能回答：

- [课程目录生成器](/09-reference/10-course-catalog)：课程模块怎么拆
- [自动生成共学包](/14-workshop-kit/07-generated-workshop-packet)：共学活动怎么组织

`scripts/build_assessment_pack.py` 会继续把课程目录和共学包合成一份模块测评包，面向学习者自测、讲师带练、PR reviewer 和准备公开展示的人。

它回答的是：

> 每个模块应该问什么题、怎么要求证据、怎么按 Level 1 到 Level 4 评分？

## 生成命令

推荐在已经生成课程目录和共学包后运行：

```bash
PYTHON=.venv/bin/python make assessment-pack
```

默认输出：

```text
.tmp/assessment/assessment_pack.json
.tmp/assessment/assessment_pack.md
```

`make assessment-pack` 会先确保这些产物存在：

```text
.tmp/course-catalog/course_catalog.json
.tmp/workshop/workshop_packet.json
```

并以 strict 模式检查：

- 课程目录存在且 `ready_for_workshop` 为 `True`
- 共学包存在且 `packet_readiness` 为 `ready`
- 共学包里的 `ready_for_public_workshop` 为 `True`
- 课程目录和共学包的模块数量一致
- 课程目录没有缺路由或缺主线

## JSON 结构

`assessment_pack.json` 的顶层结构是：

```text
report_type
generated_at
source_files
summary
validation
assessment_principles
module_assessments
capstone_review
recommended_commands
facilitator_review_flow
```

重点字段：

| 字段 | 含义 | 用法 |
| --- | --- | --- |
| `summary.assessment_readiness` | `ready` 或 `review` | 判断是否适合公开测评 |
| `module_assessments` | 每个模块的题目、任务、证据和 rubric | 用于自测、带练和 PR 复盘 |
| `capstone_review` | 跨模块答辩要求 | 用于最终展示或公开讲解 |
| `facilitator_review_flow` | 讲师测评流程 | 帮助把答题结果转成后续任务 |

## 每个模块包含什么

每个 `module_assessments` 条目都会包含：

- `questions`：诊断题、边界题、检查点题、实操题、证据题和迁移题
- `practice_tasks`：学习者应该完成的最小实践任务
- `evidence_requirements`：回答必须引用哪些证据或指出哪些证据边界
- `rubric`：Level 1 到 Level 4 的评分标准
- `facilitator_prompts`：讲师追问，用来发现浅层理解

## 四级评分怎么用

测评包沿用学习站的四级标准：

| 等级 | 含义 | 常见表现 |
| --- | --- | --- |
| Level 1 | 能复述 | 能说关键词，但说不清边界或失败路径 |
| Level 2 | 能运行 | 能找到入口并跑基础命令，但证据解释还浅 |
| Level 3 | 能复盘 | 能解释正常路径、失败路径和证据意义 |
| Level 4 | 能改进 | 能提出小而清楚的改进，并说明风险和验证 |

公开分享前，建议至少让核心模块达到 Level 3。  
如果某个模块长期停在 Level 1 或 Level 2，说明这部分文档、lab 或示例输出还需要继续补。

## 和自测页面的关系

手写自测页更适合深入讲解固定主题：

- [系统地图自测](/10-assessments/01-system-map-check)
- [Serving 与 Gateway 自测](/10-assessments/02-serving-gateway-quiz)
- [Eval 与 Finetune 自测](/10-assessments/03-eval-finetune-quiz)
- [Capstone 答辩稿](/10-assessments/04-capstone-defense)
- [参考答案与讲解](/10-assessments/05-answer-key)

自动测评包更适合把当前课程目录里的 7 个模块全部转成可分发任务。  
当课程目录发生变化时，重新运行 `make assessment-pack`，就能看到新模块是否也有可测问题、证据要求和评分标准。

如果要把 Level 1/2 的共性问题继续拆成 GitHub issue，可以在测评包生成后运行：

```bash
PYTHON=.venv/bin/python make roadmap-pack
PYTHON=.venv/bin/python make launch-pack
```

[自动生成路线图包](/08-publication/05-generated-roadmap-pack) 会把模块题目、证据要求和发布摘要合成 issue 种子，方便把薄弱点回流到 FAQ、lab、证据库或迁移指南。
[自动生成首发运营包](/08-publication/13-generated-launch-pack) 会继续把路线图 issue 种子整理成 starter issues，并统一 release notes、默认标签和发布后检查表。

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
launch-pack
```

这意味着发布前不仅检查“能不能构建、能不能跑、能不能带练”，还会检查：

- 每个模块是否能形成测评题
- 每个模块是否有证据要求
- 每个模块是否能按 Level 1 到 Level 4 评分
- Capstone 是否能把多个模块合成一次系统答辩

## 和其他产物的关系

| 产物 | 回答的问题 | 适合谁看 |
| --- | --- | --- |
| `course_catalog.md` | 内容如何组织成课程模块 | 讲师、学习者 |
| `workshop_packet.md` | 共学如何组织和复盘 | 讲师、组织者 |
| `assessment_pack.md` | 每个模块怎么测、怎么评分 | 学习者、讲师、reviewer |
| `release_brief.md` | 当前是否适合公开展示 | 发布者、维护者 |
| `roadmap_pack.md` | 哪些改进可以变成 GitHub issue | 维护者、贡献者 |
| `launch_pack.md` | release notes、starter issues 和发布后检查表是否一致 | 发布者、维护者 |

这样学习闭环就多了一层“测得出来”：

1. 内容可盘点
2. 课程可分发
3. 共学可执行
4. 证据可复盘
5. 测评可落地
6. 反馈可变成 issue
7. 首发材料可复核
