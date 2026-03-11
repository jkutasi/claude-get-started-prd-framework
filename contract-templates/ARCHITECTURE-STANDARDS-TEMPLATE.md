# Architecture Standards — {PROJECT_NAME}

> **Purpose:** This document defines the mandatory code architecture standards for all production code. These standards are the PRIMARY quality mechanism — they prevent bugs at the structural level by ensuring every file is small, every concern is isolated, and every error is traceable. All agents, teammates, and sub-agents MUST follow these standards. QA agents verify compliance.
>
> **Article 20** in the contract articles provides the summary. This document provides the full details.

---

## §1 Feature-Based Folder Organization

All source code is organized by feature, not by type. Each feature is self-contained in its own folder.

### Directory Structure

```
src/
  {feature-name}/
    {feature-name}.route.{EXT}       # HTTP layer (~20-30 lines)
    {feature-name}.service.{EXT}     # Business logic (~80-150 lines)
    {feature-name}.repository.{EXT}  # Data access (~50-100 lines)
    {feature-name}.test.{EXT}        # Tests for service layer
    {feature-name}.types.{EXT}       # Shared types/interfaces (optional)
  shared/
    errors/
      app-error.{EXT}               # Custom error class (created in Slice 0)
    logging/
      logger.{EXT}                  # Structured logger setup (created in Slice 0)
    middleware/                      # Shared middleware (auth, validation, etc.)
tests/
  integration/                      # Cross-feature integration tests ONLY
```

### Rules

- **Tests alongside code.** Unit tests live in the feature folder next to the service file they test. The `tests/` directory is ONLY for cross-feature integration tests.
- **Self-contained features.** Everything about a feature lives in one folder. To understand a feature, look at one folder. To remove a feature, delete one folder.
- **Cross-feature imports are a code smell.** If your briefs service imports from your campaigns folder, that is a design issue. Flag it in review.
- **Shared utilities** go in `src/shared/` ONLY when they serve 3+ features. Do not prematurely extract utilities.

### Escape Hatches

- **CLI tools:** Replace route → service → repository with command handler → service → data access.
- **Frontend-only projects:** The display-only rule (§4) still applies. State management replaces the route layer.
- **Workers / background jobs:** Replace route with job handler. Service and repository layers remain the same.

---

## §2 Three-Layer Separation

Every feature separates concerns into three layers. Each layer has one job.

| Layer | Responsibility | Line Target | What It Does NOT Do |
|-------|---------------|-------------|---------------------|
| **Route** | HTTP handling | ~20-30 lines | No business logic. No database calls. |
| **Service** | Business logic | ~80-150 lines | No HTTP objects (`req`, `res`). No database queries. |
| **Repository** | Data access | ~50-100 lines | No business logic. No HTTP concerns. |

### Flow

```
Route → Service → Repository
```

- Never skip a layer. A route MUST NOT call a repository directly.
- Never let a layer do another layer's job. If a service is building SQL queries, that logic belongs in the repository.

### Spawn Model (Agent Teams)

By default, one coder sub-agent is spawned per layer file. A feature with route + service + repository = 3 spawns. For complex layers with multiple functions, additional spawns per function within a layer are appropriate — the existing "one focused job per spawn" rule takes precedence over the per-file default.

---

## §3 150-Line File Limit

**Every production source file MUST stay under 150 lines** (excluding comments and blank lines).

### Why

A file that is 500 lines doing multiple things forces any agent — human or AI — to understand too much context. A file that is 80 lines doing one thing is almost impossible to get wrong. This rule eliminates context window problems at the architectural level.

### Relationship to Function Limits

The 150-line file limit complements the existing 40-line function limit (QA Code Quality §4.7). A 150-line file holds at most 3-4 functions at maximum length. If a file exceeds this, it has too many concerns — split it.

### Test Files

Test files SHOULD stay under 150 lines. If tests grow beyond this, split into multiple test files per feature:
- `{feature-name}.test.{EXT}` — core tests
- `{feature-name}.edge-cases.test.{EXT}` — edge case tests

This is a SHOULD, not a hard gate failure. The priority is comprehensive test coverage.

### Enforcement

- QA Code Quality agent checks file length as a P1 finding
- Peer reviewers flag files approaching the limit
- Files exceeding 150 lines are mandatory fixes before the slice ships

---

## §4 Display-Only Frontend

Frontend components display data and report user actions. They do NOT contain business logic.

> **See also:** Article 26 for the Backend for Frontend (BFF) pattern — including API design, one-endpoint-per-view, and worked examples.

### Prohibited in Frontend Components

- Business calculations (totals, averages, scoring, ranking)
- Filtering or sorting by business rules
- Conditional business logic ("if user is premium, show X")
- Data transformation beyond display formatting

### Permitted in Frontend Components

- UI state management (modal open/close, loading indicators, form input values)
- Form input handling and client-side validation for UX feedback
- Display formatting (date formatting, number formatting, currency display)
- The four mandatory states (loading, error, empty, populated) per `coder-frontend.md` §3.1

### The Rule

If the frontend is computing, the API contract is wrong. The backend sends exactly what the frontend needs to render. If the frontend is filtering, sorting, or calculating, the API endpoint should be doing that work.

### Enforcement

- QA Code Quality agent checks for business logic in frontend components (P1 finding)
- Peer reviewers flag any calculation or conditional business rule in client code

---

## §5 Observability Stack

All projects MUST have structured logging and error tracking. No exceptions.

### Required Tools

