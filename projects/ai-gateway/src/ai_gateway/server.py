from __future__ import annotations

import json
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from ai_gateway import __version__
from ai_gateway.config import get_config
from ai_gateway.middleware.auth import verify_bearer_token
from ai_gateway.router import (
    forward_chat_request,
    forward_chat_stream,
    probe_upstream_health,
    route_model_candidates,
)
from ai_gateway.runtime import GatewayEventLog, GatewayMetrics, InMemoryRateLimiter, InMemoryResponseCache

app = FastAPI(title="ai-gateway", version=__version__)
_config: Any = None
_metrics = GatewayMetrics()
_event_log = GatewayEventLog()
_rate_limiter: InMemoryRateLimiter | None = None
_response_cache: InMemoryResponseCache | None = None


def set_config(config: Any) -> None:
    global _config, _rate_limiter, _response_cache, _metrics, _event_log
    _config = config
    _metrics = GatewayMetrics()
    _event_log = GatewayEventLog()
    _rate_limiter = InMemoryRateLimiter(config.rate_limit.requests_per_minute) if config.rate_limit.enabled else None
    _response_cache = (
        InMemoryResponseCache(config.cache.ttl_seconds, config.cache.max_entries) if config.cache.enabled else None
    )


def get_runtime_config() -> Any:
    return _config or get_config()


def get_runtime_metrics() -> GatewayMetrics:
    return _metrics


def get_event_log() -> GatewayEventLog:
    return _event_log


def get_rate_limiter(config: Any) -> InMemoryRateLimiter | None:
    global _rate_limiter
    if not config.rate_limit.enabled:
        _rate_limiter = None
        return None
    if _rate_limiter is None:
        _rate_limiter = InMemoryRateLimiter(config.rate_limit.requests_per_minute)
    return _rate_limiter


def get_response_cache(config: Any) -> InMemoryResponseCache | None:
    global _response_cache
    if not config.cache.enabled:
        _response_cache = None
        return None
    if _response_cache is None:
        _response_cache = InMemoryResponseCache(config.cache.ttl_seconds, config.cache.max_entries)
    return _response_cache


class HealthResponse(BaseModel):
    status: str
    version: str
    upstream_services: dict[str, str]


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionsRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=256, ge=1, le=32768)
    stream: bool = False


@dataclass
class ForwardResult:
    payload: dict[str, Any]
    upstream_model: str
    fallback_used: bool


def _get_request_id(request: Request) -> str:
    return request.headers.get("x-request-id") or f"req_{uuid4().hex[:12]}"


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    cfg = get_runtime_config()
    upstream = {}
    for model in cfg.models:
        upstream[model.name] = await probe_upstream_health(model.base_url)
    overall_status = "healthy"
    if upstream and any(status != "healthy" for status in upstream.values()):
        overall_status = "degraded"
    return HealthResponse(status=overall_status, version=__version__, upstream_services=upstream)


@app.get("/metrics")
async def metrics() -> Response:
    body = get_runtime_metrics().render_prometheus()
    return Response(content=body, media_type="text/plain")


@app.get("/events")
async def events(
    limit: int = 50,
    event_type: str | None = None,
    request_id: str | None = None,
    requested_model: str | None = None,
    upstream_model: str | None = None,
) -> dict[str, Any]:
    bounded_limit = max(1, min(limit, 100))
    return {
        "events": get_event_log().snapshot(
            bounded_limit,
            event_type=event_type,
            request_id=request_id,
            requested_model=requested_model,
            upstream_model=upstream_model,
        ),
        "filters": {
            "event_type": event_type,
            "request_id": request_id,
            "requested_model": requested_model,
            "upstream_model": upstream_model,
        },
        "limit": bounded_limit,
    }


@app.get("/events/summary")
async def events_summary(
    limit: int = 100,
    event_type: str | None = None,
    request_id: str | None = None,
    requested_model: str | None = None,
    upstream_model: str | None = None,
) -> dict[str, Any]:
    bounded_limit = max(1, min(limit, 100))
    summary = get_event_log().summarize(
        bounded_limit,
        event_type=event_type,
        request_id=request_id,
        requested_model=requested_model,
        upstream_model=upstream_model,
    )
    return {
        "summary": summary,
        "filters": {
            "event_type": event_type,
            "request_id": request_id,
            "requested_model": requested_model,
            "upstream_model": upstream_model,
        },
        "limit": bounded_limit,
    }


@app.get("/events/failures")
async def event_failures(
    limit: int = 100,
    requested_model: str | None = None,
    upstream_model: str | None = None,
) -> dict[str, Any]:
    bounded_limit = max(1, min(limit, 100))
    summary = get_event_log().failure_summary(
        bounded_limit,
        requested_model=requested_model,
        upstream_model=upstream_model,
    )
    return {
        "failure_summary": summary,
        "filters": {
            "requested_model": requested_model,
            "upstream_model": upstream_model,
        },
        "limit": bounded_limit,
    }


