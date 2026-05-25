from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.build_course_catalog import (
    CATALOG_MODULES,
    CourseCatalogError,
    build_course_catalog,
    render_markdown,
    write_outputs,
)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload))


def all_catalog_routes() -> list[str]:
    routes: list[str] = []
    for module in CATALOG_MODULES:
        for group_routes in module["route_groups"].values():
            routes.extend(group_routes)
    return sorted(set(routes))


def minimal_inventory(*, omit_route: str | None = None, omit_track: str | None = None) -> dict:
    routes = [route for route in all_catalog_routes() if route != omit_route]
    pages = [
        {
            "title": route.rsplit("/", 1)[-1] or "Home",
            "route": route,
            "relative_path": f"{route.strip('/')}.md" if route != "/" else "index.md",
            "section_id": route.strip("/").split("/", 1)[0] if route != "/" else "home",
            "h2_count": 2,
            "link_count": 1,
            "code_block_count": 1,
            "learning_weight": 500,
        }
        for route in routes
    ]
    tracks = [
        {
            "id": module["id"],
            "title": module["title"],
            "goal": module["outcome"],
            "route_count": 1,
            "matched_route_count": 1,
            "missing_routes": [],
            "routes": [module["entry_route"]],
        }
        for module in CATALOG_MODULES
        if module["id"] != omit_track
    ]
    return {
        "report_type": "ai_infra_learning_inventory",
        "summary": {"page_count": len(routes), "course_track_count": len(tracks)},
        "sections": [
            {
                "id": "all",
                "title": "All Pages",
                "page_count": len(pages),
                "learning_weight": sum(page["learning_weight"] for page in pages),
                "pages": pages,
            }
        ],
        "course_tracks": tracks,
    }


def test_build_course_catalog_groups_modules_and_routes(tmp_path: Path) -> None:
    inventory = tmp_path / "inventory.json"
    write_json(inventory, minimal_inventory())

    catalog = build_course_catalog(inventory, strict=True)

    assert catalog["report_type"] == "ai_infra_course_catalog"
    assert catalog["summary"]["module_count"] == len(CATALOG_MODULES)
    assert catalog["summary"]["ready_for_workshop"] is True
    assert catalog["validation"]["missing_route_count"] == 0
    assert catalog["modules"][0]["id"] == "zero-to-one"
    assert catalog["modules"][0]["route_groups"][0]["matched_route_count"] > 0
    assert "AI Infra Course Catalog" in render_markdown(catalog)


def test_strict_mode_rejects_missing_catalog_route(tmp_path: Path) -> None:
    inventory = tmp_path / "inventory.json"
    write_json(inventory, minimal_inventory(omit_route="/09-reference/10-course-catalog"))

    with pytest.raises(CourseCatalogError, match="missing catalog routes"):
        build_course_catalog(inventory, strict=True)

    catalog = build_course_catalog(inventory, strict=False)
    assert catalog["summary"]["ready_for_workshop"] is False
    assert "/09-reference/10-course-catalog" in catalog["validation"]["missing_routes"]


def test_strict_mode_rejects_missing_track(tmp_path: Path) -> None:
    inventory = tmp_path / "inventory.json"
    write_json(inventory, minimal_inventory(omit_track="public-sharing"))

    with pytest.raises(CourseCatalogError, match="missing course tracks"):
        build_course_catalog(inventory, strict=True)


def test_write_outputs_persists_course_catalog(tmp_path: Path) -> None:
    inventory = tmp_path / "inventory.json"
    write_json(inventory, minimal_inventory())
    catalog = build_course_catalog(inventory, strict=True)

    json_target, markdown_target = write_outputs(catalog, tmp_path / "catalog.json", tmp_path / "catalog.md")

    assert json.loads(json_target.read_text())["summary"]["module_count"] == len(CATALOG_MODULES)
    assert markdown_target.read_text().startswith("# AI Infra Course Catalog")
