# LoRA、QLoRA、PEFT

LoRA、QLoRA、PEFT 经常一起出现，因为它们都围绕同一个现实问题：

> 我想让模型更适合某个任务，但我不想、也通常不能全量训练整个大模型。

如果每次适配任务都更新全部参数，成本会非常高：

- 需要更多显存
- 训练更慢
- checkpoint 更大
- 存储和版本管理更重
- 多任务、多客户、多版本很难维护

所以工程里出现了很多“参数高效微调”的方法。
它们的共同目标不是重新训练一个模型，而是用更小代价让模型往目标任务方向移动一段。

## 先理解全量微调为什么重

假设一个模型有几十亿甚至上百亿参数。
全量微调意味着训练过程中要更新大量参数，并保存完整模型权重。

这会带来几个问题：

1. 显存压力大。
2. 训练成本高。
3. 每个任务都保存一份完整模型很浪费。
4. 多个微调版本之间很难管理。
5. 回滚、比较、合并和发布都变重。

在学习阶段，你不需要马上掌握所有训练细节。
只要先建立一个直觉：

> 全量微调像是重新改造整栋楼；参数高效微调更像是在关键位置加装可替换模块。

LoRA、QLoRA、PEFT 就是在这个背景下出现的。

## PEFT：先理解大类

PEFT 是 Parameter-Efficient Fine-Tuning，参数高效微调。

它不是单个方法，而是一类方法的统称。
这类方法的共同思想是：

- 冻结大部分原模型参数
- 只训练少量新增参数或局部参数
- 用较小训练成本适配任务
- 让微调产物更容易保存、切换和管理

LoRA 和 QLoRA 都可以放在 PEFT 的大框架下理解。

所以学习顺序建议是：

```text
先理解 PEFT 为什么存在
再理解 LoRA 怎么做轻量增量
最后理解 QLoRA 如何进一步降低资源压力
```

## LoRA：训练一个低秩增量

LoRA 可以先这样理解：

> 不直接大规模改原模型权重，而是在部分线性层旁边训练一个低秩增量。

更通俗一点：

原模型像一条已经修好的主干道路。
全量微调是把整条路重新施工。
LoRA 是在关键路口加一些可拆卸的引导设施，让车流更适合某个目标方向。

训练时，原模型大部分参数冻结。
LoRA 只训练新增的小矩阵。
保存时，也主要保存这些 adapter 权重。

这带来几个工程好处：

- 训练参数少
- 显存压力小
- 产物小
- 多任务可以保存多个 adapter
- 回滚和切换更方便
- 基座模型和任务增量可以分开管理

这就是为什么 LoRA 在学习和工程实践里都很常见。

## LoRA 不是魔法

LoRA 不是“低成本必然高质量”。
它有自己的边界。

如果任务和基座模型能力差距很大，LoRA 未必够。
如果数据质量很差，LoRA 也只是更快地学到坏模式。
如果评测不完整，adapter 看似有效，实际可能只是在训练集附近表现好。

所以 LoRA 的关键问题不是“能不能训练”，而是：

- 数据是否代表目标任务
- 训练后是否真的改善
- 是否有回归风险
- adapter 如何命名、保存、发布
- 如何追踪它来自哪个数据集和基座模型

这就是为什么本项目会把 finetune 和 eval 放在同一个学习闭环里。

## QLoRA：进一步压低资源门槛

QLoRA 可以先理解成：

> 在量化基座模型的基础上做 LoRA，使微调实验对显存更友好。

它的学习价值在于让你看到一个重要方向：

训练系统不只是“算法”，也是资源工程。

很多人想做微调，但没有非常豪华的 GPU。
如果能用更低显存做实验，学习和迭代门槛就会下降。

QLoRA 这类路线通常会涉及：

- 低比特量化
- 冻结量化后的基座模型
- 训练 LoRA adapter
- 在质量和资源之间做取舍

你不需要一开始记住所有细节。
先抓住重点：

> QLoRA 是为了让轻量微调在更受限资源下变得更可行。

## LoRA 和 QLoRA 的关系

可以粗略这样理解：

| 维度 | LoRA | QLoRA |
| --- | --- | --- |
| 核心思想 | 训练低秩 adapter | 在量化基座上训练 LoRA adapter |
| 主要收益 | 减少可训练参数和产物大小 | 进一步降低显存门槛 |
| 关注重点 | adapter 训练与管理 | 量化、显存和训练稳定性 |
| 共同点 | 不全量更新整个模型 | 都属于 PEFT 思路 |

它们不是互斥概念。
QLoRA 可以看成在更省资源设置下应用 LoRA 思路。

## Adapter 是训练产物，不只是一个文件

学习微调时，一个很重要的工程直觉是：

