# 产物与文件索引

这页解释运行命令后会看到哪些文件。

学习 AI Infra 时，产物很重要。  
它们不是命令的副作用，而是系统可复盘的证据。

## Smoke 与证据包产物

目录：

```text
.tmp/smoke/
```

### serving snapshots

示例：

```text
.tmp/smoke/serving/
  inference_health.json
  gateway_health.json
  inference_models.json
  gateway_models.json
  inference_metrics.prom
  gateway_metrics.prom
  inference_events_summary.json
  gateway_events_summary.json
  gateway_failure_summary.json
  inference_request_index.json
  gateway_request_index.json
  inference_request_timeline.json
  gateway_request_timeline.json
```

含义：

- `infra-smoke` 会保存本轮服务状态、模型列表、metrics、事件摘要和 request timeline
- 这些文件是自动证据包的 serving/gateway 来源

### evidence_packet.json / .md

示例：

```text
.tmp/smoke/evidence/evidence_packet.json
.tmp/smoke/evidence/evidence_packet.md
.tmp/evidence/evidence_packet.json
.tmp/evidence/evidence_packet.md
```

含义：

- `infra-smoke` 会在 `.tmp/smoke/evidence` 里生成本轮证据包
- `make infra-evidence` 会从 `.tmp/smoke` 重新生成 `.tmp/evidence` 证据包
- JSON 适合工具读取，Markdown 适合 PR、issue、学习者工作簿和公开演示

相关页面：

- [自动生成证据包](/13-output-gallery/07-generated-evidence-packet)

## 学习站清单产物

目录：

```text
.tmp/docs-inventory/
```

示例：

```text
.tmp/docs-inventory/learning_inventory.json
.tmp/docs-inventory/learning_inventory.md
```

含义：

- `make docs-inventory` 会扫描 `docs/` 下的页面
- JSON 汇总章节、页面、课程主线、内容信号和 Makefile 目标
- Markdown 适合在 GitHub 发布、PR、共学议程或课程维护时直接阅读

相关页面：

- [学习站清单生成器](/09-reference/08-learning-inventory)

## 课程目录产物

目录：

```text
.tmp/course-catalog/
```

示例：

```text
.tmp/course-catalog/course_catalog.json
.tmp/course-catalog/course_catalog.md
```

含义：

- `make course-catalog` 会读取学习站清单
- JSON 汇总课程模块、读者目标、页面组、检查点、讲师提示和推荐命令
- Markdown 适合贴到 GitHub README、issue、共学议程或公开演示准备稿

相关页面：

- [课程目录生成器](/09-reference/10-course-catalog)

## 发布摘要产物

目录：

```text
.tmp/release/
```

示例：

```text
.tmp/release/release_brief.json
.tmp/release/release_brief.md
```

含义：

- `make release-brief` 会读取学习站清单和证据包
- JSON 汇总 release readiness、课程结构、运行证据、公开定位和推荐命令
- Markdown 适合贴到 PR、issue、GitHub 首发记录或公开演示讲稿

相关页面：

- [发布摘要生成器](/09-reference/09-release-brief)

## 共学包产物

目录：

```text
.tmp/workshop/
```

示例：

```text
.tmp/workshop/workshop_packet.json
.tmp/workshop/workshop_packet.md
```

含义：

- `make workshop-packet` 会读取课程目录和发布摘要
- JSON 汇总议程模板、模块卡片、学习者交付、讲师检查项和复盘问题
- Markdown 适合贴到共学 issue、公开分享准备稿、讲师备忘或 PR 复盘说明

相关页面：

- [自动生成共学包](/14-workshop-kit/07-generated-workshop-packet)

## 测评包产物

目录：

```text
.tmp/assessment/
```

示例：

```text
.tmp/assessment/assessment_pack.json
.tmp/assessment/assessment_pack.md
```

含义：

- `make assessment-pack` 会读取课程目录和共学包
- JSON 汇总模块题目、实操任务、证据要求、rubric、讲师追问和 Capstone review
- Markdown 适合贴到自测任务、共学 issue、PR review 或公开展示前检查

相关页面：

- [自动生成测评包](/10-assessments/06-generated-assessment-pack)

## 路线图包产物

目录：

```text
.tmp/roadmap/
```

示例：

```text
.tmp/roadmap/roadmap_pack.json
.tmp/roadmap/roadmap_pack.md
```

含义：

- `make roadmap-pack` 会读取发布摘要和测评包
- JSON 汇总路线图门禁、issue 种子、推荐 label、发布后反馈流程和推荐命令
- Markdown 适合用来创建 GitHub issue、整理首批 good first issue 或做发布后 30 天规划

