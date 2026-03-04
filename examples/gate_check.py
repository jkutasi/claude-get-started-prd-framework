#!/usr/bin/env python3
"""
Gate Check Script — Validates that all required artifacts exist for a given slice.

Checks for the presence of mandatory and optional review artifacts, Gherkin feature
files, and unit tests before a slice can proceed through quality gates.

Usage:
    python gate_check.py --slice 3
    python gate_check.py --slice 3 --frontend
    python gate_check.py --all
    python gate_check.py --all --frontend --project-root /path/to/project

Exit codes:
    0 — All required artifacts present (PASS)
    1 — One or more required artifacts missing (FAIL)
    2 — Invalid arguments or configuration error
"""

import argparse
import glob
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MANDATORY_REVIEWS = [
    ("reviews/slice-{N}-test-spec.md", "Test Specification (Article 17)"),
    ("reviews/slice-{N}-test-review.md", "Test Peer Review (Article 18)"),
    ("reviews/slice-{N}-peer-review.md", "Peer Review"),
    ("reviews/slice-{N}-qa-swarm.md", "QA Swarm"),
    ("reviews/slice-{N}-red-team-pre-build.md", "Red Team Pre-Build Gate"),
    ("reviews/slice-{N}-red-team.md", "Red Team Post-QA Review"),
    ("reviews/slice-{N}-whiskey-team.md", "Whiskey Team Report"),
]

OPTIONAL_REVIEWS = [
    ("reviews/slice-{N}-ux-sense-check.md", "UX Sense Check", "--frontend"),
]

GHERKIN_PATTERN = "features/slice-{N}-*.feature"

# Unit tests can use either underscore or hyphen as separator
# Legacy patterns (tests/ directory)
UNIT_TEST_PATTERNS = [
    "tests/*slice_{N}*",
    "tests/*slice-{N}*",
]

# Feature-folder test patterns (Article 20a)
FEATURE_TEST_PATTERNS = [
    "src/**/*.test.*",
    "src/**/*_test.*",
    "src/**/*.spec.*",
]


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class CheckResult:
    """Result of a single artifact check."""
    name: str
    path_pattern: str
    required: bool
    found: bool
    matched_files: List[str] = field(default_factory=list)
    flag_needed: Optional[str] = None  # e.g. "--frontend"


