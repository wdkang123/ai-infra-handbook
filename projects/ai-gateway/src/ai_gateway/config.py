from __future__ import annotations

import os
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GATEWAY_SERVER_")

    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8080, ge=1, le=65535)


class ModelEntry(BaseModel):
    name: str
    base_url: str
    api_key: str = ""
    target_model: str | None = None
    fallbacks: list[str] = Field(default_factory=list)


class AuthConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AUTH_")

    enabled: bool = Field(default=True)
    api_keys: list[str] = Field(default_factory=lambda: ["dev-gateway-key-1"])


class MetricsConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GATEWAY_METRICS_")

    enabled: bool = Field(default=True)


class RateLimitConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GATEWAY_RATE_LIMIT_")

    enabled: bool = Field(default=True)
    requests_per_minute: int = Field(default=60, ge=1)


class CacheConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GATEWAY_CACHE_")

    enabled: bool = Field(default=False)
    ttl_seconds: int = Field(default=60, ge=1)
    max_entries: int = Field(default=128, ge=1)


class AiGatewayConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="GATEWAY_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    server: ServerConfig = Field(default_factory=ServerConfig)
    models: list[ModelEntry] = Field(default_factory=list)
    auth: AuthConfig = Field(default_factory=AuthConfig)
    metrics: MetricsConfig = Field(default_factory=MetricsConfig)
    rate_limit: RateLimitConfig = Field(default_factory=RateLimitConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)

    @model_validator(mode="after")
    def validate_unique_model_names(self) -> AiGatewayConfig:
        counts = Counter(model.name for model in self.models)
        duplicates = sorted(name for name, count in counts.items() if count > 1)
        if duplicates:
            joined = ", ".join(duplicates)
            raise ValueError(f"Duplicate gateway model names are not allowed: {joined}")
        return self


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text()) or {}


def load_config(config_path: str | None = None, models_path: str | None = None) -> AiGatewayConfig:
    config_file = Path(config_path or os.getenv("GATEWAY_CONFIG_PATH", "configs/config.yaml"))
    models_file = Path(models_path or os.getenv("GATEWAY_MODELS_PATH", "configs/models.yaml"))
    config_data = _load_yaml(config_file)
    models_data = _load_yaml(models_file)
    merged = dict(config_data)
    if models_data.get("models"):
        merged["models"] = models_data["models"]
    return AiGatewayConfig(**merged)


@lru_cache
def get_config() -> AiGatewayConfig:
    return load_config()
