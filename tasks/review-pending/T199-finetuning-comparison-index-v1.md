Task ID: T199
Task Title: 产出 finetuning comparison-index v1
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T165/T173/T174，产出 finetuning comparison-index v1，比较 LoRA、QLoRA、PEFT、Unsloth 四个对象的定位、所处层级、典型使用场景、与本项目的关系。

Result:

# Finetuning Comparison Index v1

## 比较对象

- LoRA
- QLoRA
- PEFT
- Unsloth

## 定位比较

| 对象 | 定位 | 来源 |
|------|------|------|
| **LoRA** | 底层微调方法，通过在预训练权重旁添加低秩矩阵实现参数高效微调 | https://arxiv.org/abs/2106.09685 |
| **QLoRA** | LoRA + 4-bit 量化，在 LoRA 基础上引入 NF4 数据类型和双重量化，进一步降低显存 | https://arxiv.org/abs/2305.14314 |
| **PEFT** | Hugging Face 维护的统一框架，封装 LoRA、QLoRA、Prefix Tuning、Prompt Tuning 等多种方法 | https://github.com/huggingface/peft |
| **Unsloth** | 微调加速层，通过自研 CUDA kernel 加速 LoRA/QLoRA 训练阶段（2x 速度、50% 显存减少），底层依赖 PEFT/TRL/PyTorch | https://github.com/unslothai/unsloth |

## 所处层级比较

| 对象 | 所处层级 | 说明 | 来源 |
|------|---------|------|------|
| **LoRA** | 方法层 | 底层微调方法，不依赖特定框架 | https://arxiv.org/abs/2106.09685 |
| **QLoRA** | 方法层 | LoRA 的进阶形式，同样属于方法层 | https://arxiv.org/abs/2305.14314 |
| **PEFT** | 接口/框架层 | 封装多种方法，提供统一 API | https://github.com/huggingface/peft |
| **Unsloth** | 加速层 | PEFT 接口下的加速内核，不改变方法本身 | https://github.com/unslothai/unsloth |

层级关系：
```
接口层：PEFT（框架封装）
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
| **Unsloth** | 需要加速 LoRA/QLoRA 训练；降低训练时间和显存占用 | https://github.com/unslothai/unsloth |

## 与本项目关系

| 对象 | 与本项目关系 |
|------|------------|
| **LoRA** | finetune-demo 模块的核心微调路径之一 |
| **QLoRA** | finetune-demo 模块的可选路径，适合低显存场景 |
| **PEFT** | finetune-demo 的微调接口层，本项目通过 PEFT API 调用 LoRA/QLoRA |
| **Unsloth** | finetune-demo 的可选加速层，通过 PEFT 接口集成，不改变上层 API |

Sources:
1. https://arxiv.org/abs/2106.09685 — LoRA 原始论文
2. https://arxiv.org/abs/2305.14314 — QLoRA 原始论文
3. https://github.com/huggingface/peft — PEFT 主仓库
4. https://github.com/unslothai/unsloth — Unsloth 主仓库

Risk of Staleness:
- PEFT 库版本更新快，具体 API 以实际安装版本为准
- Unsloth 更新频繁，加速效果以实际测试为准
- LoRA 新变体（DoRA、GaLoRA 等）快速涌现，PEFT 集成状态实时变化

Out of Scope Kept:
- 未写完整训练实践
- 未做性能横评
- 未写分布式训练方案

Need Codex Review On:
- finetune-demo 模块中 PEFT 和 Unsloth 的实际集成方式（以实际实现为准）
