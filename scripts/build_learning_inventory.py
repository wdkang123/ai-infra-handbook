"""Build a structured inventory for the AI Infra learning site."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT_DIR / "docs"

DEFAULT_OUTPUT = ROOT_DIR / ".tmp" / "docs-inventory" / "learning_inventory.json"
DEFAULT_MARKDOWN_OUTPUT = ROOT_DIR / ".tmp" / "docs-inventory" / "learning_inventory.md"

SECTION_TITLES = {
    "home": "首页",
    "00-overview": "总览与学习路径",
    "01-llm-fundamentals": "LLM 基础概念",
    "02-inference-serving": "推理服务",
    "03-ai-gateway-platform": "AI Gateway 平台层",
    "04-evaluation-observability": "评测与可观测性",
    "05-finetuning-training": "微调与训练",
    "06-projects": "可运行项目",
    "07-hands-on-labs": "深度实战",
    "08-publication": "公开发布",
    "09-reference": "参考资料",
    "10-assessments": "学习自测",
    "11-case-studies": "案例复盘",
    "12-production-migration": "生产迁移",
    "13-output-gallery": "示例输出与证据库",
    "14-workshop-kit": "共学与公开分享套件",
}

COURSE_TRACKS = [
    {
        "id": "zero-to-one",
        "title": "从 0 到 1 主线",
        "goal": "让新读者按稳定顺序跑通学习、实操、自测和复盘。",
        "routes": [
            "/00-overview/00-zero-to-one",
            "/00-overview/02-learning-route",
            "/00-overview/12-course-syllabus",
            "/00-overview/15-two-week-learning-plan",
            "/00-overview/03-runbook",
            "/00-overview/04-first-walkthrough",
            "/07-hands-on-labs/00-overview",
            "/10-assessments/00-overview",
        ],
    },
    {
        "id": "serving-engineer",
        "title": "推理服务工程主线",
        "goal": "理解请求、token、streaming、metrics 和执行层边界。",
        "routes": [
            "/01-llm-fundamentals/01-model-token-context",
            "/01-llm-fundamentals/04-from-request-to-first-token",
            "/02-inference-serving/00-overview",
            "/02-inference-serving/09-streaming-batching-metrics",
            "/06-projects/01-inference-service",
            "/07-hands-on-labs/01-serving-observability-lab",
            "/13-output-gallery/01-serving-gateway-evidence",
        ],
    },
    {
        "id": "platform-engineer",
        "title": "平台治理工程主线",
        "goal": "理解鉴权、路由、fallback、限流、request id 和失败语义。",
        "routes": [
            "/03-ai-gateway-platform/00-overview",
            "/03-ai-gateway-platform/01-auth-routing-rate-limit",
            "/03-ai-gateway-platform/03-gateway-router-fallback-cache",
            "/03-ai-gateway-platform/04-streaming-errors-upstream-health",
            "/06-projects/02-ai-gateway",
            "/07-hands-on-labs/02-gateway-resilience-lab",
            "/13-output-gallery/05-failure-evidence-map",
        ],
    },
    {
        "id": "eval-release",
        "title": "评测发布判断主线",
        "goal": "理解 run、compare、leaderboard、sample analysis 和发布门禁。",
        "routes": [
            "/04-evaluation-observability/00-overview",
            "/04-evaluation-observability/01-run-compare-history",
            "/04-evaluation-observability/07-from-run-to-release-decision",
            "/04-evaluation-observability/08-benchmark-vs-production-quality",
            "/06-projects/03-eval-module",
            "/07-hands-on-labs/03-eval-release-gate-lab",
            "/13-output-gallery/02-eval-report-evidence",
        ],
    },
    {
        "id": "training-lineage",
        "title": "训练资产复现主线",
        "goal": "理解 dataset、run、checkpoint、export、manifest 和 lineage。",
        "routes": [
            "/05-finetuning-training/00-overview",
            "/05-finetuning-training/02-run-artifacts-export",
            "/05-finetuning-training/06-experiment-tracking-history-reproducibility",
            "/05-finetuning-training/08-from-demo-training-to-real-training-system",
            "/06-projects/04-finetune-demo",
            "/07-hands-on-labs/04-finetune-reproducibility-lab",
            "/13-output-gallery/03-finetune-artifact-evidence",
        ],
    },
    {
        "id": "public-sharing",
        "title": "公开分享与共学主线",
        "goal": "把个人学习项目组织成可以发布、带练、收反馈和持续协作的材料。",
        "routes": [
            "/00-overview/11-public-learning-guide",
            "/08-publication/00-overview",
            "/08-publication/01-github-pages",
            "/13-output-gallery/07-generated-evidence-packet",
            "/14-workshop-kit/00-overview",
            "/14-workshop-kit/02-learner-workbook",
            "/14-workshop-kit/06-github-release-plan",
            "/08-publication/05-generated-roadmap-pack",
        ],
    },
    {
        "id": "production-migration",
        "title": "生产迁移思维主线",
        "goal": "识别学习型实现和真实生产系统之间的接口、观测、数据和运维差距。",
        "routes": [
            "/12-production-migration/00-overview",
            "/12-production-migration/01-serving-backend-migration",
            "/12-production-migration/02-gateway-platform-hardening",
            "/12-production-migration/03-eval-judge-dashboard-migration",
            "/12-production-migration/04-finetune-real-training-migration",
            "/07-hands-on-labs/06-public-release-readiness-lab",
            "/09-reference/07-validation-matrix",
        ],
    },
]


class InventoryValidationError(RuntimeError):
    """Raised when strict inventory generation finds invalid course metadata."""


@dataclass(frozen=True)
class PageInventory:
    title: str
    route: str
    relative_path: str
    section_id: str
    h2_count: int
    link_count: int
    code_block_count: int
    learning_weight: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "route": self.route,
            "relative_path": self.relative_path,
            "section_id": self.section_id,
            "h2_count": self.h2_count,
            "link_count": self.link_count,
            "code_block_count": self.code_block_count,
            "learning_weight": self.learning_weight,
        }


def build_learning_inventory(
    docs_dir: Path = DOCS_DIR,
    root_dir: Path = ROOT_DIR,
    *,
    strict: bool = False,
) -> dict[str, Any]:
    docs_dir = docs_dir.resolve()
    root_dir = root_dir.resolve()
    pages = collect_pages(docs_dir)
    route_map = {page.route: page for page in pages}
    sections = build_sections(pages)
    tracks = build_tracks(route_map)
    signals = build_quality_signals(root_dir, pages)
    make_targets = collect_make_targets(root_dir / "Makefile")

    missing_routes = [route for track in tracks for route in track["missing_routes"]]
    missing_h1_pages = [page.relative_path for page in pages if page.title == "Untitled"]
    if strict and (missing_routes or missing_h1_pages):
        messages = []
        if missing_routes:
            messages.append(f"missing course track routes: {', '.join(sorted(set(missing_routes)))}")
        if missing_h1_pages:
            messages.append(f"pages without H1: {', '.join(missing_h1_pages)}")
        raise InventoryValidationError("; ".join(messages))

    return {
        "report_type": "ai_infra_learning_inventory",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "site": {
            "title": "AI Infra Manual",
            "docs_dir": safe_relative(docs_dir, root_dir),
            "page_count": len(pages),
            "section_count": len(sections),
        },
        "summary": {
            "page_count": len(pages),
            "section_count": len(sections),
            "course_track_count": len(tracks),
            "tracked_route_count": sum(len(track["routes"]) for track in tracks),
            "missing_track_route_count": len(set(missing_routes)),
            "page_learning_weight_total": sum(page.learning_weight for page in pages),
        },
        "quality_signals": signals,
        "make_targets": make_targets,
        "sections": sections,
        "course_tracks": tracks,
    }


def collect_pages(docs_dir: Path) -> list[PageInventory]:
    pages: list[PageInventory] = []
    for path in sorted(docs_dir.rglob("*.md")):
        if ".vitepress" in path.parts:
            continue
        relative_path = path.relative_to(docs_dir).as_posix()
        text = path.read_text()
        content = strip_frontmatter(text)
        title = extract_h1(content) or extract_frontmatter_title(text) or "Untitled"
        page = PageInventory(
            title=title,
            route=route_for_page(path, docs_dir),
            relative_path=relative_path,
            section_id=section_for_path(path, docs_dir),
            h2_count=count_headings(content, level=2),
            link_count=count_markdown_links(content),
            code_block_count=count_code_blocks(content),
            learning_weight=estimate_learning_weight(content),
        )
        pages.append(page)
    return pages


def route_for_page(path: Path, docs_dir: Path) -> str:
    relative = path.relative_to(docs_dir)
    if relative.as_posix() == "index.md":
        return "/"
    return "/" + relative.with_suffix("").as_posix()


def section_for_path(path: Path, docs_dir: Path) -> str:
    relative = path.relative_to(docs_dir)
    if relative.as_posix() == "index.md":
        return "home"
    return relative.parts[0]


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        _, _, rest = text.partition("\n---\n")
        return rest
    return text


def extract_frontmatter_title(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    frontmatter, _, _ = text[4:].partition("\n---\n")
    for pattern in [
        r"^\s*title:\s*['\"]?(?P<title>.+?)['\"]?\s*$",
        r"^\s*name:\s*['\"]?(?P<title>.+?)['\"]?\s*$",
    ]:
        for line in frontmatter.splitlines():
            match = re.match(pattern, line)
            if match:
                return match.group("title").strip().strip("\"'")
    return None


def strip_fenced_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def extract_h1(text: str) -> str | None:
    body = strip_fenced_code(text)
    for line in body.splitlines():
        match = re.match(r"^\s{0,3}#\s+(?P<title>.+?)\s*$", line)
        if match:
            return clean_heading(match.group("title"))
    return None


def clean_heading(value: str) -> str:
    value = re.sub(r"\s+#+\s*$", "", value).strip()
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    return value.strip()


def count_headings(text: str, *, level: int) -> int:
    marker = "#" * level
    return sum(1 for line in strip_fenced_code(text).splitlines() if re.match(rf"^\s{{0,3}}{marker}\s+\S", line))


def count_markdown_links(text: str) -> int:
    body = strip_fenced_code(text)
    return len(re.findall(r"(?<!!)\[[^\]]+\]\([^)]+\)", body)) + len(re.findall(r"""href=["'][^"']+["']""", body))


def count_code_blocks(text: str) -> int:
    return len(re.findall(r"```", text)) // 2


def estimate_learning_weight(text: str) -> int:
    body = strip_fenced_code(strip_frontmatter(text))
    tokens = re.findall(r"[\u4e00-\u9fff]|[A-Za-z0-9_+./:-]+", body)
    return len(tokens)


def build_sections(pages: list[PageInventory]) -> list[dict[str, Any]]:
    grouped: dict[str, list[PageInventory]] = {}
    for page in pages:
        grouped.setdefault(page.section_id, []).append(page)

    sections: list[dict[str, Any]] = []
    for section_id in sorted(grouped, key=section_sort_key):
        section_pages = sorted(grouped[section_id], key=lambda page: page.relative_path)
        sections.append(
            {
                "id": section_id,
                "title": SECTION_TITLES.get(section_id, title_from_segment(section_id)),
                "page_count": len(section_pages),
                "learning_weight": sum(page.learning_weight for page in section_pages),
                "link_count": sum(page.link_count for page in section_pages),
                "code_block_count": sum(page.code_block_count for page in section_pages),
                "routes": [page.route for page in section_pages],
                "pages": [page.as_dict() for page in section_pages],
            }
        )
    return sections


def section_sort_key(section_id: str) -> tuple[int, str]:
    if section_id == "home":
        return (-1, section_id)
    match = re.match(r"(?P<num>\d+)-", section_id)
    if match:
        return (int(match.group("num")), section_id)
    return (999, section_id)


def title_from_segment(segment: str) -> str:
    return re.sub(r"^\d+-", "", segment).replace("-", " ").title()


def build_tracks(route_map: dict[str, PageInventory]) -> list[dict[str, Any]]:
    tracks: list[dict[str, Any]] = []
    for index, track in enumerate(COURSE_TRACKS, start=1):
        pages = [route_map[route].as_dict() for route in track["routes"] if route in route_map]
        missing_routes = [route for route in track["routes"] if route not in route_map]
        tracks.append(
            {
                "order": index,
                "id": track["id"],
                "title": track["title"],
                "goal": track["goal"],
                "route_count": len(track["routes"]),
                "matched_route_count": len(pages),
                "missing_routes": missing_routes,
                "routes": track["routes"],
                "pages": pages,
                "learning_weight": sum(page["learning_weight"] for page in pages),
            }
        )
    return tracks


def build_quality_signals(root_dir: Path, pages: list[PageInventory]) -> dict[str, Any]:
    section_counts = count_pages_by_section(pages)
    return {
        "hands_on_lab_pages": section_counts.get("07-hands-on-labs", 0),
        "assessment_pages": section_counts.get("10-assessments", 0),
        "case_study_pages": section_counts.get("11-case-studies", 0),
        "production_migration_pages": section_counts.get("12-production-migration", 0),
        "evidence_gallery_pages": section_counts.get("13-output-gallery", 0),
        "workshop_kit_pages": section_counts.get("14-workshop-kit", 0),
        "project_count": count_project_dirs(root_dir / "projects"),
        "docs_quality_script": (root_dir / "scripts" / "docs_quality_check.py").exists(),
        "evidence_packet_script": (root_dir / "scripts" / "build_evidence_packet.py").exists(),
        "course_catalog_script": (root_dir / "scripts" / "build_course_catalog.py").exists(),
        "release_brief_script": (root_dir / "scripts" / "build_release_brief.py").exists(),
        "workshop_packet_script": (root_dir / "scripts" / "build_workshop_packet.py").exists(),
        "assessment_pack_script": (root_dir / "scripts" / "build_assessment_pack.py").exists(),
        "roadmap_pack_script": (root_dir / "scripts" / "build_roadmap_pack.py").exists(),
        "smoke_script": (root_dir / "scripts" / "integration_smoke_test.sh").exists(),
    }


def count_pages_by_section(pages: list[PageInventory]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for page in pages:
        counts[page.section_id] = counts.get(page.section_id, 0) + 1
    return counts


def count_project_dirs(projects_dir: Path) -> int:
    if not projects_dir.exists():
        return 0
    return sum(1 for path in projects_dir.iterdir() if path.is_dir() and (path / "pyproject.toml").exists())


def collect_make_targets(makefile: Path) -> dict[str, Any]:
    if not makefile.exists():
        return {"target_count": 0, "targets": [], "important_targets_present": {}}
    targets = sorted(
        {
            match.group("target")
            for line in makefile.read_text().splitlines()
            if (match := re.match(r"^(?P<target>[A-Za-z][A-Za-z0-9_-]+):", line))
        }
    )
    important_targets = [
        "docs-quality",
        "docs-build",
        "docs-inventory",
        "course-catalog",
        "infra-check",
        "infra-smoke",
        "infra-evidence",
        "release-brief",
        "workshop-packet",
        "assessment-pack",
        "roadmap-pack",
        "scripts-test",
    ]
    return {
        "target_count": len(targets),
        "targets": targets,
        "important_targets_present": {target: target in targets for target in important_targets},
    }


def write_outputs(packet: dict[str, Any], output: Path, markdown_output: Path) -> tuple[Path, Path]:
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n")
    markdown_output.write_text(render_markdown(packet))
    return output, markdown_output


def render_markdown(packet: dict[str, Any]) -> str:
    lines = [
        "# AI Infra Learning Inventory",
        "",
        f"- Generated at: `{packet['generated_at']}`",
        f"- Docs pages: `{packet['summary']['page_count']}`",
        f"- Sections: `{packet['summary']['section_count']}`",
        f"- Course tracks: `{packet['summary']['course_track_count']}`",
        f"- Missing tracked routes: `{packet['summary']['missing_track_route_count']}`",
        "",
        "## Quality Signals",
        "",
        "| Signal | Value |",
        "| --- | ---: |",
    ]
    for key, value in packet["quality_signals"].items():
        lines.append(f"| `{key}` | `{value}` |")

    lines.extend(
        [
            "",
            "## Sections",
            "",
            "| Section | Pages | Links | Code Blocks | Learning Weight |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for section in packet["sections"]:
        lines.append(
            "| "
            f"{section['title']} "
            f"| {section['page_count']} "
            f"| {section['link_count']} "
            f"| {section['code_block_count']} "
            f"| {section['learning_weight']} |"
        )

    lines.extend(["", "## Course Tracks", ""])
    for track in packet["course_tracks"]:
        lines.extend(
            [
                f"### {track['order']}. {track['title']}",
                "",
                track["goal"],
                "",
                f"- Matched routes: `{track['matched_route_count']}/{track['route_count']}`",
                f"- Learning weight: `{track['learning_weight']}`",
            ]
        )
        if track["missing_routes"]:
            lines.append(f"- Missing routes: `{', '.join(track['missing_routes'])}`")
        lines.extend(["", "| Order | Page | Route |", "| ---: | --- | --- |"])
        for index, page in enumerate(track["pages"], start=1):
            lines.append(f"| {index} | {page['title']} | `{page['route']}` |")
        lines.append("")

    lines.extend(["## Section Pages", ""])
    for section in packet["sections"]:
        lines.extend(
            [
                f"### {section['title']}",
                "",
                "| Page | Route | H2 | Links | Code |",
                "| --- | --- | ---: | ---: | ---: |",
            ]
        )
        for page in section["pages"]:
            lines.append(
                "| "
                f"{page['title']} "
                f"| `{page['route']}` "
                f"| {page['h2_count']} "
                f"| {page['link_count']} "
                f"| {page['code_block_count']} |"
            )
        lines.append("")

    lines.extend(
        [
            "## Maintenance Notes",
            "",
            "- If a new page is added, make sure it appears in the VitePress sidebar and rerun `make docs-quality`.",
            "- If a learning track changes, update `COURSE_TRACKS` in `scripts/build_learning_inventory.py`.",
            "- Use this inventory together with the evidence packet when preparing public demos or repository reviews.",
            "",
        ]
    )
    return "\n".join(lines)


def safe_relative(path: Path, root_dir: Path) -> str:
    try:
        return path.relative_to(root_dir).as_posix()
    except ValueError:
        return str(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a structured inventory for the AI Infra learning site.")
    parser.add_argument("--docs-dir", type=Path, default=DOCS_DIR)
    parser.add_argument("--root-dir", type=Path, default=ROOT_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN_OUTPUT)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    packet = build_learning_inventory(args.docs_dir, args.root_dir, strict=args.strict)
    json_target, markdown_target = write_outputs(packet, args.output, args.markdown_output)
    print(f"Wrote learning inventory JSON to {json_target}")
    print(f"Wrote learning inventory Markdown to {markdown_target}")
    print(f"Pages: {packet['summary']['page_count']}")
    print(f"Course tracks: {packet['summary']['course_track_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
