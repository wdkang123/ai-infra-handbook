# eval-module test_runner.py Blueprint v1

## Task ID: T1003
## Title: eval-module Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T903 scaffold（runner-cli / test-fixture-map），产出 `test_runner.py` 蓝图。

---

# eval-module test_runner.py Blueprint v1

## 概述

本文档定义 `tests/test_runner.py` 的蓝图——runner 单元测试。

## `tests/test_runner.py` 模板

```python
# tests/test_runner.py
"""
Tests for eval-module runner.

Tests:
- list_tasks returns non-empty list
- run mmlu returns accuracy
- run invalid task raises ValueError
- ResultStore save/load roundtrip
- Comparator accuracy_delta
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

# [PLACEHOLDER] Real imports when implemented:
# from eval_module.runners.lm_eval_runner import LmEvalRunner, EvalResult
# from eval_module.results.result_store import ResultStore
# from eval_module.results.comparator import Comparator


# ---------- Runner Tests ----------

class TestLmEvalRunner:
    """Tests for LmEvalRunner."""

    def test_list_tasks_returns_list(self, lm_eval_runner: Any) -> None:
        """
        Test that list_tasks returns a non-empty list.

        Should include mmlu, gsm8k, etc.
        """
        # [PLACEHOLDER]
        # tasks = lm_eval_runner.list_tasks()
        # assert isinstance(tasks, list)
        # assert len(tasks) > 0
        # assert "mmlu" in tasks
        pass

    def test_list_tasks_contains_expected_tasks(self, lm_eval_runner: Any) -> None:
        """
        Test that expected tasks are in the task list.
        """
        # [PLACEHOLDER]
        # tasks = lm_eval_runner.list_tasks()
        # for task in ["mmlu", "gsm8k"]:
        #     assert task in tasks, f"{task} not found in task list"
        pass

    def test_run_mmlu_returns_accuracy(self, lm_eval_runner: Any) -> None:
        """
        Test that running MMLU returns a result with accuracy.

        [PLACEHOLDER] Note: This requires a real or mocked downstream.
        For unit tests, use mock_mmlu_result fixture.
        """
        # [PLACEHOLDER]
        # result = lm_eval_runner.run(task="mmlu", model="Qwen/Qwen2.5-0.5B-Instruct", num_fewshot=5)
        # assert isinstance(result, EvalResult)
        # assert result.task == "mmlu"
        # assert 0.0 <= result.accuracy <= 1.0
        pass

    def test_run_invalid_task_raises(self, lm_eval_runner: Any) -> None:
        """
        Test that running an unknown task raises ValueError.
        """
        # [PLACEHOLDER]
        # with pytest.raises(ValueError, match="not found"):
        #     lm_eval_runner.run(task="nonexistent-task", model="test", num_fewshot=0)
        pass

    def test_run_with_limit(self, lm_eval_runner: Any) -> None:
        """
        Test that limit parameter is passed to lm-eval.
        """
        # [PLACEHOLDER]
        # result = lm_eval_runner.run(task="mmlu", model="test", num_fewshot=0, limit=10)
        # assert result.num_samples == 10
        pass


# ---------- Result Store Tests ----------

class TestResultStore:
    """Tests for ResultStore."""

    def test_save_and_load_roundtrip(
        self,
        result_store: Any,
        mock_mmlu_result: dict[str, Any],
        tmp_path: Path,
    ) -> None:
        """
        Test that save and load produces identical data.
        """
        # [PLACEHOLDER]
        # path = tmp_path / "test_result.json"
        # result_store.save(mock_mmlu_result, path)
        # loaded = result_store.load(path)
        # assert loaded["task"] == "mmlu"
        # assert loaded["accuracy"] == 0.6534
        pass

    def test_load_nonexistent_raises(
        self,
        result_store: Any,
    ) -> None:
        """
        Test that loading a non-existent file raises FileNotFoundError.
        """
        # [PLACEHOLDER]
        # with pytest.raises(FileNotFoundError):
        #     result_store.load(Path("/nonexistent/file.json"))
        pass

    def test_save_comparison(
        self,
        result_store: Any,
        mock_comparison_result: dict[str, Any],
        tmp_path: Path,
    ) -> None:
        """
        Test saving a comparison report.
        """
        # [PLACEHOLDER]
        # path = tmp_path / "comparison.json"
        # result_store.save_comparison(mock_comparison_result, path)
        # assert path.exists()
        pass


# ---------- Comparator Tests ----------

class TestComparator:
    """Tests for Comparator."""

    def test_compare_accuracy_delta_positive(
        self,
        comparator: Any,
        mock_mmlu_result: dict[str, Any],
    ) -> None:
        """
        Test that candidate outperforming baseline gives positive delta.
        """
        # [PLACEHOLDER]
        # baseline = {**mock_mmlu_result, "accuracy": 0.65}
        # candidate = {**mock_mmlu_result, "accuracy": 0.68}
        # diff = comparator.compare(baseline, candidate)
        # assert diff["accuracy_delta"] == pytest.approx(0.03)
        # assert diff["verdict"] == "candidate outperforms baseline"
        pass

    def test_compare_no_change(
        self,
        comparator: Any,
        mock_mmlu_result: dict[str, Any],
    ) -> None:
        """
        Test that identical accuracy gives 'no change' verdict.
        """
        # [PLACEHOLDER]
        # baseline = {**mock_mmlu_result, "accuracy": 0.65}
        # candidate = {**mock_mmlu_result, "accuracy": 0.65}
        # diff = comparator.compare(baseline, candidate)
        # assert diff["accuracy_delta"] == 0.0
        # assert diff["verdict"] == "no change"
        pass

    def test_compare_negative_delta(
        self,
        comparator: Any,
        mock_mmlu_result: dict[str, Any],
    ) -> None:
        """
        Test that candidate underperforming gives negative delta.
        """
        # [PLACEHOLDER]
        # baseline = {**mock_mmlu_result, "accuracy": 0.65}
        # candidate = {**mock_mmlu_result, "accuracy": 0.60}
        # diff = comparator.compare(baseline, candidate)
        # assert diff["accuracy_delta"] == pytest.approx(-0.05)
        # assert diff["verdict"] == "candidate underperforms baseline"
        pass
```

## 测试覆盖矩阵

| 测试 | 描述 | 依赖 |
|------|------|------|
| `test_list_tasks_returns_list` | 列出任务非空 | `lm_eval_runner` |
| `test_list_tasks_contains_expected` | 包含 mmlu/gsm8k | `lm_eval_runner` |
| `test_run_mmlu_returns_accuracy` | 运行 MMLU 有准确率 | `lm_eval_runner` |
| `test_run_invalid_task_raises` | 未知任务抛异常 | `lm_eval_runner` |
| `test_save_and_load_roundtrip` | 保存加载往返 | `result_store`, `mock_mmlu_result` |
| `test_load_nonexistent_raises` | 加载不存在文件抛异常 | `result_store` |
| `test_compare_accuracy_delta_positive` | 候选胜出 delta > 0 | `comparator`, `mock_mmlu_result` |

---

Sources:
1. https://pytest.org/ — pytest
2. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval
