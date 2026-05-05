"""
gate_check.py — Slice closure verifier.

Usage:
    python scripts/gate_check.py --all
    python scripts/gate_check.py --slice 1
    python scripts/gate_check.py --all --strict

Exit code: 0 = all slices PASS, 1 = any slice FAIL.
"""
import argparse
import re
import sys
from pathlib import Path

# Sibling modules — add scripts/ to path so this works when run directly
# or imported (e.g. python -c "import scripts.gate_check").
sys.path.insert(0, str(Path(__file__).parent))
from gate_check_artifacts import check_slice_artifacts  # noqa: E402
from gate_check_deploy import check_deploy_sha  # noqa: E402
from gate_check_sentry import check_slice_sentry  # noqa: E402
from gate_check_tests import check_slice_tests  # noqa: E402

_SLICE_PATTERN = re.compile(r"^slice-(\d+)$")


def discover_slices(repo_root: Path) -> list[int]:
    """Return sorted slice numbers from slices/slice-N/ directories."""
    slices_dir = repo_root / "slices"
    if not slices_dir.is_dir():
        return []
    numbers: list[int] = []
    for entry in slices_dir.iterdir():
        m = _SLICE_PATTERN.match(entry.name)
        if m and entry.is_dir():
            numbers.append(int(m.group(1)))
    return sorted(numbers)


# ---------------------------------------------------------------------------
# Per-slice verification
# ---------------------------------------------------------------------------
def verify_slice(slice_n: int, repo_root: Path, strict: bool) -> list[str]:
    """Aggregate all failure messages for one slice."""
    failures: list[str] = []
    failures.extend(check_slice_artifacts(slice_n, repo_root, strict))
    failures.extend(check_slice_tests(slice_n, repo_root))
    failures.extend(check_deploy_sha(slice_n, repo_root))
    failures.extend(check_slice_sentry(slice_n, repo_root))
    return failures


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Verify slice closure artifacts, tests, and deploy SHA.",
    )
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Verify every slice.")
    group.add_argument("--slice", type=int, metavar="N", help="Verify one slice.")
    p.add_argument(
        "--strict",
        action="store_true",
        help="Also require conditionally-optional artifacts.",
    )
    return p


def main() -> int:
    args = build_parser().parse_args()

    repo_root = Path(__file__).parent.parent.resolve()

    if args.all:
        slice_numbers = discover_slices(repo_root)
        if not slice_numbers:
            print("No slices found in slices/ — nothing to verify.")
            return 0
    else:
        slice_numbers = [args.slice]

    overall_pass = True
    for n in slice_numbers:
        failures = verify_slice(n, repo_root, args.strict)
        if failures:
            reasons = "; ".join(failures)
            print(f"slice-{n}: FAIL -- {reasons}")
            overall_pass = False
        else:
            print(f"slice-{n}: PASS")

    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
