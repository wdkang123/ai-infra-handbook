from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from eval_module.runners.lm_eval_runner import EvalResult


class ResultStore:
    def __init__(self, output_dir: str | Path = "./results") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(self, result: EvalResult, path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result.to_dict(), indent=2))
        return target

    def load(self, path: str | Path) -> EvalResult:
        payload = json.loads(Path(path).read_text())
        return EvalResult(**payload)

    def build_comparison(
        self,
        baseline: EvalResult,
        candidate: EvalResult,
        *,
        min_delta: float = 0.0,
    ) -> dict[str, Any]:
        if min_delta < 0:
            raise ValueError("min_delta must be greater than or equal to 0")
        if baseline.task != candidate.task:
            raise ValueError(f"Cannot compare different tasks: baseline={baseline.task}, candidate={candidate.task}")
        delta = candidate.accuracy - baseline.accuracy
        task_metrics = sorted(set(baseline.metrics) | set(candidate.metrics))
        metric_deltas = {
            metric: {
                "baseline": baseline.metrics.get(metric),
                "candidate": candidate.metrics.get(metric),
                "delta": (candidate.metrics.get(metric, 0.0) - baseline.metrics.get(metric, 0.0)),
            }
            for metric in task_metrics
        }
        verdict = self._comparison_verdict(delta, min_delta)
        recommendation = self._release_recommendation(
            verdict=verdict,
            baseline=baseline,
            candidate=candidate,
        )
        return {
            "report_type": "eval_comparison",
            "task": candidate.task,
            "baseline": {
                "model": baseline.model,
                "backend": baseline.backend,
                "accuracy": baseline.accuracy,
                "num_samples": baseline.num_samples,
                "timestamp": baseline.timestamp,
                "path_hint": f"{baseline.task}:{baseline.model}",
            },
            "candidate": {
                "model": candidate.model,
                "backend": candidate.backend,
                "accuracy": candidate.accuracy,
                "num_samples": candidate.num_samples,
                "timestamp": candidate.timestamp,
                "path_hint": f"{candidate.task}:{candidate.model}",
            },
            "summary": {
                "delta": delta,
                "absolute_gain": abs(delta),
                "min_delta": min_delta,
                "verdict": verdict,
                "release_recommendation": recommendation["decision"],
                "release_reasons": recommendation["reasons"],
                "fewshot_changed": baseline.num_fewshot != candidate.num_fewshot,
                "sample_count_changed": baseline.num_samples != candidate.num_samples,
            },
            "metric_deltas": metric_deltas,
        }

    def render_comparison_markdown(self, report: dict[str, Any]) -> str:
        lines = [
            "# Evaluation Comparison Report",
            "",
            f"- Task: `{report['task']}`",
            f"- Verdict: `{report['summary']['verdict']}`",
            f"- Release recommendation: `{report['summary'].get('release_recommendation', 'review')}`",
            f"- Delta: `{report['summary']['delta']:.4f}`",
            f"- Absolute gain: `{report['summary']['absolute_gain']:.4f}`",
            f"- Min delta: `{report['summary'].get('min_delta', 0.0):.4f}`",
            "",
            "## Recommendation Reasons",
            "",
        ]
        for reason in report["summary"].get("release_reasons", []):
            lines.append(f"- {reason}")
        lines.extend(
            [
                "",
                "## Baseline",
                "",
                f"- Model: `{report['baseline']['model']}`",
                f"- Backend: `{report['baseline']['backend']}`",
                f"- Accuracy: `{report['baseline']['accuracy']:.4f}`",
                "",
                "## Candidate",
                "",
                f"- Model: `{report['candidate']['model']}`",
                f"- Backend: `{report['candidate']['backend']}`",
                f"- Accuracy: `{report['candidate']['accuracy']:.4f}`",
                "",
                "## Metric Deltas",
                "",
            ]
        )
        for metric, payload in report["metric_deltas"].items():
            lines.append(
                "- "
                f"`{metric}`: "
                f"baseline={self._format_metric_value(payload['baseline'])}, "
                f"candidate={self._format_metric_value(payload['candidate'])}, "
                f"delta={self._format_metric_value(payload['delta'])}"
            )
        return "\n".join(lines) + "\n"

    def render_result_markdown(self, result: EvalResult) -> str:
        lines = [
            "# Evaluation Run Summary",
            "",
            f"- Task: `{result.task}`",
            f"- Model: `{result.model}`",
            f"- Backend: `{result.backend}`",
            f"- Accuracy: `{result.accuracy:.4f}`",
            f"- Samples: `{result.num_samples}`",
            f"- Few-shot: `{result.num_fewshot}`",
            f"- Timestamp: `{result.timestamp}`",
            "",
            "## Metrics",
            "",
        ]
        for metric, value in result.metrics.items():
            lines.append(f"- `{metric}`: `{value:.4f}`")
        sample_summary = self._summarize_sample_outputs(result.sample_outputs)
        sample_analysis = self._analyze_sample_outputs(result.sample_outputs)
        lines.extend(
            [
                "",
                "## Sample Summary",
                "",
                f"- Sample outputs: `{sample_summary['sample_count']}`",
                f"- Passed samples: `{sample_summary['passed_count']}`",
                f"- Failed samples: `{sample_summary['failed_count']}`",
                f"- Average sample score: `{sample_summary['average_score']:.4f}`",
                f"- Pass rate: `{sample_analysis['pass_rate']:.4f}`",
                f"- Min score: `{self._format_optional_float(sample_analysis['min_score'])}`",
                f"- Max score: `{self._format_optional_float(sample_analysis['max_score'])}`",
                f"- Judge reasons: `{sample_analysis['judge_reason_counts']}`",
            ]
        )
        if sample_analysis["failed_sample_ids"]:
            lines.append(f"- Failed sample ids: `{', '.join(sample_analysis['failed_sample_ids'])}`")
        return "\n".join(lines) + "\n"

    def save_run_bundle(self, result: EvalResult, path: str | Path) -> dict[str, Path]:
        target = Path(path)
        artifact_dir = target.with_suffix("")
        artifact_dir.mkdir(parents=True, exist_ok=True)

        result_path = artifact_dir / "result.json"
        raw_output_path = artifact_dir / "raw_output.json"
        sample_outputs_path = artifact_dir / "sample_outputs.json"
        sample_summary_path = artifact_dir / "sample_summary.json"
        sample_analysis_path = artifact_dir / "sample_analysis.json"
        manifest_path = artifact_dir / "run_manifest.json"
        summary_path = artifact_dir / "summary.md"
        sample_summary = self._summarize_sample_outputs(result.sample_outputs)
        sample_analysis = self._analyze_sample_outputs(result.sample_outputs)

        result_path.write_text(json.dumps(result.to_dict(), indent=2))
        raw_output_path.write_text(json.dumps(result.raw_output or {}, indent=2))
        sample_outputs_path.write_text(json.dumps(result.sample_outputs, indent=2))
        sample_summary_path.write_text(json.dumps(sample_summary, indent=2))
        sample_analysis_path.write_text(json.dumps(sample_analysis, indent=2))
        manifest_path.write_text(
            json.dumps(
                {
                    "artifact_type": "eval_run_bundle",
                    "task": result.task,
                    "model": result.model,
                    "backend": result.backend,
                    "result_file": result_path.name,
                    "raw_output_file": raw_output_path.name,
                    "sample_outputs_file": sample_outputs_path.name,
                    "sample_summary_file": sample_summary_path.name,
                    "sample_analysis_file": sample_analysis_path.name,
                    "sample_output_count": len(result.sample_outputs),
                    "summary_file": summary_path.name,
                },
                indent=2,
            )
        )
        summary_path.write_text(self.render_result_markdown(result))
        self._append_jsonl(
            self.output_dir / "run_history.jsonl",
            {
                "task": result.task,
                "model": result.model,
                "backend": result.backend,
                "artifact_dir": str(artifact_dir),
                "result_file": str(result_path),
                "timestamp": result.timestamp,
            },
        )
        return {
            "artifact_dir": artifact_dir,
            "result": result_path,
            "raw_output": raw_output_path,
            "sample_outputs": sample_outputs_path,
            "sample_summary": sample_summary_path,
            "sample_analysis": sample_analysis_path,
            "manifest": manifest_path,
            "summary": summary_path,
        }

    def save_comparison(self, diff: dict[str, Any], path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(diff, indent=2))
        return target

    def save_comparison_markdown(self, report: dict[str, Any], path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.render_comparison_markdown(report))
        return target

    def save_comparison_bundle(self, report: dict[str, Any], path: str | Path) -> dict[str, Path]:
        target = Path(path)
        artifact_dir = target.with_suffix("")
        artifact_dir.mkdir(parents=True, exist_ok=True)

        json_path = artifact_dir / "comparison.json"
        markdown_path = artifact_dir / "comparison.md"
        manifest_path = artifact_dir / "comparison_manifest.json"

        json_path.write_text(json.dumps(report, indent=2))
        markdown_path.write_text(self.render_comparison_markdown(report))
        manifest_path.write_text(
            json.dumps(
                {
                    "artifact_type": "eval_comparison_bundle",
                    "task": report["task"],
                    "json_file": json_path.name,
                    "markdown_file": markdown_path.name,
                    "verdict": report["summary"]["verdict"],
                    "release_recommendation": report["summary"].get("release_recommendation", "review"),
                    "min_delta": report["summary"].get("min_delta", 0.0),
                },
                indent=2,
            )
        )
        self._append_jsonl(
            self.output_dir / "comparison_history.jsonl",
            {
                "task": report["task"],
                "artifact_dir": str(artifact_dir),
                "comparison_file": str(json_path),
                "baseline_model": report["baseline"]["model"],
                "baseline_accuracy": report["baseline"]["accuracy"],
                "candidate_model": report["candidate"]["model"],
                "candidate_accuracy": report["candidate"]["accuracy"],
                "candidate_timestamp": report["candidate"]["timestamp"],
                "verdict": report["summary"]["verdict"],
                "release_recommendation": report["summary"].get("release_recommendation", "review"),
                "delta": report["summary"]["delta"],
                "min_delta": report["summary"].get("min_delta", 0.0),
            },
        )
        return {
            "artifact_dir": artifact_dir,
            "json": json_path,
            "markdown": markdown_path,
            "manifest": manifest_path,
        }

    def build_run_index(
        self,
        *,
        history_path: str | Path | None = None,
        task: str | None = None,
        model: str | None = None,
        backend: str | None = None,
        num_fewshot: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        source_history = Path(history_path) if history_path else self.output_dir / "run_history.jsonl"
        runs: list[dict[str, Any]] = []
        skipped_entries: list[dict[str, Any]] = []

        if source_history.exists():
            for line_number, line in enumerate(source_history.read_text().splitlines(), start=1):
                if not line.strip():
                    continue
                try:
                    history_entry = json.loads(line)
                except json.JSONDecodeError:
                    skipped_entries.append({"line": line_number, "reason": "invalid json"})
                    continue

                result_file = history_entry.get("result_file")
                if not result_file:
                    skipped_entries.append({"line": line_number, "reason": "missing result_file"})
                    continue

                result_path = self._resolve_history_result_path(result_file, source_history)
                if not result_path.exists():
                    skipped_entries.append(
                        {
                            "line": line_number,
                            "reason": "missing result_file",
                            "result_file": str(result_path),
                        }
                    )
                    continue

                try:
                    result = self.load(result_path)
                except (TypeError, json.JSONDecodeError):
                    skipped_entries.append(
                        {
                            "line": line_number,
                            "reason": "invalid result payload",
                            "result_file": str(result_path),
                        }
                    )
                    continue

                if task and result.task != task:
                    continue
                if model and result.model != model:
                    continue
                if backend and result.backend != backend:
                    continue
                if num_fewshot is not None and result.num_fewshot != num_fewshot:
                    continue

                runs.append(
                    {
                        "task": result.task,
                        "model": result.model,
                        "backend": result.backend,
                        "accuracy": result.accuracy,
                        "num_samples": result.num_samples,
                        "num_fewshot": result.num_fewshot,
                        "timestamp": result.timestamp,
                        "artifact_dir": history_entry.get("artifact_dir", str(result_path.parent)),
                        "result_file": str(result_path),
                        "sample_summary": self._summarize_sample_outputs(result.sample_outputs),
                        "sample_analysis": self._analyze_sample_outputs(result.sample_outputs),
                    }
                )

        runs.sort(key=lambda item: (item["timestamp"], item["task"], item["model"]), reverse=True)
        matched_run_count = len(runs)
        if limit is not None:
            runs = runs[:limit]

        return {
            "report_type": "eval_run_index",
            "source_history": str(source_history),
            "task_filter": task,
            "model_filter": model,
            "backend_filter": backend,
            "num_fewshot_filter": num_fewshot,
            "run_count": len(runs),
            "matched_run_count": matched_run_count,
            "task_count": len({run["task"] for run in runs}),
            "model_count": len({run["model"] for run in runs}),
            "backend_count": len({run["backend"] for run in runs}),
            "fewshot_count": len({run["num_fewshot"] for run in runs}),
            "task_summaries": self._summarize_run_tasks(runs),
            "skipped_entries": skipped_entries,
            "runs": runs,
        }

    def render_run_index_markdown(self, report: dict[str, Any]) -> str:
        lines = [
            "# Evaluation Run Index",
            "",
            f"- Source history: `{report['source_history']}`",
            f"- Runs: `{report['run_count']}`",
            f"- Matched runs: `{report.get('matched_run_count', report['run_count'])}`",
            f"- Tasks: `{report['task_count']}`",
            f"- Models: `{report['model_count']}`",
        ]
        if report.get("task_filter"):
            lines.append(f"- Task filter: `{report['task_filter']}`")
        if report.get("model_filter"):
            lines.append(f"- Model filter: `{report['model_filter']}`")
        if report.get("backend_filter"):
            lines.append(f"- Backend filter: `{report['backend_filter']}`")
        if report.get("num_fewshot_filter") is not None:
            lines.append(f"- Few-shot filter: `{report['num_fewshot_filter']}`")
        if report.get("skipped_entries"):
            lines.append(f"- Skipped entries: `{len(report['skipped_entries'])}`")
        if not report["runs"]:
            lines.extend(["", "No evaluation runs found."])
            return "\n".join(lines) + "\n"

        if report.get("task_summaries"):
            lines.extend(
                [
                    "",
                    "## Task Summaries",
                    "",
                    "| Task | Runs | Models | Backends | Few-shot Settings | Best Accuracy | Latest Accuracy | Latest Result File |",
                    "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
                ]
            )
            for summary in report["task_summaries"]:
                lines.append(
                    "| "
                    f"{self._markdown_table_cell(summary['task'])} | "
                    f"{summary['run_count']} | "
                    f"{summary['model_count']} | "
                    f"{summary['backend_count']} | "
                    f"{summary['fewshot_count']} | "
                    f"{summary['best_accuracy']:.4f} | "
                    f"{summary['latest_accuracy']:.4f} | "
                    f"{self._markdown_table_cell(summary['latest_result_file'])} |"
                )

        lines.extend(
            [
                "",
                "| Timestamp | Task | Model | Accuracy | Samples | Few-shot | Backend | Result File |",
                "| --- | --- | --- | ---: | ---: | ---: | --- | --- |",
            ]
        )
        for run in report["runs"]:
            lines.append(
                "| "
                f"{self._markdown_table_cell(run['timestamp'])} | "
                f"{self._markdown_table_cell(run['task'])} | "
                f"{self._markdown_table_cell(run['model'])} | "
                f"{run['accuracy']:.4f} | "
                f"{run['num_samples']} | "
                f"{run['num_fewshot']} | "
                f"{self._markdown_table_cell(run['backend'])} | "
                f"{self._markdown_table_cell(run['result_file'])} |"
            )
        return "\n".join(lines) + "\n"

    def save_run_index(self, report: dict[str, Any], path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2))
        return target

    def save_run_index_markdown(self, report: dict[str, Any], path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.render_run_index_markdown(report))
        return target

    def build_comparison_index(
        self,
        *,
        history_path: str | Path | None = None,
        task: str | None = None,
        verdict: str | None = None,
        recommendation: str | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        source_history = Path(history_path) if history_path else self.output_dir / "comparison_history.jsonl"
        comparisons: list[dict[str, Any]] = []
        skipped_entries: list[dict[str, Any]] = []

        if source_history.exists():
            for line_number, line in enumerate(source_history.read_text().splitlines(), start=1):
                if not line.strip():
                    continue
                try:
                    history_entry = json.loads(line)
                except json.JSONDecodeError:
                    skipped_entries.append({"line": line_number, "reason": "invalid json"})
                    continue

                comparison = self._comparison_index_entry(history_entry, source_history)
                if task and comparison["task"] != task:
                    continue
                if verdict and comparison["verdict"] != verdict:
                    continue
                if recommendation and comparison["release_recommendation"] != recommendation:
                    continue
                comparisons.append(comparison)

        comparisons.sort(
            key=lambda item: (item["candidate_timestamp"], item["task"], item["candidate_model"]),
            reverse=True,
        )
        matched_comparison_count = len(comparisons)
        if limit is not None:
            comparisons = comparisons[:limit]
        deltas = [float(comparison["delta"]) for comparison in comparisons]

        return {
            "report_type": "eval_comparison_index",
            "source_history": str(source_history),
            "task_filter": task,
            "verdict_filter": verdict,
            "recommendation_filter": recommendation,
            "comparison_count": len(comparisons),
            "matched_comparison_count": matched_comparison_count,
            "task_count": len({comparison["task"] for comparison in comparisons}),
            "verdict_counts": self._count_entries(comparisons, "verdict"),
            "recommendation_counts": self._count_entries(comparisons, "release_recommendation"),
            "average_delta": round(sum(deltas) / len(deltas), 6) if deltas else None,
            "max_delta": round(max(deltas), 6) if deltas else None,
            "min_delta_seen": round(min(deltas), 6) if deltas else None,
            "task_summaries": self._summarize_comparison_tasks(comparisons),
            "skipped_entries": skipped_entries,
            "comparisons": comparisons,
        }

    def render_comparison_index_markdown(self, report: dict[str, Any]) -> str:
        lines = [
            "# Evaluation Comparison Index",
            "",
            f"- Source history: `{report['source_history']}`",
            f"- Comparisons: `{report['comparison_count']}`",
            f"- Matched comparisons: `{report.get('matched_comparison_count', report['comparison_count'])}`",
            f"- Tasks: `{report['task_count']}`",
        ]
        if report.get("task_filter"):
            lines.append(f"- Task filter: `{report['task_filter']}`")
        if report.get("verdict_filter"):
            lines.append(f"- Verdict filter: `{report['verdict_filter']}`")
        if report.get("recommendation_filter"):
            lines.append(f"- Recommendation filter: `{report['recommendation_filter']}`")
        lines.append(f"- Verdict counts: `{report.get('verdict_counts', {})}`")
        lines.append(f"- Recommendation counts: `{report.get('recommendation_counts', {})}`")
        lines.append(f"- Average delta: `{report.get('average_delta')}`")
        if report.get("skipped_entries"):
            lines.append(f"- Skipped entries: `{len(report['skipped_entries'])}`")
        if not report["comparisons"]:
            lines.extend(["", "No evaluation comparisons found."])
            return "\n".join(lines) + "\n"

        if report.get("task_summaries"):
            lines.extend(
                [
                    "",
                    "## Task Summaries",
                    "",
                    "| Task | Comparisons | Average Delta | Verdict Counts | Recommendation Counts | Latest Comparison File |",
                    "| --- | ---: | ---: | --- | --- | --- |",
                ]
            )
            for summary in report["task_summaries"]:
                lines.append(
                    "| "
                    f"{self._markdown_table_cell(summary['task'])} | "
                    f"{summary['comparison_count']} | "
                    f"{self._format_optional_float(summary['average_delta'])} | "
                    f"{self._markdown_table_cell(summary['verdict_counts'])} | "
                    f"{self._markdown_table_cell(summary['recommendation_counts'])} | "
                    f"{self._markdown_table_cell(summary['latest_comparison_file'])} |"
                )

        lines.extend(
            [
                "",
                "| Task | Baseline | Candidate | Delta | Verdict | Release | Comparison File |",
                "| --- | --- | --- | ---: | --- | --- | --- |",
            ]
        )
        for comparison in report["comparisons"]:
            lines.append(
                "| "
                f"{self._markdown_table_cell(comparison['task'])} | "
                f"{self._markdown_table_cell(comparison['baseline_model'])} "
                f"({comparison['baseline_accuracy']:.4f}) | "
                f"{self._markdown_table_cell(comparison['candidate_model'])} "
                f"({comparison['candidate_accuracy']:.4f}) | "
                f"{comparison['delta']:.4f} | "
                f"{self._markdown_table_cell(comparison['verdict'])} | "
                f"{self._markdown_table_cell(comparison['release_recommendation'])} | "
                f"{self._markdown_table_cell(comparison['comparison_file'])} |"
            )
        return "\n".join(lines) + "\n"

    def save_comparison_index(self, report: dict[str, Any], path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2))
        return target

    def save_comparison_index_markdown(self, report: dict[str, Any], path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.render_comparison_index_markdown(report))
        return target

    def build_leaderboard(
        self,
        *,
        history_path: str | Path | None = None,
        task: str | None = None,
        backend: str | None = None,
        num_fewshot: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        source_history = Path(history_path) if history_path else self.output_dir / "run_history.jsonl"
        entries_by_model: dict[tuple[str, str, str, int], dict[str, Any]] = {}
        skipped_entries: list[dict[str, Any]] = []
        loaded_run_count = 0

        if source_history.exists():
            for line_number, line in enumerate(source_history.read_text().splitlines(), start=1):
                if not line.strip():
                    continue
                try:
                    history_entry = json.loads(line)
                except json.JSONDecodeError:
                    skipped_entries.append({"line": line_number, "reason": "invalid json"})
                    continue

                result_file = history_entry.get("result_file")
                if not result_file:
                    skipped_entries.append({"line": line_number, "reason": "missing result_file"})
                    continue

                result_path = self._resolve_history_result_path(result_file, source_history)
                if not result_path.exists():
                    skipped_entries.append(
                        {
                            "line": line_number,
                            "reason": "missing result_file",
                            "result_file": str(result_path),
                        }
                    )
                    continue

                try:
                    result = self.load(result_path)
                except (TypeError, json.JSONDecodeError):
                    skipped_entries.append(
                        {
                            "line": line_number,
                            "reason": "invalid result payload",
                            "result_file": str(result_path),
                        }
                    )
                    continue

                if task and result.task != task:
                    continue
                if backend and result.backend != backend:
                    continue
                if num_fewshot is not None and result.num_fewshot != num_fewshot:
                    continue

                loaded_run_count += 1
                key = (result.task, result.model, result.backend, result.num_fewshot)
                sample_summary = self._summarize_sample_outputs(result.sample_outputs)
                entry = entries_by_model.setdefault(
                    key,
                    {
                        "task": result.task,
                        "model": result.model,
                        "backend": result.backend,
                        "run_count": 0,
                        "best_accuracy": result.accuracy,
                        "best_timestamp": result.timestamp,
                        "best_result_file": str(result_path),
                        "latest_accuracy": result.accuracy,
                        "latest_timestamp": result.timestamp,
                        "latest_result_file": str(result_path),
                        "num_samples": result.num_samples,
                        "num_fewshot": result.num_fewshot,
                        "sample_summary": sample_summary,
                    },
                )
                entry["run_count"] += 1
                entry["latest_accuracy"] = result.accuracy
                entry["latest_timestamp"] = result.timestamp
                entry["latest_result_file"] = str(result_path)
                if self._is_better_leaderboard_run(result, entry):
                    entry["best_accuracy"] = result.accuracy
                    entry["best_timestamp"] = result.timestamp
                    entry["best_result_file"] = str(result_path)
                    entry["backend"] = result.backend
                    entry["num_samples"] = result.num_samples
                    entry["num_fewshot"] = result.num_fewshot
                    entry["sample_summary"] = sample_summary

        entries = sorted(
            entries_by_model.values(),
            key=lambda item: (item["task"], -item["best_accuracy"], item["model"]),
        )
        if limit is not None:
            entries = entries[:limit]

        ranked_tasks: dict[str, list[dict[str, Any]]] = {}
        for entry in entries:
            task_entries = ranked_tasks.setdefault(entry["task"], [])
            task_entries.append({"rank": len(task_entries) + 1, **entry})

        ranked_entries = [entry for task_entries in ranked_tasks.values() for entry in task_entries]
        backend_groups = self._group_leaderboard_entries(ranked_entries, "backend")
        fewshot_groups = self._group_leaderboard_entries(ranked_entries, "num_fewshot")
        return {
            "report_type": "eval_leaderboard",
            "source_history": str(source_history),
            "task_filter": task,
            "backend_filter": backend,
            "num_fewshot_filter": num_fewshot,
            "run_count": loaded_run_count,
            "model_count": len(ranked_entries),
            "entry_count": len(ranked_entries),
            "backend_count": len(backend_groups),
            "fewshot_count": len(fewshot_groups),
            "skipped_entries": skipped_entries,
            "entries": ranked_entries,
            "tasks": ranked_tasks,
            "backend_groups": backend_groups,
            "fewshot_groups": fewshot_groups,
        }

    def render_leaderboard_markdown(self, report: dict[str, Any]) -> str:
        lines = [
            "# Evaluation Leaderboard",
            "",
            f"- Source history: `{report['source_history']}`",
            f"- Runs loaded: `{report['run_count']}`",
            f"- Models: `{report['model_count']}`",
        ]
        if report.get("task_filter"):
            lines.append(f"- Task filter: `{report['task_filter']}`")
        if report.get("backend_filter"):
            lines.append(f"- Backend filter: `{report['backend_filter']}`")
        if report.get("num_fewshot_filter") is not None:
            lines.append(f"- Few-shot filter: `{report['num_fewshot_filter']}`")
        if report.get("skipped_entries"):
            lines.append(f"- Skipped entries: `{len(report['skipped_entries'])}`")
        if not report["entries"]:
            lines.extend(["", "No evaluation runs found."])
            return "\n".join(lines) + "\n"

        for task, entries in report["tasks"].items():
            lines.extend(
                [
                    "",
                    f"## {task}",
                    "",
                    "| Rank | Model | Best Accuracy | Latest Accuracy | Runs | Samples | Few-shot | Backend |",
                    "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
                ]
            )
            for entry in entries:
                lines.append(
                    "| "
                    f"{entry['rank']} | "
                    f"{self._markdown_table_cell(entry['model'])} | "
                    f"{entry['best_accuracy']:.4f} | "
                    f"{entry['latest_accuracy']:.4f} | "
                    f"{entry['run_count']} | "
                    f"{entry['num_samples']} | "
                    f"{entry['num_fewshot']} | "
                    f"{self._markdown_table_cell(entry['backend'])} |"
                )
            lines.extend(
                [
                    "",
                    "| Rank | Best Result File | Latest Result File |",
                    "| --- | --- | --- |",
                ]
            )
            for entry in entries:
                lines.append(
                    "| "
                    f"{entry['rank']} | "
                    f"{self._markdown_table_cell(entry['best_result_file'])} | "
                    f"{self._markdown_table_cell(entry['latest_result_file'])} |"
                )
        lines.extend(self._render_leaderboard_group_markdown("Backend Views", report.get("backend_groups", {}), "backend"))
        lines.extend(
            self._render_leaderboard_group_markdown("Few-shot Views", report.get("fewshot_groups", {}), "num_fewshot")
        )
        return "\n".join(lines) + "\n"

    def save_leaderboard(self, report: dict[str, Any], path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2))
        return target

    def save_leaderboard_markdown(self, report: dict[str, Any], path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.render_leaderboard_markdown(report))
        return target

    def _append_jsonl(self, path: Path, payload: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload) + "\n")

    @staticmethod
    def _format_metric_value(value: float | None) -> str:
        if value is None:
            return "n/a"
        return f"{value:.4f}"

    @staticmethod
    def _resolve_history_result_path(result_file: str, history_path: Path) -> Path:
        result_path = Path(result_file)
        if result_path.is_absolute() or result_path.exists():
            return result_path
        return history_path.parent / result_path

    def _comparison_index_entry(self, history_entry: dict[str, Any], history_path: Path) -> dict[str, Any]:
        comparison_file = history_entry.get("comparison_file")
        artifact_dir = history_entry.get("artifact_dir", "")
        if not comparison_file and artifact_dir:
            comparison_file = str(Path(artifact_dir) / "comparison.json")
        comparison_path = self._resolve_history_result_path(comparison_file, history_path) if comparison_file else None
        comparison_payload: dict[str, Any] = {}
        if comparison_path and comparison_path.exists():
            try:
                comparison_payload = json.loads(comparison_path.read_text())
            except json.JSONDecodeError:
                comparison_payload = {}

        baseline = comparison_payload.get("baseline", {})
        candidate = comparison_payload.get("candidate", {})
        summary = comparison_payload.get("summary", {})
        return {
            "task": history_entry.get("task") or comparison_payload.get("task", ""),
            "artifact_dir": artifact_dir,
            "comparison_file": str(comparison_path) if comparison_path else "",
            "baseline_model": history_entry.get("baseline_model") or baseline.get("model", ""),
            "baseline_accuracy": history_entry.get("baseline_accuracy", baseline.get("accuracy", 0.0)),
            "candidate_model": history_entry.get("candidate_model") or candidate.get("model", ""),
            "candidate_accuracy": history_entry.get("candidate_accuracy", candidate.get("accuracy", 0.0)),
            "candidate_timestamp": history_entry.get("candidate_timestamp") or candidate.get("timestamp", ""),
            "verdict": history_entry.get("verdict") or summary.get("verdict", ""),
            "release_recommendation": history_entry.get("release_recommendation")
            or summary.get("release_recommendation", "review"),
            "delta": history_entry.get("delta", summary.get("delta", 0.0)),
            "min_delta": history_entry.get("min_delta", summary.get("min_delta", 0.0)),
        }

    @staticmethod
    def _count_entries(entries: list[dict[str, Any]], field: str) -> dict[str, int]:
        counts: dict[str, int] = {}
        for entry in entries:
            value = entry.get(field)
            if value is None:
                continue
            key = str(value)
            counts[key] = counts.get(key, 0) + 1
        return counts

    def _summarize_comparison_tasks(self, comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
        groups: dict[str, list[dict[str, Any]]] = {}
        for comparison in comparisons:
            groups.setdefault(str(comparison.get("task", "")), []).append(comparison)

        summaries = []
        for task, entries in sorted(groups.items()):
            deltas = [float(entry["delta"]) for entry in entries]
            latest_entry = entries[0]
            summaries.append(
                {
                    "task": task,
                    "comparison_count": len(entries),
                    "verdict_counts": self._count_entries(entries, "verdict"),
                    "recommendation_counts": self._count_entries(entries, "release_recommendation"),
                    "average_delta": round(sum(deltas) / len(deltas), 6) if deltas else None,
                    "max_delta": round(max(deltas), 6) if deltas else None,
                    "min_delta_seen": round(min(deltas), 6) if deltas else None,
                    "latest_candidate_model": latest_entry.get("candidate_model", ""),
                    "latest_comparison_file": latest_entry.get("comparison_file", ""),
                }
            )
        return summaries

    @staticmethod
    def _summarize_run_tasks(runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
        groups: dict[str, list[dict[str, Any]]] = {}
        for run in runs:
            groups.setdefault(str(run.get("task", "")), []).append(run)

        summaries = []
        for task, entries in sorted(groups.items()):
            best_entry = max(entries, key=lambda entry: (entry["accuracy"], entry["timestamp"]))
            latest_entry = max(entries, key=lambda entry: entry["timestamp"])
            summaries.append(
                {
                    "task": task,
                    "run_count": len(entries),
                    "model_count": len({entry["model"] for entry in entries}),
                    "backend_count": len({entry["backend"] for entry in entries}),
                    "fewshot_count": len({entry["num_fewshot"] for entry in entries}),
                    "best_accuracy": best_entry["accuracy"],
                    "best_model": best_entry["model"],
                    "best_result_file": best_entry["result_file"],
                    "latest_accuracy": latest_entry["accuracy"],
                    "latest_model": latest_entry["model"],
                    "latest_result_file": latest_entry["result_file"],
                }
            )
        return summaries

    @staticmethod
    def _group_leaderboard_entries(entries: list[dict[str, Any]], field: str) -> dict[str, list[dict[str, Any]]]:
        groups: dict[str, list[dict[str, Any]]] = {}
        for entry in entries:
            group_key = str(entry.get(field, ""))
            group_entries = groups.setdefault(group_key, [])
            group_entries.append(
                {
                    "rank": len(group_entries) + 1,
                    "task": entry["task"],
                    "model": entry["model"],
                    "backend": entry["backend"],
                    "num_fewshot": entry["num_fewshot"],
                    "best_accuracy": entry["best_accuracy"],
                    "latest_accuracy": entry["latest_accuracy"],
                    "run_count": entry["run_count"],
                }
            )
        return groups

    def _render_leaderboard_group_markdown(
        self,
        title: str,
        groups: dict[str, list[dict[str, Any]]],
        group_field: str,
    ) -> list[str]:
        if not groups:
            return []

        lines = ["", f"## {title}"]
        for group_value, entries in sorted(groups.items()):
            lines.extend(
                [
                    "",
                    f"### {group_field}: {group_value}",
                    "",
                    "| Rank | Task | Model | Backend | Few-shot | Best Accuracy | Latest Accuracy | Runs |",
                    "| --- | --- | --- | --- | ---: | ---: | ---: | ---: |",
                ]
            )
            for entry in entries:
                lines.append(
                    "| "
                    f"{entry['rank']} | "
                    f"{self._markdown_table_cell(entry['task'])} | "
                    f"{self._markdown_table_cell(entry['model'])} | "
                    f"{self._markdown_table_cell(entry['backend'])} | "
                    f"{entry['num_fewshot']} | "
                    f"{entry['best_accuracy']:.4f} | "
                    f"{entry['latest_accuracy']:.4f} | "
                    f"{entry['run_count']} |"
                )
        return lines

    @staticmethod
    def _is_better_leaderboard_run(result: EvalResult, current_entry: dict[str, Any]) -> bool:
        return result.accuracy > current_entry["best_accuracy"] or (
            result.accuracy == current_entry["best_accuracy"] and result.timestamp > current_entry["best_timestamp"]
        )

    @staticmethod
    def _markdown_table_cell(value: Any) -> str:
        return str(value).replace("|", "\\|")

    @staticmethod
    def _format_optional_float(value: float | None) -> str:
        if value is None:
            return "n/a"
        return f"{value:.4f}"

    @staticmethod
    def _comparison_verdict(delta: float, min_delta: float) -> str:
        if delta > min_delta:
            return "improved"
        if delta < -min_delta:
            return "regressed"
        return "unchanged"

    @staticmethod
    def _summarize_sample_outputs(sample_outputs: list[dict[str, Any]]) -> dict[str, Any]:
        sample_count = len(sample_outputs)
        passed_count = sum(1 for sample in sample_outputs if sample.get("passed") is True)
        failed_count = sample_count - passed_count
        score_total = sum(float(sample.get("score", 0.0)) for sample in sample_outputs)
        prompt_tokens = sum(int(sample.get("prompt_tokens", 0)) for sample in sample_outputs)
        prediction_tokens = sum(int(sample.get("prediction_tokens", 0)) for sample in sample_outputs)
        return {
            "sample_count": sample_count,
            "passed_count": passed_count,
            "failed_count": failed_count,
            "average_score": round(score_total / sample_count, 4) if sample_count else 0.0,
            "prompt_tokens": prompt_tokens,
            "prediction_tokens": prediction_tokens,
        }

    @staticmethod
    def _analyze_sample_outputs(sample_outputs: list[dict[str, Any]]) -> dict[str, Any]:
        sample_count = len(sample_outputs)
        scores = [float(sample.get("score", 0.0)) for sample in sample_outputs]
        passed_count = sum(1 for sample in sample_outputs if sample.get("passed") is True)
        failed_samples = [sample for sample in sample_outputs if sample.get("passed") is not True]
        prompt_tokens = sum(int(sample.get("prompt_tokens", 0)) for sample in sample_outputs)
        prediction_tokens = sum(int(sample.get("prediction_tokens", 0)) for sample in sample_outputs)
        reason_counts: dict[str, int] = {}
        for sample in sample_outputs:
            reason = str(sample.get("judge_reason", ""))
            if not reason:
                continue
            reason_counts[reason] = reason_counts.get(reason, 0) + 1
        lowest_samples = sorted(
            sample_outputs,
            key=lambda sample: (float(sample.get("score", 0.0)), str(sample.get("sample_id", ""))),
        )[:3]
        return {
            "sample_count": sample_count,
            "pass_rate": round(passed_count / sample_count, 4) if sample_count else 0.0,
            "min_score": round(min(scores), 4) if scores else None,
            "max_score": round(max(scores), 4) if scores else None,
            "average_prompt_tokens": round(prompt_tokens / sample_count, 4) if sample_count else 0.0,
            "average_prediction_tokens": round(prediction_tokens / sample_count, 4) if sample_count else 0.0,
            "failed_sample_ids": [str(sample.get("sample_id", "")) for sample in failed_samples if sample.get("sample_id")],
            "judge_reason_counts": dict(sorted(reason_counts.items())),
            "score_buckets": {
                "low_lt_0_5": sum(1 for score in scores if score < 0.5),
                "mid_0_5_to_0_8": sum(1 for score in scores if 0.5 <= score < 0.8),
                "high_gte_0_8": sum(1 for score in scores if score >= 0.8),
            },
            "lowest_score_samples": [
                {
                    "sample_id": sample.get("sample_id", ""),
                    "score": float(sample.get("score", 0.0)),
                    "passed": sample.get("passed") is True,
                    "judge_reason": sample.get("judge_reason", ""),
                }
                for sample in lowest_samples
            ],
        }

    @staticmethod
    def _release_recommendation(
        *,
        verdict: str,
        baseline: EvalResult,
        candidate: EvalResult,
    ) -> dict[str, Any]:
        reasons: list[str] = []
        if baseline.num_fewshot != candidate.num_fewshot:
            reasons.append(
                f"Few-shot setting changed from {baseline.num_fewshot} to {candidate.num_fewshot}; review manually."
            )
        if baseline.num_samples != candidate.num_samples:
            reasons.append(
                f"Sample count changed from {baseline.num_samples} to {candidate.num_samples}; compare with caution."
            )

        if verdict == "regressed":
            reasons.insert(0, "Candidate regressed beyond the configured min_delta.")
            return {"decision": "block", "reasons": reasons}
        if reasons:
            return {"decision": "review", "reasons": reasons}
        if verdict == "improved":
            return {
                "decision": "approve",
                "reasons": ["Candidate improved beyond the configured min_delta with matching evaluation settings."],
            }
        return {
            "decision": "review",
            "reasons": ["Candidate is within the configured min_delta; treat as unchanged unless other evidence supports release."],
        }
