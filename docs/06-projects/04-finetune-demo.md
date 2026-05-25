# finetune-demo

这是学习链里的“训练迭代层”。

你在这里主要学的是：

- 一次训练 run 为什么应该沉淀成目录
- 为什么 checkpoint、logs、metrics、dataset summary 要分开
- 为什么 dataset registry 能让训练输入跨 run 被追踪
- 为什么还要多一层 manifest / history
- 为什么 export/save 这种后处理值得独立保留

`finetune-demo` 最重要的学习价值，不是它已经把训练做得多真实，而是它已经把训练工程最值得先看清楚的资产层摆出来了。

很多人第一次学训练时，最容易只盯着“怎么开始 train”。  
但这页更想帮你看到的是：

- 一次训练 run 为什么不该只剩一个 checkpoint
- 为什么输出目录、manifest、history 会决定后面你能不能复现和比较

## 先看哪些代码

- `projects/finetune-demo/src/finetune_demo/main.py`
- `projects/finetune-demo/src/finetune_demo/config.py`
- `projects/finetune-demo/src/finetune_demo/artifacts.py`
- `projects/finetune-demo/src/finetune_demo/dataset_registry.py`
- `projects/finetune-demo/src/finetune_demo/trainer/lora_trainer.py`
- `projects/finetune-demo/src/finetune_demo/export/adapter_exporter.py`

## 先跑什么

```bash
cd /path/to/ai-infra/projects/finetune-demo
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main train \
  --method lora \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --dataset ./data/train.jsonl \
  --output ./outputs/demo-run \
  --epochs 1
```

训练前会扫描 JSONL 数据集：每条记录必须是带 `messages` 的 chat-style 样本，消息需要包含合法 `role`、非空 `content`，并且至少有一条 user message 和一条 assistant response。这样坏数据会在生成训练产物前失败。

`data/dataset_summary.json` 现在不只记录样本数，也会记录 message 总数、role 分布、包含 system message 的样本数、数据集大小和 `sha256`。这让训练数据从“一个路径”变成可以被复查的输入资产。

它还会生成一个轻量 `dataset_version`，格式类似 `sha256:xxxxxxxxxxxx`。这不是完整数据版本系统，但能让你先把“训练输入应该有版本指纹”这件事落实到产物里。

这个版本指纹会继续写入 `trainer_state.json`，并在 export 阶段传到 `export_manifest.json` 与 `export_history.jsonl`。这样你不只知道“训练时用了哪份数据”，也能在导出 adapter 后继续追到同一个数据版本。

训练时还会生成 `data/dataset_registry_entry.json`，并向输出父目录追加 `dataset_registry.jsonl`。前者是这次 run 使用的数据登记卡，后者是跨多次 run 的轻量数据登记表。它们让 `dataset_id`、数据路径、sha256、role 分布和来源 run 能串起来。

checkpoint 现在也会有自己的索引：`checkpoints/latest_checkpoint.json` 指向最新 checkpoint，`checkpoints/checkpoint_index.json` / `.md` 则列出 checkpoint、文件指纹、adapter sha256 和是否可作为 resume/export 入口。即使当前只有一个 mock checkpoint，也先把真实训练系统里“checkpoint 不该只是目录名”的直觉放进来了。

然后再导出：

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main export \
  --checkpoint ./outputs/demo-run/checkpoint-0001 \
  --output ./outputs/demo-export
```

也可以把 dataset registry 导出成更容易阅读的报告：

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-datasets \
  --registry ./outputs/dataset_registry.jsonl \
  --output ./outputs/dataset_registry_report.json \
  --markdown-output ./outputs/dataset_registry_report.md
```

这个命令不会重新训练，只是读取 `dataset_registry.jsonl`，把多次 run 登记过的数据输入汇总成 JSON/Markdown。它回答的是“这些训练输入被哪些 run 用过”，不是“这次训练数据长什么样”。你也可以用 `--method lora` 或 `--model Qwen/Qwen2.5-0.5B-Instruct` 过滤报告，并通过 `duplicate_entry_count` 看重复登记数量。

如果你想比较两份登记过的数据输入，可以生成 dataset diff：

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main diff-datasets \
  --registry ./outputs/dataset_registry.jsonl \
  --left train@sha256:example_a \
  --right train@sha256:example_b \
  --output ./outputs/dataset_registry_diff.json \
  --markdown-output ./outputs/dataset_registry_diff.md
```

它会比较 dataset version、sha256、records、messages、role counts 等字段，帮助你判断两次训练输入是同一份数据，还是结构或内容已经变化。

如果你想让这轮练习更有感觉，最推荐顺序是：

1. 先跑 `train`
2. 先不要急着看代码，先看输出目录
3. 再跑 `export`
4. 再回头看 `run_manifest`、`artifacts_manifest`、history

这样你会更容易先建立“训练资产”的感觉，而不是一开始就掉进实现细节。

如果你想把训练 run history 变成可读报告，可以生成 run index：

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-runs \
  --history ./outputs/run_history.jsonl \
  --method lora \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --output ./outputs/run_index.json \
  --markdown-output ./outputs/run_index.md
```

