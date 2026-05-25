# eval-module Test Fixture Map v1

## Task ID: T903
## Title: eval-module Scaffold Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T803 test plan，产出测试 fixture 蓝图。

---

# eval-module Test Fixture Map v1

## 概述

本文档定义 eval-module 的 pytest fixture 蓝图。

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

from eval_module.evaluator import Evaluator
from eval_module.runners.lm_eval_runner import LmEvalRunner
from eval_module.results.result_store import ResultStore
from eval_module.results.comparator import Comparator


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
    }


# ---------- Runner fixtures ----------

@pytest.fixture
def lm_eval_runner(backend_config: dict) -> LmEvalRunner:
    """LmEvalRunner instance for testing."""
    return LmEvalRunner(backend_config)


@pytest.fixture
def evaluator(backend_config: dict) -> Evaluator:
    """Evaluator instance for testing."""
    return Evaluator(backend="lm-eval", backend_config=backend_config)


# ---------- Result store fixtures ----------

@pytest.fixture
def result_store(tmp_path: Path) -> ResultStore:
    """ResultStore instance pointing to temp directory."""
    return ResultStore(output_dir=tmp_path)


@pytest.fixture
def saved_result(mock_mmlu_result: dict, result_store: ResultStore, tmp_path: Path) -> Path:
    """Save a mock result and return the path."""
    result_path = tmp_path / "mmlu_result.json"
    result_store.save(mock_mmlu_result, result_path)
    return result_path


# ---------- Comparator fixtures ----------

@pytest.fixture
def comparator() -> Comparator:
    """Comparator instance for testing."""
    return Comparator()
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

## 测试用例示例

```python
# tests/test_runner.py
import pytest
from eval_module.runners.lm_eval_runner import LmEvalRunner

def test_list_tasks(lm_eval_runner: LmEvalRunner):
    """Test that list_tasks returns non-empty list."""
    tasks = lm_eval_runner.list_tasks()
    assert isinstance(tasks, list)
    assert len(tasks) > 0
    assert "mmlu" in tasks

def test_run_invalid_task(lm_eval_runner: LmEvalRunner):
    """Test that invalid task raises ValueError."""
    with pytest.raises(ValueError):
        lm_eval_runner.run(task="nonexistent-task", model="test", num_fewshot=0)


# tests/test_result_store.py
def test_save_and_load(result_store: ResultStore, mock_mmlu_result: dict, tmp_path: Path):
    """Test save and load roundtrip."""
    path = tmp_path / "test_result.json"
    result_store.save(mock_mmlu_result, path)
    loaded = result_store.load(path)
    assert loaded["task"] == "mmlu"
    assert loaded["accuracy"] == 0.6534

def test_load_nonexistent(result_store: ResultStore):
    """Test loading non-existent file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        result_store.load(Path("/nonexistent/file.json"))


# tests/test_comparator.py
def test_compare_accuracy_delta(comparator: Comparator, mock_mmlu_result: dict):
    """Test delta calculation."""
    baseline = {**mock_mmlu_result, "accuracy": 0.65}
    candidate = {**mock_mmlu_result, "accuracy": 0.68}
    diff = comparator.compare(baseline, candidate)
    assert diff["accuracy_delta"] == pytest.approx(0.03)
```

---

Sources:
1. https://pytest.org/ — pytest
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval

Risk of Staleness:
- lm-eval API 变化可能影响 fixture

Out of Scope Kept:
- 未写端到端集成测试 fixtures（需要真实 GPU）
