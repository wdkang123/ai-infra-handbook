from __future__ import annotations

from hashlib import sha256
from pathlib import Path


def file_artifact_entry(root: Path, relative_path: str) -> dict[str, str | int]:
    path = root / relative_path
    digest = sha256(path.read_bytes()).hexdigest()
    return {
        "path": relative_path,
        "size_bytes": path.stat().st_size,
        "sha256": digest,
    }


def build_artifact_entries(root: Path, relative_paths: list[str]) -> list[dict[str, str | int]]:
    return [file_artifact_entry(root, relative_path) for relative_path in sorted(relative_paths)]
