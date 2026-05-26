# 发布摘要生成器

这一页说明如何生成公开发布前的 release brief。

项目现在已经有两类自动产物：

- [学习站清单](/09-reference/08-learning-inventory)：回答“这个网站有哪些内容，适合怎么学”
- [课程目录](/09-reference/10-course-catalog)：回答“这些内容如何组织成可带练模块”
- [自动生成证据包](/13-output-gallery/07-generated-evidence-packet)：回答“这轮 smoke 跑出了哪些工程证据”
- [自动生成路线图包](/08-publication/05-generated-roadmap-pack)：回答“哪些后续改进可以变成首批 GitHub issue”
- [自动生成首发运营包](/08-publication/13-generated-launch-pack)：回答“release notes、starter issues、默认标签和发布后检查表是否一致”

`scripts/build_release_brief.py` 会把它们合成一份发布摘要，方便你在 GitHub 首发、PR 复盘、公开演示或共学带练前快速确认：

- 学习站结构是否完整
- 课程主线是否缺路由
- 端到端证据是否齐全
- eval 发布建议是什么
- finetune export 是否成功
- 当前项目应该如何被公开定位

## 它解决的真实问题

公开学习项目很容易出现四种漂移：

- 文档页越来越多，但主线不清楚
- smoke 能跑，但读者不知道这些输出证明了什么
- release notes 写得很好，但和实际验证结果脱节
- 共学和公开演示依赖个人记忆，而不是结构化证据

release brief 的作用是把这些材料收束成一次“发布前体检”。它不是替你做判断，而是把判断所需的信号放在同一份报告里。

阅读 release brief 时，可以按这个顺序：

1. 先看 `summary.release_readiness`
2. 再看 `validation.ready_for_public_review`
3. 然后看缺路由、缺证据、eval recommendation 和 export status
4. 最后读 `Public Positioning` 和 `Next Review Questions`

如果第一屏已经是 `review`，不要急着改 release notes，先回到缺失的上游产物。

## 生成命令

推荐先跑完整链路：

```bash
PYTHON=.venv/bin/python make infra-smoke
PYTHON=.venv/bin/python make release-brief
```

默认输出：

```text
.tmp/release/release_brief.json
.tmp/release/release_brief.md
```

`make release-brief` 会先生成：

```text
.tmp/docs-inventory/learning_inventory.json
.tmp/evidence/evidence_packet.json
```

然后以 strict 模式合成 release brief。  
如果课程主线缺路由、证据包缺关键产物，或者证据包没有完整的 serving / eval / finetune 三段，命令会失败。

## 一键发布前检查

如果你想跑更完整的本地发布检查，可以用：

```bash
PYTHON=.venv/bin/python make infra-release
```

这个目标会依次运行：

```text
infra-format
docs-inventory
infra-check
infra-smoke
infra-evidence
release-brief
```

它适合发布前最后一轮，不适合每次小改都跑。

## ready 和 review 怎么理解

`ready` 的含义是：自动检查没有发现阻断公开复盘的问题。
它不等于“内容已经完美”，也不等于“生产可用”。

`review` 的含义是：至少有一个关键输入不满足发布前门禁，需要人工回到上游修复或解释。

常见情况：

| 状态 | 应该怎么做 |
| --- | --- |
| `ready` + 内容刚大改 | 继续人工读 README、首页、核心章节和 release notes |
| `ready` + eval recommendation 不理想 | 在公开叙事里说明这是学习演示，不把结果包装成生产批准 |
| `review` + missing route | 回到 nav/sidebar 或课程目录修路由 |
| `review` + missing evidence | 重新跑 smoke/evidence，或修证据生成脚本 |
| `review` + public positioning 不准确 | 修改文档定位，避免生产化误导 |

release brief 更像仪表盘，不是盖章机。真正发布前仍然需要人读一遍关键入口。

## JSON 结构

`release_brief.json` 的顶层结构是：

```text
report_type
generated_at
source_files
summary
learning_site
runtime_evidence
validation
public_positioning
recommended_commands
next_review_questions
```

重点字段：

| 字段 | 含义 |
| --- | --- |
| `summary.release_readiness` | `ready` 或 `review` |
| `summary.docs_pages` | 当前文档页数量 |
| `summary.course_tracks` | 当前课程主线数量 |
| `summary.missing_track_routes` | 学习主线缺失路由数量 |
| `summary.evidence_sections` | 证据包可用章节数量 |
| `summary.missing_evidence_artifacts` | 缺失证据产物数量 |
| `summary.eval_release_recommendation` | eval comparison 给出的发布建议 |
| `summary.finetune_export_status` | finetune export 状态 |
| `validation.ready_for_public_review` | 是否满足公开复盘的最低自动门禁 |

## Markdown 结构

`release_brief.md` 更适合直接阅读：

- `Public Positioning`：公开定位，避免把学习项目说成生产平台
- `Validation`：自动门禁信号
- `Learning Site`：章节、主线和学习材料统计
- `Runtime Evidence`：serving、eval、finetune 关键运行证据
- `Recommended Commands`：发布前推荐命令
- `Next Review Questions`：公开前最后一轮人工复盘问题

## 什么时候使用

