# ai-gateway Auth Middleware Blueprint v1

## Task ID: T1002
## Title: ai-gateway Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T902 scaffold（pyproject / curl catalog），产出鉴权中间件蓝图。

---

# ai-gateway Auth Middleware Blueprint v1

## 概述

本文档定义 `src/ai_gateway/middleware/auth.py` 的蓝图——Bearer token 鉴权中间件。

## `src/ai_gateway/middleware/auth.py` 模板

```python
# src/ai_gateway/middleware/auth.py
"""
API Key authentication middleware for ai-gateway.

Supports Bearer token authentication via Authorization header.
"""
from __future__ import annotations

from typing import Optional

from fastapi import HTTPException, Request


class AuthMiddleware:
    """
    API Key authentication middleware.

    Validates Bearer token against configured api_keys.
    """

    def __init__(self, api_keys: list[str], enabled: bool = True) -> None:
        """
        Args:
            api_keys: List of valid API keys.
            enabled: If False, bypass auth (for dev mode).
        """
        self.api_keys = set(api_keys)
        self.enabled = enabled

    async def __call__(self, request: Request) -> Optional[str]:
        """
        Verify the request's Authorization header.

        Returns:
            The validated API key string.

        Raises:
            HTTPException(401): If auth is enabled but token is missing or invalid.
        """
        if not self.enabled:
            return None

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(
                status_code=401,
                detail={
                    "message": "Missing Authorization header",
                    "type": "authentication_error",
                    "code": "401",
                },
            )

        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail={
                    "message": "Invalid Authorization header format. Expected: Bearer <key>",
                    "type": "authentication_error",
                    "code": "401",
                },
            )

        token = auth_header[7:]  # Strip "Bearer " prefix

        if token not in self.api_keys:
            raise HTTPException(
                status_code=401,
                detail={
                    "message": "Invalid API key",
                    "type": "authentication_error",
                    "code": "401",
                },
            )

        return token


async def verify_bearer_token(request: Request) -> str:
    """
    Convenience function to verify bearer token from request.

    Gets api_keys and enabled from app state config.
    [PLACEHOLDER] when server.py is implemented:
        config = request.app.state.config
        middleware = AuthMiddleware(
            api_keys=config.auth.api_keys,
            enabled=config.auth.enabled,
        )
        return await middleware(request)
    """
    # [PLACEHOLDER] real implementation
    return "sk-test-key-1"


def create_auth_middleware(config: dict) -> AuthMiddleware:
    """
    Factory to create AuthMiddleware from config dict.

    Args:
        config: dict with 'enabled' and 'api_keys' fields.
    """
    return AuthMiddleware(
        api_keys=config.get("api_keys", []),
        enabled=config.get("enabled", True),
    )
```

## 鉴权流程

```
Request
  ↓
Authorization header present?
  ├─ No → 401 Missing Authorization header
  └─ Yes
       ↓
      Bearer prefix?
       ├─ No → 401 Invalid format
       └─ Yes
            ↓
           Token in api_keys?
            ├─ No → 401 Invalid API key
            └─ Yes → 200, proceed to handler
```

## Auth 错误响应

| 场景 | HTTP 状态码 | error.type | error.message |
|------|------------|-----------|---------------|
| 无 Authorization header | 401 | authentication_error | Missing Authorization header |
| 非 Bearer 格式 | 401 | authentication_error | Invalid Authorization header format |
| Token 不在 api_keys 中 | 401 | authentication_error | Invalid API key |
| Auth disabled | — | — | bypassed |

---

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey auth reference
2. https://fastapi.tiangolo.com/tutorial/middleware/ — FastAPI middleware

Risk of Staleness:
- Auth middleware API 稳定
