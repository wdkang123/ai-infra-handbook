from __future__ import annotations

import json
from pathlib import Path

import pytest
from eval_module.results.result_store import ResultStore
from eval_module.runners.factory import create_runner
from eval_module.runners.lm_eval_runner import EvalResult, LmEvalRunner


def test_runner_list_tasks() -> None:
    runner = LmEvalRunner({"type": "vllm", "base_url": "http://localhost:8000/v1"})
    tasks = runner.list_tasks()
    assert "mmlu" in tasks
    assert "gsm8k" in tasks


def test_runner_factory_rejects_unknown_backend() -> None:
    with pytest.raises(ValueError, match="Unsupported eval backend"):
        create_runner({"type": "unknown"})


def test_runner_factory_creates_openai_compatible_runner() -> None:
    runner = create_runner({"type": "openai-compatible", "base_url": "http://localhost:8000/v1"})
    assert "mmlu" in runner.list_tasks()


def test_runner_returns_eval_result() -> None:
    runner = LmEvalRunner({"type": "vllm", "base_url": "http://localhost:8000/v1"})
    result = runner.run("mmlu", "Qwen/Qwen2.5-0.5B-Instruct")
    assert isinstance(result, EvalResult)
    assert result.task == "mmlu"
    assert result.backend == "vllm"
    assert result.sample_outputs[0]["sample_id"] == "mmlu-0001"
    assert result.sample_outputs[0]["judge_reason"] == "mock score passes threshold"
    assert result.sample_outputs[0]["prompt_tokens"] == 4
    assert result.raw_output["sample_output_count"] == 5


def test_runner_rejects_unknown_task() -> None:
    runner = LmEvalRunner({"type": "vllm", "base_url": "http://localhost:8000/v1"})
    with pytest.raises(ValueError, match="Unsupported task"):
        runner.run("unknown", "Qwen/Qwen2.5-0.5B-Instruct")


def test_result_store_round_trip(tmp_path: Path) -> None:
    store = ResultStore(tmp_path)
    result = EvalResult(
        task="mmlu",
        model="Qwen/Qwen2.5-0.5B-Instruct",
        accuracy=0.5,
        num_samples=10,
        num_fewshot=5,
        timestamp="2026-04-08T00:00:00Z",
        lm_eval_version="0.4.3",
        backend="vllm",
        metrics={"mmlu": 0.5},
    )
    path = tmp_path / "result.json"
    store.save(result, path)
    loaded = store.load(path)
    assert loaded.task == "mmlu"
    assert loaded.metrics["mmlu"] == 0.5
    bundle = store.save_run_bundle(loaded, tmp_path / "result.json")
    assert (bundle["artifact_dir"] / "run_manifest.json").exists()
    assert (bundle["artifact_dir"] / "summary.md").exists()
    assert (bundle["artifact_dir"] / "sample_outputs.json").exists()
    assert (bundle["artifact_dir"] / "sample_summary.json").exists()
    assert (bundle["artifact_dir"] / "sample_analysis.json").exists()
    manifest = json.loads((bundle["artifact_dir"] / "run_manifest.json").read_text())
    assert manifest["sample_outputs_file"] == "sample_outputs.json"
    assert manifest["sample_summary_file"] == "sample_summary.json"
    assert manifest["sample_analysis_file"] == "sample_analysis.json"
    sample_summary = json.loads((bundle["artifact_dir"] / "sample_summary.json").read_text())
    assert sample_summary == {
        "sample_count": 0,
        "passed_count": 0,
        "failed_count": 0,
        "average_score": 0.0,
        "prompt_tokens": 0,
        "prediction_tokens": 0,
    }
    sample_analysis = json.loads((bundle["artifact_dir"] / "sample_analysis.json").read_text())
    assert sample_analysis["pass_rate"] == 0.0
    assert sample_analysis["failed_sample_ids"] == []
    assert sample_analysis["score_buckets"] == {
        "low_lt_0_5": 0,
        "mid_0_5_to_0_8": 0,
        "high_gte_0_8": 0,
    }
    assert "Sample Summary" in (bundle["artifact_dir"] / "summary.md").read_text()
    assert (tmp_path / "run_history.jsonl").exists()


def test_result_store_save_comparison(tmp_path: Path) -> None:
    store = ResultStore(tmp_path)
    target = tmp_path / "compare.json"
    store.save_comparison({"summary": {"delta": 0.1}}, target)
    assert target.exists()


