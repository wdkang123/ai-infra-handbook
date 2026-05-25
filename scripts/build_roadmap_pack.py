"""Build GitHub-ready roadmap issue seeds from release and assessment artifacts."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_RELEASE_BRIEF = ROOT_DIR / ".tmp" / "release" / "release_brief.json"
DEFAULT_ASSESSMENT_PACK = ROOT_DIR / ".tmp" / "assessment" / "assessment_pack.json"
DEFAULT_OUTPUT = ROOT_DIR / ".tmp" / "roadmap" / "roadmap_pack.json"
DEFAULT_MARKDOWN_OUTPUT = ROOT_DIR / ".tmp" / "roadmap" / "roadmap_pack.md"


class RoadmapPackError(RuntimeError):
    """Raised when the roadmap pack cannot be built safely."""


def build_roadmap_pack(
    release_brief_path: str | Path = DEFAULT_RELEASE_BRIEF,
    assessment_pack_path: str | Path = DEFAULT_ASSESSMENT_PACK,
    *,
    strict: bool = False,
) -> dict[str, Any]:
    release_file = Path(release_brief_path).resolve()
    assessment_file = Path(assessment_pack_path).resolve()
    release_brief = read_json_file(release_file, label="release brief")
    assessment_pack = read_json_file(assessment_file, label="assessment pack")

    validation = build_validation_summary(release_brief, assessment_pack)
    if strict:
        errors = validation_errors(validation)
        if errors:
            raise RoadmapPackError("; ".join(errors))

    module_issues = [build_module_issue(module) for module in assessment_pack.get("module_assessments", [])]
    launch_issues = build_launch_issues(release_brief, assessment_pack)
    issue_seeds = [*module_issues, *launch_issues]

    return {
        "report_type": "ai_infra_roadmap_pack",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "source_files": {
            "release_brief": str(release_file),
            "assessment_pack": str(assessment_file),
        },
        "summary": {
            "roadmap_readiness": "ready" if not validation_errors(validation) else "review",
            "issue_seed_count": len(issue_seeds),
            "module_issue_count": len(module_issues),
            "launch_issue_count": len(launch_issues),
            "docs_pages": get_nested(assessment_pack, ["summary", "docs_pages"], 0),
            "release_brief_ready": validation["release_brief_ready"],
            "assessment_pack_ready": validation["assessment_pack_ready"],
        },
        "validation": validation,
        "roadmap_principles": [
            "每条 issue 都要说明学习价值，不只描述要改什么。",
            "首批 issue 应该小而清楚，方便 first-time contributor 参与。",
            "涉及学习路径的 issue 必须包含验收命令和文档同步点。",
            "不要把学习型项目包装成生产承诺，路线图只表达下一步探索方向。",
        ],
        "issue_seeds": issue_seeds,
        "recommended_labels": build_recommended_labels(),
        "recommended_commands": [
            "PYTHON=.venv/bin/python make release-brief",
            "PYTHON=.venv/bin/python make assessment-pack",
            "PYTHON=.venv/bin/python make roadmap-pack",
            "PYTHON=.venv/bin/python make infra-release",
            "npm audit --omit=dev --audit-level=moderate",
        ],
        "publication_flow": [
            "发布前用 roadmap_pack.md 选择 5 到 8 条首批 issue。",
            "每条 issue 保留 learning value、suggested files、acceptance criteria 和 verification commands。",
            "先创建 2 到 3 条 good first issue，再创建较深的 migration 或 implementation issue。",
            "首发后 30 天把 workshop feedback 和 assessment weak spots 回流到 roadmap issue。",
        ],
    }


def read_json_file(path: Path, *, label: str) -> dict[str, Any]:
    if not path.exists():
        raise RoadmapPackError(f"Missing {label}: {path}")
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise RoadmapPackError(f"Invalid {label} JSON: {path}") from exc


def build_validation_summary(release_brief: dict[str, Any], assessment_pack: dict[str, Any]) -> dict[str, Any]:
    release_report_type = release_brief.get("report_type")
    assessment_report_type = assessment_pack.get("report_type")
    release_ready = get_nested(release_brief, ["summary", "release_readiness"]) == "ready"
    public_review_ready = bool(get_nested(release_brief, ["validation", "ready_for_public_review"], False))
    assessment_ready = get_nested(assessment_pack, ["summary", "assessment_readiness"]) == "ready"
    ready_for_assessment = bool(get_nested(assessment_pack, ["validation", "ready_for_assessment"], False))
    module_count = int(get_nested(assessment_pack, ["summary", "module_count"], 0) or 0)
    question_count = int(get_nested(assessment_pack, ["summary", "question_count"], 0) or 0)
    return {
        "release_brief_available": release_report_type == "ai_infra_release_brief",
        "assessment_pack_available": assessment_report_type == "ai_infra_assessment_pack",
        "release_brief_ready": release_ready,
        "release_ready_for_public_review": public_review_ready,
        "assessment_pack_ready": assessment_ready,
        "assessment_ready_for_review": ready_for_assessment,
        "module_count": module_count,
        "question_count": question_count,
        "ready_for_public_roadmap": (
            release_report_type == "ai_infra_release_brief"
            and assessment_report_type == "ai_infra_assessment_pack"
            and release_ready
            and public_review_ready
            and assessment_ready
            and ready_for_assessment
            and module_count > 0
            and question_count > 0
        ),
    }


def validation_errors(validation: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not validation["release_brief_available"]:
        errors.append("release brief is missing or has the wrong report_type")
    if not validation["assessment_pack_available"]:
        errors.append("assessment pack is missing or has the wrong report_type")
    if validation["release_brief_available"] and not validation["release_brief_ready"]:
        errors.append("release brief is not ready")
    if validation["release_brief_available"] and not validation["release_ready_for_public_review"]:
        errors.append("release brief is not ready for public review")
    if validation["assessment_pack_available"] and not validation["assessment_pack_ready"]:
        errors.append("assessment pack is not ready")
    if validation["assessment_pack_available"] and not validation["assessment_ready_for_review"]:
        errors.append("assessment pack is not ready for review")
    if validation["module_count"] <= 0:
        errors.append("assessment pack has no modules")
    if validation["question_count"] <= 0:
        errors.append("assessment pack has no questions")
    return errors


def build_module_issue(module: dict[str, Any]) -> dict[str, Any]:
    module_id = module["id"]
    title = module["title"]
    questions = module.get("questions") or [{}]
    evidence_requirements = module.get("evidence_requirements") or ["至少补充一条可复盘证据。"]
    primary_question = questions[0].get("prompt", f"深化 {title} 的学习任务。")
    evidence_requirement = evidence_requirements[0]
    suggested_files = route_files([module.get("entry_route", ""), *extract_routes(module)])
    return {
        "id": f"module-{module_id}-depth",
        "title": f"[Docs] Deepen {title}",
        "labels": ["documentation", "enhancement", "good first issue"],
        "priority": "P1",
        "source_module": module_id,
        "learning_value": f"帮助学习者回答：{primary_question}",
        "scope": [
            "补充一个更具体的例子或失败路径。",
            "补充至少一个证据解释，说明它能证明什么、不能证明什么。",
            "确认模块入口、lab、自测和产物说明互相能连起来。",
        ],
        "suggested_files": suggested_files[:6],
        "acceptance_criteria": [
            "页面解释比当前版本更容易让第一次学习者理解。",
            "至少有一个具体命令、输出字段或产物路径可供读者复盘。",
            f"保留学习型边界：{evidence_requirement}",
        ],
        "verification_commands": [
            "PYTHON=.venv/bin/python make docs-quality",
            "PYTHON=.venv/bin/python make assessment-pack",
        ],
    }


def build_launch_issues(release_brief: dict[str, Any], assessment_pack: dict[str, Any]) -> list[dict[str, Any]]:
    docs_pages = get_nested(assessment_pack, ["summary", "docs_pages"], 0)
    release_readiness = get_nested(release_brief, ["summary", "release_readiness"], "review")
    return [
        {
            "id": "launch-faq-from-assessment",
            "title": "[Docs] Add FAQ entries from assessment weak spots",
            "labels": ["documentation", "good first issue", "question"],
            "priority": "P0",
            "source_module": "cross-cutting",
            "learning_value": "把测评中 Level 1/2 的常见卡点回流到 FAQ，降低第一次学习门槛。",
            "scope": [
                "从 assessment_pack.md 选择 3 到 5 个最容易答浅的问题。",
                "为每个问题补一个 FAQ 条目或前后链接。",
                "避免新增大段概念堆叠，优先给出读者下一步该看哪里。",
            ],
            "suggested_files": ["docs/00-overview/10-faq.md", "docs/10-assessments/06-generated-assessment-pack.md"],
            "acceptance_criteria": [
                "FAQ 至少新增或改进 3 个问题。",
                "每个 FAQ 条目都链接到一个具体学习页或 lab。",
                f"当前站点规模 `{docs_pages}` 页，新增内容不能破坏导航。",
            ],
            "verification_commands": ["PYTHON=.venv/bin/python make docs-quality"],
        },
        {
            "id": "launch-evidence-gallery-depth",
            "title": "[Evidence] Add more public-demo evidence snippets",
            "labels": ["documentation", "evidence", "enhancement"],
            "priority": "P1",
            "source_module": "cross-cutting",
            "learning_value": "让读者跑完命令后更容易判断输出是否正确，而不是只看到抽象说明。",
            "scope": [
                "为 serving/gateway、eval、finetune 各补一条脱敏示例输出或字段解释。",
                "写清每个字段能证明什么，哪些情况不能过度解读。",
                "把新增证据链接回对应 lab 或案例复盘。",
            ],
            "suggested_files": [
                "docs/13-output-gallery/01-serving-gateway-evidence.md",
                "docs/13-output-gallery/02-eval-report-evidence.md",
                "docs/13-output-gallery/03-finetune-artifact-evidence.md",
            ],
            "acceptance_criteria": [
                "至少 3 个证据片段得到补充。",
                "每个片段都有字段解释和常见误读。",
                "新增内容不包含真实密钥、私有 endpoint 或敏感日志。",
            ],
            "verification_commands": ["PYTHON=.venv/bin/python make docs-quality"],
        },
        {
            "id": "launch-openai-compatible-serving-guide",
            "title": "[Docs] Add real OpenAI-compatible serving migration guide",
            "labels": ["documentation", "enhancement"],
            "priority": "P2",
            "source_module": "production-migration",
            "learning_value": "给进阶读者一条从 mock serving 迁移到真实 OpenAI-compatible backend 的路径。",
            "scope": [
                "说明前置条件、环境变量、启动命令和失败排查入口。",
                "保留 mock 路径，避免让第一次学习者必须安装重型 serving backend。",
                "补充验证命令和输出证据。",
            ],
            "suggested_files": [
                "docs/12-production-migration/01-serving-backend-migration.md",
                "docs/02-inference-serving/10-from-learning-service-to-real-serving-stack.md",
                "projects/inference-service/README.md",
            ],
            "acceptance_criteria": [
                "读者能区分 mock engine 和 OpenAI-compatible engine。",
                "新增路径有清晰前置条件和失败排查说明。",
                "不把真实接入路径变成默认必需依赖。",
            ],
            "verification_commands": [
                "PYTHON=.venv/bin/python make docs-quality",
                "PYTHON=.venv/bin/python make inference-test",
            ],
        },
        {
            "id": "launch-eval-judge-adapter-example",
            "title": "[Eval] Add a minimal judge adapter example",
            "labels": ["enhancement", "documentation"],
            "priority": "P2",
            "source_module": "eval-release",
            "learning_value": "让 sample-level evaluation 更接近真实评测，同时保留当前可读的学习路径。",
            "scope": [
                "补一个最小 judge adapter 接口或文档化示例。",
                "说明 judge reason、score bucket 和 release recommendation 的关系。",
                "扩展测试或 smoke 证据时保持输出结构稳定。",
            ],
            "suggested_files": [
                "projects/eval-module/src/eval_module",
                "projects/eval-module/tests/test_runner.py",
                "docs/04-evaluation-observability/05-llm-evaluation.md",
            ],
            "acceptance_criteria": [
                "示例能解释 sample output 从哪里来。",
                "不会破坏现有 run/compare/leaderboard 输出契约。",
                "文档说明它仍是学习型 adapter，不是完整评测平台。",
            ],
            "verification_commands": [
                "PYTHON=.venv/bin/python make eval-test",
                "PYTHON=.venv/bin/python make infra-check",
            ],
        },
        {
            "id": "launch-finetune-resume-checkpoint-lab",
            "title": "[Lab] Add finetune resume and checkpoint selection exercise",
            "labels": ["lab", "enhancement", "documentation"],
            "priority": "P2",
            "source_module": "training-lineage",
            "learning_value": "帮助学习者理解 checkpoint 不是单个文件，而是可选择、可恢复、可审计的训练资产。",
            "scope": [
                "设计一个小 lab，要求学习者比较 checkpoint index 和 export manifest。",
                "说明 resume / checkpoint selection 在真实训练系统中的边界。",
                "补充验收命令和产物路径。",
            ],
            "suggested_files": [
                "docs/07-hands-on-labs/04-finetune-reproducibility-lab.md",
                "docs/05-finetuning-training/02-run-artifacts-export.md",
                "projects/finetune-demo/tests/test_trainer.py",
            ],
            "acceptance_criteria": [
                "lab 有明确学习目标、步骤、证据要求和验收标准。",
                "读者能从 export manifest 追溯回 checkpoint 和 dataset。",
                "新增内容不声称执行真实 GPU 训练。",
            ],
            "verification_commands": [
                "PYTHON=.venv/bin/python make finetune-test",
                "PYTHON=.venv/bin/python make docs-quality",
            ],
        },
        {
            "id": "launch-roadmap-refresh",
            "title": "[Maintenance] Refresh public roadmap after first feedback",
            "labels": ["documentation", "feedback"],
            "priority": "P1",
            "source_module": "publication",
            "learning_value": f"让公开路线图和当前 release readiness `{release_readiness}` 保持一致，避免读者看到过期承诺。",
            "scope": [
                "首发后根据前 5 到 10 条反馈更新 public roadmap。",
                "把大想法拆成小 issue，并标出 good first issue。",
                "保留暂不优先做什么，避免路线图失焦。",
            ],
            "suggested_files": [
                "docs/08-publication/03-public-roadmap.md",
                "docs/08-publication/05-generated-roadmap-pack.md",
                "PUBLICATION_CHECKLIST.md",
            ],
            "acceptance_criteria": [
                "路线图能解释当前阶段、下一阶段和非目标。",
                "至少 5 条 issue 种子被整理成可创建的 GitHub issue。",
                "路线图不承诺具体发布日期。",
            ],
            "verification_commands": ["PYTHON=.venv/bin/python make docs-quality"],
        },
    ]


def build_recommended_labels() -> list[dict[str, str]]:
    return [
        {"name": "good first issue", "purpose": "适合第一次贡献的小任务。"},
        {"name": "documentation", "purpose": "文档、学习路径或表达改进。"},
        {"name": "lab", "purpose": "hands-on lab、练习或验收任务。"},
        {"name": "evidence", "purpose": "输出证据、manifest、报告或截图。"},
        {"name": "feedback", "purpose": "共学、公开演示或读者反馈。"},
        {"name": "enhancement", "purpose": "学习体验或项目能力增强。"},
        {"name": "question", "purpose": "需要讨论的学习或设计问题。"},
    ]


def extract_routes(module: dict[str, Any]) -> list[str]:
    routes: list[str] = []
    for question in module.get("questions", []):
        routes.extend(extract_backtick_routes(question.get("prompt", "")))
    for evidence in module.get("evidence_requirements", []):
        routes.extend(extract_backtick_routes(evidence))
    return routes


def extract_backtick_routes(text: str) -> list[str]:
    routes: list[str] = []
    for chunk in text.split("`"):
        if chunk.startswith("/"):
            routes.append(chunk)
    return routes


def route_files(routes: list[str]) -> list[str]:
    files: list[str] = []
    for route in routes:
        if not route or not route.startswith("/"):
            continue
        path = "docs" + route
        if path.endswith("/"):
            path += "index"
        if not path.endswith(".md"):
            path = f"{path}.md"
        files.append(path)
    return dedupe_keep_order(files)


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
        "# AI Infra Roadmap Pack",
        "",
        f"- Generated at: `{packet['generated_at']}`",
        f"- Roadmap readiness: `{summary['roadmap_readiness']}`",
        f"- Issue seeds: `{summary['issue_seed_count']}`",
        f"- Module issues: `{summary['module_issue_count']}`",
        f"- Launch issues: `{summary['launch_issue_count']}`",
        f"- Docs pages: `{summary['docs_pages']}`",
        "",
        "## Validation",
        "",
        "| Signal | Value |",
        "| --- | --- |",
    ]
    for key, value in validation.items():
        lines.append(f"| `{key}` | `{value}` |")

    lines.extend(["", "## Roadmap Principles", ""])
    lines.extend(f"- {item}" for item in packet["roadmap_principles"])

    lines.extend(["", "## Issue Seeds", ""])
    for issue in packet["issue_seeds"]:
        lines.extend(
            [
                f"### {issue['title']}",
                "",
                f"- ID: `{issue['id']}`",
                f"- Priority: `{issue['priority']}`",
                f"- Source module: `{issue['source_module']}`",
                f"- Labels: `{', '.join(issue['labels'])}`",
                f"- Learning value: {issue['learning_value']}",
                "",
                "Scope:",
            ]
        )
        lines.extend(f"- {item}" for item in issue["scope"])
        lines.extend(["", "Suggested files:"])
        lines.extend(f"- `{item}`" for item in issue["suggested_files"])
        lines.extend(["", "Acceptance criteria:"])
        lines.extend(f"- {item}" for item in issue["acceptance_criteria"])
        lines.extend(["", "Verification commands:"])
        lines.extend(f"- `{item}`" for item in issue["verification_commands"])
        lines.append("")

    lines.extend(["## Recommended Labels", ""])
    for label in packet["recommended_labels"]:
        lines.append(f"- `{label['name']}`: {label['purpose']}")

    lines.extend(["", "## Publication Flow", ""])
    lines.extend(f"- {item}" for item in packet["publication_flow"])
    lines.extend(["", "## Recommended Commands", ""])
    lines.extend(f"- `{command}`" for command in packet["recommended_commands"])
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build GitHub-ready roadmap issue seeds for the AI Infra project.")
    parser.add_argument("--release-brief", type=Path, default=DEFAULT_RELEASE_BRIEF)
    parser.add_argument("--assessment-pack", type=Path, default=DEFAULT_ASSESSMENT_PACK)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN_OUTPUT)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    packet = build_roadmap_pack(args.release_brief, args.assessment_pack, strict=args.strict)
    json_target, markdown_target = write_outputs(packet, args.output, args.markdown_output)
    print(f"Roadmap pack written to {json_target}")
    print(f"Roadmap pack markdown written to {markdown_target}")
    print(f"Roadmap readiness: {packet['summary']['roadmap_readiness']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