@app.get("/events/requests")
async def event_request_index(
    limit: int = 20,
    requested_model: str | None = None,
    upstream_model: str | None = None,
) -> dict[str, Any]:
    bounded_limit = max(1, min(limit, 100))
    index = get_event_log().request_index(
        bounded_limit,
        requested_model=requested_model,
        upstream_model=upstream_model,
    )
    return {
        "request_index": index,
        "filters": {
            "requested_model": requested_model,
            "upstream_model": upstream_model,
        },
        "limit": bounded_limit,
    }


@app.get("/events/requests/{request_id}")
async def event_request_timeline(request_id: str) -> dict[str, Any]:
    return {"timeline": get_event_log().timeline(request_id)}


@app.get("/v1/models")
async def list_models() -> dict[str, Any]:
    cfg = get_runtime_config()
    upstream_health = {}
    for model in cfg.models:
        upstream_health[model.name] = await probe_upstream_health(model.base_url)

    return {
        "object": "list",
        "data": [
            {
                "id": model.name,
                "object": "model",
                "created": 0,
                "owned_by": "ai-gateway",
                "metadata": {
                    "target_model": model.target_model or model.name,
                    "fallbacks": model.fallbacks,
                    "fallback_count": len(model.fallbacks),
                    "upstream_health": upstream_health[model.name],
                },
            }
            for model in cfg.models
        ],
    }


def _normalize_error_detail(exc: HTTPException) -> dict[str, str]:
    detail = exc.detail if isinstance(exc.detail, dict) else {"message": str(exc.detail)}
    nested_error = detail.get("error")
    if isinstance(nested_error, dict):
        detail = nested_error

    default_type = "bad_gateway_error" if exc.status_code >= 500 else "invalid_request_error"
    return {
        "message": str(detail.get("message", str(exc.detail))),
        "type": str(detail.get("type", default_type)),
        "code": str(detail.get("code", exc.status_code)),
    }


def _build_stream_error(error: dict[str, str]) -> str:
    return f"data: {json.dumps({'error': error})}\n\n"


async def _stream_via_gateway(
    body: dict[str, Any],
    downstream_models: list[Any],
    metrics_state: GatewayMetrics,
    request_id: str,
) -> AsyncIterator[str]:
    event_log = get_event_log()
    last_error: HTTPException | None = None
    for index, downstream_model in enumerate(downstream_models):
        emitted_chunk = False
        try:
            event_log.append(
                "upstream_attempt",
                request_id=request_id,
                requested_model=body["model"],
                upstream_model=downstream_model.name,
                stream=True,
            )
            async for chunk in forward_chat_stream(body, downstream_model, request_id):
                emitted_chunk = True
                yield chunk
            if index > 0:
                metrics_state.fallback_successes += 1
                event_log.append(
                    "fallback_success",
                    request_id=request_id,
                    requested_model=body["model"],
                    upstream_model=downstream_model.name,
                    stream=True,
                )
            metrics_state.successful_requests += 1
            event_log.append(
                "request_success",
                request_id=request_id,
                requested_model=body["model"],
                upstream_model=downstream_model.name,
                fallback_used=index > 0,
                stream=True,
            )
            return
        except HTTPException as exc:
            last_error = exc
            if exc.status_code >= 500:
                metrics_state.upstream_failures += 1
                if not emitted_chunk and index < len(downstream_models) - 1:
                    metrics_state.fallback_attempts += 1
                    event_log.append(
                        "fallback_attempt",
                        request_id=request_id,
                        requested_model=body["model"],
                        failed_upstream_model=downstream_model.name,
                        next_upstream_model=downstream_models[index + 1].name,
                        status_code=exc.status_code,
                        stream=True,
                    )
                    continue
            event_log.append(
                "stream_error",
                request_id=request_id,
                requested_model=body["model"],
                upstream_model=downstream_model.name,
                status_code=exc.status_code,
                emitted_chunk=emitted_chunk,
            )
            yield _build_stream_error(_normalize_error_detail(exc))
            yield "data: [DONE]\n\n"
            return
        except Exception:
            metrics_state.upstream_failures += 1
            if not emitted_chunk and index < len(downstream_models) - 1:
                metrics_state.fallback_attempts += 1
                event_log.append(
                    "fallback_attempt",
                    request_id=request_id,
                    requested_model=body["model"],
                    failed_upstream_model=downstream_model.name,
                    next_upstream_model=downstream_models[index + 1].name,
                    status_code=502,
                    stream=True,
                )
                continue
            event_log.append(
                "stream_error",
                request_id=request_id,
                requested_model=body["model"],
                upstream_model=downstream_model.name,
                status_code=502,
                emitted_chunk=emitted_chunk,
            )
            yield _build_stream_error(
                {
                    "message": "Downstream stream request failed",
                    "type": "bad_gateway_error",
                    "code": "502",
                }
            )
            yield "data: [DONE]\n\n"
            return

    if last_error is not None:
        yield _build_stream_error(_normalize_error_detail(last_error))
        yield "data: [DONE]\n\n"
        return
    yield _build_stream_error(
        {
            "message": "No downstream model candidates available",
            "type": "bad_gateway_error",
            "code": "502",
        }
    )
    yield "data: [DONE]\n\n"


