"""
gate_check_tests.py — Run pytest for a slice if pytest is available.

Public API:
    check_slice_tests(slice_n, repo_root) -> list[str]
    Returns a list of failure messages; empty list means PASS (or skipped).
"""
import importlib.util
import subprocess
import sys
from pathlib import Path


def _pytest_available() -> bool:
    """Return True if pytest is importable in the current Python environment."""
    return importlib.util.find_spec("pytest") is not None


def _test_config_exists(repo_root: Path) -> bool:
    """Return True if a pytest config file is present at the repo root."""
    for name in ("pyproject.toml", "pytest.ini", "setup.cfg", "tox.ini"):
        if (repo_root / name).is_file():
            return True
    return False


def _tail_lines(text: str, n: int) -> str:
    """Return the last n lines of text, joined as a single string."""
    lines = text.splitlines()
    return "\n".join(lines[-n:]) if lines else ""


def check_slice_tests(slice_n: int, repo_root: Path) -> list[str]:
    """
    Run pytest if it is installed and a config file exists at repo root.

    The slice_n argument is accepted for API consistency and future use
    (e.g. running only tests tagged for that slice).

    Args:
        slice_n:   The slice number (integer).
        repo_root: Absolute path to the repository root.

    Returns:
        List of human-readable failure messages.
        An empty list means tests passed or the check was skipped.
    """
    if not _pytest_available():
        return []

    if not _test_config_exists(repo_root):
        return []

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        return []

    # Collect stderr; fall back to stdout if stderr is empty.
    output = result.stderr.strip() or result.stdout.strip()
    summary = _tail_lines(output, 5)
    return [f"tests failed: {summary}"]
