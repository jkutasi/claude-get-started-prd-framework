"""
gate_check_sentry.py — Sentry post-deploy issue scan.

Public API:
    check_slice_sentry(slice_n, repo_root) -> list[str]

Config (gate_check.config.json, "sentry" key): org, project,
release_query, since_minutes.  Missing config -> silent skip.
Present config but no SENTRY_AUTH_TOKEN -> failure (explicit intent).
Standard library only: urllib, json, os, subprocess.
"""
import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

_CONFIG_FILE = "gate_check.config.json"
_DEFAULT_RELEASE_QUERY = "git rev-parse HEAD"
_DEFAULT_SINCE_MINUTES = 60
_SENTRY_API_BASE = "https://sentry.io/api/0"


def _load_sentry_config(repo_root: Path) -> dict | None:
    """
    Load the sentry stanza from gate_check.config.json.
    Returns None if the file or key is absent, or JSON is malformed.
    """
    config_path = repo_root / _CONFIG_FILE
    if not config_path.is_file():
        return None
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
        return data.get("sentry") or None
    except (json.JSONDecodeError, OSError):
        return None


def _run_shell(cmd: str, repo_root: Path) -> str | None:
    """
    Run a shell command and return stripped stdout.
    Returns None on non-zero exit or OSError.
    """
    try:
        result = subprocess.run(
            cmd,
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


def _fetch_issues(org: str, project: str, release: str,
                  since_minutes: int, token: str) -> tuple[list[dict], str | None]:
    """
    Call the Sentry issues API.
    Returns (issues_list, error_message).
    On success error_message is None.
    """
    query_str = f"release:{release}+age:-{since_minutes}m"
    url = (
        f"{_SENTRY_API_BASE}/projects/{org}/{project}/issues/"
        f"?query={query_str}&limit=10"
    )
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body), None
    except urllib.error.HTTPError as exc:
        return [], f"sentry: HTTP {exc.code} from Sentry API ({exc.reason})"
    except urllib.error.URLError as exc:
        return [], f"sentry: network error contacting Sentry API ({exc.reason})"
    except (json.JSONDecodeError, OSError) as exc:
        return [], f"sentry: unexpected error reading Sentry response ({exc})"


def check_slice_sentry(slice_n: int, repo_root: Path) -> list[str]:
    """
    Scan Sentry for new issues on the current release.

    Args:
        slice_n:   Slice number (accepted for API consistency; unused here).
        repo_root: Absolute path to the repository root.

    Returns:
        List of human-readable failure messages.
        Empty list means PASS or the check was silently skipped.
    """
    cfg = _load_sentry_config(repo_root)
    if cfg is None:
        return []  # silent skip — no sentry config present

    # Config present: validate token before doing anything else.
    token = os.environ.get("SENTRY_AUTH_TOKEN", "").strip()
    if not token:
        return ["sentry: SENTRY_AUTH_TOKEN env not set"]

    org = cfg.get("org", "").strip()
    project = cfg.get("project", "").strip()
    if not org or not project:
        return ["sentry: config missing required 'org' and/or 'project' fields"]

    release_query = cfg.get("release_query", _DEFAULT_RELEASE_QUERY).strip()
    since_minutes = int(cfg.get("since_minutes", _DEFAULT_SINCE_MINUTES))

    release = _run_shell(release_query, repo_root)
    if not release:
        return [f"sentry: release_query command failed: {release_query!r}"]

    issues, err = _fetch_issues(org, project, release, since_minutes, token)
    if err:
        return [err]

    if not issues:
        return []

    first_title = issues[0].get("title", "<no title>")
    failures = [
        f"sentry: {len(issues)} new issue(s) on release {release[:12]}"
        f" (since {since_minutes}m): {first_title}"
    ]
    for issue in issues[1:3]:
        failures.append(f"  - {issue.get('title', '<no title>')}")

    return failures
