from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.build_workshop_packet import (
    WorkshopPacketError,
    build_workshop_packet,
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
                    "id": "orient",
                    "title": "建立地图",
                    "pages": [
                        {
                            "title": "从 0 到 1 学习路径",
                            "route": "/00-overview/00-zero-to-one",
                        }
                    ],
                },
                {
                    "id": "practice",
                    "title": "动手练习",
                    "pages": [
                        {
                            "title": "深度实战总览",
                            "route": "/07-hands-on-labs/00-overview",
                        }
                    ],
                },
                {
                    "id": "evidence",
                    "title": "证据输出",
                    "pages": [
                        {
                            "title": "学习站清单生成器",
                            "route": "/09-reference/08-learning-inventory",
                        }
                    ],
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
            "estimated_study_blocks": 2,
            "docs_pages": 121,
            "missing_route_count": 0,
            "missing_track_count": 0,
            "ready_for_workshop": ready,
        },
        "modules": module_cards,
    }


def minimal_release_brief(*, ready: bool = True) -> dict:
    return {
        "report_type": "ai_infra_release_brief",
        "summary": {
            "release_readiness": "ready" if ready else "review",
            "docs_pages": 121,
            "course_tracks": 7,
        },
        "validation": {"ready_for_public_review": ready},
    }


def test_build_workshop_packet_combines_catalog_and_release(tmp_path: Path) -> None:
    catalog = tmp_path / "catalog.json"
    release = tmp_path / "release.json"
    write_json(catalog, minimal_course_catalog())
    write_json(release, minimal_release_brief())

    packet = build_workshop_packet(catalog, release, strict=True)

    assert packet["report_type"] == "ai_infra_workshop_packet"
    assert packet["summary"]["packet_readiness"] == "ready"
    assert packet["validation"]["ready_for_public_workshop"] is True
    assert packet["module_cards"][0]["id"] == "zero-to-one"
    assert packet["agenda_templates"][0]["id"] == "ninety-minute"
    assert "AI Infra Workshop Packet" in render_markdown(packet)


def test_strict_mode_rejects_unready_release_brief(tmp_path: Path) -> None:
    catalog = tmp_path / "catalog.json"
    release = tmp_path / "release.json"
    write_json(catalog, minimal_course_catalog())
    write_json(release, minimal_release_brief(ready=False))

    with pytest.raises(WorkshopPacketError, match="release brief is not ready"):
        build_workshop_packet(catalog, release, strict=True)

    packet = build_workshop_packet(catalog, release, strict=False)
    assert packet["summary"]["packet_readiness"] == "review"


def test_strict_mode_rejects_unready_course_catalog(tmp_path: Path) -> None:
    catalog = tmp_path / "catalog.json"
    release = tmp_path / "release.json"
    write_json(catalog, minimal_course_catalog(ready=False))
    write_json(release, minimal_release_brief())

    with pytest.raises(WorkshopPacketError, match="course catalog is not ready"):
        build_workshop_packet(catalog, release, strict=True)


def test_write_outputs_persists_workshop_packet(tmp_path: Path) -> None:
    catalog = tmp_path / "catalog.json"
    release = tmp_path / "release.json"
    write_json(catalog, minimal_course_catalog())
    write_json(release, minimal_release_brief())
    packet = build_workshop_packet(catalog, release, strict=True)

    json_target, markdown_target = write_outputs(packet, tmp_path / "packet.json", tmp_path / "packet.md")

    assert json.loads(json_target.read_text())["summary"]["packet_readiness"] == "ready"
    assert markdown_target.read_text().startswith("# AI Infra Workshop Packet")
