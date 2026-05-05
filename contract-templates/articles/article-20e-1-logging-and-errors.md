# Article 20e-1: Logging & Error Capture

> Part of [Article 20e: Observability Stack](article-20e-observability-stack.md). Load only when you need logging/error-capture rules.

## Structured logging — required

- **No raw console output** in committed code. No `console.log`, `print()`, `fmt.Println()`, or equivalent. Every log line goes through the project's structured logger.
- **JSON on stdout.** Every log entry is a single JSON object on stdout with at minimum `timestamp`, `level`, `message`, `module`. Modern log viewers parse this; teammates can grep it.
- **Pass-through `extra={...}`.** The structured formatter MUST preserve every field passed via `extra={...}` (or equivalent). No whitelist. Add fields freely.
- **Idempotent setup.** `setup_logging()` MUST guard against re-entry (`if root.handlers: return`) — critical on serverless cold starts.

## Sentry exception capture — required

Every uncaught exception MUST land in Sentry. Every `Sentry.captureException` call MUST carry a slice tag:

```js
Sentry.withScope((scope) => {
  scope.setTag('slice', '{slice-name}');
  scope.setTag('layer', 'client' | 'api' | 'database');
  Sentry.captureException(err);
});
```

Wrap entry points (route handlers, React error boundaries, repository methods) in a per-slice helper so the slice tag is automatic and can never be forgotten:

```ts
// features/{slice}/sentry.ts
export function withSliceContext<T>(fn: () => Promise<T>): Promise<T> {
  return Sentry.withScope(async (scope) => {
    scope.setTag('slice', '{slice-name}');
    scope.setTag('slice_version', slice.version);
    scope.setContext('feature_flag', { name: slice.featureFlag });
    return fn();
  });
}
```

## `beforeSend` redaction hook — required

Every Sentry init MUST register a `beforeSend` hook that runs URL + body redaction on every outgoing event. Tokens MUST be stripped before the event leaves the process. The required regex set (all case-insensitive):

| Pattern | Replacement |
|---|---|
| `access_token=[^&"'\s]*` | `access_token=[REDACTED]` |
| `appsecret_proof=[^&"'\s]*` | `appsecret_proof=[REDACTED]` |
| `client_secret=[^&"'\s]*` | `client_secret=[REDACTED]` |
| `app_secret=[^&"'\s]*` | `app_secret=[REDACTED]` |
| `Bearer\s+[^\s"']+` | `Bearer [REDACTED]` |

Use `*` (not `+`) so empty-value variants (`access_token=`) still redact. The redaction MUST cover: `event.message`, every `event.exception.values[].value`, every `event.breadcrumbs.values[].message`, and every `event.request.data` body. URLs in `event.request.url` MUST pass through `redact_url()` to strip sensitive query parameters.

Two guardrail tests live in CI forever (cost <100 ms): one verifies the structured logger preserves `extra={...}` fields with no whitelist; one verifies `redact_url` and `redact_raw_body` strip every secret pattern case-insensitively. Both run on every PR.

## Enforcement

- Husky pre-push hook blocks commits containing `console.log` / `print()` (Article 23).
- `gate_check.py` verifies the logger file exists, the Sentry DSNs are configured, and the `beforeSend` hook is wired before Slice 1 can begin.
- QA Backend agent verifies every `captureException` carries a slice tag (P0 finding if missing).

## Sentry issue resolution discipline

Never mark a Sentry issue RESOLVED based on event silence alone. An issue may stop firing simply because the affected surface has not been visited — not because the bug is gone. Resolve only when all three gates are met: (a) root cause is identified, (b) a fix is in production, and (c) a smoke test that directly exercises the failing surface is green.

Why this matters:
- Dashboards and admin pages may go days without a visit, producing artificial silence that mimics a fix.
- Sentry's auto-resolve heuristics produce false negatives on low-traffic surfaces — the event counter resets but the bug persists.
- Premature resolves skew on-call metrics and suppress alerts on the next occurrence, delaying detection.
