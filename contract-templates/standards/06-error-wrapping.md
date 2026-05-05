# §6 Error Wrapping & Context Chaining

> Part of [Architecture Standards](../ARCHITECTURE-STANDARDS-TEMPLATE.md). Aligned with [Article 20f](../articles/article-20f-error-wrapping.md).

Every major function wraps errors with context before passing them up the call stack.

## AppError Class

```
class AppError:
  message: string         # Human-readable description of what went wrong
  code: string            # Machine-readable error code (e.g., "BRIEF_NOT_FOUND")
  statusCode: number      # HTTP status code (set ONLY in the route layer)
  cause: Error | null     # Original error that triggered this
  context: object         # Additional debugging context
```

## Language Idioms

| Language | How to Wrap |
|----------|------------|
| Python | `raise AppError("message") from original_error` |
| JavaScript / TypeScript | `throw new AppError("message", { cause: originalError })` |
| Go | `fmt.Errorf("message: %w", originalError)` |

## Per-Layer Context

| Layer | Context to Add |
|-------|---------------|
| **Route** | HTTP method, endpoint path, request parameters |
| **Service** | Business operation name, input summary |
| **Repository** | Database query, table name, operation type |

## HTTP Boundary Rule

At the HTTP boundary (route layer), cause chains are **NEVER** exposed to clients. The route layer:

1. Logs the full error chain (including all causes) via the structured logger.
2. Reports the error to `{ERROR_TRACKING_SERVICE}` (with slice + layer tags — see [§5.1](05-1-logging-and-errors.md)).
3. Returns a generic error response to the client (e.g., `{ "error": "Internal server error" }`).

## Created in Slice 0

The AppError class at `src/shared/errors/app-error.{EXT}` is created during Slice 0 bootstrap. All feature code imports and uses this class.

## Enforcement

- QA Code Quality agent checks for bare `throw new Error()` or `raise Exception()` without wrapping (P1 finding).
- Peer reviewers verify that each layer adds appropriate context.
