from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.build_roadmap_pack import RoadmapPackError, build_roadmap_pack, render_markdown, write_outputs


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload))


def minimal_release_brief(*, ready: bool = True) -> dict:
    return {
        "report_type": "ai_infra_release_brief",
        "summary": {
            "release_readiness": "ready" if ready else "review",
            "docs_pages": 123,
        },
        "validation": {"ready_for_public_review": ready},
    }


def minimal_assessment_pack(*, ready: bool = True, questions: int = 1) -> dict:
    return {
        "report_type": "ai_infra_assessment_pack",
        "summary": {
            "assessment_readiness": "ready" if ready else "review",
            "module_count": 1,
            "question_count": questions,
            "docs_pages": 123,
        },
        "validation": {"ready_for_assessment": ready},
        "module_assessments": [
            {
                "id": "zero-to-one",
                "title": "从 0 到 1 学习模块",
                "entry_route": "/00-overview/00-zero-to-one",
                "questions": [{"prompt": "这个模块的核心工程问题是什么？"}],
                "evidence_requirements": ["至少引用 `/09-reference/08-learning-inventory` 中的一项证据。"],
            }
        ],
    }


def test_build_roadmap_pack_creates_issue_seeds(tmp_path: Path) -> None:
    release = tmp_path / "release.json"
    assessment = tmp_path / "assessment.json"
    write_json(release, minimal_release_brief())
    write_json(assessment, minimal_assessment_pack())

    packet = build_roadmap_pack(release, assessment, strict=True)

    assert packet["report_type"] == "ai_infra_roadmap_pack"
    assert packet["summary"]["roadmap_readiness"] == "ready"
    assert packet["validation"]["ready_for_public_roadmap"] is True
    assert packet["summary"]["issue_seed_count"] == 7
    assert packet["issue_seeds"][0]["id"] == "module-zero-to-one-depth"
    assert "AI Infra Roadmap Pack" in render_markdown(packet)


def test_strict_mode_rejects_unready_release_brief(tmp_path: Path) -> None:
    release = tmp_path / "release.json"
    assessment = tmp_path / "assessment.json"
    write_json(release, minimal_release_brief(ready=False))
    write_json(assessment, minimal_assessment_pack())

    with pytest.raises(RoadmapPackError, match="release brief is not ready"):
        build_roadmap_pack(release, assessment, strict=True)

    packet = build_roadmap_pack(release, assessment, strict=False)
    assert packet["summary"]["roadmap_readiness"] == "review"


def test_strict_mode_rejects_assessment_without_questions(tmp_path: Path) -> None:
    release = tmp_path / "release.json"
    assessment = tmp_path / "assessment.json"
    write_json(release, minimal_release_brief())
    write_json(assessment, minimal_assessment_pack(questions=0))

    with pytest.raises(RoadmapPackError, match="assessment pack has no questions"):
        build_roadmap_pack(release, assessment, strict=True)


def test_write_outputs_persists_roadmap_pack(tmp_path: Path) -> None:
    release = tmp_path / "release.json"
    assessment = tmp_path / "assessment.json"
    write_json(release, minimal_release_brief())
    write_json(assessment, minimal_assessment_pack())
    packet = build_roadmap_pack(release, assessment, strict=True)

    json_target, markdown_target = write_outputs(packet, tmp_path / "roadmap.json", tmp_path / "roadmap.md")

    assert json.loads(json_target.read_text())["summary"]["roadmap_readiness"] == "ready"
    assert markdown_target.read_text().startswith("# AI Infra Roadmap Pack")
