# 训练产物、Checkpoint、Export

微调学习里，很多人会把注意力放在“训练命令能不能跑起来”。
但真实工程里，更关键的问题往往是：

- 这次训练用的是什么数据？
- 数据版本有没有变？
- 训练参数是什么？
- checkpoint 里到底有哪些文件？
- 这个 adapter 从哪个 run 来？
- export 后的资产还能不能追溯回训练输入？
- 三个月后还能不能解释这次实验？

所以训练系统不能只留下一个 checkpoint。
它需要把一次训练变成可追踪的资产链路。

## 训练不只是生成权重

一次微调至少有三类产物：

| 类别 | 代表内容 | 解决的问题 |
| --- | --- | --- |
| Run 产物 | trainer state、training args、metrics、logs、events | 这次训练怎么跑的 |
| 数据证据 | dataset summary、dataset registry entry、dataset sha256 | 这次训练吃了什么数据 |
| 交付资产 | checkpoint、adapter、export manifest、export history | 后续部署或评测用什么 |

如果只保存 `adapter_model.safetensors`，你可能能加载它，但很难解释它。

这对公开学习项目尤其重要。
读者不是只想看到“有一个文件生成了”，而是要学会一次训练应该留下哪些证据。

## Run：训练过程本身要可回看

训练 run 解决的是：

> 这次训练是怎么发生的？

当前仓库的 `finetune-demo` 会生成一个 run 目录，里面包含：

```text
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
checkpoint-0001/adapter_config.json
checkpoint-0001/adapter_model.safetensors
checkpoint-0001/trainer_state.json
run_manifest.json
artifacts_manifest.json
```

这些文件共同表达一个思想：训练 run 是一个证据包，而不是一个临时目录。

## Dataset Summary：先说明训练输入

数据是微调质量的源头。
如果数据变了，训练结果就可能变；如果数据质量差，再漂亮的训练指标也意义有限。

当前仓库会对 JSONL 训练数据做最小检查和摘要：

- record 数量
- message 数量
- 平均每条 record 的 message 数
- role counts
- 是否包含 system message
- 文件大小
- dataset sha256
- dataset version

这让训练输入有了可比较的指纹。

例如两个 run 都叫 “demo training”，但 dataset sha256 不同，就说明它们不是同一份训练输入。
这比只记文件名可靠得多。

## Dataset Registry：把数据从单次 run 里提出来

`dataset_summary.json` 关注的是当前 run。
`dataset_registry_entry.json` 和 `dataset_registry.jsonl` 则把训练数据登记成可以跨 run 追踪的对象。

当前仓库会在每次训练后追加：

```text
outputs/dataset_registry.jsonl
```

这让你可以回答：

- 这份数据被哪些 run 使用过？
- 同一个 dataset id 是否重复登记？
- 不同 method/model 是否用了同一份数据？
- 数据版本是否变化？
- role counts 是否变化？

这就是为什么数据登记不是“多余文件”。
它把训练输入从一次性上下文变成了工程资产。

## Checkpoint：中间状态也要有索引

checkpoint 不只是一个目录。
真实训练里可能有多个 checkpoint：

```text
checkpoint-0100
checkpoint-0200
checkpoint-0300
```

你需要知道：

- 哪个是 latest？
- 哪个可以 resume？
- 每个 checkpoint 包含哪些文件？
- adapter hash 是什么？
- export 应该从哪个 checkpoint 来？

当前学习项目只有一个 mock checkpoint，但仍然生成：

```text
checkpoints/latest_checkpoint.json
checkpoints/checkpoint_index.json
checkpoints/checkpoint_index.md
```

这是为了提前建立正确结构。
等你接入真实训练框架时，不需要重新发明“多个 checkpoint 怎么追踪”。

## Export：把训练产物整理成可交付资产

export 解决的是：

> 训练过程中的中间产物如何变成后续可用的资产？

训练目录通常包含很多运行细节。
部署、评测或分享时，你需要的是更清晰的交付包，例如：

- adapter config
- adapter weights
- export manifest
- base model 信息
- dataset id / version
- adapter hash
- export status
- duration

所以 export 不是多余步骤。
它把“训练产生了东西”推进成“这个东西可以被后续系统引用”。

## Export History：交付资产也要可追溯

如果只把 adapter 复制到某个目录，后续会很难回答：

- 这个 adapter 来自哪个 run？
- 使用的 base model 是什么？
- 使用的数据版本是什么？
- export 是否成功？
- adapter 文件有没有变化？

当前仓库会追加：

```text
outputs/export_history.jsonl
```

并提供 `list-exports` 把历史整理成 index。
这让 export 和 run 一样，也能被盘点和追溯。

## Run History：实验不是一次性动作

训练实验通常会跑很多次。
如果每次只看最后一个输出目录，就会很快混乱。

`run_history.jsonl` 记录：

- method
- model
- dataset id
- dataset version
- output dir
- checkpoint
- checkpoint index file

再通过 `list-runs` 生成 run index，你就能从历史反查到对应 run 的证据文件。

