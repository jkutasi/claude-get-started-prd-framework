"""openai_qa.py — `qa` subcommand for the OpenAI Responses API coder helper.

Usage:
    python scripts/openai_qa.py --code <path> --check <type> --slice <N> [--model M]

Exit codes:
    0  PASS — QA found no issues.
    1  Error — API call or file I/O failed.
    2  FAIL — QA found issues in the code.

Environment variables:
    OPENAI_API_KEY     Required.
    OPENAI_CODE_MODEL  Optional. Defaults to gpt-5.5.
"""
import argparse
import os
import sys

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from openai_code_lib import call_openai  # noqa: E402
from openai_qa_lib import build_qa_prompt, check_types  # noqa: E402


def _read(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        print(f"ERROR: Cannot read '{path}': {exc}", file=sys.stderr)
        sys.exit(1)


def _write(path: str, content: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def cmd_qa(args: argparse.Namespace) -> int:
    """Run a QA check on a code file and write the report to reviews/slice-N/."""
    code = _read(args.code)

    try:
        prompt = build_qa_prompt(code, args.check)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(
        f"Requesting QA check '{args.check}' from OpenAI "
        f"(model={args.model or 'default'}) ..."
    )

    try:
        report = call_openai(prompt, model=args.model)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(report)

    out_path = os.path.join("reviews", f"slice-{args.slice}", f"qa-{args.check}.md")
    _write(out_path, report)
    print(f"\nReport written to: {out_path}")

    verdict = "PASS" if "VERDICT: PASS" in report else "FAIL"
    print(f"\n--- VERDICT: {verdict} ---")
    return 0 if verdict == "PASS" else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="openai_qa.py",
        description=(
            "QA subcommand for the OpenAI coder helper. "
            "Runs one of seven check types against a code file."
        ),
    )
    parser.add_argument(
        "--model", default=None,
        help="Override OPENAI_CODE_MODEL env var. Defaults to gpt-5.5.",
    )
    parser.add_argument(
        "--code", required=True,
        help="Path to the code file to QA.",
    )
    parser.add_argument(
        "--check", required=True,
        choices=list(check_types()),
        metavar="TYPE",
        help=(
            "QA check type. One of: "
            + ", ".join(check_types())
        ),
    )
    parser.add_argument(
        "--slice", required=True, type=int, metavar="N",
        help="Slice number. Report is written to reviews/slice-N/qa-<type>.md.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return cmd_qa(args)


if __name__ == "__main__":
    sys.exit(main())
