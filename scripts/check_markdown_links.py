"""Check local links in tracked Markdown files."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def tracked_markdown(repo_root: Path) -> list[Path]:
    paths: set[str] = set()
    for args in (
        ["git", "ls-files", "*.md"],
        ["git", "ls-files", "--others", "--exclude-standard", "*.md"],
    ):
        result = subprocess.run(
            args,
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "git ls-files failed")
        paths.update(line for line in result.stdout.splitlines() if line)
    return [repo_root / line for line in sorted(paths)]


def broken_links(repo_root: Path) -> list[str]:
    failures: list[str] = []
    for file_path in tracked_markdown(repo_root):
        if not file_path.is_file():
            continue
        text = file_path.read_text(encoding="utf-8", errors="replace")
        for match in LINK_RE.finditer(text):
            raw = match.group(1).strip().strip("<>")
            target = raw.split("#", 1)[0]
            if not target or re.match(r"^(https?:|mailto:|app:)", target):
                continue
            if any(marker in target for marker in ("{", "}", "<", ">")):
                continue
            resolved = (file_path.parent / unquote(target)).resolve()
            if not resolved.exists():
                relative = file_path.relative_to(repo_root).as_posix()
                failures.append(f"{relative}: missing link target {raw}")
    return sorted(set(failures))


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    failures = broken_links(repo_root)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("Markdown links: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
