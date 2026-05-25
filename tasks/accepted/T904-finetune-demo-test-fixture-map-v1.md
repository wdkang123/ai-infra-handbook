# finetune-demo Test Fixture Map v1

## Task ID: T904
## Title: finetune-demo Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T804 test plan，产出测试 fixture 蓝图。

---

# finetune-demo Test Fixture Map v1

## 概述

本文档定义 finetune-demo 的 pytest fixture 蓝图。

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

from finetune_demo.config import FinetuneConfig
from finetune_demo.trainer.lora_trainer import LoRATrainer


# ---------- Config fixtures ----------

@pytest.fixture
def lora_config_dict() -> dict:
    """Minimal LoRA config for testing."""
    return {
        "training": {
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
        },
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
        "training": {
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
        },
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
def lora_trainer(lora_config_dict: dict) -> LoRATrainer:
    """LoRATrainer instance for testing (no real training)."""
    # Note: this creates the trainer object but does NOT load model
    return LoRATrainer(config=lora_config_dict)


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
    # Write mock adapter_config.json
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
    # Write mock safetensors (just a placeholder)
    (adapter_dir / "adapter_model.safetensors").write_bytes(b"")
    return adapter_dir


# ---------- Config object ----------

@pytest.fixture
def finetune_config(lora_config_dict: dict) -> FinetuneConfig:
    """FinetuneConfig instance for testing."""
    return FinetuneConfig(**lora_config_dict)
```

## `tests/fixtures/` 内容

### `tests/fixtures/sample_train.jsonl`

```jsonl
{"instruction": "What is 2+2?", "input": "", "output": "4"}
{"instruction": "What is 3+3?", "input": "", "output": "6"}
{"instruction": "What is 5+5?", "input": "", "output": "10"}
{"instruction": "Translate to French", "input": "Hello", "output": "Bonjour"}
{"instruction": "Capital of Japan", "input": "", "output": "Tokyo"}
```

## 测试用例示例

```python
# tests/test_trainer.py
import pytest
from finetune_demo.trainer.lora_trainer import LoRATrainer

def test_lora_trainer_init(lora_trainer: LoRATrainer):
    """Test LoRA trainer initializes with valid config."""
    assert lora_trainer is not None
    assert lora_trainer.config["lora"]["r"] == 8

def test_lora_r_validation(lora_config_dict: dict):
    """Test that invalid r raises ValueError."""
    lora_config_dict["lora"]["r"] = 0
    with pytest.raises(ValueError):
        LoRATrainer(config=lora_config_dict)

def test_lora_r_negative(lora_config_dict: dict):
    """Test that negative r raises ValueError."""
    lora_config_dict["lora"]["r"] = -1
    with pytest.raises(ValueError):
        LoRATrainer(config=lora_config_dict)


# tests/test_adapter.py
def test_adapter_path(mock_adapter_path: Path):
    """Test adapter directory has required files."""
    config_path = mock_adapter_path / "adapter_config.json"
    weights_path = mock_adapter_path / "adapter_model.safetensors"
    assert config_path.exists()
    assert weights_path.exists()

def test_adapter_config_parsing(mock_adapter_path: Path):
    """Test adapter_config.json is valid JSON with required fields."""
    import json
    config = json.loads((mock_adapter_path / "adapter_config.json").read_text())
    assert config["peft_type"] == "LORA"
    assert config["r"] == 16
    assert "target_modules" in config
```

## 显存约束说明

单元测试使用 `per_device_train_batch_size=1` 和 `max_seq_length=256`，避免显存溢出。使用 tiny model（如 Qwen/Qwen2.5-0.5B-Instruct）进行真实训练测试。

---

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL

Risk of Staleness:
- PEFT API 变化可能影响 fixture

Out of Scope Kept:
- 未写端到端训练测试（需要 GPU）
