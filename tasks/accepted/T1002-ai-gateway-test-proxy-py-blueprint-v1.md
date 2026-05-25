# ai-gateway test_proxy.py Blueprint v1

## Task ID: T1002
## Title: ai-gateway Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T902 scaffold（test-fixture-map / curl catalog），产出 `test_proxy.py` 蓝图。

---

# ai-gateway test_proxy.py Blueprint v1

## 概述

本文档定义 `tests/test_proxy.py` 的蓝图——代理、路由和鉴权的单元测试。

## `tests/test_proxy.py` 模板

```python
# tests/test_proxy.py
"""
Proxy and routing tests for ai-gateway.

Tests:
- Auth: valid key, invalid key, missing key
- Routing: known model → correct downstream
- Routing: unknown model → 404
- Rate limit: 429 response
- Proxy: 200 response forwarded
- Error: downstream 500 → 502
"""
from __future__ import annotations

from typing import Any

import pytest
from httpx import AsyncClient


# ---------- Auth Tests ----------

@pytest.mark.asyncio
class TestAuth:
    """Tests for API key authentication."""

    async def test_valid_key_passes(
        self,
        async_client: AsyncClient,
        auth_headers: dict[str, str],
        mock_downstream_success: dict[str, Any],
    ) -> None:
        """
        Test that a valid Authorization header passes auth.

        [PLACEHOLDER]
        Monkeypatch httpx client to return mock_downstream_success,
        then POST /v1/chat/completions with auth_headers.
        Assert 200.
        """
        pass

    async def test_missing_key_returns_401(
        self, async_client: AsyncClient
    ) -> None:
        """
        Test that missing Authorization header returns 401.

        Expected: 401 with error.type == "authentication_error"
        """
        # [PLACEHOLDER]
        # response = await async_client.post(
        #     "/v1/chat/completions",
        #     json={"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]},
        # )
        # assert response.status_code == 401
        # data = response.json()
        # assert data["error"]["type"] == "authentication_error"
        pass

    async def test_invalid_key_returns_401(
        self,
        async_client: AsyncClient,
        invalid_auth_headers: dict[str, str],
    ) -> None:
        """
        Test that invalid API key returns 401.

        Expected: 401 with error.message == "Invalid API key"
        """
        # [PLACEHOLDER]
        pass

    async def test_wrong_auth_scheme_returns_401(
        self, async_client: AsyncClient
    ) -> None:
        """
        Test that non-Bearer auth scheme returns 401.
        """
        # [PLACEHOLDER]
        # response = await async_client.post(
        #     "/v1/chat/completions",
        #     headers={"Authorization": "Basic dXNlcjpwYXNz"},
        #     json={"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]},
        # )
        # assert response.status_code == 401
        pass


# ---------- Routing Tests ----------

@pytest.mark.asyncio
class TestRouting:
    """Tests for downstream model routing."""

    async def test_known_model_routes_to_correct_url(
        self,
        async_client: AsyncClient,
        auth_headers: dict[str, str],
    ) -> None:
        """
        Test that a known model name routes to the correct downstream URL.

        [PLACEHOLDER]
        Mock httpx to capture the URL being requested.
        Assert that vllm-local → http://localhost:8000/v1
        """
        pass

    async def test_unknown_model_returns_404(
        self,
        async_client: AsyncClient,
        auth_headers: dict[str, str],
    ) -> None:
        """
        Test that an unknown model returns 404.

        Expected: 404 with error.code == "model_not_found"
        """
        # [PLACEHOLDER]
        # response = await async_client.post(
        #     "/v1/chat/completions",
        #     headers=auth_headers,
        #     json={
        #         "model": "unknown-model-xyz",
        #         "messages": [{"role": "user", "content": "Hi"}],
        #     },
        # )
        # assert response.status_code == 404
        pass


# ---------- Proxy Tests ----------

@pytest.mark.asyncio
class TestProxy:
    """Tests for proxying requests to downstream inference-service."""

    async def test_proxy_success_returns_200(
        self,
        async_client: AsyncClient,
        auth_headers: dict[str, str],
        mock_downstream_success: dict[str, Any],
    ) -> None:
        """
        Test that a successful downstream response is returned as-is.
        """
        # [PLACEHOLDER]
        pass

    async def test_proxy_streaming(
        self,
        async_client: AsyncClient,
        auth_headers: dict[str, str],
    ) -> None:
        """
        Test that streaming responses from downstream are streamed back.
        """
        # [PLACEHOLDER]
        pass

    async def test_proxy_downstream_500_returns_502(
        self,
        async_client: AsyncClient,
        auth_headers: dict[str, str],
        mock_downstream_500: dict[str, Any],
    ) -> None:
        """
        Test that downstream 500 is transformed to 502 Bad Gateway.
        """
        # [PLACEHOLDER]
        pass

    async def test_proxy_downstream_rate_limit_returns_429(
        self,
        async_client: AsyncClient,
        auth_headers: dict[str, str],
        mock_downstream_rate_limit: dict[str, Any],
    ) -> None:
        """
        Test that downstream 429 is returned as 429 (not transformed).
        """
        # [PLACEHOLDER]
        pass

    async def test_proxy_preserves_request_body(
        self,
        async_client: AsyncClient,
        auth_headers: dict[str, str],
    ) -> None:
        """
        Test that temperature, max_tokens, stop tokens are forwarded.
        """
        # [PLACEHOLDER]
        pass


# ---------- Rate Limit Tests ----------

@pytest.mark.asyncio
class TestRateLimit:
    """Tests for rate limiting middleware."""

    async def test_exceed_rpm_returns_429(
        self,
        async_client: AsyncClient,
        auth_headers: dict[str, str],
    ) -> None:
        """
        Test that exceeding RPM limit returns 429.

        Send 65 requests rapidly, expect ~5 to get 429.
        """
        # [PLACEHOLDER] Note: slowapi test may need special setup
        pass

    async def test_rate_limit_per_model(
        self,
        async_client: AsyncClient,
        auth_headers: dict[str, str],
    ) -> None:
        """
        Test that per-model RPM limits are enforced.

        If vllm-local has higher RPM than openai-gpt4,
        sending to openai-gpt4 should hit limit first.
        """
        # [PLACEHOLDER]
        pass
```

## 测试覆盖矩阵

| 测试 | 描述 | 依赖 |
|------|------|------|
| `test_valid_key_passes` | 有效 key 通过 | `auth_headers`, `mock_downstream_success` |
| `test_missing_key_returns_401` | 无 key → 401 | — |
| `test_invalid_key_returns_401` | 无效 key → 401 | `invalid_auth_headers` |
| `test_wrong_auth_scheme_returns_401` | 非 Bearer → 401 | — |
| `test_known_model_routes_correct` | 已知模型路由正确 | `auth_headers` |
| `test_unknown_model_returns_404` | 未知模型 → 404 | `auth_headers` |
| `test_proxy_success_returns_200` | 成功代理 | `auth_headers`, `mock_downstream_success` |
| `test_proxy_streaming` | 流式代理 | `auth_headers` |
| `test_proxy_downstream_500_returns_502` | 下游 500 → 502 | `auth_headers`, `mock_downstream_500` |
| `test_exceed_rpm_returns_429` | 超 RPM → 429 | `auth_headers` |

---

Sources:
1. https://pytest.org/ — pytest
2. https://github.com/laurentS/slowapi — Slowapi

Risk of Staleness:
- Rate limit testing may need slowapi-specific test utilities
