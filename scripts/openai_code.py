"""openai_code.py — CLI entrypoint for the OpenAI Responses API coder helper.

Subcommands:
  draft   Generate code from a spec and write it to --output.
  review  Ask OpenAI to self-review the code; prints APPROVE or REVISE + issues.
  fix     Given a code file and failure log, ask OpenAI to fix; writes back to code path.
  qa      Focused QA check on a code file — delegates to openai_qa.py.

Environment variables:
  OPENAI_API_KEY      Required. Your OpenAI secret key.
  OPENAI_CODE_MODEL   Optional. Defaults to gpt-5.5.
"""
import argparse
import os
import sys

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from openai_code_lib import call_openai, build_draft_prompt  # noqa: E402
from openai_code_lib import build_review_prompt, build_fix_prompt  # noqa: E402
from openai_qa_lib import check_types  # noqa: E402
import openai_qa  # noqa: E402  — qa dispatcher lives here


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


def cmd_draft(args: argparse.Namespace) -> int:
    spec = _read(args.spec)
    conventions = _read(args.conventions)
    files = [f.strip() for f in args.files.split(",") if f.strip()] if args.files else []
    print(f"Requesting draft from OpenAI (model={args.model or 'default'}) ...")
    prompt = build_draft_prompt(spec, files, conventions)
    try:
        code = call_openai(prompt, model=args.model)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    _write(args.output, code)
    print(f"Draft written to: {args.output}")
    return 0


def cmd_review(args: argparse.Namespace) -> int:
    code = _read(args.code)
    spec = _read(args.spec)
    print("Requesting self-review from OpenAI ...")
    prompt = build_review_prompt(code, spec)
    try:
        review = call_openai(prompt, model=args.model)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(review)
    verdict = "APPROVE" if "VERDICT: APPROVE" in review else "REVISE"
    print(f"\n--- VERDICT: {verdict} ---")
    return 0 if verdict == "APPROVE" else 2


def cmd_fix(args: argparse.Namespace) -> int:
    code = _read(args.code)
    failures = _read(args.failures)
    print(f"Requesting fix from OpenAI for: {args.code} ...")
    prompt = build_fix_prompt(code, failures)
    try:
        fixed = call_openai(prompt, model=args.model)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    _write(args.code, fixed)
    print(f"Fixed code written back to: {args.code}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="openai_code.py",
        description="OpenAI Responses API coder helper — draft, review, fix, qa.",
    )
    parser.add_argument("--model", default=None,
                        help="Override OPENAI_CODE_MODEL env var. Defaults to gpt-5.5.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_draft = sub.add_parser("draft", help="Generate code from a spec.")
    p_draft.add_argument("--spec", required=True)
    p_draft.add_argument("--files", default="")
    p_draft.add_argument("--conventions", required=True)
    p_draft.add_argument("--output", required=True)

    p_review = sub.add_parser("review", help="Self-review generated code.")
    p_review.add_argument("--code", required=True)
    p_review.add_argument("--spec", required=True)

    p_fix = sub.add_parser("fix", help="Fix code given a failure log.")
    p_fix.add_argument("--code", required=True)
    p_fix.add_argument("--failures", required=True)

    p_qa = sub.add_parser("qa", help="Run a focused QA check (see openai_qa.py).")
    p_qa.add_argument("--code", required=True, help="Code file to QA.")
    p_qa.add_argument(
        "--check", required=True, choices=list(check_types()), metavar="TYPE",
        help="One of: " + ", ".join(check_types()),
    )
    p_qa.add_argument("--slice", required=True, type=int, metavar="N",
                      help="Slice number; report -> reviews/slice-N/qa-<type>.md.")

    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "draft":
        return cmd_draft(args)
    if args.command == "review":
        return cmd_review(args)
    if args.command == "fix":
        return cmd_fix(args)
    if args.command == "qa":
        return openai_qa.cmd_qa(args)
    build_parser().print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
