# Finetune 产物证据

## 这一页看什么

Finetune 最容易被简化成：

> 跑一条 train，得到一个 checkpoint。

真实训练工程里，这远远不够。

当前 `finetune-demo` 虽然是学习型实现，但它已经把训练资产拆成了几类证据：

| 证据 | 回答的问题 |
| --- | --- |
| `run_manifest.json` | 这次训练是谁、用什么配置、什么时候跑的 |
| `training_args.json` | 训练参数是什么 |
| `trainer_state.json` | 训练状态和 metric 是什么 |
| `dataset_summary.json` | 数据集结构、hash、role 分布是什么 |
| `artifacts_manifest.json` | 训练留下了哪些文件 |
| `checkpoint_index.json` | checkpoint 怎么索引、hash 是什么 |
| `export_manifest.json` | 导出产物从哪个 checkpoint 来 |
| `dataset_registry_report.json` | 数据集登记和重复情况如何 |
| `run_index.json` | 多次训练如何索引 |
| `export_index.json` | 多次导出如何索引 |

## Run manifest

`run_manifest.json` 是训练复盘的入口。

它应该能说明：

- run id
- base model
- dataset path
- dataset version
- method，例如 LoRA / QLoRA
- output directory
- created time
- training args file
- artifacts manifest file

如果一个训练目录没有 manifest，你后面只能靠猜。

## Dataset summary

`dataset_summary.json` 适合先看数据是否可解释。

重点字段：

| 字段 | 含义 |
| --- | --- |
| `dataset_sha256` | 数据内容指纹 |
| `dataset_version` | 数据版本 |
| `record_count` | 样本数量 |
| `message_count` | message 数量 |
| `role_counts` | user/assistant/system 分布 |
| `duplicate_count` | 重复样本数量 |

它回答的是：

> 这次训练到底用了哪份数据？

如果 dataset hash 变了，训练结果就不能只归因于模型或参数变化。

## Artifacts manifest

`artifacts_manifest.json` 适合看训练目录有没有完整留下证据。

你应该确认：

- 是否有 `trainer_state.json`
- 是否有 `training_args.json`
- 是否有 `dataset_summary.json`
- 是否有 checkpoint 目录
- 是否有 events 或 history 文件

它回答的是：

> 这次 run 的产物是否足够复盘？

不要只看 checkpoint 文件存在与否。

## Checkpoint index

`checkpoint_index.json` 是 checkpoint 复现的关键。

它应该回答：

| 问题 | 需要的字段 |
| --- | --- |
| 有几个 checkpoint | checkpoint list |
| 最新 checkpoint 是哪个 | latest pointer |
| checkpoint 文件是否可校验 | file hash |
| 是否可 resume | resumable marker |
| checkpoint 来自哪个 run | run id / path |

当前 demo 可能只有一个 mock checkpoint，但结构对应真实训练里的多 checkpoint 场景。

## Export manifest

`export_manifest.json` 不只是“导出了一个 adapter”。

它应该说明：

- source checkpoint
- base model
- adapter path
- adapter hash
- export status
- duration
- lineage

它回答的是：

> 这个导出产物从哪里来？以后还能不能追溯？

如果 export manifest 不能追溯 checkpoint，那么它很难进入 eval 或 serving。

## Dataset registry report

数据集 registry 适合回答：

- 同一份数据是否被重复登记
- 不同 run 是否使用了同一 dataset sha
- 按 method / model 过滤后有哪些数据集
- left/right dataset diff 是否一致

这类证据特别适合在多人协作时使用。

如果两次训练结果不同，先看：

1. dataset sha 是否一致
2. dataset version 是否一致
3. role counts 是否一致
4. training args 是否一致

## Run index 和 export index

`run_index.json` 适合回答：

- 最近有哪些训练 run
- 每个 run 指向哪个 manifest
- 每个 run 指向哪个 checkpoint index
- model/dataset summary 如何分布

`export_index.json` 适合回答：

- 最近有哪些 export
- 哪个 export 成功或失败
- 平均 duration 是多少
- adapter hash 是否可见
- model/dataset summaries 是否可读

它们不是为了好看，而是为了后续 dashboard、CI、发布流程可以读取。

## 常见误读

| 误读 | 更稳的解释 |
| --- | --- |
| 有 checkpoint 就能复现 | 还需要 config、dataset、hash、run manifest |
| export 成功就能上线 | 还需要 eval、compatibility、serving 验证 |
| dataset path 一样就说明数据一样 | path 不能替代 sha256 |
| mock training 没价值 | mock training 在训练资产结构上仍然有学习价值 |

## 复盘模板

```text
run id：
base model：
dataset version：
dataset sha：
训练方法：
checkpoint index：
export manifest：
adapter hash：
能追溯到：
还不能证明：
下一步接 eval：
```

## 关联阅读

- [finetune-demo](/06-projects/04-finetune-demo)
- [Finetune 复现资产 Lab](/07-hands-on-labs/04-finetune-reproducibility-lab)
- [训练产物复现案例](/11-case-studies/03-finetune-to-eval-asset-lineage)
- [产物与文件索引](/09-reference/03-artifacts-and-files)
