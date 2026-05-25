from __future__ import annotations

import json
from collections.abc import AsyncIterator

import anyio
import httpx
import pytest
from inference_service.config import InferenceServiceConfig
from inference_service.engines import (
    EngineError,
    GenerationRequest,
    GenerationResult,
    OpenAICompatibleEngine,
    StreamEvent,
    create_engine,
    estimate_messages_token_count,
    estimate_token_count,
)
from inference_service.server import set_engine


class RecordingEngine:
    name = "recording"

    def __init__(self) -> None:
        self.requests: list[GenerationRequest] = []

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.requests.append(request)
        return GenerationResult(
            content=f"recorded max_tokens={request.max_tokens}",
            prompt_tokens=2,
            completion_tokens=3,
        )

    async def stream(self, request: GenerationRequest) -> AsyncIterator[StreamEvent]:
        self.requests.append(request)
        yield StreamEvent(delta={"role": "assistant"})
        yield StreamEvent(delta={"content": f"streamed temperature={request.temperature}"})
        yield StreamEvent(finish_reason="stop")


class FailingEngine:
    name = "failing"

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        raise EngineError("upstream unavailable", status_code=502)

    def stream(self, request: GenerationRequest) -> AsyncIterator[StreamEvent]:
        async def _events() -> AsyncIterator[StreamEvent]:
            if request.prompt:
                raise EngineError("upstream unavailable", status_code=502)
            yield StreamEvent()

        return _events()


def test_health(client) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "healthy"
    assert payload["engine"] == "mock"


def test_list_models(client) -> None:
    response = client.get("/v1/models")
    assert response.status_code == 200
    payload = response.json()
    assert payload["object"] == "list"
    assert payload["data"][0]["id"] == "Qwen/Qwen2.5-0.5B-Instruct"
    assert payload["data"][0]["metadata"]["engine"] == "mock"


def test_metrics(client) -> None:
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "vllm_num_requests_running" in response.text


def test_metrics_reflect_completed_request(client) -> None:
    messages = [{"role": "user", "content": "Hi"}]
    client.post(
        "/v1/chat/completions",
        json={
            "model": "Qwen/Qwen2.5-0.5B-Instruct",
            "messages": messages,
        },
    )
    response = client.get("/metrics")
    expected_prompt = estimate_messages_token_count(messages)
    expected_completion = estimate_token_count("[mock] inference-service received: Hi")
    assert response.status_code == 200
    assert "vllm_num_requests_total 1" in response.text
    assert "vllm_num_requests_successful_total 1" in response.text
    assert f"vllm_prompt_tokens_total {expected_prompt}" in response.text
    assert f"vllm_completion_tokens_total {expected_completion}" in response.text


def test_events_reflect_completed_request(client) -> None:
    response = client.post(
        "/v1/chat/completions",
        headers={"X-Request-ID": "req_inference_events_1"},
        json={
            "model": "Qwen/Qwen2.5-0.5B-Instruct",
            "messages": [{"role": "user", "content": "Hi events"}],
        },
    )
    assert response.status_code == 200

    events = client.get("/events").json()["events"]
    assert events[-1]["event_type"] == "request_success"
    assert events[-1]["request_id"] == "req_inference_events_1"
    assert events[-1]["engine"] == "mock"
    assert events[-1]["prompt_tokens"] > 0
    limited_events = client.get("/events?limit=1").json()["events"]
    assert len(limited_events) == 1
    assert limited_events[0]["event_type"] == "request_success"
    filtered_events = client.get("/events?event_type=request_success&request_id=req_inference_events_1").json()[
        "events"
    ]
    assert len(filtered_events) == 1
    assert filtered_events[0]["requested_model"] == "Qwen/Qwen2.5-0.5B-Instruct"
    assert client.get("/events?requested_model=missing-model").json()["events"] == []
    event_summary = client.get(
        "/events/summary?event_type=request_success&requested_model=Qwen/Qwen2.5-0.5B-Instruct"
    ).json()["summary"]
    assert event_summary["event_count"] == 1
    assert event_summary["request_count"] == 1
    assert event_summary["event_type_counts"] == {"request_success": 1}
    assert event_summary["requested_model_counts"] == {"Qwen/Qwen2.5-0.5B-Instruct": 1}
    assert event_summary["engine_counts"] == {"mock": 1}
    assert event_summary["latest_event"]["request_id"] == "req_inference_events_1"
    timeline = client.get("/events/requests/req_inference_events_1").json()["timeline"]
    assert timeline["request_id"] == "req_inference_events_1"
    assert timeline["event_count"] >= 2
    assert timeline["terminal_event_type"] == "request_success"
    assert timeline["duration_seconds"] >= 0
    assert timeline["requested_models"] == ["Qwen/Qwen2.5-0.5B-Instruct"]
    assert timeline["engines"] == ["mock"]
    assert "request_received" in timeline["event_types"]
    request_index = client.get("/events/requests?requested_model=Qwen/Qwen2.5-0.5B-Instruct").json()["request_index"]
    assert request_index["request_count"] >= 1
    assert request_index["requested_model_filter"] == "Qwen/Qwen2.5-0.5B-Instruct"
    assert request_index["requests"][0]["terminal_event_type"] == "request_success"
    assert "events" not in request_index["requests"][0]


