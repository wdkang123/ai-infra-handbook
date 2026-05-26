# 自动生成路线图包

这一页说明如何用自动生成的 roadmap pack，把发布摘要和测评结果整理成 GitHub-ready issue 种子。

公开学习项目最容易卡在这里：

- README 和文档已经能看，但第一批 issue 太宽
- 路线图写了方向，但没有拆成可贡献的小任务
- 测评发现了薄弱点，但没有回流到 FAQ、lab、证据库或迁移指南
- 发布后想收反馈，却不知道哪些任务适合 good first issue

`scripts/build_roadmap_pack.py` 会读取 release brief 和 assessment pack，生成一份 JSON / Markdown 路线图包。它的目标不是替你自动创建 GitHub issue，而是把首批 issue 所需的标题、学习价值、范围、建议文件、验收标准、验证命令和 label 先整理好。

如果你准备进入真正的 GitHub 首发阶段，可以再运行 [自动生成首发运营包](/08-publication/13-generated-launch-pack)。
它会读取 roadmap pack，把 issue 种子整理成 starter issues，并把自定义标签规范化为新仓库默认可用的 GitHub labels。

## 它解决的真实维护问题

公开仓库最怕两种路线图：

- 太宏大：比如“完善评测系统”“接入真实训练”
- 太碎片：比如只有几十个没有学习价值的 TODO

roadmap pack 的目标是在中间找平衡：

```text
学习价值清楚
范围足够小
建议文件明确
验收标准能检查
验证命令能运行
```

这会让路线图更适合 GitHub 协作，而不是只适合维护者自己看。

## 生成命令

在仓库根目录运行：

```bash
PYTHON=.venv/bin/python make roadmap-pack
```

默认输出：

```text
.tmp/roadmap/roadmap_pack.json
.tmp/roadmap/roadmap_pack.md
```

`make roadmap-pack` 会先确保这些产物存在：

```text
.tmp/release/release_brief.json
.tmp/assessment/assessment_pack.json
```

并以 strict 模式检查：

- release brief 存在且 `release_readiness` 为 `ready`
- release brief 的 `ready_for_public_review` 为 `True`
- assessment pack 存在且 `assessment_readiness` 为 `ready`
- assessment pack 的 `ready_for_assessment` 为 `True`
- assessment pack 至少有一个模块和一个题目

如果其中任一项不满足，命令会失败。这能避免把“还不能公开复盘”的材料包装成路线图。

## 生成后先看什么

打开 `.tmp/roadmap/roadmap_pack.md` 后，建议先看：

1. `Validation`：是否 ready。
2. `Roadmap Principles`：是否仍然保持学习项目边界。
3. `Issue Seeds`：任务是否足够小。
4. `Recommended Labels`：是否能映射到现有 GitHub labels。
5. `Publication Flow`：首发后如何使用。

如果 issue seed 看起来像“大项目”，不要直接创建。先拆小，或者放到 public roadmap 作为长期方向。

## JSON 结构

`roadmap_pack.json` 的顶层结构是：

```text
report_type
generated_at
source_files
summary
validation
roadmap_principles
issue_seeds
recommended_labels
recommended_commands
publication_flow
```

重点字段：

| 字段 | 含义 | 用法 |
| --- | --- | --- |
| `summary.roadmap_readiness` | `ready` 或 `review` | 判断是否适合整理首批公开 issue |
| `summary.issue_seed_count` | issue 种子总数 | 判断首批任务池是否足够 |
| `summary.module_issue_count` | 从测评模块生成的深挖 issue 数量 | 把学习薄弱点回流到文档和 lab |
| `summary.launch_issue_count` | 横向发布任务数量 | 覆盖 FAQ、证据库、迁移指南和发布运营 |
| `validation.ready_for_public_roadmap` | 是否通过路线图门禁 | 公开前的自动信号 |
| `issue_seeds` | 可复制到 GitHub 的 issue 草稿 | 首批 good first issue、docs、lab、evidence 任务来源 |
| `recommended_labels` | 推荐 label 列表 | 对齐 GitHub 仓库设置 |
| `publication_flow` | 首发后如何使用 issue 种子 | 指导 30 天反馈闭环 |

## Issue 种子包含什么

每条 `issue_seeds` 都会包含：

