# inference-service conftest.py Blueprint v1

## Task ID: T1001
## Title: inference-service Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T901 scaffold test-fixture-map，产出 `conftest.py` pytest fixtures 蓝图。

---

# inference-service conftest.py Blueprint v1

## 概述

本文档定义 `tests/conftest.py` 的蓝图——共享 pytest fixtures，供 inference-service 测试使用。

## `tests/conftest.py` 模板

```python
# tests/conftest.py
"""
Pytest configuration and shared fixtures for inference-service.

Fixtures:
- test_config_dict    — minimal config dict for unit tests
- mock_env            — monkeypatched env vars
- async_client        — AsyncClient pointing to test app
- mock_vllm_response  — mock vLLM chat completion response
- mock_vllm_stream_chunks — mock SSE stream chunks
- mock_health_response — mock /health response
- mock_metrics_text   — mock Prometheus metrics text
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Generator

import pytest
from httpx import ASGITransport, AsyncClient

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# [PLACEHOLDER] Real imports when implemented:
# from inference_service.config import load_config
# from inference_service.server import app, set_engine


# ---------- Config fixtures ----------

@pytest.fixture
def test_config_dict() -> dict:
    """
    Minimal config dict for testing without loading from file.

    Returns:
        dict matching InferenceServiceConfig structure
    """
    return {
        "server": {
            "host": "0.0.0.0",
            "port": 8000,
            "workers": 1,
            "timeout": 300,
        },
        "engine": {
            "type": "vllm",
            "model_path": "Qwen/Qwen2.5-0.5B-Instruct",
            "trust_remote_code": True,
        },
        "vllm": {
            "tensor_parallel_size": 1,
            "gpu_memory_utilization": 0.9,
            "max_model_len": 4096,
            "enforce_eager": False,
            "enable_chunked_prefill": True,
            "max_num_batched_tokens": 8192,
        },
        "metrics": {
            "enabled": True,
            "port": 9090,
        },
        "health": {
            "enabled": True,
        },
        "model": {
            "cache_dir": "./model_cache",
            "adapter_dir": "./adapters",
        },
    }


@pytest.fixture
def mock_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set minimal env vars for testing."""
    monkeypatch.setenv("INFERENCE_ENGINE_TYPE", "vllm")
    monkeypatch.setenv("INFERENCE_MODEL_PATH", "Qwen/Qwen2.5-0.5B-Instruct")
    monkeypatch.setenv("INFERENCE_SERVER__PORT", "8000")
    monkeypatch.setenv("METRICS_ENABLED", "true")
    monkeypatch.setenv("HEALTH_ENABLED", "true")


# ---------- HTTP fixtures ----------

@pytest.fixture
async def async_client() -> Generator[AsyncClient, None, None]:
    """
    Async HTTP client for API testing via ASGI transport.

    Uses the FastAPI test app without real engine.
    [PLACEHOLDER] Real implementation:
        from inference_service.server import app, set_engine
        # set_engine(mock_engine)
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
    """
    # Placeholder: returns a client that will error without real app
    from httpx import ASGITransport
    # [PLACEHOLDER] replace with real app import
    class DummyApp:
        pass
    transport = ASGITransport(app=DummyApp())
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


# ---------- Engine fixtures ----------

@pytest.fixture
def mock_vllm_response() -> dict:
    """
    Mock vLLM chat completion response (non-streaming).

    Matches OpenAI ChatCompletion format.
    """
    return {
        "id": "chatcmpl-test-123",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "Qwen2.5-0.5B-Instruct",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "2+2 equals 4.",
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 12,
            "completion_tokens": 8,
            "total_tokens": 20,
        },
    }


@pytest.fixture
def mock_vllm_stream_chunks() -> list[str]:
    """
    Mock SSE stream chunks from vLLM.

    Format: one string per data: ...\\n\\n event.
    """
    return [
        'data: {"id":"chatcmpl-test-123","object":"chat.completion.chunk","created":1234567890,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{"role":"assistant","content":"2"},"finish_reason":null}]}\n\n',
        'data: {"id":"chatcmpl-test-123","object":"chat.completion.chunk","created":1234567890,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{"content":"+"},"finish_reason":null}]}\n\n',
        'data: {"id":"chatcmpl-test-123","object":"chat.completion.chunk","created":1234567890,"model":"Qwen2.5-0.5B-Instruct","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}\n\n',
        "data: [DONE]\n",
    ]


# ---------- Health/Metrics fixtures ----------

@pytest.fixture
def mock_health_response() -> dict:
    """Mock /health response."""
    return {
        "status": "healthy",
        "engine": "vllm",
        "model": "Qwen2.5-0.5B-Instruct",
        "gpu_available": True,
    }


@pytest.fixture
def mock_metrics_text() -> str:
    """
    Mock Prometheus metrics text.

    Contains vLLM-specific and inference-service metrics.
    """
    return """# HELP vllm_num_requests_running Number of requests currently running
# TYPE vllm_num_requests_running gauge
vllm_num_requests_running 0
# HELP vllm_num_tokens_total Total number of tokens processed
# TYPE vllm_num_tokens_total counter
vllm_num_tokens_total 12345
# HELP vllm_gpu_cache_usage GPU cache usage fraction
# TYPE vllm_gpu_cache_usage gauge
vllm_gpu_cache_usage 0.85
# HELP inference_service_requests_total Total HTTP requests
# TYPE inference_service_requests_total counter
inference_service_requests_total{method="POST",endpoint="/v1/chat/completions",status="200"} 50
inference_service_requests_total{method="GET",endpoint="/health",status="200"} 10
"""


# ---------- Fixture dependency graph ----------
"""
conftest.py
  ├── mock_env          → test_config_dict
  ├── test_config_dict  → async_client (via app initialization)
  └── async_client      → app (server.py)

mock_vllm_response     → tests/test_api.py, tests/test_engine.py
mock_health_response   → tests/test_api.py
mock_metrics_text      → tests/test_api.py
"""
```

## `tests/fixtures/` 内容模板

### `tests/fixtures/chat_request.json`

```json
{
  "model": "Qwen2.5-0.5B-Instruct",
  "messages": [
    {"role": "user", "content": "What is 2+2?"}
  ],
  "temperature": 0.7,
  "max_tokens": 256,
  "stream": false
}
```

### `tests/fixtures/chat_request_stream.json`

```json
{
  "model": "Qwen2.5-0.5B-Instruct",
  "messages": [{"role": "user", "content": "Count to 3"}],
  "stream": true
}
```

### `tests/fixtures/invalid_model.json`

```json
{
  "model": "nonexistent-model-xyz",
  "messages": [{"role": "user", "content": "Hello"}]
}
```

### `tests/fixtures/empty_messages.json`

```json
{
  "model": "Qwen2.5-0.5B-Instruct",
  "messages": []
}
```

---

Sources:
1. https://pytest.org/ — pytest
2. https://www.python-httpx.org/ — httpx
3. https://docs.pytest.org/en/latest/reference/fixtures.html — pytest fixtures

Risk of Staleness:
- pytest-async 版本变化可能影响 fixture 用法
