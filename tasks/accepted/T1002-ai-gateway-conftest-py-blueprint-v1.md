# ai-gateway conftest.py Blueprint v1

## Task ID: T1002
## Title: ai-gateway Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T902 scaffold test-fixture-map，产出 `conftest.py` pytest fixtures 蓝图。

---

# ai-gateway conftest.py Blueprint v1

## 概述

本文档定义 `tests/conftest.py` 的蓝图——共享 pytest fixtures。

## `tests/conftest.py` 模板

```python
# tests/conftest.py
"""
Pytest configuration and shared fixtures for ai-gateway.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Generator

import pytest
from httpx import ASGITransport, AsyncClient

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# [PLACEHOLDER] Real imports when implemented:
# from ai_gateway.config import load_config, AiGatewayConfig
# from ai_gateway.server import app, set_config


# ---------- Config fixtures ----------

@pytest.fixture
def test_config_dict() -> dict:
    """Minimal config for testing."""
    return {
        "server": {
            "host": "0.0.0.0",
            "port": 8080,
            "timeout": 300,
            "workers": 1,
        },
        "models": [
            {
                "name": "vllm-local",
                "base_url": "http://localhost:8000/v1",
                "api_key": "",
            },
            {
                "name": "openai-gpt4",
                "base_url": "https://api.openai.com/v1",
                "api_key": "test-openai-key",
            },
        ],
        "auth": {
            "enabled": True,
            "type": "api_key",
            "api_keys": ["dev-gateway-key-1", "dev-gateway-key-2"],
        },
        "rate_limit": {
            "enabled": True,
            "algorithm": "sliding_window",
            "default_rpm": 60,
            "per_model_rpm": {},
        },
        "metrics": {
            "enabled": True,
            "port": 9091,
        },
        "logging": {
            "enabled": True,
            "level": "INFO",
        },
    }


@pytest.fixture
def auth_headers() -> dict:
    """Valid auth headers for testing."""
    return {"Authorization": "Bearer dev-gateway-key-1"}


@pytest.fixture
def invalid_auth_headers() -> dict:
    """Invalid auth headers for testing."""
    return {"Authorization": "Bearer invalid-key"}


# ---------- HTTP fixtures ----------

@pytest.fixture
async def async_client() -> Generator[AsyncClient, None, None]:
    """
    Async HTTP client pointing to test app.

    [PLACEHOLDER] Real implementation:
        from ai_gateway.server import app, set_config
        config = test_config_dict()  # or AiGatewayConfig
        set_config(config)
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
    """
    from httpx import ASGITransport
    class DummyApp:
        pass
    transport = ASGITransport(app=DummyApp())
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


# ---------- Mock downstream ----------

@pytest.fixture
def mock_downstream_success() -> dict:
    """Mock successful response from downstream inference-service."""
    return {
        "id": "chatcmpl-downstream-123",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "Qwen2.5-0.5B-Instruct",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "The capital of France is Paris.",
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 15,
            "completion_tokens": 10,
            "total_tokens": 25,
        },
    }


@pytest.fixture
def mock_downstream_rate_limit() -> dict:
    """Mock 429 response from downstream."""
    return {
        "error": {
            "message": "Rate limit exceeded",
            "type": "rate_limit_error",
            "code": 429,
        }
    }


@pytest.fixture
def mock_downstream_500() -> dict:
    """Mock 500 response from downstream."""
    return {
        "error": {
            "message": "Internal server error",
            "type": "internal_error",
            "code": 500,
        }
    }


# ---------- Metrics fixtures ----------

@pytest.fixture
def mock_metrics_text() -> str:
    """Mock Prometheus metrics text."""
    return """# HELP ai_gateway_requests_total Total number of requests
# TYPE ai_gateway_requests_total counter
ai_gateway_requests_total{model="vllm-local",status="200"} 100
ai_gateway_requests_total{model="vllm-local",status="401"} 5
# HELP ai_gateway_request_duration_seconds Request duration
# TYPE ai_gateway_request_duration_seconds histogram
ai_gateway_request_duration_seconds_bucket{model="vllm-local",le="1.0"} 80
# HELP ai_gateway_tokens_total Total tokens processed
# TYPE ai_gateway_tokens_total counter
ai_gateway_tokens_total{model="vllm-local"} 5000
"""


# ---------- Fixture dependency graph ----------
"""
conftest.py
  ├── test_config_dict
  │     ↓
  │   async_client (via set_config)
  ├── auth_headers       → test_proxy.py
  ├── invalid_auth_headers → test_proxy.py
  ├── mock_downstream_success → test_proxy.py
  ├── mock_downstream_rate_limit → test_proxy.py
  └── mock_metrics_text → test_proxy.py
"""
```

## `tests/fixtures/` 内容

### `tests/fixtures/chat_request_valid.json`

```json
{
  "model": "vllm-local",
  "messages": [
    {"role": "user", "content": "Hello"}
  ]
}
```

### `tests/fixtures/chat_request_invalid_model.json`

```json
{
  "model": "unknown-model",
  "messages": [
    {"role": "user", "content": "Hello"}
  ]
}
```

---

Sources:
1. https://pytest.org/ — pytest
2. https://www.python-httpx.org/ — httpx

Risk of Staleness:
- pytest-async 版本变化可能影响 fixture 用法
