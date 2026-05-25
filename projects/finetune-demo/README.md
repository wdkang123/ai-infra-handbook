# finetune-demo

这是学习链路里的“训练迭代层”入口。

它不是要立刻变成完整训练框架，而是帮你理解：

- 一次训练 run 应该沉淀哪些文件
- 为什么 checkpoint、logs、metrics、dataset summary 要分开
- 为什么 dataset registry 和单次 dataset summary 不是同一层
- 为什么 registry 查询需要 method/model 过滤和重复登记统计
- 为什么还要多一层 manifest / history
- export/save 这些后处理步骤为什么值得单独保留
- 为什么 dataset role stats 和 export lineage 对复现重要

## 先看哪里

- [main.py](src/finetune_demo/main.py)
- [config.py](src/finetune_demo/config.py)
- [lora_trainer.py](src/finetune_demo/trainer/lora_trainer.py)
- [adapter_exporter.py](src/finetune_demo/export/adapter_exporter.py)

## 先跑什么

```bash
cd projects/finetune-demo
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main train \
  --method lora \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --dataset ./data/train.jsonl \
  --output ./outputs/demo-run \
  --epochs 1
```

然后再导出：

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main export \
  --checkpoint ./outputs/demo-run/checkpoint-0001 \
  --output ./outputs/demo-export
```

查看 dataset registry：

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-datasets \
  --registry ./outputs/dataset_registry.jsonl \
  --method lora \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --output ./outputs/dataset_registry_report.json \
  --markdown-output ./outputs/dataset_registry_report.md
```

比较两份 registry 数据：

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main diff-datasets \
  --registry ./outputs/dataset_registry.jsonl \
  --left train@sha256:example_a \
  --right train@sha256:example_b \
  --output ./outputs/dataset_registry_diff.json \
  --markdown-output ./outputs/dataset_registry_diff.md
```

查看 run history：

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-runs \
  --history ./outputs/run_history.jsonl \
  --method lora \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --output ./outputs/run_index.json \
  --markdown-output ./outputs/run_index.md
```

查看 export history：

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-exports \
  --history ./outputs/export_history.jsonl \
  --output ./outputs/export_index.json \
  --markdown-output ./outputs/export_index.md
```

## 你应该看到什么

- `trainer_state.json`
- `training_args.json`
- `metrics/train_metrics.json`
- `logs/train.log`
- `logs/events.jsonl`
- `data/dataset_summary.json`
- `data/dataset_registry_entry.json`
- `checkpoints/latest_checkpoint.json`
- `checkpoints/checkpoint_index.json`
- `checkpoints/checkpoint_index.md`
- `run_manifest.json`
- `artifacts_manifest.json`
- `dataset_registry.jsonl`
- `run_history.jsonl`
- `export_history.jsonl`
- `export_index.json`
- `export_index.md`
- `dataset_registry_report.json`
- `dataset_registry_report.md`
- `dataset_registry_diff.json`
- `dataset_registry_diff.md`
- `run_index.json`
- `run_index.md`

重点看：

- `data/dataset_summary.json` 里的 `role_counts`、`dataset_size_bytes`、`dataset_sha256`
- `data/dataset_summary.json` 里的 `dataset_version` 和 `average_messages_per_record`
- `data/dataset_registry_entry.json` 里的 `dataset_id`
- `outputs/dataset_registry.jsonl` 里的追加式数据登记记录
- `outputs/dataset_registry_report.json` 里的 `method_filter`、`model_filter`、`duplicate_entry_count`
- `outputs/demo-export/export_manifest.json` 里的 `base_model` 和 `lineage`
- `outputs/demo-export/export_manifest.json` 里的 `status` 和 `duration_seconds`
- `outputs/export_history.jsonl` 里的 `export_manifest_file`
- `outputs/run_index.json` 里的 `run_manifest_file`
- `outputs/run_index.json` 里的 `checkpoint_index_file`
- `outputs/run_index.json` 里的 `method_counts`
- `outputs/run_index.json` 里的 `model_summaries` 和 `dataset_summaries`
- `outputs/export_index.json` 里的 `status_counts` 和 `average_duration_seconds`
- `outputs/export_index.json` 里的 `model_summaries` 和 `dataset_summaries`

## 这段代码现在解决什么

- 最小 train/save/export CLI
- 最小 dataset registry 查询 CLI
- 最小 dataset registry diff CLI
- 最小 run history 查询 CLI
- 最小 export history 查询 CLI
- 最小训练产物目录
- 最小 checkpoint 与 export 链
- 可追加的 run/export history
- dataset role stats、数据集大小和 sha256
- dataset version 和平均 messages per record
- dataset registry entry 和 `dataset_registry.jsonl`
- dataset registry report 的 method/model 过滤与重复登记统计
- dataset registry diff 的 sha256/version/role counts 对比
- checkpoint index 的 adapter hash、resumable 标记和文件指纹
- run index 的 run manifest/checkpoint index pointer 与 model/dataset summaries
- export manifest 的 base model、status、duration 与 lineage
- export history 的 `export_manifest_file`
- export index 的 status/duration 与 model/dataset summaries 聚合

## 这段代码现在还没解决什么

- 没有真实 Trainer / GPU 训练
- 没有真实 PEFT 权重保存逻辑
- 没有 resume / multi-checkpoint 策略
- 还没有真正接实验追踪系统
