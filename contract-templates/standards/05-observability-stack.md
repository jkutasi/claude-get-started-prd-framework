# §5 Observability Stack

> Part of [Architecture Standards](../ARCHITECTURE-STANDARDS-TEMPLATE.md). Aligned with [Article 20e](../articles/article-20e-observability-stack.md).

All projects MUST have **structured logging** AND **distributed-trace-grade error tracking via Sentry**. No exceptions. Sentry is the named platform — do not generalize.

This section is split into two sub-files:

- **[§5.1 Logging & Error Capture](05-1-logging-and-errors.md)** — structured logger, no-raw-console rule, captureException with slice tag, beforeSend redaction with required regex
- **[§5.2 Distributed Tracing](05-2-distributed-tracing.md)** — three-layer Sentry init, tracePropagationTargets, withScope, startSpan, setUser, same release across layers

## Required Tools

| Placeholder | Purpose | Required |
|-------------|---------|----------|
| `{ERROR_TRACKING_SERVICE}` | Error tracking + performance monitoring (Sentry) | YES |
| `{STRUCTURED_LOGGER}` | Structured JSON logging | YES |
| `{LOGGER_TRANSPORT}` | Bridge between logger and error tracker | YES |
| `{ERROR_TRACKING_MCP}` | MCP server for Claude Code integration | RECOMMENDED |

## Language Equivalents

| Language | Error Tracker | Structured Logger | Bridge |
|----------|--------------|-------------------|--------|
| Node.js / TypeScript | Sentry | Pino | pino-sentry-transport |
| Python | Sentry | structlog | sentry-sdk |
| Go | Sentry | zerolog / zap | sentry-go |
| Browser / SPA | Sentry Browser SDK | Custom `logger.ts` wrapping console | @sentry/browser |
| {PRIMARY_LANGUAGE} | {ERROR_TRACKING_SERVICE} | {STRUCTURED_LOGGER} | {LOGGER_TRANSPORT} |

## Slice 0 Bootstrap

The shared logger at `src/shared/logging/logger.{EXT}`, the AppError class, and **all three Sentry projects** (client / server / DB) are created during Slice 0. Slice 0 is incomplete until structured logging, the `beforeSend` redaction hook, `tracePropagationTargets`, and distributed-tracing init are all wired.

> **See also:** [Article 28](../articles/article-28-service-log-inventory.md) for the operational service log inventory template.