### GitHub 首发前

建议顺序：

```bash
nvm use 22
PYTHON=.venv/bin/python make infra-release
npm audit --omit=dev --audit-level=moderate
```

然后打开：

```text
.tmp/release/release_brief.md
```

重点看：

- `Release readiness` 是否为 `ready`
- `missing_track_route_count` 是否为 0
- `missing_evidence_artifact_count` 是否为 0
- `Eval release recommendation` 是否符合你的展示叙事
- `Public Positioning` 是否仍然准确

### PR 复盘时

如果某个 PR 改了学习路径、证据生成、smoke 或发布流程，可以在 PR 里贴：

```text
.tmp/release/release_brief.md
```

它比单独贴一堆命令输出更容易说明：

- 改动影响了哪些学习主线
- 运行证据是否仍然完整
- 是否还有需要人工 review 的发布边界

### 共学带练前

带练者可以先读 release brief，再安排议程：

- 用 `Learning Site` 判断当天应该走哪条主线
- 用 `Runtime Evidence` 选择展示哪些输出
- 用 `Next Review Questions` 组织讨论
- 如果要直接安排学习活动，再运行 `make workshop-packet`
- 如果要做模块测评或 PR review，再运行 `make assessment-pack`
- 如果要整理首批路线图 issue，再运行 `make roadmap-pack`
- 如果要写第一个 GitHub release，再运行 `make launch-pack`，并对照 [v0.1 首发发布手册](/08-publication/10-v0-1-release-playbook)

## 常见失败和修复方向

### 学习主线缺路由

现象通常是 `missing_track_routes` 大于 0。

优先检查：

- 新增页面是否真实存在
- VitePress sidebar 是否包含该页面
- 文档链接路径是否和文件路径一致
- 页面是否缺少标题或被误放到错误目录

修复后先跑：

```bash
PYTHON=.venv/bin/python make docs-quality
PYTHON=.venv/bin/python make release-brief
```

### 证据包缺关键产物

如果 release brief 提示 evidence artifact 缺失，先不要改报告脚本。优先确认 smoke 是否真的生成了对应文件。

常见原因：

- 没有先运行 `make infra-smoke`
- `.tmp/` 被清理后直接运行 release brief
- 某个子项目输出路径改变，但 evidence collector 没同步
- eval 或 finetune 阶段失败，被后续报告吞掉了上下文

### eval recommendation 与叙事冲突

如果 eval 给出的 recommendation 不适合“发布候选”，公开表达要诚实：

```text
当前 eval 证据用于学习如何做模型比较和发布判断，
不代表真实生产模型已经获批上线。
```

不要为了让 release notes 更好看而改 recommendation。应该改的是数据、比较策略、阈值，或者公开叙事。

### export status 不成功

finetune export 失败时，要回到资产链：

```text
dataset_summary -> run_manifest -> checkpoint_index -> export_manifest
```

缺哪一环，就先修哪一环。release brief 只负责暴露问题，不负责替训练流程补产物。

## 和其他产物的关系

| 产物 | 回答的问题 | 适合谁看 |
| --- | --- | --- |
| `learning_inventory.md` | 学习站有哪些章节和路线 | 维护者、带练者、新贡献者 |
| `course_catalog.md` | 课程模块如何组织入口、练习、自测和证据 | 讲师、学习者、分享者 |
| `evidence_packet.md` | 本轮 smoke 跑出了哪些证据 | 工程读者、PR reviewer |
| `release_brief.md` | 当前是否适合公开展示或发布 | 发布者、维护者、带练者 |
| `workshop_packet.md` | 共学活动如何组织、交付和复盘 | 讲师、组织者、学习小组 |
| `assessment_pack.md` | 模块如何测评、举证和评分 | 学习者、讲师、reviewer |
| `roadmap_pack.md` | 哪些改进可以变成 GitHub issue | 维护者、贡献者 |
| `launch_pack.md` | release notes、starter issues、默认标签和发布后检查表是否一致 | 发布者、维护者 |

这些产物一起使用时，项目就有了比较完整的公开复盘链路：

1. 课程结构可盘点
2. 学习模块可分发
3. 运行结果可追溯
4. 发布状态可判断
5. 共学活动可执行
6. 模块测评可落地
7. 路线图 issue 可创建
8. 首发运营包可复核

## 可以复制到 PR 的摘要模板

当 PR 改动影响文档站、生成脚本、证据链或公开发布流程时，可以在 PR 描述里贴一个简版 release brief 摘要：

```text
Release brief:
- readiness:
- docs pages:
- missing track routes:
- missing evidence artifacts:
- eval recommendation:
- finetune export:
- ready for public review:

Verification:
- PYTHON=.venv/bin/python make docs-quality
- PYTHON=.venv/bin/python make release-brief
```

这样 reviewer 不需要在大量命令输出里找重点。

## 不要过度解读

release brief 不能证明：

- 站点内容已经足够深入
- 所有读者都能看懂
- 生产迁移已经完成
- 模型效果真实优于其他方案
- 开源发布没有任何安全风险

它能证明的是：当前自动化链路已经把学习站、课程主线、运行证据和公开定位放到同一份摘要里，方便人做最后判断。
