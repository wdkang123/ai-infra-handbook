from __future__ import annotations

import json
from pathlib import Path
from shutil import copyfile
from time import perf_counter
from typing import Any

from finetune_demo.artifacts import build_artifact_entries, file_artifact_entry


def export_adapter(checkpoint_dir: str | Path, output_dir: str | Path) -> Path:
    started_at = perf_counter()
    checkpoint = Path(checkpoint_dir)
    output = Path(output_dir)
    if not checkpoint.exists():
        raise FileNotFoundError(f"Checkpoint directory not found: {checkpoint}")
    if not checkpoint.is_dir():
        raise NotADirectoryError(f"Checkpoint path is not a directory: {checkpoint}")
    source_adapter_config = checkpoint / "adapter_config.json"
    source_adapter_model = checkpoint / "adapter_model.safetensors"
    missing = [path for path in (source_adapter_config, source_adapter_model) if not path.exists()]
    if missing:
        missing_names = ", ".join(str(path) for path in missing)
        raise FileNotFoundError(f"Checkpoint is missing required adapter files: {missing_names}")

    output.mkdir(parents=True, exist_ok=True)

    adapter_config = output / "adapter_config.json"
    adapter_model = output / "adapter_model.safetensors"
    source_state = checkpoint / "trainer_state.json"
    adapter_config_payload = _read_json(source_adapter_config)
    trainer_state_payload = _read_json(source_state) if source_state.exists() else {}

    copyfile(source_adapter_config, adapter_config)
    copyfile(source_adapter_model, adapter_model)

    if source_state.exists():
        (output / "trainer_state.snapshot.json").write_text(source_state.read_text())
    exported_files = ["adapter_config.json", "adapter_model.safetensors"]
    if (output / "trainer_state.snapshot.json").exists():
        exported_files.append("trainer_state.snapshot.json")
    duration_seconds = round(perf_counter() - started_at, 6)
    export_manifest = output / "export_manifest.json"
    export_manifest.write_text(
        json.dumps(
            {
                "artifact_type": "finetune_adapter_export",
                "format": "mock-peft-adapter-export",
                "status": "success",
                "duration_seconds": duration_seconds,
                "source_checkpoint": str(checkpoint),
                "output_dir": str(output),
                "base_model": adapter_config_payload.get("base_model"),
                "adapter_format": adapter_config_payload.get("format"),
                "lineage": {
                    "source_checkpoint": str(checkpoint),
                    "training_method": trainer_state_payload.get("method"),
                    "training_model": trainer_state_payload.get("model"),
                    "train_file": trainer_state_payload.get("train_file"),
                    "dataset_id": trainer_state_payload.get("dataset_id"),
                    "dataset_version": trainer_state_payload.get("dataset_version"),
                    "dataset_sha256": trainer_state_payload.get("dataset_sha256"),
                    "epochs": trainer_state_payload.get("epochs"),
                },
                "files": sorted(exported_files),
                "exported_file_count": len(exported_files),
                "file_artifacts": build_artifact_entries(output, exported_files),
            },
            indent=2,
        )
        + "\n"
    )
    history_path = output.parent / "export_history.jsonl"
    adapter_entry = file_artifact_entry(output, "adapter_model.safetensors")
    with history_path.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {
                    "source_checkpoint": str(checkpoint),
                    "output_dir": str(output),
                    "export_manifest_file": str(export_manifest),
                    "status": "success",
                    "duration_seconds": duration_seconds,
                    "base_model": adapter_config_payload.get("base_model"),
                    "dataset_id": trainer_state_payload.get("dataset_id"),
                    "dataset_version": trainer_state_payload.get("dataset_version"),
                    "adapter_model_sha256": adapter_entry["sha256"],
                }
            )
            + "\n"
        )

    return output


