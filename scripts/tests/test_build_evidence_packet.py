from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.build_evidence_packet import MissingArtifactError, build_evidence_packet, render_markdown


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload))


def write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload)


def create_smoke_artifacts(root: Path) -> None:
    serving = root / "serving"
    write_json(serving / "inference_health.json", {"status": "healthy", "engine": "mock"})
    write_json(
        serving / "gateway_health.json",
        {"status": "healthy", "upstream_services": {"vllm-local": "healthy"}},
    )
    write_json(serving / "inference_models.json", {"data": [{"id": "Qwen/Qwen2.5-0.5B-Instruct"}]})
    write_json(serving / "gateway_models.json", {"data": [{"id": "vllm-local"}]})
    write_json(serving / "inference_events_summary.json", {"summary": {"event_type_counts": {"request_success": 1}}})
    write_json(serving / "gateway_events_summary.json", {"summary": {"event_type_counts": {"request_success": 1}}})
    write_json(
        serving / "gateway_failure_summary.json",
        {"failure_summary": {"status_code_counts": {"404": 1}}},
    )
    write_json(serving / "inference_request_index.json", {"request_index": {"matched_request_count": 1}})
    write_json(serving / "gateway_request_index.json", {"request_index": {"matched_request_count": 1}})
    write_json(serving / "inference_request_timeline.json", {"timeline": {"event_types": ["request_success"]}})
    write_json(serving / "gateway_request_timeline.json", {"timeline": {"event_types": ["upstream_attempt"]}})
    write_text(serving / "inference_metrics.prom", "vllm_num_requests_total 1\n")
    write_text(serving / "gateway_metrics.prom", "ai_gateway_requests_total 1\n")

    eval_dir = root / "eval"
    write_json(
        eval_dir / "baseline.json",
        {
            "task": "mmlu",
            "model": "Qwen/Qwen2.5-0.5B-Instruct",
            "backend": "vllm",
            "accuracy": 0.65,
            "num_samples": 100,
            "num_fewshot": 5,
            "metrics": {"mmlu": 0.65},
        },
    )
    write_json(
        eval_dir / "baseline" / "sample_summary.json",
        {"sample_count": 2, "passed_count": 1, "failed_count": 1, "average_score": 0.65},
    )
    write_json(
        eval_dir / "baseline" / "sample_analysis.json",
        {
            "pass_rate": 0.5,
            "score_buckets": {"mid_0_5_to_0_8": 2},
            "judge_reason_counts": {"mock": 2},
            "failed_sample_ids": ["mmlu-2"],
        },
    )
    write_json(
        eval_dir / "compare.json",
        {
            "summary": {
                "verdict": "unchanged",
                "release_recommendation": "review",
                "delta": 0.0,
                "min_delta": 0.0,
                "release_reasons": ["unchanged"],
            }
        },
    )
    write_json(
        eval_dir / "leaderboard.json",
        {
            "entry_count": 1,
            "model_count": 1,
            "backend_groups": {"vllm": []},
            "fewshot_groups": {"5": []},
        },
    )
    write_json(eval_dir / "run_index.json", {"matched_run_count": 1})
    write_json(
        eval_dir / "comparison_index.json",
        {"matched_comparison_count": 1, "verdict_counts": {"unchanged": 1}, "recommendation_counts": {"review": 1}},
    )

    finetune = root / "finetune"
    write_json(
        finetune / "run" / "run_manifest.json",
        {
            "method": "lora",
            "model": "Qwen/Qwen2.5-0.5B-Instruct",
            "output_dir": "run",
            "dataset": {"id": "train@sha256:abc", "version": "sha256:abc"},
        },
    )
    write_json(
        finetune / "run" / "data" / "dataset_summary.json",
        {
            "records": 2,
            "messages": 4,
            "role_counts": {"user": 2, "assistant": 2},
            "dataset_version": "sha256:abc",
            "dataset_sha256": "abc",
        },
    )
    write_json(
        finetune / "run" / "checkpoints" / "checkpoint_index.json",
        {
            "checkpoint_count": 1,
            "latest_checkpoint": "checkpoint-0001",
            "checkpoints": [{"adapter_model_sha256": "adapter-sha", "resumable": True}],
        },
    )
    write_json(
        finetune / "exported" / "export_manifest.json",
        {
            "status": "success",
            "adapter_format": "mock-peft-adapter",
            "duration_seconds": 0.1,
            "exported_file_count": 3,
            "lineage": {
                "source_checkpoint": "checkpoint-0001",
                "training_method": "lora",
                "training_model": "Qwen/Qwen2.5-0.5B-Instruct",
                "dataset_id": "train@sha256:abc",
                "dataset_version": "sha256:abc",
                "epochs": 1,
            },
        },
    )
    write_json(
        finetune / "dataset_registry_report.json",
        {"entry_count": 1, "duplicate_entry_count": 0},
    )
    write_json(finetune / "run_index.json", {"matched_run_count": 1})
    write_json(
        finetune / "export_index.json",
        {
            "matched_export_count": 1,
            "status_counts": {"success": 1},
            "exports": [{"adapter_model_sha256": "adapter-sha"}],
        },
    )


def test_build_evidence_packet_summarizes_all_sections(tmp_path: Path) -> None:
    create_smoke_artifacts(tmp_path)

    packet = build_evidence_packet(tmp_path, strict=True)

    assert packet["report_type"] == "ai_infra_evidence_packet"
    assert packet["summary"]["available_section_count"] == 3
    assert packet["summary"]["release_recommendation"] == "review"
    assert packet["sections"]["serving_gateway"]["models"]["gateway_model_ids"] == ["vllm-local"]
    assert packet["sections"]["eval"]["sample_summary"]["pass_rate"] == 0.5
    assert packet["sections"]["finetune"]["export"]["adapter_model_sha256"] == "adapter-sha"
    assert "AI Infra Evidence Packet" in render_markdown(packet)


def test_strict_mode_rejects_missing_artifacts(tmp_path: Path) -> None:
    create_smoke_artifacts(tmp_path)
    (tmp_path / "eval" / "compare.json").unlink()

    with pytest.raises(MissingArtifactError):
        build_evidence_packet(tmp_path, strict=True)

    packet = build_evidence_packet(tmp_path, strict=False)
    assert packet["summary"]["missing_artifact_count"] == 1
    assert packet["sections"]["eval"]["status"] == "partial"
