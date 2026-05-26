from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.build_launch_pack import (
    LaunchPackError,
    build_launch_pack,
    normalize_labels,
    render_markdown,
    write_outputs,
)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload))


def minimal_release_brief(*, ready: bool = True) -> dict:
    return {
        "report_type": "ai_infra_release_brief",
        "summary": {
            "release_readiness": "ready" if ready else "review",
            "docs_pages": 133,
            "course_tracks": 7,
        },
        "validation": {"ready_for_public_review": ready},
    }


def minimal_roadmap_pack(*, ready: bool = True, issues: int = 2) -> dict:
    issue_seeds = [
        {
            "id": "launch-faq-from-assessment",
            "title": "[Docs] Add FAQ entries from assessment weak spots",
            "labels": ["documentation", "good first issue", "question"],
            "priority": "P0",
            "source_module": "cross-cutting",
            "learning_value": "把测评弱点回流到 FAQ。",
            "scope": ["补充 3 个 FAQ。"],
            "suggested_files": ["docs/00-overview/10-faq.md"],
            "acceptance_criteria": ["FAQ 链接到具体学习页。"],
            "verification_commands": ["PYTHON=.venv/bin/python make docs-quality"],
        },
        {
            "id": "launch-evidence-gallery-depth",
            "title": "[Evidence] Add more public-demo evidence snippets",
            "labels": ["lab", "evidence", "feedback", "enhancement"],
            "priority": "P1",
            "source_module": "cross-cutting",
            "learning_value": "让读者更容易判断输出是否正确。",
            "scope": ["补充脱敏示例输出。"],
            "suggested_files": ["docs/13-output-gallery/01-serving-gateway-evidence.md"],
            "acceptance_criteria": ["不包含真实密钥或私有 endpoint。"],
            "verification_commands": ["PYTHON=.venv/bin/python make docs-quality"],
        },
    ][:issues]
    return {
        "report_type": "ai_infra_roadmap_pack",
        "summary": {
            "roadmap_readiness": "ready" if ready else "review",
            "issue_seed_count": issues,
        },
        "validation": {"ready_for_public_roadmap": ready},
        "issue_seeds": issue_seeds,
        "recommended_commands": ["PYTHON=.venv/bin/python make roadmap-pack"],
    }


def test_build_launch_pack_creates_release_notes_and_starter_issues(tmp_path: Path) -> None:
    release = tmp_path / "release.json"
    roadmap = tmp_path / "roadmap.json"
    write_json(release, minimal_release_brief())
    write_json(roadmap, minimal_roadmap_pack())

    packet = build_launch_pack(release, roadmap, strict=True)

    assert packet["report_type"] == "ai_infra_launch_pack"
    assert packet["summary"]["launch_readiness"] == "ready"
    assert packet["validation"]["ready_for_public_launch"] is True
    assert packet["summary"]["starter_issue_count"] == 2
    assert packet["release_notes"]["title"] == "AI Infra Handbook v0.1.0-learning-site"
    assert packet["starter_issues"][1]["labels"] == ["documentation", "enhancement", "question"]
    assert "AI Infra Launch Pack" in render_markdown(packet)
    assert "[Docs] Add FAQ entries" in render_markdown(packet)


def test_strict_mode_rejects_unready_release_brief(tmp_path: Path) -> None:
    release = tmp_path / "release.json"
    roadmap = tmp_path / "roadmap.json"
    write_json(release, minimal_release_brief(ready=False))
    write_json(roadmap, minimal_roadmap_pack())

    with pytest.raises(LaunchPackError, match="release brief is not ready"):
        build_launch_pack(release, roadmap, strict=True)

    packet = build_launch_pack(release, roadmap, strict=False)
    assert packet["summary"]["launch_readiness"] == "review"


def test_strict_mode_rejects_unready_roadmap_pack(tmp_path: Path) -> None:
    release = tmp_path / "release.json"
    roadmap = tmp_path / "roadmap.json"
    write_json(release, minimal_release_brief())
    write_json(roadmap, minimal_roadmap_pack(ready=False))

    with pytest.raises(LaunchPackError, match="roadmap pack is not ready"):
        build_launch_pack(release, roadmap, strict=True)


def test_strict_mode_rejects_roadmap_without_issue_seeds(tmp_path: Path) -> None:
    release = tmp_path / "release.json"
    roadmap = tmp_path / "roadmap.json"
    write_json(release, minimal_release_brief())
    write_json(roadmap, minimal_roadmap_pack(issues=0))

    with pytest.raises(LaunchPackError, match="roadmap pack has no issue seeds"):
        build_launch_pack(release, roadmap, strict=True)


def test_strict_mode_rejects_stale_roadmap_summary(tmp_path: Path) -> None:
    release = tmp_path / "release.json"
    roadmap = tmp_path / "roadmap.json"
    payload = minimal_roadmap_pack()
    payload["summary"]["issue_seed_count"] = 99
    write_json(release, minimal_release_brief())
    write_json(roadmap, payload)

    with pytest.raises(LaunchPackError, match="issue seed count does not match"):
        build_launch_pack(release, roadmap, strict=True)


def test_normalize_labels_uses_github_default_labels() -> None:
    assert normalize_labels(["lab", "evidence", "feedback", "enhancement"]) == [
        "documentation",
        "enhancement",
        "question",
    ]
    assert normalize_labels(["unknown-special-label"]) == ["enhancement"]
    assert normalize_labels([]) == ["enhancement"]


def test_write_outputs_persists_launch_pack(tmp_path: Path) -> None:
    release = tmp_path / "release.json"
    roadmap = tmp_path / "roadmap.json"
    write_json(release, minimal_release_brief())
    write_json(roadmap, minimal_roadmap_pack())
    packet = build_launch_pack(release, roadmap, strict=True)

    json_target, markdown_target = write_outputs(packet, tmp_path / "launch.json", tmp_path / "launch.md")

    assert json.loads(json_target.read_text())["summary"]["launch_readiness"] == "ready"
    assert markdown_target.read_text().startswith("# AI Infra Launch Pack")
