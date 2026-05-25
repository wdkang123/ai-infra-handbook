# inference-service config.py Blueprint v1

## Task ID: T1001
## Title: inference-service Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T901 scaffold（pyproject / env-example），产出 `config.py` 配置加载蓝图。

---

# inference-service config.py Blueprint v1

## 概述

本文档定义 `src/inference_service/config.py` 的蓝图——Pydantic 配置加载，支持 YAML 文件和环境变量。

## `src/inference_service/config.py` 模板

```python
# src/inference_service/config.py
"""
Configuration loading for inference-service.

支持：
- config.yaml 文件
- 环境变量覆盖
- Pydantic validation
"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# ---------- Settings Models ----------

class ServerConfig(BaseSettings):
    """HTTP server settings."""
    model_config = SettingsConfigDict(env_prefix="INFERENCE_SERVER_")

    host: str = Field(default="0.0.0.0", description="Listen address")
    port: int = Field(default=8000, ge=1, le=65535, description="HTTP port")
    workers: int = Field(default=1, ge=1, description="Uvicorn worker count")
    timeout: int = Field(default=300, ge=1, description="Request timeout (seconds)")


class VLLMConfig(BaseSettings):
    """vLLM engine settings."""
    model_config = SettingsConfigDict(env_prefix="VLLM_")

    tensor_parallel_size: int = Field(default=1, ge=1, description="Tensor parallel size")
    gpu_memory_utilization: float = Field(
        default=0.9, ge=0.0, le=1.0,
        description="Fraction of GPU memory to use",
    )
    max_model_len: int = Field(default=4096, ge=256, description="Max context length")
    enforce_eager: bool = Field(default=False, description="Disable CUDA graphs")
    enable_chunked_prefill: bool = Field(default=True, description="Enable chunked prefill")
    max_num_batched_tokens: int = Field(default=8192, ge=1, description="Max batched tokens")
    trust_remote_code: bool = Field(default=True, description="Trust remote code")


class EngineConfig(BaseSettings):
    """Engine selection and settings."""
    model_config = SettingsConfigDict(env_prefix="INFERENCE_")

    type: str = Field(default="vllm", description="Engine type: vllm | sglang | triton")
    model_path: str = Field(
        default="Qwen/Qwen2.5-0.5B-Instruct",
        description="HuggingFace model name or local path",
    )
    trust_remote_code: bool = Field(default=True)


class MetricsConfig(BaseSettings):
    """Prometheus metrics settings."""
    model_config = SettingsConfigDict(env_prefix="METRICS_")

    enabled: bool = Field(default=True)
    port: int = Field(default=9090, ge=1, le=65535)


class HealthConfig(BaseSettings):
    """Health check settings."""
    model_config = SettingsConfigDict(env_prefix="HEALTH_")

    enabled: bool = Field(default=True)


class ModelConfig(BaseSettings):
    """Model paths and caching."""
    model_config = SettingsConfigDict(env_prefix="INFERENCE_MODEL_")

    cache_dir: str = Field(default="./model_cache")
    adapter_dir: Optional[str] = Field(default=None)


class InferenceServiceConfig(BaseSettings):
    """
    Top-level configuration for inference-service.

    Fields can be overridden by:
    1. Environment variables (highest priority)
    2. config.yaml file
    3. Default values (lowest priority)
    """
    model_config = SettingsConfigDict(
        env_prefix="INFERENCE_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    # Sub-configs
    server: ServerConfig = Field(default_factory=ServerConfig)
    engine: EngineConfig = Field(default_factory=EngineConfig)
    vllm: VLLMConfig = Field(default_factory=VLLMConfig)
    metrics: MetricsConfig = Field(default_factory=MetricsConfig)
    health: HealthConfig = Field(default_factory=HealthConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)


# ---------- Loader ----------

def load_config(config_path: Optional[str] = None) -> InferenceServiceConfig:
    """
    Load configuration from YAML file and/or environment variables.

    Args:
        config_path: Path to config.yaml. If None, looks for ./config.yaml
                     or INFERENCE_CONFIG_PATH env var.

    Returns:
        InferenceServiceConfig instance with all fields validated.
    """
    config_data: dict[str, Any] = {}

    # Load from YAML if file exists
    if config_path is None:
        config_path = os.getenv("INFERENCE_CONFIG_PATH", "config.yaml")

    config_file = Path(config_path)
    if config_file.exists():
        with open(config_file) as f:
            yaml_data = yaml.safe_load(f)
            if yaml_data:
                config_data = _flatten_dict(yaml_data)

    # Environment variables override YAML
    config = InferenceServiceConfig(**config_data)
    return config


def _flatten_dict(d: dict, parent_key: str = "", sep: str = "__") -> dict:
    """Flatten nested dict for Pydantic env var support."""
    items: list[tuple[str, Any]] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(_flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


# ---------- CLI helper ----------

@lru_cache
def get_config() -> InferenceServiceConfig:
    """Cached config singleton for use within a running server."""
    return load_config()
```

## `config.yaml` 模板

```yaml
# config.yaml — inference-service

server:
  host: "0.0.0.0"
  port: 8000
  workers: 1
  timeout: 300

engine:
  type: "vllm"
  model_path: "Qwen/Qwen2.5-0.5B-Instruct"
  trust_remote_code: true

vllm:
  tensor_parallel_size: 1
  gpu_memory_utilization: 0.9
  max_model_len: 4096
  enforce_eager: false
  enable_chunked_prefill: true
  max_num_batched_tokens: 8192

metrics:
  enabled: true
  port: 9090

health:
  enabled: true

model:
  cache_dir: "./model_cache"
  adapter_dir: "./adapters"
```

## 环境变量覆盖示例

```bash
# 环境变量覆盖 config.yaml
export INFERENCE_SERVER__PORT=9000
export INFERENCE_ENGINE__TYPE=vllm
export INFERENCE_ENGINE__MODEL_PATH=Qwen/Qwen2.5-1.5B-Instruct
export VLLM__GPU_MEMORY_UTILIZATION=0.85
```

---

Sources:
1. https://docs.pydantic.dev/ — Pydantic v2
2. https://docs.pydantic.dev/latest/concepts/settings/ — Pydantic Settings

Risk of Staleness:
- Pydantic v2 Settings API 稳定

Out of Scope Kept:
- 未写多引擎并发配置
- 未写 GPU 资源调度
