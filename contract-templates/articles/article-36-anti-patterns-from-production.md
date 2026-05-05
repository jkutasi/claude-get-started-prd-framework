# Article 36: Anti-Patterns from Production (Index)

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.
>
> **Cross-references:** Article 17 (Test-First), Article 18 (Test Peer Review),
> Article 35 (Error & Rescue Registry)

## What This Article Is

A catalog of universal anti-patterns drawn from production incidents. Every slice that
ships UI changes, data-shape changes, external-API calls, or SQL changes MUST be checked
against this catalog before Phase E peer review. If your change touches any surface below,
the corresponding regression test is mandatory — not optional.

---

## Anti-Pattern Catalog

| # | Anti-Pattern | Surface | Detail |
|---|--------------|---------|--------|
| 1 | Server data interpolated into inline JS | Frontend | [36a §1](article-36a-anti-patterns-frontend.md#1-server-data-interpolated-into-inline-js) |
| 2 | Hidden-field vs. visual-chip drift | Frontend | [36a §2](article-36a-anti-patterns-frontend.md#2-hidden-field-vs-visual-chip-drift) |
| 3 | Pre-applied defaults violating cross-field invariants | Frontend | [36a §3](article-36a-anti-patterns-frontend.md#3-pre-applied-defaults-that-violate-cross-field-invariants) |
| 4 | Status defaults that break UI promises | Frontend | [36a §4](article-36a-anti-patterns-frontend.md#4-status-defaults-that-break-ui-promises) |
| 5 | DB parser quirks — non-portable SQL syntax | Backend | [36b §5](article-36b-anti-patterns-backend.md#5-database-parser-quirks--non-portable-sql-syntax) |
| 6 | Wrong API endpoint or model identifier | Backend | [36b §6](article-36b-anti-patterns-backend.md#6-wrong-api-endpoint-or-model-identifier) |
| 7 | Silent fallback to a degraded model | Backend | [36b §7](article-36b-anti-patterns-backend.md#7-silent-fallback-to-a-degraded-model) |
| 8 | Marking issues resolved based on event silence | Backend | [36b §8](article-36b-anti-patterns-backend.md#8-marking-issues-resolved-based-on-event-silence) |
| 9 | NULL-tolerant ORDER BY with no fallback rank | Backend | [36b §9](article-36b-anti-patterns-backend.md#9-null-tolerant-order-by-with-no-fallback-rank) |
| 10 | Silent fallback paths masking exceptions | Backend | [36b §10](article-36b-anti-patterns-backend.md#10-silent-fallback-paths-masking-exceptions) |

---

## Sub-Articles

- **[article-36a-anti-patterns-frontend.md](article-36a-anti-patterns-frontend.md)** — Frontend patterns #1–#4 (inline JS injection, chip drift, cross-field defaults, status defaults). Full BAD / FIX / test for each.
- **[article-36b-anti-patterns-backend.md](article-36b-anti-patterns-backend.md)** — Backend patterns #5–#10 (DB parser quirks, wrong API endpoint, silent model fallback, Sentry resolved on silence, NULL ORDER BY, silent fallback paths). Full BAD / FIX / test for each.
