from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from threading import Lock
from time import time
from typing import Any


@dataclass
class InferenceMetrics:
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    running_requests: int = 0
    prompt_tokens_total: int = 0
    completion_tokens_total: int = 0

    def render_prometheus(self) -> str:
        return "\n".join(
            [
                "# HELP vllm_num_requests_running Number of running requests",
                "# TYPE vllm_num_requests_running gauge",
                f"vllm_num_requests_running {self.running_requests}",
                "# HELP vllm_num_requests_total Total handled requests",
                "# TYPE vllm_num_requests_total counter",
                f"vllm_num_requests_total {self.total_requests}",
                "# HELP vllm_num_requests_successful_total Total successful requests",
                "# TYPE vllm_num_requests_successful_total counter",
                f"vllm_num_requests_successful_total {self.successful_requests}",
                "# HELP vllm_num_requests_failed_total Total failed requests",
                "# TYPE vllm_num_requests_failed_total counter",
                f"vllm_num_requests_failed_total {self.failed_requests}",
                "# HELP vllm_prompt_tokens_total Total processed prompt tokens",
                "# TYPE vllm_prompt_tokens_total counter",
                f"vllm_prompt_tokens_total {self.prompt_tokens_total}",
                "# HELP vllm_completion_tokens_total Total generated completion tokens",
                "# TYPE vllm_completion_tokens_total counter",
                f"vllm_completion_tokens_total {self.completion_tokens_total}",
                "# HELP vllm_num_tokens_total Total processed tokens",
                "# TYPE vllm_num_tokens_total counter",
                f"vllm_num_tokens_total {self.prompt_tokens_total + self.completion_tokens_total}",
            ]
        )


class InferenceEventLog:
    def __init__(self, max_entries: int = 100) -> None:
        self._events: deque[dict[str, Any]] = deque(maxlen=max_entries)
        self._lock = Lock()

    def append(self, event_type: str, **payload: Any) -> None:
        event = {
            "event_type": event_type,
            "timestamp": time(),
            **payload,
        }
        with self._lock:
            self._events.append(event)

    def snapshot(
        self,
        limit: int | None = None,
        *,
        event_type: str | None = None,
        request_id: str | None = None,
        requested_model: str | None = None,
    ) -> list[dict[str, Any]]:
        with self._lock:
            events = list(self._events)
        if event_type is not None:
            events = [event for event in events if event.get("event_type") == event_type]
        if request_id is not None:
            events = [event for event in events if event.get("request_id") == request_id]
        if requested_model is not None:
            events = [event for event in events if event.get("requested_model") == requested_model]
        if limit is not None:
            return events[-limit:]
        return events

    def summarize(
        self,
        limit: int | None = None,
        *,
        event_type: str | None = None,
        request_id: str | None = None,
        requested_model: str | None = None,
    ) -> dict[str, Any]:
        events = self.snapshot(
            limit,
            event_type=event_type,
            request_id=request_id,
            requested_model=requested_model,
        )
        return {
            "event_count": len(events),
            "request_count": len({event["request_id"] for event in events if event.get("request_id")}),
            "event_type_counts": self._count_by(events, "event_type"),
            "requested_model_counts": self._count_by(events, "requested_model"),
            "engine_counts": self._count_by(events, "engine"),
            "latest_event": events[-1] if events else None,
        }

    def timeline(self, request_id: str) -> dict[str, Any]:
        events = self.snapshot(request_id=request_id)
        return self._build_timeline(request_id, events, include_events=True)

    def request_index(
        self,
        limit: int | None = None,
        *,
        requested_model: str | None = None,
    ) -> dict[str, Any]:
        events = self.snapshot(requested_model=requested_model)
        grouped_events: dict[str, list[dict[str, Any]]] = {}
        for event in events:
            request_id = event.get("request_id")
            if not request_id:
                continue
            grouped_events.setdefault(str(request_id), []).append(event)

        requests = [
            self._build_timeline(request_id, request_events, include_events=False)
            for request_id, request_events in grouped_events.items()
        ]
        requests.sort(key=lambda item: item.get("ended_at") or 0, reverse=True)
        matched_request_count = len(requests)
        if limit is not None:
            requests = requests[:limit]
        return {
            "request_count": len(requests),
            "matched_request_count": matched_request_count,
            "requested_model_filter": requested_model,
            "requests": requests,
        }

    @staticmethod
    def _build_timeline(request_id: str, events: list[dict[str, Any]], *, include_events: bool) -> dict[str, Any]:
        started_at = events[0]["timestamp"] if events else None
        ended_at = events[-1]["timestamp"] if events else None
        timeline = {
            "request_id": request_id,
            "event_count": len(events),
            "started_at": started_at,
            "ended_at": ended_at,
            "duration_seconds": round(ended_at - started_at, 6)
            if started_at is not None and ended_at is not None
            else None,
            "event_types": [str(event.get("event_type", "")) for event in events],
            "requested_models": sorted(
                {str(event["requested_model"]) for event in events if event.get("requested_model")}
            ),
            "engines": sorted({str(event["engine"]) for event in events if event.get("engine")}),
            "terminal_event_type": events[-1].get("event_type") if events else None,
        }
        if include_events:
            timeline["events"] = events
        return timeline

    @staticmethod
    def _count_by(events: list[dict[str, Any]], field: str) -> dict[str, int]:
        counts: dict[str, int] = {}
        for event in events:
            value = event.get(field)
            if value is None:
                continue
            key = str(value)
            counts[key] = counts.get(key, 0) + 1
        return counts
