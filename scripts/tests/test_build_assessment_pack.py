from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.build_assessment_pack import (
    AssessmentPackError,
    build_assessment_pack,
    render_markdown,
    write_outputs,
)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload))


def minimal_course_catalog(*, ready: bool = True, modules: list[dict] | None = None) -> dict:
    module_cards = modules or [
        {
            "id": "zero-to-one",
            "title": "从 0 到 1 学习模块",
            "audience": "第一次系统学习 AI Infra 的读者。",
            "outcome": "能讲清 AI Infra 的基本分层。",
            "entry_route": "/00-overview/00-zero-to-one",
            "entry_title": "从 0 到 1 学习路径",
            "estimated_study_blocks": 2,
            "route_groups": [
                {
                    "id": "practice",
                    "pages": [{"title": "深度实战总览", "route": "/07-hands-on-labs/00-overview"}],
                },
                {
                    "id": "evidence",
                    "pages": [{"title": "学习站清单生成器", "route": "/09-reference/08-learning-inventory"}],
                },
                {
                    "id": "assessment",
                    "pages": [{"title": "系统地图自测", "route": "/10-assessments/01-system-map-check"}],
                },
            ],
            "checkpoints": ["能画出系统地图。"],
            "facilitator_notes": ["先让读者选择目标。"],
        }
    ]
    return {
        "report_type": "ai_infra_course_catalog",
        "summary": {
            "module_count": len(module_cards),
            "docs_pages": 122,
            "missing_route_count": 0,
            "missing_track_count": 0,
            "ready_for_workshop": ready,
        },
        "modules": module_cards,
    }


def minimal_workshop_packet(*, ready: bool = True, module_count: int = 1) -> dict:
    return {
        "report_type": "ai_infra_workshop_packet",
        "summary": {
            "packet_readiness": "ready" if ready else "review",
            "module_count": module_count,
            "docs_pages": 122,
        },
        "validation": {"ready_for_public_workshop": ready},
        "module_cards": [
            {
                "id": "zero-to-one",
                "learner_tasks": ["读入口页并写下系统分层。"],
                "evidence_expectations": ["能指向学习清单或系统地图。"],
            }
        ],
    }


def test_build_assessment_pack_combines_course_and_workshop(tmp_path: Path) -> None:
    catalog = tmp_path / "catalog.json"
    workshop = tmp_path / "workshop.json"
    write_json(catalog, minimal_course_catalog())
    write_json(workshop, minimal_workshop_packet())

    packet = build_assessment_pack(catalog, workshop, strict=True)

    assert packet["report_type"] == "ai_infra_assessment_pack"
    assert packet["summary"]["assessment_readiness"] == "ready"
    assert packet["validation"]["ready_for_assessment"] is True
    assert packet["module_assessments"][0]["id"] == "zero-to-one"
    assert packet["module_assessments"][0]["rubric"][0]["level"] == "Level 1"
    assert "AI Infra Assessment Pack" in render_markdown(packet)


def test_strict_mode_rejects_unready_workshop_packet(tmp_path: Path) -> None:
    catalog = tmp_path / "catalog.json"
    workshop = tmp_path / "workshop.json"
    write_json(catalog, minimal_course_catalog())
    write_json(workshop, minimal_workshop_packet(ready=False))

    with pytest.raises(AssessmentPackError, match="workshop packet is not ready"):
        build_assessment_pack(catalog, workshop, strict=True)

    packet = build_assessment_pack(catalog, workshop, strict=False)
    assert packet["summary"]["assessment_readiness"] == "review"


def test_strict_mode_rejects_module_count_mismatch(tmp_path: Path) -> None:
    catalog = tmp_path / "catalog.json"
    workshop = tmp_path / "workshop.json"
    write_json(catalog, minimal_course_catalog())
    write_json(workshop, minimal_workshop_packet(module_count=2))

    with pytest.raises(AssessmentPackError, match="module counts do not match"):
        build_assessment_pack(catalog, workshop, strict=True)


def test_write_outputs_persists_assessment_pack(tmp_path: Path) -> None:
    catalog = tmp_path / "catalog.json"
    workshop = tmp_path / "workshop.json"
    write_json(catalog, minimal_course_catalog())
    write_json(workshop, minimal_workshop_packet())
    packet = build_assessment_pack(catalog, workshop, strict=True)

    json_target, markdown_target = write_outputs(packet, tmp_path / "assessment.json", tmp_path / "assessment.md")

    assert json.loads(json_target.read_text())["summary"]["assessment_readiness"] == "ready"
    assert markdown_target.read_text().startswith("# AI Infra Assessment Pack")