def test_compare_report_round_trip(tmp_path: Path) -> None:
    store = ResultStore(tmp_path)
    baseline = EvalResult(
        task="mmlu",
        model="Qwen/Qwen2.5-0.5B-Instruct",
        accuracy=0.5,
        num_samples=10,
        num_fewshot=5,
        timestamp="2026-04-08T00:00:00Z",
        lm_eval_version="0.4.3",
        backend="vllm",
        metrics={"mmlu": 0.5},
    )
    candidate = EvalResult(
        task="mmlu",
        model="Qwen/Qwen2.5-0.5B-Instruct",
        accuracy=0.6,
        num_samples=10,
        num_fewshot=5,
        timestamp="2026-04-08T00:01:00Z",
        lm_eval_version="0.4.3",
        backend="vllm",
        metrics={"mmlu": 0.6},
    )
    baseline_path = tmp_path / "baseline.json"
    candidate_path = tmp_path / "candidate.json"
    report_path = tmp_path / "report.json"
    store.save(baseline, baseline_path)
    store.save(candidate, candidate_path)
    diff = store.build_comparison(baseline, candidate)
    store.save_comparison(diff, report_path)
    markdown_path = tmp_path / "report.md"
    store.save_comparison_markdown(diff, markdown_path)
    bundle = store.save_comparison_bundle(diff, report_path)
    assert report_path.exists()
    assert markdown_path.exists()
    report = report_path.read_text()
    assert '"verdict": "improved"' in report
    assert '"release_recommendation": "approve"' in report
    assert '"metric_deltas"' in report
    markdown = markdown_path.read_text()
    assert "Evaluation Comparison Report" in markdown
    assert "Release recommendation" in markdown
    assert (bundle["artifact_dir"] / "comparison_manifest.json").exists()
    manifest = json.loads((bundle["artifact_dir"] / "comparison_manifest.json").read_text())
    assert manifest["release_recommendation"] == "approve"
    assert (tmp_path / "comparison_history.jsonl").exists()
    history_entry = json.loads((tmp_path / "comparison_history.jsonl").read_text())
    assert history_entry["comparison_file"].endswith("report/comparison.json")
    assert history_entry["baseline_model"] == baseline.model
    assert history_entry["candidate_model"] == candidate.model

    comparison_index = store.build_comparison_index()
    assert comparison_index["report_type"] == "eval_comparison_index"
    assert comparison_index["comparison_count"] == 1
    assert comparison_index["verdict_counts"] == {"improved": 1}
    assert comparison_index["recommendation_counts"] == {"approve": 1}
    assert comparison_index["average_delta"] == 0.1
    assert comparison_index["max_delta"] == 0.1
    assert comparison_index["min_delta_seen"] == 0.1
    assert comparison_index["task_summaries"][0]["task"] == "mmlu"
    assert comparison_index["task_summaries"][0]["comparison_count"] == 1
    assert comparison_index["task_summaries"][0]["verdict_counts"] == {"improved": 1}
    assert comparison_index["task_summaries"][0]["recommendation_counts"] == {"approve": 1}
    assert comparison_index["task_summaries"][0]["latest_comparison_file"].endswith("report/comparison.json")
    assert comparison_index["comparisons"][0]["release_recommendation"] == "approve"
    assert comparison_index["comparisons"][0]["comparison_file"].endswith("report/comparison.json")
    comparison_index_markdown = store.render_comparison_index_markdown(comparison_index)
    assert "Evaluation Comparison Index" in comparison_index_markdown
    assert "approve" in comparison_index_markdown
    assert "Verdict counts" in comparison_index_markdown
    assert "Task Summaries" in comparison_index_markdown
    comparison_index_json = store.save_comparison_index(comparison_index, tmp_path / "comparison_index.json")
    comparison_index_md = store.save_comparison_index_markdown(comparison_index, tmp_path / "comparison_index.md")
    assert comparison_index_json.exists()
    assert comparison_index_md.exists()


