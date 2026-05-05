# §2 Three-Layer Separation

> Part of [Architecture Standards](../ARCHITECTURE-STANDARDS-TEMPLATE.md). Aligned with [Article 20b](../articles/article-20b-three-layer-separation.md).

Every feature separates concerns into three layers. Each layer has one job.

| Layer | Responsibility | Line Target | What It Does NOT Do |
|-------|---------------|-------------|---------------------|
| **Route** | HTTP handling | ~20-30 lines | No business logic. No database calls. |
| **Service** | Business logic | ~80-150 lines | No HTTP objects (`req`, `res`). No database queries. |
| **Repository** | Data access | ~50-100 lines | No business logic. No HTTP concerns. |

## Flow

```
Route → Service → Repository
```

- Never skip a layer. A route MUST NOT call a repository directly.
- Never let a layer do another layer's job. If a service is building SQL queries, that logic belongs in the repository.

## Spawn Model (Agent Teams)

By default, one coder sub-agent is spawned per layer file. A feature with route + service + repository = 3 spawns. For complex layers with multiple functions, additional spawns per function within a layer are appropriate — the existing "one focused job per spawn" rule takes precedence over the per-file default.
