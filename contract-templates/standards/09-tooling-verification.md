# §9 Tooling Verification Checklist (Enforced by gate_check.py)

> Part of [Architecture Standards](../ARCHITECTURE-STANDARDS-TEMPLATE.md).

The following checks are **mechanically enforced** — not advisory. The gate check script validates each item. If any check fails, the slice CANNOT proceed.

## Slice 0 Tooling Gate (blocks Slice 1)

| Check | What gate_check.py Verifies | Why |
|-------|----------------------------|-----|
| **Structured logger exists** | File exists at `src/shared/logging/logger.{EXT}` (or project-configured path) | Without a logger, all observability is advisory |
| **No raw console output** | `grep -r "console\.\(log\|error\|warn\)" src/` and `grep -r "print(" src/` return zero matches (excluding test files) | Raw output bypasses structured logging and Sentry integration |
| **Sentry DSNs configured** | `.env` or environment config contains `SENTRY_DSN_CLIENT`, `SENTRY_DSN_SERVER`, `SENTRY_DSN_DB` (or single `SENTRY_DSN` if using one project) with non-empty values | Error tracking without a DSN is silently disabled |
| **`beforeSend` hook wired** | `sentry_init` (or equivalent) registers a `beforeSend` hook that calls the redaction utility | Last line of defense against token leaks |
| **`tracePropagationTargets` set** | Client Sentry init lists every internal API origin in `tracePropagationTargets` | Without it, client → server traces don't stitch |
| **Linter config exists** | `pyproject.toml` contains `[tool.ruff]` (Python) OR `.eslintrc*` / `eslint.config.*` exists (JS/TS) | Without config, linting gates are theater |
| **Pre-push hook exists** | `.husky/pre-push` file exists and is executable (or equivalent Git hook) | Without the hook, linting depends on agents remembering — they won't |

## Every Slice Tooling Gate (blocks next slice)

| Check | What gate_check.py Verifies |
|-------|----------------------------|
| **No raw console output** | Same grep check as Slice 0 — enforced on every slice, not just the first |
| **150-line file limit** | All production source files under 150 lines (already enforced) |
| **No cross-slice imports** | Static check: `features/A/` MUST NOT import from `features/B/`. Violations block merge |
| **Single-slice PR (default)** | CI flags any PR touching more than one slice folder for elevated review |

## Enforcement Principle

> **If it's in the architecture standard, there must be an automated check that blocks progress if it's missing. Documentation alone does not work.**
