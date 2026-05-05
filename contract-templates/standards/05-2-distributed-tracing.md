# §5.2 Distributed Tracing

> Part of [§5 Observability Stack](05-observability-stack.md). Aligned with [Article 20e-2](../articles/article-20e-2-distributed-tracing.md).

Sentry MUST be initialized at three layers (client, server, database) so traces stitch end-to-end. Error capture alone is not sufficient.

## Three-Layer Sentry Init

| Layer | SDK | Required integrations |
|---|---|---|
| Client | `@sentry/react` (or `@sentry/nextjs`) | `browserTracingIntegration`, `replayIntegration` (optional) |
| Server | `@sentry/node` (or framework-specific) | `httpIntegration`, framework integration |
| Database | `@sentry/node` + DB integration | `postgresIntegration`, `prismaIntegration`, etc. |

Three **separate Sentry projects** (e.g., `{project}-frontend`, `{project}-api`, `{project}-db`) are RECOMMENDED. Each gets its own DSN. Traces still stitch via shared `trace_id`, but alerting volume and ownership stay clean per layer.

## `tracePropagationTargets` — Required (Client)

The client MUST configure `tracePropagationTargets` so the browser attaches `sentry-trace` and `baggage` HTTP headers to outbound `fetch` / `XHR` requests. Without this, the server has no way to know that an API call belongs to the user's click trace.

```js
Sentry.init({
  dsn: SENTRY_DSN_CLIENT,
  integrations: [Sentry.browserTracingIntegration()],
  tracePropagationTargets: [
    "localhost",
    /^https:\/\/api\.yourdomain\.com/,
    // every internal API origin MUST be listed
  ],
  release: process.env.APP_VERSION,
});
```

## `withScope` Enrichment at Every Request Boundary

Every server-side request boundary MUST enrich the Sentry scope **before any code that can throw runs**:

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

Required tags: `route`, `layer`, `slice`. Required contexts: `request` (body MUST be redacted before attaching). Required user: `setUser({ id })` from auth middleware.

## `Sentry.startSpan()` Around DB and Outbound HTTP

For DB drivers and HTTP clients with auto-integrations (postgres, prisma, http), the integration auto-wraps queries in spans — no manual code needed. For custom query builders, raw DB calls, BigQuery, or any non-instrumented client, wrap manually:

```js
return Sentry.startSpan(
  { op: 'db.query', name: 'getCampaignById' },
  async (span) => {
    span.setAttribute('db.campaign_id', id);
    return await db.query('SELECT * FROM campaigns WHERE id = $1', [id]);
  }
);
```

Outbound HTTP to third-party APIs MUST be wrapped in `Sentry.startSpan({ op: 'http.client', name: '<api>.<operation>' }, ...)`.

## `setUser` Everywhere

Call `Sentry.setUser({ id, email })` on the client immediately after login, and again on the server from auth middleware on every request.

## Same Release Across All Three Layers

Tag every layer with the **same release version string** (git SHA or semver). CI MUST inject `APP_VERSION` (or equivalent) into the build of every layer so they match. When an error fires, you know exactly which build of client + server + DB was running together.
