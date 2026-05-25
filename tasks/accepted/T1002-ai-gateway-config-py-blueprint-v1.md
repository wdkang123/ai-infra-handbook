# ai-gateway config.py Blueprint v1

## Task ID: T1002
## Title: ai-gateway Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T902 scaffold（pyproject / env-example），产出 `config.py` 配置加载蓝图。

---

# ai-gateway config.py Blueprint v1

## 概述

本文档定义 `src/ai_gateway/config.py` 的蓝图——Pydantic 配置加载，支持 YAML 和环境变量。

## `src/ai_gateway/config.py` 模板

```python
# src/ai_gateway/config.py
"""
Configuration loading for ai-gateway.

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
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# ---------- Settings Models ----------

class ServerConfig(BaseSettings):
    """HTTP server settings."""
    model_config = SettingsConfigDict(env_prefix="GATEWAY_SERVER_")

    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8080, ge=1, le=65535)
    workers: int = Field(default=1, ge=1)
    timeout: int = Field(default=300, ge=1)


class ModelEntry(BaseModel):
    """A single model routing entry."""
    name: str = Field(description="Model name as seen by gateway clients")
    base_url: str = Field(description="Downstream inference-service base URL")
    api_key: str = Field(default="", description="API key for downstream (if required)")


class AuthConfig(BaseSettings):
    """Auth middleware settings."""
    model_config = SettingsConfigDict(env_prefix="AUTH_")

    enabled: bool = Field(default=True, description="Enable API key verification")
    type: str = Field(default="api_key", description="Auth type: api_key | jwt | ...")
    api_keys: list[str] = Field(
        default_factory=lambda: ["sk-test-key-1", "sk-test-key-2"],
        description="Valid API keys",
    )


class RateLimitConfig(BaseSettings):
    """Rate limiting settings."""
    model_config = SettingsConfigDict(env_prefix="RATE_LIMIT_")

    enabled: bool = Field(default=True)
    algorithm: str = Field(default="sliding_window", description="sliding_window | fixed_window")
    default_rpm: int = Field(default=60, ge=1, description="Default requests per minute")
    per_model_rpm: dict[str, int] = Field(
        default_factory=dict,
        description="Per-model RPM overrides",
    )


class MetricsConfig(BaseSettings):
    """Prometheus metrics settings."""
    model_config = SettingsConfigDict(env_prefix="GATEWAY_METRICS_")

    enabled: bool = Field(default=True)
    port: int = Field(default=9091, ge=1, le=65535)


class LoggingConfig(BaseSettings):
    """Logging settings."""
    model_config = SettingsConfigDict(env_prefix="LOGGING_")

    enabled: bool = Field(default=True)
    level: str = Field(default="INFO", description="DEBUG|INFO|WARNING|ERROR")


class AiGatewayConfig(BaseSettings):
    """
    Top-level configuration for ai-gateway.

    Nested env var format: GATEWAY__SERVER__PORT, AUTH__ENABLED, etc.
    """
    model_config = SettingsConfigDict(
        env_prefix="GATEWAY_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    server: ServerConfig = Field(default_factory=ServerConfig)
    models: list[ModelEntry] = Field(
        default_factory=lambda: [
            ModelEntry(name="vllm-local", base_url="http://localhost:8000/v1", api_key=""),
            ModelEntry(
                name="openai-gpt4",
                base_url="https://api.openai.com/v1",
                api_key="sk-...",
            ),
        ],
    )
    auth: AuthConfig = Field(default_factory=AuthConfig)
    rate_limit: RateLimitConfig = Field(default_factory=RateLimitConfig)
    metrics: MetricsConfig = Field(default_factory=MetricsConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


# ---------- Loader ----------

def load_config(config_path: Optional[str] = None) -> AiGatewayConfig:
    """
    Load configuration from YAML file and/or environment variables.

    Args:
        config_path: Path to config.yaml. Defaults to ./config.yaml or
                     GATEWAY_CONFIG_PATH env var.
    """
    config_data: dict[str, Any] = {}

    if config_path is None:
        config_path = os.getenv("GATEWAY_CONFIG_PATH", "config.yaml")

    config_file = Path(config_path)
    if config_file.exists():
        with open(config_file) as f:
            yaml_data = yaml.safe_load(f)
            if yaml_data:
                config_data = _flatten_dict(yaml_data)

    config = AiGatewayConfig(**config_data)
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


@lru_cache
def get_config() -> AiGatewayConfig:
    """Cached config singleton."""
    return load_config()
```

## `config.yaml` 模板

```yaml
# config.yaml — ai-gateway

server:
  host: "0.0.0.0"
  port: 8080
  workers: 1
  timeout: 300

models:
  - name: "vllm-local"
    base_url: "http://localhost:8000/v1"
    api_key: ""
  - name: "openai-gpt4"
    base_url: "https://api.openai.com/v1"
    api_key: "sk-your-openai-key"

auth:
  enabled: true
  type: "api_key"
  api_keys:
    - "sk-test-key-1"
    - "sk-test-key-2"

rate_limit:
  enabled: true
  algorithm: "sliding_window"
  default_rpm: 60
  per_model_rpm:
    "vllm-local": 120
    "openai-gpt4": 30

metrics:
  enabled: true
  port: 9091

logging:
  enabled: true
  level: "INFO"
```

---

Sources:
1. https://docs.pydantic.dev/ — Pydantic v2
2. https://github.com/laurentS/slowapi — Slowapi rate limiting

Risk of Staleness:
- Pydantic v2 Settings API 稳定
