# §7 P0/P1/P2 Test Priority Classification

> Part of [Architecture Standards](../ARCHITECTURE-STANDARDS-TEMPLATE.md). Aligned with [Article 20g](../articles/article-20g-test-priority.md).

Features are classified by business criticality. Classification determines test coverage requirements.

| Priority | Definition | Coverage Requirement | When Tested |
|----------|-----------|---------------------|-------------|
| **P0** | If it breaks, everything is down. Revenue-critical paths. | 100% service-layer coverage | Tested FIRST in Phase B |
| **P1** | Important but not catastrophic | ≥ 90% service-layer coverage | Tested after P0 |
| **P2** | Nice-to-have | Best-effort coverage | Tested last |

## Rules

- **Classification is a planning decision.** The owner classifies features as P0/P1/P2 during Step 1e (slice definition). Agents do not assign priority — the owner does.
- **P0 is never deprioritized.** Under time pressure, P2 coverage can be deferred. P1 coverage can be reduced (with documented exemptions). P0 coverage is **NEVER** reduced.
- **Tests focus on the service layer.** The service layer contains all business logic. Route tests are minimal (HTTP plumbing). Repository tests use integration test fixtures. Service-layer testing is where correctness lives.

## Examples (Project-Specific)

| Priority | Examples |
|----------|---------|
| P0 | {P0_EXAMPLES — e.g., "Authentication, payment processing, core data pipeline"} |
| P1 | {P1_EXAMPLES — e.g., "User settings, reporting dashboards, admin panel"} |
| P2 | {P2_EXAMPLES — e.g., "Cosmetic features, convenience shortcuts, tooltips"} |
