# 从 Demo Training 到真实训练系统

当前 `finetune-demo` 是学习型训练骨架。它不会真的加载大模型、跑 GPU、保存真实 LoRA 权重，但它已经把训练系统里最应该先稳定的资产结构留下来了。

这一页回答一个进阶问题：

> 如果后续要把这个 demo 推向更真实的训练系统，应该按什么顺序推进，哪些边界必须保住？

答案不是“一步到位换成真实训练框架”。更稳的方式是先保住训练资产和验证闭环，再逐步替换内部执行。

## 当前 Demo 已经解决了什么

`finetune-demo` 已经保留了几类真实训练系统会需要的结构。

### 训练入口

它有 train CLI 和 config loading。也就是说，一次训练不是临时 notebook 操作，而是可以用命令和配置复现的动作。

### 数据检查

它会验证 dataset schema，并生成 dataset summary。训练系统必须先知道自己吃进去的是什么数据。

### Dataset Registry

它会登记 dataset entry，并支持 list / diff。这个能力看起来朴素，但它让后续多次训练可以追踪数据版本变化。

### Run State

它会记录一次 run 的状态、配置、数据摘要和产物位置。Run 是训练系统最重要的复盘单位。

### Checkpoint Index

它会生成 checkpoint index，说明哪些 checkpoint 存在、状态如何、路径在哪里。

### Export Manifest

它会记录 export 产物以及 lineage，让导出的 adapter 或模型包能追溯到 run、dataset 和 checkpoint。

### History

它会保留 run/export history，让多次实验不是散落目录，而是可横向查看的记录。

这些能力不依赖是否真实训练。它们是未来接入真实训练前应该先保住的系统骨架。

## 当前 Demo 还没有做什么

它还没有做满这些部分：

- 真实 GPU 训练
- Transformers / PEFT / TRL / Unsloth 深度接入
- 真实 LoRA adapter 权重保存
- resume from checkpoint
- 多 checkpoint 策略
- 分布式训练
- mixed precision 与显存优化
- 外部 experiment tracker
- 自动评测触发
- 模型仓库或 artifact store 集成

这些不是缺陷，而是刻意控制学习复杂度。

如果一开始就把所有真实训练能力都接上，读者很可能只看到工具命令，而看不清训练系统最重要的资产关系。

## 迁移原则

### 先保资产边界，再替训练执行

迁移时要先保住：

- dataset registry
- run manifest
- checkpoint index
- artifacts manifest
- export manifest
- run/export history
- validation command

然后再替换内部 trainer。

这样即使底层从 mock trainer 换成 PEFT 或 Unsloth，上层证据结构仍然稳定。

### 先单机清楚，再分布式复杂

不要一上来做多机多卡。

更稳的顺序是：

1. 单机小模型或小 adapter 跑通
2. 产物结构保持一致
3. eval 能消费 export
4. resume 和失败路径可验证
5. 再考虑分布式和大规模实验

训练系统的复杂度应该跟证据能力一起增长。

### 先让 Eval 接住，再扩大训练规模

如果训练结果不能进入 eval，训练规模越大，争论越大。

真实迁移中，每次训练升级都应该回答：

- 这个 export 如何被 eval-module 识别
- baseline 和 candidate 如何对比
- 哪些任务必须不退化
- 哪些样本需要人工复核
- 发布建议如何生成

训练和评测必须成对推进。

## 推荐迁移路线

### 第一步：接入真实数据预处理

先把 dataset pipeline 做得更真实：

- 支持 train / validation split
- 增加样本去重
- 增加格式规范化
- 保存数据质量报告
- 记录数据来源和版本

这一步不急着训练大模型。目标是让输入更可信。

### 第二步：替换 Mock Trainer

把内部 mock trainer 替换成真实训练执行，例如：

- Transformers Trainer
- TRL SFTTrainer
- PEFT LoRA / QLoRA
- Unsloth 加速路径

替换时不要破坏 run manifest 和 checkpoint index。外部 CLI 可以尽量保持兼容。

### 第三步：保存真实 Adapter 产物

真实 LoRA/QLoRA 训练后，要保存：

