# 实验追踪、History、复现

训练实验最容易留下的不是清晰资产，而是一堆后来没人敢删的目录。

例如：

```text
outputs/run1
outputs/run-new
outputs/test-final
outputs/final-final
outputs/try-lora-r8
outputs/try-lora-r16-good
```

几天后你可能已经说不清：

- 哪个 run 用了哪份数据？
- 哪个 checkpoint 导出了哪个 adapter？
- 哪个结果最好？
- 哪次训练可以复现？
- 哪个产物已经进入评测？

这就是为什么训练工程必须重视 experiment tracking、history 和 reproducibility。

## 追踪解决什么问题

实验追踪不是为了形式感。
它解决的是：

> 训练结果能不能被解释、比较、复现和继续使用？

一次训练如果只留下 checkpoint，信息太少。
你还需要知道：

- 数据版本
- 训练配置
- 方法和基础模型
- metrics
- logs
- checkpoint 索引
- export 产物
- 文件 hash
- run manifest
- export manifest
- history 记录

这些信息共同构成训练资产的上下文。

## History 和 Manifest 的区别

这两个词经常一起出现，但职责不同。

| 对象 | 主要作用 | 更像什么 |
| --- | --- | --- |
| manifest | 描述一次 run/export 目录内部文件关系 | 单个证据包的目录说明 |
| history | 记录多次 run/export 的追加历史 | 多次实验的索引流水 |

manifest 让你理解一个目录。
history 让你在多个目录之间导航。

缺 manifest，单个 run 难懂。
缺 history，多次实验难找。

## 复现到底是什么意思

复现不是保证每次训练 bit-by-bit 完全相同。
在学习项目里，它至少意味着你能回答：

- 这次训练用的是哪份数据？
- 数据 sha256 是什么？
- method 是 LoRA 还是 QLoRA？
- base model 是什么？
- training args 是什么？
- checkpoint 在哪里？
- export 来自哪个 checkpoint？
- 评测结果来自哪个 export 或模型入口？

真实训练还会继续关心：

- random seed
- library version
- GPU/driver
- distributed config
- tokenizer version
- 数据预处理版本
- mixed precision / quantization setting

当前仓库先从最小可解释结构开始。

## 为什么 dataset version 很关键

训练最容易被忽略的变量是数据。

文件名相同，不代表内容相同。
目录相同，不代表样本没变。
数据行数相同，也不代表答案质量一致。

所以当前仓库会记录：

- dataset sha256
- dataset version
- role counts
- record count
- message count
- dataset registry entry

这些字段让你能确认：这次训练到底用了什么输入。

如果 dataset version 变了，后续比较训练结果时就要格外小心。
模型变好可能来自方法改进，也可能只是数据变了。

## Run History：训练实验的主索引

`run_history.jsonl` 记录每次训练 run 的关键信息。

当前仓库会记录：

- method
- model
- dataset id
- dataset version
- output dir
- checkpoint
- checkpoint index file

它的价值是把多个 run 串起来。

例如你可以问：

- 这个 base model 最近跑过哪些数据版本？
- LoRA 和 QLoRA 各跑了几次？
- 哪个 run 产生了某个 checkpoint？
- 某个 dataset id 被重复训练了几次？

这些问题不能靠手动翻目录稳定回答。

## Run Index：把 History 变成人能读的目录

JSONL 很适合追加，但不一定适合阅读。
所以当前仓库提供 `list-runs`，把 `run_history.jsonl` 转成 run index。

run index 可以帮助你看：

- run count
- method summaries
- model summaries
- dataset summaries
- latest run
- checkpoint index pointer
- run manifest pointer

这一步很重要。
history 是机器友好的记录，index 是人和工具都更容易消费的视图。

## Export History：交付资产也要追踪

训练 run 结束后，checkpoint 还不是最终交付资产。
export 会把 adapter 整理成后续可用的输出。

因此 export 也需要 history。

`export_history.jsonl` 记录：

- output dir
- export manifest pointer
- status
- duration
- base model
- dataset id
- dataset version
- adapter hash
- model summaries
- dataset summaries

