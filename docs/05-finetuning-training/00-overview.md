# 05. Finetuning Training

这一组讲的是“模型能力怎么通过训练迭代出来”。

学习重点不是一开始就把训练系统做得很重，而是先理解：

- 训练 run 应该沉淀成什么
- LoRA / QLoRA / PEFT 在解决什么问题
- 为什么 checkpoint、manifest、history 这些工程资产很重要

推荐阅读顺序：

1. [LoRA、QLoRA、PEFT](/05-finetuning-training/01-lora-qlora-peft)
2. [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)
3. [Unsloth 与训练栈](/05-finetuning-training/03-unsloth-training-stack)
4. [数据集、Run、Checkpoint](/05-finetuning-training/04-datasets-runs-checkpoints)
5. [SFT、DPO 与训练目标](/05-finetuning-training/05-sft-dpo-and-training-objectives)
6. [实验追踪、History、复现](/05-finetuning-training/06-experiment-tracking-history-reproducibility)
7. [什么时候该微调](/05-finetuning-training/07-when-to-finetune)
8. [从 Demo Training 到真实训练系统](/05-finetuning-training/08-from-demo-training-to-real-training-system)

如果你想同步看代码，再配合：

- [finetune-demo 项目页](/06-projects/04-finetune-demo)
