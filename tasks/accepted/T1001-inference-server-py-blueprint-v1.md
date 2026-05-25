# inference-service server.py Blueprint v1

## Task ID: T1001
## Title: inference-service Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T901 scaffold（curl catalog / run-script），产出 `server.py` FastAPI 服务蓝图。

---

# inference-service server.py Blueprint v1

## 概述

本文档定义 `src/inference_service/server.py` 的蓝图——FastAPI 应用，包含 /health、/metrics 和 /v1/chat/completions 三个 MVP 必须端点。

## `src/inference_service/server.py` 模板

```python
# src/inference_service/server.py
"""
FastAPI server for inference-service.

MVP 端点：
- GET  /health        — 健康检查
- GET  /metrics       — Prometheus metrics
- POST /v1/chat/completions — OpenAI 兼容推理
"""
from __future__ import annotations

from typing import Any, AsyncIterator, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

# ---------- App ----------
app = FastAPI(
    title="inference-service",
    description="OpenAI-compatible inference service powered by vLLM",
    version="0.1.0",
)

# ---------- Request/Response Models ----------

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
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)
    frequency_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)
    presence_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)


class UsageInfo(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatMessageResponse(BaseModel):
    role: str
    content: str


class ChatCompletionsChoice(BaseModel):
    index: int
    message: ChatMessageResponse
    finish_reason: Optional[str] = None


class ChatCompletionsResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list[ChatCompletionsChoice]
    usage: UsageInfo
    service_tier: Optional[str] = None
    system_fingerprint: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    engine: str
    model: str
    gpu_available: bool


# ---------- State (set by main.py on startup) ----------
_engine: Any = None  # [PLACEHOLDER] VLLMEngine instance


def set_engine(engine: Any) -> None:
    """Called by main.py to inject the engine after init."""
    global _engine
    _engine = engine


def get_engine() -> Any:
    """Get the current engine. Raises if not initialized."""
    if _engine is None:
        raise RuntimeError("Engine not initialized. Call set_engine() first.")
    return _engine


# ---------- Health ----------

@app.get("/health", response_model=HealthResponse, tags=["observability"])
async def health() -> HealthResponse:
    """
    Health check endpoint.

    Returns 200 with status even if engine is not fully loaded.
    """
    # [PLACEHOLDER] 真实实现从 _engine 读取状态
    return HealthResponse(
        status="healthy",
        engine="vllm",  # [PLACEHOLDER] from _engine.engine_type
        model="Qwen2.5-0.5B-Instruct",  # [PLACEHOLDER] from _engine.model_name
        gpu_available=True,  # [PLACEHOLDER] check via torch.cuda.is_available()
    )


# ---------- Metrics ----------

@app.get("/metrics", tags=["observability"])
async def metrics() -> str:
    """
    Prometheus metrics endpoint.

    Returns metrics in Prometheus text format.
    """
    # [PLACEHOLDER] 真实实现：
    # from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    # return StreamingResponse(
    #     iter([generate_latest()]),
    #     media_type=CONTENT_TYPE_LATEST,
    # )
    # [PLACEHOLDER] 真实实现应返回 Prometheus client 生成的指标，
    # 包含 vLLM 指标（vllm_num_requests_running、vllm_num_tokens_total 等）
    # 和 inference_service 指标（inference_service_requests_total 等）。
    # 下例为对齐 smoke 测试预期，仅作占位：
    return (
        "# metrics placeholder\n"
        "inference_service_requests_total 0\n"
        "vllm_num_requests_running 0\n"
        "vllm_num_tokens_total 0\n"
    )


# ---------- Chat Completions ----------

@app.post("/v1/chat/completions", tags=["inference"])
async def chat_completions(
    request: ChatCompletionsRequest,
) -> ChatCompletionsResponse | StreamingResponse:
    """
    OpenAI-compatible /v1/chat/completions endpoint.

    Supports both streaming and non-streaming responses.
    """
    engine = get_engine()

    if request.stream:
        return StreamingResponse(
            _stream_chat(engine, request),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache"},
        )

    # Non-streaming
    # [PLACEHOLDER] 真实实现：
    # result = engine.predict(
    #     messages=[m.model_dump() for m in request.messages],
    #     temperature=request.temperature,
    #     max_tokens=request.max_tokens,
    #     stop=request.stop,
    # )
    import time
    result = {
        "id": f"chatcmpl-{int(time.time()*1000)}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": request.model,
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": "[PLACEHOLDER] response"},
            "finish_reason": "stop",
        }],
        "usage": {"prompt_tokens": 10, "completion_tokens": 8, "total_tokens": 18},
    }
    return ChatCompletionsResponse(**result)


async def _stream_chat(
    engine: Any,
    request: ChatCompletionsRequest,
) -> AsyncIterator[str]:
    """
    Stream SSE chunks for chat completions.

    Yields strings in the format:
        data: {"id": "...", "choices": [...], ...}
    """
    # [PLACEHOLDER] 真实实现：
    # for chunk in engine.predict_stream(messages, temperature, max_tokens, stop):
    #     yield f"data: {json.dumps(chunk)}\n\n"
    # yield "data: [DONE]\n\n"
    import time
    chunk_id = f"chatcmpl-{int(time.time()*1000)}"
    for i, token in enumerate(["[PLACE", "HOLDER", "]"]):
        chunk = {
            "id": chunk_id,
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": request.model,
            "choices": [{
                "index": 0,
                "delta": {"role": "assistant", "content": token},
                "finish_reason": None,
            }],
        }
        import json
        yield f"data: {json.dumps(chunk)}\n\n"
    done_chunk = {
        "id": chunk_id,
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": request.model,
        "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
    }
    import json
    yield f"data: {json.dumps(done_chunk)}\n\n"
    yield "data: [DONE]\n\n"


# ---------- Error Handlers ----------

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Return errors in OpenAI error format."""
    import json
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail,
                "type": "invalid_request_error",
                "code": str(exc.status_code),
            }
        },
    )
```

## API 契约（来自 T811）

| 端点 | 方法 | 请求体 | 响应 |
|------|------|--------|------|
| `/health` | GET | — | `HealthResponse` |
| `/metrics` | GET | — | Prometheus text |
| `/v1/chat/completions` | POST | `ChatCompletionsRequest` | `ChatCompletionsResponse` 或 SSE stream |

## 错误响应格式

```json
{
  "error": {
    "message": "Error description",
    "type": "invalid_request_error | authentication_error | rate_limit_error | server_error",
    "code": "string"
  }
}
```

---

Sources:
1. https://docs.vllm.ai/ — vLLM OpenAI compatibility
2. https://fastapi.tiangolo.com/ — FastAPI

Risk of Staleness:
- OpenAI API 格式在 v1.0 后相对稳定

Out of Scope Kept:
- 未写 `/v1/completions`
- 未写 `/v1/models`
