# eval-module result_store.py Blueprint v1

## Task ID: T1003
## Title: eval-module Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T903 scaffold（sample-results catalog），产出结果持久化蓝图。

---

# eval-module result_store.py Blueprint v1

## 概述

本文档定义 `src/eval_module/results/result_store.py` 和 `comparator.py` 的蓝图——结果 JSON 持久化和历史对比。

## `src/eval_module/results/result_store.py` 模板

```python
# src/eval_module/results/result_store.py
"""
Result persistence for eval-module.

Saves and loads evaluation results as JSON files.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import jsonpickle


class ResultStore:
    """
    Persists evaluation results to JSON files.

    Format: eval_result_{task}_{timestamp}.json
    """

    def __init__(self, output_dir: Path | str = "./results") -> None:
        """
        Args:
            output_dir: Directory to save result files.
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(
        self,
        result: dict[str, Any] | Any,
        path: Path | str,
    ) -> Path:
        """
        Save an evaluation result to JSON.

        Args:
            result: EvalResult dict or object (dataclass).
            path: Target file path.

        Returns:
            The resolved path.
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Use jsonpickle for dataclass serialization
        serialized = jsonpickle.encode(result)
        with open(path, "w") as f:
            json.dump(json.loads(serialized), f, indent=2, ensure_ascii=False)

        return path

    def load(self, path: Path | str) -> dict[str, Any]:
        """
        Load a result file from JSON.

        Args:
            path: Path to result JSON file.

        Returns:
            Dict representation of EvalResult.

        Raises:
            FileNotFoundError: If file does not exist.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Result file not found: {path}")

        with open(path) as f:
            data = json.load(f)

        # Decode jsonpickle if present
        if isinstance(data, dict) and data.get("py/state/"):
            decoded = jsonpickle.decode(json.dumps(data))
            return decoded if isinstance(decoded, dict) else vars(decoded)
        return data

    def save_comparison(
        self,
        diff: dict[str, Any],
        path: Path | str,
    ) -> Path:
        """
        Save a comparison report to JSON.

        Args:
            diff: Diff dict from Comparator.compare().
            path: Target file path.

        Returns:
            The resolved path.
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        report = {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "comparison": diff,
        }

        with open(path, "w") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return path
```

## `src/eval_module/results/comparator.py` 模板

```python
# src/eval_module/results/comparator.py
"""
Comparator for evaluation results.

Compares baseline vs candidate results and computes deltas.
"""
from __future__ import annotations

from typing import Any


class Comparator:
    """
    Compare two evaluation results.

    Computes accuracy delta and determines verdict.
    """

    def compare(
        self,
        baseline: dict[str, Any],
        candidate: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Compare baseline and candidate results.

        Args:
            baseline: Baseline EvalResult dict.
            candidate: Candidate EvalResult dict.

        Returns:
            Diff dict with:
            - accuracy_delta: float
            - baseline: {task, accuracy, ...}
            - candidate: {task, accuracy, ...}
            - verdict: str
        """
        baseline_acc = baseline.get("accuracy", 0.0)
        candidate_acc = candidate.get("accuracy", 0.0)
        delta = candidate_acc - baseline_acc

        if delta > 0:
            verdict = "candidate outperforms baseline"
        elif delta < 0:
            verdict = "candidate underperforms baseline"
        else:
            verdict = "no change"

        # [PLACEHOLDER] add per-subject delta for MMLU
        diff: dict[str, Any] = {
            "accuracy_delta": round(delta, 4),
            "relative_improvement": round((delta / baseline_acc) * 100, 2) if baseline_acc else 0.0,
            "improvement_percent": f"{'+' if delta >= 0 else ''}{round(delta * 100, 2)}pp",
            "verdict": verdict,
            "baseline": {
                "task": baseline.get("task"),
                "model": baseline.get("model"),
                "accuracy": baseline_acc,
                "num_samples": baseline.get("num_samples"),
                "timestamp": baseline.get("timestamp"),
            },
            "candidate": {
                "task": candidate.get("task"),
                "model": candidate.get("model"),
                "accuracy": candidate_acc,
                "num_samples": candidate.get("num_samples"),
                "timestamp": candidate.get("timestamp"),
            },
        }

        # Per-subject delta for MMLU
        if "subjects" in baseline and "subjects" in candidate:
            diff["subjects_delta"] = {
                subject: round(
                    candidate["subjects"].get(subject, 0) - baseline["subjects"].get(subject, 0),
                    4,
                )
                for subject in set(baseline["subjects"]) | set(candidate["subjects"])
            }

        return diff
```

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
2. https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks/mmlu — MMLU

Risk of Staleness:
- Result JSON 格式基于 lm-eval 0.4.x 输出
