# 训练产物复现案例

这个案例模拟一次训练产物复盘：

> 有人给你一个导出的 adapter 目录，问它能不能用于下一轮评测或发布。你要判断它是否可追溯、可复现、可解释。

重点不是“文件存在就可以”，而是看这个产物能不能回答：

- 从哪个训练 run 来
- 用了哪个 dataset
- checkpoint 是否完整
- export 是否成功
- 后续 eval 能否记录清楚来源

这个案例训练的是 lineage 思维。训练产物不是孤立文件，而是一条链：数据、配置、训练、checkpoint、导出、评测和发布判断。链条上任何一段缺失，后面的人都只能靠猜。

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

## 先画出资产链

开始检查前，先写下你期望看到的链路：

```text
dataset file
  -> dataset_summary.json
  -> dataset_registry_entry.json
  -> run_manifest.json
  -> checkpoint_index.json
  -> export_manifest.json
  -> export_history.jsonl
  -> eval run metadata
```

后面的步骤就是逐段确认这条链有没有断。

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

export manifest 是最适合从后往前查的入口，因为很多时候别人交给你的不是训练目录，而是一个导出产物。你需要从交付物反推它的来源。

判断时可以问：

- 这个 export 是成功还是失败。
- 它来自哪个 checkpoint。
- 它记录了 base model 和 method 吗。
- 它记录了 dataset id / sha256 / version 吗。
- 它能指向 run manifest 或 source lineage 吗。

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

如果 run manifest 不完整，后续复现会非常困难。真实训练系统里，很多事故不是模型没保存，而是后来没人知道当时用了哪份数据、哪组参数和哪个 checkpoint。

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

checkpoint index 的价值是把“目录存在”变成“目录可解释”。它应该帮助你回答：

- 当前最新 checkpoint 是哪个。
- 这个 checkpoint 是否可 resume。
- adapter 文件是否有 hash。
- checkpoint 文件是否完整。
- export 是否引用了正确 checkpoint。

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

dataset summary 和 registry 不要混用：

| 文件 | 回答的问题 |
| --- | --- |
| `dataset_summary.json` | 这一次 run 实际使用的数据是什么 |
| `dataset_registry_entry.json` | 这一次数据输入如何登记 |
| `dataset_registry.jsonl` | 多次 run 之间哪些数据被使用过 |
| dataset diff | 两份登记数据是否发生变化 |

如果后续 eval 发现效果异常，dataset registry 能帮助你判断问题是否可能来自训练输入变化。

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

索引的价值在于跨 run 复盘。单次 manifest 能说明“这一次发生了什么”，索引能说明“同类事情发生过多少次、分别来自哪里、是否重复、是否存在异常分布”。

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

## 第 7 步：把 lineage 写进 eval 记录

训练产物进入 eval 后，评测记录也应该保留来源。否则你虽然能评测 adapter，却无法解释分数对应哪次训练。

建议在 eval 复盘里记录：

```text
eval target：
adapter export dir：
export manifest：
source checkpoint：
base model：
dataset version：
dataset sha256：
training method：
run manifest：
```

这一步把训练资产链和评测判断链接起来。没有这一步，eval 和 finetune 仍然是两个孤立模块。

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

更完整的判断可以加：

```text
我确认的 lineage：

我无法确认的 lineage：

进入 eval 的条件：

阻止进入 eval 的条件：

如果后续发布，需要额外记录：
```

## 这个案例应该带走什么

训练工程的核心不是“保存一个权重文件”，而是让模型能力变化可以被解释：

1. 数据从哪里来
2. 训练怎么跑
3. checkpoint 是否完整
4. export 是否成功
5. 后续 eval 能否追溯来源

如果你能从 export 一路追回 dataset 和 checkpoint，再把它接到 eval 发布判断，这条训练资产链路就真正连起来了。

## 常见风险

### 只有 adapter，没有来源

这类产物最危险。它可能能被加载，但无法解释从哪里来，也无法可靠进入发布判断。

### dataset 路径存在，但没有版本指纹

路径不能证明数据没变。至少要有 sha256 或其他版本指纹，才能把训练输入固定下来。

### checkpoint 能找到，但 index 不完整

没有文件列表、hash 或 latest 指针时，后续 resume/export 很容易靠人工猜。

### export 成功，但没有 history

单次 export manifest 可以解释当前产物，history 才能支持长期管理和比较。

## 生产系统还需要什么

真实训练平台还会继续补：

- 数据集版本管理系统。
- 实验追踪后端。
- 多 checkpoint 策略和保留策略。
- 权重存储和权限控制。
- 训练代码版本、镜像版本、硬件环境记录。
- eval 结果和模型 registry 的绑定。

但学习阶段先掌握这条最小 lineage，就能避免很多“文件存在但没人敢用”的问题。