async def _forward_with_fallback(
    body: dict[str, Any],
    downstream_models: list[Any],
    metrics_state: GatewayMetrics,
    request_id: str,
) -> ForwardResult:
    event_log = get_event_log()
    last_error: HTTPException | None = None
    for index, downstream_model in enumerate(downstream_models):
        try:
            event_log.append(
                "upstream_attempt",
                request_id=request_id,
                requested_model=body["model"],
                upstream_model=downstream_model.name,
                stream=False,
            )
            payload = await forward_chat_request(body, downstream_model, request_id)
            if index > 0:
                metrics_state.fallback_successes += 1
                event_log.append(
                    "fallback_success",
                    request_id=request_id,
                    requested_model=body["model"],
                    upstream_model=downstream_model.name,
                    stream=False,
                )
            return ForwardResult(
                payload=payload,
                upstream_model=downstream_model.name,
                fallback_used=index > 0,
            )
        except HTTPException as exc:
            last_error = exc
            if exc.status_code >= 500:
                metrics_state.upstream_failures += 1
                if index < len(downstream_models) - 1:
                    metrics_state.fallback_attempts += 1
                    event_log.append(
                        "fallback_attempt",
                        request_id=request_id,
                        requested_model=body["model"],
                        failed_upstream_model=downstream_model.name,
                        next_upstream_model=downstream_models[index + 1].name,
                        status_code=exc.status_code,
                        stream=False,
                    )
                    continue
            event_log.append(
                "upstream_error",
                request_id=request_id,
                requested_model=body["model"],
                upstream_model=downstream_model.name,
                status_code=exc.status_code,
                stream=False,
            )
            raise exc

    if last_error is not None:
        raise last_error
    raise HTTPException(
        status_code=502,
        detail={
            "message": "No downstream model candidates available",
            "type": "bad_gateway_error",
            "code": "502",
        },
    )


@app.post("/v1/chat/completions")
async def chat_completions(request: Request, body: ChatCompletionsRequest) -> Response:
    metrics_state = get_runtime_metrics()
    event_log = get_event_log()
    request_id = _get_request_id(request)
    metrics_state.total_requests += 1
    event_log.append(
        "request_received",
        request_id=request_id,
        requested_model=body.model,
        stream=body.stream,
    )

    try:
        token = await verify_bearer_token(request)
    except HTTPException as exc:
        metrics_state.auth_failures += 1
        event_log.append("auth_failed", request_id=request_id, requested_model=body.model, status_code=exc.status_code)
        raise exc

    cfg = get_runtime_config()
    rate_limiter = get_rate_limiter(cfg)
    if token and rate_limiter is not None and not rate_limiter.allow(token):
        metrics_state.rate_limited_requests += 1
        event_log.append("rate_limited", request_id=request_id, requested_model=body.model, status_code=429)
        raise HTTPException(
            status_code=429,
            detail={
                "message": "Rate limit exceeded for API key",
                "type": "rate_limit_error",
                "code": "429",
            },
        )

    downstream_models = route_model_candidates(body.model, cfg.models)
    if not downstream_models:
        event_log.append("route_not_found", request_id=request_id, requested_model=body.model, status_code=404)
        raise HTTPException(
            status_code=404,
            detail={
                "message": f"Model not found: {body.model}",
                "type": "invalid_request_error",
                "code": "404",
            },
        )

    request_payload = body.model_dump()
    if body.stream:
        return StreamingResponse(
            _stream_via_gateway(request_payload, downstream_models, metrics_state, request_id),
            media_type="text/event-stream",
            headers={"x-request-id": request_id},
        )

    response_cache = get_response_cache(cfg)
    if response_cache is not None:
        cached_payload = response_cache.get(token, request_payload)
        if cached_payload is not None:
            metrics_state.cache_hits += 1
            metrics_state.successful_requests += 1
            event_log.append("cache_hit", request_id=request_id, requested_model=body.model)
            return JSONResponse(
                status_code=200,
                content=cached_payload,
                headers={"x-request-id": request_id, "x-cache": "HIT"},
            )
        metrics_state.cache_misses += 1
        event_log.append("cache_miss", request_id=request_id, requested_model=body.model)

    forward_result = await _forward_with_fallback(request_payload, downstream_models, metrics_state, request_id)
    if response_cache is not None:
        response_cache.set(token, request_payload, forward_result.payload)

    metrics_state.successful_requests += 1
    event_log.append(
        "request_success",
        request_id=request_id,
        requested_model=body.model,
        upstream_model=forward_result.upstream_model,
        fallback_used=forward_result.fallback_used,
        stream=False,
    )
    cache_status = "MISS" if response_cache is not None else "BYPASS"
    return JSONResponse(
        status_code=200,
        content=forward_result.payload,
        headers={
            "x-request-id": request_id,
            "x-cache": cache_status,
            "x-upstream-model": forward_result.upstream_model,
            "x-fallback-used": str(forward_result.fallback_used).lower(),
        },
    )


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
