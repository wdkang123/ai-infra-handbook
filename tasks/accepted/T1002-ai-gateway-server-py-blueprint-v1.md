# ai-gateway server.py Blueprint v1

## Task ID: T1002
## Title: ai-gateway Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T902 scaffold（curl catalog / run-script / test-fixture-map），产出 `server.py` FastAPI 服务蓝图。

---

# ai-gateway server.py Blueprint v1

## 概述

本文档定义 `src/ai_gateway/server.py` 的蓝图——FastAPI 应用，包含代理、鉴权和限流中间件。

## `src/ai_gateway/server.py` 模板

```python
# src/ai_gateway/server.py
"""
FastAPI server for ai-gateway.

功能：
- 路由：代理 /v1/chat/completions 到下游 inference-service
- 鉴权：Bearer token 验证
- 限流：sliding_window RPM 限制
- 观测：/health, /metrics
"""
from __future__ import annotations

from typing import Any, AsyncIterator, Optional

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# ---------- Limiter ----------
limiter = Limiter(key_func=get_remote_address)

# ---------- App ----------
app = FastAPI(
    title="ai-gateway",
    description="AI Gateway: proxy, auth, rate-limit, and observability layer",
    version="0.1.0",
)

# Add rate limiter to app state
app.state.limiter = limiter

# ---------- Config (set by main.py) ----------
_config: Any = None  # [PLACEHOLDER] AiGatewayConfig instance


def set_config(config: Any) -> None:
    global _config
    _config = config


def get_config() -> Any:
    if _config is None:
        raise RuntimeError("Config not initialized. Call set_config() first.")
    return _config


# ---------- Request Models ----------

class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionsRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=256, ge=1, le=32768)
    stream: bool = False
    stop: Optional[list[str]] = None


class HealthResponse(BaseModel):
    status: str
    version: str


# ---------- Middleware: Auth ----------

async def verify_api_key(request: Request) -> str | None:
    """
    Verify Bearer token from Authorization header.

    Returns the API key if valid, None if auth is disabled.
    Raises HTTPException(401) if token is invalid.

    [PLACEHOLDER] 真实实现：从 middleware/auth.py 导入
    """
    # [PLACEHOLDER]
    # from ai_gateway.middleware.auth import verify_bearer_token
    # return await verify_bearer_token(request)
    enabled = get_config().auth.get("enabled", True) if _config else False
    if not enabled:
        return None
    # Placeholder: always pass
    return "dev-gateway-key-1"


# ---------- Health ----------

@app.get("/health", response_model=HealthResponse, tags=["observability"])
async def health() -> HealthResponse:
    """Health check endpoint."""
    from ai_gateway import __version__
    return HealthResponse(status="healthy", version=__version__)


# ---------- Metrics ----------

@app.get("/metrics", tags=["observability"])
async def metrics() -> str:
    """
    Prometheus metrics endpoint.

    [PLACEHOLDER] 真实实现：
    from prometheus_client import generate_latest
    return Response(
        content=generate_latest(),
        media_type="text/plain",
    )
    """
    return "# metrics placeholder\nai_gateway_requests_total 0\n"


# ---------- Proxy: Chat Completions ----------

@app.post("/v1/chat/completions")
@limiter.limit("60/minute")  # [PLACEHOLDER] make configurable per model
async def chat_completions(
    request: Request,
    body: ChatCompletionsRequest,
) -> JSONResponse | StreamingResponse:
    """
    Proxy /v1/chat/completions to downstream inference-service.

    Flow:
    1. Verify API key (via verify_api_key)
    2. Route to downstream by model name
    3. Forward request
    4. Return response (streaming or non-streaming)
    """
    # 1. Auth
    await verify_api_key(request)

    # 2. Route
    config = get_config()
    downstream_url = _route_model(body.model, config)
    if downstream_url is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": f"Model not found: {body.model}",
                "type": "invalid_request_error",
                "code": "model_not_found",
            }
        )

    # 3. Forward request
    # [PLACEHOLDER] 真实实现：
    # from ai_gateway.router import forward_chat_request
    # return await forward_chat_request(body, downstream_url)
    return JSONResponse(
        status_code=200,
        content={
            "id": "chatcmpl-proxy-placeholder",
            "object": "chat.completion",
            "created": 1234567890,
            "model": body.model,
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": "[PLACEHOLDER] proxied response"},
                "finish_reason": "stop",
            }],
            "usage": {"prompt_tokens": 10, "completion_tokens": 8, "total_tokens": 18},
        },
    )


def _route_model(model_name: str, config: Any) -> str | None:
    """
    Route model name to downstream base_url.

    [PLACEHOLDER] 真实实现：
    from ai_gateway.router import Router
    router = Router(config.models)
    return router.route(model_name)
    """
    # Placeholder routing
    if model_name == "vllm-local":
        return "http://localhost:8000/v1"
    return None


# ---------- Error Handlers ----------

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Return 429 with OpenAI error format."""
    return JSONResponse(
        status_code=429,
        content={
            "error": {
                "message": "Rate limit exceeded",
                "type": "rate_limit_error",
                "code": "429",
            }
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Return errors in OpenAI error format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail.get("message", str(exc.detail)),
                "type": exc.detail.get("type", "invalid_request_error"),
                "code": str(exc.status_code),
            }
        },
    )
```

## API 契约

| 端点 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/metrics` | GET | Prometheus metrics |
| `/v1/chat/completions` | POST | 代理推理请求 |

## 错误响应格式

```json
{
  "error": {
    "message": "Error description",
    "type": "authentication_error | rate_limit_error | invalid_request_error",
    "code": "401 | 404 | 429 | ..."
  }
}
```

---

Sources:
1. https://github.com/Portkey-AI/gateway — Portkey Gateway reference
2. https://github.com/laurentS/slowapi — Slowapi

Risk of Staleness:
- Slowapi rate limit format may vary by version
