from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.build_learning_inventory import (
    InventoryValidationError,
    build_learning_inventory,
    render_markdown,
    write_outputs,
)


def write_page(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def create_minimal_docs(root: Path) -> None:
    write_page(
        root / "index.md",
        """---
layout: home
---

# Home

Welcome to the local site.
""",
    )
    write_page(
        root / "00-overview" / "00-zero-to-one.md",
        """# 从 0 到 1

## 目标

读者先建立系统地图。

[下一步](/00-overview/02-learning-route)
""",
    )
    write_page(
        root / "00-overview" / "02-learning-route.md",
        """# 学习路线

## 路线

```bash
make docs-quality
```
""",
    )
    write_page(
        root / "07-hands-on-labs" / "00-overview.md",
        """# 深度实战总览

## Lab

把命令、产物和验收连起来。
""",
    )


def test_build_learning_inventory_groups_pages_and_tracks(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    create_minimal_docs(docs_dir)
    (tmp_path / "projects" / "demo").mkdir(parents=True)
    (tmp_path / "projects" / "demo" / "pyproject.toml").write_text("[project]\nname='demo'\n")
    (tmp_path / "Makefile").write_text("docs-quality:\n\ndocs-inventory:\n\ninfra-check:\n")

    packet = build_learning_inventory(docs_dir, tmp_path)

    assert packet["report_type"] == "ai_infra_learning_inventory"
    assert packet["summary"]["page_count"] == 4
    assert packet["summary"]["section_count"] == 3
    assert packet["quality_signals"]["hands_on_lab_pages"] == 1
    assert packet["quality_signals"]["project_count"] == 1
    assert packet["make_targets"]["important_targets_present"]["docs-inventory"] is True
    assert packet["sections"][0]["id"] == "home"
    assert packet["sections"][1]["id"] == "00-overview"
    zero_to_one_track = packet["course_tracks"][0]
    assert zero_to_one_track["id"] == "zero-to-one"
    assert zero_to_one_track["matched_route_count"] == 3
    assert "/00-overview/12-course-syllabus" in zero_to_one_track["missing_routes"]
    assert "AI Infra Learning Inventory" in render_markdown(packet)


def test_strict_mode_rejects_missing_course_routes(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    create_minimal_docs(docs_dir)

    with pytest.raises(InventoryValidationError, match="missing course track routes"):
        build_learning_inventory(docs_dir, tmp_path, strict=True)


def test_write_outputs_persists_json_and_markdown(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    create_minimal_docs(docs_dir)
    packet = build_learning_inventory(docs_dir, tmp_path)

    json_target, markdown_target = write_outputs(
        packet,
        tmp_path / "inventory.json",
        tmp_path / "inventory.md",
    )

    assert json.loads(json_target.read_text())["summary"]["page_count"] == 4
    assert markdown_target.read_text().startswith("# AI Infra Learning Inventory")