def build_export_history_report(
    path: str | Path,
    *,
    dataset_id: str | None = None,
    model: str | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    history_path = Path(path)
    exports: list[dict[str, Any]] = []
    skipped_entries: list[dict[str, Any]] = []
    total_export_count = 0

    if history_path.exists():
        for line_number, line in enumerate(history_path.read_text().splitlines(), start=1):
            if not line.strip():
                continue
            total_export_count += 1
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                skipped_entries.append({"line": line_number, "reason": "invalid json"})
                continue
            if dataset_id and entry.get("dataset_id") != dataset_id:
                continue
            if model and entry.get("base_model") != model:
                continue
            exports.append(
                {
                    "source_checkpoint": entry.get("source_checkpoint", ""),
                    "output_dir": entry.get("output_dir", ""),
                    "export_manifest_file": _export_manifest_file(entry),
                    "status": entry.get("status", "unknown"),
                    "duration_seconds": entry.get("duration_seconds"),
                    "base_model": entry.get("base_model"),
                    "dataset_id": entry.get("dataset_id"),
                    "dataset_version": entry.get("dataset_version"),
                    "adapter_model_sha256": entry.get("adapter_model_sha256"),
                }
            )

    matched_export_count = len(exports)
    if limit is not None:
        exports = exports[-limit:]
    durations = [
        float(entry["duration_seconds"]) for entry in exports if isinstance(entry.get("duration_seconds"), (int, float))
    ]

    return {
        "report_type": "finetune_export_index",
        "source_history": str(history_path),
        "dataset_id_filter": dataset_id,
        "model_filter": model,
        "total_export_count": total_export_count,
        "matched_export_count": matched_export_count,
        "export_count": len(exports),
        "dataset_count": len({entry["dataset_id"] for entry in exports if entry.get("dataset_id")}),
        "model_count": len({entry["base_model"] for entry in exports if entry.get("base_model")}),
        "status_counts": {
            status: sum(1 for entry in exports if entry["status"] == status)
            for status in sorted({entry["status"] for entry in exports})
        },
        "model_summaries": _summarize_export_groups(exports, "base_model"),
        "dataset_summaries": _summarize_export_groups(exports, "dataset_id"),
        "total_duration_seconds": round(sum(durations), 6),
        "average_duration_seconds": round(sum(durations) / len(durations), 6) if durations else None,
        "skipped_entries": skipped_entries,
        "exports": exports,
    }


def render_export_history_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Finetune Export Index",
        "",
        f"- Source history: `{report['source_history']}`",
        f"- Exports: `{report['export_count']}`",
        f"- Matched exports: `{report.get('matched_export_count', report['export_count'])}`",
        f"- Datasets: `{report['dataset_count']}`",
        f"- Models: `{report['model_count']}`",
        f"- Total duration seconds: `{report.get('total_duration_seconds', 0.0)}`",
        f"- Average duration seconds: `{report.get('average_duration_seconds')}`",
    ]
    if report.get("dataset_id_filter"):
        lines.append(f"- Dataset filter: `{report['dataset_id_filter']}`")
    if report.get("model_filter"):
        lines.append(f"- Model filter: `{report['model_filter']}`")
    if report.get("skipped_entries"):
        lines.append(f"- Skipped entries: `{len(report['skipped_entries'])}`")
    if not report["exports"]:
        lines.extend(["", "No exports found."])
        return "\n".join(lines) + "\n"

    lines.extend(
        [
            "",
            "| Output Dir | Export Manifest | Status | Duration Seconds | Base Model | Dataset ID | Dataset Version | Adapter SHA256 |",
            "| --- | --- | --- | ---: | --- | --- | --- | --- |",
        ]
    )
    for entry in report["exports"]:
        lines.append(
            "| "
            f"{_markdown_table_cell(entry['output_dir'])} | "
            f"{_markdown_table_cell(entry['export_manifest_file'])} | "
            f"{_markdown_table_cell(entry['status'])} | "
            f"{_markdown_table_cell(entry.get('duration_seconds'))} | "
            f"{_markdown_table_cell(entry['base_model'])} | "
            f"{_markdown_table_cell(entry['dataset_id'])} | "
            f"{_markdown_table_cell(entry['dataset_version'])} | "
            f"{_markdown_table_cell(entry['adapter_model_sha256'])} |"
        )
    lines.extend(_render_export_group_markdown("Model Summaries", report.get("model_summaries", []), "base_model"))
    lines.extend(_render_export_group_markdown("Dataset Summaries", report.get("dataset_summaries", []), "dataset_id"))
    return "\n".join(lines) + "\n"


def save_export_history_report(report: dict[str, Any], path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2))
    return target


def save_export_history_markdown(report: dict[str, Any], path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_export_history_markdown(report))
    return target


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return {}


def _markdown_table_cell(value: Any) -> str:
    return str(value or "").replace("|", "\\|")


def _export_manifest_file(entry: dict[str, Any]) -> str:
    manifest_file = entry.get("export_manifest_file")
    if manifest_file:
        return str(manifest_file)
    output_dir = entry.get("output_dir")
    if not output_dir:
        return ""
    return str(Path(str(output_dir)) / "export_manifest.json")


def _summarize_export_groups(exports: list[dict[str, Any]], field: str) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for entry in exports:
        value = entry.get(field)
        if not value:
            continue
        groups.setdefault(str(value), []).append(entry)

    summaries = []
    for value, entries in sorted(groups.items()):
        durations = [
            float(entry["duration_seconds"])
            for entry in entries
            if isinstance(entry.get("duration_seconds"), (int, float))
        ]
        latest_entry = entries[-1]
        summaries.append(
            {
                field: value,
                "export_count": len(entries),
                "model_count": len({entry["base_model"] for entry in entries if entry.get("base_model")}),
                "dataset_count": len({entry["dataset_id"] for entry in entries if entry.get("dataset_id")}),
                "status_counts": {
                    status: sum(1 for entry in entries if entry["status"] == status)
                    for status in sorted({entry["status"] for entry in entries})
                },
                "average_duration_seconds": round(sum(durations) / len(durations), 6) if durations else None,
                "latest_output_dir": latest_entry.get("output_dir", ""),
                "latest_export_manifest_file": latest_entry.get("export_manifest_file", ""),
                "latest_adapter_model_sha256": latest_entry.get("adapter_model_sha256"),
            }
        )
    return summaries


def _render_export_group_markdown(title: str, summaries: list[dict[str, Any]], group_field: str) -> list[str]:
    if not summaries:
        return []

    lines = [
        "",
        f"## {title}",
        "",
        "| Group | Exports | Models | Datasets | Average Duration Seconds | Latest Output Dir |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for summary in summaries:
        lines.append(
            "| "
            f"{_markdown_table_cell(summary[group_field])} | "
            f"{summary['export_count']} | "
            f"{summary['model_count']} | "
            f"{summary['dataset_count']} | "
            f"{_markdown_table_cell(summary['average_duration_seconds'])} | "
            f"{_markdown_table_cell(summary['latest_output_dir'])} |"
        )
    return lines
