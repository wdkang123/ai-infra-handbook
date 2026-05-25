# eval-module lm_eval_runner.py Blueprint v1

## Task ID: T1003
## Title: eval-module Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T903 scaffold（runner-cli blueprint / sample-results），产出 `lm_eval_runner.py` 蓝图。

---

# eval-module lm_eval_runner.py Blueprint v1

## 概述

本文档定义 `src/eval_module/runners/lm_eval_runner.py` 的蓝图——lm-eval harness 的封装 runner。

## `src/eval_module/runners/lm_eval_runner.py` 模板

```python
# src/eval_module/runners/lm_eval_runner.py
"""
lm-eval harness runner for eval-module.

Wraps EleutherAI/lm-evaluation-harness to provide a clean Python API.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import httpx


@dataclass
class EvalResult:
    """Evaluation result container."""
    task: str
    model: str
    accuracy: float
    num_samples: int
    num_fewshot: int
    timestamp: str
    lm_eval_version: str
    backend: str
    metrics: dict[str, float] = field(default_factory=dict)
    # [PLACEHOLDER] add raw lm-eval output for debugging
    raw_output: dict[str, Any] | None = None


class LmEvalRunner:
    """
    Wrapper around lm-evaluation-harness.

    Provides a Python API to run evaluations without CLI subprocess.
    """

    def __init__(self, backend_config: dict[str, Any]) -> None:
        """
        Args:
            backend_config: dict with keys:
                - type: "vllm" | "openai" | ...
                - base_url: str
                - api_key: str (optional)
        """
        self.backend_type = backend_config.get("type", "vllm")
        self.base_url = backend_config.get("base_url", "http://localhost:8000/v1")
        self.api_key = backend_config.get("api_key", "")

    def list_tasks(self) -> list[str]:
        """
        List all available tasks from lm-eval.

        Returns:
            List of task names (e.g. ["mmlu", "gsm8k", "humaneval", ...])
        """
        # [PLACEHOLDER] 真实实现：
        # from lm_eval import evaluator, tasks
        # return sorted(tasks.TaskManager().all_tasks.keys())
        return ["mmlu", "gsm8k", "humaneval", "truthfulqa"]

    def run(
        self,
        task: str,
        model: str,
        num_fewshot: int = 5,
        limit: int | None = None,
        **kwargs: Any,
    ) -> EvalResult:
        """
        Run a single evaluation task.

        Args:
            task: Task name (e.g. "mmlu", "gsm8k")
            model: HuggingFace model name
            num_fewshot: Number of few-shot examples
            limit: Limit number of samples (for debugging)
            **kwargs: Additional lm-eval arguments

        Returns:
            EvalResult with accuracy and metadata.

        Raises:
            ValueError: If task is not found.
            RuntimeError: If evaluation fails.
        """
        # [PLACEHOLDER] 真实实现：
        # import time
        #
        # results = lm_eval.evaluator.evaluate(
        #     lm_eval.tasks.get_task(task),
        #     model=self._make_lm_model(),
        #     num_fewshot=num_fewshot,
        #     limit=limit,
        # )
        #
        # task_results = results["results"][task]
        # accuracy = task_results.get("acc", task_results.get("accuracy", 0.0))
        #
        # return EvalResult(
        #     task=task,
        #     model=model,
        #     accuracy=accuracy,
        #     num_samples=results["configs"][task].get("num_samples", 0),
        #     num_fewshot=num_fewshot,
        #     timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        #     lm_eval_version=self._get_lm_eval_version(),
        #     backend=self.backend_type,
        #     metrics={task: accuracy},
        #     raw_output=results,
        # )
        import time
        return EvalResult(
            task=task,
            model=model,
            accuracy=0.6534,  # [PLACEHOLDER]
            num_samples=14242,  # [PLACEHOLDER]
            num_fewshot=num_fewshot,
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            lm_eval_version="0.4.3",  # [PLACEHOLDER]
            backend=self.backend_type,
            metrics={task: 0.6534},
        )

    def _make_lm_model(self) -> Any:
        """
        Create lm-eval compatible model instance.

        [PLACEHOLDER] 真实实现根据 self.backend_type 选择:
        - vllm: VLLM(model=..., base_url=..., ...)
        - openai: OpenAI(model=..., api_key=..., ...)
        """
        # [PLACEHOLDER]
        return None

    def _get_lm_eval_version(self) -> str:
        """Get lm-eval version string."""
        # [PLACEHOLDER]
        return "0.4.3"
```

## EvalResult 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `task` | str | 任务名 |
| `model` | str | 模型名 |
| `accuracy` | float | 整体准确率 |
| `num_samples` | int | 样本数量 |
| `num_fewshot` | int | few-shot 数 |
| `timestamp` | ISO8601 | 评测时间 |
| `lm_eval_version` | str | lm-eval 版本 |
| `backend` | str | 推理 backend |
| `metrics` | dict | 任务特定指标 |

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
2. https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks — lm-eval tasks

Risk of Staleness:
- lm-eval API 在 0.4.x 相对稳定
