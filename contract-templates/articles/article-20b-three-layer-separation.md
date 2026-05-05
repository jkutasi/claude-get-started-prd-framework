# Article 20b: Three-Layer Separation

> Part of [Article 20: Code Architecture Standards](article-20-code-architecture.md). Load only when you need this specific subsection.

Every feature separates concerns into three layers:

- **Route** — HTTP only, ~20-30 lines
- **Service** — business logic only, ~80-150 lines
- **Repository** — data access only, ~50-100 lines

## Flow

```
Route → Service → Repository
```

- Never skip a layer. A route MUST NOT call a repository directly.
- Never let a layer do another layer's job. If a service is building SQL queries, that logic belongs in the repository.

## Spawn Model

By default, one coder sub-agent is spawned per layer file. A feature with route + service + repository = 3 spawns. For complex layers with multiple functions, additional spawns per function within a layer are appropriate — the existing "one focused job per spawn" rule takes precedence over the per-file default.

See `contracts/ARCHITECTURE_STANDARDS.md` §2 for the full layer responsibility table.
