# 05. Finetuning Training

> 本页解决：一次训练为什么不应该只剩一个模型文件，而要留下可复现资产。
> 读完能做：解释 dataset registry、run manifest、checkpoint index、export manifest 和 lineage 的关系。
> 关联代码：`projects/finetune-demo`、`projects/eval-module`。
> 验证命令：`PYTHON=.venv/bin/python make infra-smoke`。

这一组讲的是“模型能力怎么通过训练迭代出来”。

这里的重点不是一上来跑一个很重的 GPU 训练，也不是把所有训练框架参数都背下来。更重要的是先理解：

> 一次训练为什么不应该只剩一个模型文件，而应该留下可复盘、可比较、可导出、可评测的工程资产？

很多人第一次学微调，会把注意力全部放在“怎么开始训练”。但真实工程里，更难的问题往往在训练前后：

- 数据集从哪里来，版本是什么
- 为什么选择 SFT、DPO 或其他目标
- 训练参数如何记录
- checkpoint 如何命名和保留
- adapter 如何导出
- 训练结果如何进入 eval
- 多次实验如何比较
- 失败后如何恢复和复现

这一章就是围绕这些问题展开。

## 微调不是万能按钮

微调经常被误解成“模型回答不好就训练一下”。这很危险。

在真实项目里，很多问题不应该先微调：

- prompt 没写清楚
- RAG 检索质量差
- 工具调用链路不稳定
- evaluation 还没有建立
- 业务目标没有定义
- 数据质量很差
- 只是想让模型记住少量事实

这些问题如果直接进入训练，很可能只是把混乱固化进模型。

所以本模块会反复强调：先判断是否需要微调，再谈训练技术。

## 先问：这个问题真的该训练吗

在真实项目里，“要不要微调”通常比“怎么微调”更难。

可以先用这张表做判断：

| 问题类型 | 更优先的手段 | 什么时候才考虑微调 |
| --- | --- | --- |
| 知识缺失 | RAG、工具调用、知识库更新 | 知识表达需要稳定内化到行为里 |
| 格式不稳定 | Prompt、schema、约束解码 | 大量同类格式样本已经沉淀 |
| 风格不一致 | Prompt、few-shot、系统消息 | 风格要求长期稳定且样本充足 |
| 任务能力弱 | 更强 base model、评测集、数据分析 | 目标任务清楚，数据质量可控 |
| 偏好不符合 | 人工反馈、DPO 数据准备 | 有成对偏好数据，且评测能覆盖风险 |
| 工具链失败 | 修业务逻辑、修检索、修解析 | 通常不应该靠微调解决 |

这张表的重点是：微调不是第一反应。你先要证明问题属于模型行为层，而不是系统链路、数据来源或评测缺失。

## 这一章关注的训练工程对象

当前学习站里，训练系统会围绕几个核心对象展开。

### Dataset

Dataset 不只是一个 JSONL 文件。它应该有：

- schema
- role 分布
- 样本数量
- 数据来源说明
- 版本或 hash
- 质量检查结果
- 与 run 的对应关系

没有 dataset 记录，就很难解释模型为什么变了。

### Run

Run 是一次训练实验的完整记录。它应该回答：

- 这次训练用的是什么数据
- 训练目标是什么
- 参数是什么
- 输出了哪些 checkpoint
- 是否成功
- 花了多久
- 产物在哪里

Run 是训练可复现的核心单位。

### Checkpoint

Checkpoint 不是临时文件。它是训练过程中的可恢复、可比较节点。

一个 checkpoint 如果没有 manifest、step、指标、路径和状态，就很难被后续系统安全使用。

### Export

Export 是把训练产物变成可部署或可评测资产的过程。

对 LoRA/QLoRA 来说，export 可能是 adapter；对完整模型来说，可能是 merged model 或部署包。无论形式如何，export 都应该保留 lineage：它来自哪个 run、哪个 dataset、哪个 checkpoint。

### History

History 让多次训练能被横向观察。没有 history，你只有一堆目录；有了 history，才有实验轨迹。

## 训练资产为什么比训练命令更重要

一次训练命令可能只运行十几分钟或几个小时，但训练资产会影响后续很多事情：

- eval 要知道 candidate 来自哪个 export
- 发布要知道 export 来自哪个 checkpoint
- 复现要知道 checkpoint 来自哪个 run
- 审计要知道 run 使用哪个 dataset
- 回滚要知道哪个版本可以安全恢复
- 继续训练要知道上次训练停在哪里

如果这些关系没有记录，训练就会变成“当时某台机器上跑过一次”。这种结果很难进入团队协作，也很难进入公开学习项目。

所以当前 `finetune-demo` 即使不跑真实 GPU 训练，也要保留 dataset registry、run manifest、checkpoint index、export manifest 和 history。它训练的是资产意识。

## 推荐阅读顺序

1. [LoRA、QLoRA、PEFT](/05-finetuning-training/01-lora-qlora-peft)
2. [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)
3. [Unsloth 与训练栈](/05-finetuning-training/03-unsloth-training-stack)
4. [数据集、Run、Checkpoint](/05-finetuning-training/04-datasets-runs-checkpoints)
5. [SFT、DPO 与训练目标](/05-finetuning-training/05-sft-dpo-and-training-objectives)
6. [实验追踪、History、复现](/05-finetuning-training/06-experiment-tracking-history-reproducibility)
7. [什么时候该微调](/05-finetuning-training/07-when-to-finetune)
8. [从 Demo Training 到真实训练系统](/05-finetuning-training/08-from-demo-training-to-real-training-system)

