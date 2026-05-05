# Architecture Standards — {PROJECT_NAME}

> **Purpose:** This document defines the mandatory code architecture standards for all production code. These standards are the PRIMARY quality mechanism — they prevent bugs at the structural level by ensuring every file is small, every concern is isolated, and every error is traceable. All agents, teammates, and sub-agents MUST follow these standards. QA agents verify compliance.
>
> **[Article 20](articles/article-20-code-architecture.md)** in the contract articles is the summary; the section files below provide the full details.

This document is split into one file per section. Load only the section you need.

| § | File | Topic |
|---|------|-------|
| 1 | [standards/01-feature-modules.md](standards/01-feature-modules.md) | Feature-based folders + slice-isolation hard rules (3 rules) |
| 2 | [standards/02-three-layer-separation.md](standards/02-three-layer-separation.md) | Route → Service → Repository |
| 3 | [standards/03-file-limit.md](standards/03-file-limit.md) | 150-line file limit |
| 4 | [standards/04-display-only-frontend.md](standards/04-display-only-frontend.md) | Display-only frontend rule |
| 5 | [standards/05-observability-stack.md](standards/05-observability-stack.md) | Observability overview (Sentry + structured logging) |
| 5.1 | [standards/05-1-logging-and-errors.md](standards/05-1-logging-and-errors.md) | Structured logging, captureException slice tag, beforeSend redaction |
| 5.2 | [standards/05-2-distributed-tracing.md](standards/05-2-distributed-tracing.md) | Three-layer Sentry init, trace propagation, withScope, startSpan, setUser, release |
| 6 | [standards/06-error-wrapping.md](standards/06-error-wrapping.md) | AppError + per-layer context chaining |
| 7 | [standards/07-test-priority.md](standards/07-test-priority.md) | P0/P1/P2 classification |
| 8 | [standards/08-migration-strategy.md](standards/08-migration-strategy.md) | Refactor-when-you-touch-it migration |
| 9 | [standards/09-tooling-verification.md](standards/09-tooling-verification.md) | gate_check.py mechanical enforcement |

## What Changed in This Revision

- **§1 (Feature Modules)** — promoted slice isolation from "code smell" advisory to **three hard rules**: (1) slices never import from each other, (2) slices own their DB access, (3) every slice ships behind a feature flag. Backed by CODEOWNERS on `shared/` and CI checks on multi-slice PRs.
- **§5 (Observability)** — extended from error tracking + structured logging to **distributed-trace-grade observability**: three-layer Sentry init (client / server / DB) with separate projects, `tracePropagationTargets`, `withScope` enrichment, `Sentry.startSpan()` around DB and outbound HTTP, mandatory `beforeSend` redaction hook with required token-stripping regex, slice tag on every `captureException`, `setUser` everywhere, same release across all three layers.
- **§9 (Tooling Verification)** — added gate-check rows for `beforeSend` hook, `tracePropagationTargets`, and cross-slice import bans.
