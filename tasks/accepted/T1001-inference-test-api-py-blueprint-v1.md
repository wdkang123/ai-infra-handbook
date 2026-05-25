# inference-service test_api.py Blueprint v1

## Task ID: T1001
## Title: inference-service Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T901 scaffold（test-fixture-map / curl catalog），产出 `test_api.py` 蓝图。

---

# inference-service test_api.py Blueprint v1

## 概述

本文档定义 `tests/test_api.py` 的蓝图——FastAPI API 端点的单元测试，不包含真实实现（占位符 + 注释）。

## `tests/test_api.py` 模板

```python
# tests/test_api.py
"""
API endpoint tests for inference-service.

Tests:
- GET  /health         — health check
- GET  /metrics        — Prometheus metrics
- POST /v1/chat/completions — non-streaming + streaming
- Error cases: invalid model, empty messages
"""
from __future__ import annotations

import json
from typing import Any

import pytest
from httpx import AsyncClient

# [PLACEHOLDER] Real imports when implemented:
# from inference_service.server import app, set_engine


# ---------- Health ----------

@pytest.mark.asyncio
class TestHealth:
    """Tests for GET /health."""

    async def test_health_returns_200(self, async_client: AsyncClient) -> None:
        """
        Test that /health returns 200 with expected fields.

        Expected response:
        {
            "status": "healthy",
            "engine": "vllm",
            "model": "Qwen2.5-0.5B-Instruct",
            "gpu_available": true
        }
        """
        # [PLACEHOLDER] when async_client is connected to real app:
        # response = await async_client.get("/health")
        # assert response.status_code == 200
        # data = response.json()
        # assert data["status"] == "healthy"
        # assert "engine" in data
        # assert "model" in data
        # assert "gpu_available" in data
        pass

    async def test_health_never_returns_500_for_engine_not_ready(
        self, async_client: AsyncClient
    ) -> None:
        """
        Even if engine is not fully initialized, /health should return 200.
        The service should be resilient.
        """
        # [PLACEHOLDER]
        pass


# ---------- Metrics ----------

@pytest.mark.asyncio
class TestMetrics:
    """Tests for GET /metrics."""

    async def test_metrics_returns_prometheus_text(
        self, async_client: AsyncClient, mock_metrics_text: str
    ) -> None:
        """
        Test that /metrics returns Prometheus text format.
        Should include vllm_* and inference_service_* metrics.
        """
        # [PLACEHOLDER]
        # response = await async_client.get("/metrics")
        # assert response.status_code == 200
        # assert "vllm_" in response.text
        pass

    async def test_metrics_content_type(
        self, async_client: AsyncClient
    ) -> None:
        """Test that /metrics has correct content type."""
        # [PLACEHOLDER]
        # response = await async_client.get("/metrics")
        # assert response.status_code == 200
        pass


# ---------- Chat Completions ----------

@pytest.mark.asyncio
class TestChatCompletions:
    """Tests for POST /v1/chat/completions."""

    async def test_chat_basic_request(
        self,
        async_client: AsyncClient,
        mock_vllm_response: dict[str, Any],
    ) -> None:
        """
        Test basic non-streaming /v1/chat/completions request.

        [PLACEHOLDER]
        Monkeypatch the engine to return mock_vllm_response,
        then verify the response matches expected format.
        """
        # 1. monkeypatch engine.predict() → mock_vllm_response
        # 2. POST /v1/chat/completions with valid body
        # 3. assert response.status_code == 200
        # 4. assert "choices" in response.json()
        # 5. assert response.json()["choices"][0]["message"]["role"] == "assistant"
        pass

    async def test_chat_with_system_message(
        self,
        async_client: AsyncClient,
        mock_vllm_response: dict[str, Any],
    ) -> None:
        """
        Test that system messages are passed through correctly.
        """
        # [PLACEHOLDER]
        pass

    async def test_chat_streaming(
        self,
        async_client: AsyncClient,
        mock_vllm_stream_chunks: list[str],
    ) -> None:
        """
        Test streaming /v1/chat/completions.

        Verifies:
        - Response is 200
        - Content-Type is text/event-stream
        - Data chunks are in SSE format
        - Ends with "data: [DONE]"
        """
        # [PLACEHOLDER]
        # response = await async_client.post(
        #     "/v1/chat/completions",
        #     json={
        #         "model": "Qwen2.5-0.5B-Instruct",
        #         "messages": [{"role": "user", "content": "Count to 3"}],
        #         "stream": True,
        #     },
        #     timeout=30.0,
        # )
        # assert response.status_code == 200
        # assert "text/event-stream" in response.headers.get("content-type", "")
        pass

    async def test_chat_with_stop_token(
        self,
        async_client: AsyncClient,
        mock_vllm_response: dict[str, Any],
    ) -> None:
        """Test that stop tokens are passed to engine."""
        # [PLACEHOLDER]
        pass

    async def test_chat_temperature_validation(
        self, async_client: AsyncClient
    ) -> None:
        """
        Test that temperature > 2.0 raises 422 validation error.
        """
        # [PLACEHOLDER]
        # response = await async_client.post(
        #     "/v1/chat/completions",
        #     json={
        #         "model": "Qwen2.5-0.5B-Instruct",
        #         "messages": [{"role": "user", "content": "Hi"}],
        #         "temperature": 3.0,  # invalid: max is 2.0
        #     },
        # )
        # assert response.status_code == 422
        pass


# ---------- Error Cases ----------

@pytest.mark.asyncio
class TestErrorCases:
    """Tests for error responses."""

    async def test_invalid_model_returns_404(
        self, async_client: AsyncClient
    ) -> None:
        """
        Test that requesting an unknown model returns 404.

        Expected:
        {
            "error": {
                "message": "Model not found: nonexistent-model",
                "type": "invalid_request_error",
                "code": "model_not_found"
            }
        }
        """
        # [PLACEHOLDER]
        pass

    async def test_empty_messages_returns_422(
        self, async_client: AsyncClient
    ) -> None:
        """
        Test that empty messages array returns 422.
        """
        # [PLACEHOLDER]
        # response = await async_client.post(
        #     "/v1/chat/completions",
        #     json={
        #         "model": "Qwen2.5-0.5B-Instruct",
        #         "messages": [],
        #     },
        # )
        # assert response.status_code == 422
        pass

    async def test_missing_model_field_returns_422(
        self, async_client: AsyncClient
    ) -> None:
        """Test that missing model field returns 422."""
        # [PLACEHOLDER]
        pass

    async def test_downstream_error_returns_502(
        self, async_client: AsyncClient
    ) -> None:
        """Test that engine error returns 502 Bad Gateway."""
        # [PLACEHOLDER]
        pass
```

