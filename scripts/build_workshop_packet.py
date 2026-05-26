"""Build a shareable workshop packet from the course catalog and release brief."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_COURSE_CATALOG = ROOT_DIR / ".tmp" / "course-catalog" / "course_catalog.json"
DEFAULT_RELEASE_BRIEF = ROOT_DIR / ".tmp" / "release" / "release_brief.json"
DEFAULT_OUTPUT = ROOT_DIR / ".tmp" / "workshop" / "workshop_packet.json"
DEFAULT_MARKDOWN_OUTPUT = ROOT_DIR / ".tmp" / "workshop" / "workshop_packet.md"


class WorkshopPacketError(RuntimeError):
    """Raised when the workshop packet cannot be built safely."""


def build_workshop_packet(
    course_catalog_path: str | Path = DEFAULT_COURSE_CATALOG,
    release_brief_path: str | Path = DEFAULT_RELEASE_BRIEF,
    *,
    strict: bool = False,
) -> dict[str, Any]:
    catalog_file = Path(course_catalog_path).resolve()
    release_file = Path(release_brief_path).resolve()
    catalog = read_json_file(catalog_file, label="course catalog")
    release_brief = read_json_file(release_file, label="release brief")

    validation = build_validation_summary(catalog, release_brief)
    if strict:
        errors = validation_errors(validation)
        if errors:
            raise WorkshopPacketError("; ".join(errors))

    module_cards = [build_module_card(module) for module in catalog.get("modules", [])]
    packet = {
        "report_type": "ai_infra_workshop_packet",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "source_files": {
            "course_catalog": str(catalog_file),
            "release_brief": str(release_file),
        },
        "summary": {
            "packet_readiness": "ready" if not validation_errors(validation) else "review",
            "module_count": len(module_cards),
            "estimated_study_blocks": get_nested(catalog, ["summary", "estimated_study_blocks"], 0),
            "docs_pages": get_nested(catalog, ["summary", "docs_pages"], 0),
            "course_catalog_ready": validation["course_catalog_ready"],
            "release_brief_ready": validation["release_brief_ready"],
        },
        "validation": validation,
        "facilitation_principles": [
            "先让学习者选一个目标模块，再进入命令和产物。",
            "每个模块都要留下学习记录、运行证据和一个复盘问题。",
            "公开讲解时保持学习型边界，不把 mock 实现说成生产能力。",
            "把反馈整理成 issue、PR 或下一轮课程任务，而不是只停留在口头讨论。",
        ],
        "agenda_templates": build_agenda_templates(module_cards),
        "module_cards": module_cards,
        "learner_deliverables": [
            "一段说明自己选择了哪个模块、为什么选择它的学习目标记录。",
            "至少一条实际运行过的命令和对应输出路径。",
            "一份证据引用清单，指向 events、report、manifest 或 generated packet。",
            "一个还不能解释清楚的问题，转成后续 issue 或学习任务。",
            "一次 3 到 5 分钟模块复盘，说明系统边界和下一步改进。",
        ],
        "facilitator_checklist": build_facilitator_checklist(release_brief),
        "recommended_commands": [
            "PYTHON=.venv/bin/python make docs-inventory",
            "PYTHON=.venv/bin/python make course-catalog",
            "PYTHON=.venv/bin/python make release-brief",
            "PYTHON=.venv/bin/python make workshop-packet",
            "PYTHON=.venv/bin/python make assessment-pack",
            "PYTHON=.venv/bin/python make roadmap-pack",
            "PYTHON=.venv/bin/python make launch-pack",
            "PYTHON=.venv/bin/python make infra-release",
        ],
        "review_questions": [
            "这次共学是否让每位学习者都选到了明确模块？",
            "每个模块是否都留下了可复盘的命令、输出和解释？",
            "哪些页面在带练过程中仍然需要讲师口头补充？",
            "哪些反馈应该转成 GitHub issue、PR 或下一轮课程任务？",
        ],
    }
    return packet


def read_json_file(path: Path, *, label: str) -> dict[str, Any]:
    if not path.exists():
        raise WorkshopPacketError(f"Missing {label}: {path}")
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise WorkshopPacketError(f"Invalid {label} JSON: {path}") from exc


def build_validation_summary(catalog: dict[str, Any], release_brief: dict[str, Any]) -> dict[str, Any]:
    catalog_report_type = catalog.get("report_type")
    release_report_type = release_brief.get("report_type")
    module_count = int(get_nested(catalog, ["summary", "module_count"], 0) or 0)
    missing_routes = int(get_nested(catalog, ["summary", "missing_route_count"], 0) or 0)
    missing_tracks = int(get_nested(catalog, ["summary", "missing_track_count"], 0) or 0)
    course_ready = bool(get_nested(catalog, ["summary", "ready_for_workshop"], False))
    release_ready = get_nested(release_brief, ["summary", "release_readiness"]) == "ready"
    public_review_ready = bool(get_nested(release_brief, ["validation", "ready_for_public_review"], False))
    return {
        "course_catalog_available": catalog_report_type == "ai_infra_course_catalog",
        "release_brief_available": release_report_type == "ai_infra_release_brief",
        "module_count": module_count,
        "missing_catalog_routes": missing_routes,
        "missing_catalog_tracks": missing_tracks,
        "course_catalog_ready": course_ready,
        "release_brief_ready": release_ready,
        "release_ready_for_public_review": public_review_ready,
        "ready_for_public_workshop": (
            catalog_report_type == "ai_infra_course_catalog"
            and release_report_type == "ai_infra_release_brief"
            and module_count > 0
            and missing_routes == 0
            and missing_tracks == 0
            and course_ready
            and release_ready
            and public_review_ready
        ),
    }


def validation_errors(validation: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not validation["course_catalog_available"]:
        errors.append("course catalog is missing or has the wrong report_type")
    if not validation["release_brief_available"]:
        errors.append("release brief is missing or has the wrong report_type")
    if validation["module_count"] <= 0:
        errors.append("course catalog has no modules")
    if validation["missing_catalog_routes"]:
        errors.append(f"course catalog has {validation['missing_catalog_routes']} missing routes")
    if validation["missing_catalog_tracks"]:
        errors.append(f"course catalog has {validation['missing_catalog_tracks']} missing tracks")
    if validation["course_catalog_available"] and not validation["course_catalog_ready"]:
        errors.append("course catalog is not ready for workshop")
    if validation["release_brief_available"] and not validation["release_brief_ready"]:
        errors.append("release brief is not ready")
    if validation["release_brief_available"] and not validation["release_ready_for_public_review"]:
        errors.append("release brief is not ready for public review")
    return errors


def build_module_card(module: dict[str, Any]) -> dict[str, Any]:
    grouped_routes = {group["id"]: group.get("pages", []) for group in module.get("route_groups", [])}
    orient_routes = route_titles(grouped_routes.get("orient", []))
    core_routes = route_titles(grouped_routes.get("core", []))
    practice_routes = route_titles(grouped_routes.get("practice", []))
    evidence_routes = route_titles(grouped_routes.get("evidence", []))
    assessment_routes = route_titles(grouped_routes.get("assessment", []))
    migration_routes = route_titles(grouped_routes.get("migration", []))
    share_routes = route_titles(grouped_routes.get("share", []))

    return {
        "id": module["id"],
        "title": module["title"],
        "audience": module["audience"],
        "outcome": module["outcome"],
        "entry_route": module["entry_route"],
        "entry_title": module.get("entry_title"),
        "estimated_study_blocks": module.get("estimated_study_blocks", 0),
        "learning_sequence": [
            *build_sequence_item("建立地图", orient_routes),
            *build_sequence_item("核心阅读", core_routes),
            *build_sequence_item("动手练习", practice_routes),
            *build_sequence_item("证据输出", evidence_routes),
            *build_sequence_item("自测与答辩", assessment_routes),
            *build_sequence_item("公开分享", share_routes),
            *build_sequence_item("生产迁移", migration_routes),
        ],
        "checkpoints": module.get("checkpoints", []),
        "facilitator_notes": module.get("facilitator_notes", []),
        "learner_tasks": build_learner_tasks(module, practice_routes, evidence_routes, assessment_routes),
        "evidence_expectations": build_evidence_expectations(module["id"], evidence_routes),
        "discussion_prompts": build_discussion_prompts(module),
    }


def route_titles(pages: list[dict[str, Any]]) -> list[dict[str, str]]:
    return [{"title": page["title"], "route": page["route"]} for page in pages]


def build_sequence_item(label: str, routes: list[dict[str, str]]) -> list[dict[str, Any]]:
    if not routes:
        return []
    return [{"label": label, "routes": routes}]


def build_learner_tasks(
    module: dict[str, Any],
    practice_routes: list[dict[str, str]],
    evidence_routes: list[dict[str, str]],
    assessment_routes: list[dict[str, str]],
) -> list[str]:
    tasks = [
        f"先读入口页 `{module['entry_route']}`，写下这个模块要解决的一个工程问题。",
        "从学习序列里选择 2 到 3 个页面，记录最关键的系统边界。",
    ]
    if practice_routes:
        tasks.append(f"完成 `{practice_routes[0]['route']}`，记录命令、输出和失败处理过程。")
    if evidence_routes:
        tasks.append(f"引用 `{evidence_routes[0]['route']}` 中的一类证据，说明它能证明什么。")
    if assessment_routes:
        tasks.append(f"用 `{assessment_routes[0]['route']}` 做一次自测或短答辩。")
    tasks.append("最后用 3 到 5 分钟讲清本模块的当前边界和下一步改进。")
    return tasks


def build_evidence_expectations(module_id: str, evidence_routes: list[dict[str, str]]) -> list[str]:
    baseline = {
        "zero-to-one": ["能指向学习清单或系统地图，说明学习路径没有断。"],
        "serving-engineer": ["能指向 request id、events、metrics 或 streaming 输出。"],
        "platform-engineer": ["能指向 gateway header、failure summary 或 fallback 记录。"],
        "eval-release": ["能指向 eval result、comparison、leaderboard 或 sample analysis。"],
        "training-lineage": ["能指向 run manifest、checkpoint index、export manifest 或 lineage。"],
        "public-sharing": ["能指向 course catalog、evidence packet、release brief 或 GitHub 发布计划。"],
        "production-migration": ["能指向验证矩阵、迁移页或 capstone 答辩稿。"],
    }.get(module_id, ["能指向至少一份可复盘的页面或生成产物。"])
    route_expectations = [f"参考 `{route['route']}`，说明这类证据适合放进哪种复盘。" for route in evidence_routes]
    return [*baseline, *route_expectations]


def build_discussion_prompts(module: dict[str, Any]) -> list[str]:
    return [
        f"如果只保留 `{module['entry_route']}` 这一个入口，学习者还缺哪类上下文？",
        "这个模块里哪些能力是学习型脚手架，哪些边界可以迁移到真实系统？",
        "如果要把这个模块变成一个 issue，最小可交付改动是什么？",
    ]


def build_agenda_templates(module_cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    focus_modules = [module["id"] for module in module_cards[:3]]
    return [
        {
            "id": "ninety-minute",
            "title": "90 分钟快速共学",
            "best_for": "第一次线上分享或小范围试讲。",
            "module_scope": focus_modules,
            "segments": [
                {"minutes": 10, "activity": "说明项目定位、学习型边界和今天的模块选择。"},
                {"minutes": 20, "activity": "按课程目录选择一个模块，快速读入口页和核心问题。"},
                {"minutes": 25, "activity": "跑一个最小命令或阅读一份产物，记录证据。"},
                {"minutes": 20, "activity": "学习者用 evidence expectations 做短复盘。"},
                {"minutes": 15, "activity": "收集卡点，转成 issue、FAQ 或下一轮任务。"},
            ],
        },
        {
            "id": "half-day",
            "title": "半天模块深挖",
            "best_for": "已经能本地运行，希望理解系统边界的学习小组。",
            "module_scope": [module["id"] for module in module_cards[:5]],
            "segments": [
                {"minutes": 20, "activity": "统一系统地图和验证命令。"},
                {"minutes": 45, "activity": "分组阅读 serving / gateway / eval / training 中的一个模块。"},
                {"minutes": 60, "activity": "完成对应 lab 或证据页复盘。"},
                {"minutes": 45, "activity": "每组展示一份证据和一个失败路径。"},
                {"minutes": 30, "activity": "用 release brief 和 workshop packet 收束下一步。"},
            ],
        },
        {
            "id": "two-week",
            "title": "两周共学节奏",
            "best_for": "准备持续共学、写系列文章或公开维护 GitHub 项目。",
            "module_scope": [module["id"] for module in module_cards],
            "segments": [
                {"day": "Day 1-2", "activity": "从 0 到 1 模块，完成环境和系统地图。"},
                {"day": "Day 3-5", "activity": "serving 与 gateway 模块，完成请求和失败路径复盘。"},
                {"day": "Day 6-8", "activity": "eval 与 training 模块，完成结果判断和资产复现。"},
                {"day": "Day 9-11", "activity": "案例、证据库和 capstone，形成端到端讲解。"},
                {"day": "Day 12-14", "activity": "公开发布、workshop packet、release brief 和反馈计划。"},
            ],
        },
    ]


def build_facilitator_checklist(release_brief: dict[str, Any]) -> list[str]:
    summary = release_brief.get("summary", {})
    return [
        f"确认 release readiness 当前为 `{summary.get('release_readiness')}`。",
        f"确认文档页数当前为 `{summary.get('docs_pages')}`，课程主线为 `{summary.get('course_tracks')}`。",
        "课前运行 `make workshop-packet`，把生成的 Markdown 作为讲师备忘。",
        "课中只选 1 到 2 个模块深挖，避免把全站一次讲完。",
        "课后把反馈按 docs、lab、evidence、workflow 四类整理成 issue。",
    ]


def get_nested(payload: dict[str, Any], path: list[str], default: Any = None) -> Any:
    current: Any = payload
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def write_outputs(packet: dict[str, Any], output: str | Path, markdown_output: str | Path) -> tuple[Path, Path]:
    json_path = Path(output)
    markdown_path = Path(markdown_output)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n")
    markdown_path.write_text(render_markdown(packet))
    return json_path, markdown_path


def render_markdown(packet: dict[str, Any]) -> str:
    summary = packet["summary"]
    validation = packet["validation"]
    lines = [
        "# AI Infra Workshop Packet",
        "",
        f"- Generated at: `{packet['generated_at']}`",
        f"- Packet readiness: `{summary['packet_readiness']}`",
        f"- Modules: `{summary['module_count']}`",
        f"- Estimated study blocks: `{summary['estimated_study_blocks']}`",
        f"- Docs pages: `{summary['docs_pages']}`",
        "",
        "## Validation",
        "",
        "| Signal | Value |",
        "| --- | --- |",
    ]
    for key, value in validation.items():
        lines.append(f"| `{key}` | `{value}` |")

    lines.extend(["", "## Facilitation Principles", ""])
    lines.extend(f"- {item}" for item in packet["facilitation_principles"])

    lines.extend(["", "## Agenda Templates", ""])
    for agenda in packet["agenda_templates"]:
        lines.extend([f"### {agenda['title']}", "", f"- Best for: {agenda['best_for']}"])
        if agenda.get("module_scope"):
            lines.append(f"- Module scope: `{', '.join(agenda['module_scope'])}`")
        lines.extend(["", "| Time | Activity |", "| --- | --- |"])
        for segment in agenda["segments"]:
            label = f"{segment['minutes']} min" if "minutes" in segment else segment["day"]
            lines.append(f"| {label} | {segment['activity']} |")
        lines.append("")

    lines.extend(["## Module Cards", ""])
    for module in packet["module_cards"]:
        lines.extend(
            [
                f"### {module['title']}",
                "",
                f"- Audience: {module['audience']}",
                f"- Outcome: {module['outcome']}",
                f"- Entry: `{module['entry_title']}` (`{module['entry_route']}`)",
                f"- Estimated study blocks: `{module['estimated_study_blocks']}`",
                "",
                "Learning sequence:",
            ]
        )
        for sequence in module["learning_sequence"]:
            routes = ", ".join(f"`{route['route']}`" for route in sequence["routes"])
            lines.append(f"- {sequence['label']}: {routes}")
        lines.extend(["", "Learner tasks:"])
        lines.extend(f"- {task}" for task in module["learner_tasks"])
        lines.extend(["", "Evidence expectations:"])
        lines.extend(f"- {item}" for item in module["evidence_expectations"])
        lines.extend(["", "Discussion prompts:"])
        lines.extend(f"- {item}" for item in module["discussion_prompts"])
        lines.append("")

    lines.extend(["## Learner Deliverables", ""])
    lines.extend(f"- {item}" for item in packet["learner_deliverables"])
    lines.extend(["", "## Facilitator Checklist", ""])
    lines.extend(f"- {item}" for item in packet["facilitator_checklist"])
    lines.extend(["", "## Recommended Commands", ""])
    lines.extend(f"- `{command}`" for command in packet["recommended_commands"])
    lines.extend(["", "## Review Questions", ""])
    lines.extend(f"- {question}" for question in packet["review_questions"])
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a shareable workshop packet for the AI Infra learning site.")
    parser.add_argument("--course-catalog", type=Path, default=DEFAULT_COURSE_CATALOG)
    parser.add_argument("--release-brief", type=Path, default=DEFAULT_RELEASE_BRIEF)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN_OUTPUT)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    packet = build_workshop_packet(args.course_catalog, args.release_brief, strict=args.strict)
    json_target, markdown_target = write_outputs(packet, args.output, args.markdown_output)
    print(f"Workshop packet written to {json_target}")
    print(f"Workshop packet markdown written to {markdown_target}")
    print(f"Packet readiness: {packet['summary']['packet_readiness']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
