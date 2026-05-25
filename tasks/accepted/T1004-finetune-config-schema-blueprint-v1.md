# finetune-demo config schema Blueprint v1

## Task ID: T1004
## Title: finetune-demo Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T904 scaffold（sample-config catalog / pyproject），产出配置 schema 蓝图。

---

# finetune-demo config schema Blueprint v1

## 概述

本文档定义 `src/finetune_demo/config.py` 的蓝图——Pydantic 配置 schema，支持 YAML 文件和 CLI 参数。

## `src/finetune_demo/config.py` 模板

```python
# src/finetune_demo/config.py
"""
Configuration schema for finetune-demo.

Supports:
- YAML config file (configs/lora_config_example.yaml)
- CLI argument override
- Pydantic validation
"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# ---------- Model Config ----------

class ModelConfig(BaseSettings):
    """Model configuration."""
    model_config = SettingsConfigDict(env_prefix="FINETUNE_MODEL_")

    name_or_path: str = Field(
        default="Qwen/Qwen2.5-0.5B-Instruct",
        description="HuggingFace model name or local path",
    )
    trust_remote_code: bool = Field(default=True)


# ---------- LoRA Config ----------

class LoRAConfig(BaseModel):
    """LoRA-specific configuration."""
    r: int = Field(default=16, ge=1, description="LoRA rank")
    lora_alpha: int = Field(default=32, ge=1, description="LoRA alpha (scaling factor)")
    target_modules: list[str] = Field(
        default_factory=lambda: ["q_proj", "v_proj"],
        description="Module names to apply LoRA to",
    )
    lora_dropout: float = Field(default=0.05, ge=0.0, le=1.0)
    bias: str = Field(default="none", description="Bias type: none | all | lora_only")

    @field_validator("target_modules")
    @classmethod
    def validate_target_modules(cls, v: list[str]) -> list[str]:
        valid = {"q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"}
        for m in v:
            if m not in valid:
                raise ValueError(f"Invalid target_module: {m}. Must be one of {valid}")
        return v


# ---------- QLoRA Config ----------

class QLoRAConfig(BaseModel):
    """QLoRA-specific configuration (used when load_in_4bit=True)."""
    load_in_4bit: bool = Field(default=False)
    bnb_4bit_compute_dtype: str = Field(default="float16")
    bnb_4bit_use_double_quant: bool = Field(default=True)
    bnb_4bit_quant_type: str = Field(default="nf4")


# ---------- Data Config ----------

class DataConfig(BaseModel):
    """Dataset configuration."""
    train_file: str = Field(..., description="Path to training JSONL file")
    val_file: Optional[str] = Field(None, description="Path to validation JSONL file (optional)")
    text_field: str = Field(default="instruction", description="JSONL field for input text")
    output_field: str = Field(default="output", description="JSONL field for target output")
    cutoff_len: int = Field(default=512, ge=1)


# ---------- Training Config ----------

class TrainingConfig(BaseSettings):
    """
    Top-level training configuration.

    Env var format: FINETUNE__METHOD=lora, FINETUNE__LEARNING_RATE=1e-4
    """
    model_config = SettingsConfigDict(
        env_prefix="FINETUNE_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    method: str = Field(default="lora", description="Training method: lora | qlora")
    model: ModelConfig = Field(default_factory=ModelConfig)
    output_dir: str = Field(default="./models", description="Output directory")
    num_train_epochs: int = Field(default=3, ge=1)
    per_device_train_batch_size: int = Field(default=4, ge=1)
    gradient_accumulation_steps: int = Field(default=4, ge=1)
    learning_rate: float = Field(default=2e-4, gt=0.0)
    warmup_steps: int = Field(default=100, ge=0)
    logging_steps: int = Field(default=10, ge=1)
    save_steps: int = Field(default=500, ge=1)
    max_seq_length: int = Field(default=512, ge=1)
    fp16: bool = Field(default=True)
    gradient_checkpointing: bool = Field(default=True)

    lora: LoRAConfig = Field(default_factory=LoRAConfig)
    qlora: QLoRAConfig = Field(default_factory=QLoRAConfig)
    data: DataConfig | None = Field(None)

    @field_validator("method")
    @classmethod
    def validate_method(cls, v: str) -> str:
        if v not in ("lora", "qlora"):
            raise ValueError(f"method must be 'lora' or 'qlora', got '{v}'")
        return v


# ---------- Config Loader ----------

def load_config(config_path: Optional[str] = None) -> TrainingConfig:
    """
    Load configuration from YAML file and/or environment variables.

    Args:
        config_path: Path to YAML config. If None, uses FINETUNE_CONFIG_PATH
                     env var or raises.
    """
    config_data: dict[str, Any] = {}

    if config_path is None:
        config_path = os.getenv("FINETUNE_CONFIG_PATH")

    if config_path:
        config_file = Path(config_path)
        if config_file.exists():
            with open(config_file) as f:
                config_data = yaml.safe_load(f) or {}

    return TrainingConfig(**config_data)


def load_config_from_cli(**kwargs: Any) -> TrainingConfig:
    """
    Build config from CLI arguments, with YAML as base.

    CLI values override YAML values.
    """
    # Extract YAML path if provided
    yaml_path = kwargs.pop("config", None)
    config_data: dict[str, Any] = {}

    if yaml_path:
        with open(Path(yaml_path)) as f:
            config_data = yaml.safe_load(f) or {}

    # Merge CLI overrides
    _merge_cli_overrides(config_data, kwargs)
    return TrainingConfig(**config_data)


def _merge_cli_overrides(config: dict[str, Any], overrides: dict[str, Any]) -> None:
    """Deep merge CLI overrides into config dict."""
    for key, value in overrides.items():
        if value is None:
            continue
        if key in config and isinstance(config[key], dict) and isinstance(value, dict):
            config[key].update(value)
        else:
            config[key] = value


@lru_cache
def get_config() -> TrainingConfig:
    """Cached config singleton."""
    return load_config()


# ---------- Dataset formatting ----------

def format_instruction_sample(
    sample: dict[str, str],
    input_field: str = "instruction",
    output_field: str = "output",
) -> str:
    """
    Format an instruction-following sample as a single text string.

    Args:
        sample: dict with 'instruction' and 'output' keys.
        input_field: JSON key for instruction.
        output_field: JSON key for output.

    Returns:
        Formatted string like "Instruction: ...\nOutput: ..."
    """
    instruction = sample.get(input_field, "")
    output = sample.get(output_field, "")
    return f"Instruction: {instruction}\nOutput: {output}"


def load_jsonl_dataset(path: Path | str, text_field: str = "instruction") -> list[dict]:
    """
    Load a JSONL dataset file.

    Args:
        path: Path to JSONL file.
        text_field: Field to include in text column.

    Returns:
        List of dicts with 'text' column.
    """
    import json
    path = Path(path)
    samples = []
    with open(path) as f:
        for line in f:
            sample = json.loads(line)
            samples.append({"text": format_instruction_sample(sample, text_field)})
    return samples
```

---

Sources:
1. https://docs.pydantic.dev/ — Pydantic v2
2. https://github.com/huggingface/peft — PEFT LoRA config
