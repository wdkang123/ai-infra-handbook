from __future__ import annotations

import json
import re
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Protocol

import httpx


@dataclass
class GenerationRequest:
    model: str
    prompt: str
    messages: list[dict[str, str]]
    temperature: float
    max_tokens: int


@dataclass
class GenerationResult:
    content: str
    prompt_tokens: int
    completion_tokens: int
    finish_reason: str = "stop"

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


@dataclass
class StreamEvent:
    delta: dict[str, str] | None = None
    finish_reason: str | None = None


class EngineError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        status_code: int = 502,
        error_type: str = "bad_gateway_error",
        code: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_type = error_type
        self.code = code or str(status_code)


class InferenceEngine(Protocol):
    name: str

    async def generate(self, request: GenerationRequest) -> GenerationResult: ...

    async def stream(self, request: GenerationRequest) -> AsyncIterator[StreamEvent]: ...


def estimate_token_count(text: str) -> int:
    """Approximate token count for the learning mock without pulling in a tokenizer."""
    if not text:
        return 0
    pieces = re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE)
    return max(1, len(pieces))


def estimate_messages_token_count(messages: list[dict[str, str]]) -> int:
    total = 0
    for message in messages:
        content = message.get("content", "")
        role = message.get("role", "")
        role_overhead = 1 if role else 0
        total += role_overhead + estimate_token_count(content)
    return total


class MockInferenceEngine:
    def __init__(self, name: str = "mock") -> None:
        self.name = name

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        content = f"[mock] inference-service received: {request.prompt}"
        return GenerationResult(
            content=content,
            prompt_tokens=estimate_messages_token_count(request.messages),
            completion_tokens=min(request.max_tokens, estimate_token_count(content)),
        )

    async def stream(self, request: GenerationRequest) -> AsyncIterator[StreamEvent]:
        result = await self.generate(request)
        yield StreamEvent(delta={"role": "assistant"})
        yield StreamEvent(delta={"content": result.content})
        yield StreamEvent(finish_reason=result.finish_reason)


class OpenAICompatibleEngine:
    def __init__(
        self,
        *,
        base_url: str,
        api_key: str = "",
        timeout: float = 30.0,
        name: str = "openai-compatible",
    ) -> None:
        if not base_url:
            raise ValueError("OpenAI-compatible engine requires engine.base_url")
        self.name = name
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        payload = self._build_payload(request, stream=False)
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self._chat_completions_url(),
                    json=payload,
                    headers=self._headers(),
                )
            response.raise_for_status()
            data = response.json()
            choice = data["choices"][0]
            message = choice.get("message") or {}
            usage = data.get("usage") or {}
            return GenerationResult(
                content=message.get("content", ""),
                prompt_tokens=int(usage.get("prompt_tokens", 0)),
                completion_tokens=int(usage.get("completion_tokens", 0)),
                finish_reason=choice.get("finish_reason") or "stop",
            )
        except httpx.HTTPStatusError as exc:
            raise self._status_error(exc) from exc
        except httpx.HTTPError as exc:
            raise EngineError(f"Upstream engine request failed: {exc}") from exc
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise EngineError(f"Upstream engine returned malformed response: {exc}") from exc

    async def stream(self, request: GenerationRequest) -> AsyncIterator[StreamEvent]:
        payload = self._build_payload(request, stream=True)
        try:
            async with (
                httpx.AsyncClient(timeout=self.timeout) as client,
                client.stream(
                    "POST",
                    self._chat_completions_url(),
                    json=payload,
                    headers=self._headers(),
                ) as response,
            ):
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line.startswith("data:"):
                        continue
                    raw = line.removeprefix("data:").strip()
                    if not raw or raw == "[DONE]":
                        continue
                    chunk = json.loads(raw)
                    choice = chunk["choices"][0]
                    yield StreamEvent(
                        delta=choice.get("delta") or {},
                        finish_reason=choice.get("finish_reason"),
                    )
        except httpx.HTTPStatusError as exc:
            raise self._status_error(exc) from exc
        except httpx.HTTPError as exc:
            raise EngineError(f"Upstream engine stream failed: {exc}") from exc
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise EngineError(
                f"Upstream engine returned malformed stream response: {exc}",
            ) from exc

    def _build_payload(self, request: GenerationRequest, *, stream: bool) -> dict:
        return {
            "model": request.model,
            "messages": request.messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": stream,
        }

    def _headers(self) -> dict[str, str]:
        headers = {"content-type": "application/json"}
        if self.api_key:
            headers["authorization"] = f"Bearer {self.api_key}"
        return headers

    def _chat_completions_url(self) -> str:
        return f"{self.base_url}/chat/completions"

    def _status_error(self, exc: httpx.HTTPStatusError) -> EngineError:
        status_code = exc.response.status_code
        return EngineError(
            f"Upstream engine returned HTTP {status_code}",
            status_code=502,
            error_type="bad_gateway_error",
            code="502",
        )


def create_engine(config) -> InferenceEngine:
    engine_type = config.engine.type
    if engine_type == "mock":
        return MockInferenceEngine()
    if engine_type in {"openai-compatible", "vllm", "sglang"}:
        return OpenAICompatibleEngine(
            base_url=config.engine.base_url,
            api_key=config.engine.api_key,
            timeout=config.engine.timeout,
            name=engine_type,
        )
    raise ValueError(f"Unsupported inference engine type: {engine_type}")
