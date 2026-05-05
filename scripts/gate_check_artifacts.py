"""
gate_check_artifacts.py — Verify per-slice review artifact files exist.

Public API:
    check_slice_artifacts(slice_n, repo_root, strict) -> list[str]
    Returns a list of missing-artifact messages; empty list means PASS.
"""
from pathlib import Path


# Always required for every slice.
_REQUIRED_ARTIFACTS = [
    "slice-{n}-test-spec.md",
    "slice-{n}-test-review.md",
    "slice-{n}-peer-review.md",
    "slice-{n}-qa-swarm.md",
    "slice-{n}-red-team-pre-build.md",
    "slice-{n}-red-team.md",
    "slice-{n}-whiskey-team.md",
]

# Only required when --strict is passed.
# peer-review-pass2: required when round-1 was REQUEST_CHANGES.
#   For now we include it unconditionally under --strict because we cannot
#   detect REQUEST_CHANGES status without parsing the review file itself.
# ux-sense-check: required for UI slices.
#   TODO: detect from slice manifest when a manifest format is defined.
_STRICT_ARTIFACTS = [
    "slice-{n}-peer-review-pass2.md",
    "slice-{n}-ux-sense-check.md",
]


def _reviews_dir(repo_root: Path) -> Path:
    return repo_root / "reviews"


def _artifact_path(reviews: Path, template: str, n: int) -> Path:
    return reviews / template.replace("{n}", str(n))


def check_slice_artifacts(
    slice_n: int,
    repo_root: Path,
    strict: bool,
) -> list[str]:
    """
    Check that every required artifact file exists for slice_n.

    Args:
        slice_n:   The slice number (integer).
        repo_root: Absolute path to the repository root.
        strict:    When True, also check conditionally-required artifacts.

    Returns:
        List of human-readable missing-artifact messages.
        An empty list means every checked artifact is present (PASS).
    """
    reviews = _reviews_dir(repo_root)
    missing: list[str] = []

    templates = list(_REQUIRED_ARTIFACTS)
    if strict:
        templates.extend(_STRICT_ARTIFACTS)

    for tmpl in templates:
        artifact = _artifact_path(reviews, tmpl, slice_n)
        if not artifact.is_file():
            # Relative path for readability in output.
            rel = artifact.relative_to(repo_root)
            missing.append(f"missing: {rel.as_posix()}")

    return missing
