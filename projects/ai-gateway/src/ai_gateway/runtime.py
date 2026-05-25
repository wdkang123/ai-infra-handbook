from __future__ import annotations

import json
from collections import OrderedDict, deque
from dataclasses import dataclass
from threading import Lock
from time import time
from typing import Any


@dataclass
class GatewayMetrics:
    total_requests: int = 0
    successful_requests: int = 0
    rate_limited_requests: int = 0
    auth_failures: int = 0
    upstream_failures: int = 0
    fallback_attempts: int = 0
    fallback_successes: int = 0
    cache_hits: int = 0
    cache_misses: int = 0

    def render_prometheus(self) -> str:
        lines = [
            "# HELP ai_gateway_requests_total Total requests handled by gateway",
            "# TYPE ai_gateway_requests_total counter",
            f"ai_gateway_requests_total {self.total_requests}",
            "# HELP ai_gateway_successful_requests_total Successful proxied requests",
            "# TYPE ai_gateway_successful_requests_total counter",
            f"ai_gateway_successful_requests_total {self.successful_requests}",
            "# HELP ai_gateway_rate_limited_requests_total Requests rejected by rate limit",
            "# TYPE ai_gateway_rate_limited_requests_total counter",
            f"ai_gateway_rate_limited_requests_total {self.rate_limited_requests}",
            "# HELP ai_gateway_auth_failures_total Requests rejected by auth",
            "# TYPE ai_gateway_auth_failures_total counter",
            f"ai_gateway_auth_failures_total {self.auth_failures}",
            "# HELP ai_gateway_upstream_failures_total Requests failed by upstream errors",
            "# TYPE ai_gateway_upstream_failures_total counter",
            f"ai_gateway_upstream_failures_total {self.upstream_failures}",
            "# HELP ai_gateway_fallback_attempts_total Attempts to move from a failed primary candidate to fallback",
            "# TYPE ai_gateway_fallback_attempts_total counter",
            f"ai_gateway_fallback_attempts_total {self.fallback_attempts}",
            "# HELP ai_gateway_fallback_successes_total Requests successfully served by fallback candidates",
            "# TYPE ai_gateway_fallback_successes_total counter",
            f"ai_gateway_fallback_successes_total {self.fallback_successes}",
            "# HELP ai_gateway_cache_hits_total Requests served from response cache",
            "# TYPE ai_gateway_cache_hits_total counter",
            f"ai_gateway_cache_hits_total {self.cache_hits}",
            "# HELP ai_gateway_cache_misses_total Cache lookups that required upstream work",
            "# TYPE ai_gateway_cache_misses_total counter",
            f"ai_gateway_cache_misses_total {self.cache_misses}",
        ]
        return "\n".join(lines)


class InMemoryRateLimiter:
    def __init__(self, requests_per_minute: int) -> None:
        self.requests_per_minute = requests_per_minute
        self._windows: dict[str, deque[float]] = {}
        self._lock = Lock()

    def allow(self, key: str) -> bool:
        now = time()
        cutoff = now - 60.0

        with self._lock:
            window = self._windows.setdefault(key, deque())
            while window and window[0] <= cutoff:
                window.popleft()
            if len(window) >= self.requests_per_minute:
                return False
            window.append(now)
            return True


class InMemoryResponseCache:
    def __init__(self, ttl_seconds: int, max_entries: int) -> None:
        self.ttl_seconds = ttl_seconds
        self.max_entries = max_entries
        self._entries: OrderedDict[str, tuple[float, dict]] = OrderedDict()
        self._lock = Lock()

    def get(self, token: str | None, body: dict) -> dict | None:
        key = self._build_key(token, body)
        now = time()
        with self._lock:
            cached = self._entries.get(key)
            if cached is None:
                return None
            expires_at, payload = cached
            if expires_at <= now:
                self._entries.pop(key, None)
                return None
            self._entries.move_to_end(key)
            return dict(payload)

    def set(self, token: str | None, body: dict, payload: dict) -> None:
        key = self._build_key(token, body)
        expires_at = time() + self.ttl_seconds
        with self._lock:
            self._entries[key] = (expires_at, dict(payload))
            self._entries.move_to_end(key)
            while len(self._entries) > self.max_entries:
                self._entries.popitem(last=False)

    @staticmethod
    def _build_key(token: str | None, body: dict) -> str:
        return json.dumps(
            {
                "token": token or "",
                "body": body,
            },
            sort_keys=True,
            separators=(",", ":"),
        )