它会列出 method、model、dataset id、dataset version、output dir、checkpoint、`run_manifest_file` 和 `checkpoint_index_file`，并生成 `method_counts`、`model_summaries`、`dataset_summaries`。这层报告回答的是“训练 run 本身有哪些、证据 manifest 和 checkpoint 索引在哪里”，和 export index 回答的“导出了哪些 adapter”不是同一个问题。

## 你应该观察什么

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
- `dataset_registry_report.json`
- `dataset_registry_report.md`
- dataset registry report 里的 `method_filter`、`model_filter`、`duplicate_entry_count`
- `dataset_registry_diff.json`
- `dataset_registry_diff.md`
- `run_history.jsonl`
- `run_index.json`
- `run_index.md`
- `export_history.jsonl`
- `export_index.json`
- `export_index.md`

这里最值得刻意观察的几个问题是：

1. 为什么训练产物要分目录和分角色存
2. 为什么 `dataset_summary.json` 这种文件看起来不起眼，但其实很关键
3. 为什么 `dataset_registry.jsonl` 和单次 summary 解决的是不同问题
4. 为什么 export 不是训练的附属步骤，而是单独一层结果整理
5. 为什么 history 能让这套东西不只是一轮性的实验

现在 `artifacts_manifest.json` 和 `export_manifest.json` 里也会记录关键文件的 `size_bytes` 与 `sha256`。这能帮你提前建立一个真实训练系统里很重要的直觉：产物不仅要“存在”，还要能被校验。

导出的 `export_manifest.json` 还会保留 lineage 信息，例如来源 checkpoint、base model、训练方法、训练数据路径、dataset id、dataset version、dataset sha256 和 epochs。这样 export 不只是几个文件的拷贝，而是能追溯回训练 run 的交付资产。

`export_history.jsonl` 也会记录 base model、dataset id、dataset version、adapter 文件 hash、`export_manifest_file`、导出状态和导出耗时，方便你把多次导出放在一起比较，并且能从历史行直接回到导出 manifest。

如果你想把导出历史变成可读报告，可以生成 export index：

```bash
PYTHONPATH=src ../../.venv/bin/python -m finetune_demo.main list-exports \
  --history ./outputs/export_history.jsonl \
  --output ./outputs/export_index.json \
  --markdown-output ./outputs/export_index.md
```

它会列出 output dir、export manifest、status、duration seconds、base model、dataset id、dataset version、adapter sha256、model summaries 和 dataset summaries，适合回答“这些 adapter 分别来自哪份训练输入、导出是否成功、耗时大概是多少、按模型或数据集怎么汇总，以及证据 manifest 在哪里”。

## 这部分当前已经做到什么

- 最小 train / save / export CLI
- 最小 finetune run history 查询 CLI
- 最小 dataset registry 查询 CLI
- 最小 dataset registry diff CLI
- 最小训练产物目录
- 最小 checkpoint 与 export 链
- 可追加 run / export history
- chat-style JSONL 数据集结构校验
- dataset role 统计、数据集大小和 sha256
- dataset version 和平均 messages per record
- dataset registry entry 和追加式 dataset registry
- dataset registry report 的 method/model 过滤与重复登记统计
- dataset registry diff 的 sha256/version/role counts 对比
- checkpoint index 的 adapter hash、resumable 标记和文件指纹
- run index 的 run manifest/checkpoint index pointer 与 model/dataset summaries
- trainer state 中的数据版本指纹
- 关键产物 size 与 sha256 记录
- export manifest / export history 的 base model、dataset id、dataset version、export manifest pointer、status、duration 与 lineage 信息
- export index 的 base model、dataset id、dataset version、export manifest pointer、status、duration、model/dataset summaries 与 adapter hash 查询

也就是说，它已经很适合你拿来建立“训练工程对象”这层直觉。

## 这部分当前还没做到什么

- 真实 Trainer / GPU 训练
- 真实 PEFT 权重保存逻辑
- resume / multi-checkpoint 策略
- 真正接实验追踪系统

## 最适合的继续学习顺序

如果你已经把这页跑过一轮，下一步最推荐接着读：

1. [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)
2. [实验追踪、History、复现](/05-finetuning-training/06-experiment-tracking-history-reproducibility)
3. [什么时候该微调](/05-finetuning-training/07-when-to-finetune)
4. [从 Demo Training 到真实训练系统](/05-finetuning-training/08-from-demo-training-to-real-training-system)

这样你会更容易把 `finetune-demo` 从“命令演示”看成“训练工程骨架”。
