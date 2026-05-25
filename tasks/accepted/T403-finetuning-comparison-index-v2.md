Task ID: T403
Task Title: Finetuning Long-Run Pack v1
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T209-v1，产出 finetuning comparison-index v2，增加 TRL 为比较对象，补齐 v1 中缺失的方法层对比。

Result:

# Finetuning Comparison Index v2

## 比较对象

- LoRA
- QLoRA
- PEFT
- TRL
- Unsloth

## 定位比较

| 对象 | 定位 | 来源 |
|------|------|------|
| **LoRA** | 底层微调方法，通过在预训练权重旁添加低秩矩阵实现参数高效微调 | https://arxiv.org/abs/2106.09685 |
| **QLoRA** | LoRA + 4-bit NF4 量化，进一步降低显存，单卡 24GB GPU 可微调大模型 | https://arxiv.org/abs/2305.14314 |
| **PEFT** | Hugging Face 维护的统一框架，封装 LoRA、QLoRA、Prefix Tuning、Prompt Tuning 等多种方法 | https://github.com/huggingface/peft |
| **TRL** | Hugging Face 的训练框架，提供 SFT Trainer、DPO Trainer、PPO Trainer 等完整训练流程 | https://github.com/huggingface/trl |
| **Unsloth** | 微调加速层，通过自研 CUDA kernel 加速 LoRA/QLoRA 训练，底层依赖 PEFT/TRL/PyTorch | https://github.com/unslothai/unsloth |

## 所处层级比较

| 对象 | 所处层级 | 说明 | 来源 |
|------|---------|------|------|
| **LoRA** | 方法层 | 底层微调方法，不依赖特定框架 | https://arxiv.org/abs/2106.09685 |
| **QLoRA** | 方法层 | LoRA 的进阶形式，同样属于方法层 | https://arxiv.org/abs/2305.14314 |
| **PEFT** | 接口/框架层 | 封装多种方法，提供统一 API | https://github.com/huggingface/peft |
| **TRL** | 训练流程层 | 封装完整训练循环（SFT/DPO/PPO），支持 PEFT 接口 | https://github.com/huggingface/trl |
| **Unsloth** | 加速层 | PEFT 接口下的加速内核，不改变方法本身 | https://github.com/unslothai/unsloth |

层级关系：
```
训练流程层：TRL（SFT/DPO/PPO 训练循环）
    ↓
接口/框架层：PEFT（统一微调 API）
    ↓
加速层：Unsloth（PEFT 下加速内核）
    ↓
方法层：LoRA / QLoRA（底层微调方法）
```

## 典型使用场景

| 对象 | 典型使用场景 | 来源 |
|------|-------------|------|
| **LoRA** | 领域适配、任务定制；需要一定显存（单卡 A100 级别） | https://arxiv.org/abs/2106.09685 |
| **QLoRA** | 个人开发者或小团队；单卡 24GB GPU 微调大模型 | https://arxiv.org/abs/2305.14314 |
| **PEFT** | 通用微调工程；需要统一接口管理多种微调方法 | https://github.com/huggingface/peft |
| **TRL** | 需要完整训练流程（SFT/DPO）；偏好学习训练 | https://github.com/huggingface/trl |
| **Unsloth** | 需要加速 LoRA/QLoRA 训练；降低训练时间和显存占用 | https://github.com/unslothai/unsloth |

## 与本项目关系

| 对象 | 与本项目关系 | 来源 |
|------|------------|------|
| **LoRA** | finetune-demo 的核心微调方法之一 | https://arxiv.org/abs/2106.09685 |
| **QLoRA** | finetune-demo 的可选路径，适合低显存场景 | https://arxiv.org/abs/2305.14314 |
| **PEFT** | finetune-demo 的微调接口层，本项目通过 PEFT API 调用 LoRA/QLoRA | https://github.com/huggingface/peft |
| **TRL** | finetune-demo 的训练流程层，提供 SFT/DPO 训练器 | https://github.com/huggingface/trl |
| **Unsloth** | finetune-demo 的可选加速层，通过 PEFT 接口集成 | https://github.com/unslothai/unsloth |

Sources:
1. https://arxiv.org/abs/2106.09685 — LoRA 原始论文
2. https://arxiv.org/abs/2305.14314 — QLoRA 原始论文
3. https://github.com/huggingface/peft — PEFT 主仓库
4. https://github.com/huggingface/trl — TRL 主仓库
5. https://github.com/unslothai/unsloth — Unsloth 主仓库

Risk of Staleness:
- PEFT/TRL 版本更新快，具体 API 以实际安装版本为准
- Unsloth 更新频繁，加速效果以实际测试为准
- LoRA 新变体（DoRA、GaLoRA 等）快速涌现，PEFT 集成状态实时变化

Out of Scope Kept:
- 未写完整训练实践
- 未做性能横评
- 未写分布式训练方案

Need Codex Review On:
- finetune-demo 的默认微调路径选择（LoRA vs QLoRA）
- Unsloth 是否纳入 MVP
