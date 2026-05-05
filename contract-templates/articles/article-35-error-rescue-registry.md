# Article 35: Error & Rescue Registry

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.
>
> **Enforces:** Nuclear Rule 7 (Never Commit Without Checking Runtime Errors)
>
> **Cross-references:** Article 28 (Service Log Inventory), Article 34 (Error Diagnosis Protocol)

## The Rule

Every slice that adds or modifies code paths that can fail MUST produce an Error & Rescue Registry table during Phase D (Self-Reflection). The registry maps every failure point to its exception, handler, test coverage, and user-visible impact. Any row where RESCUED=No AND TEST=No AND USER SEES=Silent is a CRITICAL GAP that blocks Phase E.

## Registry Table Format

Each coder produces this table for their module during Phase D:

| Method / Endpoint | Failure Mode | Exception / Error | Rescued? | Rescue Action | Test Covers? | User Sees |
|---|---|---|---|---|---|---|
| `POST /api/upload` | File too large | `PayloadTooLargeError` | Yes | Return 413 + message | Yes | "File exceeds 10MB limit" |
| `fetchScores()` | API timeout | `TimeoutError` | Yes | Retry 2x, then fallback | Yes | Loading spinner + retry button |
| `db.query(...)` | Connection lost | `ConnectionError` | No | — | No | Silent |

The last row is a CRITICAL GAP — no rescue, no test, user sees nothing. This must be fixed before proceeding.

## Critical Gap Detection

A row is a CRITICAL GAP when ALL three conditions are true:
- **RESCUED = No** — no error handler catches this failure
- **TEST = No** — no test verifies behavior under this failure
- **USER SEES = Silent** — the user gets no feedback when this fails

Any CRITICAL GAP found in Phase D blocks progression to Phase E (Peer Review) until resolved.

## Warning Gaps

A row is a WARNING GAP when any TWO of the three conditions are true (e.g., no rescue + no test, but user sees an error page). Warning gaps do not block Phase E but MUST be logged in the registry and targeted by QA agents in Phase F for failure-path testing.

## When to Produce the Registry

- **Phase D (Self-Reflection):** Each coder produces the registry for their module
- **Phase E (Peer Review):** Reviewers verify the registry is complete and accurate
- **Phase F (QA):** QA agents use the registry to target failure-path testing

## Registry Scope

Only include failure points that are NEW, MODIFIED, or MOVED in the current slice. Code relocated between modules counts as modified because its error-handling context may have changed. Do not audit the entire codebase — focus on what changed.

In refactoring slices, any failure point that enters your module's responsibility (via extraction, migration, or restructuring) must be included, even if the code itself was not modified. You are inheriting its failure behavior.

**SECURITY:** When moving code between modules, explicitly verify that error handlers from the source location have been replicated or replaced in the destination. Lost error handlers are the most common source of information leakage in refactored code.

## Security — Public Repositories

If the project repository is public, the registry file MUST be added to `.gitignore` or stored in a private review channel. Never commit unresolved CRITICAL GAPs to a public repository — they are vulnerability disclosures that map unhandled failure points for attackers.

## Why This Matters

Silent failures are the most dangerous bugs. They don't crash, they don't log, and users don't report them — data just quietly goes wrong. The registry forces every failure point to be explicitly documented and classified, making silent failures visible before they reach production.

## See also

For a catalog of recurring anti-patterns drawn from production incidents that should be checked against during Phase D, see [Article 36](article-36-anti-patterns-from-production.md).