> 微调产物不是“训练完有个文件”这么简单，而是一组需要可追溯、可复现、可评测的资产。

一个 adapter 至少要知道：

- 基座模型是什么
- 数据集是什么
- 数据版本是什么
- 训练参数是什么
- 训练代码版本是什么
- checkpoint 来自哪一步
- export 是什么时候生成的
- eval 结果如何
- 是否通过发布门禁

如果这些信息丢了，adapter 就很难进入真实工程流程。

这也是当前仓库 `finetune-demo` 的重点：它不追求真实 GPU 训练，而是保留训练资产该有的结构。

## 微调和评测必须连在一起

很多学习材料会把 fine-tuning 当成一个独立主题：

```text
准备数据 -> 训练 -> 保存模型
```

但在 AI Infra 里，更完整的链路应该是：

```text
准备数据 -> 训练 -> 导出 adapter -> 评测 -> 比较 baseline -> 决定是否发布
```

如果没有评测，微调只是“做了一次训练”。
你不知道它是否真的改善，也不知道是否引入退化。

所以一个微调系统至少要和 eval 系统共享一些信息：

- model id
- dataset id
- run id
- checkpoint id
- export path
- eval result
- comparison report
- release recommendation

这就是训练资产化。

## 什么时候该微调

微调不是万能答案。

更合理的顺序通常是：

1. 先确认 prompt / system instruction 是否足够。
2. 再确认 RAG 或工具调用是否能解决知识问题。
3. 再看是否有稳定、可代表目标任务的数据。
4. 再考虑微调。
5. 微调后必须评测和回归。

适合微调的场景通常包括：

- 固定格式输出
- 特定风格或语气
- 特定领域任务模式
- 已有模型会做但不够稳定的能力
- 有足够高质量示例数据

不适合直接微调的情况：

- 只是缺少最新知识
- 数据很少且质量差
- 需求还在频繁变化
- 没有评测集
- 不知道成功标准

这些判断会在 [什么时候该微调](/05-finetuning-training/07-when-to-finetune) 里继续展开。

## 和当前仓库怎么对应

当前 `projects/finetune-demo` 是学习型训练资产项目。
它不会执行真实大模型训练，但保留了工程结构：

- `train`
- `save`
- `export`
- `list-runs`
- `list-datasets`
- `diff-datasets`
- `list-exports`
- run manifest
- checkpoint index
- export manifest
- dataset registry
- history
- lineage

你可以重点看：

- `projects/finetune-demo/src/finetune_demo/trainer/`
- `projects/finetune-demo/src/finetune_demo/export/`
- `projects/finetune-demo/tests/test_trainer.py`
- [Finetune 复现资产 Lab](/07-hands-on-labs/04-finetune-reproducibility-lab)
- [训练产物复现案例](/11-case-studies/03-finetune-to-eval-asset-lineage)

这些内容会帮助你把“LoRA/QLoRA/PEFT”从方法名变成工程资产链路。

## 一个学习任务

你可以这样练习：

1. 运行一次 `finetune-demo train`。
2. 打开 run manifest，看基座模型、数据集和训练参数。
3. 查看 checkpoint index。
4. 运行 export。
5. 打开 export manifest。
6. 追踪 export manifest 能否回到 run、checkpoint 和 dataset。
7. 思考：如果这个 adapter 要发布，还缺哪些 eval 证据？

这个练习不是为了训练出好模型，而是为了理解一个训练产物怎样变成可审计资产。

## 常见误区

### 误区 1：以为 LoRA 一定比 prompt 好

不一定。
如果问题可以通过 prompt、RAG 或工具解决，微调可能增加不必要的复杂度。

### 误区 2：只保存 adapter，不保存上下文

adapter 文件本身不够。
你还需要保存数据、训练配置、基座模型、checkpoint、评测结果和 lineage。

### 误区 3：没有评测就宣布微调成功

训练 loss 下降不等于业务质量提升。
必须用 eval 和 sample review 判断。

### 误区 4：忽略数据质量

微调会放大数据里的模式。
如果示例混乱、格式不一致或目标不清楚，模型也会学得混乱。

## 学完这一页应该能回答

- PEFT 是什么大类？
- LoRA 为什么能降低训练和保存成本？
- QLoRA 解决了哪类资源问题？
- adapter 为什么是一种工程资产？
- 微调为什么必须和 eval 连起来？
- 当前 `finetune-demo` 保留了哪些训练资产结构？

## 下一步

继续读：

- [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)
- [数据集、Run、Checkpoint](/05-finetuning-training/04-datasets-runs-checkpoints)
- [什么时候该微调](/05-finetuning-training/07-when-to-finetune)
- [从 Demo Training 到真实训练系统](/05-finetuning-training/08-from-demo-training-to-real-training-system)
