"""
gate_check_artifacts.py — Verify per-slice review artifact files exist.

Public API:
    check_slice_artifacts(slice_n, repo_root, strict) -> list[str]
    Returns a list of missing-artifact messages; empty list means PASS.

Artifact pattern (post-consolidated-review migration):
    REQUIRED (always):
        reviews/slice-{N}.md          — consolidated review file

    CONDITIONALLY REQUIRED (--strict only):
        reviews/slice-{N}/peer-review-gemini.md
        reviews/slice-{N}/peer-review-openai.md
        reviews/slice-{N}/peer-review-grok.md
        reviews/slice-{N}/qa-api-contract.md
        reviews/slice-{N}/qa-backend.md
        reviews/slice-{N}/qa-routing.md
        reviews/slice-{N}/qa-data-integrity.md
        reviews/slice-{N}/qa-code-quality.md
        reviews/slice-{N}/qa-security.md   (any 6 of 7 QA checks pass)
        reviews/slice-{N}/smoke.md

    NOTE: The CTO peer review (4th model) does NOT have a separate file —
    its findings are recorded directly in the consolidated slice-{N}.md.
"""
from pathlib import Path

# Always required for every slice — the one consolidated review file.
_REQUIRED = "reviews/slice-{N}.md"

# Required when --strict is passed.
_STRICT_ARTIFACTS = [
    "reviews/slice-{N}/peer-review-gemini.md",
    "reviews/slice-{N}/peer-review-openai.md",
    "reviews/slice-{N}/peer-review-grok.md",
    "reviews/slice-{N}/qa-api-contract.md",
    "reviews/slice-{N}/qa-backend.md",
    "reviews/slice-{N}/qa-routing.md",
    "reviews/slice-{N}/qa-data-integrity.md",
    "reviews/slice-{N}/qa-code-quality.md",
    "reviews/slice-{N}/qa-security.md",
    "reviews/slice-{N}/smoke.md",
]

# Minimum QA checks that must be present under --strict.
# uiux is optional (frontend slices only), so we require 6 of the 7 types.
_QA_REQUIRED_COUNT = 6
_QA_PREFIXES = [t for t in _STRICT_ARTIFACTS if "/qa-" in t]
_NON_QA_STRICT = [t for t in _STRICT_ARTIFACTS if "/qa-" not in t]


def _reviews_dir(repo_root: Path) -> Path:
    return repo_root / "reviews"


def _resolve(repo_root: Path, template: str, n: int) -> Path:
    return repo_root / template.replace("{N}", str(n))


def check_slice_artifacts(
    slice_n: int,
    repo_root: Path,
    strict: bool,
) -> list[str]:
    """
    Check that required artifacts exist for slice_n.

    Args:
        slice_n:   The slice number (integer).
        repo_root: Absolute path to the repository root.
        strict:    When True, also verify the detail-level artifacts.

    Returns:
        List of human-readable missing-artifact messages.
        Empty list means PASS.
    """
    missing: list[str] = []

    # Always required: the consolidated review file.
    consolidated = _resolve(repo_root, _REQUIRED, slice_n)
    if not consolidated.is_file():
        rel = consolidated.relative_to(repo_root)
        missing.append(f"missing: {rel.as_posix()}")

    if not strict:
        return missing

    # Non-QA strict artifacts.
    for tmpl in _NON_QA_STRICT:
        artifact = _resolve(repo_root, tmpl, slice_n)
        if not artifact.is_file():
            rel = artifact.relative_to(repo_root)
            missing.append(f"missing: {rel.as_posix()}")

    # QA checks: require at least _QA_REQUIRED_COUNT of the defined QA files.
    found_qa = sum(
        1 for tmpl in _QA_PREFIXES
        if _resolve(repo_root, tmpl, slice_n).is_file()
    )
    if found_qa < _QA_REQUIRED_COUNT:
        missing.append(
            f"qa checks: only {found_qa}/{len(_QA_PREFIXES)} present "
            f"(need at least {_QA_REQUIRED_COUNT})"
        )

    return missing
