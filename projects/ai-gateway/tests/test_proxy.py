from __future__ import annotations

from types import SimpleNamespace

import pytest
from ai_gateway.config import AiGatewayConfig, ModelEntry, load_config
from ai_gateway.router import _build_downstream_headers, route_model_candidates
from ai_gateway.runtime import InMemoryResponseCache
from ai_gateway.server import app, set_config
from fastapi import HTTPException
from fastapi.testclient import TestClient


def _make_client() -> TestClient:
    cfg = load_config()
    cfg.auth.enabled = True
    cfg.auth.api_keys = ["sk-test-key-1"]
    cfg.rate_limit.enabled = True
    cfg.rate_limit.requests_per_minute = 2
    set_config(cfg)
    app.state.config = cfg
    return TestClient(app)


def test_health(monkeypatch) -> None:
    async def _fake_probe_upstream_health(base_url: str) -> str:
        assert base_url == "http://localhost:8000/v1"
        return "healthy"

    monkeypatch.setattr("ai_gateway.server.probe_upstream_health", _fake_probe_upstream_health)
    client = _make_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["upstream_services"]["vllm-local"] == "healthy"


def test_health_reflects_unhealthy_upstream(monkeypatch) -> None:
    async def _fake_probe_upstream_health(base_url: str) -> str:
        return "unhealthy"

    monkeypatch.setattr("ai_gateway.server.probe_upstream_health", _fake_probe_upstream_health)
    client = _make_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "degraded"
    assert response.json()["upstream_services"]["vllm-local"] == "unhealthy"


def test_list_models_includes_gateway_metadata_without_api_keys(monkeypatch) -> None:
    async def _fake_probe_upstream_health(base_url: str) -> str:
        return "healthy"

    cfg = load_config()
    cfg.auth.enabled = True
    cfg.auth.api_keys = ["sk-test-key-1"]
    cfg.models = [
        ModelEntry(
            name="vllm-local",
            base_url="http://primary.example/v1",
            api_key="sk-secret",
            target_model="primary-model",
            fallbacks=["vllm-backup"],
        ),
        ModelEntry(name="vllm-backup", base_url="http://backup.example/v1", target_model="backup-model"),
    ]
    set_config(cfg)
    app.state.config = cfg
    monkeypatch.setattr("ai_gateway.server.probe_upstream_health", _fake_probe_upstream_health)

    response = TestClient(app).get("/v1/models")

    assert response.status_code == 200
    payload = response.json()
    assert payload["object"] == "list"
    assert payload["data"][0]["id"] == "vllm-local"
    assert payload["data"][0]["metadata"]["target_model"] == "primary-model"
    assert payload["data"][0]["metadata"]["fallbacks"] == ["vllm-backup"]
    assert payload["data"][0]["metadata"]["fallback_count"] == 1
    assert payload["data"][0]["metadata"]["upstream_health"] == "healthy"
    assert "sk-secret" not in response.text


def test_config_rejects_duplicate_model_names() -> None:
    with pytest.raises(ValueError, match="Duplicate gateway model names"):
        AiGatewayConfig(
            models=[
                ModelEntry(name="duplicate", base_url="http://localhost:8000/v1"),
                ModelEntry(name="duplicate", base_url="http://localhost:8001/v1"),
            ]
        )


def test_route_model_candidates_include_configured_fallbacks() -> None:
    models = [
        ModelEntry(
            name="primary",
            base_url="http://localhost:8000/v1",
            fallbacks=["backup", "missing"],
        ),
        ModelEntry(name="backup", base_url="http://localhost:8001/v1"),
    ]

    candidates = route_model_candidates("primary", models)

    assert [candidate.name for candidate in candidates] == ["primary", "backup"]


def test_default_models_config_includes_learning_fallback() -> None:
    cfg = load_config()
    candidates = route_model_candidates("vllm-local", cfg.models)

    assert [candidate.name for candidate in candidates] == ["vllm-local", "vllm-backup"]


def test_metrics() -> None:
    client = _make_client()
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "ai_gateway_requests_total" in response.text
    assert "ai_gateway_rate_limited_requests_total" in response.text
    assert "ai_gateway_fallback_attempts_total" in response.text
    assert "ai_gateway_fallback_successes_total" in response.text