def test_chat_completion_success(client) -> None:
    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "Qwen/Qwen2.5-0.5B-Instruct",
            "messages": [{"role": "user", "content": "Hi"}],
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["object"] == "chat.completion"
    assert payload["choices"][0]["message"]["role"] == "assistant"
    assert response.headers["x-request-id"].startswith("req_")


def test_mock_engine_estimates_usage_from_messages_and_completion(client) -> None:
    messages = [
        {"role": "system", "content": "Answer briefly."},
        {"role": "user", "content": "What is TTFT?"},
    ]
    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "Qwen/Qwen2.5-0.5B-Instruct",
            "messages": messages,
            "max_tokens": 4,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["usage"]["prompt_tokens"] == estimate_messages_token_count(messages)
    assert payload["usage"]["completion_tokens"] == 4
    assert payload["usage"]["total_tokens"] == payload["usage"]["prompt_tokens"] + 4


def test_chat_completion_uses_configured_engine(client) -> None:
    engine = RecordingEngine()
    set_engine(engine)
    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "Qwen/Qwen2.5-0.5B-Instruct",
            "messages": [{"role": "user", "content": "Hi"}],
            "max_tokens": 12,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["choices"][0]["message"]["content"] == "recorded max_tokens=12"
    assert payload["usage"] == {"prompt_tokens": 2, "completion_tokens": 3, "total_tokens": 5}
    assert engine.requests[0].prompt == "Hi"


def test_create_engine_builds_openai_compatible_engine() -> None:
    cfg = InferenceServiceConfig()
    cfg.engine.type = "openai-compatible"
    cfg.engine.base_url = "http://upstream.example/v1"
    cfg.engine.api_key = "sk-upstream"
    engine = create_engine(cfg)
    assert isinstance(engine, OpenAICompatibleEngine)
    assert engine.name == "openai-compatible"


async def _fake_openai_handler(request: httpx.Request) -> httpx.Response:
    payload = json.loads(request.content)
    assert request.headers["authorization"] == "Bearer sk-upstream"
    assert payload["model"] == "Qwen/Qwen2.5-0.5B-Instruct"
    if payload.get("stream"):
        return httpx.Response(
            200,
            content=(
                'data: {"choices":[{"delta":{"role":"assistant"},"finish_reason":null}]}\n\n'
                'data: {"choices":[{"delta":{"content":"stream upstream ok"},"finish_reason":null}]}\n\n'
                'data: {"choices":[{"delta":{},"finish_reason":"stop"}]}\n\n'
                "data: [DONE]\n\n"
            ),
        )
    return httpx.Response(
        200,
        json={
            "choices": [
                {
                    "message": {"role": "assistant", "content": "upstream ok"},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 4, "completion_tokens": 5, "total_tokens": 9},
        },
    )


def test_openai_compatible_engine_generate(monkeypatch) -> None:
    transport = httpx.MockTransport(_fake_openai_handler)
    original_async_client = httpx.AsyncClient
    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda *args, **kwargs: original_async_client(transport=transport),
    )
    engine = OpenAICompatibleEngine(
        base_url="http://upstream.example/v1",
        api_key="sk-upstream",
    )

    result = anyio.run(
        engine.generate,
        GenerationRequest(
            model="Qwen/Qwen2.5-0.5B-Instruct",
            prompt="Hi",
            messages=[{"role": "user", "content": "Hi"}],
            temperature=0.7,
            max_tokens=16,
        ),
    )

    assert result.content == "upstream ok"
    assert result.total_tokens == 9


def test_openai_compatible_engine_stream(monkeypatch) -> None:
    transport = httpx.MockTransport(_fake_openai_handler)
    original_async_client = httpx.AsyncClient
    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda *args, **kwargs: original_async_client(transport=transport),
    )
    engine = OpenAICompatibleEngine(
        base_url="http://upstream.example/v1",
        api_key="sk-upstream",
    )

    async def _collect_events() -> list[StreamEvent]:
        events = []
        async for event in engine.stream(
            GenerationRequest(
                model="Qwen/Qwen2.5-0.5B-Instruct",
                prompt="Hi",
                messages=[{"role": "user", "content": "Hi"}],
                temperature=0.7,
                max_tokens=16,
            )
        ):
            events.append(event)
        return events

    events = anyio.run(_collect_events)

    assert events[0].delta == {"role": "assistant"}
    assert events[1].delta == {"content": "stream upstream ok"}
    assert events[2].finish_reason == "stop"