- `title`：适合直接作为 GitHub issue 标题
- `labels`：推荐 label
- `priority`：P0、P1 或 P2
- `source_module`：来自哪个学习模块或 cross-cutting 任务
- `learning_value`：为什么这个任务能帮助学习者
- `scope`：本次任务应该做什么
- `suggested_files`：优先查看或修改的文件
- `acceptance_criteria`：合并前应该满足什么
- `verification_commands`：应该跑哪些命令

这比“完善文档”“补充案例”更适合公开协作，因为读者能立刻看见任务边界。

## 默认会生成哪些方向

路线图包会为每个测评模块生成一个深挖 issue，例如：

- 从 0 到 1 学习模块继续补具体例子和证据解释
- 推理服务工程模块继续补请求链路、metrics 或失败路径
- 平台治理工程模块继续补鉴权、路由、fallback 或事件复盘
- 评测发布判断模块继续补 sample analysis 或发布门禁说明
- 训练资产复现模块继续补 checkpoint、manifest 和 lineage 解释
- 公开分享与共学模块继续补共学反馈和协作入口
- 生产迁移思维模块继续补真实系统差距和迁移边界

同时也会生成一组横向发布 issue：

- 从测评薄弱点补 FAQ
- 给证据库补更多脱敏输出和字段解释
- 增加 OpenAI-compatible serving 迁移指南
- 增加最小 judge adapter 示例
- 增加 finetune resume / checkpoint selection lab
- 首发后刷新公开路线图

这些方向会随着 assessment pack 和 release brief 的状态一起变化。

## 和 GitHub issue templates 的关系

路线图包不是 issue template 的替代品。

推荐用法是：

1. 先运行 `make roadmap-pack`
2. 打开 `.tmp/roadmap/roadmap_pack.md`
3. 从中挑 5 到 8 条首批 issue
4. 用现有 issue template 填写背景、证据和复现信息
5. 保留路线图包里的 learning value、suggested files、acceptance criteria 和 verification commands

这样新贡献者看到的 issue 既有结构，也有学习价值。

## 选择首批 issue 的原则

首批公开 issue 建议满足：

- 读者不用理解全仓库也能开始
- 改动范围限定在 1 到 3 个文件
- 验收命令清楚
- 不需要真实密钥、GPU 或私有资源
- 能改善一个明确学习卡点

不建议首批 issue 做：

- 大规模目录重组
- 生产级架构迁移
- 引入重型依赖
- 需要维护者大量口头解释的任务

首批 issue 是读者对项目协作体验的第一印象。小而清楚，比大而模糊更好。

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

这意味着发布前不仅检查“能不能构建、能不能跑、能不能带练、能不能测评”，还会检查：

- 能不能把测评弱点转成 issue
- 能不能把发布后 30 天的反馈入口拆小
- 首批任务是否带有学习价值、建议文件和验收命令
- 路线图是否仍然保持学习型项目边界
- release notes、starter issues、默认标签和发布后复盘清单是否能由 launch pack 统一复核

## 和其他自动产物的关系

| 产物 | 回答的问题 | 适合谁看 |
| --- | --- | --- |
| `learning_inventory.md` | 学习站有哪些页面、章节和主线 | 维护者、新贡献者 |
| `course_catalog.md` | 内容如何组织成课程模块 | 讲师、学习者 |
| `evidence_packet.md` | 本轮 smoke 跑出了哪些证据 | 工程读者、PR reviewer |
| `release_brief.md` | 当前是否适合公开展示 | 发布者、维护者 |
| `workshop_packet.md` | 共学如何组织和复盘 | 讲师、组织者 |
| `assessment_pack.md` | 每个模块怎么测、怎么评分 | 学习者、讲师、reviewer |
| `roadmap_pack.md` | 哪些改进可以变成首批 GitHub issue | 维护者、贡献者 |
| `launch_pack.md` | release notes、starter issues、默认标签和发布后检查表是否一致 | 发布者、维护者 |

完整闭环是：

1. 内容可盘点
2. 课程可分发
3. 运行证据可复盘
4. 发布状态可判断
5. 共学活动可执行
6. 模块测评可落地
7. 路线图 issue 可创建
8. 首发运营包可复核

这样项目发到 GitHub 后，不只是“可以看”，也更容易持续接住反馈和贡献。