- adapter weights
- adapter config
- tokenizer 相关文件
- training config
- base model id
- checkpoint step
- export manifest

这里最容易漏的是 base model 和 tokenizer 信息。一旦漏掉，adapter 很难安全复现。

### 第四步：补 Resume 与失败恢复

真实训练会失败，尤其是长任务。

需要补：

- checkpoint resume
- interrupted run status
- failed run manifest
- partial artifact 标记
- retry policy
- cleanup policy

失败也要留下证据。没有失败证据的训练平台，只能靠记忆排查。

### 第五步：接入 Experiment Tracking

当 run 变多后，可以接：

- MLflow
- Weights & Biases
- TensorBoard
- 自建 metadata store

但外部 tracker 不应该替代本仓库里的 manifest。更好的做法是 manifest 保存本地可复盘信息，同时记录 tracker run id。

### 第六步：接入 Eval Gate

训练完成后自动触发 eval：

```text
train run
  -> export adapter
  -> eval baseline/candidate
  -> compare report
  -> recommendation
  -> release decision
```

这一步会把训练系统从“产物生成器”升级成“能力迭代闭环”。

### 第七步：进入更真实的发布和回滚

最后再考虑：

- 模型仓库
- artifact storage
- 权限控制
- 灰度发布
- 回滚策略
- 成本统计
- 多团队协作

这些属于生产化治理，不应该抢在训练资产和 eval gate 前面。

## 每次迁移都要检查什么

| 检查点 | 要回答的问题 |
| --- | --- |
| Dataset | 数据版本、schema、样本数量是否可追踪 |
| Config | 训练参数和 base model 是否记录 |
| Run | 这次实验能否复现 |
| Checkpoint | 路径、step、状态是否可索引 |
| Export | 产物是否能追溯到 run/dataset/checkpoint |
| History | 多次实验是否可比较 |
| Eval | 训练结果是否进入质量判断 |
| Failure | 失败时是否留下证据 |

如果某一步回答不了，就不应该急着扩大训练规模。

## 和当前文档怎么配合

阅读顺序建议：

1. [数据集、Run、Checkpoint](/05-finetuning-training/04-datasets-runs-checkpoints)
2. [Unsloth 与训练栈](/05-finetuning-training/03-unsloth-training-stack)
3. [实验追踪、History、复现](/05-finetuning-training/06-experiment-tracking-history-reproducibility)
4. [什么时候该微调](/05-finetuning-training/07-when-to-finetune)
5. [Finetune 真实训练迁移](/12-production-migration/04-finetune-real-training-migration)
6. [从 Run 到发布决策](/04-evaluation-observability/07-from-run-to-release-decision)

这条路径会把训练技术、资产治理和发布判断串起来。

## 最小演进任务

如果后续要继续写代码，可以按这个顺序拆任务：

1. 增加 dataset split 与数据质量报告。
2. 在 run manifest 中记录更完整 base model / tokenizer 字段。
3. 增加真实 PEFT adapter 目录结构示例。
4. 增加 failed run 与 interrupted run 示例。
5. 增加 eval handoff manifest。
6. 增加 export 后自动生成 eval candidate metadata。
7. 增加训练到评测的端到端案例复盘。

每个任务都不必一次做很大，但都要保留测试和输出证据。

## 常见误区

### 误区一：把 Mock Trainer 换掉就等于真实训练系统

不等于。真实训练系统还需要数据、run、checkpoint、export、history、eval 和失败恢复。

### 误区二：只要有外部 Tracker，本地 Manifest 就不重要

不对。外部 tracker 可能配置变化、权限变化或不可访问。本地 manifest 是仓库内可复盘的最低保障。

### 误区三：训练越真实，文档越可以少

恰好相反。真实训练更需要文档说明产物、路径、失败模式和验证方法。

### 误区四：先做大规模训练，再补评测

这会让训练结果无法判断。更好的顺序是先有最小 eval gate，再扩大训练能力。

### 误区五：Checkpoint 都应该永久保留

不一定。需要保留的是可解释、可复现、可追溯的 checkpoint。保留策略本身也应该写入系统设计。
