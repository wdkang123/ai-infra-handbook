from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelConfig(BaseModel):
    name_or_path: str = Field(default="Qwen/Qwen2.5-0.5B-Instruct")
    trust_remote_code: bool = Field(default=True)


class LoRAConfig(BaseModel):
    r: int = Field(default=16, ge=1)
    lora_alpha: int = Field(default=32, ge=1)
    lora_dropout: float = Field(default=0.05, ge=0.0, le=1.0)
    target_modules: list[str] = Field(default_factory=lambda: ["q_proj", "v_proj"])


class QLoRAConfig(BaseModel):
    load_in_4bit: bool = Field(default=False)
    bnb_4bit_quant_type: str = Field(default="nf4")


class DataConfig(BaseModel):
    train_file: str = Field(default="./data/train.jsonl")


class TrainingConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="FINETUNE_", env_nested_delimiter="__", extra="ignore")

    method: str = Field(default="lora")
    model: ModelConfig = Field(default_factory=ModelConfig)
    output_dir: str = Field(default="./models")
    num_train_epochs: int = Field(default=3, ge=1)
    per_device_train_batch_size: int = Field(default=4, ge=1)
    learning_rate: float = Field(default=2e-4, gt=0.0)
    lora: LoRAConfig = Field(default_factory=LoRAConfig)
    qlora: QLoRAConfig = Field(default_factory=QLoRAConfig)
    data: DataConfig = Field(default_factory=DataConfig)


def load_config(config_path: str | None = None) -> TrainingConfig:
    data: dict[str, Any] = {}
    target = config_path or os.getenv("FINETUNE_CONFIG_PATH")
    if target:
        config_file = Path(target)
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")
        data = yaml.safe_load(config_file.read_text()) or {}
    return TrainingConfig(**data)


def load_config_from_cli(**kwargs: Any) -> TrainingConfig:
    config_path = kwargs.pop("config", None)
    base = load_config(config_path).model_dump()
    model_data = base.get("model", {})
    data_data = base.get("data", {})
    lora_data = base.get("lora", {})
    qlora_data = base.get("qlora", {})

    if kwargs.get("model") is not None:
        model_data["name_or_path"] = kwargs["model"]
    if kwargs.get("dataset") is not None:
        data_data["train_file"] = kwargs["dataset"]
    if kwargs.get("output") is not None:
        base["output_dir"] = kwargs["output"]
    if kwargs.get("method") is not None:
        base["method"] = kwargs["method"]
    if kwargs.get("epochs") is not None:
        base["num_train_epochs"] = kwargs["epochs"]
    if kwargs.get("per_device_batch_size") is not None:
        base["per_device_train_batch_size"] = kwargs["per_device_batch_size"]
    if kwargs.get("learning_rate") is not None:
        base["learning_rate"] = kwargs["learning_rate"]
    if kwargs.get("lora_r") is not None:
        lora_data["r"] = kwargs["lora_r"]
    if kwargs.get("lora_alpha") is not None:
        lora_data["lora_alpha"] = kwargs["lora_alpha"]
    if kwargs.get("load_in_4bit") is not None:
        qlora_data["load_in_4bit"] = kwargs["load_in_4bit"]

    base["model"] = model_data
    base["data"] = data_data
    base["lora"] = lora_data
    base["qlora"] = qlora_data
    return TrainingConfig(**base)


@lru_cache
def get_config() -> TrainingConfig:
    return load_config()
