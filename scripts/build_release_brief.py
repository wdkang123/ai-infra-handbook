"""Build a public release brief from the learning inventory and evidence packet."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_INVENTORY = ROOT_DIR / ".tmp" / "docs-inventory" / "learning_inventory.json"
DEFAULT_EVIDENCE = ROOT_DIR / ".tmp" / "evidence" / "evidence_packet.json"
DEFAULT_OUTPUT = ROOT_DIR / ".tmp" / "release" / "release_brief.json"
DEFAULT_MARKDOWN_OUTPUT = ROOT_DIR / ".tmp" / "release" / "release_brief.md"


class ReleaseBriefError(RuntimeError):
    """Raised when strict release brief generation finds missing or incomplete inputs."""


def build_release_brief(
    inventory_path: str | Path = DEFAULT_INVENTORY,
    evidence_path: str | Path = DEFAULT_EVIDENCE,
    *,
    strict: bool = False,
) -> dict[str, Any]:
    inventory_file = Path(inventory_path)
    evidence_file = Path(evidence_path)
    inventory = read_json_file(inventory_file, strict=strict, label="learning inventory")
    evidence = read_json_file(evidence_file, strict=strict, label="evidence packet")

    validation = build_validation_summary(inventory, evidence)
    if strict:
        errors = validation_errors(validation)
        if errors:
            raise ReleaseBriefError("; ".join(errors))

    return {
        "report_type": "ai_infra_release_brief",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "source_files": {
            "learning_inventory": str(inventory_file),
            "evidence_packet": str(evidence_file),
        },
        "summary": {
            "release_readiness": "ready" if not validation_errors(validation) else "review",
            "docs_pages": get_nested(inventory, ["summary", "page_count"], 0),
            "sections": get_nested(inventory, ["summary", "section_count"], 0),
            "course_tracks": get_nested(inventory, ["summary", "course_track_count"], 0),
            "missing_track_routes": get_nested(inventory, ["summary", "missing_track_route_count"], 0),
            "evidence_sections": get_nested(evidence, ["summary", "available_section_count"], 0),
            "missing_evidence_artifacts": get_nested(evidence, ["summary", "missing_artifact_count"], 0),
            "eval_release_recommendation": get_nested(evidence, ["summary", "release_recommendation"]),
            "finetune_export_status": get_nested(evidence, ["summary", "finetune_export_status"]),
        },
        "learning_site": build_learning_site_summary(inventory),
        "runtime_evidence": build_runtime_evidence_summary(evidence),
        "validation": validation,
        "public_positioning": [
            "Learning-first AI Infra manual, not a production platform.",
            "The site combines structured docs, runnable scaffolds, course catalog modules, hands-on labs, assessments, and evidence artifacts.",
            "Release claims should be backed by generated inventory, smoke evidence, and local validation commands.",
        ],
        "recommended_commands": [
            "PYTHON=.venv/bin/python make docs-inventory",
            "PYTHON=.venv/bin/python make course-catalog",
            "PYTHON=.venv/bin/python make infra-check",
            "PYTHON=.venv/bin/python make infra-smoke",
            "PYTHON=.venv/bin/python make infra-evidence",
            "PYTHON=.venv/bin/python make release-brief",
            "PYTHON=.venv/bin/python make workshop-packet",
            "PYTHON=.venv/bin/python make assessment-pack",
            "PYTHON=.venv/bin/python make roadmap-pack",
            "npm audit --omit=dev --audit-level=moderate",
        ],
        "next_review_questions": [
            "Can a first-time reader choose a path without asking the maintainer?",
            "Can every public claim point to docs inventory, smoke output, or evidence packet fields?",
            "Are learning boundaries clear enough that nobody mistakes this for a production system?",
            "Which feedback loop should be opened first after publishing to GitHub?",
        ],
    }


def read_json_file(path: Path, *, strict: bool, label: str) -> dict[str, Any]:
    if not path.exists():
        if strict:
            raise ReleaseBriefError(f"Missing {label}: {path}")
        return {}
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ReleaseBriefError(f"Invalid {label} JSON: {path}") from exc


def build_validation_summary(inventory: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    inventory_report_type = inventory.get("report_type")
    evidence_report_type = evidence.get("report_type")
    missing_track_routes = int(get_nested(inventory, ["summary", "missing_track_route_count"], 0) or 0)
    missing_evidence = int(get_nested(evidence, ["summary", "missing_artifact_count"], 0) or 0)
    evidence_sections = int(get_nested(evidence, ["summary", "available_section_count"], 0) or 0)
    expected_evidence_sections = int(get_nested(evidence, ["summary", "section_count"], 0) or 0)

    return {
        "inventory_available": inventory_report_type == "ai_infra_learning_inventory",
        "evidence_available": evidence_report_type == "ai_infra_evidence_packet",
        "missing_track_route_count": missing_track_routes,
        "missing_evidence_artifact_count": missing_evidence,
        "evidence_sections_available": evidence_sections,
        "evidence_sections_expected": expected_evidence_sections,
        "all_evidence_sections_available": evidence_sections > 0 and evidence_sections == expected_evidence_sections,
        "ready_for_public_review": (
            inventory_report_type == "ai_infra_learning_inventory"
            and evidence_report_type == "ai_infra_evidence_packet"
            and missing_track_routes == 0
            and missing_evidence == 0
            and evidence_sections > 0
            and evidence_sections == expected_evidence_sections
        ),
    }


def validation_errors(validation: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not validation["inventory_available"]:
        errors.append("learning inventory is missing or has the wrong report_type")
    if not validation["evidence_available"]:
        errors.append("evidence packet is missing or has the wrong report_type")
    if validation["missing_track_route_count"]:
        errors.append(f"learning inventory has {validation['missing_track_route_count']} missing tracked routes")
    if validation["missing_evidence_artifact_count"]:
        errors.append(f"evidence packet has {validation['missing_evidence_artifact_count']} missing artifacts")
    if validation["evidence_available"] and not validation["all_evidence_sections_available"]:
        errors.append(
            "evidence packet does not have all expected sections "
            f"({validation['evidence_sections_available']}/{validation['evidence_sections_expected']})"
        )
    return errors


def build_learning_site_summary(inventory: dict[str, Any]) -> dict[str, Any]:
    sections = inventory.get("sections") or []
    course_tracks = inventory.get("course_tracks") or []
    quality_signals = inventory.get("quality_signals") or {}
    return {
        "page_count": get_nested(inventory, ["summary", "page_count"], 0),
        "section_count": get_nested(inventory, ["summary", "section_count"], 0),
        "course_track_count": get_nested(inventory, ["summary", "course_track_count"], 0),
        "top_sections_by_pages": [
            {
                "title": section.get("title"),
                "page_count": section.get("page_count", 0),
                "learning_weight": section.get("learning_weight", 0),
            }
            for section in sorted(sections, key=lambda item: item.get("page_count", 0), reverse=True)[:5]
        ],
        "course_tracks": [
            {
                "id": track.get("id"),
                "title": track.get("title"),
                "matched_route_count": track.get("matched_route_count", 0),
                "route_count": track.get("route_count", 0),
                "missing_routes": track.get("missing_routes", []),
            }
            for track in course_tracks
        ],
        "quality_signals": {
            "hands_on_lab_pages": quality_signals.get("hands_on_lab_pages", 0),
            "assessment_pages": quality_signals.get("assessment_pages", 0),
            "case_study_pages": quality_signals.get("case_study_pages", 0),
            "evidence_gallery_pages": quality_signals.get("evidence_gallery_pages", 0),
            "workshop_kit_pages": quality_signals.get("workshop_kit_pages", 0),
            "project_count": quality_signals.get("project_count", 0),
        },
    }


def build_runtime_evidence_summary(evidence: dict[str, Any]) -> dict[str, Any]:
    sections = evidence.get("sections") or {}
    serving = sections.get("serving_gateway") or {}
    eval_section = sections.get("eval") or {}
    finetune = sections.get("finetune") or {}
    return {
        "available_sections": get_nested(evidence, ["summary", "available_sections"], []),
        "release_recommendation": get_nested(evidence, ["summary", "release_recommendation"]),
        "finetune_export_status": get_nested(evidence, ["summary", "finetune_export_status"]),
        "serving_gateway": {
            "status": serving.get("status"),
            "inference_status": get_nested(serving, ["health", "inference_status"]),
            "gateway_status": get_nested(serving, ["health", "gateway_status"]),
            "gateway_status_code_counts": get_nested(serving, ["events", "gateway_status_code_counts"], {}),
        },
        "eval": {
            "status": eval_section.get("status"),
            "task": get_nested(eval_section, ["run", "task"]),
            "accuracy": get_nested(eval_section, ["run", "accuracy"]),
            "release_recommendation": eval_section.get("release_recommendation"),
        },
        "finetune": {
            "status": finetune.get("status"),
            "method": get_nested(finetune, ["run", "method"]),
            "dataset_id": get_nested(finetune, ["run", "dataset_id"]),
            "export_status": finetune.get("export_status"),
            "adapter_model_sha256": get_nested(finetune, ["export_index", "adapter_model_sha256"]),
        },
    }


def get_nested(payload: dict[str, Any], path: list[str], default: Any = None) -> Any:
    current: Any = payload
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def write_outputs(brief: dict[str, Any], output: str | Path, markdown_output: str | Path) -> tuple[Path, Path]:
    json_path = Path(output)
    markdown_path = Path(markdown_output)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(brief, ensure_ascii=False, indent=2) + "\n")
    markdown_path.write_text(render_markdown(brief))
    return json_path, markdown_path


def render_markdown(brief: dict[str, Any]) -> str:
    summary = brief["summary"]
    validation = brief["validation"]
    learning = brief["learning_site"]
    evidence = brief["runtime_evidence"]

    lines = [
        "# AI Infra Release Brief",
        "",
        f"- Generated at: `{brief['generated_at']}`",
        f"- Release readiness: `{summary['release_readiness']}`",
        f"- Docs pages: `{summary['docs_pages']}`",
        f"- Course tracks: `{summary['course_tracks']}`",
        f"- Evidence sections: `{summary['evidence_sections']}`",
        f"- Eval release recommendation: `{summary['eval_release_recommendation']}`",
        f"- Finetune export status: `{summary['finetune_export_status']}`",
        "",
        "## Public Positioning",
        "",
    ]
    lines.extend(f"- {item}" for item in brief["public_positioning"])

    lines.extend(
        [
            "",
            "## Validation",
            "",
            "| Check | Value |",
            "| --- | ---: |",
        ]
    )
    for key, value in validation.items():
        lines.append(f"| `{key}` | `{value}` |")

    lines.extend(
        [
            "",
            "## Learning Site",
            "",
            f"- Sections: `{learning['section_count']}`",
            f"- Course tracks: `{learning['course_track_count']}`",
            f"- Hands-on lab pages: `{learning['quality_signals']['hands_on_lab_pages']}`",
            f"- Assessment pages: `{learning['quality_signals']['assessment_pages']}`",
            f"- Evidence gallery pages: `{learning['quality_signals']['evidence_gallery_pages']}`",
            f"- Workshop kit pages: `{learning['quality_signals']['workshop_kit_pages']}`",
            "",
            "### Top Sections",
            "",
            "| Section | Pages | Learning Weight |",
            "| --- | ---: | ---: |",
        ]
    )
    for section in learning["top_sections_by_pages"]:
        lines.append(f"| {section['title']} | {section['page_count']} | {section['learning_weight']} |")

    lines.extend(["", "### Course Tracks", "", "| Track | Routes | Missing |", "| --- | ---: | --- |"])
    for track in learning["course_tracks"]:
        missing = ", ".join(track["missing_routes"]) if track["missing_routes"] else "none"
        lines.append(f"| {track['title']} | {track['matched_route_count']}/{track['route_count']} | {missing} |")

    lines.extend(
        [
            "",
            "## Runtime Evidence",
            "",
            f"- Available sections: `{', '.join(evidence['available_sections'])}`",
            f"- Serving status: `{evidence['serving_gateway']['status']}`",
            f"- Gateway status codes: `{evidence['serving_gateway']['gateway_status_code_counts']}`",
            f"- Eval task: `{evidence['eval']['task']}`",
            f"- Eval accuracy: `{evidence['eval']['accuracy']}`",
            f"- Eval release recommendation: `{evidence['eval']['release_recommendation']}`",
            f"- Finetune method: `{evidence['finetune']['method']}`",
            f"- Finetune dataset id: `{evidence['finetune']['dataset_id']}`",
            f"- Finetune export status: `{evidence['finetune']['export_status']}`",
            "",
            "## Recommended Commands",
            "",
        ]
    )
    lines.extend(f"- `{command}`" for command in brief["recommended_commands"])

    lines.extend(["", "## Next Review Questions", ""])
    lines.extend(f"- {question}" for question in brief["next_review_questions"])
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a public release brief for the AI Infra learning site.")
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN_OUTPUT)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    brief = build_release_brief(args.inventory, args.evidence, strict=args.strict)
    json_target, markdown_target = write_outputs(brief, args.output, args.markdown_output)
    print(f"Release brief written to {json_target}")
    print(f"Release brief markdown written to {markdown_target}")
    print(f"Release readiness: {brief['summary']['release_readiness']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
