from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_dataset_registry_entry(
    *,
    train_file: str,
    dataset_summary: dict[str, Any],
    run_output_dir: str | Path,
    method: str,
    model: str,
) -> dict[str, Any]:
    dataset_path = Path(train_file)
    dataset_version = dataset_summary["dataset_version"]
    return {
        "artifact_type": "finetune_dataset_registry_entry",
        "dataset_id": f"{dataset_path.stem}@{dataset_version}",
        "dataset_name": dataset_path.stem,
        "dataset_uri": str(dataset_path),
        "dataset_version": dataset_version,
        "dataset_sha256": dataset_summary["dataset_sha256"],
        "dataset_size_bytes": dataset_summary["dataset_size_bytes"],
        "detected_format": "jsonl",
        "records": dataset_summary["records"],
        "messages": dataset_summary["messages"],
        "average_messages_per_record": dataset_summary["average_messages_per_record"],
        "role_counts": dataset_summary["role_counts"],
        "records_with_system": dataset_summary["records_with_system"],
        "registered_from": {
            "run_output_dir": str(run_output_dir),
            "method": method,
            "model": model,
        },
    }


def append_dataset_registry(path: str | Path, entry: dict[str, Any]) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")
    return target


def build_dataset_registry_report(
    path: str | Path,
    *,
    dataset_id: str | None = None,
    method: str | None = None,
    model: str | None = None,
) -> dict[str, Any]:
    registry_path = Path(path)
    entries: list[dict[str, Any]] = []
    skipped_entries: list[dict[str, Any]] = []
    total_entry_count = 0

    if registry_path.exists():
        for line_number, line in enumerate(registry_path.read_text().splitlines(), start=1):
            if not line.strip():
                continue
            total_entry_count += 1
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                skipped_entries.append({"line": line_number, "reason": "invalid json"})
                continue
            if dataset_id and entry.get("dataset_id") != dataset_id:
                continue
            registered_from = entry.get("registered_from", {})
            if method and registered_from.get("method") != method:
                continue
            if model and registered_from.get("model") != model:
                continue
            entries.append(entry)

    datasets = _summarize_registry_entries(entries)
    return {
        "report_type": "finetune_dataset_registry",
        "registry_file": str(registry_path),
        "dataset_id_filter": dataset_id,
        "method_filter": method,
        "model_filter": model,
        "total_entry_count": total_entry_count,
        "entry_count": len(entries),
        "dataset_count": len(datasets),
        "duplicate_entry_count": max(0, len(entries) - len(datasets)),
        "skipped_entries": skipped_entries,
        "datasets": datasets,
        "entries": entries,
    }


def build_dataset_registry_diff(
    path: str | Path,
    *,
    left_dataset_id: str,
    right_dataset_id: str,
) -> dict[str, Any]:
    registry_path = Path(path)
    entries = _load_registry_entries(registry_path)
    left = _latest_entry_for_dataset(entries, left_dataset_id)
    right = _latest_entry_for_dataset(entries, right_dataset_id)
    if left is None:
        raise ValueError(f"Dataset not found in registry: {left_dataset_id}")
    if right is None:
        raise ValueError(f"Dataset not found in registry: {right_dataset_id}")

    fields = [
        "dataset_name",
        "dataset_uri",
        "dataset_version",
        "dataset_sha256",
        "dataset_size_bytes",
        "records",
        "messages",
        "average_messages_per_record",
        "role_counts",
        "records_with_system",
    ]
    left_snapshot = _dataset_diff_snapshot(left)
    right_snapshot = _dataset_diff_snapshot(right)
    field_diffs = {
        field: {"left": left_snapshot.get(field), "right": right_snapshot.get(field)}
        for field in fields
        if left_snapshot.get(field) != right_snapshot.get(field)
    }
    return {
        "report_type": "finetune_dataset_diff",
        "registry_file": str(registry_path),
        "left_dataset_id": left_dataset_id,
        "right_dataset_id": right_dataset_id,
        "identical_dataset_sha256": left_snapshot["dataset_sha256"] == right_snapshot["dataset_sha256"],
        "identical_dataset_version": left_snapshot["dataset_version"] == right_snapshot["dataset_version"],
        "changed_fields": list(field_diffs),
        "field_diffs": field_diffs,
        "left": left_snapshot,
        "right": right_snapshot,
    }


