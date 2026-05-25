from __future__ import annotations

from typing import Any

from eval_module.runners.base import EvalRunner
from eval_module.runners.lm_eval_runner import LmEvalRunner

SUPPORTED_BACKENDS = {"vllm", "openai-compatible", "mock"}


def create_runner(backend_config: dict[str, Any]) -> EvalRunner:
    backend_type = backend_config.get("type", "vllm")
    if backend_type not in SUPPORTED_BACKENDS:
        supported = ", ".join(sorted(SUPPORTED_BACKENDS))
        raise ValueError(f"Unsupported eval backend '{backend_type}'. Supported backends: {supported}")
    return LmEvalRunner(backend_config)
