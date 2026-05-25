# finetune-demo Training Config Map v1

## Task ID: T804
## Task Title: finetune-demo Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T713 决策 memo、T703 boundary matrix，准备 finetune-demo 实施前包。

---

# finetune-demo Training Config Map v1

## 概述

本文档定义 LoRA、QLoRA、SFT 的配置参数映射，供 Codex 实施时参考。

---

## LoRA 配置

### 核心参数

| 参数 | 默认值 | 范围 | 说明 | MVP 建议 |
|------|-------|------|------|---------|
| `r` | 16 | 4-128 | rank，低秩矩阵维度 | 8-16 |
| `lora_alpha` | 32 | 1-2*r | 缩放因子 | 2*r |
| `target_modules` | `["q_proj", "v_proj"]` | — | 应用 LoRA 的模块 | q_proj, v_proj, k_proj, o_proj |
| `lora_dropout` | 0.05 | 0-0.5 | Dropout 概率 | 0.05 |
| `bias` | `"none"` | none/all/lora_only | Bias 处理 | none |
| `task_type` | `CAUSAL_LM` | — | 任务类型 | CAUSAL_LM |

### 显存估算

| 模型大小 | FP16 LoRA 显存 | 备注 |
|---------|---------------|------|
| 7B | ~16GB | base model |
| 13B | ~28GB | base model |
| 70B | ~140GB | base model |

来源：https://arxiv.org/abs/2106.09685

---

## QLoRA 配置

### 核心参数

| 参数 | 默认值 | 范围 | 说明 | MVP 建议 |
|------|-------|------|------|---------|
| `r` | 64 | 4-128 | rank | 16-64 |
| `lora_alpha` | 16 | 1-2*r | 缩放因子 | 2*r |
| `target_modules` | `["q_proj", "v_proj"]` | — | 应用 LoRA 的模块 | q_proj, v_proj, k_proj, o_proj |
| `load_in_4bit` | `True` | True/False | 4-bit 量化 | True |
| `bnb_4bit_compute_dtype` | `"float16"` | — | 计算精度 | float16 |
| `bnb_4bit_use_double_quant` | `True` | True/False | 双量化 | True |
| `bnb_4bit_quant_type` | `"nf4"` | nf4/fp4 | 量化类型 | nf4 |

### 显存估算

| 模型大小 | QLoRA 4-bit 显存 | 备注 |
|---------|----------------|------|
| 7B | ~5GB | base model |
| 13B | ~10GB | base model |
| 70B | ~35GB | base model |

来源：https://arxiv.org/abs/2305.14314

---

## SFT 配置（SFTTrainer）

### 核心参数

| 参数 | 默认值 | 说明 | MVP 建议 |
|------|-------|------|---------|
| `max_seq_length` | 512 | 最大序列长度 | 512-1024 |
| `dataset_text_field` | `None` | 数据集文本字段 | "text" |
| `packing` | `False` | 序列打包 | False（MVP） |
| `formatting_prompter` | `None` | 格式转换器 | 默认格式 |

来源：https://github.com/huggingface/trl

---

## 配置对比

| 参数 | LoRA | QLoRA | SFT |
|------|------|-------|-----|
| `r` | 8-16 | 16-64 | N/A |
| `lora_alpha` | 16-32 | 32-128 | N/A |
| `load_in_4bit` | False | True | False |
| `bnb_4bit_*` | N/A | True | N/A |
| `target_modules` | q,v | q,v,k,o | N/A |
| `bias` | none | none | all |

---

## Unsloth 配置

### 与 PEFT 的关系

Unsloth 是 PEFT 的加速实现，配置参数兼容 PEFT。

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="Qwen/Qwen2.5-7B",
    load_in_4bit=True  # 等同于 QLoRA
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "v_proj"]
)
```

来源：https://github.com/unslothai/unsloth

---

## 训练超参数

### 推荐配置

| 参数 | LoRA | QLoRA | SFT |
|------|------|-------|-----|
| `learning_rate` | 2e-4 | 2e-4 | 1e-5 ~ 2e-5 |
| `num_epochs` | 3 | 3 | 3 |
| `batch_size` | 4 | 4 | 4 |
| `gradient_accumulation_steps` | 4 | 4 | 4 |
| `warmup_steps` | 100 | 100 | 100 |
| `weight_decay` | 0.01 | 0.01 | 0.01 |

---

## 配置选择决策树

```
输入：GPU 显存
    │
    ├── < 10GB
    │     → QLoRA + Unsloth（如 GPU 兼容）
    │
    ├── 10GB - 20GB
    │     → QLoRA 或 LoRA
    │
    └── >= 20GB
          → LoRA

输入：是否需要 DPO
    │
    ├── 否
    │     → LoRA / QLoRA
    │
    └── 是
          → LoRA + TRL DPO Trainer（后续）
```

---

Sources:
1. https://arxiv.org/abs/2106.09685 — LoRA
2. https://arxiv.org/abs/2305.14314 — QLoRA
3. https://github.com/huggingface/peft — PEFT
4. https://github.com/huggingface/trl — TRL
5. https://github.com/unslothai/unsloth — Unsloth

Risk of Staleness:
- LoRA/QLoRA 超参数最佳实践可能随新研究更新

Out of Scope Kept:
- 未写分布式训练配置
