# finetune-demo conftest.py Blueprint v1

## Task ID: T1004
## Title: finetune-demo Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T904 scaffold test-fixture-map，产出 `conftest.py` pytest fixtures 蓝图。

---

# finetune-demo conftest.py Blueprint v1

## 概述

本文档定义 `tests/conftest.py` 的蓝图——共享 pytest fixtures。

## `tests/conftest.py` 模板

```python
# tests/conftest.py
"""
Pytest configuration and shared fixtures for finetune-demo.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Generator

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# [PLACEHOLDER] Real imports when implemented:
# from finetune_demo.config import FinetuneConfig, LoRAConfig, TrainingConfig
# from finetune_demo.trainer.lora_trainer import LoRATrainer


# ---------- Config fixtures ----------

@pytest.fixture
def lora_config_dict() -> dict:
    """Minimal LoRA config for testing."""
    return {
        "method": "lora",
        "model": {
            "name_or_path": "Qwen/Qwen2.5-0.5B-Instruct",
            "trust_remote_code": True,
        },
        "output_dir": "./models/test_lora",
        "num_train_epochs": 1,
        "per_device_train_batch_size": 1,
        "learning_rate": 2e-4,
        "gradient_accumulation_steps": 1,
        "warmup_steps": 0,
        "logging_steps": 10,
        "save_steps": 50,
        "max_seq_length": 256,
        "lora": {
            "r": 8,
            "lora_alpha": 16,
            "target_modules": ["q_proj", "v_proj"],
            "lora_dropout": 0.05,
            "bias": "none",
        },
    }


@pytest.fixture
def qlora_config_dict() -> dict:
    """Minimal QLoRA config for testing."""
    return {
        "method": "qlora",
        "model": {
            "name_or_path": "Qwen/Qwen2.5-0.5B-Instruct",
            "trust_remote_code": True,
        },
        "output_dir": "./models/test_qlora",
        "num_train_epochs": 1,
        "per_device_train_batch_size": 1,
        "learning_rate": 2e-4,
        "gradient_accumulation_steps": 1,
        "max_seq_length": 256,
        "lora": {
            "r": 16,
            "lora_alpha": 32,
            "target_modules": ["q_proj", "v_proj", "k_proj", "o_proj"],
            "lora_dropout": 0.05,
            "bias": "none",
        },
        "qlora": {
            "load_in_4bit": True,
            "bnb_4bit_compute_dtype": "float16",
            "bnb_4bit_use_double_quant": True,
            "bnb_4bit_quant_type": "nf4",
        },
    }


# ---------- Trainer fixtures ----------

@pytest.fixture
def lora_trainer(lora_config_dict: dict) -> "LoRATrainer":  # [PLACEHOLDER]
    """LoRATrainer instance for testing (no real training)."""
    # [PLACEHOLDER] return LoRATrainer(config=lora_config_dict)
    class DummyTrainer:
        config = lora_config_dict
    return DummyTrainer()


# ---------- Dataset fixtures ----------

@pytest.fixture
def sample_dataset(tmp_path: Path) -> Path:
    """Small sample dataset for testing."""
    data = [
        {"instruction": "What is 2+2?", "input": "", "output": "4"},
        {"instruction": "What is 3+3?", "input": "", "output": "6"},
        {"instruction": "What is 1+1?", "input": "", "output": "2"},
    ]
    path = tmp_path / "test_dataset.jsonl"
    with open(path, "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
    return path


@pytest.fixture
def sample_dataset_content() -> list[dict]:
    """Sample dataset as list of dicts."""
    return [
        {"instruction": "What is 2+2?", "input": "", "output": "4"},
        {"instruction": "What is 3+3?", "input": "", "output": "6"},
        {"instruction": "Hello", "input": "", "output": "Hi there!"},
    ]


# ---------- Adapter fixtures ----------

@pytest.fixture
def mock_adapter_path(tmp_path: Path) -> Path:
    """Mock adapter directory structure."""
    adapter_dir = tmp_path / "mock_adapter"
    adapter_dir.mkdir()
    config = {
        "base_model_name_or_path": "Qwen/Qwen2.5-0.5B-Instruct",
        "peft_type": "LORA",
        "r": 16,
        "lora_alpha": 32,
        "target_modules": ["q_proj", "v_proj"],
        "lora_dropout": 0.05,
        "bias": "none",
    }
    (adapter_dir / "adapter_config.json").write_text(json.dumps(config))
    (adapter_dir / "adapter_model.safetensors").write_bytes(b"")
    return adapter_dir


# ---------- Config object ----------

@pytest.fixture
def finetune_config(lora_config_dict: dict) -> "FinetuneConfig":  # [PLACEHOLDER]
    """FinetuneConfig instance for testing."""
    # [PLACEHOLDER] return FinetuneConfig(**lora_config_dict)
    class DummyConfig:
        def __init__(self, d):
            self.__dict__.update(d)
    return DummyConfig(lora_config_dict)
```

## `tests/fixtures/sample_train.jsonl`

```jsonl
{"instruction": "What is 2+2?", "input": "", "output": "4"}
{"instruction": "What is 3+3?", "input": "", "output": "6"}
{"instruction": "What is 5+5?", "input": "", "output": "10"}
{"instruction": "Translate to French", "input": "Hello", "output": "Bonjour"}
{"instruction": "Capital of Japan", "input": "", "output": "Tokyo"}
```

---

Sources:
1. https://pytest.org/ — pytest
2. https://github.com/huggingface/peft — PEFT
