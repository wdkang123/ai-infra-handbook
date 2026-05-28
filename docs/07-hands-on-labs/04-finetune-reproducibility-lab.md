# Finetune 复现资产 Lab

## 学习目标

这个 lab 训练你理解训练工程里“产物资产化”的价值。

完成后你应该能说清楚：

- 为什么训练 run 不应该只留下 checkpoint
- dataset summary 为什么重要
- dataset role 统计为什么能帮助理解训练输入
- artifacts manifest 为什么要记录 `size_bytes` 和 `sha256`
- export 为什么应该独立于 train
- export lineage 为什么能帮助追溯训练来源
- dataset version 为什么应该从 train 传到 export
- dataset registry report 为什么要支持 method/model 过滤和重复登记统计
- run index 为什么要保留 run manifest pointer
- history 如何帮助复盘训练过程

## 前置知识

建议先读：

- [LoRA、QLoRA、PEFT](/05-finetuning-training/01-lora-qlora-peft)
- [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)
- [实验追踪、History、复现](/05-finetuning-training/06-experiment-tracking-history-reproducibility)
- [finetune-demo 项目页](/06-projects/04-finetune-demo)

## 代码入口

重点看这些文件：

- `projects/finetune-demo/src/finetune_demo/main.py`
- `projects/finetune-demo/src/finetune_demo/config.py`
- `projects/finetune-demo/src/finetune_demo/trainer/lora_trainer.py`
- `projects/finetune-demo/src/finetune_demo/dataset_registry.py`
- `projects/finetune-demo/src/finetune_demo/artifacts.py`
- `projects/finetune-demo/src/finetune_demo/export/adapter_exporter.py`
- `projects/finetune-demo/tests/test_trainer.py`

## 本 Lab 的最终交付物

完成后建议写一份“训练资产复盘”：

```text
训练 run：
dataset id / version：
dataset sha256：
checkpoint：
checkpoint index：
export：
export manifest：
export lineage 能追溯到：
我确认的文件指纹：
如果要进入 eval，还缺什么：
```

这份复盘的重点不是证明“训练命令跑了”，而是证明“训练产物可追踪、可校验、可交付”。

## 操作步骤

### 1. 跑一次训练

```bash
cd /path/to/ai-infra/projects/finetune-demo
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main train \
  --method lora \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --dataset ./data/train.jsonl \
  --output ./outputs/lab-run \
  --epochs 1
```

观察输出目录：

```text
outputs/lab-run/
  trainer_state.json
  training_args.json
  metrics/train_metrics.json
  logs/train.log
  logs/events.jsonl
  data/dataset_summary.json
  data/dataset_registry_entry.json
  checkpoints/latest_checkpoint.json
  checkpoints/checkpoint_index.json
  checkpoints/checkpoint_index.md
  checkpoint-0001/
  run_manifest.json
  artifacts_manifest.json
```

### 2. 检查 dataset summary

打开：

```bash
cat ./outputs/lab-run/data/dataset_summary.json
```

你应该看到：

- 使用的数据文件
- 数据格式
- 记录数
- message 总数
- user / assistant / system role 分布
- average messages per record
- dataset version
- dataset registry entry
- 数据集大小和 `sha256`

当前训练入口还会校验 chat-style JSONL：每条记录需要 `messages`，并包含 user 和 assistant。

你可以用下面问题检查自己是否读懂了 dataset summary：

```text
这次训练到底用了哪份数据？
这份数据有多少条记录？
user / assistant / system 的角色分布是否合理？
dataset version 是什么？
sha256 是否能帮助我确认数据没有被替换？
```

如果你只知道“用了 train.jsonl”，说明数据资产还没有被你真正读懂。

### 3. 检查 dataset registry

打开：

```bash
cat ./outputs/lab-run/data/dataset_registry_entry.json
cat ./outputs/dataset_registry.jsonl
```

观察：

- `dataset_id`
- `dataset_uri`
- `dataset_version`
- `role_counts`
- `registered_from`

`dataset_summary.json` 解释这一次 run 看到了什么数据；`dataset_registry.jsonl` 负责把多次 run 用过的数据输入登记起来。

再生成一份 registry 报告：

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-datasets \
  --registry ./outputs/dataset_registry.jsonl \
  --method lora \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --output ./outputs/dataset_registry_report.json \
  --markdown-output ./outputs/dataset_registry_report.md
