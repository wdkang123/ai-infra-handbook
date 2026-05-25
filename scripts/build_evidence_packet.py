"""Build an end-to-end evidence packet from smoke-test artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class MissingArtifactError(RuntimeError):
    """Raised when strict mode is enabled and required evidence is missing."""


def build_evidence_packet(smoke_dir: str | Path, *, strict: bool = False) -> dict[str, Any]:
    smoke_path = Path(smoke_dir)
    missing: list[dict[str, str]] = []
    sections = {
        "serving_gateway": build_serving_gateway_section(smoke_path / "serving", missing),
        "eval": build_eval_section(smoke_path / "eval", missing),
        "finetune": build_finetune_section(smoke_path / "finetune", missing),
    }
    if strict and missing:
        missing_paths = ", ".join(item["path"] for item in missing)
        raise MissingArtifactError(f"Missing required evidence artifacts: {missing_paths}")

    available_sections = [name for name, section in sections.items() if section["status"] == "available"]
    return {
        "report_type": "ai_infra_evidence_packet",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source": {
            "smoke_dir": str(smoke_path),
        },
        "summary": {
            "section_count": len(sections),
            "available_sections": available_sections,
            "available_section_count": len(available_sections),
            "missing_artifact_count": len(missing),
            "release_recommendation": sections["eval"].get("release_recommendation"),
            "finetune_export_status": sections["finetune"].get("export_status"),
        },
        "sections": sections,
        "missing_artifacts": missing,
        "review_prompts": [
            "Can a reader trace one request through gateway and inference evidence?",
            "Can a reader explain the eval release recommendation from the comparison report?",
            "Can a reader trace the finetune export back to dataset, run, and checkpoint?",
            "Which conclusions are supported by this evidence, and which still need production data?",
        ],
    }


def build_serving_gateway_section(serving_dir: Path, missing: list[dict[str, str]]) -> dict[str, Any]:
    files = {
        "inference_health": serving_dir / "inference_health.json",
        "gateway_health": serving_dir / "gateway_health.json",
        "inference_models": serving_dir / "inference_models.json",
        "gateway_models": serving_dir / "gateway_models.json",
        "inference_events_summary": serving_dir / "inference_events_summary.json",
        "gateway_events_summary": serving_dir / "gateway_events_summary.json",
        "gateway_failure_summary": serving_dir / "gateway_failure_summary.json",
        "inference_request_index": serving_dir / "inference_request_index.json",
        "gateway_request_index": serving_dir / "gateway_request_index.json",
        "inference_request_timeline": serving_dir / "inference_request_timeline.json",
        "gateway_request_timeline": serving_dir / "gateway_request_timeline.json",
        "inference_metrics": serving_dir / "inference_metrics.prom",
        "gateway_metrics": serving_dir / "gateway_metrics.prom",
    }
    loaded = {
        name: read_json_artifact(path, "serving_gateway", missing)
        for name, path in files.items()
        if path.suffix == ".json"
    }
    inference_metrics = read_text_artifact(files["inference_metrics"], "serving_gateway", missing)
    gateway_metrics = read_text_artifact(files["gateway_metrics"], "serving_gateway", missing)

    inference_health = loaded.get("inference_health") or {}
    gateway_health = loaded.get("gateway_health") or {}
    inference_models = loaded.get("inference_models") or {}
    gateway_models = loaded.get("gateway_models") or {}
    inference_summary = (loaded.get("inference_events_summary") or {}).get("summary", {})
    gateway_summary = (loaded.get("gateway_events_summary") or {}).get("summary", {})
    gateway_failures = (loaded.get("gateway_failure_summary") or {}).get("failure_summary", {})

    return {
        "status": section_status(files.values()),
        "files": file_manifest(files, serving_dir),
        "health": {
            "inference_status": inference_health.get("status"),
            "inference_engine": inference_health.get("engine"),
            "gateway_status": gateway_health.get("status"),
            "gateway_upstream_services": gateway_health.get("upstream_services", {}),
        },
        "models": {
            "inference_model_ids": model_ids(inference_models),
            "gateway_model_ids": model_ids(gateway_models),
        },
        "events": {
            "inference_event_type_counts": inference_summary.get("event_type_counts", {}),
            "gateway_event_type_counts": gateway_summary.get("event_type_counts", {}),
            "gateway_status_code_counts": gateway_failures.get("status_code_counts", {}),
            "inference_request_count": (loaded.get("inference_request_index") or {})
            .get("request_index", {})
            .get("matched_request_count"),
            "gateway_request_count": (loaded.get("gateway_request_index") or {})
            .get("request_index", {})
            .get("matched_request_count"),
        },
        "metrics": {
            "inference_metric_names": prometheus_metric_names(inference_metrics or ""),
            "gateway_metric_names": prometheus_metric_names(gateway_metrics or ""),
        },
        "evidence_notes": [
            "Health snapshots show whether gateway can see its inference upstream.",
            "Header and event snapshots should be paired by request id when explaining one request.",
            "Metrics prove counters are moving, not that latency or quality is production-ready.",
        ],
    }


def build_eval_section(eval_dir: Path, missing: list[dict[str, str]]) -> dict[str, Any]:
    files = {
        "run_result": eval_dir / "baseline.json",
        "sample_summary": eval_dir / "baseline" / "sample_summary.json",
        "sample_analysis": eval_dir / "baseline" / "sample_analysis.json",
        "comparison": eval_dir / "compare.json",
        "leaderboard": eval_dir / "leaderboard.json",
        "run_index": eval_dir / "run_index.json",
        "comparison_index": eval_dir / "comparison_index.json",
    }
    loaded = {name: read_json_artifact(path, "eval", missing) for name, path in files.items()}
    run_result = loaded.get("run_result") or {}
    sample_summary = loaded.get("sample_summary") or {}
    sample_analysis = loaded.get("sample_analysis") or {}
    comparison = loaded.get("comparison") or {}
    comparison_summary = comparison.get("summary", {})
    leaderboard = loaded.get("leaderboard") or {}
    run_index = loaded.get("run_index") or {}
    comparison_index = loaded.get("comparison_index") or {}

    return {
        "status": section_status(files.values()),
        "files": file_manifest(files, eval_dir),
        "run": {
            "task": run_result.get("task"),
            "model": run_result.get("model"),
            "backend": run_result.get("backend"),
            "accuracy": run_result.get("accuracy"),
            "num_samples": run_result.get("num_samples"),
            "num_fewshot": run_result.get("num_fewshot"),
            "metrics": run_result.get("metrics", {}),
        },
        "sample_summary": {
            "sample_count": sample_summary.get("sample_count"),
            "passed_count": sample_summary.get("passed_count"),
            "failed_count": sample_summary.get("failed_count"),
            "average_score": sample_summary.get("average_score"),
            "pass_rate": sample_analysis.get("pass_rate"),
            "score_buckets": sample_analysis.get("score_buckets", {}),
            "judge_reason_counts": sample_analysis.get("judge_reason_counts", {}),
            "failed_sample_ids": sample_analysis.get("failed_sample_ids", []),
        },
        "comparison": {
            "verdict": comparison_summary.get("verdict"),
            "release_recommendation": comparison_summary.get("release_recommendation"),
            "delta": comparison_summary.get("delta"),
            "min_delta": comparison_summary.get("min_delta"),
            "release_reasons": comparison_summary.get("release_reasons", []),
        },
        "leaderboard": {
            "entry_count": leaderboard.get("entry_count"),
            "model_count": leaderboard.get("model_count"),
            "backend_groups": sorted((leaderboard.get("backend_groups") or {}).keys()),
            "fewshot_groups": sorted((leaderboard.get("fewshot_groups") or {}).keys()),
        },
        "indexes": {
            "matched_run_count": run_index.get("matched_run_count"),
            "matched_comparison_count": comparison_index.get("matched_comparison_count"),
            "verdict_counts": comparison_index.get("verdict_counts", {}),
            "recommendation_counts": comparison_index.get("recommendation_counts", {}),
        },
        "release_recommendation": comparison_summary.get("release_recommendation"),
        "evidence_notes": [
            "Run evidence records the factual result and sample-level outputs.",
            "Comparison evidence records whether the candidate clears the configured release gate.",
            "Leaderboard evidence is a view over history, not a release decision by itself.",
        ],
    }


def build_finetune_section(finetune_dir: Path, missing: list[dict[str, str]]) -> dict[str, Any]:
    files = {
        "run_manifest": finetune_dir / "run" / "run_manifest.json",
        "dataset_summary": finetune_dir / "run" / "data" / "dataset_summary.json",
        "checkpoint_index": finetune_dir / "run" / "checkpoints" / "checkpoint_index.json",
        "export_manifest": finetune_dir / "exported" / "export_manifest.json",
        "dataset_registry_report": finetune_dir / "dataset_registry_report.json",
        "run_index": finetune_dir / "run_index.json",
        "export_index": finetune_dir / "export_index.json",
    }
    loaded = {name: read_json_artifact(path, "finetune", missing) for name, path in files.items()}
    run_manifest = loaded.get("run_manifest") or {}
    dataset_summary = loaded.get("dataset_summary") or {}
    checkpoint_index = loaded.get("checkpoint_index") or {}
    export_manifest = loaded.get("export_manifest") or {}
    dataset_registry_report = loaded.get("dataset_registry_report") or {}
    run_index = loaded.get("run_index") or {}
    export_index = loaded.get("export_index") or {}
    lineage = export_manifest.get("lineage", {})
    first_checkpoint = first_item(checkpoint_index.get("checkpoints", [])) or {}
    first_export = first_item(export_index.get("exports", [])) or {}

    return {
        "status": section_status(files.values()),
        "files": file_manifest(files, finetune_dir),
        "run": {
            "method": run_manifest.get("method"),
            "model": run_manifest.get("model"),
            "output_dir": run_manifest.get("output_dir"),
            "dataset_id": (run_manifest.get("dataset") or {}).get("id"),
            "dataset_version": (run_manifest.get("dataset") or {}).get("version"),
        },
        "dataset": {
            "records": dataset_summary.get("records"),
            "messages": dataset_summary.get("messages"),
            "role_counts": dataset_summary.get("role_counts", {}),
            "dataset_version": dataset_summary.get("dataset_version"),
            "dataset_sha256": dataset_summary.get("dataset_sha256"),
            "registry_entry_count": dataset_registry_report.get("entry_count"),
            "duplicate_entry_count": dataset_registry_report.get("duplicate_entry_count"),
        },
        "checkpoint": {
            "checkpoint_count": checkpoint_index.get("checkpoint_count"),
            "latest_checkpoint": checkpoint_index.get("latest_checkpoint"),
            "adapter_model_sha256": first_checkpoint.get("adapter_model_sha256"),
            "resumable": first_checkpoint.get("resumable"),
        },
        "export": {
            "status": export_manifest.get("status"),
            "adapter_format": export_manifest.get("adapter_format"),
            "duration_seconds": export_manifest.get("duration_seconds"),
            "exported_file_count": export_manifest.get("exported_file_count"),
            "adapter_model_sha256": first_export.get("adapter_model_sha256"),
            "lineage": {
                "source_checkpoint": lineage.get("source_checkpoint"),
                "training_method": lineage.get("training_method"),
                "training_model": lineage.get("training_model"),
                "dataset_id": lineage.get("dataset_id"),
                "dataset_version": lineage.get("dataset_version"),
                "epochs": lineage.get("epochs"),
            },
        },
        "indexes": {
            "matched_run_count": run_index.get("matched_run_count"),
            "matched_export_count": export_index.get("matched_export_count"),
            "status_counts": export_index.get("status_counts", {}),
        },
        "export_status": export_manifest.get("status"),
        "evidence_notes": [
            "Run manifest records the training method, model, dataset, and artifact pointers.",
            "Checkpoint index records resumability and adapter file fingerprints.",
            "Export manifest records lineage from exported adapter back to checkpoint and dataset.",
        ],
    }


def read_json_artifact(path: Path, section: str, missing: list[dict[str, str]]) -> Any:
    if not path.exists():
        missing.append({"section": section, "path": str(path), "reason": "missing"})
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        missing.append({"section": section, "path": str(path), "reason": f"invalid_json:{exc.lineno}"})
        return None


def read_text_artifact(path: Path, section: str, missing: list[dict[str, str]]) -> str | None:
    if not path.exists():
        missing.append({"section": section, "path": str(path), "reason": "missing"})
        return None
    return path.read_text()


def section_status(paths: Any) -> str:
    return "available" if all(Path(path).exists() for path in paths) else "partial"


def file_manifest(files: dict[str, Path], root: Path) -> dict[str, dict[str, Any]]:
    return {name: file_entry(path, root) for name, path in files.items()}


def file_entry(path: Path, root: Path) -> dict[str, Any]:
    try:
        display_path = path.relative_to(root).as_posix()
    except ValueError:
        display_path = path.as_posix()
    return {
        "path": display_path,
        "exists": path.exists(),
        "size_bytes": path.stat().st_size if path.exists() else None,
    }


def model_ids(payload: dict[str, Any]) -> list[str]:
    models = payload.get("data", [])
    return [str(model.get("id")) for model in models if isinstance(model, dict) and model.get("id")]


def prometheus_metric_names(metrics_text: str) -> list[str]:
    names: set[str] = set()
    for line in metrics_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = re.match(r"(?P<name>[a-zA-Z_:][a-zA-Z0-9_:]*)", stripped)
        if match:
            names.add(match.group("name"))
    return sorted(names)


def first_item(items: Any) -> dict[str, Any] | None:
    if isinstance(items, list) and items and isinstance(items[0], dict):
        return items[0]
    return None


def write_outputs(packet: dict[str, Any], output: Path, markdown_output: Path | None) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n")
    if markdown_output:
        markdown_output.parent.mkdir(parents=True, exist_ok=True)
        markdown_output.write_text(render_markdown(packet))


def render_markdown(packet: dict[str, Any]) -> str:
    sections = packet["sections"]
    lines = [
        "# AI Infra Evidence Packet",
        "",
        f"- Generated at: `{packet['generated_at']}`",
        f"- Smoke dir: `{packet['source']['smoke_dir']}`",
        f"- Available sections: `{', '.join(packet['summary']['available_sections'])}`",
        f"- Missing artifacts: `{packet['summary']['missing_artifact_count']}`",
        "",
        "## Serving / Gateway",
        "",
    ]
    serving = sections["serving_gateway"]
    lines.extend(
        [
            f"- Status: `{serving['status']}`",
            f"- Inference health: `{serving['health']['inference_status']}`",
            f"- Gateway health: `{serving['health']['gateway_status']}`",
            f"- Inference models: `{', '.join(serving['models']['inference_model_ids'])}`",
            f"- Gateway models: `{', '.join(serving['models']['gateway_model_ids'])}`",
            f"- Gateway failure status codes: `{serving['events']['gateway_status_code_counts']}`",
            "",
            "## Eval",
            "",
        ]
    )
    eval_section = sections["eval"]
    comparison = eval_section["comparison"]
    lines.extend(
        [
            f"- Status: `{eval_section['status']}`",
            f"- Task: `{eval_section['run']['task']}`",
            f"- Model: `{eval_section['run']['model']}`",
            f"- Accuracy: `{eval_section['run']['accuracy']}`",
            f"- Sample pass rate: `{eval_section['sample_summary']['pass_rate']}`",
            f"- Verdict: `{comparison['verdict']}`",
            f"- Release recommendation: `{comparison['release_recommendation']}`",
            "",
            "## Finetune",
            "",
        ]
    )
    finetune = sections["finetune"]
    lines.extend(
        [
            f"- Status: `{finetune['status']}`",
            f"- Method: `{finetune['run']['method']}`",
            f"- Model: `{finetune['run']['model']}`",
            f"- Dataset version: `{finetune['dataset']['dataset_version']}`",
            f"- Latest checkpoint: `{finetune['checkpoint']['latest_checkpoint']}`",
            f"- Export status: `{finetune['export']['status']}`",
            f"- Adapter sha256: `{finetune['export']['adapter_model_sha256']}`",
            "",
            "## Review Prompts",
            "",
        ]
    )
    lines.extend(f"- {prompt}" for prompt in packet["review_prompts"])
    if packet["missing_artifacts"]:
        lines.extend(["", "## Missing Artifacts", ""])
        lines.extend(
            f"- `{item['section']}`: `{item['path']}` ({item['reason']})" for item in packet["missing_artifacts"]
        )
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build an AI Infra evidence packet from smoke artifacts.")
    parser.add_argument("--smoke-dir", default=".tmp/smoke", help="Directory containing smoke-test artifacts.")
    parser.add_argument("--output", default=".tmp/evidence/evidence_packet.json", help="JSON output path.")
    parser.add_argument("--markdown-output", default=".tmp/evidence/evidence_packet.md", help="Markdown output path.")
    parser.add_argument("--strict", action="store_true", help="Fail when any required artifact is missing.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        packet = build_evidence_packet(args.smoke_dir, strict=args.strict)
    except MissingArtifactError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    markdown_output = Path(args.markdown_output) if args.markdown_output else None
    write_outputs(packet, Path(args.output), markdown_output)
    print(f"Evidence packet written to {args.output}")
    if markdown_output:
        print(f"Evidence packet markdown written to {markdown_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