这样你拿到一个 adapter 时，不会只知道“这里有个文件”，而能回到：

```text
adapter -> export -> checkpoint -> run -> dataset
```

这就是资产 lineage。

## Checkpoint Index：避免 checkpoint 目录失控

真实训练中可能会出现很多 checkpoint。
如果没有索引，你会很难判断：

- 哪个是 latest？
- 哪个可以 resume？
- 哪个已经 export？
- 哪个 adapter hash 对应哪个文件？

当前仓库的 `checkpoint_index.json` 只有一个 mock checkpoint，但结构上已经表达：

- checkpoint count
- latest checkpoint
- checkpoint files
- adapter model sha256
- resumable

这是在为真实训练系统预留正确习惯。

## 一个具体复盘场景

假设你发现某个导出的 adapter 在 eval 上退化了。

你应该能这样追溯：

1. 从 eval comparison 找到 candidate 模型或产物。
2. 查 export index，找到 export manifest。
3. 从 export manifest 找到 dataset id/version 和 adapter hash。
4. 查 run index，找到对应训练 run。
5. 打开 run manifest，确认 training args、checkpoint 和 artifacts。
6. 打开 dataset registry，确认数据版本和 sha256。
7. 对比 baseline run，判断是数据变了、配置变了，还是训练方法变了。

没有 tracking，这个问题会变成猜谜。

## 当前仓库怎么表达

相关文件：

```text
projects/finetune-demo/src/finetune_demo/trainer/lora_trainer.py
projects/finetune-demo/src/finetune_demo/dataset_registry.py
projects/finetune-demo/src/finetune_demo/run_history.py
projects/finetune-demo/src/finetune_demo/export/adapter_exporter.py
projects/finetune-demo/src/finetune_demo/main.py
```

相关 CLI：

```text
train
export
list-runs
list-exports
list-datasets
diff-datasets
```

关键文件：

```text
outputs/run_history.jsonl
outputs/export_history.jsonl
outputs/dataset_registry.jsonl
outputs/<run>/run_manifest.json
outputs/<run>/artifacts_manifest.json
outputs/<run>/checkpoints/checkpoint_index.json
```

这些文件不是为了显得复杂，而是为了把训练从“目录产物”升级为“可追踪资产”。

## 和 Eval 的关系

训练追踪本身还不够。
微调产物最终必须进入 eval。

一个健康闭环是：

```text
dataset registry
  -> training run
  -> checkpoint index
  -> export manifest
  -> eval run
  -> compare report
  -> release decision
```

这条链路把“我训练了一个 adapter”变成“这个 adapter 是否值得发布”的工程判断。

如果没有 eval，tracking 只能说明产物从哪里来，不能说明它是否更好。
如果没有 tracking，eval 发现问题后又很难回溯原因。

两者必须连起来。

## 常见误区

### “学习阶段不用管复现”

正好相反。
学习阶段最适合养成记录习惯，因为项目还小，结构容易看清。

### “History 只是日志”

不是。
history 是多次实验之间的索引层。

### “有 checkpoint 就能复现”

不够。
你还需要数据、配置、manifest、hash、export 和评测记录。

### “文件多说明系统复杂”

不一定。
如果每个文件都有清晰职责，文件多是在降低理解成本。

### “接了 MLflow/W&B 才叫实验追踪”

不一定。
完整平台很有价值，但学习阶段先用本地 history/manifest 建立结构也很好。

## 学完应该能回答

读完这一页后，你应该能回答：

1. manifest 和 history 分别解决什么问题？
2. 为什么 dataset version / sha256 对训练复现很关键？
3. run history 和 export history 有什么区别？
4. checkpoint index 为什么不能省？
5. 如何从一个退化的 eval 结果追溯回训练数据和 export 资产？

## 继续阅读

- [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)
- [数据集、Runs 与 Checkpoints](/05-finetuning-training/04-datasets-runs-checkpoints)
- [Run、Compare、History](/04-evaluation-observability/01-run-compare-history)
- [Finetune 到 Eval 的资产链路案例](/11-case-studies/03-finetune-to-eval-asset-lineage)
