# inference-service Test Fixture Map v1

## Task ID: T901
## Title: inference-service Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T801 test plan 和 T801 validation checklist，产出测试 fixture 蓝图。

---

# inference-service Test Fixture Map v1

## 概述

本文档定义 inference-service 的 pytest fixture 和测试数据蓝图。

## `tests/conftest.py` 模板

```python
# tests/conftest.py
"""
Pytest configuration and shared fixtures for inference-service.
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

from inference_service.config import load_config
from inference_service.server import app


# ---------- Config fixtures ----------

@pytest.fixture
def test_config_dict() -> dict:
    """Minimal config dict for testing without loading from file."""
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
    monkeypatch.setenv("INFERENCE_PORT", "8000")
    monkeypatch.setenv("METRICS_ENABLED", "true")
    monkeypatch.setenv("HEALTH_CHECK_ENABLED", "true")


# ---------- HTTP fixtures ----------

@pytest.fixture
async def async_client() -> Generator[AsyncClient, None, None]:
    """Async HTTP client for API testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


# ---------- Engine fixtures ----------

@pytest.fixture
def mock_vllm_response() -> dict:
    """Mock vLLM chat completion response."""
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
    """Mock SSE stream chunks from vLLM."""
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
    """Mock Prometheus metrics text."""
    return """# HELP vllm_num_requests_running Number of requests currently running
# TYPE vllm_num_requests_running gauge
vllm_num_requests_running 0
# HELP vllm_num_tokens_total Total number of tokens processed
# TYPE vllm_num_tokens_total counter
vllm_num_tokens_total 12345
# HELP vllm_gpu_cache_usage GPU cache usage fraction
# TYPE vllm_gpu_cache_usage gauge
vllm_gpu_cache_usage 0.85
"""
```

## 测试 Fixture 目录结构

```
tests/
├── conftest.py              # 共享 fixtures
├── fixtures/
│   ├── chat_request.json    # 基本聊天请求
│   ├── chat_request_stream.json  # 流式请求
│   ├── invalid_model.json   # 无效模型请求
│   ├── empty_messages.json  # 空消息请求
│   └── health_response.json # 健康检查响应
└── ...
```

## `tests/fixtures/` 内容模板

### `tests/fixtures/chat_request.json`

```json
{
  "model": "Qwen2.5-0.5B-Instruct",
  "messages": [
    {
      "role": "user",
      "content": "What is 2+2?"
    }
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
  "messages": [
    {
      "role": "user",
      "content": "Count to 3"
    }
  ],
  "stream": true
}
```

### `tests/fixtures/invalid_model.json`

```json
{
  "model": "nonexistent-model",
  "messages": [
    {
      "role": "user",
      "content": "Hello"
    }
  ]
}
```

### `tests/fixtures/empty_messages.json`

```json
{
  "model": "Qwen2.5-0.5B-Instruct",
  "messages": []
}
```

## 单元测试 Fixture 使用示例

```python
# tests/test_engine.py
import pytest
from inference_service.engines.vllm_engine import VLLMEngine

def test_vllm_engine_init(mock_env, test_config_dict):
    """Test VLLM engine initialization with mocked config."""
    config = test_config_dict
    engine = VLLMEngine(config)
    assert engine.model_path == "Qwen/Qwen2.5-0.5B-Instruct"

def test_vllm_engine_infer_with_mock(mock_vllm_response, monkeypatch):
    """Test inference with mocked vLLM response."""
    def mock_predict(*args, **kwargs):
        return mock_vllm_response
    # ... setup and assert
```

## 集成测试 Fixture 使用示例

```python
# tests/test_api.py
import pytest
from httpx import ASGITransport, AsyncClient
from inference_service.server import app

@pytest.mark.asyncio
async def test_chat_completions_basic(async_client, mock_vllm_response, monkeypatch):
    """Test POST /v1/chat/completions with mocked engine."""
    monkeypatch.setattr(
        "inference_service.api.chat.vllm_engine_predict",
        lambda *a, **kw: mock_vllm_response
    )
    response = await async_client.post(
        "/v1/chat/completions",
        json={
            "model": "Qwen2.5-0.5B-Instruct",
            "messages": [{"role": "user", "content": "Hello"}],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "choices" in data
    assert data["choices"][0]["message"]["role"] == "assistant"
```

## Fixtures 依赖关系

```
conftest.py
  ├── mock_env          → test_config_dict
  ├── test_config_dict  → async_client
  └── async_client      → app

mock_vllm_response     → tests/test_engine.py, tests/test_api.py
mock_health_response   → tests/test_api.py
mock_metrics_text      → tests/test_api.py
```

---

Sources:
1. https://pytest.org/ — pytest
2. https://www.python-httpx.org/ — httpx
3. https://docs.pytest.org/en/latest/reference/fixtures.html — pytest fixtures

Risk of Staleness:
- pytest-async 版本变化可能影响 fixture 用法

Out of Scope Kept:
- 未写性能/压力测试 fixtures
- 未写故障注入 fixtures
