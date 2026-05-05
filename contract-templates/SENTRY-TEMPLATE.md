# Sentry Contract -- {PROJECT_NAME}

> **Purpose:** One-page operational reference for Sentry SDK on this project. Derived from [Article 20e: Observability Stack](articles/article-20e-observability-stack.md) and its sub-articles. If anything here conflicts with Article 20e, Article 20e wins.
>
> For CLI usage (releases, sourcemap upload), see [SENTRY-CLI-TEMPLATE.md](SENTRY-CLI-TEMPLATE.md).

Sentry is the named, opinionated platform. Do NOT generalize to "an error tracker." Three separate Sentry projects, three DSNs, one shared release string, slice tag on every event.

---

## Three-Layer Init (required)

Each layer initializes its own Sentry SDK against its own DSN. Traces stitch end-to-end via shared `trace_id`; alerts stay clean per layer.

| Layer | SDK | Required integrations | DSN env var |
|-------|-----|----------------------|-------------|
| Client | `@sentry/react` (or `@sentry/nextjs`) | `browserTracingIntegration`, `replayIntegration` (optional) | `SENTRY_DSN_CLIENT` |
| Server | `@sentry/node` (or framework-specific) | `httpIntegration`, framework integration | `SENTRY_DSN_SERVER` |
| Database | `@sentry/node` + DB integration | `postgresIntegration` / `prismaIntegration` / `mongoIntegration` | `SENTRY_DSN_DB` |

Mixing DSNs across layers is a CONTRACT VIOLATION. The client DSN MUST NOT appear in server or DB init, and vice versa.

---

## Required Behaviors

| # | Requirement | Where it lives |
|---|-------------|----------------|
| 1 | `tracePropagationTargets` configured on client to cover every internal API origin | client `Sentry.init` |
| 2 | `Sentry.withScope` enrichment at every request boundary BEFORE any throwable code runs | route / RPC / worker entrypoints |
| 3 | `scope.setTag('route', ...)`, `setTag('layer', ...)`, `setTag('slice', ...)` on every boundary | inside `withScope` |
| 4 | `scope.setContext('request', { body: redactRawBody(...) })` -- body MUST be redacted before attaching | inside `withScope` |
| 5 | `scope.setUser({ id, email })` on client after login AND on server from auth middleware on every request | both layers |
| 6 | `Sentry.startSpan({ op: 'db.query', ... })` around uninstrumented DB calls | repository layer |
| 7 | `Sentry.startSpan({ op: 'http.client', name: '<api>.<op>' })` around outbound third-party HTTP | service layer |
| 8 | `beforeSend` / `before_send` hook registered with the redaction regex set below | every layer's `Sentry.init` |
| 9 | Slice tag on every `Sentry.captureException` (use a `withSliceContext` helper so it cannot be forgotten) | all layers |
| 10 | Same `release` string injected into all three layers (git SHA from CI) | all three `Sentry.init` calls |

---

## Forbidden

- Calling `Sentry.captureException` without a `slice` tag set in scope.
- Logging URLs or request bodies into Sentry without running them through `redact_url` / `redact_raw_body` first.
- Using one layer's DSN inside another layer's init (e.g., client DSN on server).
- Passing raw secrets via `extra={...}` -- redaction only runs on event fields covered by `beforeSend`.
- Disabling `beforeSend` "temporarily" for debugging. Redaction is non-negotiable.

---

## `beforeSend` Redaction Regex Set (case-insensitive, required)

| Pattern | Replacement |
|---------|-------------|
| `access_token=[^&"'\s]*` | `access_token=[REDACTED]` |
| `appsecret_proof=[^&"'\s]*` | `appsecret_proof=[REDACTED]` |
| `client_secret=[^&"'\s]*` | `client_secret=[REDACTED]` |
| `app_secret=[^&"'\s]*` | `app_secret=[REDACTED]` |
| `Bearer\s+[^\s"']+` | `Bearer [REDACTED]` |

Use `*` (not `+`) so empty-value variants still redact. Redaction MUST cover: `event.message`, every `event.exception.values[].value`, every `event.breadcrumbs.values[].message`, `event.request.data`, and `event.request.url`.

---

## Boundary Enrichment Pattern (server)

```js
return Sentry.withScope(async (scope) => {
  scope.setTag('route', '/api/{slice}/{action}');
  scope.setTag('layer', 'api');
  scope.setTag('slice', '{slice-name}');
  scope.setContext('request', {
    body: redactRawBody(JSON.stringify(await req.json())),
    headers: { 'user-agent': req.headers.get('user-agent') },
  });
  scope.setUser({ id: req.user.id });
  return await handle(req);
});
```

---

## Project-Specific Values (fill in)

| Placeholder | This project's value |
|-------------|---------------------|
| `{PROJECT_DSN_FRONTEND}` | _e.g., `https://abc123@o0.ingest.sentry.io/{frontend-project-id}`_ |
| `{PROJECT_DSN_API}` | _e.g., `https://def456@o0.ingest.sentry.io/{api-project-id}`_ |
| `{PROJECT_DSN_DB}` | _e.g., `https://ghi789@o0.ingest.sentry.io/{db-project-id}`_ |
| `{RELEASE_FORMAT}` | _e.g., `${GIT_SHA}` or `{project}@${SEMVER}+${GIT_SHA}`_ |
| `{SLICE_TAG_VALUES}` | _enumerated list, e.g., `slice-0-bootstrap`, `slice-1-auth`, `slice-2-ingest`_ |

DSNs live in the secret manager (see [SECURITY.md](SECURITY.md)). Never hardcode DSNs in source.

---

## Enforcement

- `gate_check.py` verifies all three DSNs are configured, `beforeSend` is wired, and `tracePropagationTargets` is non-empty before Slice 1 begins.
- QA Backend agent flags any `captureException` missing a `slice` tag as P0.
- Two CI guardrail tests (cost <100 ms): one verifies the structured logger preserves `extra={...}` fields; one verifies the redaction regex set strips every secret pattern case-insensitively.
- Post-push runtime verification: check Sentry for new errors before starting new work (Nuclear Rule 7).

See [Article 20e-1](articles/article-20e-1-logging-and-errors.md) for logging + redaction details and [Article 20e-2](articles/article-20e-2-distributed-tracing.md) for tracing details.
