# §5.1 Logging & Error Capture

> Part of [§5 Observability Stack](05-observability-stack.md). Aligned with [Article 20e-1](../articles/article-20e-1-logging-and-errors.md).

## Structured Logging Rules

- **No raw console output.** No `console.log`, `print()`, `fmt.Println()`, or equivalent in committed code. All logging goes through the structured logger.
- **JSON on stdout.** Every log entry is a single JSON object with at minimum `timestamp`, `level`, `message`, `module`. Modern log viewers parse this; teammates can grep it.
- **Pass-through `extra={...}`.** The structured formatter MUST preserve every field passed via `extra={...}`. No whitelist.
- **Idempotent setup.** `setup_logging()` MUST guard against re-entry (`if root.handlers: return`) — critical on serverless cold starts.
- **Created in Slice 0.** The shared logger at `src/shared/logging/logger.{EXT}` is created during Slice 0 bootstrap, before any feature code is written.

## Sentry Error Capture Rules

Every uncaught exception MUST land in Sentry. Every `captureException` call MUST carry a slice tag:

```js
Sentry.withScope((scope) => {
  scope.setTag('slice', '{slice-name}');
  scope.setTag('layer', 'client' | 'api' | 'database');
  Sentry.captureException(err);
});
```

A per-slice `withSliceContext()` helper at `features/{slice}/sentry.ts` makes the slice tag automatic; wrap every entry point (route handler, React error boundary, repository method) in it.

## `beforeSend` Redaction Hook — Required

Every Sentry init MUST register a `beforeSend` hook that runs URL + body redaction on every outgoing event. Required regex set (all case-insensitive):

| Pattern | Replacement |
|---|---|
| `access_token=[^&"'\s]*` | `access_token=[REDACTED]` |
| `appsecret_proof=[^&"'\s]*` | `appsecret_proof=[REDACTED]` |
| `client_secret=[^&"'\s]*` | `client_secret=[REDACTED]` |
| `app_secret=[^&"'\s]*` | `app_secret=[REDACTED]` |
| `Bearer\s+[^\s"']+` | `Bearer [REDACTED]` |

Use `*` (not `+`) so empty-value variants (`access_token=`) still redact. Coverage MUST include: `event.message`, every `event.exception.values[].value`, every `event.breadcrumbs.values[].message`, and `event.request.data`. URLs in `event.request.url` MUST pass through `redact_url()` to strip sensitive query parameters.

## Two Guardrail Tests

Two tests live in CI forever (cost <100 ms):

1. Structured logger preserves every `extra={...}` field — no whitelist.
2. `redact_url` and `redact_raw_body` strip every secret pattern case-insensitively.

## Enforcement

- Husky pre-push hook blocks commits containing `console.log` / `print()` (Article 23).
- `gate_check.py` verifies the logger file exists, all three Sentry DSNs are configured, and the `beforeSend` hook is wired before Slice 1.
- QA Backend agent verifies every `captureException` carries a slice tag (P0 finding if missing).