def test_missing_auth_returns_401() -> None:
    client = _make_client()
    response = client.post(
        "/v1/chat/completions",
        json={"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]},
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "401"


def test_invalid_auth_format_returns_401() -> None:
    client = _make_client()
    response = client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Token sk-test-key-1"},
        json={"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]},
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "401"


def test_unknown_model_returns_404() -> None:
    client = _make_client()
    response = client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer sk-test-key-1"},
        json={"model": "unknown-model", "messages": [{"role": "user", "content": "Hi"}]},
    )
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "404"


def test_stream_proxy_success(monkeypatch) -> None:
    async def _fake_forward_chat_stream(body, downstream_model, request_id):
        assert body["stream"] is True
        assert downstream_model.target_model == "Qwen/Qwen2.5-0.5B-Instruct"
        assert request_id == "req_gateway_stream_1"
        yield 'data: {"object":"chat.completion.chunk","choices":[{"delta":{"role":"assistant"}}]}\n\n'
        yield 'data: {"object":"chat.completion.chunk","choices":[{"delta":{"content":"proxy stream ok"}}]}\n\n'
        yield "data: [DONE]\n\n"

    client = _make_client()
    monkeypatch.setattr("ai_gateway.server.forward_chat_stream", _fake_forward_chat_stream)
    with client.stream(
        "POST",
        "/v1/chat/completions",
        headers={
            "Authorization": "Bearer sk-test-key-1",
            "X-Request-ID": "req_gateway_stream_1",
        },
        json={
            "model": "vllm-local",
            "messages": [{"role": "user", "content": "Hi"}],
            "stream": True,
        },
    ) as response:
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/event-stream")
        assert response.headers["x-request-id"] == "req_gateway_stream_1"
        body = "".join(response.iter_text())

    assert "chat.completion.chunk" in body
    assert "proxy stream ok" in body
    assert "data: [DONE]" in body


def test_stream_proxy_updates_success_metrics(monkeypatch) -> None:
    async def _fake_forward_chat_stream(body, downstream_model, request_id):
        yield 'data: {"object":"chat.completion.chunk","choices":[{"delta":{"content":"proxy stream ok"}}]}\n\n'
        yield "data: [DONE]\n\n"

    client = _make_client()
    monkeypatch.setattr("ai_gateway.server.forward_chat_stream", _fake_forward_chat_stream)
    with client.stream(
        "POST",
        "/v1/chat/completions",
        headers={"Authorization": "Bearer sk-test-key-1"},
        json={
            "model": "vllm-local",
            "messages": [{"role": "user", "content": "Hi"}],
            "stream": True,
        },
    ) as response:
        assert response.status_code == 200
        _ = "".join(response.iter_text())

    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    assert "ai_gateway_successful_requests_total 1" in metrics.text


def test_stream_proxy_falls_back_before_first_chunk(monkeypatch) -> None:
    calls = []

    async def _fake_forward_chat_stream(body, downstream_model, request_id):
        calls.append(downstream_model.name)
        if downstream_model.name == "vllm-local":
            raise HTTPException(
                status_code=502,
                detail={
                    "message": "primary stream failed",
                    "type": "bad_gateway_error",
                    "code": "502",
                },
            )
        yield 'data: {"object":"chat.completion.chunk","choices":[{"delta":{"content":"backup stream ok"}}]}\n\n'
        yield "data: [DONE]\n\n"

    cfg = load_config()
    cfg.auth.enabled = True
    cfg.auth.api_keys = ["sk-test-key-1"]
    cfg.rate_limit.enabled = False
    cfg.models = [
        ModelEntry(
            name="vllm-local",
            base_url="http://primary.example/v1",
            target_model="primary-model",
            fallbacks=["vllm-backup"],
        ),
        ModelEntry(
            name="vllm-backup",
            base_url="http://backup.example/v1",
            target_model="backup-model",
        ),
    ]
    set_config(cfg)
    app.state.config = cfg
    monkeypatch.setattr("ai_gateway.server.forward_chat_stream", _fake_forward_chat_stream)

    client = TestClient(app)
    with client.stream(
        "POST",
        "/v1/chat/completions",
        headers={"Authorization": "Bearer sk-test-key-1"},
        json={
            "model": "vllm-local",
            "messages": [{"role": "user", "content": "Hi stream fallback"}],
            "stream": True,
        },
    ) as response:
        assert response.status_code == 200
        body = "".join(response.iter_text())

    assert calls == ["vllm-local", "vllm-backup"]
    assert "backup stream ok" in body
    assert "data: [DONE]" in body
    metrics = client.get("/metrics")
    assert "ai_gateway_upstream_failures_total 1" in metrics.text
    assert "ai_gateway_successful_requests_total 1" in metrics.text


def test_stream_proxy_emits_error_when_all_candidates_fail(monkeypatch) -> None:
    calls = []

    async def _fake_forward_chat_stream(body, downstream_model, request_id):
        calls.append(downstream_model.name)
        raise HTTPException(
            status_code=502,
            detail={
                "message": f"{downstream_model.name} stream failed",
                "type": "bad_gateway_error",
                "code": "502",
            },
        )
        yield "data: unreachable\n\n"

    cfg = load_config()
    cfg.auth.enabled = True
    cfg.auth.api_keys = ["sk-test-key-1"]
    cfg.rate_limit.enabled = False
    cfg.models = [
        ModelEntry(
            name="vllm-local",
            base_url="http://primary.example/v1",
            target_model="primary-model",
            fallbacks=["vllm-backup"],
        ),
        ModelEntry(
            name="vllm-backup",
            base_url="http://backup.example/v1",
            target_model="backup-model",
        ),
    ]
    set_config(cfg)
    app.state.config = cfg
    monkeypatch.setattr("ai_gateway.server.forward_chat_stream", _fake_forward_chat_stream)

    client = TestClient(app)
    with client.stream(
        "POST",
        "/v1/chat/completions",
        headers={"Authorization": "Bearer sk-test-key-1"},
        json={
            "model": "vllm-local",
            "messages": [{"role": "user", "content": "Hi all fail"}],
            "stream": True,
        },
    ) as response:
        assert response.status_code == 200
        body = "".join(response.iter_text())

    assert calls == ["vllm-local", "vllm-backup"]
    assert '"error":' in body
    assert "vllm-backup stream failed" in body
    assert "data: [DONE]" in body
    metrics = client.get("/metrics")
    assert "ai_gateway_upstream_failures_total 2" in metrics.text
    assert "ai_gateway_successful_requests_total 0" in metrics.text


def test_stream_proxy_emits_error_without_fallback_after_first_chunk(monkeypatch) -> None:
    calls = []

    async def _fake_forward_chat_stream(body, downstream_model, request_id):
        calls.append(downstream_model.name)
        yield 'data: {"object":"chat.completion.chunk","choices":[{"delta":{"content":"partial"}}]}\n\n'
        raise HTTPException(
            status_code=502,
            detail={
                "message": "primary failed mid-stream",
                "type": "bad_gateway_error",
                "code": "502",
            },
        )

    cfg = load_config()
    cfg.auth.enabled = True
    cfg.auth.api_keys = ["sk-test-key-1"]
    cfg.rate_limit.enabled = False
    cfg.models = [
        ModelEntry(
            name="vllm-local",
            base_url="http://primary.example/v1",
            target_model="primary-model",
            fallbacks=["vllm-backup"],
        ),
        ModelEntry(
            name="vllm-backup",
            base_url="http://backup.example/v1",
            target_model="backup-model",
        ),
    ]
    set_config(cfg)
    app.state.config = cfg
    monkeypatch.setattr("ai_gateway.server.forward_chat_stream", _fake_forward_chat_stream)

    client = TestClient(app)
    with client.stream(
        "POST",
        "/v1/chat/completions",
        headers={"Authorization": "Bearer sk-test-key-1"},
        json={
            "model": "vllm-local",
            "messages": [{"role": "user", "content": "Hi mid stream fail"}],
            "stream": True,
        },
    ) as response:
        assert response.status_code == 200
        body = "".join(response.iter_text())

    assert calls == ["vllm-local"]
    assert "partial" in body
    assert '"error":' in body
    assert "primary failed mid-stream" in body
    assert "data: [DONE]" in body
    metrics = client.get("/metrics")
    assert "ai_gateway_upstream_failures_total 1" in metrics.text
    assert "ai_gateway_successful_requests_total 0" in metrics.text


def test_proxy_success(monkeypatch) -> None:
    async def _fake_forward_chat_request(body, downstream_model, request_id):
        assert request_id == "req_gateway_json_1"
        return {
            "id": "chatcmpl-proxy-test",
            "object": "chat.completion",
            "model": downstream_model.target_model or body["model"],
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "proxy ok"},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
        }

    monkeypatch.setattr("ai_gateway.server.forward_chat_request", _fake_forward_chat_request)
    client = _make_client()
    response = client.post(
        "/v1/chat/completions",
        headers={
            "Authorization": "Bearer sk-test-key-1",
            "X-Request-ID": "req_gateway_json_1",
        },
        json={"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]},
    )
    assert response.status_code == 200
    assert response.json()["choices"][0]["message"]["content"] == "proxy ok"
    assert response.headers["x-request-id"] == "req_gateway_json_1"
    assert response.headers["x-cache"] == "BYPASS"
    assert response.headers["x-upstream-model"] == "vllm-local"
    assert response.headers["x-fallback-used"] == "false"
    events = client.get("/events").json()["events"]
    assert events[-1]["event_type"] == "request_success"
    assert events[-1]["request_id"] == "req_gateway_json_1"
    assert events[-1]["upstream_model"] == "vllm-local"
    limited_events = client.get("/events?limit=1").json()["events"]
    assert len(limited_events) == 1
    assert limited_events[0]["event_type"] == "request_success"
    filtered_events = client.get(
        "/events?event_type=request_success&request_id=req_gateway_json_1&upstream_model=vllm-local"
    ).json()["events"]
    assert len(filtered_events) == 1
    assert filtered_events[0]["requested_model"] == "vllm-local"
    assert client.get("/events?request_id=missing-request").json()["events"] == []
    event_summary = client.get(
        "/events/summary?event_type=request_success&request_id=req_gateway_json_1&upstream_model=vllm-local"
    ).json()["summary"]
    assert event_summary["event_count"] == 1
    assert event_summary["request_count"] == 1
    assert event_summary["event_type_counts"] == {"request_success": 1}
    assert event_summary["requested_model_counts"] == {"vllm-local": 1}
    assert event_summary["upstream_model_counts"] == {"vllm-local": 1}
    assert event_summary["latest_event"]["request_id"] == "req_gateway_json_1"
    timeline = client.get("/events/requests/req_gateway_json_1").json()["timeline"]
    assert timeline["request_id"] == "req_gateway_json_1"
    assert timeline["event_count"] >= 2
    assert timeline["terminal_event_type"] == "request_success"
    assert timeline["duration_seconds"] >= 0
    assert timeline["requested_models"] == ["vllm-local"]
    assert timeline["upstream_models"] == ["vllm-local"]
    assert "upstream_attempt" in timeline["event_types"]
    request_index = client.get("/events/requests?requested_model=vllm-local&upstream_model=vllm-local").json()[
        "request_index"
    ]
    assert request_index["request_count"] >= 1
    assert request_index["requested_model_filter"] == "vllm-local"
    assert request_index["upstream_model_filter"] == "vllm-local"
    assert request_index["requests"][0]["terminal_event_type"] == "request_success"
    assert "events" not in request_index["requests"][0]


def test_proxy_generates_request_id_when_missing(monkeypatch) -> None:
    async def _fake_forward_chat_request(body, downstream_model, request_id):
        assert request_id.startswith("req_")
        return {
            "id": "chatcmpl-proxy-test",
            "object": "chat.completion",
            "model": downstream_model.target_model or body["model"],
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "proxy ok"},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
        }

    monkeypatch.setattr("ai_gateway.server.forward_chat_request", _fake_forward_chat_request)
    client = _make_client()
    response = client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer sk-test-key-1"},
        json={"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]},
    )
    assert response.status_code == 200
    assert response.headers["x-request-id"].startswith("req_")


def test_proxy_falls_back_on_upstream_5xx(monkeypatch) -> None:
    calls = []

    async def _fake_forward_chat_request(body, downstream_model, request_id):
        calls.append(downstream_model.name)
        if downstream_model.name == "vllm-local":
            raise HTTPException(
                status_code=502,
                detail={
                    "message": "primary failed",
                    "type": "bad_gateway_error",
                    "code": "502",
                },
            )
        return {
            "id": "chatcmpl-fallback-test",
            "object": "chat.completion",
            "model": downstream_model.target_model or body["model"],
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "fallback ok"},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
        }

    cfg = load_config()
    cfg.auth.enabled = True
    cfg.auth.api_keys = ["sk-test-key-1"]
    cfg.rate_limit.enabled = False
    cfg.models = [
        ModelEntry(
            name="vllm-local",
            base_url="http://primary.example/v1",
            target_model="primary-model",
            fallbacks=["vllm-backup"],
        ),
        ModelEntry(
            name="vllm-backup",
            base_url="http://backup.example/v1",
            target_model="backup-model",
        ),
    ]
    set_config(cfg)
    app.state.config = cfg
    monkeypatch.setattr("ai_gateway.server.forward_chat_request", _fake_forward_chat_request)

    client = TestClient(app)
    response = client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer sk-test-key-1"},
        json={"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]},
    )

    assert response.status_code == 200
    assert response.json()["choices"][0]["message"]["content"] == "fallback ok"
    assert response.headers["x-upstream-model"] == "vllm-backup"
    assert response.headers["x-fallback-used"] == "true"
    assert calls == ["vllm-local", "vllm-backup"]
    metrics = client.get("/metrics")
    assert "ai_gateway_upstream_failures_total 1" in metrics.text
    assert "ai_gateway_fallback_attempts_total 1" in metrics.text
    assert "ai_gateway_fallback_successes_total 1" in metrics.text
    assert "ai_gateway_successful_requests_total 1" in metrics.text
    event_types = [event["event_type"] for event in client.get("/events").json()["events"]]
    assert "fallback_attempt" in event_types
    assert "fallback_success" in event_types


