from __future__ import annotations

from inference_service.runtime import InferenceMetrics


def render_metrics(metrics: InferenceMetrics) -> str:
    return metrics.render_prometheus()
