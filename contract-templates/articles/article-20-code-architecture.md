# Article 20: Code Architecture Standards

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

All production code MUST follow the architecture standards defined in `contracts/ARCHITECTURE_STANDARDS.md` (customized from `contract-templates/ARCHITECTURE-STANDARDS-TEMPLATE.md`). This article provides the summary; the contract document provides the full details.

### Article 20a: Feature-Based Folder Organization

All source code is organized in feature-based folders under `src/`. Each feature folder contains route, service, repository, test, and optionally types files. Tests live alongside the code they test. Cross-feature imports are a code smell — flag in review. See `contracts/ARCHITECTURE_STANDARDS.md` §1 for the full directory structure template.

### Article 20b: Three-Layer Separation

Every feature separates concerns into three layers: Route (HTTP only, ~20-30 lines), Service (business logic only, ~80-150 lines), Repository (data access only, ~50-100 lines). Flow is always Route → Service → Repository. Never skip a layer. One coder sub-agent is spawned per layer file.

### Article 20c: 150-Line File Limit

Every production source file MUST stay under 150 lines (excluding comments and blank lines). This is a hard rule enforced in peer review and QA Code Quality checks. If a file is approaching the limit, the concern must be split. This complements the existing 40-line function limit — a 150-line file holds at most 3-4 max-length functions. Test files SHOULD stay under 150 lines but may be split into multiple test files per feature rather than gate-fail.

### Article 20d: Display-Only Frontend

Frontend components render data and report user actions. They do NOT contain business calculations, filtering by business rules, or conditional business logic. Permitted: UI state management (modals, loading indicators), form input handling, display formatting (dates, numbers), and the four mandatory states (loading, error, empty, populated). If the frontend is computing, the API contract is wrong.

### Article 20e: Observability Stack

All projects MUST have structured logging via `{STRUCTURED_LOGGER}` and error tracking via `{ERROR_TRACKING_SERVICE}`. No raw console output (`console.log`, `print()`, etc.) in committed code. All log entries must be structured JSON. The shared logger is created during Slice 0 at `src/shared/logging/logger.{EXT}`. See `contracts/ARCHITECTURE_STANDARDS.md` §5 for language-equivalent recommendations.

### Article 20f: Error Wrapping & Context Chaining

All errors MUST be wrapped with context using the project's AppError class before being passed up the call stack. Each layer adds its own context: route adds endpoint and parameters, service adds operation name, repository adds query and table. At the HTTP boundary, cause chains are NEVER exposed to clients — return a generic error response and log the full chain server-side. The AppError class is created during Slice 0 at `src/shared/errors/app-error.{EXT}`. See `contracts/ARCHITECTURE_STANDARDS.md` §6 for the full AppError specification.

### Article 20g: P0/P1/P2 Test Priority Classification

Features are classified by business criticality: P0 (revenue-critical, 100% service-layer coverage), P1 (important, ≥90% coverage), P2 (best-effort). Classification is a planning decision made by the owner during Step 1d — agents do not assign priority. P0 coverage is NEVER reduced under time pressure. See `contracts/ARCHITECTURE_STANDARDS.md` §7.

### Article 20h: Migration Strategy

Existing projects refactor only when touching a file. Do not rewrite the entire codebase. When a bug fix or feature change requires touching an existing file, refactor it into the new pattern (feature folder, layer separation, error wrapping) at that time. New features always use the new structure from the start. See `contracts/ARCHITECTURE_STANDARDS.md` §8.