| Placeholder | Purpose | Required |
|-------------|---------|----------|
| `{ERROR_TRACKING_SERVICE}` | Error tracking + performance monitoring | YES |
| `{STRUCTURED_LOGGER}` | Structured JSON logging | YES |
| `{LOGGER_TRANSPORT}` | Bridge between logger and error tracker | YES |
| `{ERROR_TRACKING_MCP}` | MCP server for Claude Code integration | RECOMMENDED |

### Language Equivalents

| Language | Error Tracker | Structured Logger | Bridge |
|----------|--------------|-------------------|--------|
| Node.js / TypeScript | Sentry | Pino | pino-sentry-transport |
| Python | Sentry | structlog | sentry-sdk |
| Go | Sentry | zerolog / zap | sentry-go |
| Browser / SPA | Sentry Browser SDK | Custom `logger.ts` wrapping console | @sentry/browser |
| {PRIMARY_LANGUAGE} | {ERROR_TRACKING_SERVICE} | {STRUCTURED_LOGGER} | {LOGGER_TRANSPORT} |

### Rules

- **No raw console output.** No `console.log`, `print()`, `fmt.Println()`, or equivalent in committed code. All logging goes through the structured logger.
- **Structured entries.** Every log entry is a JSON object with at minimum: `level`, `message`, and `context` (relevant data for debugging).
- **Error tracking integration.** Every `logger.error()` call automatically creates an event in `{ERROR_TRACKING_SERVICE}` via `{LOGGER_TRANSPORT}`.
- **Created in Slice 0.** The shared logger at `src/shared/logging/logger.{EXT}` and the error tracking configuration are created during Slice 0 bootstrap, before any feature code is written.
8. Husky pre-push hooks block pushes containing `console.log` or `print()` (see Article 23).

> **See also:** Article 28 for the operational service log inventory template.

---

## §6 Error Wrapping & Context Chaining

Every major function wraps errors with context before passing them up the call stack.

### AppError Class

```
class AppError:
  message: string         # Human-readable description of what went wrong
  code: string            # Machine-readable error code (e.g., "BRIEF_NOT_FOUND")
  statusCode: number      # HTTP status code (set ONLY in the route layer)
  cause: Error | null     # Original error that triggered this
  context: object         # Additional debugging context
```

### Language Idioms

| Language | How to Wrap |
|----------|------------|
| Python | `raise AppError("message") from original_error` |
| JavaScript / TypeScript | `throw new AppError("message", { cause: originalError })` |
| Go | `fmt.Errorf("message: %w", originalError)` |

### Per-Layer Context

| Layer | Context to Add |
|-------|---------------|
| **Route** | HTTP method, endpoint path, request parameters |
| **Service** | Business operation name, input summary |
| **Repository** | Database query, table name, operation type |

### HTTP Boundary Rule

At the HTTP boundary (route layer), cause chains are **NEVER** exposed to clients. The route layer:
1. Logs the full error chain (including all causes) via the structured logger
2. Reports the error to `{ERROR_TRACKING_SERVICE}`
3. Returns a generic error response to the client (e.g., `{ "error": "Internal server error" }`)

### Created in Slice 0

The AppError class at `src/shared/errors/app-error.{EXT}` is created during Slice 0 bootstrap. All feature code imports and uses this class.

### Enforcement

- QA Code Quality agent checks for bare `throw new Error()` or `raise Exception()` without wrapping (P1 finding)
- Peer reviewers verify that each layer adds appropriate context

---

## §7 P0/P1/P2 Test Priority Classification

Features are classified by business criticality. Classification determines test coverage requirements.

| Priority | Definition | Coverage Requirement | When Tested |
|----------|-----------|---------------------|-------------|
| **P0** | If it breaks, everything is down. Revenue-critical paths. | 100% service-layer coverage | Tested FIRST in Phase B |
| **P1** | Important but not catastrophic | ≥ 90% service-layer coverage | Tested after P0 |
| **P2** | Nice-to-have | Best-effort coverage | Tested last |

### Rules

- **Classification is a planning decision.** The owner classifies features as P0/P1/P2 during Step 1e (slice definition). Agents do not assign priority — the owner does.
- **P0 is never deprioritized.** Under time pressure, P2 coverage can be deferred. P1 coverage can be reduced (with documented exemptions). P0 coverage is NEVER reduced.
- **Tests focus on the service layer.** The service layer contains all business logic. Route tests are minimal (HTTP plumbing). Repository tests use integration test fixtures. Service-layer testing is where correctness lives.

### Examples (Project-Specific)

| Priority | Examples |
|----------|---------|
| P0 | {P0_EXAMPLES — e.g., "Authentication, payment processing, core data pipeline"} |
| P1 | {P1_EXAMPLES — e.g., "User settings, reporting dashboards, admin panel"} |
| P2 | {P2_EXAMPLES — e.g., "Cosmetic features, convenience shortcuts, tooltips"} |

---

## §8 Migration Strategy (Existing Projects)

For projects that are already in progress under the old directory structure:

- **Do not rewrite the codebase.** Migrating everything at once is wasteful and risky.
- **Refactor only when you touch it.** When a bug fix or feature change requires touching an existing file, refactor it into the new pattern (feature folder, layer separation, error wrapping) at that time.
- **New features always use the new structure.** Any new feature created after adopting these standards uses feature-based folders from the start.
- **Over time, the codebase naturally migrates.** As files are touched, they move into the new pattern. After several slices, most active code will be in feature folders.
- **Security during refactoring:** Refactoring is NOT exempt from security review. When restructuring code, run the same security checks as new code: OWASP Top 10, secrets scan, dependency audit, auth/authz verification. Code that was secure in its original location may become insecure when moved (e.g., a function that relied on middleware validation in its old route may lack that protection in its new location).
