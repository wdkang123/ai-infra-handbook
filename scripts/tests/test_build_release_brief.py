from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.build_release_brief import ReleaseBriefError, build_release_brief, render_markdown, write_outputs


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload))


def minimal_inventory() -> dict:
    return {
        "report_type": "ai_infra_learning_inventory",
        "summary": {
            "page_count": 119,
            "section_count": 16,
            "course_track_count": 7,
            "missing_track_route_count": 0,
        },
        "quality_signals": {
            "hands_on_lab_pages": 7,
            "assessment_pages": 6,
            "case_study_pages": 4,
            "evidence_gallery_pages": 8,
            "workshop_kit_pages": 7,
            "project_count": 4,
        },
        "sections": [
            {"title": "总览与学习路径", "page_count": 16, "learning_weight": 100},
            {"title": "参考资料", "page_count": 10, "learning_weight": 80},
        ],
        "course_tracks": [
            {
                "id": "zero-to-one",
                "title": "从 0 到 1 主线",
                "matched_route_count": 8,
                "route_count": 8,
                "missing_routes": [],
            }
        ],
    }


def minimal_evidence() -> dict:
    return {
        "report_type": "ai_infra_evidence_packet",
        "summary": {
            "section_count": 3,
            "available_sections": ["serving_gateway", "eval", "finetune"],
            "available_section_count": 3,
            "missing_artifact_count": 0,
            "release_recommendation": "review",
            "finetune_export_status": "success",
        },
        "sections": {
            "serving_gateway": {
                "status": "available",
                "health": {"inference_status": "healthy", "gateway_status": "healthy"},
                "events": {"gateway_status_code_counts": {"401": 1, "404": 1}},
            },
            "eval": {
                "status": "available",
                "release_recommendation": "review",
                "run": {"task": "mmlu", "accuracy": 0.65},
            },
            "finetune": {
                "status": "available",
                "export_status": "success",
                "run": {"method": "lora", "dataset_id": "train@sha256:abc"},
                "export_index": {"adapter_model_sha256": "adapter-sha"},
            },
        },
    }


def test_build_release_brief_combines_inventory_and_evidence(tmp_path: Path) -> None:
    inventory = tmp_path / "inventory.json"
    evidence = tmp_path / "evidence.json"
    write_json(inventory, minimal_inventory())
    write_json(evidence, minimal_evidence())

    brief = build_release_brief(inventory, evidence, strict=True)

    assert brief["report_type"] == "ai_infra_release_brief"
    assert brief["summary"]["release_readiness"] == "ready"
    assert brief["summary"]["docs_pages"] == 119
    assert brief["summary"]["evidence_sections"] == 3
    assert brief["validation"]["ready_for_public_review"] is True
    assert brief["runtime_evidence"]["eval"]["task"] == "mmlu"
    assert "AI Infra Release Brief" in render_markdown(brief)


def test_strict_mode_rejects_incomplete_evidence(tmp_path: Path) -> None:
    inventory = tmp_path / "inventory.json"
    evidence = tmp_path / "evidence.json"
    payload = minimal_evidence()
    payload["summary"]["missing_artifact_count"] = 1
    write_json(inventory, minimal_inventory())
    write_json(evidence, payload)

    with pytest.raises(ReleaseBriefError, match="missing artifacts"):
        build_release_brief(inventory, evidence, strict=True)

    brief = build_release_brief(inventory, evidence, strict=False)
    assert brief["summary"]["release_readiness"] == "review"


def test_write_outputs_persists_release_brief(tmp_path: Path) -> None:
    inventory = tmp_path / "inventory.json"
    evidence = tmp_path / "evidence.json"
    write_json(inventory, minimal_inventory())
    write_json(evidence, minimal_evidence())
    brief = build_release_brief(inventory, evidence, strict=True)

    json_target, markdown_target = write_outputs(brief, tmp_path / "brief.json", tmp_path / "brief.md")

    assert json.loads(json_target.read_text())["summary"]["release_readiness"] == "ready"
    assert markdown_target.read_text().startswith("# AI Infra Release Brief")
