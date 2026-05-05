# Article 20e-2: Distributed Tracing

> Part of [Article 20e: Observability Stack](article-20e-observability-stack.md). Load only when you need distributed-tracing rules.

Sentry must be initialized at three layers (client, server, database) so traces stitch end-to-end. Error capture alone is not sufficient.

## Three-layer Sentry init — required

| Layer | SDK | Required integrations |
|---|---|---|
| Client | `@sentry/react` (or `@sentry/nextjs`) | `browserTracingIntegration`, `replayIntegration` (optional) |
| Server | `@sentry/node` (or framework-specific) | `httpIntegration`, framework integration |
| Database | `@sentry/node` + DB integration | `postgresIntegration`, `prismaIntegration`, `mongoIntegration` (whichever applies) |

Three **separate Sentry projects** (one per layer, e.g., `{project}-frontend`, `{project}-api`, `{project}-db`) are RECOMMENDED. Each gets its own DSN. Traces still stitch via shared `trace_id`, but alerting volume and ownership stay clean per layer.

## `tracePropagationTargets` on the client — required

The client MUST configure `tracePropagationTargets` so the browser attaches `sentry-trace` and `baggage` HTTP headers to outbound `fetch` / `XHR` requests. Without this, the server has no way to know that an API call belongs to the user's click trace.

```js
Sentry.init({
  dsn: SENTRY_DSN_CLIENT,
  integrations: [Sentry.browserTracingIntegration()],
  tracePropagationTargets: [
    "localhost",
    /^https:\/\/api\.yourdomain\.com/,
    // every internal API origin MUST be listed here
  ],
  release: process.env.APP_VERSION,
});
```

## `withScope` enrichment at every request boundary — required

Every server-side request boundary (route handler, RPC handler, queue worker entry) MUST enrich the Sentry scope **before any code that can throw runs**:

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

Required tags: `route`, `layer`, `slice`. Required contexts: `request` (body MUST be redacted via `redact_raw_body` before attaching). Required user: `setUser({ id })` from auth middleware.

## `Sentry.startSpan()` around DB queries and outbound HTTP — required

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

Outbound HTTP to third-party APIs (Meta, RedTrack, etc.) MUST be wrapped in `Sentry.startSpan({ op: 'http.client', name: '<api>.<operation>' }, ...)` so the third-party call shows up in the trace alongside DB and route spans.

## `setUser` everywhere — required

Call `Sentry.setUser({ id, email })` on the client immediately after login, and again on the server from auth middleware on every request. Errors become triageable because the affected user is identified in one click.

## Same release across all three layers — required

Tag every layer with the **same release version string** (git SHA or semver). When an error fires, you know exactly which build of client + server + DB was running together:

```js
release: process.env.APP_VERSION  // SAME value injected into all three init calls
```

CI must inject `APP_VERSION` into the build of every layer so they match.