## 测试覆盖矩阵

| 测试 | 方法 | 描述 | 状态 |
|------|------|------|------|
| `test_health_returns_200` | GET /health | 健康检查返回 200 | [PLACEHOLDER] |
| `test_health_never_returns_500` | GET /health | 服务韧性 | [PLACEHOLDER] |
| `test_metrics_returns_prometheus_text` | GET /metrics | Prometheus 格式 | [PLACEHOLDER] |
| `test_chat_basic_request` | POST /v1/chat/completions | 基本推理 | [PLACEHOLDER] |
| `test_chat_with_system_message` | POST /v1/chat/completions | 系统消息 | [PLACEHOLDER] |
| `test_chat_streaming` | POST /v1/chat/completions | 流式输出 | [PLACEHOLDER] |
| `test_chat_with_stop_token` | POST /v1/chat/completions | stop token | [PLACEHOLDER] |
| `test_chat_temperature_validation` | POST /v1/chat/completions | 参数校验 | [PLACEHOLDER] |
| `test_invalid_model_returns_404` | POST /v1/chat/completions | 未知模型 | [PLACEHOLDER] |
| `test_empty_messages_returns_422` | POST /v1/chat/completions | 空消息 | [PLACEHOLDER] |

---

Sources:
1. https://docs.pytest.org/en/latest/ — pytest
2. https://www.python-httpx.org/ — httpx

Risk of Staleness:
- FastAPI TestClient / AsyncClient API 稳定
