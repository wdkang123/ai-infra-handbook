from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_run_history_report(
    path: str | Path,
    *,
    dataset_id: str | None = None,
    model: str | None = None,
    method: str | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    history_path = Path(path)
    runs: list[dict[str, Any]] = []
    skipped_entries: list[dict[str, Any]] = []
    total_run_count = 0

    if history_path.exists():
        for line_number, line in enumerate(history_path.read_text().splitlines(), start=1):
            if not line.strip():
                continue
            total_run_count += 1
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                skipped_entries.append({"line": line_number, "reason": "invalid json"})
                continue
            if dataset_id and entry.get("dataset_id") != dataset_id:
                continue
            if model and entry.get("model") != model:
                continue
            if method and entry.get("method") != method:
                continue
            runs.append(_run_index_entry(entry))

    matched_run_count = len(runs)
    if limit is not None:
        runs = runs[-limit:]

    return {
        "report_type": "finetune_run_index",
        "source_history": str(history_path),
        "dataset_id_filter": dataset_id,
        "model_filter": model,
        "method_filter": method,
        "total_run_count": total_run_count,
        "matched_run_count": matched_run_count,
        "run_count": len(runs),
        "dataset_count": len({entry["dataset_id"] for entry in runs if entry.get("dataset_id")}),
        "model_count": len({entry["model"] for entry in runs if entry.get("model")}),
        "method_count": len({entry["method"] for entry in runs if entry.get("method")}),
        "method_counts": _count_entries(runs, "method"),
        "model_summaries": _summarize_run_groups(runs, "model"),
        "dataset_summaries": _summarize_run_groups(runs, "dataset_id"),
        "skipped_entries": skipped_entries,
        "runs": runs,
    }


def render_run_history_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Finetune Run Index",
        "",
        f"- Source history: `{report['source_history']}`",
        f"- Runs: `{report['run_count']}`",
        f"- Matched runs: `{report.get('matched_run_count', report['run_count'])}`",
        f"- Datasets: `{report['dataset_count']}`",
        f"- Models: `{report['model_count']}`",
        f"- Methods: `{report['method_count']}`",
        f"- Method counts: `{report.get('method_counts', {})}`",
    ]
    if report.get("dataset_id_filter"):
        lines.append(f"- Dataset filter: `{report['dataset_id_filter']}`")
    if report.get("model_filter"):
        lines.append(f"- Model filter: `{report['model_filter']}`")
    if report.get("method_filter"):
        lines.append(f"- Method filter: `{report['method_filter']}`")
    if report.get("skipped_entries"):
        lines.append(f"- Skipped entries: `{len(report['skipped_entries'])}`")
    if not report["runs"]:
        lines.extend(["", "No finetune runs found."])
        return "\n".join(lines) + "\n"

    lines.extend(_render_run_group_markdown("Model Summaries", report.get("model_summaries", []), "model"))
    lines.extend(_render_run_group_markdown("Dataset Summaries", report.get("dataset_summaries", []), "dataset_id"))
    lines.extend(
        [
            "",
            "## Runs",
            "",
            "| Method | Model | Dataset ID | Dataset Version | Output Dir | Checkpoint | Run Manifest | Checkpoint Index |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for entry in report["runs"]:
        lines.append(
            "| "
            f"{_markdown_table_cell(entry['method'])} | "
            f"{_markdown_table_cell(entry['model'])} | "
            f"{_markdown_table_cell(entry['dataset_id'])} | "
            f"{_markdown_table_cell(entry['dataset_version'])} | "
            f"{_markdown_table_cell(entry['output_dir'])} | "
            f"{_markdown_table_cell(entry['checkpoint'])} | "
            f"{_markdown_table_cell(entry['run_manifest_file'])} | "
            f"{_markdown_table_cell(entry['checkpoint_index_file'])} |"
        )
    return "\n".join(lines) + "\n"


def save_run_history_report(report: dict[str, Any], path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2))
    return target


def save_run_history_markdown(report: dict[str, Any], path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_run_history_markdown(report))
    return target


def _run_index_entry(entry: dict[str, Any]) -> dict[str, Any]:
    output_dir = str(entry.get("output_dir", ""))
    return {
        "method": entry.get("method"),
        "model": entry.get("model"),
        "dataset_id": entry.get("dataset_id"),
        "dataset_version": entry.get("dataset_version"),
        "output_dir": output_dir,
        "checkpoint": entry.get("checkpoint"),
        "run_manifest_file": str(Path(output_dir) / "run_manifest.json") if output_dir else "",
        "checkpoint_index_file": entry.get("checkpoint_index_file")
        or (str(Path(output_dir) / "checkpoints" / "checkpoint_index.json") if output_dir else ""),
    }


def _count_entries(entries: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for entry in entries:
        value = entry.get(field)
        if value is None:
            continue
        key = str(value)
        counts[key] = counts.get(key, 0) + 1
    return counts


def _summarize_run_groups(runs: list[dict[str, Any]], field: str) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for entry in runs:
        value = entry.get(field)
        if not value:
            continue
        groups.setdefault(str(value), []).append(entry)

    summaries = []
    for value, entries in sorted(groups.items()):
        latest_entry = entries[-1]
        summaries.append(
            {
                field: value,
                "run_count": len(entries),
                "model_count": len({entry["model"] for entry in entries if entry.get("model")}),
                "dataset_count": len({entry["dataset_id"] for entry in entries if entry.get("dataset_id")}),
                "method_counts": _count_entries(entries, "method"),
                "latest_output_dir": latest_entry.get("output_dir", ""),
                "latest_run_manifest_file": latest_entry.get("run_manifest_file", ""),
                "latest_checkpoint_index_file": latest_entry.get("checkpoint_index_file", ""),
            }
        )
    return summaries


def _render_run_group_markdown(title: str, summaries: list[dict[str, Any]], group_field: str) -> list[str]:
    if not summaries:
        return []

    lines = [
        "",
        f"## {title}",
        "",
        "| Group | Runs | Models | Datasets | Latest Output Dir | Latest Run Manifest | Latest Checkpoint Index |",
        "| --- | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for summary in summaries:
        lines.append(
            "| "
            f"{_markdown_table_cell(summary[group_field])} | "
            f"{summary['run_count']} | "
            f"{summary['model_count']} | "
            f"{summary['dataset_count']} | "
            f"{_markdown_table_cell(summary['latest_output_dir'])} | "
            f"{_markdown_table_cell(summary['latest_run_manifest_file'])} | "
            f"{_markdown_table_cell(summary['latest_checkpoint_index_file'])} |"
        )
    return lines


def _markdown_table_cell(value: Any) -> str:
    return str(value or "").replace("|", "\\|")
