"""Risk-aware deterministic completion gate."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))

from risk_check import (  # noqa: E402
    RiskFinding,
    canonical_diff_sha256,
    changed_files,
    classify_change,
)
from workflow_config import (  # noqa: E402
    ConfigError,
    load_config,
    orchestrator_model,
    provider_policy_failures,
)

APPROVED = "APPROVE"


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"record not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"record must be a JSON object: {path}")
    return value


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_high_risk_record(
    path: Path,
    change_id: str,
    config: dict[str, Any],
    expected_diff_sha256: str,
    expected_orchestrator: str | None = None,
) -> list[str]:
    """Validate independent sign-off, verification, and rollback evidence."""
    try:
        record = _read_json(path)
    except ValueError as exc:
        return [str(exc)]
    failures: list[str] = []
    if record.get("change_id") != change_id:
        failures.append("high-risk record change_id does not match")
    if record.get("risk_level") != "high":
        failures.append("high-risk record risk_level must be 'high'")

    author = record.get("author_model")
    reviewer = record.get("reviewer_model")
    orchestrator = record.get("orchestrator_model")
    frontier = {
        config["models"]["default_orchestrator"],
        config["models"]["alternate_orchestrator"],
    }
    if not _nonempty(author):
        failures.append("author_model is required")
    if reviewer not in frontier:
        failures.append("reviewer must be Fable 5 or GPT-5.6 Sol")
    if _nonempty(author) and reviewer == author:
        failures.append("reviewer must not be the author")
    if reviewer == orchestrator:
        failures.append("reviewer must be the other frontier model")
    if expected_orchestrator and orchestrator != expected_orchestrator:
        failures.append("record orchestrator does not match the active orchestrator")

    plan_review = record.get("plan_review")
    if not isinstance(plan_review, dict) or plan_review.get("verdict") != APPROVED:
        failures.append("plan_review.verdict must be APPROVE")
    elif not _nonempty(plan_review.get("requirements_source")):
        failures.append("plan_review.requirements_source is required")
    diff_review = record.get("diff_review")
    if not isinstance(diff_review, dict) or diff_review.get("verdict") != APPROVED:
        failures.append("diff_review.verdict must be APPROVE")
    elif not _nonempty(diff_review.get("scope")):
        failures.append("diff_review.scope is required")
    elif diff_review.get("diff_sha256") != expected_diff_sha256:
        failures.append("diff_review.diff_sha256 does not match the current diff")
    verification = record.get("verification")
    if not isinstance(verification, dict) or verification.get("status") != "PASS":
        failures.append("verification.status must be PASS")
    rollback = record.get("rollback")
    if not isinstance(rollback, dict):
        failures.append("rollback evidence is missing")
    elif not _nonempty(rollback.get("method")) or not _nonempty(
        rollback.get("evidence")
    ):
        failures.append("rollback.method and rollback.evidence are required")
    review_counts = record.get("review_counts")
    limits = config["limits"]
    expected_limits = {
        "plan": "plan_review_passes",
        "diff": "diff_review_passes",
        "scoped_followups": "scoped_followups",
    }
    if not isinstance(review_counts, dict):
        failures.append("review_counts is required")
    else:
        for field, limit_field in expected_limits.items():
            value = review_counts.get(field)
            if not isinstance(value, int) or value < 0:
                failures.append(f"review_counts.{field} must be a non-negative integer")
            elif field in {"plan", "diff"} and value < 1:
                failures.append(f"review_counts.{field} must be at least 1")
            elif value > limits[limit_field]:
                failures.append(f"review_counts.{field} exceeds configured limit")
    return failures


def validate_downgrade(path: Path, change_id: str | None = None) -> list[str]:
    try:
        record = _read_json(path)
    except ValueError as exc:
        return [str(exc)]
    failures: list[str] = []
    if change_id and record.get("change_id") != change_id:
        failures.append("risk downgrade change_id does not match")
    if record.get("approved_by") != "user":
        failures.append("risk downgrade must have approved_by set to 'user'")
    if not _nonempty(record.get("rationale")):
        failures.append("risk downgrade requires a rationale")
    return failures


def _paths_overlap(left: str, right: str) -> bool:
    a = left.strip("/").replace("\\", "/").casefold()
    b = right.strip("/").replace("\\", "/").casefold()
    return a == b or a.startswith(f"{b}/") or b.startswith(f"{a}/")


def ownership_failures(repo_root: Path, config: dict[str, Any]) -> list[str]:
    path = repo_root / config["records"]["ownership_file"]
    if not path.is_file():
        return []
    try:
        record = _read_json(path)
    except ValueError as exc:
        return [str(exc)]
    tasks = record.get("tasks", [])
    if not isinstance(tasks, list):
        return ["ownership tasks must be a list"]
    failures: list[str] = []
    claims: list[tuple[str, str]] = []
    for task in tasks:
        if not isinstance(task, dict) or task.get("status") != "active":
            continue
        task_id = str(task.get("id", "unknown"))
        attempts = task.get("attempts", 0)
        if isinstance(attempts, int) and attempts > config["limits"]["worker_attempts"]:
            failures.append(
                f"worker attempts exceeded for {task_id}: "
                f"{attempts}/{config['limits']['worker_attempts']}"
            )
        for owned_path in task.get("paths", []):
            if isinstance(owned_path, str):
                claims.append((task_id, owned_path))
    for index, (task_a, path_a) in enumerate(claims):
        for task_b, path_b in claims[index + 1 :]:
            if task_a != task_b and _paths_overlap(path_a, path_b):
                failures.append(
                    f"overlapping ownership: {task_a}:{path_a} and {task_b}:{path_b}"
                )
    return failures


def handoff_failures(
    repo_root: Path, config: dict[str, Any], active_orchestrator: str
) -> list[str]:
    path = repo_root / config["records"]["handoff_file"]
    if not path.is_file():
        return []
    try:
        record = _read_json(path)
    except ValueError as exc:
        return [str(exc)]
    required_text = (
        "task_id",
        "from_orchestrator",
        "to_orchestrator",
        "reason",
        "goal",
    )
    failures = [
        f"handoff.{field} is required"
        for field in required_text
        if not _nonempty(record.get(field))
    ]
    if record.get("to_orchestrator") != active_orchestrator:
        failures.append("handoff target does not match active orchestrator")
    if record.get("repository_reconciled") is not True:
        failures.append("handoff repository_reconciled must be true")
    commands = record.get("reconciliation_commands")
    if not isinstance(commands, list) or not commands:
        failures.append("handoff reconciliation_commands are required")
    return failures


def budget_failures(
    config: dict[str, Any],
    tokens_used: int | None,
    cost_usd: float | None,
) -> list[str]:
    failures: list[str] = []
    max_tokens = config["limits"].get("max_total_tokens")
    max_cost = config["limits"].get("max_cost_usd")
    if max_tokens is not None:
        if tokens_used is None:
            failures.append("tokens-used is required when max_total_tokens is configured")
        elif tokens_used > max_tokens:
            failures.append(f"token budget exceeded: {tokens_used}/{max_tokens}")
    if max_cost is not None:
        if cost_usd is None:
            failures.append("cost-usd is required when max_cost_usd is configured")
        elif cost_usd > max_cost:
            failures.append(f"cost budget exceeded: {cost_usd}/{max_cost}")
    return failures


def run_checks(repo_root: Path, commands: list[str]) -> tuple[list[str], list[dict]]:
    failures: list[str] = []
    results: list[dict] = []
    for command in commands:
        started = time.monotonic()
        result = subprocess.run(
            command,
            cwd=repo_root,
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        elapsed = round(time.monotonic() - started, 3)
        results.append(
            {
                "command": command,
                "exit_code": result.returncode,
                "elapsed_seconds": elapsed,
            }
        )
        if result.returncode:
            output = (result.stderr.strip() or result.stdout.strip()).splitlines()
            failures.append(
                f"check failed ({command}): {' | '.join(output[-5:])}"
            )
        else:
            print(f"PASS: {command}")
    return failures, results


def write_metrics(
    repo_root: Path,
    config: dict[str, Any],
    change_id: str,
    risk_level: str,
    orchestrator: str,
    files: list[str],
    check_results: list[dict],
    passed: bool,
    tokens_used: int | None,
    cost_usd: float | None,
) -> None:
    path = repo_root / config["records"]["metrics_file"]
    path.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "change_id": change_id,
        "risk_level": risk_level,
        "orchestrator": orchestrator_model(config, orchestrator),
        "changed_files": files,
        "checks": check_results,
        "passed": passed,
        "tokens_used": tokens_used,
        "cost_usd": cost_usd,
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, separators=(",", ":")) + "\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--change-id", required=True)
    parser.add_argument("--orchestrator", choices=("fable", "sol"), required=True)
    parser.add_argument("--risk", choices=("auto", "normal", "high"), default="auto")
    parser.add_argument("--base", help="Git revision used as the diff base.")
    parser.add_argument("--config", type=Path)
    parser.add_argument(
        "--downgrade-record",
        type=Path,
        help="Deprecated; if supplied, must equal the configured durable path.",
    )
    parser.add_argument("--tokens-used", type=int)
    parser.add_argument("--cost-usd", type=float)
    parser.add_argument("--no-metrics", action="store_true")
    return parser


def _format_finding(finding: RiskFinding) -> str:
    return f"{finding.source}:{finding.trigger} ({finding.detail})"


def main() -> int:
    args = build_parser().parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    try:
        config = load_config(repo_root, args.config)
    except ConfigError as exc:
        print(f"FAIL: {exc}")
        return 1

    classification_failure: str | None = None
    try:
        files, findings = classify_change(repo_root, config, args.base)
    except RuntimeError as exc:
        classification_failure = str(exc)
        findings = []
        try:
            files = changed_files(repo_root, args.base)
        except RuntimeError as files_exc:
            files = []
            classification_failure = (
                f"{classification_failure}; changed paths unavailable: {files_exc}"
            )

    detected_high = bool(findings) or classification_failure is not None
    risk_level = "high" if detected_high else "normal"
    failures = provider_policy_failures(config, args.orchestrator)
    if classification_failure:
        failures.append(f"risk classification failed: {classification_failure}")
    failures.extend(ownership_failures(repo_root, config))
    failures.extend(
        handoff_failures(
            repo_root,
            config,
            orchestrator_model(config, args.orchestrator),
        )
    )
    failures.extend(budget_failures(config, args.tokens_used, args.cost_usd))

    if args.risk == "high":
        risk_level = "high"
    elif args.risk == "normal":
        if classification_failure:
            risk_level = "high"
            failures.append(
                "risk cannot be downgraded when changed content was not reviewed"
            )
        else:
            risk_level = "normal"
        if detected_high and not classification_failure:
            downgrade_path = (
                repo_root
                / config["records"]["downgrade_dir"]
                / f"{args.change_id}.downgrade.json"
            )
            if (
                args.downgrade_record
                and args.downgrade_record.resolve() != downgrade_path.resolve()
            ):
                failures.append(
                    "downgrade record must use the configured durable review path"
                )
            if not downgrade_path.is_file():
                failures.append(
                    f"mechanical high-risk trigger requires {downgrade_path}"
                )
            else:
                failures.extend(validate_downgrade(downgrade_path, args.change_id))

    if classification_failure:
        print("Risk triggers: classification incomplete; forcing high risk")
    elif findings:
        print("Risk triggers:")
        for finding in findings:
            print(f"  - {_format_finding(finding)}")
    else:
        print("Risk triggers: none")

    commands = list(config["checks"]["normal"])
    if risk_level == "high":
        targeted = config["checks"]["high_risk"]
        if not targeted:
            failures.append("checks.high_risk must be configured for high-risk work")
        commands.extend(targeted)
        review_path = (
            repo_root
            / config["records"]["high_risk_dir"]
            / f"{args.change_id}.json"
        )
        review_relative = review_path.relative_to(repo_root).as_posix()
        diff_sha256: str | None = None
        if not classification_failure:
            try:
                diff_sha256 = canonical_diff_sha256(
                    repo_root,
                    files,
                    args.base,
                    {review_relative},
                )
            except RuntimeError as exc:
                failures.append(f"review diff hashing failed: {exc}")
        if diff_sha256:
            print(f"Review diff SHA-256: {diff_sha256}")
            failures.extend(
                validate_high_risk_record(
                    review_path,
                    args.change_id,
                    config,
                    diff_sha256,
                    orchestrator_model(config, args.orchestrator),
                )
            )

    check_failures, check_results = run_checks(repo_root, commands)
    failures.extend(check_failures)
    passed = not failures

    if not args.no_metrics:
        write_metrics(
            repo_root,
            config,
            args.change_id,
            risk_level,
            args.orchestrator,
            files,
            check_results,
            passed,
            args.tokens_used,
            args.cost_usd,
        )

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print(f"Gate: FAIL ({risk_level})")
        return 1
    print(f"Gate: PASS ({risk_level})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