def test_openai_compatible_engine_maps_upstream_http_errors(monkeypatch) -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(500, json={"error": "boom"}))
    original_async_client = httpx.AsyncClient
    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda *args, **kwargs: original_async_client(transport=transport),
    )
    engine = OpenAICompatibleEngine(base_url="http://upstream.example/v1")

    with pytest.raises(EngineError, match="Upstream engine returned HTTP 500") as exc_info:
        anyio.run(
            engine.generate,
            GenerationRequest(
                model="Qwen/Qwen2.5-0.5B-Instruct",
                prompt="Hi",
                messages=[{"role": "user", "content": "Hi"}],
                temperature=0.7,
                max_tokens=16,
            ),
        )

    assert exc_info.value.status_code == 502


def test_chat_completion_engine_error_returns_502(client) -> None:
    set_engine(FailingEngine())
    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "Qwen/Qwen2.5-0.5B-Instruct",
            "messages": [{"role": "user", "content": "Hi"}],
        },
    )
    assert response.status_code == 502
    assert response.json()["error"] == {
        "message": "upstream unavailable",
        "type": "bad_gateway_error",
        "code": "502",
    }


def test_chat_completion_preserves_request_id_header(client) -> None:
    response = client.post(
        "/v1/chat/completions",
        headers={"X-Request-ID": "req_demo_123"},
        json={
            "model": "Qwen/Qwen2.5-0.5B-Instruct",
            "messages": [{"role": "user", "content": "Hi"}],
        },
    )
    assert response.status_code == 200
    assert response.headers["x-request-id"] == "req_demo_123"


def test_chat_completion_stream_success(client) -> None:
    with client.stream(
        "POST",
        "/v1/chat/completions",
        headers={"X-Request-ID": "req_stream_456"},
        json={
            "model": "Qwen/Qwen2.5-0.5B-Instruct",
            "messages": [{"role": "user", "content": "Hi"}],
            "stream": True,
        },
    ) as response:
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/event-stream")
        assert response.headers["x-request-id"] == "req_stream_456"
        body = "".join(response.iter_text())

    assert '"object": "chat.completion.chunk"' in body
    assert "[mock] inference-service received: Hi" in body
    assert "data: [DONE]" in body


def test_streaming_uses_configured_engine(client) -> None:
    engine = RecordingEngine()
    set_engine(engine)
    with client.stream(
        "POST",
        "/v1/chat/completions",
        json={
            "model": "Qwen/Qwen2.5-0.5B-Instruct",
            "messages": [{"role": "user", "content": "Hi"}],
            "temperature": 0.2,
            "stream": True,
        },
    ) as response:
        assert response.status_code == 200
        body = "".join(response.iter_text())

    assert "streamed temperature=0.2" in body
    assert engine.requests[0].temperature == 0.2


def test_chat_completion_stream_engine_error_emits_error_event(client) -> None:
    set_engine(FailingEngine())
    with client.stream(
        "POST",
        "/v1/chat/completions",
        json={
            "model": "Qwen/Qwen2.5-0.5B-Instruct",
            "messages": [{"role": "user", "content": "Hi"}],
            "stream": True,
        },
    ) as response:
        assert response.status_code == 200
        body = "".join(response.iter_text())

    assert '"error":' in body
    assert "upstream unavailable" in body
    assert "data: [DONE]" in body
    metrics = client.get("/metrics")
    assert "vllm_num_requests_failed_total 1" in metrics.text
    assert "vllm_num_requests_running 0" in metrics.text


def test_metrics_reflect_streaming_request(client) -> None:
    messages = [{"role": "user", "content": "Hi"}]
    with client.stream(
        "POST",
        "/v1/chat/completions",
        json={
            "model": "Qwen/Qwen2.5-0.5B-Instruct",
            "messages": messages,
            "stream": True,
        },
    ) as response:
        assert response.status_code == 200
        _ = "".join(response.iter_text())

    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    assert "vllm_num_requests_total 1" in metrics.text
    assert "vllm_num_requests_successful_total 1" in metrics.text
    assert "vllm_num_requests_running 0" in metrics.text
    assert f"vllm_prompt_tokens_total {estimate_messages_token_count(messages)}" in metrics.text


def test_chat_completion_unknown_model(client) -> None:
    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "unknown-model",
            "messages": [{"role": "user", "content": "Hi"}],
        },
    )
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "404"


def test_chat_completion_empty_messages_returns_422(client) -> None:
    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "Qwen/Qwen2.5-0.5B-Instruct",
            "messages": [],
        },
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "422"
