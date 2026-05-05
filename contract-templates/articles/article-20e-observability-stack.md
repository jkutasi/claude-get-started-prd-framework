# Article 20e: Observability Stack

> Part of [Article 20: Code Architecture Standards](article-20-code-architecture.md). Load only when you need this specific subsection.

All projects MUST have **structured logging** AND **distributed-trace-grade error tracking**. Sentry is the named, opinionated platform — do NOT generalize.

This article is split into two parts:

- **[Article 20e-1: Logging & Error Capture](article-20e-1-logging-and-errors.md)** — structured logger, no-raw-console rule, captureException with slice tag, beforeSend redaction
- **[Article 20e-2: Distributed Tracing](article-20e-2-distributed-tracing.md)** — three-layer Sentry init, tracePropagationTargets, withScope/setTag/setContext/setUser, Sentry.startSpan around DB + outbound HTTP, same release across layers

## Why both parts are required

Error capture alone (Sentry on exceptions) tells you **what** broke. Distributed tracing tells you **the entire chain that led to it** — which user clicked which button, which API route handled it, which DB query failed, all stitched into one trace_id. Without tracing you spend hours correlating client-side timestamps with server-side stack traces. With tracing it's one Sentry issue page.

## Slice 0 bootstrap

The shared logger at `src/shared/logging/logger.{EXT}`, the AppError class, and the three Sentry projects (client / server / DB) are all created during Slice 0 — before any feature code is written. Slice 0 is incomplete until:

1. `setup_logging()` (or equivalent) runs first thing at app entrypoint.
2. `init_sentry()` runs second, after env vars load.
3. All three Sentry DSNs are configured: `SENTRY_DSN_CLIENT`, `SENTRY_DSN_SERVER`, `SENTRY_DSN_DB`.
4. The `beforeSend` redaction hook is wired (see 20e-1).
5. `tracePropagationTargets` covers every internal API origin (see 20e-2).

See `contracts/ARCHITECTURE_STANDARDS.md` §5 for language-equivalent recommendations (Pino/structlog/zap, etc.).
