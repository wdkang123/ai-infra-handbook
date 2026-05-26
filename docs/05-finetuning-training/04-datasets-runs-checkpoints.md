# 数据集、Run、Checkpoint

训练学习不能只盯着模型和参数。

一旦你真的开始跑实验，最容易失控的往往不是模型本身，而是：

- 这次到底用了哪份数据？
- 这个 checkpoint 属于哪次 run？
- export 对应哪个 checkpoint？
- 两次训练结果差异来自数据、配置，还是随机性？
- 这个 adapter 还能不能追溯？

所以训练工程的核心，不只是训练本身，还包括如何把训练过程组织成可回看的对象。

## 三个对象分别是什么

| 对象 | 主要回答 | 典型文件 |
| --- | --- | --- |
| Dataset | 这次训练看到了什么数据 | `dataset_summary.json`、`dataset_registry_entry.json` |
| Run | 这次训练怎么跑的 | `run_manifest.json`、`training_args.json`、metrics/logs |
| Checkpoint | 训练过程留下了哪个状态 | `checkpoint-0001/`、`checkpoint_index.json` |

它们不是附属文件，而是训练资产链路的核心。

## Dataset：实验方向的来源

数据集决定模型往哪个方向被推动。

如果数据不清楚，训练结果就很难解释。

一个训练数据集至少要回答：

- 有多少 records？
- 每条 record 有哪些 messages？
- role 分布是什么？
- 是否包含 system message？
- 文件 sha256 是什么？
- dataset version 是什么？
- 数据格式是否有效？
- 这份数据是否被登记到 registry？

当前仓库用这些产物表达：

```text
data/dataset_summary.json
data/dataset_registry_entry.json
outputs/dataset_registry.jsonl
```

这些文件的价值是让数据变成可追踪对象，而不是训练前的一次性输入。

## Dataset Registry：跨 Run 追踪数据

单个 run 里的 dataset summary 只回答“这次用了什么”。
dataset registry 进一步回答：

> 多次 run 之间，这些数据输入如何被登记和追踪？

它适合回答：

- 同一份数据被训练了几次？
- 同一个 dataset id 是否重复出现？
- 某个 model/method 用过哪些数据版本？
- 两份数据的 sha256 是否不同？
- role counts 是否变化？

当前仓库提供：

```text
list-datasets
diff-datasets
```

它们不会改变训练产物，只是把 registry 读成更可理解的报告。

## Run：一次完整训练尝试

Run 最好被理解成：

> 一次完整训练尝试的目录对象。

它不只是一个命令执行结果。

一个 run 至少应该包含：

- 训练方法
- base model
- dataset id/version
- training args
- trainer state
- metrics
- logs
- events
- checkpoint
- checkpoint index
- run manifest
- artifacts manifest

这些信息让你后面能回答：

- 这次训练怎么跑的？
- 和上次相比改了什么？
- 如果结果变差，应该从哪里查？
- 哪个 checkpoint 能导出？

## Manifest：让 Run 目录可读

run 目录里文件很多。
没有 manifest，读者只能自己猜文件关系。

当前仓库用：

```text
run_manifest.json
artifacts_manifest.json
```

表达：

- 本次 run 的 method/model/output_dir
- 关键 artifacts 路径
- dataset id/version/sha256
- 文件清单
- 文件 artifact 信息

manifest 的价值是让一次训练从“散落文件”变成“有入口的证据包”。

## Checkpoint：训练过程中的正式节点

很多初学者会把 checkpoint 当成训练过程里的临时文件。
但从工程视角看，它是正式节点。

checkpoint 连接：

- resume training
- export adapter
- 对比不同阶段
- 回溯实验状态
- 记录 adapter hash

真实训练里可能有多个 checkpoint：

```text
checkpoint-0100
checkpoint-0200
checkpoint-0300
```

如果没有 checkpoint index，你很快会不知道哪个能用。

## Checkpoint Index：避免目录失控

当前仓库用：

```text
checkpoints/checkpoint_index.json
checkpoints/checkpoint_index.md
```

表达：

- checkpoint count
- latest checkpoint
- checkpoint files
- adapter model sha256
- resumable

未来真实训练中，它还可以继续扩展：

- best checkpoint
- metrics per checkpoint
- exported checkpoint
- optimizer state
- scheduler state
- resume readiness

Checkpoint index 应该成为 export 和 resume 的入口。

## Export：从训练状态到交付资产

export 回答的是：

> 训练出来的东西，如何变成后续可以继续使用的资产？

如果没有 export 层，checkpoint 和部署/评测之间会混乱。

export 应该记录：

- source checkpoint
- base model
- dataset id/version
- adapter hash
- export status
- duration
- export manifest

这让 adapter 可以进入 eval 和 release decision。

## 一条资产链路

可以把训练资产链记成：

```text
dataset
  -> dataset registry
  -> run
  -> checkpoint index
  -> export
  -> eval
  -> release decision
```

任何一环断了，后续复盘都会变难。

## 当前仓库怎么对应

相关文件：

```text
projects/finetune-demo/src/finetune_demo/trainer/lora_trainer.py
projects/finetune-demo/src/finetune_demo/dataset_registry.py
projects/finetune-demo/src/finetune_demo/run_history.py
projects/finetune-demo/src/finetune_demo/export/adapter_exporter.py
```

相关命令：

```text
train
export
list-datasets
diff-datasets
list-runs
list-exports
```

当前实现是学习型 mock，但对象边界是真实训练系统也需要的。

## 一个具体复盘场景

假设某个 export 在 eval 上退化。

你应该能追溯：

1. 从 eval comparison 找 candidate。
2. 查 export manifest。
3. 找 source checkpoint。
4. 查 checkpoint index。
5. 打开 run manifest。
6. 查 dataset id/version/sha256。
7. 对比 baseline run。

如果 dataset、run、checkpoint 没有被对象化，这个过程会变成猜。

## 常见误区

### “训练成功 = 生成 checkpoint”

太窄。
训练成功至少意味着 run 及上下文被完整留下。

### “数据集以后再整理”

风险很大。
一旦训练跑完再补数据来源，很多细节已经不可复现。

### “Checkpoint 是临时文件”

不对。
它是 resume、export 和回溯的正式节点。

### “Export 只是部署前最后一步”

不只是。
它是把实验结果变成可流转资产的关键步骤。

### “文件多就是复杂”

不一定。
如果每个文件职责清楚，文件是在降低长期理解成本。

## 学完应该能回答

读完这一页后，你应该能回答：

1. Dataset、run、checkpoint 分别解决什么问题？
2. Dataset registry 为什么比单个 dataset summary 更进一步？
3. Run manifest 和 artifacts manifest 有什么价值？
4. Checkpoint index 为什么是 export/resume 的入口？
5. 如何从 eval 退化结果追溯回训练数据？

## 继续阅读

- [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)
- [实验追踪、History、复现](/05-finetuning-training/06-experiment-tracking-history-reproducibility)
- [Finetune 真实训练迁移](/12-production-migration/04-finetune-real-training-migration)
- [Finetune 到 Eval 的资产链路案例](/11-case-studies/03-finetune-to-eval-asset-lineage)