```

观察：

- `dataset_registry_report.json`
- `dataset_registry_report.md`
- `entry_count`
- `dataset_count`
- `registered_count`
- `method_filter` / `model_filter`
- `duplicate_entry_count`

### 4. 比较 dataset registry 条目

先从 `dataset_registry.jsonl` 里复制一个 `dataset_id`，然后可以先比较它自己：

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main diff-datasets \
  --registry ./outputs/dataset_registry.jsonl \
  --left train@sha256:example \
  --right train@sha256:example \
  --output ./outputs/dataset_registry_diff.json \
  --markdown-output ./outputs/dataset_registry_diff.md
```

观察：

- `dataset_registry_diff.json`
- `dataset_registry_diff.md`
- `identical_dataset_sha256`
- `changed_fields`

当 left/right 是同一个 dataset id 时，diff 应该显示没有变化。后续你跑出两份不同数据后，再用它比较 version、sha256、records、messages 和 role counts。

### 5. 检查 artifacts manifest

打开：

```bash
cat ./outputs/lab-run/artifacts_manifest.json
```

观察：

- `files`
- `file_artifacts`
- 每个文件的 `size_bytes`
- 每个文件的 `sha256`

这让训练产物从“目录里有一些文件”变成“可校验的资产清单”。

再检查 checkpoint index：

```bash
cat ./outputs/lab-run/checkpoints/checkpoint_index.json
```

观察：

- `latest_checkpoint`
- `adapter_model_sha256`
- `resumable`
- `file_artifacts`

### 6. 导出 adapter

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main export \
  --checkpoint ./outputs/lab-run/checkpoint-0001 \
  --output ./outputs/lab-export
```

检查：

```bash
cat ./outputs/lab-export/export_manifest.json
```

观察 export manifest 如何记录：

- source checkpoint
- output dir
- base model
- lineage
- lineage 里的 dataset id、dataset version 和 dataset sha256
- exported files
- file artifacts

再检查 export history：

```bash
cat ./outputs/export_history.jsonl
```

观察每条记录里的 `base_model`、`dataset_id`、`dataset_version` 和 `adapter_model_sha256`。这些字段让你能从“这次导出了什么”继续追到“它来自哪份训练数据和哪个 adapter 文件”。

再生成 export index：

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-exports \
  --history ./outputs/export_history.jsonl \
  --output ./outputs/export_index.json \
  --markdown-output ./outputs/export_index.md
```

观察：

- `export_index.json`
- `export_index.md`
- `dataset_id`
- `dataset_version`
- `adapter_model_sha256`

### 7. 生成训练 run index

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-runs \
  --history ./outputs/run_history.jsonl \
  --method lora \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --output ./outputs/run_index.json \
  --markdown-output ./outputs/run_index.md
