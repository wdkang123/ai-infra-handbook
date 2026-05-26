# 自动生成测评包

这一页说明如何生成 assessment pack。

前面的自动产物已经能回答：

- [课程目录生成器](/09-reference/10-course-catalog)：课程模块怎么拆
- [自动生成共学包](/14-workshop-kit/07-generated-workshop-packet)：共学活动怎么组织

`scripts/build_assessment_pack.py` 会继续把课程目录和共学包合成一份模块测评包，面向学习者自测、讲师带练、PR reviewer 和准备公开展示的人。

它回答的是：

> 每个模块应该问什么题、怎么要求证据、怎么按 Level 1 到 Level 4 评分？

## 为什么需要自动测评包

手写自测页适合深入讲一个主题，但公开学习站会持续变化：新增页面、调整模块、补充 lab、更新证据库。只靠人工维护题目，很容易出现“课程已经变了，测评还停在旧结构”的问题。

自动测评包的价值是把当前课程目录和共学包重新扫描一遍，生成一份和当前内容同步的测评视图。它帮助维护者确认：

- 每个模块是否都有可回答的问题。
- 每个模块是否有实践任务。
- 每个模块是否要求引用证据。
- Level 1 到 Level 4 是否能区分浅层理解和工程理解。
- Capstone 是否能把模块串起来。

它不是替代讲师，而是给讲师、学习者和 reviewer 一个统一评审底稿。

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

如果这些 strict 条件失败，不建议绕过。测评包依赖课程目录和共学包；上游结构不稳定时，生成出来的题目也很可能不可靠。

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

## Markdown 怎么读

`assessment_pack.md` 更适合人读。建议按这个顺序看：

1. 先看 summary，确认 readiness。
2. 看 assessment principles，确认评分口径。
3. 按模块看 questions 和 practice tasks。
4. 看 evidence requirements，确认题目是否要求引用证据。
5. 看 rubric，确认 Level 3/4 是否足够明确。
6. 最后看 capstone review，确认最终答辩是否覆盖跨模块能力。

如果你只看题目，不看 evidence requirements 和 rubric，就会把测评包误用成普通问答清单。

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

## 三种使用场景

### 自学复盘

学习者可以用它回答：

```text
这个模块我能答哪些题？
哪些题我只能背概念？
哪些题我能引用证据？
我离 Level 3 还差什么？
```

自学时不需要一次完成所有模块。最推荐的是每学完一个模块，就从测评包里挑 2 到 3 道题写短复盘。

### 讲师带练

讲师可以用它设计活动：

```text
开场问题：
实操任务：
证据要求：
追问：
评分标准：
活动后 issue：
```

这样带练不只是“讲一遍”，而是能把学习者回答转成反馈和后续任务。

### PR / 内容评审

Reviewer 可以用它判断一批文档改动是否真正提升学习质量：

- 新模块是否有题可问。
- 新页面是否能支持证据要求。
- 新 lab 是否能让 Level 2 走向 Level 3。
- 新案例是否能帮助 Capstone 答辩。

如果文档变长了，但测评包里仍然没有更清楚的题目和 evidence requirements，说明内容可能只是扩写，没有真正提升验收能力。

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

## 从评分结果回流到改进

测评包真正有价值的地方，是把“学得不够深”转成具体改进。

| 发现 | 可能改进 |
| --- | --- |
| 很多人停在 Level 1 | overview 需要补场景和边界 |
| 很多人停在 Level 2 | lab 需要补观察点和验收标准 |
| 证据题答不好 | output gallery 需要补字段解释 |
| Capstone 讲不连贯 | 系统地图和案例复盘需要补 |
| 讲师追问经常卡住 | FAQ 或 answer key 需要补 |

所以不要把测评包只当成结果。它更像一面镜子，帮你看下一批内容应该加厚哪里。

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

## 常见误区

### 把测评包当考试卷

它不是为了筛人，而是为了暴露学习断点。答不出来的题目，应该回流到文档、lab、案例和证据库。

### 只看 questions，不看 evidence requirements

AI Infra 学习不能只靠口头解释。好的回答应该能指向命令、代码、header、events、JSON、manifest 或 history。

### Level 4 只看“说得更详细”

Level 4 的关键不是篇幅，而是能提出改进方案，并说明风险和验证方式。

### 生成一次后就不更新

课程结构变化后应该重新生成测评包。否则测评会和当前学习站脱节。