def test_result_store_builds_leaderboard_from_run_history(tmp_path: Path) -> None:
    store = ResultStore(tmp_path)
    base = EvalResult(
        task="mmlu",
        model="base",
        accuracy=0.5,
        num_samples=10,
        num_fewshot=5,
        timestamp="2026-04-08T00:00:00Z",
        lm_eval_version="0.4.3",
        backend="vllm",
        metrics={"mmlu": 0.5},
    )
    candidate_best = EvalResult(
        task="mmlu",
        model="candidate",
        accuracy=0.62,
        num_samples=10,
        num_fewshot=5,
        timestamp="2026-04-08T00:01:00Z",
        lm_eval_version="0.4.3",
        backend="vllm",
        metrics={"mmlu": 0.62},
        sample_outputs=[{"score": 0.62, "passed": True, "prompt_tokens": 4, "prediction_tokens": 5}],
    )
    candidate_latest = EvalResult(
        task="mmlu",
        model="candidate",
        accuracy=0.58,
        num_samples=10,
        num_fewshot=5,
        timestamp="2026-04-08T00:02:00Z",
        lm_eval_version="0.4.3",
        backend="vllm",
        metrics={"mmlu": 0.58},
    )
    candidate_other_backend = EvalResult(
        task="mmlu",
        model="candidate",
        accuracy=0.7,
        num_samples=10,
        num_fewshot=0,
        timestamp="2026-04-08T00:03:00Z",
        lm_eval_version="0.4.3",
        backend="openai-compatible",
        metrics={"mmlu": 0.7},
    )

    store.save_run_bundle(base, tmp_path / "base.json")
    candidate_best_bundle = store.save_run_bundle(candidate_best, tmp_path / "candidate-best.json")
    store.save_run_bundle(candidate_latest, tmp_path / "candidate-latest.json")
    store.save_run_bundle(candidate_other_backend, tmp_path / "candidate-openai.json")
    candidate_best_analysis = json.loads((candidate_best_bundle["artifact_dir"] / "sample_analysis.json").read_text())
    assert candidate_best_analysis["pass_rate"] == 1.0
    assert candidate_best_analysis["score_buckets"]["mid_0_5_to_0_8"] == 1

    report = store.build_leaderboard()
    assert report["report_type"] == "eval_leaderboard"
    assert report["run_count"] == 4
    assert report["model_count"] == 3
    assert report["backend_count"] == 2
    assert report["fewshot_count"] == 2
    assert report["entries"][0]["model"] == "candidate"
    assert report["entries"][0]["backend"] == "openai-compatible"
    assert report["entries"][0]["rank"] == 1
    assert report["entries"][0]["best_accuracy"] == 0.7
    assert report["backend_groups"]["vllm"][0]["model"] == "candidate"
    assert report["fewshot_groups"]["5"][0]["model"] == "candidate"

    filtered_report = store.build_leaderboard(backend="vllm", num_fewshot=5)
    assert filtered_report["run_count"] == 3
    assert filtered_report["model_count"] == 2
    assert filtered_report["backend_filter"] == "vllm"
    assert filtered_report["num_fewshot_filter"] == 5
    assert filtered_report["entries"][0]["model"] == "candidate"
    assert filtered_report["entries"][0]["rank"] == 1
    assert filtered_report["entries"][0]["best_accuracy"] == 0.62
    assert filtered_report["entries"][0]["latest_accuracy"] == 0.58
    assert filtered_report["entries"][0]["run_count"] == 2
    assert filtered_report["entries"][0]["sample_summary"]["prompt_tokens"] == 4

    markdown = store.render_leaderboard_markdown(report)
    assert "Evaluation Leaderboard" in markdown
    assert "| Rank | Model | Best Accuracy" in markdown
    assert "| Rank | Best Result File | Latest Result File |" in markdown
    assert "Backend Views" in markdown
    assert "Few-shot Views" in markdown
    assert "candidate-best/result.json" in markdown
    assert "candidate-latest/result.json" in markdown
    assert "candidate" in markdown

    json_path = store.save_leaderboard(report, tmp_path / "leaderboard.json")
    markdown_path = store.save_leaderboard_markdown(report, tmp_path / "leaderboard.md")
    assert json_path.exists()
    assert markdown_path.exists()

    run_index = store.build_run_index(model="candidate", backend="vllm", num_fewshot=5)
    assert run_index["report_type"] == "eval_run_index"
    assert run_index["run_count"] == 2
    assert run_index["matched_run_count"] == 2
    assert run_index["backend_filter"] == "vllm"
    assert run_index["num_fewshot_filter"] == 5
    assert run_index["backend_count"] == 1
    assert run_index["fewshot_count"] == 1
    assert run_index["task_summaries"][0]["task"] == "mmlu"
    assert run_index["task_summaries"][0]["run_count"] == 2
    assert run_index["task_summaries"][0]["best_accuracy"] == 0.62
    assert run_index["task_summaries"][0]["latest_accuracy"] == 0.58
    assert run_index["task_summaries"][0]["latest_result_file"].endswith("candidate-latest/result.json")
    assert run_index["runs"][0]["timestamp"] == "2026-04-08T00:02:00Z"
    assert run_index["runs"][0]["result_file"].endswith("candidate-latest/result.json")
    assert run_index["runs"][1]["sample_analysis"]["pass_rate"] == 1.0
    run_index_markdown = store.render_run_index_markdown(run_index)
    assert "Evaluation Run Index" in run_index_markdown
    assert "Task Summaries" in run_index_markdown
    assert "candidate-latest/result.json" in run_index_markdown
    run_index_json_path = store.save_run_index(run_index, tmp_path / "run_index.json")
    run_index_markdown_path = store.save_run_index_markdown(run_index, tmp_path / "run_index.md")
    assert run_index_json_path.exists()
    assert run_index_markdown_path.exists()