相关页面：

- [自动生成路线图包](/08-publication/05-generated-roadmap-pack)

## Eval 产物

目录：

```text
projects/eval-module/results/
```

### result JSON

示例：

```text
results/mmlu_eval_result.json
```

含义：

- 一次 eval run 的结构化结果
- 包含 task、model、accuracy、metrics 等字段

相关代码：

- `projects/eval-module/src/eval_module/results/result_store.py`

### run bundle

示例：

```text
results/mmlu_eval_result/
  result.json
  raw_output.json
  sample_outputs.json
  sample_summary.json
  sample_analysis.json
  run_manifest.json
  summary.md
```

含义：

- 一次 run 的完整复盘包
- 不只保存分数，也保存 raw output 和 summary
- `sample_outputs.json` 保存少量样本级输出，帮助解释分数从哪里来
- `sample_summary.json` 汇总样本数量、通过/失败数量、平均分和 token 统计
- `sample_analysis.json` 汇总 pass rate、score buckets、failed sample ids 和 judge reason counts

### comparison JSON

示例：

```text
results/mmlu_compare.json
```

含义：

- baseline 和 candidate 的对比结果
- 包含 delta、verdict、min_delta、metric_deltas
- 包含 `release_recommendation` 和 `release_reasons`

### comparison bundle

示例：

```text
results/mmlu_compare/
  comparison.json
  comparison.md
  comparison_manifest.json
```

含义：

- 一次 compare 的复盘包
- Markdown 适合人读，JSON 适合工具读

### comparison index

示例：

```text
results/comparison_index.json
results/comparison_index.md
```

含义：

- 从 `comparison_history.jsonl` 聚合
- 汇总 baseline、candidate、delta、verdict、release recommendation、comparison file、verdict counts、recommendation counts、task summaries 和平均 delta
- 适合回看过去做过哪些发布判断

### leaderboard

示例：

```text
results/leaderboard.json
results/leaderboard.md
```

含义：

- 从 `run_history.jsonl` 指向的 run bundle 聚合
- 按 task/model/backend/few-shot 汇总 `best_accuracy`、`latest_accuracy`、`run_count`、sample summary、`best_result_file` 和 `latest_result_file`
- 额外提供 `backend_groups` 和 `fewshot_groups`，避免不同评测设置被混成一个榜单数字
- JSON 适合工具继续处理，Markdown 适合快速阅读

### run index

示例：

```text
results/run_index.json
results/run_index.md
```

含义：

- 从 `run_history.jsonl` 指向的 run bundle 聚合
- 按时间列出历史 run、accuracy、result file、artifact dir 和 sample summary
- 额外按 task 汇总 run count、best/latest accuracy 和对应 result file
- 适合先盘点历史结果，再进入 leaderboard 或 compare

### history

示例：

```text
results/run_history.jsonl
results/comparison_history.jsonl
```

含义：

- 追加式历史记录
- 用于长期观察趋势

## Finetune 产物

目录：

```text
projects/finetune-demo/outputs/
```

### trainer_state.json

含义：

- 本次训练 run 的核心状态
- 记录 method、model、dataset、epoch 等信息
- 记录 dataset version 和 dataset sha256，方便 export 阶段继续追溯输入数据

### training_args.json

含义：

- 训练参数快照
- 用于复盘 batch size、learning rate 等配置

### metrics/train_metrics.json

含义：

- 训练指标
- 当前是 mock 指标，但表达真实训练系统中的 metrics 位置

### logs/train.log

含义：

- 人类可读训练日志

### logs/events.jsonl

含义：

- 结构化事件流
- 比纯文本日志更适合后续工具读取

### data/dataset_summary.json

含义：

- 数据集摘要
- 当前记录 train file、格式、样本数、message 数、role 分布、数据集大小和 sha256
- 还记录 `dataset_version`、`dataset_registry_entry` 和平均 messages per record

重要性：

- 训练复现必须知道当时用了什么数据
- 数据版本指纹能帮助你判断两次 run 是否真的用了同一份输入

### data/dataset_registry_entry.json

含义：

- 当前训练 run 的数据登记卡
- 记录 `dataset_id`、dataset name、dataset uri、version、sha256、role_counts 和来源 run
- 适合从单次训练产物追溯到“这份数据在 registry 里叫什么”

### dataset_registry.jsonl

目录：

```text
outputs/dataset_registry.jsonl
```

含义：

- 追加式数据登记表
- 每次 train 都会追加一条 dataset registry entry
- 用于跨多次 run 观察哪些训练输入被使用过

### dataset_registry_report.json / .md

目录：

```text
outputs/dataset_registry_report.json
outputs/dataset_registry_report.md
```

含义：

- 由 `finetune_demo.main list-datasets` 读取 registry 生成
- JSON 适合工具读取，Markdown 适合人快速查看
- 汇总 `entry_count`、`dataset_count`、`registered_count`、models、last run、`method_filter`、`model_filter` 和 `duplicate_entry_count`

### dataset_registry_diff.json / .md

目录：

```text
outputs/dataset_registry_diff.json
outputs/dataset_registry_diff.md
```

含义：

- 由 `finetune_demo.main diff-datasets` 读取 registry 生成
- 比较两份 dataset registry entry 的 version、sha256、records、messages、role counts 等字段
- 帮你判断两次训练输入是否相同，以及差异具体在哪里

### checkpoint-0001/

示例：

```text
checkpoint-0001/
  adapter_config.json
  adapter_model.safetensors
  trainer_state.json
```

含义：

- 模拟 PEFT adapter checkpoint
- 是 export 的输入

### checkpoints/latest_checkpoint.json

含义：

- 指向当前最新 checkpoint
- 为 resume 或 export 提供入口

### checkpoints/checkpoint_index.json / .md

含义：

- 列出当前 run 下的 checkpoint
- 记录 checkpoint 文件、adapter sha256、文件 size/hash 和 resumable 标记
- 是后续多 checkpoint、resume 和 export 选择策略的学习入口

### run_manifest.json

含义：

- 训练 run 的产物目录说明
- 告诉读者和工具“这个 run 有哪些关键文件”

### artifacts_manifest.json

含义：

- 文件级资产清单
- 包含 path、size_bytes、sha256

重要性：

- 让产物从“目录里有文件”变成“可校验资产”

### export_manifest.json

目录：

```text
outputs/demo-export/export_manifest.json
```

含义：

- export 阶段的交付清单
- 记录 source checkpoint、base model、lineage、dataset id、dataset version、dataset sha256、输出文件和文件 hash

### run_index.json / .md

目录：

```text
outputs/run_index.json
outputs/run_index.md
```

含义：

- 由 `finetune_demo.main list-runs` 读取 `run_history.jsonl` 生成
- 汇总 method、model、dataset id、dataset version、output dir、checkpoint、`run_manifest_file`、`checkpoint_index_file`、method counts、model summaries 和 dataset summaries
- 适合从训练历史反查每次 run 的证据 manifest，再决定是否继续看 checkpoint 或 export

### export_history.jsonl

目录：

```text
outputs/export_history.jsonl
```

含义：

- 追加式导出历史
- 记录 base model、dataset id、dataset version、adapter 文件 sha256、`export_manifest_file`、导出 status 和 duration
- 用于把多次导出和对应训练输入串起来看

### export_index.json / .md

目录：

```text
outputs/export_index.json
outputs/export_index.md
```

含义：

- 由 `finetune_demo.main list-exports` 读取 export history 生成
- 汇总 output dir、export manifest、status、duration、base model、dataset id、dataset version、adapter sha256、model summaries 和 dataset summaries
- 适合从交付 adapter 反查训练输入和文件指纹

## 哪些产物不建议提交

这些目录默认在 `.gitignore` 中忽略：

```text
projects/*/outputs/
projects/*/results/
```

原因：

- 它们是运行产物
- 可能频繁变化
- 可能包含本地路径或实验信息

如果需要展示示例产物，建议单独创建脱敏后的 sample 文件，而不是提交完整 outputs。

## 产物和学习问题的对应关系

| 你想理解的问题 | 优先看 |
| --- | --- |
| 评测结果是什么 | eval result JSON |
| 一次评测如何复盘 | run bundle |
| 分数背后的样本长什么样 | sample outputs 和 judge reason |
| 样本级结果整体怎样 | sample summary、sample analysis |
| baseline/candidate 怎么判断 | comparison bundle、comparison index |
| 多个模型或多次 run 怎么横向看 | run index、leaderboard、backend/few-shot 分组、best/latest result file |
| 训练用了什么数据 | dataset summary、dataset registry、registry report、registry diff、run index、dataset_version 和 role_counts |
| 训练产物有哪些 | run manifest、checkpoint index、finetune run index |
| 文件是否可校验 | artifacts manifest |
| checkpoint 如何交付 | export manifest、export history、export index、status/duration 和 lineage |
| 跑完以后怎么整理证据 | [示例输出与证据库](/13-output-gallery/00-overview) 和 [端到端复盘证据包](/13-output-gallery/04-end-to-end-review-packet) |
