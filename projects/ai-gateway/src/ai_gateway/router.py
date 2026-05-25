from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any
from urllib.parse import urlsplit, urlunsplit

import httpx
from fastapi import HTTPException


def route_model(model_name: str, models: list[Any]) -> Any | None:
    for model in models:
        if model.name == model_name:
            return model
    return None


def route_model_candidates(model_name: str, models: list[Any]) -> list[Any]:
    primary = route_model(model_name, models)
    if primary is None:
        return []

    by_name = {model.name: model for model in models}
    candidates = [primary]
    seen = {primary.name}
    for fallback_name in getattr(primary, "fallbacks", []):
        fallback = by_name.get(fallback_name)
        if fallback is not None and fallback.name not in seen:
            candidates.append(fallback)
            seen.add(fallback.name)
    return candidates


def _build_health_url(base_url: str) -> str:
    parsed = urlsplit(base_url.rstrip("/"))
    path = parsed.path
    if path.endswith("/v1"):
        path = path[:-3]
    if not path:
        path = ""
    return urlunsplit((parsed.scheme, parsed.netloc, f"{path}/health", "", ""))


async def probe_upstream_health(base_url: str) -> str:
    target = _build_health_url(base_url)
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(target)
    except httpx.HTTPError:
        return "unhealthy"

    if response.status_code >= 400:
        return "unhealthy"

    try:
        payload = response.json()
    except ValueError:
        return "healthy"

    status = payload.get("status") if isinstance(payload, dict) else None
    if status in {"healthy", "ok"}:
        return "healthy"
    if status:
        return str(status)
    return "healthy"


def _build_downstream_headers(downstream_model: Any, request_id: str) -> dict[str, str]:
    headers = {"x-request-id": request_id}
    api_key = getattr(downstream_model, "api_key", "")
    if api_key:
        headers["authorization"] = f"Bearer {api_key}"
    return headers


async def forward_chat_request(
    body: dict[str, Any],
    downstream_model: Any,
    request_id: str,
) -> dict[str, Any]:
    target = f"{downstream_model.base_url.rstrip('/')}/chat/completions"
    payload = dict(body)
    payload["model"] = downstream_model.target_model or payload["model"]
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                target,
                json=payload,
                headers=_build_downstream_headers(downstream_model, request_id),
            )
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail={
                "message": f"Downstream request failed: {exc}",
                "type": "bad_gateway_error",
                "code": "502",
            },
        ) from exc

    try:
        payload = response.json()
    except ValueError as exc:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "Downstream returned non-JSON response",
                "type": "bad_gateway_error",
                "code": "502",
            },
        ) from exc

    if response.status_code >= 400:
        detail = (
            payload.get("error")
            or payload.get("detail")
            or {
                "message": "Downstream error",
                "type": "bad_gateway_error",
                "code": str(response.status_code),
            }
        )
        raise HTTPException(status_code=response.status_code, detail=detail)

    return payload


async def forward_chat_stream(
    body: dict[str, Any],
    downstream_model: Any,
    request_id: str,
) -> AsyncIterator[str]:
    target = f"{downstream_model.base_url.rstrip('/')}/chat/completions"
    payload = dict(body)
    payload["model"] = downstream_model.target_model or payload["model"]
    try:
        async with (
            httpx.AsyncClient(timeout=30.0) as client,
            client.stream(
                "POST",
                target,
                json=payload,
                headers=_build_downstream_headers(downstream_model, request_id),
            ) as response,
        ):
            if response.status_code >= 400:
                try:
                    error_payload = await response.aread()
                    parsed = httpx.Response(
                        status_code=response.status_code,
                        content=error_payload,
                    ).json()
                except ValueError:
                    parsed = None
                detail = (parsed or {}).get("error") if isinstance(parsed, dict) else None
                if detail is None:
                    detail = {
                        "message": "Downstream stream request failed",
                        "type": "bad_gateway_error",
                        "code": str(response.status_code),
                    }
                raise HTTPException(status_code=response.status_code, detail=detail)

            async for chunk in response.aiter_text():
                if chunk:
                    yield chunk
    except HTTPException:
        raise
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail={
                "message": f"Downstream request failed: {exc}",
                "type": "bad_gateway_error",
                "code": "502",
            },
        ) from exc