这和 eval 里的 run history 是同一种思想：
每次实验都要进入历史，才能变成可复盘对象。

## Manifest：告诉读者文件之间的关系

run 目录里文件很多，如果没有 manifest，读者需要自己猜：

- 哪个文件是入口？
- 哪个文件描述数据？
- 哪个文件描述 checkpoint？
- 哪个文件可以交给 export？
- 哪些文件属于同一次 run？

当前仓库用两个 manifest 解决这个问题：

| 文件 | 作用 |
| --- | --- |
| `run_manifest.json` | 描述本次训练的 method、model、output dir、关键 artifacts 和 dataset 信息 |
| `artifacts_manifest.json` | 列出 run bundle 中的文件，并保存文件 artifact 信息 |

manifest 的价值是降低读者理解成本。
它让目录结构从“散落文件”变成“有入口的证据包”。

## 一个具体资产追溯场景

假设你拿到一个导出的 adapter，想判断能不能发布给 eval 使用。

合理追溯路径是：

1. 看 export manifest，确认 base model、adapter hash、dataset id、dataset version。
2. 查 `export_history.jsonl`，确认这次 export 是否记录在历史里。
3. 查 `run_history.jsonl`，找到对应 dataset id/version 的训练 run。
4. 打开 run manifest，确认训练参数、checkpoint 和数据摘要。
5. 看 dataset registry，确认数据版本和 sha256。
6. 交给 eval-module 跑评测，形成发布判断。

这条链路就是：

```text
dataset -> run -> checkpoint -> export -> eval -> release decision
```

如果任何一环断了，发布判断都会变弱。

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
list-datasets
diff-datasets
list-runs
list-exports
```

关键产物：

```text
outputs/dataset_registry.jsonl
outputs/run_history.jsonl
outputs/export_history.jsonl
outputs/<run>/run_manifest.json
outputs/<run>/artifacts_manifest.json
outputs/<run>/checkpoints/checkpoint_index.json
```

这些实现都还是学习型 mock，但它们表达了真实训练系统很重要的结构：数据、训练、checkpoint、导出和历史必须连起来。

## 如何阅读一个训练目录

学习时建议按这个顺序：

1. 先看 `run_manifest.json`，确认本次 run 的入口和文件关系。
2. 看 `data/dataset_summary.json`，确认数据规模、role 分布和 sha256。
3. 看 `data/dataset_registry_entry.json`，确认 dataset id/version。
4. 看 `training_args.json` 和 `trainer_state.json`，确认训练配置。
5. 看 `metrics/train_metrics.json` 和 `logs/events.jsonl`，确认训练过程。
6. 看 `checkpoints/checkpoint_index.json`，确认 checkpoint 和 adapter hash。
7. 看 `artifacts_manifest.json`，确认文件清单和 artifact 信息。
8. 最后看 run/export history，确认它进入了长期追踪。

这个顺序会比直接打开 checkpoint 更容易理解。

## 学习阶段和真实训练的区别

当前 `finetune-demo` 不是真实训练框架。
它不会真的消耗 GPU 训练模型，也不会替代 Transformers、PEFT、Unsloth、DeepSpeed 或 Megatron 类工具。

它的目标是让你先学会训练工程对象：

- 数据要有版本
- run 要有 manifest
- checkpoint 要有索引
- export 要有历史
- artifact 要能反查
- 微调结果必须接 eval

当这些结构清楚以后，再接真实训练栈才不会乱。

## 常见误区

### “有 checkpoint 就算训练完成”

不够。
没有数据摘要、训练配置、metrics、manifest 和 history，checkpoint 很难被解释。

### “Export 只是复制文件”

不是。
export 是把训练中间产物整理成可交付资产，并保留 lineage 的过程。

### “数据文件名没变，数据就没变”

不一定。
要看 sha256、dataset version、record count 和 role counts。

### “Mock 训练没有学习价值”

如果目标是学算法，mock 不够。
如果目标是学训练工程结构，mock 很有价值，因为它让你先看清 artifact 边界。

### “训练指标好就可以发布”

不一定。
训练指标必须接 eval。发布判断应该来自评测、样本分析和 release gate，而不是只看训练 loss。

## 学完应该能回答

读完这一页后，你应该能回答：

1. 为什么训练 run 不应该只留下 checkpoint？
2. dataset summary、dataset registry、run history 分别解决什么问题？
3. checkpoint index 为什么对后续 resume/export 有意义？
4. export 和 checkpoint 的边界是什么？
5. 当前仓库如何把 dataset、run、checkpoint、export 和 eval 连接成资产链路？

## 继续阅读

- [LoRA、QLoRA 与 PEFT](/05-finetuning-training/01-lora-qlora-peft)
- [数据集、Runs 与 Checkpoints](/05-finetuning-training/04-datasets-runs-checkpoints)
- [实验追踪、History 与可复现性](/05-finetuning-training/06-experiment-tracking-history-reproducibility)
- [Finetune 到 Eval 的资产链路案例](/11-case-studies/03-finetune-to-eval-asset-lineage)