class GatewayEventLog:
    FAILURE_EVENT_TYPES = {
        "auth_failed",
        "fallback_attempt",
        "rate_limited",
        "route_not_found",
        "stream_error",
        "upstream_error",
    }
    TERMINAL_FAILURE_EVENT_TYPES = {
        "auth_failed",
        "rate_limited",
        "route_not_found",
        "stream_error",
        "upstream_error",
    }

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
        upstream_model: str | None = None,
    ) -> list[dict[str, Any]]:
        with self._lock:
            events = list(self._events)
        if event_type is not None:
            events = [event for event in events if event.get("event_type") == event_type]
        if request_id is not None:
            events = [event for event in events if event.get("request_id") == request_id]
        if requested_model is not None:
            events = [event for event in events if event.get("requested_model") == requested_model]
        if upstream_model is not None:
            events = [event for event in events if event.get("upstream_model") == upstream_model]
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
        upstream_model: str | None = None,
    ) -> dict[str, Any]:
        events = self.snapshot(
            limit,
            event_type=event_type,
            request_id=request_id,
            requested_model=requested_model,
            upstream_model=upstream_model,
        )
        return {
            "event_count": len(events),
            "request_count": len({event["request_id"] for event in events if event.get("request_id")}),
            "event_type_counts": self._count_by(events, "event_type"),
            "requested_model_counts": self._count_by(events, "requested_model"),
            "upstream_model_counts": self._count_by(events, "upstream_model"),
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
        upstream_model: str | None = None,
    ) -> dict[str, Any]:
        events = self.snapshot(requested_model=requested_model, upstream_model=upstream_model)
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
            "upstream_model_filter": upstream_model,
            "requests": requests,
        }

    def failure_summary(
        self,
        limit: int | None = None,
        *,
        requested_model: str | None = None,
        upstream_model: str | None = None,
    ) -> dict[str, Any]:
        events = self.snapshot(requested_model=requested_model)
        if upstream_model is not None:
            events = [
                event
                for event in events
                if upstream_model
                in {
                    event.get("upstream_model"),
                    event.get("failed_upstream_model"),
                    event.get("next_upstream_model"),
                }
            ]
        if limit is not None:
            events = events[-limit:]
        failure_events = [event for event in events if str(event.get("event_type", "")) in self.FAILURE_EVENT_TYPES]
        terminal_failure_events = [
            event for event in failure_events if str(event.get("event_type", "")) in self.TERMINAL_FAILURE_EVENT_TYPES
        ]
        return {
            "event_count": len(events),
            "failure_event_count": len(failure_events),
            "terminal_failure_count": len(terminal_failure_events),
            "affected_request_count": len({event["request_id"] for event in failure_events if event.get("request_id")}),
            "failed_request_count": len(
                {event["request_id"] for event in terminal_failure_events if event.get("request_id")}
            ),
            "event_type_counts": self._count_by(failure_events, "event_type"),
            "status_code_counts": self._count_by(failure_events, "status_code"),
            "requested_model_counts": self._count_by(failure_events, "requested_model"),
            "upstream_model_counts": self._count_by_any(
                failure_events,
                ("upstream_model", "failed_upstream_model", "next_upstream_model"),
            ),
            "failed_upstream_model_counts": self._count_by(failure_events, "failed_upstream_model"),
            "latest_failure_event": failure_events[-1] if failure_events else None,
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
            "upstream_models": sorted(
                {str(event["upstream_model"]) for event in events if event.get("upstream_model")}
            ),
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

    @staticmethod
    def _count_by_any(events: list[dict[str, Any]], fields: tuple[str, ...]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for event in events:
            seen_values = {str(event[field]) for field in fields if event.get(field) is not None}
            for value in seen_values:
                counts[value] = counts.get(value, 0) + 1
        return counts
