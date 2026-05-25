# eval-module conftest.py Blueprint v1

## Task ID: T1003
## Title: eval-module Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T903 scaffold test-fixture-map，产出 `conftest.py` pytest fixtures 蓝图。

---

# eval-module conftest.py Blueprint v1

## 概述

本文档定义 `tests/conftest.py` 的蓝图——共享 pytest fixtures。

## `tests/conftest.py` 模板

```python
# tests/conftest.py
"""
Pytest configuration and shared fixtures for eval-module.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Generator

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# [PLACEHOLDER] Real imports when implemented:
# from eval_module.runners.lm_eval_runner import LmEvalRunner, EvalResult
# from eval_module.results.result_store import ResultStore
# from eval_module.results.comparator import Comparator


# ---------- Config fixtures ----------

@pytest.fixture
def backend_config() -> dict:
    """Backend config for testing (mock)."""
    return {
        "type": "vllm",
        "base_url": "http://localhost:8000/v1",
    }


@pytest.fixture
def eval_config() -> dict:
    """Full eval config for testing."""
    return {
        "eval": {"backend": "lm-eval", "lm_eval_version": "0.4.3"},
        "backend": {"type": "vllm", "base_url": "http://localhost:8000/v1"},
        "datasets": {
            "mmlu": {"enabled": True, "num_fewshot": 5},
            "gsm8k": {"enabled": True, "num_fewshot": 5},
        },
        "results": {"output_dir": "./results", "format": "json"},
    }


# ---------- Mock Result fixtures ----------

@pytest.fixture
def mock_mmlu_result() -> dict:
    """Mock MMLU evaluation result."""
    return {
        "task": "mmlu",
        "model": "Qwen/Qwen2.5-0.5B-Instruct",
        "accuracy": 0.6534,
        "num_samples": 14242,
        "num_fewshot": 5,
        "timestamp": "2026-04-03T12:00:00Z",
        "lm_eval_version": "0.4.3",
        "backend": "vllm",
        "metrics": {"mmlu": 0.6534},
    }


@pytest.fixture
def mock_gsm8k_result() -> dict:
    """Mock GSM8K evaluation result."""
    return {
        "task": "gsm8k",
        "model": "Qwen/Qwen2.5-0.5B-Instruct",
        "accuracy": 0.5023,
        "num_samples": 1319,
        "num_fewshot": 5,
        "timestamp": "2026-04-03T12:05:00Z",
        "lm_eval_version": "0.4.3",
        "backend": "vllm",
        "metrics": {"gsm8k": 0.5023},
    }


@pytest.fixture
def mock_comparison_result() -> dict:
    """Mock comparison result."""
    return {
        "accuracy_delta": 0.031,
        "baseline": {"task": "mmlu", "accuracy": 0.6534},
        "candidate": {"task": "mmlu", "accuracy": 0.6845},
        "verdict": "candidate outperforms baseline",
    }


# ---------- Runner fixtures ----------

@pytest.fixture
def lm_eval_runner(backend_config: dict) -> "LmEvalRunner":  # [PLACEHOLDER] type
    """LmEvalRunner instance for testing."""
    # [PLACEHOLDER] return LmEvalRunner(backend_config)
    class DummyRunner:
        def list_tasks(self): return ["mmlu", "gsm8k", "humaneval", "truthfulqa"]
    return DummyRunner()


# ---------- Result store fixtures ----------

@pytest.fixture
def result_store(tmp_path: Path) -> "ResultStore":  # [PLACEHOLDER] type
    """ResultStore instance pointing to temp directory."""
    # [PLACEHOLDER] return ResultStore(output_dir=tmp_path)
    class DummyStore:
        pass
    return DummyStore()


@pytest.fixture
def saved_result(
    mock_mmlu_result: dict,
    result_store: "ResultStore",  # [PLACEHOLDER]
    tmp_path: Path,
) -> Path:
    """Save a mock result and return the path."""
    # [PLACEHOLDER]
    result_path = tmp_path / "mmlu_result.json"
    # result_store.save(mock_mmlu_result, result_path)
    return result_path


# ---------- Comparator fixtures ----------

@pytest.fixture
def comparator() -> "Comparator":  # [PLACEHOLDER] type
    """Comparator instance for testing."""
    # [PLACEHOLDER] return Comparator()
    class DummyComparator:
        def compare(self, baseline, candidate):
            return {"accuracy_delta": 0.031}
    return DummyComparator()
```

## `tests/fixtures/` 内容

### `tests/fixtures/mmlu_result.json`

```json
{
  "task": "mmlu",
  "model": "Qwen/Qwen2.5-0.5B-Instruct",
  "accuracy": 0.6534,
  "num_samples": 14242,
  "num_fewshot": 5,
  "timestamp": "2026-04-03T12:00:00Z",
  "lm_eval_version": "0.4.3",
  "backend": "vllm",
  "metrics": {"mmlu": 0.6534}
}
```

### `tests/fixtures/gsm8k_result.json`

```json
{
  "task": "gsm8k",
  "model": "Qwen/Qwen2.5-0.5B-Instruct",
  "accuracy": 0.5023,
  "num_samples": 1319,
  "num_fewshot": 5,
  "timestamp": "2026-04-03T12:05:00Z",
  "lm_eval_version": "0.4.3",
  "backend": "vllm",
  "metrics": {"gsm8k": 0.5023}
}
```

---

Sources:
1. https://pytest.org/ — pytest
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
