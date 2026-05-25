# ai-gateway Test Fixture Map v1

## Task ID: T902
## Title: ai-gateway Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T802 test plan 和 validation checklist，产出测试 fixture 蓝图。

---

# ai-gateway Test Fixture Map v1

## 概述

本文档定义 ai-gateway 的 pytest fixture 蓝图。

## `tests/conftest.py` 模板

```python
# tests/conftest.py
"""
Pytest configuration and shared fixtures for ai-gateway.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Generator

import pytest
from httpx import ASGITransport, AsyncClient

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_gateway.config import load_config
from ai_gateway.server import app


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
    """Async HTTP client pointing to test app."""
    transport = ASGITransport(app=app)
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
```

## 测试 Fixture 目录结构

```
tests/
├── conftest.py
├── fixtures/
│   ├── chat_request_valid.json
│   ├── chat_request_no_auth.json
│   └── chat_request_invalid_model.json
└── ...
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

## 单元测试 Fixture 使用示例

```python
# tests/test_router.py
import pytest
from ai_gateway.router import Router

def test_route_valid_model(test_config_dict):
    router = Router(test_config_dict["models"])
    url = router.route("vllm-local")
    assert url == "http://localhost:8000/v1"

def test_route_invalid_model_raises(test_config_dict):
    router = Router(test_config_dict["models"])
    with pytest.raises(ModelNotFoundError):
        router.route("unknown-model")

# tests/test_middleware.py
def test_auth_valid_key(auth_headers):
    # mock request with valid key
    pass

def test_auth_invalid_key(invalid_auth_headers):
    # mock request with invalid key
    pass
```

## 集成测试 Fixture 使用示例

```python
# tests/test_integration.py
@pytest.mark.asyncio
async def test_proxy_chat_success(
    async_client, auth_headers, mock_downstream_success, monkeypatch
):
    async def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self): return mock_downstream_success
        return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient.post", mock_post)

    response = await async_client.post(
        "/v1/chat/completions",
        json={"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]},
        headers=auth_headers,
    )
    assert response.status_code == 200
```

---

Sources:
1. https://pytest.org/ — pytest
2. https://www.python-httpx.org/ — httpx

Risk of Staleness:
- pytest-async 版本变化可能影响 fixture 用法

Out of Scope Kept:
- 未写故障注入测试 fixtures
- 未写 chaos testing fixtures
