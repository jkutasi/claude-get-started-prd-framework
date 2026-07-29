"""Mechanical risk detection for changed paths and diff content."""

from __future__ import annotations

import hashlib
import re
import stat
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

MAX_UNTRACKED_REVIEW_BYTES = 1_000_000


@dataclass(frozen=True)
class RiskFinding:
    source: str
    trigger: str
    detail: str


def _run_git(repo_root: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout


def changed_files(repo_root: Path, base: str | None = None) -> list[str]:
    """Return tracked and untracked changed paths."""
    diff_args = ["diff", "--name-only"]
    if base:
        diff_args.append(base)
    tracked = _run_git(repo_root, diff_args).splitlines()
    if not base:
        tracked.extend(
            _run_git(repo_root, ["diff", "--cached", "--name-only"]).splitlines()
        )
    untracked = _run_git(
        repo_root, ["ls-files", "--others", "--exclude-standard"]
    ).splitlines()
    return sorted(
        {path.replace("\\", "/") for path in [*tracked, *untracked] if path.strip()}
    )


def changed_diff(
    repo_root: Path,
    files: list[str],
    base: str | None = None,
    excluded_files: set[str] | None = None,
) -> str:
    """Return the tracked diff plus bounded text from untracked files."""
    excluded = {
        path.replace("\\", "/") for path in (excluded_files or set())
    }
    included = [path for path in files if path not in excluded]
    tracked = set(
        _run_git(repo_root, ["ls-files"]).replace("\\", "/").splitlines()
    )
    tracked_files = [path for path in included if path in tracked]
    untracked_files = [path for path in included if path not in tracked]
    parts: list[str] = []
    if tracked_files:
        pathspecs = [f":(literal){path}" for path in tracked_files]
        diff_args = ["diff", "--no-ext-diff", "--unified=0"]
        if base:
            diff_args.append(base)
        parts.append(_run_git(repo_root, [*diff_args, "--", *pathspecs]))
        if not base:
            parts.append(
                _run_git(
                    repo_root,
                    ["diff", "--cached", "--unified=0", "--", *pathspecs],
                )
            )
    oversized: list[str] = []
    inaccessible: list[str] = []
    for relative in untracked_files:
        path = repo_root / relative
        try:
            details = path.stat()
        except OSError as exc:
            inaccessible.append(f"{relative} ({exc})")
            continue
        if not stat.S_ISREG(details.st_mode):
            inaccessible.append(f"{relative} (not a regular file)")
        elif details.st_size > MAX_UNTRACKED_REVIEW_BYTES:
            oversized.append(f"{relative} ({details.st_size} bytes)")
    if oversized or inaccessible:
        messages: list[str] = []
        if oversized:
            messages.append(
                "untracked files exceed the 1,000,000-byte review limit: "
                + ", ".join(oversized)
            )
        if inaccessible:
            messages.append(
                "untracked files cannot be reviewed: " + ", ".join(inaccessible)
            )
        raise RuntimeError("; ".join(messages))

    for relative in untracked_files:
        path = repo_root / relative
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            raise RuntimeError(
                f"untracked file cannot be reviewed: {relative} ({exc})"
            ) from exc
        parts.append(f"\n+++ untracked/{relative}\n")
        parts.append("\n".join(f"+{line}" for line in text.splitlines()))
    return "\n".join(parts)


def canonical_diff_sha256(
    repo_root: Path,
    files: list[str],
    base: str | None = None,
    excluded_files: set[str] | None = None,
) -> str:
    """Hash the exact changed content reviewed by the frontier reviewer."""
    content = changed_diff(repo_root, files, base, excluded_files)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def detect_risk(
    files: list[str], diff_text: str, config: dict[str, Any]
) -> list[RiskFinding]:
    """Return every configured path or diff trigger."""
    findings: list[RiskFinding] = []
    for pattern in config["risk"]["path_patterns"]:
        regex = re.compile(pattern, re.IGNORECASE)
        for path in files:
            if regex.search(path):
                findings.append(RiskFinding("path", pattern, path))

    added_text = "\n".join(
        line[1:]
        for line in diff_text.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    )
    for item in config["risk"]["diff_patterns"]:
        name = item.get("name", "unnamed diff trigger")
        pattern = item.get("pattern")
        if not isinstance(pattern, str):
            continue
        if re.search(pattern, added_text, re.IGNORECASE | re.MULTILINE):
            findings.append(RiskFinding("diff", name, pattern))
    return findings


def classify_change(
    repo_root: Path, config: dict[str, Any], base: str | None = None
) -> tuple[list[str], list[RiskFinding]]:
    files = changed_files(repo_root, base)
    return files, detect_risk(files, changed_diff(repo_root, files, base), config)
