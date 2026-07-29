"""Direct GPT-5.6 Sol plan or diff reviewer using the Responses API."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))

from workflow_config import (  # noqa: E402
    ConfigError,
    load_config,
    provider_policy_failures,
)

API_URL = "https://api.openai.com/v1/responses"


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"cannot read {path}: {exc}") from exc


def _extract_text(response: dict[str, Any]) -> str:
    direct = response.get("output_text")
    if isinstance(direct, str) and direct.strip():
        return direct
    parts: list[str] = []
    for item in response.get("output", []):
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []):
            if not isinstance(content, dict):
                continue
            if content.get("type") == "refusal":
                refusal = content.get("refusal") or content.get("text") or "refused"
                raise PermissionError(str(refusal))
            text = content.get("text")
            if content.get("type") == "output_text" and isinstance(text, str):
                parts.append(text)
    if not parts:
        raise RuntimeError("OpenAI response contained no output text")
    return "\n".join(parts)


def call_sol(prompt: str, model: str, effort: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    payload = {
        "model": model,
        "input": prompt,
        "reasoning": {"effort": effort},
        "text": {"verbosity": "low"},
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"OpenAI network error: {exc.reason}") from exc
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("OpenAI returned invalid JSON") from exc
    if parsed.get("status") == "incomplete":
        raise RuntimeError(f"OpenAI response incomplete: {parsed.get('incomplete_details')}")
    return _extract_text(parsed)


def build_prompt(stage: str, requirements: str, subject: str) -> str:
    label = "PLAN" if stage == "plan" else "RAW DIFF AND VERIFICATION OUTPUT"
    return f"""You are the independent non-author frontier reviewer.
Review the original requirements and {label.lower()} without trusting the author's framing.

Return strict JSON with:
- verdict: APPROVE or REQUEST_CHANGES
- findings: array of objects with severity, location, issue, correction
- unresolved_risks: array of strings

Block on correctness, security, privacy, data loss, rollback, or unmet requirements.
Do not rewrite the implementation.

ORIGINAL REQUIREMENTS
{requirements}

{label}
{subject}
"""


def select_model(config: dict[str, Any], explicit_model: str | None) -> str:
    """Select an explicit override or the centrally configured Sol model."""
    return str(
        explicit_model
        or os.environ.get("OPENAI_REVIEW_MODEL")
        or config["models"]["alternate_orchestrator"]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("plan", "diff"))
    parser.add_argument("--requirements", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--model")
    parser.add_argument("--config", type=Path)
    parser.add_argument(
        "--effort",
        choices=("low", "medium", "high", "xhigh", "max"),
        default="high",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    try:
        config = load_config(repo_root, args.config)
        policy_failures = provider_policy_failures(config, "sol")
        if policy_failures:
            raise RuntimeError("; ".join(policy_failures))
        model = select_model(config, args.model)
        result = call_sol(
            build_prompt(
                args.stage,
                _read(args.requirements),
                _read(args.input),
            ),
            model,
            args.effort,
        )
    except PermissionError as exc:
        print(f"REFUSAL: {exc}", file=sys.stderr)
        return 3
    except (ConfigError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(result)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result + "\n", encoding="utf-8")
    try:
        verdict = json.loads(result).get("verdict")
    except json.JSONDecodeError:
        print("ERROR: reviewer output was not strict JSON", file=sys.stderr)
        return 1
    return 0 if verdict == "APPROVE" else 2


if __name__ == "__main__":
    sys.exit(main())
