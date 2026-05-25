# finetune-demo Sample Config Catalog v1

## Task ID: T904
## Title: finetune-demo Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T804 training config map，产出训练配置样例模板。

---

# finetune-demo Sample Config Catalog v1

## 概述

本文档定义 finetune-demo 的 `configs/` 目录下的配置样例模板。

## 目录结构

```
configs/
├── lora_config_example.yaml    # LoRA 配置样例
├── qlora_config_example.yaml    # QLoRA 配置样例
└── README.md                   # 说明文档
```

## `configs/lora_config_example.yaml`

```yaml
# finetune-demo — LoRA Config Example
# 用法：finetune-demo train --config configs/lora_config_example.yaml

training:
  method: "lora"  # lora | qlora | sft

  model:
    name_or_path: "Qwen/Qwen2.5-0.5B-Instruct"
    trust_remote_code: true

  output_dir: "./models/lora"
  num_train_epochs: 3
  per_device_train_batch_size: 4
  gradient_accumulation_steps: 4
  learning_rate: 2.0e-4
  warmup_steps: 100
  logging_steps: 10
  save_steps: 500
  max_seq_length: 512
  fp16: true  # 混合精度

lora:
  r: 16
  lora_alpha: 32
  target_modules:
    - "q_proj"
    - "v_proj"
  lora_dropout: 0.05
  bias: "none"
  task_type: "CAUSAL_LM"

# Data settings
data:
  train_file: "./data/train.jsonl"
  val_file: null  # null = no validation split
  text_field: "instruction"  # JSONL 中的指令字段
  train_on_inputs: false
  cutoff_len: 512

# Logging
logging:
  use_wandb: false
  wandb_project: "finetune-demo"
  tensorboard: true
  log_dir: "./runs"
```

来源：https://github.com/huggingface/peft — PEFT LoRA config

## `configs/qlora_config_example.yaml`

```yaml
# finetune-demo — QLoRA Config Example
# 用法：finetune-demo train --config configs/qlora_config_example.yaml

training:
  method: "qlora"

  model:
    name_or_path: "Qwen/Qwen2.5-0.5B-Instruct"
    trust_remote_code: true

  output_dir: "./models/qlora"
  num_train_epochs: 3
  per_device_train_batch_size: 4
  gradient_accumulation_steps: 4
  learning_rate: 2.0e-4
  warmup_steps: 100
  logging_steps: 10
  save_steps: 500
  max_seq_length: 512
  fp16: true

lora:
  r: 64
  lora_alpha: 16
  target_modules:
    - "q_proj"
    - "v_proj"
    - "k_proj"
    - "o_proj"
  lora_dropout: 0.05
  bias: "none"
  task_type: "CAUSAL_LM"

qlora:
  load_in_4bit: true
  bnb_4bit_compute_dtype: "float16"
  bnb_4bit_use_double_quant: true
  bnb_4bit_quant_type: "nf4"

# Data settings
data:
  train_file: "./data/train.jsonl"
  val_file: null
  text_field: "instruction"
  train_on_inputs: false
  cutoff_len: 512

# Logging
logging:
  use_wandb: false
  tensorboard: true
  log_dir: "./runs"
```

来源：https://arxiv.org/abs/2305.14314 — QLoRA paper

## LoRA vs QLoRA 参数对比

| 参数 | LoRA | QLoRA | 说明 |
|------|------|-------|------|
| `r` | 8-16 | 16-64 | 更高 rank 更强，但显存更大 |
| `lora_alpha` | 2*r | 2*r | 通常设为 2*r |
| `target_modules` | q_proj, v_proj | q,v,k,o_proj | QLoRA 可用更多模块 |
| `load_in_4bit` | false | true | QLoRA 专有 |
| 显存（7B） | ~16GB | ~5GB | 单卡可训练 |

## 训练配置决策树

```
GPU 显存 < 10GB
  → QLoRA + Unsloth（如支持）

10GB <= GPU 显存 < 20GB
  → QLoRA 或 LoRA（较小 r）

GPU 显存 >= 20GB
  → LoRA
```

## 数据集 JSONL 格式要求

```jsonl
{"instruction": "问题内容", "input": "可选输入", "output": "期望输出"}
{"instruction": "Translate to French", "input": "Hello", "output": "Bonjour"}
```

## Adapter 产物结构

```
./models/lora/
├── adapter/                    # save_adapter() 输出
│   ├── adapter_config.json    # PEFT 配置
│   ├── adapter_model.safetensors  # adapter 权重
│   └── README.md
├── checkpoint-500/            # 中间 checkpoint
│   ├── adapter_config.json
│   ├── adapter_model.safetensors
│   └── trainer_state.json
└── checkpoint-1000/
    └── ...
```

来源：https://github.com/huggingface/peft — PEFT adapter 保存格式

---

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL
3. https://arxiv.org/abs/2305.14314 — QLoRA paper
4. https://github.com/unslothai/unsloth — Unsloth

Risk of Staleness:
- PEFT/TRL 配置格式可能随版本变化

Out of Scope Kept:
- 未写 SFT 配置样例
- 未写 DPO 配置样例
