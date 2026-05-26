"""Build a workshop-ready course catalog from the learning inventory."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_INVENTORY = ROOT_DIR / ".tmp" / "docs-inventory" / "learning_inventory.json"
DEFAULT_OUTPUT = ROOT_DIR / ".tmp" / "course-catalog" / "course_catalog.json"
DEFAULT_MARKDOWN_OUTPUT = ROOT_DIR / ".tmp" / "course-catalog" / "course_catalog.md"

GROUP_TITLES = {
    "orient": "建立地图",
    "core": "核心阅读",
    "run": "运行与观察",
    "practice": "动手练习",
    "evidence": "证据输出",
    "assessment": "自测与答辩",
    "share": "公开分享",
    "migration": "生产迁移",
}

CATALOG_MODULES: list[dict[str, Any]] = [
    {
        "id": "zero-to-one",
        "title": "从 0 到 1 学习模块",
        "audience": "第一次系统学习 AI Infra 的读者。",
        "outcome": "能讲清 AI Infra 的基本分层，并完成第一轮本地运行和复盘。",
        "entry_route": "/00-overview/00-zero-to-one",
        "route_groups": {
            "orient": [
                "/00-overview/00-zero-to-one",
                "/00-overview/02-learning-route",
                "/00-overview/12-course-syllabus",
                "/00-overview/15-two-week-learning-plan",
            ],
            "run": ["/00-overview/03-runbook", "/00-overview/04-first-walkthrough"],
            "practice": ["/07-hands-on-labs/00-overview", "/07-hands-on-labs/05-capstone-review-rubric"],
            "assessment": ["/10-assessments/00-overview", "/10-assessments/01-system-map-check"],
            "evidence": ["/13-output-gallery/00-overview", "/09-reference/08-learning-inventory"],
        },
        "checkpoints": [
            "能画出 request 从 gateway 到 inference 的基本路径。",
            "能解释为什么学习型项目不等于生产平台。",
            "能跑完本地站点、基础验证和第一次实操。",
        ],
        "facilitator_notes": [
            "先让读者说出自己要解决的问题，再选学习路径。",
            "第一轮不要急着讲全部工具，先把运行证据看明白。",
        ],
    },
    {
        "id": "serving-engineer",
        "title": "推理服务工程模块",
        "audience": "想理解 token、streaming、batching、metrics 和 serving 边界的工程读者。",
        "outcome": "能从请求、首 token、流式输出和事件记录解释推理服务的关键观测面。",
        "entry_route": "/02-inference-serving/00-overview",
        "route_groups": {
            "orient": [
                "/01-llm-fundamentals/01-model-token-context",
                "/01-llm-fundamentals/04-from-request-to-first-token",
                "/02-inference-serving/00-overview",
            ],
            "core": [
                "/02-inference-serving/09-streaming-batching-metrics",
                "/02-inference-serving/10-from-learning-service-to-real-serving-stack",
                "/06-projects/01-inference-service",
            ],
            "practice": ["/07-hands-on-labs/01-serving-observability-lab"],
            "evidence": ["/13-output-gallery/01-serving-gateway-evidence", "/09-reference/05-api-surface"],
            "migration": ["/12-production-migration/01-serving-backend-migration"],
        },
        "checkpoints": [
            "能区分 prefill、decode、TTFT、ITL 和吞吐。",
            "能用 request id、events 和 metrics 定位一次请求。",
            "能说明学习型 inference-service 迁移到真实 serving stack 时要保留哪些接口。",
        ],
        "facilitator_notes": [
            "用一次 streaming 请求做现场观察，比只讲概念更有效。",
            "把 mock usage 当成观测结构演示，不要把它讲成真实计费逻辑。",
        ],
    },
    {
        "id": "platform-engineer",
        "title": "平台治理工程模块",
        "audience": "想理解 gateway、鉴权、路由、fallback、限流和失败语义的读者。",
        "outcome": "能解释平台层如何保护模型服务，并能复盘一次失败请求。",
        "entry_route": "/03-ai-gateway-platform/00-overview",
        "route_groups": {
            "orient": ["/03-ai-gateway-platform/00-overview", "/03-ai-gateway-platform/05-platform-vs-model-service"],
            "core": [
                "/03-ai-gateway-platform/01-auth-routing-rate-limit",
                "/03-ai-gateway-platform/03-gateway-router-fallback-cache",
                "/03-ai-gateway-platform/04-streaming-errors-upstream-health",
                "/06-projects/02-ai-gateway",
            ],
            "practice": ["/07-hands-on-labs/02-gateway-resilience-lab"],
            "evidence": ["/13-output-gallery/05-failure-evidence-map", "/09-reference/04-troubleshooting"],
            "migration": ["/12-production-migration/02-gateway-platform-hardening"],
        },
        "checkpoints": [
            "能说清外部模型名和内部 upstream target 的边界。",
            "能用 header、events 和 failure summary 复盘鉴权、路由或上游失败。",
            "能说明生产 gateway 还需要哪些策略、存储和审计能力。",
        ],
        "facilitator_notes": [
            "让读者故意制造 401、404、fallback 三类路径，再比较证据。",
            "强调 gateway 的价值在治理和观测，不是替代模型服务本身。",
        ],
    },
    {
        "id": "eval-release",
        "title": "评测发布判断模块",
        "audience": "想理解 run、compare、leaderboard、sample analysis 和发布门禁的读者。",
        "outcome": "能用评测产物解释一个模型是否适合进入下一轮 review。",
        "entry_route": "/04-evaluation-observability/00-overview",
        "route_groups": {
            "orient": ["/04-evaluation-observability/00-overview", "/04-evaluation-observability/05-llm-evaluation"],
            "core": [
                "/04-evaluation-observability/01-run-compare-history",
                "/04-evaluation-observability/07-from-run-to-release-decision",
                "/04-evaluation-observability/08-benchmark-vs-production-quality",
                "/06-projects/03-eval-module",
            ],
            "practice": ["/07-hands-on-labs/03-eval-release-gate-lab"],
            "evidence": ["/13-output-gallery/02-eval-report-evidence", "/09-reference/09-release-brief"],
            "assessment": ["/10-assessments/03-eval-finetune-quiz"],
            "migration": ["/12-production-migration/03-eval-judge-dashboard-migration"],
        },
        "checkpoints": [
            "能解释 run、comparison、leaderboard 和 release recommendation 的关系。",
            "能说明 benchmark 分数为什么不能直接等价为生产质量。",
            "能把 sample analysis 放进发布复盘，而不是只看一个总分。",
        ],
        "facilitator_notes": [
            "现场讨论至少一个反例：分数提高但不应发布的情况。",
            "把 release recommendation 视为辅助信号，保留人工 review 问题。",
        ],
    },
    {
        "id": "training-lineage",
        "title": "训练资产复现模块",
        "audience": "想理解 dataset、run、checkpoint、export、manifest 和 lineage 的读者。",
        "outcome": "能从训练输入追到导出产物，并解释复现所需的最小证据。",
        "entry_route": "/05-finetuning-training/00-overview",
        "route_groups": {
            "orient": ["/05-finetuning-training/00-overview", "/05-finetuning-training/07-when-to-finetune"],
            "core": [
                "/05-finetuning-training/02-run-artifacts-export",
                "/05-finetuning-training/04-datasets-runs-checkpoints",
                "/05-finetuning-training/06-experiment-tracking-history-reproducibility",
                "/06-projects/04-finetune-demo",
            ],
            "practice": ["/07-hands-on-labs/04-finetune-reproducibility-lab"],
            "evidence": ["/13-output-gallery/03-finetune-artifact-evidence"],
            "assessment": ["/10-assessments/03-eval-finetune-quiz"],
            "migration": ["/12-production-migration/04-finetune-real-training-migration"],
        },
        "checkpoints": [
            "能说明 dataset version、checkpoint index 和 export manifest 的关系。",
            "能判断一次 export 是否有足够 lineage 证据。",
            "能说明 demo trainer 迁移到真实训练系统时要替换哪些执行层。",
        ],
        "facilitator_notes": [
            "让读者先读 manifest，再回看命令，这样更容易建立复现意识。",
            "不要把 mock checkpoint 当作真实训练效果，重点是产物契约。",
        ],
    },
    {
        "id": "public-sharing",
        "title": "公开分享与共学模块",
        "audience": "准备把项目发到 GitHub、组织学习小组或做公开演示的人。",
        "outcome": "能把个人学习项目整理成可带练、可复盘、可贡献的公开材料。",
        "entry_route": "/14-workshop-kit/00-overview",
        "route_groups": {
            "orient": ["/00-overview/11-public-learning-guide", "/08-publication/00-overview"],
            "core": [
                "/08-publication/01-github-pages",
                "/08-publication/02-content-style-guide",
                "/14-workshop-kit/00-overview",
                "/14-workshop-kit/01-facilitator-guide",
                "/14-workshop-kit/02-learner-workbook",
            ],
            "practice": ["/07-hands-on-labs/06-public-release-readiness-lab"],
            "share": ["/14-workshop-kit/04-review-templates", "/14-workshop-kit/06-github-release-plan"],
            "evidence": [
                "/13-output-gallery/07-generated-evidence-packet",
                "/09-reference/10-course-catalog",
                "/14-workshop-kit/07-generated-workshop-packet",
                "/10-assessments/06-generated-assessment-pack",
                "/09-reference/09-release-brief",
                "/08-publication/05-generated-roadmap-pack",
                "/08-publication/13-generated-launch-pack",
                "/08-publication/14-github-entrypoints",
            ],
        },
        "checkpoints": [
            "能为不同读者选择合适的学习主线。",
            "能用 evidence packet、course catalog、workshop packet、assessment pack、release brief、roadmap pack 和 launch pack 组织公开复盘。",
            "能把贡献入口和发布边界讲清楚。",
        ],
        "facilitator_notes": [
            "共学前先选一个模块，不要把全站一次性讲完。",
            "把 feedback 收到 issue 或 PR 模板里，避免只停留在聊天记录。",
        ],
    },
    {
        "id": "production-migration",
        "title": "生产迁移思维模块",
        "audience": "已经跑通学习闭环，想理解下一步如何接近真实生产系统的人。",
        "outcome": "能识别学习型实现和生产级系统之间的接口、观测、数据和运维差距。",
        "entry_route": "/12-production-migration/00-overview",
        "route_groups": {
            "orient": ["/12-production-migration/00-overview", "/00-overview/14-project-maturity-map"],
            "core": [
                "/12-production-migration/01-serving-backend-migration",
                "/12-production-migration/02-gateway-platform-hardening",
                "/12-production-migration/03-eval-judge-dashboard-migration",
                "/12-production-migration/04-finetune-real-training-migration",
            ],
            "practice": ["/07-hands-on-labs/06-public-release-readiness-lab"],
            "evidence": ["/09-reference/07-validation-matrix", "/09-reference/09-release-brief"],
            "assessment": ["/10-assessments/04-capstone-defense"],
        },
        "checkpoints": [
            "能说明哪些接口应该稳定保留，哪些执行层可以替换。",
            "能用验证矩阵判断一次迁移改动该跑哪些检查。",
            "能把生产化下一步拆成 serving、gateway、eval 和 training 四条路线。",
        ],
        "facilitator_notes": [
            "把讨论聚焦在迁移边界和风险，不要过早追求大而全架构。",
            "要求读者为每个迁移方向写出一个可验证的小改动。",
        ],
    },
]


class CourseCatalogError(RuntimeError):
    """Raised when the course catalog cannot be built safely."""


def build_course_catalog(inventory_path: Path = DEFAULT_INVENTORY, *, strict: bool = False) -> dict[str, Any]:
    inventory_path = inventory_path.resolve()
    inventory = load_inventory(inventory_path)
    route_map = build_route_map(inventory)
    track_map = {track["id"]: track for track in inventory.get("course_tracks", [])}

    modules: list[dict[str, Any]] = []
    missing_routes: set[str] = set()
    missing_track_ids: list[str] = []

    for order, module_definition in enumerate(CATALOG_MODULES, start=1):
        module, module_missing_routes, missing_track_id = build_module(
            module_definition,
            order=order,
            route_map=route_map,
            track_map=track_map,
        )
        modules.append(module)
        missing_routes.update(module_missing_routes)
        if missing_track_id:
            missing_track_ids.append(missing_track_id)

    validation = {
        "inventory_available": True,
        "missing_route_count": len(missing_routes),
        "missing_routes": sorted(missing_routes),
        "missing_track_count": len(missing_track_ids),
        "missing_track_ids": missing_track_ids,
        "ready_for_workshop": not missing_routes and not missing_track_ids,
    }
    catalog = {
        "report_type": "ai_infra_course_catalog",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "source_inventory": str(inventory_path),
        "summary": build_summary(inventory, modules, validation),
        "validation": validation,
        "program_outcomes": [
            "读者能从概念地图进入可运行项目，而不是只读静态文章。",
            "读者能用 lab、assessment 和 evidence 验证自己是否真正理解。",
            "维护者能把公开分享、PR 复盘和发布检查放到同一套材料中。",
        ],
        "modules": modules,
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
        "maintenance_notes": [
            "新增关键学习页后，先把它加入 VitePress sidebar，再决定是否加入课程目录模块。",
            "新增课程主线后，同时更新 build_learning_inventory.py 和 build_course_catalog.py。",
            "公开带练前优先检查 course_catalog.md、release_brief.md、workshop_packet.md、assessment_pack.md、roadmap_pack.md 和 launch_pack.md。",
        ],
    }

    if strict and not validation["ready_for_workshop"]:
        raise CourseCatalogError("; ".join(validation_errors(validation)))

    return catalog


def load_inventory(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise CourseCatalogError(f"inventory file does not exist: {path}")
    payload = json.loads(path.read_text())
    if payload.get("report_type") != "ai_infra_learning_inventory":
        raise CourseCatalogError("inventory report_type must be ai_infra_learning_inventory")
    return payload


def build_route_map(inventory: dict[str, Any]) -> dict[str, dict[str, Any]]:
    route_map: dict[str, dict[str, Any]] = {}
    for section in inventory.get("sections", []):
        for page in section.get("pages", []):
            route_map[page["route"]] = {
                **page,
                "section_title": section.get("title", page.get("section_id", "")),
            }
    return route_map


def build_module(
    module_definition: dict[str, Any],
    *,
    order: int,
    route_map: dict[str, dict[str, Any]],
    track_map: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], list[str], str | None]:
    module_id = module_definition["id"]
    track = track_map.get(module_id)
    missing_track_id = None if track else module_id
    route_groups: list[dict[str, Any]] = []
    missing_routes: list[str] = []
    unique_routes: set[str] = set()
    total_learning_weight = 0

    for group_id, routes in module_definition["route_groups"].items():
        pages, group_missing_routes = build_group_pages(routes, route_map)
        route_groups.append(
            {
                "id": group_id,
                "title": GROUP_TITLES.get(group_id, group_id),
                "route_count": len(routes),
                "matched_route_count": len(pages),
                "missing_routes": group_missing_routes,
                "pages": pages,
            }
        )
        missing_routes.extend(group_missing_routes)
        unique_routes.update(page["route"] for page in pages)
        total_learning_weight += sum(page["learning_weight"] for page in pages)

    if track:
        missing_routes.extend(track.get("missing_routes", []))

    module = {
        "order": order,
        "id": module_id,
        "title": module_definition["title"],
        "audience": module_definition["audience"],
        "outcome": module_definition["outcome"],
        "entry_route": module_definition["entry_route"],
        "entry_title": route_map.get(module_definition["entry_route"], {}).get(
            "title", module_definition["entry_route"]
        ),
        "track_goal": track.get("goal") if track else None,
        "track_route_count": track.get("route_count", 0) if track else 0,
        "unique_route_count": len(unique_routes),
        "learning_weight": total_learning_weight,
        "estimated_study_blocks": estimate_study_blocks(total_learning_weight, len(unique_routes)),
        "missing_route_count": len(set(missing_routes)),
        "missing_routes": sorted(set(missing_routes)),
        "route_groups": route_groups,
        "checkpoints": module_definition["checkpoints"],
        "facilitator_notes": module_definition["facilitator_notes"],
    }
    return module, module["missing_routes"], missing_track_id


def build_group_pages(
    routes: list[str], route_map: dict[str, dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[str]]:
    pages: list[dict[str, Any]] = []
    missing_routes: list[str] = []
    for route in routes:
        page = route_map.get(route)
        if page is None:
            missing_routes.append(route)
            continue
        pages.append(
            {
                "title": page["title"],
                "route": page["route"],
                "relative_path": page["relative_path"],
                "section_id": page["section_id"],
                "section_title": page["section_title"],
                "learning_weight": page["learning_weight"],
                "code_block_count": page["code_block_count"],
            }
        )
    return pages, missing_routes


def estimate_study_blocks(learning_weight: int, route_count: int) -> int:
    if route_count == 0:
        return 0
    by_weight = max(1, (learning_weight + 3499) // 3500)
    by_routes = max(1, (route_count + 3) // 4)
    return max(by_weight, by_routes)


def build_summary(
    inventory: dict[str, Any], modules: list[dict[str, Any]], validation: dict[str, Any]
) -> dict[str, Any]:
    unique_routes = {page["route"] for module in modules for group in module["route_groups"] for page in group["pages"]}
    return {
        "module_count": len(modules),
        "unique_route_count": len(unique_routes),
        "docs_pages": inventory.get("summary", {}).get("page_count", 0),
        "course_tracks": inventory.get("summary", {}).get("course_track_count", 0),
        "missing_route_count": validation["missing_route_count"],
        "missing_track_count": validation["missing_track_count"],
        "ready_for_workshop": validation["ready_for_workshop"],
        "estimated_study_blocks": sum(module["estimated_study_blocks"] for module in modules),
    }


def validation_errors(validation: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if validation["missing_track_ids"]:
        errors.append(f"missing course tracks: {', '.join(validation['missing_track_ids'])}")
    if validation["missing_routes"]:
        errors.append(f"missing catalog routes: {', '.join(validation['missing_routes'])}")
    return errors


def write_outputs(catalog: dict[str, Any], output: Path, markdown_output: Path) -> tuple[Path, Path]:
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    markdown_output.write_text(render_markdown(catalog))
    return output, markdown_output


def render_markdown(catalog: dict[str, Any]) -> str:
    summary = catalog["summary"]
    validation = catalog["validation"]
    lines = [
        "# AI Infra Course Catalog",
        "",
        f"- Generated at: `{catalog['generated_at']}`",
        f"- Modules: `{summary['module_count']}`",
        f"- Unique catalog routes: `{summary['unique_route_count']}`",
        f"- Docs pages: `{summary['docs_pages']}`",
        f"- Estimated study blocks: `{summary['estimated_study_blocks']}`",
        f"- Ready for workshop: `{summary['ready_for_workshop']}`",
        "",
        "## Validation",
        "",
        "| Signal | Value |",
        "| --- | --- |",
        f"| Missing catalog routes | `{validation['missing_route_count']}` |",
        f"| Missing course tracks | `{validation['missing_track_count']}` |",
        f"| Ready for workshop | `{validation['ready_for_workshop']}` |",
        "",
        "## Program Outcomes",
        "",
    ]
    lines.extend(f"- {outcome}" for outcome in catalog["program_outcomes"])

    lines.extend(["", "## Modules", ""])
    for module in catalog["modules"]:
        lines.extend(
            [
                f"### {module['order']}. {module['title']}",
                "",
                f"- Audience: {module['audience']}",
                f"- Outcome: {module['outcome']}",
                f"- Entry: `{module['entry_title']}` (`{module['entry_route']}`)",
                f"- Unique routes: `{module['unique_route_count']}`",
                f"- Estimated study blocks: `{module['estimated_study_blocks']}`",
                f"- Missing routes: `{module['missing_route_count']}`",
                "",
                "| Group | Pages | Routes |",
                "| --- | ---: | --- |",
            ]
        )
        for group in module["route_groups"]:
            route_list = "<br>".join(f"`{page['route']}`" for page in group["pages"])
            if group["missing_routes"]:
                missing = "<br>".join(f"`{route}`" for route in group["missing_routes"])
                route_list = f"{route_list}<br>Missing: {missing}" if route_list else f"Missing: {missing}"
            lines.append(f"| {group['title']} | {group['matched_route_count']}/{group['route_count']} | {route_list} |")

        lines.extend(["", "Checkpoints:"])
        lines.extend(f"- {checkpoint}" for checkpoint in module["checkpoints"])
        lines.extend(["", "Facilitator notes:"])
        lines.extend(f"- {note}" for note in module["facilitator_notes"])
        lines.append("")

    lines.extend(
        [
            "## Recommended Commands",
            "",
        ]
    )
    lines.extend(f"- `{command}`" for command in catalog["recommended_commands"])
    lines.extend(["", "## Maintenance Notes", ""])
    lines.extend(f"- {note}" for note in catalog["maintenance_notes"])
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a workshop-ready course catalog from the learning inventory.")
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN_OUTPUT)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    catalog = build_course_catalog(args.inventory, strict=args.strict)
    json_target, markdown_target = write_outputs(catalog, args.output, args.markdown_output)
    print(f"Wrote course catalog JSON to {json_target}")
    print(f"Wrote course catalog Markdown to {markdown_target}")
    print(f"Modules: {catalog['summary']['module_count']}")
    print(f"Ready for workshop: {catalog['summary']['ready_for_workshop']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
