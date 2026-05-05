"""
gate_check_deploy.py — Verify the deployed SHA matches local HEAD.

Public API:
    check_deploy_sha(slice_n, repo_root) -> list[str]
    Returns a list of mismatch messages; empty list means PASS (or skipped).

Configuration (gate_check.config.json at repo root):
    {
      "deploy": {
        "provider": "<string label>",
        "query": "<shell command that prints the deployed commit SHA>"
      }
    }

If the config file is absent or lacks a "deploy" key, this check is skipped
and an empty list is returned.  Gate check never fails due to a missing config.
"""
import json
import subprocess
from pathlib import Path

_CONFIG_FILE = "gate_check.config.json"


def _load_deploy_config(repo_root: Path) -> dict | None:
    """
    Load the deploy stanza from gate_check.config.json.
    Returns None if the file or key is absent, or the JSON is malformed.
    """
    config_path = repo_root / _CONFIG_FILE
    if not config_path.is_file():
        return None
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
        return data.get("deploy") or None
    except (json.JSONDecodeError, OSError):
        return None


def _local_head_sha(repo_root: Path) -> str | None:
    """Return the SHA of the current git HEAD, or None on failure."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _run_query(query: str, repo_root: Path) -> str | None:
    """
    Run the user-supplied shell command and return its stdout (stripped).
    Returns None on non-zero exit or OSError.
    """
    try:
        result = subprocess.run(
            query,
            shell=True,  # noqa: S602 — user-supplied from config, not user input
            cwd=str(repo_root),
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return None
        return result.stdout.strip()
    except OSError:
        return None


def check_deploy_sha(slice_n: int, repo_root: Path) -> list[str]:
    """
    Compare the live deployed SHA against local git HEAD.

    Args:
        slice_n:   The slice number (accepted for API consistency; unused here).
        repo_root: Absolute path to the repository root.

    Returns:
        List of human-readable mismatch messages.
        An empty list means SHAs match or the check was skipped.
    """
    cfg = _load_deploy_config(repo_root)
    if cfg is None:
        return []

    query = cfg.get("query", "").strip()
    if not query:
        return []

    local_sha = _local_head_sha(repo_root)
    if local_sha is None:
        return ["deploy-sha: could not determine local HEAD (is this a git repo?)"]

    deployed_sha = _run_query(query, repo_root)
    if deployed_sha is None:
        provider = cfg.get("provider", "unknown")
        return [f"deploy-sha: query command failed for provider '{provider}'"]

    if local_sha != deployed_sha:
        return [
            f"deploy-sha mismatch: local={local_sha[:12]} deployed={deployed_sha[:12]}"
        ]

    return []
