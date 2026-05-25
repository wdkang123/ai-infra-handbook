# finetune-demo .env.example Blueprint v1

## Task ID: T904
## Title: finetune-demo Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T804 training config map，产出 .env.example 模板。

---

# finetune-demo .env.example Blueprint v1

## 概述

本文档定义 finetune-demo 的 `.env.example` 模板。

## 模板全文

```bash
# ============================================================
# finetune-demo — .env.example
# ============================================================

# ---------- Base Model ----------
# HuggingFace model name 或本地路径
FINETUNE_MODEL_NAME=Qwen/Qwen2.5-0.5B-Instruct
FINETUNE_MODEL_TRUST_REMOTE_CODE=true

# ---------- Training Method ----------
# 训练方法: lora | qlora
FINETUNE_METHOD=lora

# ---------- LoRA Config ----------
FINETUNE_LORA_R=16
FINETUNE_LORA_ALPHA=32
FINETUNE_LORA_DROPOUT=0.05
FINETUNE_LORA_TARGET_MODULES=q_proj,v_proj

# ---------- QLoRA Config ----------
FINETUNE_QLORA_LOAD_IN_4BIT=true
FINETUNE_QLORA_BNB_COMPUTE_DTYPE=float16
FINETUNE_QLORA_BNB_USE_DOUBLE_QUANT=true
FINETUNE_QLORA_BNB_QUANT_TYPE=nf4

# ---------- Training Hyperparameters ----------
FINETUNE_OUTPUT_DIR=./models
FINETUNE_NUM_EPOCHS=3
FINETUNE_PER_DEVICE_BATCH_SIZE=4
FINETUNE_LEARNING_RATE=2e-4
FINETUNE_GRADIENT_ACCUMULATION_STEPS=4
FINETUNE_WARMUP_STEPS=100
FINETUNE_LOGGING_STEPS=10
FINETUNE_SAVE_STEPS=500
FINETUNE_MAX_SEQ_LENGTH=512

# ---------- Data ----------
# 数据集格式: jsonl (必须包含 instruction, output 字段)
FINETUNE_DATASET_PATH=./data/example_dataset.jsonl
FINETUNE_DATASET_TEXT_FIELD=instruction

# ---------- Adapter ----------
# Adapter 保存目录
FINETUNE_ADAPTER_DIR=./adapters

# ---------- Hardware ----------
# GPU 数量（Tensor 并行）
FINETUNE_NUM_GPUS=1

# ---------- Logging ----------
# WandB 日志（可选）
# WANDB_API_KEY=your-key-here
# WANDB_PROJECT=finetune-demo
FINETUNE_USE_WANDB=false

# TensorBoard 日志
FINETUNE_USE_TENSORBOARD=true
FINETUNE_TENSORBOARD_DIR=./runs

# ---------- Resume ----------
# 从 checkpoint 恢复训练
# FINETUNE_RESUME_FROM_CHECKPOINT=./models/lora/checkpoint-1000
```

## LoRA vs QLoRA 配置差异

| 配置项 | LoRA | QLoRA |
|--------|------|-------|
| `FINETUNE_METHOD` | `lora` | `qlora` |
| `FINETUNE_QLORA_LOAD_IN_4BIT` | — | `true` |
| `FINETUNE_QLORA_BNB_*` | — | 必须设置 |
| 显存需求 | ~16GB (7B) | ~5GB (7B) |

## 数据集格式

finetune-demo 使用 JSONL 格式，每行包含 `instruction` 和 `output` 字段：

```jsonl
{"instruction": "What is 2+2?", "input": "", "output": "4"}
{"instruction": "Translate to French", "input": "Hello", "output": "Bonjour"}
```

---

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL

Risk of Staleness:
- PEFT/TRL 环境变量尚未标准化

Out of Scope Kept:
- 未写多数据集配置
- 未写数据集流式加载配置