def test_compare_report_respects_min_delta_threshold(tmp_path: Path) -> None:
    store = ResultStore(tmp_path)
    baseline = EvalResult(
        task="mmlu",
        model="base",
        accuracy=0.5,
        num_samples=10,
        num_fewshot=5,
        timestamp="2026-04-08T00:00:00Z",
        lm_eval_version="0.4.3",
        backend="vllm",
        metrics={"mmlu": 0.5},
    )
    candidate = EvalResult(
        task="mmlu",
        model="candidate",
        accuracy=0.51,
        num_samples=10,
        num_fewshot=5,
        timestamp="2026-04-08T00:01:00Z",
        lm_eval_version="0.4.3",
        backend="vllm",
        metrics={"mmlu": 0.51},
    )

    diff = store.build_comparison(baseline, candidate, min_delta=0.02)
    markdown = store.render_comparison_markdown(diff)

    assert diff["summary"]["verdict"] == "unchanged"
    assert diff["summary"]["release_recommendation"] == "review"
    assert diff["summary"]["min_delta"] == 0.02
    assert "Min delta" in markdown


def test_compare_report_blocks_regressed_candidate(tmp_path: Path) -> None:
    store = ResultStore(tmp_path)
    baseline = EvalResult(
        task="mmlu",
        model="base",
        accuracy=0.6,
        num_samples=10,
        num_fewshot=5,
        timestamp="2026-04-08T00:00:00Z",
        lm_eval_version="0.4.3",
        backend="vllm",
        metrics={"mmlu": 0.6},
    )
    candidate = EvalResult(
        task="mmlu",
        model="candidate",
        accuracy=0.5,
        num_samples=10,
        num_fewshot=5,
        timestamp="2026-04-08T00:01:00Z",
        lm_eval_version="0.4.3",
        backend="vllm",
        metrics={"mmlu": 0.5},
    )

    diff = store.build_comparison(baseline, candidate, min_delta=0.02)

    assert diff["summary"]["verdict"] == "regressed"
    assert diff["summary"]["release_recommendation"] == "block"
    assert "regressed" in diff["summary"]["release_reasons"][0]


def test_compare_report_reviews_changed_eval_settings(tmp_path: Path) -> None:
    store = ResultStore(tmp_path)
    baseline = EvalResult(
        task="mmlu",
        model="base",
        accuracy=0.5,
        num_samples=10,
        num_fewshot=5,
        timestamp="2026-04-08T00:00:00Z",
        lm_eval_version="0.4.3",
        backend="vllm",
        metrics={"mmlu": 0.5},
    )
    candidate = EvalResult(
        task="mmlu",
        model="candidate",
        accuracy=0.7,
        num_samples=5,
        num_fewshot=0,
        timestamp="2026-04-08T00:01:00Z",
        lm_eval_version="0.4.3",
        backend="vllm",
        metrics={"mmlu": 0.7},
    )

    diff = store.build_comparison(baseline, candidate, min_delta=0.02)

    assert diff["summary"]["verdict"] == "improved"
    assert diff["summary"]["release_recommendation"] == "review"
    assert diff["summary"]["fewshot_changed"] is True
    assert diff["summary"]["sample_count_changed"] is True


def test_compare_report_rejects_different_tasks(tmp_path: Path) -> None:
    store = ResultStore(tmp_path)
    baseline = EvalResult(
        task="mmlu",
        model="base",
        accuracy=0.5,
        num_samples=10,
        num_fewshot=5,
        timestamp="2026-04-08T00:00:00Z",
        lm_eval_version="0.4.3",
        backend="vllm",
        metrics={"mmlu": 0.5},
    )
    candidate = EvalResult(
        task="gsm8k",
        model="candidate",
        accuracy=0.6,
        num_samples=10,
        num_fewshot=5,
        timestamp="2026-04-08T00:01:00Z",
        lm_eval_version="0.4.3",
        backend="vllm",
        metrics={"gsm8k": 0.6},
    )

    with pytest.raises(ValueError, match="Cannot compare different tasks"):
        store.build_comparison(baseline, candidate)


def test_compare_markdown_handles_metric_added_or_removed(tmp_path: Path) -> None:
    store = ResultStore(tmp_path)
    report = {
        "task": "mmlu",
        "baseline": {"model": "base", "backend": "vllm", "accuracy": 0.5},
        "candidate": {"model": "candidate", "backend": "vllm", "accuracy": 0.6},
        "summary": {"verdict": "improved", "delta": 0.1, "absolute_gain": 0.1},
        "metric_deltas": {
            "new_metric": {"baseline": None, "candidate": 0.6, "delta": 0.6},
            "old_metric": {"baseline": 0.4, "candidate": None, "delta": -0.4},
        },
    }
    markdown = store.render_comparison_markdown(report)
    assert "baseline=n/a" in markdown
    assert "candidate=n/a" in markdown
