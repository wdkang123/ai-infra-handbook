"""Build a module assessment pack from the course catalog and workshop packet."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_COURSE_CATALOG = ROOT_DIR / ".tmp" / "course-catalog" / "course_catalog.json"
DEFAULT_WORKSHOP_PACKET = ROOT_DIR / ".tmp" / "workshop" / "workshop_packet.json"
DEFAULT_OUTPUT = ROOT_DIR / ".tmp" / "assessment" / "assessment_pack.json"
DEFAULT_MARKDOWN_OUTPUT = ROOT_DIR / ".tmp" / "assessment" / "assessment_pack.md"


class AssessmentPackError(RuntimeError):
    """Raised when the assessment pack cannot be built safely."""


def build_assessment_pack(
    course_catalog_path: str | Path = DEFAULT_COURSE_CATALOG,
    workshop_packet_path: str | Path = DEFAULT_WORKSHOP_PACKET,
    *,
    strict: bool = False,
) -> dict[str, Any]:
    catalog_file = Path(course_catalog_path).resolve()
    workshop_file = Path(workshop_packet_path).resolve()
    catalog = read_json_file(catalog_file, label="course catalog")
    workshop = read_json_file(workshop_file, label="workshop packet")

    validation = build_validation_summary(catalog, workshop)
    if strict:
        errors = validation_errors(validation)
        if errors:
            raise AssessmentPackError("; ".join(errors))

    workshop_cards = {module["id"]: module for module in workshop.get("module_cards", [])}
    module_assessments = [
        build_module_assessment(module, workshop_cards.get(module["id"], {})) for module in catalog.get("modules", [])
    ]
    question_count = sum(len(module["questions"]) for module in module_assessments)

    return {
        "report_type": "ai_infra_assessment_pack",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "source_files": {
            "course_catalog": str(catalog_file),
            "workshop_packet": str(workshop_file),
        },
        "summary": {
            "assessment_readiness": "ready" if not validation_errors(validation) else "review",
            "module_count": len(module_assessments),
            "question_count": question_count,
            "rubric_level_count": 4,
            "docs_pages": get_nested(catalog, ["summary", "docs_pages"], 0),
            "course_catalog_ready": validation["course_catalog_ready"],
            "workshop_packet_ready": validation["workshop_packet_ready"],
        },
        "validation": validation,
        "assessment_principles": [
            "先测系统边界，再测命令记忆。",
            "每个回答都要尽量指向页面、代码、命令或产物证据。",
            "评分时看推理链路，不只看关键词是否出现。",
            "答不稳的问题应该回流到 lab、FAQ、issue 或下一轮共学任务。",
        ],
        "module_assessments": module_assessments,
        "capstone_review": build_capstone_review(module_assessments),
        "recommended_commands": [
            "PYTHON=.venv/bin/python make docs-inventory",
            "PYTHON=.venv/bin/python make course-catalog",
            "PYTHON=.venv/bin/python make workshop-packet",
            "PYTHON=.venv/bin/python make assessment-pack",
            "PYTHON=.venv/bin/python make roadmap-pack",
            "PYTHON=.venv/bin/python make infra-release",
        ],
        "facilitator_review_flow": [
            "课前从 assessment_pack.md 选择 1 到 2 个模块作为本次测评范围。",
            "课中先让学习者独立回答 diagnostic 问题，再进入 evidence 追问。",
            "评分时使用 module rubric，要求学习者指出至少一个具体页面或产物。",
            "课后把 Level 1/2 的共性问题写入 FAQ、lab 补充或 GitHub issue。",
        ],
    }


def read_json_file(path: Path, *, label: str) -> dict[str, Any]:
    if not path.exists():
        raise AssessmentPackError(f"Missing {label}: {path}")
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise AssessmentPackError(f"Invalid {label} JSON: {path}") from exc


def build_validation_summary(catalog: dict[str, Any], workshop: dict[str, Any]) -> dict[str, Any]:
    catalog_report_type = catalog.get("report_type")
    workshop_report_type = workshop.get("report_type")
    catalog_module_count = int(get_nested(catalog, ["summary", "module_count"], 0) or 0)
    workshop_module_count = int(get_nested(workshop, ["summary", "module_count"], 0) or 0)
    missing_routes = int(get_nested(catalog, ["summary", "missing_route_count"], 0) or 0)
    missing_tracks = int(get_nested(catalog, ["summary", "missing_track_count"], 0) or 0)
    course_ready = bool(get_nested(catalog, ["summary", "ready_for_workshop"], False))
    workshop_ready = get_nested(workshop, ["summary", "packet_readiness"]) == "ready"
    public_workshop_ready = bool(get_nested(workshop, ["validation", "ready_for_public_workshop"], False))
    return {
        "course_catalog_available": catalog_report_type == "ai_infra_course_catalog",
        "workshop_packet_available": workshop_report_type == "ai_infra_workshop_packet",
        "catalog_module_count": catalog_module_count,
        "workshop_module_count": workshop_module_count,
        "module_counts_match": catalog_module_count == workshop_module_count,
        "missing_catalog_routes": missing_routes,
        "missing_catalog_tracks": missing_tracks,
        "course_catalog_ready": course_ready,
        "workshop_packet_ready": workshop_ready,
        "workshop_ready_for_public_workshop": public_workshop_ready,
        "ready_for_assessment": (
            catalog_report_type == "ai_infra_course_catalog"
            and workshop_report_type == "ai_infra_workshop_packet"
            and catalog_module_count > 0
            and catalog_module_count == workshop_module_count
            and missing_routes == 0
            and missing_tracks == 0
            and course_ready
            and workshop_ready
            and public_workshop_ready
        ),
    }


def validation_errors(validation: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not validation["course_catalog_available"]:
        errors.append("course catalog is missing or has the wrong report_type")
    if not validation["workshop_packet_available"]:
        errors.append("workshop packet is missing or has the wrong report_type")
    if validation["catalog_module_count"] <= 0:
        errors.append("course catalog has no modules")
    if not validation["module_counts_match"]:
        errors.append("course catalog and workshop packet module counts do not match")
    if validation["missing_catalog_routes"]:
        errors.append(f"course catalog has {validation['missing_catalog_routes']} missing routes")
    if validation["missing_catalog_tracks"]:
        errors.append(f"course catalog has {validation['missing_catalog_tracks']} missing tracks")
    if validation["course_catalog_available"] and not validation["course_catalog_ready"]:
        errors.append("course catalog is not ready for workshop")
    if validation["workshop_packet_available"] and not validation["workshop_packet_ready"]:
        errors.append("workshop packet is not ready")
    if validation["workshop_packet_available"] and not validation["workshop_ready_for_public_workshop"]:
        errors.append("workshop packet is not ready for public workshop")
    return errors


def build_module_assessment(module: dict[str, Any], workshop_card: dict[str, Any]) -> dict[str, Any]:
    grouped_routes = {group["id"]: group.get("pages", []) for group in module.get("route_groups", [])}
    practice_routes = route_refs(grouped_routes.get("practice", []))
    evidence_routes = route_refs(grouped_routes.get("evidence", []))
    assessment_routes = route_refs(grouped_routes.get("assessment", []))
    migration_routes = route_refs(grouped_routes.get("migration", []))
    learner_tasks = workshop_card.get("learner_tasks", [])
    evidence_expectations = workshop_card.get("evidence_expectations", [])

    questions = build_questions(module, practice_routes, evidence_routes, assessment_routes, migration_routes)
    return {
        "id": module["id"],
        "title": module["title"],
        "audience": module["audience"],
        "outcome": module["outcome"],
        "entry_route": module["entry_route"],
        "entry_title": module.get("entry_title"),
        "estimated_study_blocks": module.get("estimated_study_blocks", 0),
        "questions": questions,
        "practice_tasks": build_practice_tasks(module, learner_tasks, practice_routes),
        "evidence_requirements": build_evidence_requirements(evidence_routes, evidence_expectations),
        "rubric": build_rubric(module),
        "facilitator_prompts": build_facilitator_prompts(module, evidence_routes, migration_routes),
    }


def route_refs(pages: list[dict[str, Any]]) -> list[dict[str, str]]:
    return [{"title": page["title"], "route": page["route"]} for page in pages]


def build_questions(
    module: dict[str, Any],
    practice_routes: list[dict[str, str]],
    evidence_routes: list[dict[str, str]],
    assessment_routes: list[dict[str, str]],
    migration_routes: list[dict[str, str]],
) -> list[dict[str, str]]:
    questions = [
        {
            "id": f"{module['id']}-q1",
            "type": "diagnostic",
            "prompt": f"这个模块的核心工程问题是什么？请结合 `{module['entry_route']}` 说明。",
            "look_for": "能说清模块目标、上游/下游边界，以及为什么它属于 AI Infra 主线。",
        },
        {
            "id": f"{module['id']}-q2",
            "type": "boundary",
            "prompt": "这个模块里哪些能力是学习型脚手架，哪些接口或观测习惯可以迁移到真实系统？",
            "look_for": "能主动承认 mock 或简化边界，同时保留可迁移的契约、证据和验证方式。",
        },
    ]
    if module.get("checkpoints"):
        questions.append(
            {
                "id": f"{module['id']}-q3",
                "type": "checkpoint",
                "prompt": module["checkpoints"][0],
                "look_for": "回答要具体，最好能指向页面、命令、输出或代码入口。",
            }
        )
    if practice_routes:
        questions.append(
            {
                "id": f"{module['id']}-q4",
                "type": "practice",
                "prompt": f"如果从 `{practice_routes[0]['route']}` 开始练，你会先跑什么命令，观察什么结果？",
                "look_for": "能把 lab 步骤、验证命令和失败处理连起来。",
            }
        )
    if evidence_routes:
        questions.append(
            {
                "id": f"{module['id']}-q5",
                "type": "evidence",
                "prompt": f"引用 `{evidence_routes[0]['route']}` 中的一类证据，说明它能证明什么，不能证明什么。",
                "look_for": "能区分运行证据、课程证据、发布证据和生产质量证据。",
            }
        )
    if assessment_routes:
        questions.append(
            {
                "id": f"{module['id']}-q6",
                "type": "self-check",
                "prompt": f"用 `{assessment_routes[0]['route']}` 做一次短答辩，说明你最不确定的问题。",
                "look_for": "能把不确定点转成下一步阅读、实验或 issue。",
            }
        )
    if migration_routes:
        questions.append(
            {
                "id": f"{module['id']}-q7",
                "type": "migration",
                "prompt": f"如果参考 `{migration_routes[0]['route']}` 继续生产迁移，第一步应该替换或加固什么？",
                "look_for": "能说明迁移顺序、风险和应该补的验证命令。",
            }
        )
    return questions


def build_practice_tasks(
    module: dict[str, Any], learner_tasks: list[str], practice_routes: list[dict[str, str]]
) -> list[str]:
    tasks = list(learner_tasks[:3])
    if not tasks:
        tasks = [
            f"阅读 `{module['entry_route']}`，写下本模块的上游、下游和核心产物。",
            "选择一个检查点，用自己的话解释并指出证据来源。",
        ]
    if practice_routes:
        tasks.append(f"完成 `{practice_routes[0]['route']}`，并记录一条成功路径和一条失败路径。")
    tasks.append("用 3 到 5 分钟口头说明：我验证了什么、还不能证明什么、下一步该补什么。")
    return dedupe_keep_order(tasks)


def build_evidence_requirements(evidence_routes: list[dict[str, str]], evidence_expectations: list[str]) -> list[str]:
    requirements = list(evidence_expectations[:3])
    for route in evidence_routes[:2]:
        requirements.append(f"至少引用 `{route['route']}` 中的一项证据，并解释它的适用边界。")
    requirements.append("至少记录一个无法靠当前证据回答的问题，作为后续复盘入口。")
    return dedupe_keep_order(requirements)


def build_rubric(module: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "level": "Level 1",
            "label": "能复述",
            "criteria": f"能说出 `{module['title']}` 的关键词，但还不能解释上游、下游或失败路径。",
        },
        {
            "level": "Level 2",
            "label": "能运行",
            "criteria": "能找到入口页面、完成基础命令，并指出至少一个相关产物或页面。",
        },
        {
            "level": "Level 3",
            "label": "能复盘",
            "criteria": "能解释正常路径和失败路径，并能用证据说明自己为什么这样判断。",
        },
        {
            "level": "Level 4",
            "label": "能改进",
            "criteria": "能提出一个小而清楚的改进方案，并说明风险、验证命令和文档同步点。",
        },
    ]


def build_facilitator_prompts(
    module: dict[str, Any], evidence_routes: list[dict[str, str]], migration_routes: list[dict[str, str]]
) -> list[str]:
    prompts = [
        f"如果学习者只读 `{module['entry_route']}`，他最可能误解什么？",
        "请学习者指出一个真实系统会比当前学习型实现更复杂的地方。",
        "请学习者把一个回答改写成 GitHub issue 标题。",
    ]
    if evidence_routes:
        prompts.append(f"追问：`{evidence_routes[0]['route']}` 里的证据能否支撑公开演示？为什么？")
    if migration_routes:
        prompts.append(f"追问：`{migration_routes[0]['route']}` 的第一步迁移会带来什么测试压力？")
    return prompts


def build_capstone_review(module_assessments: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "goal": "把多个模块的理解合成一次 8 到 10 分钟系统答辩。",
        "minimum_scope": [module["id"] for module in module_assessments[:4]],
        "required_evidence": [
            "一张系统分层图或文字版调用链。",
            "至少两条实际验证命令。",
            "至少两份生成产物或运行证据。",
            "一个学习型边界和一个生产迁移方向。",
        ],
        "review_prompts": [
            "四层系统分别解决什么问题？",
            "一次请求或一次模型迭代如何跨层留下证据？",
            "当前最容易被误解成生产能力的是哪一部分？",
            "如果只能改一个点来提升公开学习价值，你会改什么？",
        ],
    }


def get_nested(payload: dict[str, Any], path: list[str], default: Any = None) -> Any:
    current: Any = payload
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped


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
        "# AI Infra Assessment Pack",
        "",
        f"- Generated at: `{packet['generated_at']}`",
        f"- Assessment readiness: `{summary['assessment_readiness']}`",
        f"- Modules: `{summary['module_count']}`",
        f"- Questions: `{summary['question_count']}`",
        f"- Rubric levels: `{summary['rubric_level_count']}`",
        f"- Docs pages: `{summary['docs_pages']}`",
        "",
        "## Validation",
        "",
        "| Signal | Value |",
        "| --- | --- |",
    ]
    for key, value in validation.items():
        lines.append(f"| `{key}` | `{value}` |")

    lines.extend(["", "## Assessment Principles", ""])
    lines.extend(f"- {item}" for item in packet["assessment_principles"])

    lines.extend(["", "## Module Assessments", ""])
    for module in packet["module_assessments"]:
        lines.extend(
            [
                f"### {module['title']}",
                "",
                f"- Audience: {module['audience']}",
                f"- Outcome: {module['outcome']}",
                f"- Entry: `{module['entry_title']}` (`{module['entry_route']}`)",
                f"- Estimated study blocks: `{module['estimated_study_blocks']}`",
                "",
                "Questions:",
            ]
        )
        for question in module["questions"]:
            lines.append(f"- `{question['type']}` {question['prompt']} Look for: {question['look_for']}")
        lines.extend(["", "Practice tasks:"])
        lines.extend(f"- {task}" for task in module["practice_tasks"])
        lines.extend(["", "Evidence requirements:"])
        lines.extend(f"- {item}" for item in module["evidence_requirements"])
        lines.extend(["", "Rubric:"])
        for rubric in module["rubric"]:
            lines.append(f"- `{rubric['level']}` {rubric['label']}: {rubric['criteria']}")
        lines.extend(["", "Facilitator prompts:"])
        lines.extend(f"- {prompt}" for prompt in module["facilitator_prompts"])
        lines.append("")

    capstone = packet["capstone_review"]
    lines.extend(["## Capstone Review", "", f"- Goal: {capstone['goal']}"])
    lines.append(f"- Minimum scope: `{', '.join(capstone['minimum_scope'])}`")
    lines.extend(["", "Required evidence:"])
    lines.extend(f"- {item}" for item in capstone["required_evidence"])
    lines.extend(["", "Review prompts:"])
    lines.extend(f"- {item}" for item in capstone["review_prompts"])

    lines.extend(["", "## Facilitator Review Flow", ""])
    lines.extend(f"- {item}" for item in packet["facilitator_review_flow"])
    lines.extend(["", "## Recommended Commands", ""])
    lines.extend(f"- `{command}`" for command in packet["recommended_commands"])
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build an assessment pack for the AI Infra learning site.")
    parser.add_argument("--course-catalog", type=Path, default=DEFAULT_COURSE_CATALOG)
    parser.add_argument("--workshop-packet", type=Path, default=DEFAULT_WORKSHOP_PACKET)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN_OUTPUT)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    packet = build_assessment_pack(args.course_catalog, args.workshop_packet, strict=args.strict)
    json_target, markdown_target = write_outputs(packet, args.output, args.markdown_output)
    print(f"Assessment pack written to {json_target}")
    print(f"Assessment pack markdown written to {markdown_target}")
    print(f"Assessment readiness: {packet['summary']['assessment_readiness']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
