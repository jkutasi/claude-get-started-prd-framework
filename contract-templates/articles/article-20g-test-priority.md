# Article 20g: P0/P1/P2 Test Priority Classification

> Part of [Article 20: Code Architecture Standards](article-20-code-architecture.md). Load only when you need this specific subsection.

Features are classified by business criticality. Classification determines test coverage requirements.

| Priority | Definition | Coverage | When Tested |
|----------|-----------|----------|-------------|
| **P0** | Revenue-critical. If it breaks, everything is down. | 100% service-layer coverage | Tested FIRST in Phase B |
| **P1** | Important but not catastrophic | ≥ 90% service-layer coverage | Tested after P0 |
| **P2** | Nice-to-have | Best-effort coverage | Tested last |

## Rules

- **Classification is a planning decision.** The owner classifies features as P0/P1/P2 during Step 1e (slice definition). Agents do not assign priority — the owner does.
- **P0 is never deprioritized.** Under time pressure, P2 coverage can be deferred. P1 coverage can be reduced (with documented exemptions). P0 coverage is **NEVER** reduced.
- **Tests focus on the service layer.** The service layer contains all business logic. Route tests are minimal. Repository tests use integration fixtures. Service-layer testing is where correctness lives.

See `contracts/ARCHITECTURE_STANDARDS.md` §7 for examples.
