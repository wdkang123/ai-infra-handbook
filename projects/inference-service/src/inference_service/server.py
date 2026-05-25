from __future__ import annotations

import json
import time
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from inference_service.api.metrics import render_metrics
from inference_service.config import get_config
from inference_service.engines import (
    EngineError,
    GenerationRequest,
    GenerationResult,
    InferenceEngine,
    StreamEvent,
    create_engine,
    estimate_messages_token_count,
    estimate_token_count,
)
from inference_service.runtime import InferenceEventLog, InferenceMetrics

app = FastAPI(title="inference-service", version="0.1.0")
_engine: InferenceEngine | None = None
_config: Any = None
_metrics = InferenceMetrics()
_event_log = InferenceEventLog()


def set_engine(engine: InferenceEngine) -> None:
    global _engine
    _engine = engine


def get_engine() -> InferenceEngine:
    global _engine
    cfg = get_runtime_config()
    if _engine is None:
        _engine = create_engine(cfg)
    return _engine


def set_config(config: Any) -> None:
    global _config, _engine, _metrics, _event_log
    _config = config
    _engine = None
    _metrics = InferenceMetrics()
    _event_log = InferenceEventLog()


def get_runtime_config() -> Any:
    return _config or get_config()


def get_runtime_metrics() -> InferenceMetrics:
    return _metrics


def get_event_log() -> InferenceEventLog:
    return _event_log


class HealthResponse(BaseModel):
    status: str
    engine: str
    model: str
    gpu_available: bool


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionsRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=256, ge=1, le=32768)
    stream: bool = False


def _get_request_id(request: Request) -> str:
    return request.headers.get("x-request-id") or f"req_{uuid4().hex[:12]}"


def _build_generation_request(body: ChatCompletionsRequest) -> GenerationRequest:
    return GenerationRequest(
        model=body.model,
        prompt=body.messages[-1].content,
        messages=[message.model_dump() for message in body.messages],
        temperature=body.temperature,
        max_tokens=body.max_tokens,
    )


def _build_chat_completion(model: str, result: GenerationResult) -> dict[str, Any]:
    return {
        "id": "chatcmpl-mock-001",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": result.content,
                },
                "finish_reason": result.finish_reason,
            }
        ],
        "usage": {
            "prompt_tokens": result.prompt_tokens,
            "completion_tokens": result.completion_tokens,
            "total_tokens": result.total_tokens,
        },
    }


def _build_stream_chunk(
    completion_id: str,
    model: str,
    *,
    delta: dict[str, str] | None = None,
    finish_reason: str | None = None,
) -> str:
    payload = {
        "id": completion_id,
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "delta": delta or {},
                "finish_reason": finish_reason,
            }
        ],
    }
    return f"data: {json.dumps(payload)}\n\n"


def _build_stream_error(message: str, error_type: str, code: str) -> str:
    payload = {
        "error": {
            "message": message,
            "type": error_type,
            "code": code,
        }
    }
    return f"data: {json.dumps(payload)}\n\n"


async def _stream_chat_completion(
    model: str,
    engine: InferenceEngine,
    generation_request: GenerationRequest,
    metrics: InferenceMetrics,
    request_id: str,
):
    completion_id = "chatcmpl-mock-stream-001"
    prompt_tokens = estimate_messages_token_count(generation_request.messages)
    completion_parts: list[str] = []
    event_log = get_event_log()
    event_log.append(
        "engine_stream_start",
        request_id=request_id,
        requested_model=generation_request.model,
        engine=engine.name,
    )
    try:
        async for event in engine.stream(generation_request):
            if event.delta and event.delta.get("content"):
                completion_parts.append(event.delta["content"])
            yield _build_stream_event(completion_id, model, event)
        yield "data: [DONE]\n\n"
        completion_tokens = estimate_token_count("".join(completion_parts))
        metrics.successful_requests += 1
        metrics.prompt_tokens_total += prompt_tokens
        metrics.completion_tokens_total += completion_tokens
        event_log.append(
            "request_success",
            request_id=request_id,
            requested_model=generation_request.model,
            engine=engine.name,
            stream=True,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
        )
    except EngineError as exc:
        metrics.failed_requests += 1
        event_log.append(
            "engine_error",
            request_id=request_id,
            requested_model=generation_request.model,
            engine=engine.name,
            stream=True,
            status_code=exc.status_code,
            code=exc.code,
        )
        yield _build_stream_error(exc.message, exc.error_type, exc.code)
        yield "data: [DONE]\n\n"
    except Exception:
        metrics.failed_requests += 1
        event_log.append(
            "engine_error",
            request_id=request_id,
            requested_model=generation_request.model,
            engine=engine.name,
            stream=True,
            status_code=500,
            code="500",
        )
        yield _build_stream_error(
            "Inference engine failed while streaming",
            "internal_server_error",
            "500",
        )
        yield "data: [DONE]\n\n"
    finally:
        metrics.running_requests -= 1


def _build_stream_event(completion_id: str, model: str, event: StreamEvent) -> str:
    return _build_stream_chunk(
        completion_id,
        model,
        delta=event.delta,
        finish_reason=event.finish_reason,
    )


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    cfg = get_runtime_config()
    engine_name = get_engine().name
    return HealthResponse(
        status="healthy",
        engine=engine_name,
        model=cfg.engine.model_path,
        gpu_available=False,
    )


@app.get("/v1/models")
async def list_models() -> dict[str, Any]:
    cfg = get_runtime_config()
    return {
        "object": "list",
        "data": [
            {
                "id": cfg.engine.model_path,
                "object": "model",
                "created": 0,
                "owned_by": "inference-service",
                "metadata": {
                    "engine": get_engine().name,
                    "gpu_available": False,
                },
            }
        ],
    }


