# finetune-demo test_trainer.py Blueprint v1

## Task ID: T1004
## Title: finetune-demo Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T904 scaffold（test-fixture-map / sample-config），产出 `test_trainer.py` 蓝图。

---

# finetune-demo test_trainer.py Blueprint v1

## 概述

本文档定义 `tests/test_trainer.py` 的蓝图——LoRA trainer 单元测试。

## `tests/test_trainer.py` 模板

```python
# tests/test_trainer.py
"""
Tests for LoRA/QLoRA trainer.

Tests:
- Trainer initializes with valid config
- LoRA r validation (positive integer)
- LoRA target_modules validation
- QLoRA requires load_in_4bit
- Adapter path structure
- Dataset loading and formatting
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

# [PLACEHOLDER] Real imports when implemented:
# from finetune_demo.trainer.lora_trainer import LoRATrainer, TrainingConfig
# from finetune_demo.config import format_instruction_sample, load_jsonl_dataset


# ---------- Trainer Init Tests ----------

class TestLoRATrainerInit:
    """Tests for LoRATrainer initialization."""

    def test_lora_trainer_init_valid_config(
        self,
        lora_trainer: Any,
    ) -> None:
        """
        Test that trainer initializes with valid config.
        """
        # [PLACEHOLDER]
        # assert lora_trainer is not None
        # assert lora_trainer.config.method == "lora"
        pass

    def test_lora_r_positive_required(
        self,
        lora_config_dict: dict,
    ) -> None:
        """
        Test that lora_r must be a positive integer.
        """
        # [PLACEHOLDER]
        # lora_config_dict["lora"]["r"] = 0
        # with pytest.raises(ValueError, match="positive"):
        #     LoRATrainer(config=lora_config_dict)
        pass

    def test_lora_r_negative_rejected(
        self,
        lora_config_dict: dict,
    ) -> None:
        """
        Test that negative lora_r raises ValueError.
        """
        # [PLACEHOLDER]
        # lora_config_dict["lora"]["r"] = -1
        # with pytest.raises(ValueError):
        #     LoRATrainer(config=lora_config_dict)
        pass

    def test_invalid_target_module_rejected(
        self,
        lora_config_dict: dict,
    ) -> None:
        """
        Test that invalid target_module names raise ValueError.
        """
        # [PLACEHOLDER]
        # lora_config_dict["lora"]["target_modules"] = ["invalid_module"]
        # with pytest.raises(ValueError, match="Invalid target_module"):
        #     LoRATrainer(config=lora_config_dict)
        pass

    def test_qlora_requires_load_in_4bit(
        self,
        qlora_config_dict: dict,
    ) -> None:
        """
        Test that QLoRA method requires load_in_4bit=True.
        """
        # [PLACEHOLDER]
        # qlora_config_dict["qlora"]["load_in_4bit"] = False
        # with pytest.raises(ValueError, match="load_in_4bit"):
        #     LoRATrainer(config=qlora_config_dict)
        pass


# ---------- Config Tests ----------

class TestTrainingConfig:
    """Tests for TrainingConfig validation."""

    def test_valid_lora_config(self, lora_config_dict: dict) -> None:
        """
        Test that valid LoRA config passes validation.
        """
        # [PLACEHOLDER]
        # cfg = TrainingConfig(**lora_config_dict)
        # assert cfg.method == "lora"
        # assert cfg.lora.r == 8
        pass

    def test_invalid_method_rejected(self, lora_config_dict: dict) -> None:
        """
        Test that invalid method raises ValueError.
        """
        # [PLACEHOLDER]
        # lora_config_dict["method"] = "dpo"
        # with pytest.raises(ValueError):
        #     TrainingConfig(**lora_config_dict)
        pass


# ---------- Dataset Tests ----------

class TestDatasetFormatting:
    """Tests for dataset formatting utilities."""

    def test_format_instruction_sample(self) -> None:
        """
        Test instruction-following sample formatting.
        """
        # [PLACEHOLDER]
        # sample = {"instruction": "What is 2+2?", "input": "", "output": "4"}
        # text = format_instruction_sample(sample)
        # assert "Instruction: What is 2+2?" in text
        # assert "Output: 4" in text
        pass

    def test_format_with_input_field(self) -> None:
        """
        Test formatting samples with non-empty input field.
        """
        # [PLACEHOLDER]
        # sample = {"instruction": "Translate", "input": "Hello", "output": "Bonjour"}
        # text = format_instruction_sample(sample)
        # assert "Bonjour" in text
        pass

    def test_load_jsonl_dataset(
        self,
        sample_dataset: Path,
    ) -> None:
        """
        Test loading a JSONL dataset file.
        """
        # [PLACEHOLDER]
        # samples = load_jsonl_dataset(sample_dataset)
        # assert len(samples) == 3
        # assert "text" in samples[0]
        pass


# ---------- Adapter Tests ----------

class TestAdapter:
    """Tests for adapter save/load."""

    def test_adapter_path_has_required_files(
        self,
        mock_adapter_path: Path,
    ) -> None:
        """
        Test that adapter directory has required files.
        """
        # [PLACEHOLDER]
        # config_path = mock_adapter_path / "adapter_config.json"
        # weights_path = mock_adapter_path / "adapter_model.safetensors"
        # assert config_path.exists()
        # assert weights_path.exists()
        pass

    def test_adapter_config_parsing(
        self,
        mock_adapter_path: Path,
    ) -> None:
        """
        Test that adapter_config.json is valid JSON.
        """
        # [PLACEHOLDER]
        # import json
        # config = json.loads((mock_adapter_path / "adapter_config.json").read_text())
        # assert config["peft_type"] == "LORA"
        # assert config["r"] == 16
        # assert "target_modules" in config
        pass

    def test_save_adapter_creates_files(
        self,
        lora_trainer: Any,
        tmp_path: Path,
    ) -> None:
        """
        Test that save_adapter creates expected files.
        [PLACEHOLDER] Note: requires real model, skip in unit tests.
        """
        pass
```

## 测试覆盖矩阵

| 测试 | 描述 | 依赖 |
|------|------|------|
| `test_lora_trainer_init_valid_config` | 有效配置初始化 | `lora_trainer` |
| `test_lora_r_positive_required` | r 必须为正 | `lora_config_dict` |
| `test_lora_r_negative_rejected` | 负数 r 拒绝 | `lora_config_dict` |
| `test_invalid_target_module_rejected` | 无效模块名拒绝 | `lora_config_dict` |
| `test_qlora_requires_load_in_4bit` | QLoRA 需 4bit | `qlora_config_dict` |
| `test_format_instruction_sample` | 样本格式化 | — |
| `test_load_jsonl_dataset` | JSONL 加载 | `sample_dataset` |
| `test_adapter_path_has_required_files` | adapter 目录结构 | `mock_adapter_path` |

---

Sources:
1. https://github.com/huggingface/peft — PEFT
2. https://github.com/huggingface/trl — TRL
