"""Build a GitHub launch operations pack from release and roadmap artifacts."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_RELEASE_BRIEF = ROOT_DIR / ".tmp" / "release" / "release_brief.json"
DEFAULT_ROADMAP_PACK = ROOT_DIR / ".tmp" / "roadmap" / "roadmap_pack.json"
DEFAULT_OUTPUT = ROOT_DIR / ".tmp" / "launch" / "launch_pack.json"
DEFAULT_MARKDOWN_OUTPUT = ROOT_DIR / ".tmp" / "launch" / "launch_pack.md"

DEFAULT_PUBLIC_LABELS = {
    "bug",
    "documentation",
    "duplicate",
    "enhancement",
    "good first issue",
    "help wanted",
    "invalid",
    "question",
    "wontfix",
}

CUSTOM_LABEL_MAP = {
    "case-study": ["documentation", "enhancement"],
    "ci": ["enhancement"],
    "dependencies": ["enhancement"],
    "evidence": ["documentation"],
    "feedback": ["documentation", "question"],
    "lab": ["documentation", "enhancement"],
    "maintenance": ["documentation", "enhancement"],
    "python": ["enhancement"],
    "release": ["documentation"],
}


class LaunchPackError(RuntimeError):
    """Raised when the launch pack cannot be built safely."""


def build_launch_pack(
    release_brief_path: str | Path = DEFAULT_RELEASE_BRIEF,
    roadmap_pack_path: str | Path = DEFAULT_ROADMAP_PACK,
    *,
    strict: bool = False,
) -> dict[str, Any]:
    release_file = Path(release_brief_path).resolve()
    roadmap_file = Path(roadmap_pack_path).resolve()
    release_brief = read_json_file(release_file, label="release brief")
    roadmap_pack = read_json_file(roadmap_file, label="roadmap pack")

    validation = build_validation_summary(release_brief, roadmap_pack)
    if strict:
        errors = validation_errors(validation)
        if errors:
            raise LaunchPackError("; ".join(errors))

    issue_seeds = roadmap_pack.get("issue_seeds") or []
    starter_issues = build_starter_issues(issue_seeds)
    release_notes = build_release_notes(release_brief, roadmap_pack)
    commands = build_recommended_commands(roadmap_pack)

    return {
        "report_type": "ai_infra_launch_pack",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "source_files": {
            "release_brief": str(release_file),
            "roadmap_pack": str(roadmap_file),
        },
        "summary": {
            "launch_readiness": "ready" if not validation_errors(validation) else "review",
            "release_title": release_notes["title"],
            "docs_pages": get_nested(release_brief, ["summary", "docs_pages"], 0),
            "release_readiness": get_nested(release_brief, ["summary", "release_readiness"], "review"),
            "roadmap_readiness": get_nested(roadmap_pack, ["summary", "roadmap_readiness"], "review"),
            "issue_seed_count": validation["issue_seed_count"],
            "starter_issue_count": len(starter_issues),
            "public_label_mode": "github-default-labels",
        },
        "validation": validation,
        "release_notes": release_notes,
        "starter_issues": starter_issues,
        "post_release_checklist": build_post_release_checklist(),
        "recommended_commands": commands,
        "publication_flow": [
            "发布前先运行 launch pack，确认 release notes、首批 issue 和验证命令来自同一套结构化产物。",
            "首批 issue 默认只使用 GitHub 新仓库已有标签，避免创建 issue 时出现 label 不存在的提示。",
            "如果后续维护量增加，再按 Issue 分类文档创建 `lab`、`evidence`、`feedback` 等自定义标签。",
            "发布后 24 小时优先检查 README、Pages、Actions、release 和首批 issue 是否互相一致。",
        ],
    }


def read_json_file(path: Path, *, label: str) -> dict[str, Any]:
    if not path.exists():
        raise LaunchPackError(f"Missing {label}: {path}")
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise LaunchPackError(f"Invalid {label} JSON: {path}") from exc


def build_validation_summary(release_brief: dict[str, Any], roadmap_pack: dict[str, Any]) -> dict[str, Any]:
    release_report_type = release_brief.get("report_type")
    roadmap_report_type = roadmap_pack.get("report_type")
    release_ready = get_nested(release_brief, ["summary", "release_readiness"]) == "ready"
    public_review_ready = bool(get_nested(release_brief, ["validation", "ready_for_public_review"], False))
    roadmap_ready = get_nested(roadmap_pack, ["summary", "roadmap_readiness"]) == "ready"
    public_roadmap_ready = bool(get_nested(roadmap_pack, ["validation", "ready_for_public_roadmap"], False))
    reported_issue_seed_count = int(get_nested(roadmap_pack, ["summary", "issue_seed_count"], 0) or 0)
    issue_seed_count = len(roadmap_pack.get("issue_seeds") or [])
    starter_issue_count = min(issue_seed_count, 8)
    return {
        "release_brief_available": release_report_type == "ai_infra_release_brief",
        "roadmap_pack_available": roadmap_report_type == "ai_infra_roadmap_pack",
        "release_brief_ready": release_ready,
        "release_ready_for_public_review": public_review_ready,
        "roadmap_pack_ready": roadmap_ready,
        "roadmap_ready_for_public_review": public_roadmap_ready,
        "reported_issue_seed_count": reported_issue_seed_count,
        "issue_seed_count": issue_seed_count,
        "starter_issue_count": starter_issue_count,
        "ready_for_public_launch": (
            release_report_type == "ai_infra_release_brief"
            and roadmap_report_type == "ai_infra_roadmap_pack"
            and release_ready
            and public_review_ready
            and roadmap_ready
            and public_roadmap_ready
            and issue_seed_count > 0
        ),
    }


def validation_errors(validation: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not validation["release_brief_available"]:
        errors.append("release brief is missing or has the wrong report_type")
    if not validation["roadmap_pack_available"]:
        errors.append("roadmap pack is missing or has the wrong report_type")
    if validation["release_brief_available"] and not validation["release_brief_ready"]:
        errors.append("release brief is not ready")
    if validation["release_brief_available"] and not validation["release_ready_for_public_review"]:
        errors.append("release brief is not ready for public review")
    if validation["roadmap_pack_available"] and not validation["roadmap_pack_ready"]:
        errors.append("roadmap pack is not ready")
    if validation["roadmap_pack_available"] and not validation["roadmap_ready_for_public_review"]:
        errors.append("roadmap pack is not ready for public review")
    if validation["roadmap_pack_available"] and validation["reported_issue_seed_count"] != validation["issue_seed_count"]:
        errors.append("roadmap pack issue seed count does not match issue_seeds")
    if validation["issue_seed_count"] <= 0:
        errors.append("roadmap pack has no issue seeds")
    return errors


def build_release_notes(release_brief: dict[str, Any], roadmap_pack: dict[str, Any]) -> dict[str, Any]:
    docs_pages = get_nested(release_brief, ["summary", "docs_pages"], 0)
    course_tracks = get_nested(release_brief, ["summary", "course_tracks"], 0)
    issue_seed_count = len(roadmap_pack.get("issue_seeds") or [])
    return {
        "title": "AI Infra Handbook v0.1.0-learning-site",
        "summary": (
            "这是一个学习型首发版本，用于系统学习 AI Infra 的主干工程路径；"
            "它把文档站、可运行脚手架、hands-on labs、证据包和公开协作材料收成同一套学习闭环。"
        ),
        "highlights": [
            f"VitePress 学习站覆盖 `{docs_pages}` 个文档页和 `{course_tracks}` 条课程主线。",
            "四个可运行学习项目：`inference-service`、`ai-gateway`、`eval-module`、`finetune-demo`。",
            "深度实战、案例复盘、示例输出、学习自测和共学套件已经互相连通。",
            "自动产物覆盖 learning inventory、course catalog、evidence packet、release brief、workshop packet、assessment pack、roadmap pack 和 launch pack。",
            f"路线图包提供 `{issue_seed_count}` 条 issue 种子，可继续整理为首批 GitHub 协作任务。",
        ],
        "verification": [
            "nvm use",
            "PYTHON=.venv/bin/python make public-check",
            "PYTHON=.venv/bin/python make infra-smoke",
            "PYTHON=.venv/bin/python make infra-evidence",
            "PYTHON=.venv/bin/python make release-brief",
            "PYTHON=.venv/bin/python make workshop-packet",
            "PYTHON=.venv/bin/python make assessment-pack",
            "PYTHON=.venv/bin/python make roadmap-pack",
            "PYTHON=.venv/bin/python make launch-pack",
            "npm audit --omit=dev --audit-level=moderate",
        ],
        "boundaries": [
            "这是学习项目，不是生产平台。",
            "默认路径使用 mock / local scaffold，便于读者复现和拆解工程概念。",
            "真实 serving、gateway、eval 和 training 接入请沿生产迁移章节逐步替换。",
            "发布说明只描述已经能验证的学习价值，不承诺生产可用性或具体发布日期。",
        ],
    }


def build_starter_issues(issue_seeds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    starter_issues: list[dict[str, Any]] = []
    for issue in issue_seeds[:8]:
        starter_issues.append(
            {
                "id": issue.get("id"),
                "title": issue.get("title"),
                "priority": issue.get("priority", "P2"),
                "labels": normalize_labels(issue.get("labels") or []),
                "source_module": issue.get("source_module", "cross-cutting"),
                "learning_value": issue.get("learning_value", ""),
                "scope": issue.get("scope") or [],
                "suggested_files": issue.get("suggested_files") or [],
                "acceptance_criteria": issue.get("acceptance_criteria") or [],
                "verification_commands": issue.get("verification_commands") or [],
            }
        )
    return starter_issues


def normalize_labels(labels: list[str]) -> list[str]:
    normalized: list[str] = []
    for label in labels:
        if label in DEFAULT_PUBLIC_LABELS:
            normalized.append(label)
            continue
        normalized.extend(CUSTOM_LABEL_MAP.get(label, ["enhancement"]))
    if not normalized:
        normalized.append("enhancement")
    return dedupe_keep_order(normalized)


def build_post_release_checklist() -> list[dict[str, str]]:
    return [
        {"window": "0-2h", "task": "确认 GitHub release 页面、README 和在线站点链接互相一致。"},
        {"window": "0-2h", "task": "打开 Pages 站点首页、学习路线、公开发布总览和 release notes 中提到的核心入口。"},
        {"window": "24h", "task": "检查 `ci`、`docs-pages`、Dependabot 和 dependency review 是否有失败或噪音。"},
        {"window": "24h", "task": "从 starter issues 中挑 3 到 6 条创建到 GitHub，并保留学习价值和验收命令。"},
        {"window": "7d", "task": "把读者卡点回流到 FAQ、排障手册、示例输出与路线图 issue。"},
        {"window": "30d", "task": "复盘首批 issue、共学反馈和测评弱点，决定是否创建自定义 labels。"},
    ]


def build_recommended_commands(roadmap_pack: dict[str, Any]) -> list[str]:
    commands = [
        "PYTHON=.venv/bin/python make public-check",
        "PYTHON=.venv/bin/python make roadmap-pack",
        "PYTHON=.venv/bin/python make launch-pack",
        "npm audit --omit=dev --audit-level=moderate",
    ]
    for command in roadmap_pack.get("recommended_commands", []):
        if command not in commands:
            commands.append(command)
    return commands


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
    release_notes = packet["release_notes"]
    lines = [
        "# AI Infra Launch Pack",
        "",
        f"- Generated at: `{packet['generated_at']}`",
        f"- Launch readiness: `{summary['launch_readiness']}`",
        f"- Release title: `{summary['release_title']}`",
        f"- Docs pages: `{summary['docs_pages']}`",
        f"- Issue seeds: `{summary['issue_seed_count']}`",
        f"- Starter issues: `{summary['starter_issue_count']}`",
        f"- Public label mode: `{summary['public_label_mode']}`",
        "",
        "## Validation",
        "",
        "| Signal | Value |",
        "| --- | --- |",
    ]
    for key, value in validation.items():
        lines.append(f"| `{key}` | `{value}` |")

    lines.extend(["", "## Release Notes Draft", "", f"### {release_notes['title']}", "", release_notes["summary"], ""])
    lines.extend(["Highlights:", ""])
    lines.extend(f"- {item}" for item in release_notes["highlights"])
    lines.extend(["", "Verification:", ""])
    lines.extend(f"- `{command}`" for command in release_notes["verification"])
    lines.extend(["", "Boundaries:", ""])
    lines.extend(f"- {item}" for item in release_notes["boundaries"])

    lines.extend(["", "## Starter Issues", ""])
    for issue in packet["starter_issues"]:
        lines.extend(
            [
                f"### {issue['title']}",
                "",
                f"- ID: `{issue['id']}`",
                f"- Priority: `{issue['priority']}`",
                f"- Labels: `{', '.join(issue['labels'])}`",
                f"- Source module: `{issue['source_module']}`",
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

    lines.extend(["## Post-release Checklist", ""])
    for item in packet["post_release_checklist"]:
        lines.append(f"- `{item['window']}`: {item['task']}")

    lines.extend(["", "## Publication Flow", ""])
    lines.extend(f"- {item}" for item in packet["publication_flow"])
    lines.extend(["", "## Recommended Commands", ""])
    lines.extend(f"- `{command}`" for command in packet["recommended_commands"])
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a GitHub launch operations pack for the AI Infra project.")
    parser.add_argument("--release-brief", type=Path, default=DEFAULT_RELEASE_BRIEF)
    parser.add_argument("--roadmap-pack", type=Path, default=DEFAULT_ROADMAP_PACK)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN_OUTPUT)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    packet = build_launch_pack(args.release_brief, args.roadmap_pack, strict=args.strict)
    json_target, markdown_target = write_outputs(packet, args.output, args.markdown_output)
    print(f"Launch pack written to {json_target}")
    print(f"Launch pack markdown written to {markdown_target}")
    print(f"Launch readiness: {packet['summary']['launch_readiness']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