@app.get("/events")
async def events(
    limit: int = 50,
    event_type: str | None = None,
    request_id: str | None = None,
    requested_model: str | None = None,
) -> dict[str, Any]:
    bounded_limit = max(1, min(limit, 100))
    return {
        "events": get_event_log().snapshot(
            bounded_limit,
            event_type=event_type,
            request_id=request_id,
            requested_model=requested_model,
        ),
        "filters": {
            "event_type": event_type,
            "request_id": request_id,
            "requested_model": requested_model,
        },
        "limit": bounded_limit,
    }


@app.get("/events/summary")
async def events_summary(
    limit: int = 100,
    event_type: str | None = None,
    request_id: str | None = None,
    requested_model: str | None = None,
) -> dict[str, Any]:
    bounded_limit = max(1, min(limit, 100))
    summary = get_event_log().summarize(
        bounded_limit,
        event_type=event_type,
        request_id=request_id,
        requested_model=requested_model,
    )
    return {
        "summary": summary,
        "filters": {
            "event_type": event_type,
            "request_id": request_id,
            "requested_model": requested_model,
        },
        "limit": bounded_limit,
    }


@app.get("/events/requests")
async def event_request_index(
    limit: int = 20,
    requested_model: str | None = None,
) -> dict[str, Any]:
    bounded_limit = max(1, min(limit, 100))
    index = get_event_log().request_index(bounded_limit, requested_model=requested_model)
    return {
        "request_index": index,
        "filters": {"requested_model": requested_model},
        "limit": bounded_limit,
    }


@app.get("/events/requests/{request_id}")
async def event_request_timeline(request_id: str) -> dict[str, Any]:
    return {"timeline": get_event_log().timeline(request_id)}


@app.post("/v1/chat/completions")
async def chat_completions(request: Request, body: ChatCompletionsRequest) -> Response:
    cfg = get_runtime_config()
    metrics = get_runtime_metrics()
    event_log = get_event_log()
    request_id = _get_request_id(request)
    metrics.total_requests += 1
    metrics.running_requests += 1
    event_log.append(
        "request_received",
        request_id=request_id,
        requested_model=body.model,
        stream=body.stream,
    )
    if not body.messages:
        metrics.failed_requests += 1
        metrics.running_requests -= 1
        event_log.append(
            "validation_failed",
            request_id=request_id,
            requested_model=body.model,
            reason="empty_messages",
        )
        raise HTTPException(
            status_code=422,
            detail={
                "message": "messages must not be empty",
                "type": "invalid_request_error",
                "code": "422",
            },
        )
    if body.model != cfg.engine.model_path:
        metrics.failed_requests += 1
        metrics.running_requests -= 1
        event_log.append(
            "model_not_found",
            request_id=request_id,
            requested_model=body.model,
            configured_model=cfg.engine.model_path,
        )
        raise HTTPException(
            status_code=404,
            detail={
                "message": f"Model not found: {body.model}",
                "type": "invalid_request_error",
                "code": "404",
            },
        )

    engine = get_engine()
    generation_request = _build_generation_request(body)
    if body.stream:
        return StreamingResponse(
            _stream_chat_completion(cfg.engine.model_path, engine, generation_request, metrics, request_id),
            media_type="text/event-stream",
            headers={"x-request-id": request_id},
        )

    try:
        event_log.append(
            "engine_generate_start",
            request_id=request_id,
            requested_model=body.model,
            engine=engine.name,
        )
        generation_result = await engine.generate(generation_request)
    except EngineError as exc:
        metrics.failed_requests += 1
        metrics.running_requests -= 1
        event_log.append(
            "engine_error",
            request_id=request_id,
            requested_model=body.model,
            engine=engine.name,
            stream=False,
            status_code=exc.status_code,
            code=exc.code,
        )
        raise HTTPException(
            status_code=exc.status_code,
            detail={
                "message": exc.message,
                "type": exc.error_type,
                "code": exc.code,
            },
        ) from exc
    except Exception as exc:
        metrics.failed_requests += 1
        metrics.running_requests -= 1
        event_log.append(
            "engine_error",
            request_id=request_id,
            requested_model=body.model,
            engine=engine.name,
            stream=False,
            status_code=500,
            code="500",
        )
        raise HTTPException(
            status_code=500,
            detail={
                "message": f"Inference engine failed: {exc}",
                "type": "internal_server_error",
                "code": "500",
            },
        ) from exc

    response = _build_chat_completion(cfg.engine.model_path, generation_result)
    metrics.successful_requests += 1
    metrics.prompt_tokens_total += response["usage"]["prompt_tokens"]
    metrics.completion_tokens_total += response["usage"]["completion_tokens"]
    metrics.running_requests -= 1
    event_log.append(
        "request_success",
        request_id=request_id,
        requested_model=body.model,
        engine=engine.name,
        stream=False,
        prompt_tokens=response["usage"]["prompt_tokens"],
        completion_tokens=response["usage"]["completion_tokens"],
    )
    return JSONResponse(content=response, headers={"x-request-id": request_id})


@app.get("/metrics")
async def metrics() -> Response:
    return Response(content=render_metrics(get_runtime_metrics()), media_type="text/plain")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    detail = exc.detail if isinstance(exc.detail, dict) else {"message": str(exc.detail)}
    return JSONResponse(
        status_code=exc.status_code,
        headers={"x-request-id": _get_request_id(request)},
        content={
            "error": {
                "message": detail.get("message", str(exc.detail)),
                "type": detail.get("type", "invalid_request_error"),
                "code": str(detail.get("code", exc.status_code)),
            }
        },
    )
