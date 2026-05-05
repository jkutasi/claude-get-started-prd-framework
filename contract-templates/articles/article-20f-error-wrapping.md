# Article 20f: Error Wrapping & Context Chaining

> Part of [Article 20: Code Architecture Standards](article-20-code-architecture.md). Load only when you need this specific subsection.

All errors MUST be wrapped with context using the project's AppError class before being passed up the call stack.

## Per-Layer Context

Each layer adds its own context as the error propagates upward:

| Layer | Context to Add |
|-------|---------------|
| **Route** | HTTP method, endpoint path, request parameters |
| **Service** | Business operation name, input summary |
| **Repository** | Database query, table name, operation type |

## HTTP Boundary Rule

At the HTTP boundary, cause chains are **NEVER** exposed to clients. The route layer:

1. Logs the full error chain (including all causes) via the structured logger.
2. Reports the error to Sentry (with slice + layer tags — see [20e-1](article-20e-1-logging-and-errors.md)).
3. Returns a generic error response to the client.

## Created in Slice 0

The AppError class is created during Slice 0 at `src/shared/errors/app-error.{EXT}`. All feature code imports and uses this class.

## Enforcement

- QA Code Quality agent flags bare `throw new Error()` or `raise Exception()` without wrapping (P1 finding).
- Peer reviewers verify each layer adds appropriate context.

See `contracts/ARCHITECTURE_STANDARDS.md` §6 for the full AppError specification and language idioms.
