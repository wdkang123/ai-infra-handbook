# finetune-demo LoRA Config Samples v1

## Task ID: T1104
## Title: finetune-demo Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# finetune-demo LoRA Config Samples

本文档定义 finetune-demo 的 LoRA / QLoRA 训练配置文件样本，对应真实文件 `finetune-demo/configs/lora/` 和 `finetune-demo/configs/qlora/`。

## 文件路径总览

| 文件 | 场景 | 精度 |
|---|---|---|
| `configs/lora/lora_config_qwen_05b.yaml` | Qwen2.5-0.5B LoRA | FP16 |
| `configs/qlora/qlora_config_qwen_05b.yaml` | Qwen2.5-0.5B QLoRA | NF4 (4-bit) |

---

## LoRA Config — Qwen2.5-0.5B-Instruct（FP16）

**对应文件：** `finetune-demo/configs/lora/lora_config_qwen_05b.yaml`

```yaml
# LoRA fine-tuning configuration for Qwen2.5-0.5B-Instruct
# Training: FP16 full fine-tuning with LoRA adapters

base_model: "Qwen/Qwen2.5-0.5B-Instruct"
output_dir: "./outputs/lora_qwen_05b"

# Training hyperparameters
per_device_train_batch_size: 2
gradient_accumulation_steps: 8
  # effective batch size = 2 * 8 = 16
learning_rate: 3.0e-4
num_train_epochs: 3
max_steps: -1
lr_scheduler_type: "cosine"
warmup_ratio: 0.03
logging_steps: 10
save_steps: 100
save_total_limit: 3

# LoRA configuration
lora_config:
  r: 16                        # LoRA attention dimension
  lora_alpha: 32               # LoRA scaling factor (alpha/r)
  lora_dropout: 0.05
  target_modules:
    - "q_proj"
    - "k_proj"
    - "v_proj"
    - "o_proj"
    - "gate_proj"
    - "up_proj"
    - "down_proj"
  bias: "none"
  task_type: "CAUSAL_LM"

# Quantization (standard LoRA: FP16, no quantization)
quantization:
  enabled: false

# Data
train_data_path: "data/samples/conversation_sample_01.jsonl"
max_seq_length: 1024

# Optimizer
optim: "adamw_torch"
lr_scheduler_kwargs:
  eta_min: 3.0e-5

# Precision
bf16: false
fp16: true

# Logging & checkpointing
report_to: "tensorboard"
logging_dir: "./outputs/lora_qwen_05b/logs"
```

---

## QLoRA Config — Qwen2.5-0.5B-Instruct（NF4）

**对应文件：** `finetune-demo/configs/qlora/qlora_config_qwen_05b.yaml`

```yaml
# QLoRA fine-tuning configuration for Qwen2.5-0.5B-Instruct
# Training: 4-bit NF4 quantization + LoRA = QLoRA
# Memory efficient: ~6GB GPU memory for 0.5B model

base_model: "Qwen/Qwen2.5-0.5B-Instruct"
output_dir: "./outputs/qlora_qwen_05b"

# Training hyperparameters
per_device_train_batch_size: 4
gradient_accumulation_steps: 4
  # effective batch size = 4 * 4 = 16
learning_rate: 2.0e-4
num_train_epochs: 3
max_steps: -1
lr_scheduler_type: "cosine"
warmup_ratio: 0.03
logging_steps: 10
save_steps: 100
save_total_limit: 3

# LoRA configuration
lora_config:
  r: 64                        # higher r for QLoRA
  lora_alpha: 64               # alpha = r for QLoRA
  lora_dropout: 0.1
  target_modules:
    - "q_proj"
    - "k_proj"
    - "v_proj"
    - "o_proj"
    - "gate_proj"
    - "up_proj"
    - "down_proj"
  bias: "none"
  task_type: "CAUSAL_LM"

# NF4 Quantization (QLoRA-specific)
quantization:
  enabled: true
  load_in_4bit: true
  bnb_4bit_compute_dtype: "bfloat16"
  bnb_4bit_use_double_quant: true
  bnb_4bit_quant_type: "nf4"

# Data
train_data_path: "data/samples/conversation_sample_01.jsonl"
max_seq_length: 2048            # QLoRA allows longer context with NF4

# Optimizer
optim: "adamw_torch"
lr_scheduler_kwargs:
  eta_min: 2.0e-5

# Precision
bf16: true
fp16: false

# Logging & checkpointing
report_to: "tensorboard"
logging_dir: "./outputs/qlora_qwen_05b/logs"
```

---

## LoRA vs QLoRA 参数对比

| 参数 | LoRA (FP16) | QLoRA (NF4) |
|---|---|---|
| `load_in_4bit` | `false` | `true` |
| `bnb_4bit_quant_type` | N/A | `nf4` |
| `bnb_4bit_compute_dtype` | N/A | `bfloat16` |
| `lora.r` | 16 | 64 |
| `lora.alpha` | 32 | 64 |
| `lora.dropout` | 0.05 | 0.1 |
| `max_seq_length` | 1024 | 2048 |
| 预估 GPU 显存 | ~8 GB | ~6 GB |

---

## LoRA Target Modules（Qwen 系列）

所有 Qwen2.5 模型均使用相同的 target_modules：

```python
target_modules = [
    "q_proj",    # Query projection
    "k_proj",    # Key projection
    "v_proj",    # Value projection
    "o_proj",    # Output projection
    "gate_proj", # Gate (FFN up projection)
    "up_proj",   # FFN up projection
    "down_proj", # FFN down projection
]
```

---

## PEFT Adapter 合并脚本

训练完成后合并 LoRA adapter 到 base model：

```bash
# finetune-demo/scripts/merge_lora_adapter.sh
python -m peft.merge_peft_adapter \
  --base_model Qwen/Qwen2.5-0.5B-Instruct \
  --adapter_path ./outputs/qlora_qwen_05b/checkpoint-300 \
  --output_path ./outputs/merged_qwen_05b
```

---

Sources:
1. https://github.com/artidoro/qlora — QLoRA paper and config
2. https://github.com/huggingface/peft — PEFT library
3. https://docs.unsloth.org/ — Unsloth optimized LoRA

Risk of Staleness:
- PEFT/LoRA config schema is stable; QLoRA NF4 approach well-established