def test_proxy_cache_serves_repeated_non_stream_request(monkeypatch) -> None:
    calls = 0

    async def _fake_forward_chat_request(body, downstream_model, request_id):
        nonlocal calls
        calls += 1
        return {
            "id": f"chatcmpl-cache-{calls}",
            "object": "chat.completion",
            "model": downstream_model.target_model or body["model"],
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": f"cache response {calls}"},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
        }

    cfg = load_config()
    cfg.auth.enabled = True
    cfg.auth.api_keys = ["sk-test-key-1"]
    cfg.rate_limit.enabled = False
    cfg.cache.enabled = True
    cfg.cache.ttl_seconds = 60
    cfg.cache.max_entries = 2
    set_config(cfg)
    app.state.config = cfg
    monkeypatch.setattr("ai_gateway.server.forward_chat_request", _fake_forward_chat_request)

    client = TestClient(app)
    headers = {"Authorization": "Bearer sk-test-key-1"}
    payload = {"model": "vllm-local", "messages": [{"role": "user", "content": "Hi cache"}]}

    first = client.post("/v1/chat/completions", headers=headers, json=payload)
    second = client.post("/v1/chat/completions", headers=headers, json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.headers["x-cache"] == "MISS"
    assert second.headers["x-cache"] == "HIT"
    assert first.json()["choices"][0]["message"]["content"] == "cache response 1"
    assert second.json()["choices"][0]["message"]["content"] == "cache response 1"
    assert calls == 1
    metrics = client.get("/metrics")
    assert "ai_gateway_cache_hits_total 1" in metrics.text
    assert "ai_gateway_cache_misses_total 1" in metrics.text


def test_response_cache_expires_entries(monkeypatch) -> None:
    clock = {"now": 100.0}
    monkeypatch.setattr("ai_gateway.runtime.time", lambda: clock["now"])
    cache = InMemoryResponseCache(ttl_seconds=1, max_entries=2)
    body = {"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}

    cache.set("sk-a", body, {"choices": [{"message": {"content": "cached"}}]})
    assert cache.get("sk-a", body)["choices"][0]["message"]["content"] == "cached"

    clock["now"] = 101.0
    assert cache.get("sk-a", body) is None


def test_response_cache_is_scoped_by_token() -> None:
    cache = InMemoryResponseCache(ttl_seconds=60, max_entries=2)
    body = {"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}

    cache.set("sk-a", body, {"id": "for-a"})

    assert cache.get("sk-a", body)["id"] == "for-a"
    assert cache.get("sk-b", body) is None


def test_response_cache_evicts_oldest_entry_when_full() -> None:
    cache = InMemoryResponseCache(ttl_seconds=60, max_entries=2)
    first = {"model": "vllm-local", "messages": [{"role": "user", "content": "one"}]}
    second = {"model": "vllm-local", "messages": [{"role": "user", "content": "two"}]}
    third = {"model": "vllm-local", "messages": [{"role": "user", "content": "three"}]}

    cache.set("sk-a", first, {"id": "first"})
    cache.set("sk-a", second, {"id": "second"})
    cache.set("sk-a", third, {"id": "third"})

    assert cache.get("sk-a", first) is None
    assert cache.get("sk-a", second)["id"] == "second"
    assert cache.get("sk-a", third)["id"] == "third"


def test_downstream_headers_include_request_id_and_optional_api_key() -> None:
    without_key = _build_downstream_headers(SimpleNamespace(api_key=""), "req_downstream_1")
    assert without_key == {"x-request-id": "req_downstream_1"}

    with_key = _build_downstream_headers(SimpleNamespace(api_key="sk-downstream"), "req_downstream_2")
    assert with_key == {
        "x-request-id": "req_downstream_2",
        "authorization": "Bearer sk-downstream",
    }


def test_proxy_auth_uses_config_fallback_without_app_state(monkeypatch) -> None:
    async def _fake_forward_chat_request(body, downstream_model, request_id):
        return {
            "id": "chatcmpl-proxy-test",
            "object": "chat.completion",
            "model": downstream_model.target_model or body["model"],
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "proxy ok"},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
        }

    cfg = load_config()
    cfg.auth.enabled = True
    cfg.auth.api_keys = ["sk-test-key-1"]
    cfg.rate_limit.enabled = False
    set_config(cfg)
    if hasattr(app.state, "config"):
        delattr(app.state, "config")

    monkeypatch.setattr("ai_gateway.server.forward_chat_request", _fake_forward_chat_request)
    client = TestClient(app)
    response = client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer sk-test-key-1"},
        json={"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]},
    )
    assert response.status_code == 200


def test_upstream_failure_returns_502(monkeypatch) -> None:
    async def _fake_forward_chat_request(body, downstream_model, request_id):
        raise HTTPException(
            status_code=502,
            detail={
                "message": "Downstream request failed: connect timeout",
                "type": "bad_gateway_error",
                "code": "502",
            },
        )

    monkeypatch.setattr("ai_gateway.server.forward_chat_request", _fake_forward_chat_request)
    client = _make_client()
    response = client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer sk-test-key-1"},
        json={"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]},
    )
    assert response.status_code == 502
    assert response.json()["error"]["code"] == "502"


def test_rate_limit_returns_429(monkeypatch) -> None:
    async def _fake_forward_chat_request(body, downstream_model, request_id):
        return {
            "id": "chatcmpl-proxy-test",
            "object": "chat.completion",
            "model": downstream_model.target_model or body["model"],
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "proxy ok"},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
        }

    monkeypatch.setattr("ai_gateway.server.forward_chat_request", _fake_forward_chat_request)
    client = _make_client()
    headers = {"Authorization": "Bearer sk-test-key-1"}
    payload = {"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}

    assert client.post("/v1/chat/completions", headers=headers, json=payload).status_code == 200
    assert client.post("/v1/chat/completions", headers=headers, json=payload).status_code == 200
    response = client.post("/v1/chat/completions", headers=headers, json=payload)

    assert response.status_code == 429
    assert response.json()["error"]["code"] == "429"


def test_metrics_reflect_error_paths(monkeypatch) -> None:
    async def _fake_forward_chat_request(body, downstream_model, request_id):
        raise HTTPException(
            status_code=502,
            detail={
                "message": "Downstream request failed: connect timeout",
                "type": "bad_gateway_error",
                "code": "502",
            },
        )

    monkeypatch.setattr("ai_gateway.server.forward_chat_request", _fake_forward_chat_request)
    client = _make_client()
    payload = {"model": "vllm-local", "messages": [{"role": "user", "content": "Hi"}]}

    client.post("/v1/chat/completions", json=payload)
    client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer sk-test-key-1"},
        json=payload,
    )
    metrics = client.get("/metrics")

    assert metrics.status_code == 200
    assert "ai_gateway_auth_failures_total 1" in metrics.text
    assert "ai_gateway_upstream_failures_total 2" in metrics.text
    failure_summary = client.get("/events/failures").json()["failure_summary"]
    assert failure_summary["failed_request_count"] == 2
    assert failure_summary["event_type_counts"]["auth_failed"] == 1
    assert failure_summary["event_type_counts"]["fallback_attempt"] == 1
    assert failure_summary["event_type_counts"]["upstream_error"] == 1
    assert failure_summary["status_code_counts"] == {"401": 1, "502": 2}
    assert failure_summary["failed_upstream_model_counts"] == {"vllm-local": 1}
    upstream_failure_summary = client.get("/events/failures?upstream_model=vllm-local").json()["failure_summary"]
    assert upstream_failure_summary["failure_event_count"] == 1