def render_dataset_registry_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Finetune Dataset Registry",
        "",
        f"- Registry file: `{report['registry_file']}`",
        f"- Entries: `{report['entry_count']}`",
        f"- Datasets: `{report['dataset_count']}`",
    ]
    if report.get("dataset_id_filter"):
        lines.append(f"- Dataset filter: `{report['dataset_id_filter']}`")
    if report.get("method_filter"):
        lines.append(f"- Method filter: `{report['method_filter']}`")
    if report.get("model_filter"):
        lines.append(f"- Model filter: `{report['model_filter']}`")
    lines.append(f"- Duplicate registrations: `{report.get('duplicate_entry_count', 0)}`")
    if report.get("skipped_entries"):
        lines.append(f"- Skipped entries: `{len(report['skipped_entries'])}`")
    if not report["datasets"]:
        lines.extend(["", "No dataset registry entries found."])
        return "\n".join(lines) + "\n"

    lines.extend(
        [
            "",
            "| Dataset ID | URI | Records | Messages | Runs | Models | Last Run |",
            "| --- | --- | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for dataset in report["datasets"]:
        lines.append(
            "| "
            f"{_markdown_table_cell(dataset['dataset_id'])} | "
            f"{_markdown_table_cell(dataset['dataset_uri'])} | "
            f"{dataset['records']} | "
            f"{dataset['messages']} | "
            f"{dataset['registered_count']} | "
            f"{_markdown_table_cell(', '.join(dataset['models']))} | "
            f"{_markdown_table_cell(dataset['last_run_output_dir'])} |"
        )
    return "\n".join(lines) + "\n"


def render_dataset_registry_diff_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Finetune Dataset Diff",
        "",
        f"- Registry file: `{report['registry_file']}`",
        f"- Left: `{report['left_dataset_id']}`",
        f"- Right: `{report['right_dataset_id']}`",
        f"- Identical sha256: `{str(report['identical_dataset_sha256']).lower()}`",
        f"- Identical version: `{str(report['identical_dataset_version']).lower()}`",
        f"- Changed fields: `{len(report['changed_fields'])}`",
        "",
        "| Field | Left | Right |",
        "| --- | --- | --- |",
    ]
    if not report["field_diffs"]:
        lines.append("| n/a | identical | identical |")
        return "\n".join(lines) + "\n"

    for field, payload in report["field_diffs"].items():
        lines.append(
            "| "
            f"{_markdown_table_cell(field)} | "
            f"{_markdown_table_cell(json.dumps(payload['left'], sort_keys=True))} | "
            f"{_markdown_table_cell(json.dumps(payload['right'], sort_keys=True))} |"
        )
    return "\n".join(lines) + "\n"


def save_dataset_registry_report(report: dict[str, Any], path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2))
    return target


def save_dataset_registry_markdown(report: dict[str, Any], path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_dataset_registry_markdown(report))
    return target


def save_dataset_registry_diff(report: dict[str, Any], path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2))
    return target


def save_dataset_registry_diff_markdown(report: dict[str, Any], path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_dataset_registry_diff_markdown(report))
    return target


def _summarize_registry_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summaries: dict[str, dict[str, Any]] = {}
    for entry in entries:
        dataset_id = str(entry.get("dataset_id", "unknown"))
        registered_from = entry.get("registered_from", {})
        summary = summaries.setdefault(
            dataset_id,
            {
                "dataset_id": dataset_id,
                "dataset_name": entry.get("dataset_name"),
                "dataset_uri": entry.get("dataset_uri"),
                "dataset_version": entry.get("dataset_version"),
                "dataset_sha256": entry.get("dataset_sha256"),
                "records": entry.get("records", 0),
                "messages": entry.get("messages", 0),
                "role_counts": entry.get("role_counts", {}),
                "registered_count": 0,
                "methods": set(),
                "models": set(),
                "last_run_output_dir": "",
            },
        )
        summary["registered_count"] += 1
        if registered_from.get("method"):
            summary["methods"].add(registered_from["method"])
        if registered_from.get("model"):
            summary["models"].add(registered_from["model"])
        if registered_from.get("run_output_dir"):
            summary["last_run_output_dir"] = registered_from["run_output_dir"]

    normalized = []
    for summary in summaries.values():
        normalized.append(
            {
                **summary,
                "methods": sorted(summary["methods"]),
                "models": sorted(summary["models"]),
            }
        )
    return sorted(normalized, key=lambda item: item["dataset_id"])


def _load_registry_entries(path: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    if not path.exists():
        return entries
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def _latest_entry_for_dataset(entries: list[dict[str, Any]], dataset_id: str) -> dict[str, Any] | None:
    matches = [entry for entry in entries if entry.get("dataset_id") == dataset_id]
    return matches[-1] if matches else None


def _dataset_diff_snapshot(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "dataset_id": entry.get("dataset_id"),
        "dataset_name": entry.get("dataset_name"),
        "dataset_uri": entry.get("dataset_uri"),
        "dataset_version": entry.get("dataset_version"),
        "dataset_sha256": entry.get("dataset_sha256"),
        "dataset_size_bytes": entry.get("dataset_size_bytes"),
        "records": entry.get("records"),
        "messages": entry.get("messages"),
        "average_messages_per_record": entry.get("average_messages_per_record"),
        "role_counts": entry.get("role_counts", {}),
        "records_with_system": entry.get("records_with_system"),
        "registered_from": entry.get("registered_from", {}),
    }


def _markdown_table_cell(value: Any) -> str:
    return str(value or "").replace("|", "\\|")