这个顺序先讲轻量微调方法，再讲训练资产，再讲工具栈和数据对象，最后回到目标选择、复现和真实迁移。

## 当前仓库如何体现训练工程

`projects/finetune-demo` 是一个学习型训练项目。它不会真的跑大模型训练，但会把训练系统的资产层先保留下来：

- train CLI
- export CLI
- config loading
- dataset validation
- dataset summary
- dataset registry
- run state
- run history
- checkpoint index
- artifacts manifest
- export manifest
- export history
- dataset diff
- list-runs / list-exports / list-datasets

这些对象比一次 mock 训练本身更重要。

因为未来你把内部 trainer 换成真实 PEFT、TRL、Unsloth 或其他训练框架时，这些资产边界仍然应该保留。

## 一个训练 run 应该讲得清楚什么

一个训练 run 至少应该回答这些问题：

```text
这次训练为什么发生？
使用了哪份 dataset？
数据是否通过 schema 和质量检查？
训练目标是 SFT、DPO 还是别的？
关键参数是什么？
产出了哪些 checkpoint？
最终选择哪个 checkpoint export？
export 能否追溯到 run 和 dataset？
后续 eval 如何引用这个 export？
```

如果这些问题答不上来，即使训练命令成功，工程上也仍然不完整。

## 和 Eval 模块怎么连起来

训练不是终点。训练输出必须进入评测。

一条合理链路应该是：

```text
Dataset
  -> Train Run
  -> Checkpoint
  -> Export
  -> Eval Run
  -> Compare Report
  -> Release Decision
```

如果训练系统只保存 checkpoint，却不能告诉 eval 这个 checkpoint 来自哪个 dataset 和 run，那么发布判断会很脆弱。

所以本模块会不断强调 lineage。它听起来像管理细节，但实际上是质量判断的基础。

## 从 notebook 到训练系统的差别

Notebook 很适合探索，但训练系统还需要处理协作和复现。

| 维度 | Notebook 常见状态 | 训练系统应该提供 |
| --- | --- | --- |
| 数据 | 手动加载某个文件 | dataset registry 和 summary |
| 参数 | 写在 cell 里 | config 和 run manifest |
| 产物 | 输出到临时目录 | checkpoint index 和 artifacts manifest |
| 记录 | 靠人截图或复制日志 | run history 和 structured metadata |
| 导出 | 手动挑文件 | export manifest 和 lineage |
| 评测 | 训练后临时看几条样本 | 接入 eval run 和 compare |

这个差别不是为了复杂而复杂，而是为了让训练结果能被别人理解、复现、比较和继续使用。

## 读这一章时应该带着哪些问题

不要只问“怎么训练”。更好的问题是：

- 这个问题真的需要微调吗
- 数据集是否足够干净、稳定、可追踪
- 训练目标是 SFT、DPO，还是别的
- 这次 run 如何被复现
- checkpoint 如何被索引和清理
- export 如何证明来源
- 训练结果如何进入 eval
- 多次实验如何比较
- 失败后如何从证据里定位原因

这些问题会让你更接近真实训练系统，而不是只停在 notebook。

## 学完这一章应该能回答的问题

读完后，你应该能解释：

- LoRA、QLoRA、PEFT 大致解决什么问题
- SFT 和 DPO 的目标差异
- 为什么 dataset registry 很重要
- 为什么 run manifest 不是形式主义
- checkpoint 和 export 的边界在哪里
- 实验追踪为什么影响复现
- 什么时候不该微调
- demo training 如何迁移到真实训练系统

如果这些问题能回答，你就已经从“跑一个训练脚本”走向“管理训练资产”了。

## 最小实践路线

建议这样动手：

1. 查看 `finetune-demo` 的 sample dataset。
2. 运行一次 train，生成 run state 和 checkpoint index。
3. 查看 dataset registry。
4. 运行 export，生成 export manifest。
5. 用 list-runs、list-exports、list-datasets 看索引。
6. 修改 dataset 后运行 diff-datasets。
7. 想象这个 export 如何进入 eval-module 做对比。

这条路线能让你把训练过程看成一条资产链，而不是一个孤立命令。

## 建议做一个资产追溯练习

完成最小实践后，可以用下面模板写一次追溯：

```text
Export:
来自哪个 checkpoint:
checkpoint 属于哪个 run:
run 使用哪个 dataset:
dataset 的样本数和 hash:
这次训练目标:
后续 eval 应该如何引用:
如果结果异常，优先排查哪里:
```

这份追溯写得越清楚，你越能理解真实训练平台为什么需要 registry、manifest、history 和 lineage。

## 常见误区

### 误区一：微调就是让模型记住知识

很多知识更新更适合 RAG 或工具调用。微调更适合稳定行为、格式、风格、任务能力和偏好。

### 误区二：训练成功就是 loss 降了

Loss 是信号之一，但最终要看目标任务、样本表现、回归风险和发布门禁。

### 误区三：checkpoint 越多越好

Checkpoint 要能索引、解释、清理和复现。没有管理的 checkpoint 只会制造混乱。

### 误区四：真实训练系统的第一步是接 GPU

接 GPU 很重要，但更早要稳定 dataset、run、manifest、export 和 eval 关系。

### 误区五：训练和部署是两件完全分开的事

训练产物最终要被部署或评测。没有 export lineage 和发布判断，训练很难进入工程闭环。

### 误区六：数据质量可以训练后再看

不建议。数据问题进入训练后会变得更难定位。最好在训练前就保留 summary、schema 检查、role 分布、样本数量和来源说明。
