"""openai_code_lib.py — HTTP + prompt logic for the OpenAI Responses API coder helper.

All HTTP calls use stdlib urllib only. No third-party deps.
"""
import json
import os
import urllib.request
import urllib.error

_DEFAULT_MODEL = "gpt-5.5"
_API_URL = "https://api.openai.com/v1/responses"


def call_openai(prompt: str, model: str = None) -> str:
    """POST to OpenAI Responses API. Returns output_text string.

    Raises RuntimeError with a diagnostic message on any non-200 response,
    missing API key, missing response field, or network error.
    Never falls back to a different model — caller sees the error clearly.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY env var is not set. "
            "Export it before running: export OPENAI_API_KEY=sk-..."
        )
    resolved_model = model or os.environ.get("OPENAI_CODE_MODEL", _DEFAULT_MODEL)
    payload = json.dumps({"model": resolved_model, "input": prompt}).encode("utf-8")
    req = urllib.request.Request(
        _API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"OpenAI API returned HTTP {exc.code} for model={resolved_model}.\n"
            f"Response body: {body}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error reaching {_API_URL}: {exc.reason}") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"OpenAI response was not valid JSON.\nRaw: {raw[:500]}"
        ) from exc
    if "output_text" not in data:
        raise RuntimeError(
            f"OpenAI response JSON missing 'output_text' field. "
            f"Got keys: {list(data.keys())}\nRaw: {raw[:500]}"
        )
    return data["output_text"]


def _read_file_safe(path: str) -> str:
    """Read a file and return its content, or an error note if unreadable."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        return f"[Could not read {path}: {exc}]"


def build_draft_prompt(spec: str, files: list, conventions: str) -> str:
    """Build the code-generation prompt with spec, sibling files, conventions, and hard rules.

    Instructs OpenAI to return ONLY code — no prose, no markdown fences.
    """
    parts = [
        "You are an expert software engineer. Write the implementation described below.",
        "",
        "=== SPEC ===",
        spec,
        "",
        "=== CONVENTIONS ===",
        conventions,
        "",
        "=== SIBLING FILES (for context — follow their patterns) ===",
    ]
    for path in files:
        parts.append(f"--- {path} ---")
        parts.append(_read_file_safe(path))
        parts.append("")
    parts += [
        "=== HARD RULES ===",
        "1. Every file MUST be 150 lines or fewer. Split into multiple files if needed.",
        "2. Return ONLY the code. No explanations, no markdown code fences, no prose.",
        "3. If multiple files are needed, separate them with: === FILE: <path> ===",
        "4. Use structured logging only — no print() or console.log.",
        "5. Wrap all errors with context (operation name, params, original error as cause).",
        "6. No hardcoded secrets or config values.",
        "7. Type all function signatures and return types.",
    ]
    return "\n".join(parts)


def build_review_prompt(code: str, spec: str) -> str:
    """Build the self-review prompt checking invariants, security, silent failures, 150-line rule.

    Final line of OpenAI's response must be: VERDICT: APPROVE or VERDICT: REVISE.
    """
    return "\n".join([
        "You are a senior code reviewer. Review the code below against the spec.",
        "",
        "=== SPEC ===",
        spec,
        "",
        "=== CODE UNDER REVIEW ===",
        code,
        "",
        "=== REVIEW CHECKLIST ===",
        "1. Invariant violations: null/None inputs, empty collections, boundary values.",
        "2. Silent failures: exceptions caught but not logged or re-raised.",
        "3. Security surfaces: unvalidated inputs, hardcoded secrets, injection vectors.",
        "4. 150-line compliance: flag any file section exceeding 150 lines.",
        "5. Type completeness: missing type annotations on signatures or return types.",
        "6. Missing error context: bare throws without operation name or params.",
        "",
        "List each issue found (if any). Then end your response with exactly one of:",
        "VERDICT: APPROVE",
        "VERDICT: REVISE",
    ])


def build_fix_prompt(code: str, failures: str) -> str:
    """Build the fix prompt: here's the code, here's what failed, return corrected code only."""
    return "\n".join([
        "You are an expert software engineer. Fix the code below based on the failure output.",
        "",
        "=== FAILING CODE ===",
        code,
        "",
        "=== FAILURE OUTPUT ===",
        failures,
        "",
        "=== INSTRUCTIONS ===",
        "1. Fix every error shown in the failure output.",
        "2. Keep all files at or under 150 lines.",
        "3. Return ONLY the corrected code — no explanations, no markdown fences.",
        "4. If multiple files are needed, separate them with: === FILE: <path> ===",
    ])
