# 训练产物复现案例

这个案例模拟一次训练产物复盘：

> 有人给你一个导出的 adapter 目录，问它能不能用于下一轮评测或发布。你要判断它是否可追溯、可复现、可解释。

重点不是“文件存在就可以”，而是看这个产物能不能回答：

- 从哪个训练 run 来
- 用了哪个 dataset
- checkpoint 是否完整
- export 是否成功
- 后续 eval 能否记录清楚来源

## 场景设定

你已经跑过一次 finetune：

```bash
cd /path/to/ai-infra/projects/finetune-demo

PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main train \
  --method lora \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --dataset ./data/train.jsonl \
  --output ./outputs/demo-run \
  --epochs 1
```

然后导出：

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main export \
  --checkpoint ./outputs/demo-run/checkpoint-0001 \
  --output ./outputs/demo-export
```

## 第 1 步：从 export manifest 开始

先看导出目录：

```bash
cat ./outputs/demo-export/export_manifest.json
```

重点看：

- `artifact_type`
- `source_checkpoint`
- `model`
- `method`
- `dataset_id`
- `dataset_sha256`
- `status`
- `duration_seconds`
- `lineage`

如果 export manifest 不能说明来源，就很难进入后续评测或发布。

## 第 2 步：回到训练 run manifest

```bash
cat ./outputs/demo-run/run_manifest.json
```

重点看：

- `model`
- `method`
- `dataset`
- `training_args`
- `metrics`
- `artifacts`
- `checkpoint`

run manifest 是训练资产目录的核心说明书。  
它告诉你这次训练为什么存在、用了什么输入、留下了哪些输出。

## 第 3 步：检查 checkpoint index

```bash
cat ./outputs/demo-run/checkpoints/checkpoint_index.json
```

重点看：

- `artifact_type`
- `checkpoint_count`
- `latest_checkpoint`
- `checkpoints`
- `adapter_model_sha256`
- `resumable`

如果 checkpoint index 里没有 hash、文件列表或 latest checkpoint，你就只能靠目录猜测，这在真实训练系统里很危险。

## 第 4 步：检查 dataset summary 和 registry

```bash
cat ./outputs/demo-run/data/dataset_summary.json
cat ./dataset_registry.jsonl
```

重点看：

- `dataset_id`
- `dataset_sha256`
- `dataset_version`
- `role_counts`
- `message_count`
- `example_count`

dataset summary 说明这次训练实际看到了什么数据。  
dataset registry 则让你能跨 run 查询“哪些训练用过同一份数据”。

## 第 5 步：生成 run / dataset / export 索引

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-runs \
  --history ./run_history.jsonl \
  --output ./outputs/run_index.json

PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-datasets \
  --registry ./dataset_registry.jsonl \
  --output ./outputs/dataset_registry_report.json

PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-exports \
  --history ./export_history.jsonl \
  --output ./outputs/export_index.json
```

重点看：

- run index 的 `checkpoint_index_file`
- dataset registry report 的 duplicate count 和 filters
- export index 的 `model_summaries`
- export index 的 `dataset_summaries`
- export history 的 `export_manifest_file`

单个 manifest 适合解释一次产物。  
index 适合解释一批产物。

## 第 6 步：判断是否可以进入 eval

你可以用这个清单：

- [ ] export manifest 存在
- [ ] export status 是 success
- [ ] source checkpoint 能找到
- [ ] checkpoint index 能列出文件和 hash
- [ ] run manifest 能解释训练参数和产物
- [ ] dataset summary 能解释数据结构
- [ ] dataset sha256 能贯穿 train 和 export
- [ ] run history 和 export history 能找到记录

如果这些都满足，就可以进入下一步 eval。  
如果缺了 dataset 或 checkpoint 证据，即使 adapter 文件存在，也不建议直接进入发布判断。

## 复盘模板

```text
导出产物：

source checkpoint：

训练 run：

dataset id / sha256：

checkpoint index：

export status：

是否可进入 eval：

风险：

下一步：
```

## 这个案例应该带走什么

训练工程的核心不是“保存一个权重文件”，而是让模型能力变化可以被解释：

1. 数据从哪里来
2. 训练怎么跑
3. checkpoint 是否完整
4. export 是否成功
5. 后续 eval 能否追溯来源

如果你能从 export 一路追回 dataset 和 checkpoint，再把它接到 eval 发布判断，这条训练资产链路就真正连起来了。
