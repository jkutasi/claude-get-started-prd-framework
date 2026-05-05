# Article 20: Code Architecture Standards

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

All production code MUST follow the architecture standards defined in `contracts/ARCHITECTURE_STANDARDS.md` (customized from `contract-templates/ARCHITECTURE-STANDARDS-TEMPLATE.md`). The articles below are the contract summary; the standards document provides full implementation details.

This article is split into one file per subsection. Load only the subsection you need.

| Sub | File | Topic |
|-----|------|-------|
| 20a | [article-20a-feature-modules.md](article-20a-feature-modules.md) | Feature-based folders + slice-isolation hard rules |
| 20b | [article-20b-three-layer-separation.md](article-20b-three-layer-separation.md) | Route → Service → Repository |
| 20c | [article-20c-150-line-file-limit.md](article-20c-150-line-file-limit.md) | 150-line file limit |
| 20d | [article-20d-display-only-frontend.md](article-20d-display-only-frontend.md) | Display-only frontend rule |
| 20e | [article-20e-observability-stack.md](article-20e-observability-stack.md) | Observability overview (Sentry + structured logging) |
| 20e-1 | [article-20e-1-logging-and-errors.md](article-20e-1-logging-and-errors.md) | Structured logging, captureException slice tag, beforeSend redaction |
| 20e-2 | [article-20e-2-distributed-tracing.md](article-20e-2-distributed-tracing.md) | Three-layer Sentry init, trace propagation, withScope, startSpan, setUser, release |
| 20f | [article-20f-error-wrapping.md](article-20f-error-wrapping.md) | AppError + per-layer context chaining |
| 20g | [article-20g-test-priority.md](article-20g-test-priority.md) | P0/P1/P2 classification |
| 20h | [article-20h-migration-strategy.md](article-20h-migration-strategy.md) | Refactor-when-you-touch-it migration |

## What changed in this revision

- **20a** — promoted from "code smell" warning to **three hard rules** (no cross-slice imports, slices own their DB access, every slice ships behind a feature flag) backed by CODEOWNERS + CI checks. This was required for safe parallel slice development by humans and Claude Code agents.
- **20e** — extended from "error tracking + structured logging" to **distributed-trace-grade observability**: three-layer Sentry init (client / server / DB), `tracePropagationTargets`, `withScope` enrichment, `Sentry.startSpan()` around DB and outbound HTTP, `beforeSend` redaction hook with required token-stripping regex, mandatory slice tag on every `captureException`, same release across all three layers, `setUser` everywhere.
