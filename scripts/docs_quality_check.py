"""Lightweight documentation quality checks for the learning site."""

from __future__ import annotations

import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, unquote, urlparse

ROOT_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT_DIR / "docs"
CONFIG_PATH = DOCS_DIR / ".vitepress" / "config.mts"
HOME_LAUNCH_PADS = DOCS_DIR / ".vitepress" / "theme" / "components" / "HomeLaunchPads.vue"
VITEPRESS_THEME_DIR = DOCS_DIR / ".vitepress" / "theme"
LLMS_ROOT = ROOT_DIR / "llms.txt"
LLMS_PUBLIC = DOCS_DIR / "public" / "llms.txt"
VITEPRESS_SPECIAL_RE = re.compile(r"""[\s~`!@#$%^&*()\-_+=[\]{}|\\;:"'“”‘’<>,.?/]+""")

CHECKED_MARKDOWN_FILES = [
    ROOT_DIR / "README.md",
    ROOT_DIR / "CONTRIBUTING.md",
    ROOT_DIR / "PUBLICATION_CHECKLIST.md",
    ROOT_DIR / "CHANGELOG.md",
    *sorted(path for path in DOCS_DIR.rglob("*.md") if ".vitepress" not in path.parts),
]

CHECKED_VUE_FILES = sorted(VITEPRESS_THEME_DIR.rglob("*.vue"))

REQUIRED_README_LINKS = [
    "docs/00-overview/00-zero-to-one.md",
    "docs/00-overview/02-learning-route.md",
    "docs/00-overview/12-course-syllabus.md",
    "docs/00-overview/14-project-maturity-map.md",
    "docs/00-overview/15-two-week-learning-plan.md",
    "docs/07-hands-on-labs/00-overview.md",
    "docs/07-hands-on-labs/06-public-release-readiness-lab.md",
    "docs/11-case-studies/00-overview.md",
    "docs/13-output-gallery/00-overview.md",
    "docs/13-output-gallery/07-generated-evidence-packet.md",
    "docs/14-workshop-kit/00-overview.md",
    "docs/14-workshop-kit/07-generated-workshop-packet.md",
    "docs/12-production-migration/00-overview.md",
    "docs/10-assessments/00-overview.md",
    "docs/10-assessments/06-generated-assessment-pack.md",
    "docs/08-publication/05-generated-roadmap-pack.md",
    "docs/08-publication/13-generated-launch-pack.md",
    "docs/09-reference/05-api-surface.md",
    "docs/09-reference/06-cli-surface.md",
    "docs/09-reference/07-validation-matrix.md",
    "docs/09-reference/08-learning-inventory.md",
    "docs/09-reference/09-release-brief.md",
    "docs/09-reference/10-course-catalog.md",
    "PUBLICATION_CHECKLIST.md",
]

REQUIRED_PUBLICATION_LINKS = [
    "/00-overview/14-project-maturity-map",
    "/07-hands-on-labs/06-public-release-readiness-lab",
    "/13-output-gallery/00-overview",
    "/14-workshop-kit/00-overview",
    "/14-workshop-kit/07-generated-workshop-packet",
    "/10-assessments/06-generated-assessment-pack",
    "/08-publication/05-generated-roadmap-pack",
    "/08-publication/13-generated-launch-pack",
    "/09-reference/09-release-brief",
    "/09-reference/10-course-catalog",
]


@dataclass(frozen=True)
class LinkIssue:
    source: Path
    line: int
    target: str
    message: str


