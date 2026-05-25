#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THIS_FILE = Path(__file__).resolve()
MAX_TEXT_SCAN_BYTES = 2_000_000
MAX_REPORTED_ISSUES = 80


@dataclass(frozen=True)
class PatternCheck:
    name: str
    pattern: re.Pattern[str]


@dataclass(frozen=True)
class Issue:
    path: Path
    line: int | None
    check: str
    detail: str


SECRET_CHECKS = [
    PatternCheck("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    PatternCheck("GitHub token", re.compile(r"\b(?:github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9_]{20,})\b")),
    PatternCheck("GitLab token", re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b")),
    PatternCheck("OpenAI-style long key", re.compile(r"\b(?:sk-proj-|sk-live-)[A-Za-z0-9_-]{20,}\b|\bsk-[A-Za-z0-9]{32,}\b")),
    PatternCheck("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    PatternCheck("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    PatternCheck("Google OAuth token", re.compile(r"\bya29\.[0-9A-Za-z_-]+\b")),
    PatternCheck("SendGrid API key", re.compile(r"\bSG\.[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}\b")),
    PatternCheck(
        "Private key block",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |)?PRIVATE KEY-----"),
    ),
    PatternCheck(
        "Database or broker URL",
        re.compile(
            r"\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqp|kafka|clickhouse|snowflake)"
            r"://[^\s\"'<>]+"
        ),
    ),
    PatternCheck(
        "Local absolute path",
        re.compile(
            r"(?i)(?:/Users/[^\s\"'<>]+|/home/[A-Za-z0-9._-]+/[^\s\"'<>]+|"
            r"C:\\Users\\[^\s\"'<>]+|/private/var/folders/[^\s\"'<>]+)"
        ),
    ),
]

PERSONAL_EMAIL_DOMAINS = (
    "126.com",
    "163.com",
    "gmail.com",
    "hotmail.com",
    "icloud.com",
    "outlook.com",
    "qq.com",
)

PRIVACY_CHECKS = [
    PatternCheck(
        "Personal email address",
        re.compile(
            r"\b[A-Za-z0-9._%+-]+@(?:"
            + "|".join(re.escape(domain) for domain in PERSONAL_EMAIL_DOMAINS)
            + r")\b",
            re.IGNORECASE,
        ),
    ),
    PatternCheck(
        "Potential phone number",
        re.compile(r"(?<!\d)(?:\+86[- ]?)?1[3-9]\d[- ]?\d{4}[- ]?\d{4}(?!\d)"),
    ),
    PatternCheck(
        "Potential Chinese national ID",
        re.compile(
            r"(?<!\d)[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])"
            r"(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx](?!\d)"
        ),
    ),
]

RISKY_SUFFIXES = {
    ".cer",
    ".crt",
    ".db",
    ".dump",
    ".gz",
    ".key",
    ".log",
    ".onnx",
    ".p12",
    ".parquet",
    ".pem",
    ".pfx",
    ".pt",
    ".pth",
    ".safetensors",
    ".sql",
    ".sqlite",
    ".sqlite3",
    ".tar",
    ".tgz",
    ".zip",
}

RISKY_FILENAMES = {
    ".envrc",
    ".netrc",
    ".npmrc",
    ".pypirc",
    "id_ed25519",
    "id_rsa",
}


def local_username() -> str | None:
    parts = ROOT.parts
    if len(parts) < 3 or parts[1] not in {"Users", "home"}:
        return None

    username = parts[2]
    if username in {"runner", "sandbox", "workspace"}:
        return None
    return username


def local_username_check() -> PatternCheck | None:
    username = local_username()
    if username is None:
        return None
    return PatternCheck("Local username", re.compile(rf"\b{re.escape(username)}\b", re.IGNORECASE))


def git_candidate_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    files = []
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        path = ROOT / raw.decode()
        if path.is_file():
            files.append(path)
    return sorted(files)


def relative(path: Path) -> Path:
    return path.relative_to(ROOT)


def read_scan_text(path: Path) -> str | None:
    data = path.read_bytes()
    if b"\0" in data:
        return None
    if len(data) > MAX_TEXT_SCAN_BYTES:
        return None
    return data.decode("utf-8", errors="replace")


def risky_filename_issue(path: Path) -> Issue | None:
    rel = relative(path)
    name = path.name
    if name.startswith(".env") and name != ".env.example":
        return Issue(rel, None, "Risky env file", "env files should stay local; commit .env.example only")
    if name in RISKY_FILENAMES or path.suffix.lower() in RISKY_SUFFIXES:
        return Issue(rel, None, "Risky file type", "logs, credentials, archives, databases, and model weights are not public-safe")
    return None


def scan_text_file(path: Path, text: str) -> list[Issue]:
    issues: list[Issue] = []
    rel = relative(path)
    checks = [*SECRET_CHECKS, *PRIVACY_CHECKS]
    username_check = local_username_check()
    if username_check is not None:
        checks.append(username_check)

    for line_number, line in enumerate(text.splitlines(), start=1):
        for check in checks:
            if path == THIS_FILE and check.name == "Local absolute path":
                continue
            if check.pattern.search(line):
                issues.append(Issue(rel, line_number, check.name, line.strip()[:180]))
    return issues


def main() -> int:
    files = git_candidate_files()
    issues: list[Issue] = []

    for path in files:
        filename_issue = risky_filename_issue(path)
        if filename_issue is not None:
            issues.append(filename_issue)
            continue

        text = read_scan_text(path)
        if text is None:
            continue
        issues.extend(scan_text_file(path, text))

    if issues:
        print("Security scan failed.")
        print(f"Candidate files scanned: {len(files)}")
        print(f"Issues found: {len(issues)}")
        print()
        for issue in issues[:MAX_REPORTED_ISSUES]:
            location = str(issue.path)
            if issue.line is not None:
                location = f"{location}:{issue.line}"
            print(f"- {location} [{issue.check}] {issue.detail}")
        if len(issues) > MAX_REPORTED_ISSUES:
            print(f"- ... {len(issues) - MAX_REPORTED_ISSUES} more issue(s) omitted")
        return 1

    print("Security scan passed.")
    print(f"Candidate files scanned: {len(files)}")
    print(
        "Checks: high-confidence secrets, private keys, connection strings, local paths, "
        "personal markers, and risky file types."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
