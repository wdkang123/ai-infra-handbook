from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="INFERENCE_SERVER_")

    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000, ge=1, le=65535)
    workers: int = Field(default=1, ge=1)
    timeout: int = Field(default=300, ge=1)


class EngineConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="INFERENCE_ENGINE_")

    type: str = Field(default="mock")
    model_path: str = Field(default="Qwen/Qwen2.5-0.5B-Instruct")
    base_url: str = Field(default="")
    api_key: str = Field(default="")
    timeout: float = Field(default=30.0, gt=0.0)
    trust_remote_code: bool = Field(default=True)


class MetricsConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="INFERENCE_METRICS_")

    enabled: bool = Field(default=False)
    port: int = Field(default=9090, ge=1, le=65535)


class InferenceServiceConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="INFERENCE_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    server: ServerConfig = Field(default_factory=ServerConfig)
    engine: EngineConfig = Field(default_factory=EngineConfig)
    metrics: MetricsConfig = Field(default_factory=MetricsConfig)


def _flatten_dict(data: dict[str, Any], parent_key: str = "", sep: str = "__") -> dict[str, Any]:
    items: list[tuple[str, Any]] = []
    for key, value in data.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(_flatten_dict(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def load_config(config_path: str | None = None) -> InferenceServiceConfig:
    data: dict[str, Any] = {}
    target = config_path or os.getenv("INFERENCE_CONFIG_PATH", "config.yaml")
    config_file = Path(target)
    if config_file.exists():
        loaded = yaml.safe_load(config_file.read_text()) or {}
        data = _flatten_dict(loaded)
    return InferenceServiceConfig(**data)


@lru_cache
def get_config() -> InferenceServiceConfig:
    return load_config()
