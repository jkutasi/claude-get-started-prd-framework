"""openai_qa_lib.py — QA prompt builders for the OpenAI Responses API coder helper.

Each check type produces a focused prompt for OpenAI 5.5.
Import build_qa_prompt for use in openai_qa.py.
"""

_CHECK_TYPES = (
    "api-contract",
    "backend",
    "routing",
    "data-integrity",
    "code-quality",
    "security",
    "uiux",
)

_FOCUS = {
    "api-contract": (
        "Verify the HTTP layer: response body shapes, HTTP status codes (2xx/4xx/5xx "
        "semantics), Content-Type headers, authentication/authorisation headers, and "
        "proper error envelope structure. Flag any mismatch between the declared contract "
        "and the implementation."
    ),
    "backend": (
        "Verify server-side logic: business rule correctness, transaction safety "
        "(atomicity, rollback on error), proper error propagation with context, absence "
        "of silent swallowed exceptions, and correct handling of edge-case inputs "
        "(None/null, empty collections, boundary values)."
    ),
    "routing": (
        "Verify routing correctness: Next.js App Router conventions, dynamic segment "
        "params, redirect rules, middleware ordering, and correct handling of 404/redirect "
        "cases. Flag any route that may conflict or shadow another."
    ),
    "data-integrity": (
        "Verify database queries: correct JOINs, NULL handling, transaction boundaries, "
        "deterministic ORDER BY (tiebreaker column present), index usage hints, and "
        "prevention of partial writes. If the code references Article 38, verify it is "
        "followed correctly."
    ),
    "code-quality": (
        "Verify code quality: the 150-line-per-file rule (flag any file section over "
        "150 lines), naming conventions, lint compliance (no unused imports, no shadowed "
        "names), absence of dead code, and type annotation completeness on all "
        "function signatures."
    ),
    "security": (
        "Verify security surfaces: XSS/CSRF/SQL-injection vectors, authentication and "
        "authorisation checks on every route, absence of secrets hardcoded in source, "
        "input validation before any DB or shell call, and safe output encoding. "
        "If the code references Article 36, verify it is followed correctly."
    ),
    "uiux": (
        "Verify UI/UX correctness: the four mandatory component states (loading, empty, "
        "error, populated), responsive breakpoints (mobile/tablet/desktop), ARIA roles "
        "and labels on interactive elements, keyboard navigation, colour-contrast "
        "compliance, and absence of layout shifts."
    ),
}


def check_types() -> tuple:
    """Return the tuple of valid check type strings."""
    return _CHECK_TYPES


def build_qa_prompt(code: str, check_type: str) -> str:
    """Return a QA prompt for OpenAI 5.5 focused on check_type.

    Args:
        code:       The source code to analyse.
        check_type: One of the seven _CHECK_TYPES values.

    Raises:
        ValueError: When check_type is not recognised.
    """
    if check_type not in _CHECK_TYPES:
        raise ValueError(
            f"Unknown check_type '{check_type}'. "
            f"Valid types: {', '.join(_CHECK_TYPES)}"
        )

    focus = _FOCUS[check_type]

    return "\n".join([
        "You are a QA engineer performing a structured code review.",
        f"Check type: {check_type}",
        "",
        "=== QA FOCUS ===",
        focus,
        "",
        "=== CODE UNDER REVIEW ===",
        code,
        "",
        "=== INSTRUCTIONS ===",
        "1. Apply the QA focus above. List every issue found, each on its own line.",
        "2. For each issue: state the file/line (if determinable), the rule violated,",
        "   and the recommended fix.",
        "3. If no issues are found, state: No issues found.",
        "4. End your response with exactly one of:",
        "VERDICT: PASS",
        "VERDICT: FAIL",
    ])