@dataclass
class SliceReport:
    """Aggregate report for a single slice."""
    slice_number: int
    results: List[CheckResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(
            r.found for r in self.results if r.required
        )

    @property
    def missing_mandatory(self) -> List[CheckResult]:
        return [r for r in self.results if r.required and not r.found]

    @property
    def missing_optional(self) -> List[CheckResult]:
        return [r for r in self.results if not r.required and not r.found]

    @property
    def found_items(self) -> List[CheckResult]:
        return [r for r in self.results if r.found]


# ---------------------------------------------------------------------------
# Check functions
# ---------------------------------------------------------------------------

def resolve_pattern(pattern: str, slice_number: int) -> str:
    """Replace {N} placeholder with the actual slice number."""
    return pattern.replace("{N}", str(slice_number))


def check_file_exists(
    project_root: Path,
    pattern: str,
    slice_number: int,
    name: str,
    required: bool,
    flag_needed: Optional[str] = None,
) -> CheckResult:
    """Check if a specific file exists."""
    resolved = resolve_pattern(pattern, slice_number)
    full_path = project_root / resolved
    found = full_path.is_file() and full_path.stat().st_size > 0
    matched = [str(full_path)] if found else []
    return CheckResult(
        name=name,
        path_pattern=resolved,
        required=required,
        found=found,
        matched_files=matched,
        flag_needed=flag_needed,
    )


def check_glob_pattern(
    project_root: Path,
    pattern: str,
    slice_number: int,
    name: str,
    required: bool,
) -> CheckResult:
    """Check if any files match a glob pattern."""
    resolved = resolve_pattern(pattern, slice_number)
    full_pattern = str(project_root / resolved)
    matched = sorted(glob.glob(full_pattern))
    return CheckResult(
        name=name,
        path_pattern=resolved,
        required=required,
        found=len(matched) > 0,
        matched_files=matched,
    )


def count_code_lines(file_path: Path) -> int:
    """Count non-blank, non-comment lines in a source file."""
    comment_prefixes = ("#", "//", "*", "/*", "*/")
    count = 0
    try:
        with open(file_path, encoding="utf-8", errors="replace") as fh:
            in_block_comment = False
            for raw_line in fh:
                stripped = raw_line.strip()
                if not stripped:
                    continue
                # Python/JS block comments
                if stripped.startswith("/*"):
                    in_block_comment = True
                    continue
                if in_block_comment:
                    if stripped.endswith("*/"):
                        in_block_comment = False
                    continue
                # Python docstrings (triple-quote toggle)
                if stripped.startswith(('"""', "'''")):
                    # Single-line docstring
                    if stripped.count('"""') >= 2 or stripped.count("'''") >= 2:
                        continue
                    in_block_comment = True
                    continue
                if in_block_comment and (stripped.endswith('"""') or stripped.endswith("'''")):
                    in_block_comment = False
                    continue
                if stripped.startswith(comment_prefixes):
                    continue
                count += 1
    except OSError:
        return 0
    return count


def check_file_line_limit(
    project_root: Path,
    limit: int = 150,
) -> CheckResult:
    """Check that all production source files in src/ are under the line limit."""
    src_dir = project_root / "src"
    if not src_dir.is_dir():
        return CheckResult(
            name=f"150-Line File Limit (Article 20c)",
            path_pattern="src/**/*",
            required=True,
            found=True,
            matched_files=[],
        )

    source_extensions = {
        ".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs",
        ".java", ".kt", ".cs", ".rb", ".swift",
    }
    # Exclude test files from the hard limit
    test_indicators = {".test.", ".spec.", "_test."}

    violations: List[str] = []
    for root_dir, _dirs, files in os.walk(src_dir):
        for fname in files:
            fpath = Path(root_dir) / fname
            if fpath.suffix not in source_extensions:
                continue
            if any(indicator in fname for indicator in test_indicators):
                continue
            code_lines = count_code_lines(fpath)
            if code_lines > limit:
                violations.append(f"{fpath} ({code_lines} lines)")

    return CheckResult(
        name=f"150-Line File Limit (Article 20c)",
        path_pattern="src/**/*",
        required=True,
        found=len(violations) == 0,
        matched_files=violations,
    )


def check_slice(
    project_root: Path,
    slice_number: int,
    include_frontend: bool = False,
) -> SliceReport:
    """Run all checks for a single slice and return a report."""
    report = SliceReport(slice_number=slice_number)

    # --- Mandatory reviews ---
    for pattern, name in MANDATORY_REVIEWS:
        result = check_file_exists(
            project_root, pattern, slice_number, name, required=True
        )
        report.results.append(result)

    # --- Optional reviews (conditional on flags) ---
    for pattern, name, flag in OPTIONAL_REVIEWS:
        is_required = (flag == "--frontend" and include_frontend)
        result = check_file_exists(
            project_root, pattern, slice_number, name,
            required=is_required, flag_needed=flag
        )
        report.results.append(result)

    # --- Gherkin feature files ---
    result = check_glob_pattern(
        project_root, GHERKIN_PATTERN, slice_number,
        "Gherkin Feature Files", required=True
    )
    report.results.append(result)

    # --- Unit tests (match either naming convention) ---
    all_test_matches: List[str] = []
    for test_pattern in UNIT_TEST_PATTERNS:
        resolved = resolve_pattern(test_pattern, slice_number)
        full_pattern = str(project_root / resolved)
        all_test_matches.extend(glob.glob(full_pattern))

    # Feature-folder tests (Article 20a) — not slice-specific
    for test_pattern in FEATURE_TEST_PATTERNS:
        full_pattern = str(project_root / test_pattern)
        all_test_matches.extend(glob.glob(full_pattern, recursive=True))

    all_test_matches = sorted(set(all_test_matches))
    report.results.append(CheckResult(
        name="Unit Tests",
        path_pattern=f"tests/*slice_{slice_number}* or tests/*slice-{slice_number}* or src/**/*.test.*",
        required=True,
        found=len(all_test_matches) > 0,
        matched_files=all_test_matches,
    ))

    # --- 150-line file limit (Article 20c) ---
    report.results.append(check_file_line_limit(project_root))

    return report


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def discover_slices(project_root: Path) -> List[int]:
    """Discover all slice numbers from existing review files and contracts."""
    slice_numbers = set()
    search_dirs = ["reviews", "contracts", "features"]

    for search_dir in search_dirs:
        dir_path = project_root / search_dir
        if not dir_path.is_dir():
            continue
        for item in dir_path.iterdir():
            name = item.name.lower()
            # Extract slice numbers from filenames like "slice-3-..." or "slice_3_..."
            for sep in ["-", "_"]:
                prefix = f"slice{sep}"
                if prefix in name:
                    rest = name.split(prefix, 1)[1]
                    num_str = ""
                    for char in rest:
                        if char.isdigit():
                            num_str += char
                        else:
                            break
                    if num_str:
                        slice_numbers.add(int(num_str))

    return sorted(slice_numbers)


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

PASS_MARK = "[PASS]"
FAIL_MARK = "[FAIL]"
SKIP_MARK = "[SKIP]"
INFO_MARK = "[INFO]"

COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_CYAN = "\033[96m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"


def supports_color() -> bool:
    """Check if the terminal supports ANSI color codes."""
    if os.getenv("NO_COLOR"):
        return False
    if os.getenv("FORCE_COLOR"):
        return True
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def colorize(text: str, color: str) -> str:
    """Apply color if terminal supports it."""
    if supports_color():
        return f"{color}{text}{COLOR_RESET}"
    return text


def print_report(report: SliceReport) -> None:
    """Print a formatted report for a single slice."""
    header = f"Gate Check — Slice {report.slice_number}"
    print()
    print(colorize(f"{'=' * 60}", COLOR_BOLD))
    print(colorize(f"  {header}", COLOR_BOLD))
    print(colorize(f"{'=' * 60}", COLOR_BOLD))
    print()

    for result in report.results:
        if result.found:
            status = colorize(PASS_MARK, COLOR_GREEN)
            detail = ""
            if len(result.matched_files) > 1:
                detail = f" ({len(result.matched_files)} files)"
        elif not result.required:
            status = colorize(SKIP_MARK, COLOR_YELLOW)
            detail = ""
            if result.flag_needed:
                detail = f" (enable with {result.flag_needed})"
        else:
            status = colorize(FAIL_MARK, COLOR_RED)
            detail = f" -- MISSING: {result.path_pattern}"

        print(f"  {status}  {result.name}{detail}")
        # Show individual violations for line-limit check
        if not result.found and "150-Line" in result.name and result.matched_files:
            for violation in result.matched_files:
                print(colorize(f"           ↳ {violation}", COLOR_RED))

    # Summary
    print()
    if report.passed:
        verdict = colorize(f"{PASS_MARK} GATE CHECK PASSED", COLOR_GREEN)
        print(f"  {verdict} — Slice {report.slice_number} has all required artifacts.")
    else:
        verdict = colorize(f"{FAIL_MARK} GATE CHECK FAILED", COLOR_RED)
        print(f"  {verdict} — Slice {report.slice_number} is missing required artifacts:")
        for missing in report.missing_mandatory:
            print(colorize(f"    - {missing.name}: {missing.path_pattern}", COLOR_RED))

    if report.missing_optional:
        print()
        print(f"  {colorize(INFO_MARK, COLOR_CYAN)} Optional artifacts not present:")
        for opt in report.missing_optional:
            flag_hint = f" (enable with {opt.flag_needed})" if opt.flag_needed else ""
            print(f"    - {opt.name}: {opt.path_pattern}{flag_hint}")

    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Gate Check — Validate slice artifacts before proceeding.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --slice 3                  Check slice 3 (backend only)
  %(prog)s --slice 3 --frontend       Check slice 3 (including UX sense check)
  %(prog)s --all                      Check all discovered slices
  %(prog)s --all --frontend           Check all slices with frontend artifacts
  %(prog)s --slice 3 --project-root . Check slice 3 in current directory

Exit codes:
  0  All required artifacts present (PASS)
  1  One or more required artifacts missing (FAIL)
  2  Invalid arguments or configuration error
        """,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--slice", type=int, metavar="N",
        help="Check a specific slice number",
    )
    group.add_argument(
        "--all", action="store_true",
        help="Check all discovered slices",
    )

    parser.add_argument(
        "--frontend", action="store_true",
        help="Include frontend-specific checks (UX Sense Check)",
    )
    parser.add_argument(
        "--project-root", type=str, default=".",
        help="Path to the project root directory (default: current directory)",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point. Returns exit code."""
    args = parse_args()
    project_root = Path(args.project_root).resolve()

    if not project_root.is_dir():
        print(
            colorize(f"Error: Project root does not exist: {project_root}", COLOR_RED),
            file=sys.stderr,
        )
        return 2

    # Determine which slices to check
    if args.all:
        slice_numbers = discover_slices(project_root)
        if not slice_numbers:
            print(
                colorize(
                    "No slices discovered. Ensure your project has files matching "
                    "slice-N naming in reviews/, contracts/, or features/.",
                    COLOR_YELLOW,
                ),
            )
            return 2
        print(
            colorize(
                f"Discovered slices: {', '.join(str(n) for n in slice_numbers)}",
                COLOR_CYAN,
            ),
        )
    else:
        slice_numbers = [args.slice]

    # Run checks
    all_passed = True
    for slice_num in slice_numbers:
        report = check_slice(project_root, slice_num, include_frontend=args.frontend)
        print_report(report)
        if not report.passed:
            all_passed = False

    # Final summary for --all
    if args.all and len(slice_numbers) > 1:
        print(colorize(f"{'=' * 60}", COLOR_BOLD))
        if all_passed:
            print(colorize(
                f"  {PASS_MARK} ALL {len(slice_numbers)} SLICES PASSED GATE CHECK",
                COLOR_GREEN,
            ))
        else:
            print(colorize(
                f"  {FAIL_MARK} ONE OR MORE SLICES FAILED GATE CHECK",
                COLOR_RED,
            ))
        print(colorize(f"{'=' * 60}", COLOR_BOLD))
        print()

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