def main() -> int:
    issues: list[str] = []
    link_issues = find_broken_markdown_links()
    issues.extend(format_link_issue(issue) for issue in link_issues)
    issues.extend(format_link_issue(issue) for issue in check_vitepress_config_links())
    issues.extend(format_link_issue(issue) for issue in check_vitepress_component_links())
    issues.extend(check_sidebar_coverage())
    issues.extend(check_markdown_structure())
    issues.extend(check_home_doc_count())
    issues.extend(check_readme_publication_links())
    issues.extend(check_llms_txt_sync())

    if issues:
        print("Documentation quality check failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    markdown_count = count_docs_markdown()
    print(f"Documentation quality check passed ({markdown_count} docs pages checked).")
    return 0


def find_broken_markdown_links() -> list[LinkIssue]:
    issues: list[LinkIssue] = []
    anchor_cache: dict[Path, set[str]] = {}
    for source in CHECKED_MARKDOWN_FILES:
        if not source.exists():
            continue
        text = strip_fenced_code(source.read_text())
        for line_number, line in enumerate(text.splitlines(), start=1):
            for target in extract_markdown_links(line):
                if should_skip_link(target):
                    continue
                anchor = extract_anchor(target)
                resolved = resolve_link(source, target)
                if resolved is None:
                    issues.append(LinkIssue(source, line_number, target, "could not resolve local markdown target"))
                    continue
                if anchor and resolved.suffix == ".md":
                    anchors = anchor_cache.setdefault(resolved, collect_markdown_anchors(resolved))
                    if not anchor_exists(anchor, anchors):
                        issues.append(LinkIssue(source, line_number, target, "could not resolve local heading anchor"))
    return issues


def extract_markdown_links(line: str) -> list[str]:
    targets = [match.group("target").strip() for match in re.finditer(r"(?<!!)\[[^\]]+\]\((?P<target>[^)]+)\)", line)]
    html_targets = [
        match.group("target").strip() for match in re.finditer(r"""href=["'](?P<target>[^"']+)["']""", line)
    ]
    frontmatter_targets = [
        match.group("target").strip().strip("\"'")
        for match in re.finditer(r"^\s*link:\s*(?P<target>/[^\s#]+(?:#[^\s]+)?)\s*$", line)
    ]
    return [*targets, *html_targets, *frontmatter_targets]


def should_skip_link(target: str) -> bool:
    if not target or target == "#":
        return True
    parsed = urlparse(target)
    if parsed.scheme in {"http", "https", "mailto"}:
        return True
    return bool(target.startswith("file:"))


def extract_anchor(target: str) -> str:
    parsed = urlparse(target)
    return parsed.fragment


def resolve_link(source: Path, target: str) -> Path | None:
    target_without_anchor = unquote(target.split("#", 1)[0]).strip()
    if not target_without_anchor:
        return source
    if target_without_anchor.startswith("/"):
        if target_without_anchor == "/":
            candidates = [DOCS_DIR / "index.md"]
        else:
            relative = target_without_anchor.lstrip("/")
            candidates = candidates_for_path(DOCS_DIR / relative)
    else:
        candidates = candidates_for_path((source.parent / target_without_anchor).resolve())
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def candidates_for_path(path: Path) -> list[Path]:
    if path.suffix:
        return [path]
    return [path, path.with_suffix(".md"), path / "index.md"]


def strip_fenced_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def collect_markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    seen_slugs: dict[str, int] = {}
    text = strip_fenced_code(path.read_text())
    for line in text.splitlines():
        heading_match = re.match(r"^\s{0,3}#{1,6}\s+(?P<heading>.+?)\s*$", line)
        if heading_match:
            heading = heading_match.group("heading").strip()
            explicit_match = re.search(r"\s*\{#(?P<anchor>[-_a-zA-Z0-9\u4e00-\u9fff]+)\}\s*$", heading)
            if explicit_match:
                anchors.add(explicit_match.group("anchor"))
                heading = heading[: explicit_match.start()].strip()
            for slug in slug_candidates(heading):
                anchors.update(unique_slug_variants(slug, seen_slugs))
        for html_id in re.findall(r"""id=["'](?P<anchor>[^"']+)["']""", line):
            anchors.add(html_id)
    return anchors


def unique_slug_variants(slug: str, seen_slugs: dict[str, int]) -> set[str]:
    if not slug:
        return set()
    if slug not in seen_slugs:
        seen_slugs[slug] = 1
        return {slug}
    suffix = seen_slugs[slug]
    seen_slugs[slug] += 1
    return {slug, f"{slug}-{suffix}"}


def slug_candidates(heading: str) -> set[str]:
    text = normalize_heading_text(heading)
    if not text:
        return set()
    vitepress_slug = vitepress_slugify(text)
    spaced = re.sub(r"\s+", "-", text.strip().lower())
    punctuation_light = re.sub(r"[`*_~()[\]{}<>.,，。:：;；!?！？/\\|\"'“”‘’]", "", spaced)
    collapsed = re.sub(r"-+", "-", punctuation_light).strip("-")
    candidates = {vitepress_slug, spaced, collapsed}
    encoded_candidates = {quote(candidate, safe="-%_") for candidate in candidates if candidate}
    return {candidate for candidate in [*candidates, *encoded_candidates] if candidate}


def vitepress_slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    normalized = re.sub(r"[\u0300-\u036f]", "", normalized)
    normalized = re.sub(r"[\u0000-\u001f]", "", normalized)
    slug = VITEPRESS_SPECIAL_RE.sub("-", normalized)
    slug = re.sub(r"-{2,}", "-", slug).strip("-").lower()
    if slug[:1].isdigit():
        return f"_{slug}"
    return slug


def normalize_heading_text(heading: str) -> str:
    text = re.sub(r"\s+#+\s*$", "", heading).strip()
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def anchor_exists(anchor: str, anchors: set[str]) -> bool:
    decoded = unquote(anchor)
    return anchor in anchors or decoded in anchors or decoded.lower() in anchors


def check_vitepress_config_links() -> list[LinkIssue]:
    issues: list[LinkIssue] = []
    anchor_cache: dict[Path, set[str]] = {}
    for line_number, target in extract_vitepress_config_links():
        if should_skip_link(target):
            continue
        resolved = resolve_link(CONFIG_PATH, target)
        if resolved is None:
            issues.append(LinkIssue(CONFIG_PATH, line_number, target, "could not resolve VitePress config route"))
            continue
        anchor = extract_anchor(target)
        if anchor and resolved.suffix == ".md":
            anchors = anchor_cache.setdefault(resolved, collect_markdown_anchors(resolved))
            if not anchor_exists(anchor, anchors):
                issues.append(LinkIssue(CONFIG_PATH, line_number, target, "could not resolve VitePress config anchor"))
    return issues


def check_vitepress_component_links() -> list[LinkIssue]:
    issues: list[LinkIssue] = []
    anchor_cache: dict[Path, set[str]] = {}
    for source in CHECKED_VUE_FILES:
        for line_number, target in extract_vitepress_component_links(source):
            if should_skip_link(target):
                continue
            resolved = resolve_link(source, target)
            if resolved is None:
                issues.append(LinkIssue(source, line_number, target, "could not resolve VitePress component route"))
                continue
            anchor = extract_anchor(target)
            if anchor and resolved.suffix == ".md":
                anchors = anchor_cache.setdefault(resolved, collect_markdown_anchors(resolved))
                if not anchor_exists(anchor, anchors):
                    issues.append(
                        LinkIssue(source, line_number, target, "could not resolve VitePress component anchor")
                    )
    return issues


def extract_vitepress_config_links() -> list[tuple[int, str]]:
    links: list[tuple[int, str]] = []
    for line_number, line in enumerate(CONFIG_PATH.read_text().splitlines(), start=1):
        for match in re.finditer(r'link:\s*"(?P<target>[^"]+)"', line):
            links.append((line_number, match.group("target").strip()))
    return links


def extract_vitepress_component_links(source: Path) -> list[tuple[int, str]]:
    links: list[tuple[int, str]] = []
    for line_number, line in enumerate(source.read_text().splitlines(), start=1):
        for pattern in [
            r'(?<![:\w-])href\s*=\s*"(?P<target>[^"]+)"',
            r"(?<![:\w-])href\s*=\s*'(?P<target>[^']+)'",
            r'href:\s*"(?P<target>[^"]+)"',
            r"href:\s*'(?P<target>[^']+)'",
        ]:
            for match in re.finditer(pattern, line):
                links.append((line_number, match.group("target").strip()))
    return links


def check_sidebar_coverage() -> list[str]:
    config_text = CONFIG_PATH.read_text()
    sidebar_block = extract_sidebar_block(config_text)
    sidebar_links = set(re.findall(r'link:\s*"(?P<link>/[^"]*)"', sidebar_block))
    issues: list[str] = []
    for page in sorted(DOCS_DIR.rglob("*.md")):
        if ".vitepress" in page.parts:
            continue
        expected_link = "/" if page.name == "index.md" else "/" + page.relative_to(DOCS_DIR).with_suffix("").as_posix()
        if expected_link not in sidebar_links:
            issues.append(f"{relative(page)} is not linked from docs/.vitepress/config.mts sidebar")
    return issues


def check_markdown_structure() -> list[str]:
    issues: list[str] = []
    for page in sorted(DOCS_DIR.rglob("*.md")):
        if ".vitepress" in page.parts or page.name == "index.md":
            continue
        text = strip_fenced_code(page.read_text())
        h1_lines = [
            line_number for line_number, line in enumerate(text.splitlines(), start=1) if re.match(r"^#\s+\S", line)
        ]
        if not h1_lines:
            issues.append(f"{relative(page)} should include one top-level H1 heading")
        elif len(h1_lines) > 1:
            issues.append(f"{relative(page)} should include only one top-level H1 heading, found {len(h1_lines)}")
    return issues


def extract_sidebar_block(config_text: str) -> str:
    sidebar_start = config_text.find("sidebar:")
    if sidebar_start == -1:
        return ""
    footer_start = config_text.find("outline:", sidebar_start)
    if footer_start == -1:
        return config_text[sidebar_start:]
    return config_text[sidebar_start:footer_start]


def check_home_doc_count() -> list[str]:
    text = HOME_LAUNCH_PADS.read_text()
    match = re.search(r"<strong>(?P<count>\d+)</strong>\s*<span>文档页</span>", text)
    if match is None:
        return [f"{relative(HOME_LAUNCH_PADS)} does not expose the docs page stat"]
    actual = count_docs_markdown()
    expected = int(match.group("count"))
    if expected != actual:
        return [f"{relative(HOME_LAUNCH_PADS)} docs page stat is {expected}, expected {actual}"]
    return []


def check_readme_publication_links() -> list[str]:
    issues: list[str] = []
    readme_text = (ROOT_DIR / "README.md").read_text()
    for target in REQUIRED_README_LINKS:
        if target not in readme_text:
            issues.append(f"README.md should link to {target}")

    publication_text = (DOCS_DIR / "08-publication" / "00-overview.md").read_text()
    for target in REQUIRED_PUBLICATION_LINKS:
        if target not in publication_text:
            issues.append(f"docs/08-publication/00-overview.md should link to {target}")
    return issues


def check_llms_txt_sync() -> list[str]:
    if not LLMS_ROOT.exists():
        return ["llms.txt is missing from the repository root"]
    if not LLMS_PUBLIC.exists():
        return ["docs/public/llms.txt is missing from the public docs assets"]
    if LLMS_ROOT.read_text() != LLMS_PUBLIC.read_text():
        return ["llms.txt and docs/public/llms.txt should stay identical"]
    return []


def count_docs_markdown() -> int:
    return sum(1 for path in DOCS_DIR.rglob("*.md") if ".vitepress" not in path.parts)


def format_link_issue(issue: LinkIssue) -> str:
    return f"{relative(issue.source)}:{issue.line} link '{issue.target}' {issue.message}"


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT_DIR).as_posix()


if __name__ == "__main__":
    sys.exit(main())
