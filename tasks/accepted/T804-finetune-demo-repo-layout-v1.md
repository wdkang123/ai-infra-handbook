# finetune-demo Repo Layout v1

## Task ID: T804
## Task Title: finetune-demo Execution Prep Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T304 MVP 设计，准备 finetune-demo 实施前包。

---

# finetune-demo Repo Layout v1

## 概述

本文档定义 finetune-demo 模块的完整目录结构，对应 MVP 实施需求。

---

## 顶层结构

```
finetune-demo/
├── README.md
├── pyproject.toml
├── config.yaml
├── .env.example
├── src/
│   └── finetune_demo/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── trainer/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── lora_trainer.py
│       │   ├── qlora_trainer.py
│       │   └── sft_trainer.py
│       ├── adapter/
│       │   ├── __init__.py
│       │   ├── saver.py
│       │   └── loader.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── model_manager.py
│       └── export/
│           ├── __init__.py
│           └── adapter_exporter.py
├── configs/
│   ├── lora_config_example.yaml
│   └── qlora_config_example.yaml
├── data/
│   └── example_dataset.jsonl
├── models/
│   └── .gitkeep
├── tests/
│   ├── __init__.py
│   ├── test_trainer.py
│   └── test_adapter.py
├── examples/
│   ├── train_lora.py
│   └── train_qlora.py
└── scripts/
    └── train.sh
```

---

## 目录说明

### `src/finetune_demo/`

| 文件 | 说明 |
|------|------|
| `__init__.py` | 包初始化 |
| `main.py` | CLI 入口 |
| `config.py` | 配置加载 |
| `trainer/` | 训练器目录 |
| `adapter/` | Adapter 管理 |
| `models/` | 模型管理 |
| `export/` | 导出工具 |

### `trainer/`

| 文件 | 说明 |
|------|------|
| `base.py` | `BaseTrainer` 抽象基类 |
| `lora_trainer.py` | LoRA 训练器 |
| `qlora_trainer.py` | QLoRA 训练器 |
| `sft_trainer.py` | SFT 训练器（TRL SFTTrainer） |

### `adapter/`

| 文件 | 说明 |
|------|------|
| `saver.py` | Adapter 保存 |
| `loader.py` | Adapter 加载 |

### `configs/`

| 文件 | 说明 |
|------|------|
| `lora_config_example.yaml` | LoRA 配置示例 |
| `qlora_config_example.yaml` | QLoRA 配置示例 |

---

## 关键文件内容概要

### `pyproject.toml`

```toml
[project]
name = "finetune-demo"
version = "0.1.0"
requires-python = ">=3.10"

dependencies = [
    "transformers>=4.40.0",
    "peft>=0.10.0",
    "trl>=0.8.0",
    "bitsandbytes>=0.43.0",
    "accelerate>=0.28.0",
    "torch>=2.0.0",
    "pyyaml>=6.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
]

[project.optional-dependencies]
unsloth = [
    "unsloth @ git+https://github.com/unslothai/unsloth.git",
]
```

### `config.yaml`

```yaml
training:
  method: "qlora"  # lora | qlora | sft
  model:
    name_or_path: "Qwen/Qwen2.5-0.5B-Instruct"
    trust_remote_code: true

  lora:
    r: 16
    lora_alpha: 32
    target_modules: ["q_proj", "v_proj"]
    lora_dropout: 0.05
    bias: "none"

  qlora:
    load_in_4bit: true
    bnb_4bit_compute_dtype: "float16"
    bnb_4bit_use_double_quant: true
    bnb_4bit_quant_type: "nf4"

  training:
    output_dir: "./models"
    num_train_epochs: 3
    per_device_train_batch_size: 4
    learning_rate: 2e-4
    gradient_accumulation_steps: 4
    warmup_steps: 100
    logging_steps: 10
    save_steps: 500
```

---

## 与 MVP 设计（T304）的差异

| 维度 | T304 MVP | T804（本版） |
|------|---------|-------------|
| 目录结构 | 骨架 | 更完整 |
| Trainer 分离 | 未提 | 独立 `trainer/` |
| Adapter 管理 | 未提 | 独立 `adapter/` |
| Config 分离 | 提到有 config | 独立 `configs/` |
| Scripts | 未提 | 新增 `scripts/` |

---

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL

Risk of Staleness:
- PEFT/TRL 版本更新可能改变目录结构

Out of Scope Kept:
- 未写分布式训练配置
