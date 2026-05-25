Task ID: T603
Task Title: Finetuning / Training Zero-Touch Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
T603 Finetuning / Training Zero-Touch Pack 收口 manifest。

Result:

# Finetuning / Training Zero-Touch Pack Manifest

## 包概述

本包为 Finetuning / Training 专题的 0 接管链式长跑包，7 个文件全部完成，围绕微调方法、框架、工具的选型和实践路径展开。

## 已完成交付物

### 1. T603-finetuning-sources-index-v3
PEFT / TRL / LoRA / QLoRA / bitsandbytes / Unsloth / preference-reward 相关稳定入口。

### 2. T603-finetuning-comparison-index-v3
方法（LoRA / QLoRA / 全参数）、框架（PEFT / TRL / Unsloth）、工具（量化 / DPO / PPO）的边界分开写。

### 3. T603-finetuning-practice-catalog-v3
10 个实践，从最小训练验证（F01-F03）到量化训练（F04-F05）、偏好优化（F06）、适配器管理（F07-F08）、模块联动（F09-F10）。

### 4. T603-finetune-demo-training-map-v2
finetune-demo 的可能训练路径：QLoRA / LoRA / SFT / DPO / Unsloth，以及训练后与 eval-module 的联动。

### 5. T603-finetuning-glossary-batch-07
12 个核心术语：DPO / RLHF / Reward Model / Preference Data / Adapter Merge / Safetensors / Checkpoint / Quantization / Target Modules / Gradient Checkpointing / Adapter / bitsandbytes。

### 6. T603-finetuning-decision-memo-v2
5 个决策点的资料级输入：LoRA vs QLoRA、DPO 第一阶段、Unsloth 启用条件、训练框架选型、训练监控工具。

### 7. T603-finetuning-training-pack-manifest
本文件，总结完成项、未定项、对下一包可复用输入。

## 各交付物关系

```
sources-index-v3（工具和来源）
    ↓
comparison-index-v3（方法/框架/工具边界）
    ↓
glossary-batch-07（术语定义）
    ↓
practice-catalog-v3（实践路径）
    ↓
training-map-v2（训练路径说明）
    ↓
decision-memo-v2（决策输入）
    ↓
manifest（本文件）
```

## 对下一包可复用的输入

### 供 T604（Cross-Project Systemization）使用
- T601-inference-stack-decision-memo-v1（推理栈决策输入）
- T602-observability-eval-decision-memo-v1（observability/evaluation 决策输入）
- T603-finetuning-decision-memo-v2（finetuning 决策输入）
- 三个 MVP 模块（inference-service / eval-module / finetune-demo）的接口草案

## 需要 Codex 最终判断的点

1. **MVP 阶段是否接受 QLoRA（4-bit）作为默认微调方法？**
2. **DPO 是否在 MVP 阶段排除？**
3. **Unsloth 是否作为默认加速工具？**
4. **训练监控是否强制使用 Langfuse？**

## 风险与依赖

- LoRA/QLoRA 超参数配置复杂，需要根据实际模型调整
- Unsloth 加速效果依赖 GPU 型号（Ampere/Hopper）
- DPO 需要高质量偏好数据集，数据准备成本高

Sources:
1. https://arxiv.org/abs/2106.09685 — LoRA
2. https://arxiv.org/abs/2305.14314 — QLoRA
3. https://arxiv.org/abs/2305.18290 — DPO
4. https://github.com/huggingface/peft — PEFT
5. https://github.com/huggingface/trl — TRL
6. https://github.com/unslothai/unsloth — Unsloth
7. https://langfuse.com/docs/observability/overview — Langfuse
