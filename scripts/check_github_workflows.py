"""Check this template for retired Claude GitHub Action configuration."""

from __future__ import annotations

import sys
from pathlib import Path


def failures(repo_root: Path) -> list[str]:
    workflow_dir = repo_root / ".github" / "workflows"
    problems: list[str] = []
    paths = {*workflow_dir.glob("*.yml"), *workflow_dir.glob("*.yaml")}
    for path in sorted(paths):
        text = path.read_text(encoding="utf-8", errors="replace")
        relative = path.relative_to(repo_root).as_posix()
        if "anthropics/claude-code-action@beta" in text:
            problems.append(f"{relative}: uses retired @beta action")
        if "direct_prompt:" in text:
            problems.append(f"{relative}: uses retired direct_prompt input")
        if "anthropics/claude-code-action@" in text:
            if "anthropics/claude-code-action@v1" not in text:
                problems.append(f"{relative}: Claude action must use @v1")
            if "prompt:" not in text:
                problems.append(f"{relative}: Claude action is missing prompt input")
    return problems


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    problems = failures(repo_root)
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}")
        return 1
    print("GitHub workflow configuration: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