```

观察：

- `run_index.json`
- `run_index.md`
- `run_manifest_file`
- `method_counts`
- `model_summaries`
- `dataset_summaries`

## 关键观察点

### 观察点 1：训练 run 是一个资产目录

训练不是只产出权重文件。  
一次可复盘的训练至少应该留下：

- 配置
- 数据摘要
- 数据登记
- 指标
- 日志
- checkpoint
- manifest
- history

### 观察点 2：export 是独立阶段

训练产生 checkpoint。  
部署或分享时，通常需要整理成 adapter export。

把 export 独立出来，可以让你更清楚地区分：

- 训练过程资产
- 可交付模型资产

### 观察点 3：校验比“文件存在”更进一步

`sha256` 和 `size_bytes` 不能证明模型质量，但能帮助你确认：

- 文件没有被无意替换
- 文件大小异常可以被发现
- manifest 可以被后续工具读取

### 观察点 4：lineage 让 export 能追溯

如果只看导出目录，你很难知道它来自哪次训练。  
`export_manifest.json` 里的 lineage 会保留 source checkpoint、base model、训练方法、训练数据路径、dataset id、dataset version、dataset sha256 和 epochs，让交付资产能回到训练资产。

### 观察点 5：registry report 是跨 run 查询层

`dataset_registry.jsonl` 是追加式历史，重复登记同一份数据是正常现象。  
registry report 用 `registered_count` 表达每个 dataset 被登记过多少次，用 `duplicate_entry_count` 提醒你当前过滤范围里有多少重复登记。`--method` 和 `--model` 则让你从“全部训练输入”收窄到某类训练方法或某个 base model。

### 观察点 6：dataset diff 是输入变化审计层

两次训练如果 dataset id 不同，不代表一定有问题；它可能只是数据真的变了。  
dataset diff 会把 `dataset_sha256`、`dataset_version`、records、messages、role counts 等字段摆出来，让你先判断“输入是否相同”，再讨论训练结果是否可比。

### 观察点 7：checkpoint index 是恢复和导出的入口

`latest_checkpoint.json` 只告诉你最新 checkpoint 是谁。  
`checkpoint_index.json` 会把 checkpoint 文件、adapter hash、文件指纹和 resumable 标记放在一起。真实训练系统里，这层索引会继续长成多 checkpoint 选择、resume 和 export 的入口。

### 观察点 8：run index 是训练历史目录

`run_history.jsonl` 负责追加事实，run index 负责把事实整理成人能读的目录。  
当 run index 保留 dataset id、dataset version、checkpoint、run manifest pointer 和 checkpoint index pointer 时，你就能从“这轮训练发生过”继续追到“证据文件在哪里”，也能按模型或数据集盘点历史 run。

### 观察点 9：export index 是交付资产清单

训练 run 解释“怎么训练出来”，export index 解释“交付出了哪些 adapter”。  
当 export index 同时保留 dataset id、dataset version、adapter hash、export manifest pointer、status、duration、model summaries 和 dataset summaries 时，你就能从一个导出文件反查训练输入，也能从一份数据输入找到对应导出，并且知道这次导出是否成功、耗时大概是多少、按模型或数据集怎么归类、证据 manifest 在哪里。

## 如何判断产物是否可复现

可以用这张表检查：

| 问题 | 应该在哪找 |
| --- | --- |
| 训练用了哪份数据 | `dataset_summary.json`、`dataset_registry_entry.json` |
| 数据是否被替换过 | dataset `sha256` |
| 训练参数是什么 | `training_args.json`、`run_manifest.json` |
| checkpoint 是否完整 | `checkpoint_index.json` |
| adapter 文件指纹是什么 | checkpoint/export file artifacts |
| export 来自哪个 checkpoint | `export_manifest.json` lineage |
| 这个 export 是否进入历史 | `export_history.jsonl`、export index |
| 后续 eval 应该引用什么 | export manifest、dataset id、base model |

如果这些问题都能回答，训练产物才从“文件夹”变成“资产”。

## 常见错误结论

### “有 checkpoint 就能复现”

不够。
还要知道 checkpoint 来自哪份数据、哪个配置、哪个 base model、哪个训练 run。

### “dataset summary 和 registry 是重复的”

不是。
summary 解释单次 run 的输入，registry 负责跨 run 登记和查询。

### “export 只是复制文件”

不对。
export 是把训练产物整理成可交付资产，并保留 lineage。

### “hash 和 size 对质量没帮助，所以不用管”

它们不能证明质量，但能证明文件身份。
没有文件指纹，复现和审计会变弱。

## 扩展任务

任选一个完成：

1. 在 `export_manifest.json` 里增加一个可读的 run display name。
2. 给 checkpoint index 增加 checkpoint 创建时间字段。
3. 给 run index 增加按 method 的小节表。
4. 给 export index 增加按 status 的小节表。
5. 新增一个坏数据样本，验证 schema 校验会在训练产物生成前失败。

## 验收标准

完成这个 lab 后，至少要能通过：

```bash
PYTHON=.venv/bin/python make infra-check
```

你还应该能回答：

- 为什么训练产物要拆目录
- 为什么 dataset role 统计比单纯 records 更有用
- 为什么 dataset registry 和 dataset summary 是两层东西
- 为什么 `list-datasets` 只是查询 registry，不会重新训练
- 为什么 `list-runs` 只是查询 run history，不会重新训练
- 为什么 checkpoint index 是 resume/export 的预备入口
- 为什么 registry report 里的 duplicate count 不等于坏数据
- 为什么 manifest 对复现有价值
- 为什么 export 不是 train 的附属日志
- 为什么 export lineage 能降低复现成本
- 为什么 export history 里应该有 dataset version 和 adapter hash
- 为什么坏数据应该尽早失败
