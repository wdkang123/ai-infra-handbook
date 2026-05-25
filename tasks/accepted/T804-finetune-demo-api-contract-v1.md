# finetune-demo API Contract v1

## Task ID: T804
## Task Title: finetune-demo Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T304 MVP 设计，准备 finetune-demo 实施前包。

---

# finetune-demo API Contract v1

## 概述

本文档定义 finetune-demo 的训练接口契约。

---

## 接口总览

| 接口 | 方法 | 说明 | MVP 必须 |
|------|------|------|---------|
| `LoRATrainer` | Python API | LoRA 训练 | 是 |
| `QLoRATrainer` | Python API | QLoRA 训练 | 是 |
| `SFTTrainer` | Python API | SFT 训练 | 否 |
| `save_adapter()` | Python API | 保存 adapter | 是 |
| `load_adapter()` | Python API | 加载 adapter | 是 |

---

## Python API

### LoRATrainer

```python
from finetune_demo import LoRATrainer

trainer = LoRATrainer(
    model="Qwen/Qwen2.5-7B-Instruct",
    method="lora",
    output_dir="./models/lora",
    lora_config={
        "r": 16,
        "lora_alpha": 32,
        "target_modules": ["q_proj", "v_proj"],
        "lora_dropout": 0.05,
        "bias": "none"
    }
)

# 启动训练
trainer.train(
    dataset="path/to/dataset.jsonl",
    num_epochs=3,
    batch_size=4,
    learning_rate=2e-4
)

# 保存 adapter
adapter_path = trainer.save_adapter()

# 获取 adapter 路径
print(trainer.get_adapter_path())
```

来源：https://github.com/huggingface/peft

---

### QLoRATrainer

```python
from finetune_demo import QLoRATrainer

trainer = QLoRATrainer(
    model="Qwen/Qwen2.5-7B-Instruct",
    method="qlora",
    output_dir="./models/qlora",
    qlora_config={
        "r": 64,
        "lora_alpha": 16,
        "target_modules": ["q_proj", "v_proj"],
        "load_in_4bit": True,
        "bnb_4bit_compute_dtype": "float16",
        "bnb_4bit_use_double_quant": True,
        "bnb_4bit_quant_type": "nf4"
    }
)

trainer.train(dataset="path/to/dataset.jsonl", num_epochs=3)
adapter_path = trainer.save_adapter()
```

来源：https://arxiv.org/abs/2305.14314

---

### SFTTrainer（可选）

```python
from finetune_demo import SFTTrainer

trainer = SFTTrainer(
    model="Qwen/Qwen2.5-7B-Instruct",
    method="sft",
    output_dir="./models/sft"
)

trainer.train(dataset="path/to/dataset.jsonl", num_epochs=3)
```

来源：https://github.com/huggingface/trl

---

## CLI 接口

### LoRA 训练

```bash
finetune-demo train \
    --model Qwen/Qwen2.5-7B-Instruct \
    --method lora \
    --dataset data/example_dataset.jsonl \
    --epochs 3 \
    --output ./models/lora
```

### QLoRA 训练

```bash
finetune-demo train \
    --model Qwen/Qwen2.5-7B-Instruct \
    --method qlora \
    --dataset data/example_dataset.jsonl \
    --epochs 3 \
    --output ./models/qlora
```

### 保存 Adapter

```bash
finetune-demo save \
    --checkpoint ./models/lora/checkpoint-500 \
    --output ./models/lora/adapter
```

### 加载 Adapter

```bash
finetune-demo load \
    --base-model Qwen/Qwen2.5-7B-Instruct \
    --adapter ./models/lora/adapter
```

---

## 数据集格式

### JSONL 格式

```jsonl
{"instruction": "What is 2+2?", "input": "", "output": "4"}
{"instruction": "Translate to French", "input": "Hello", "output": "Bonjour"}
```

### 必需字段

| 字段 | 说明 |
|------|------|
| `instruction` | 指令 |
| `output` | 期望输出 |
| `input` | 可选输入 |

---

## Adapter 保存格式

```
./models/
└── lora/
    └── adapter/
        ├── adapter_config.json  # PEFT config
        └── adapter_model.safetensors  # adapter weights
```

来源：https://github.com/huggingface/peft

---

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL
3. https://arxiv.org/abs/2305.14314 — QLoRA

Risk of Staleness:
- PEFT/TRL 版本更新可能改变 API

Out of Scope Kept:
- 未写 DPO 接口
- 未写模型合并接口
