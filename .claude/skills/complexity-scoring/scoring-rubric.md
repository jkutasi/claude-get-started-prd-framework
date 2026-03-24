# Complexity Scoring Rubric

Use this rubric alongside `SKILL.md` to assign a score from 1–10 before
starting any implementation task.

## Score Bands

### 1–2: Trivial

- Single file change
- Fewer than 20 lines changed
- No new dependencies
- No architecture decisions required
- Reversible without risk

Examples: fix a typo in a constant, rename a variable, add a missing null
check in an isolated utility function.

### 3–4: Simple

- 2–3 files touched
- Requirements are unambiguous
- No new architecture decisions
- Existing patterns can be followed directly
- Low edge-case surface area

Examples: add a new field to an existing form, add a CRUD endpoint that
follows an established pattern, update a config value.

### 5–6: Moderate

- Multiple files touched (4–8)
- Some design decisions required (which layer owns what, what the data shape is)
- Edge cases exist and must be handled explicitly
- May touch shared utilities or a shared data contract

Examples: add a new feature end-to-end (route + service + repo + test), add
OAuth provider to an existing auth system, add pagination to an existing list
endpoint.

### 7–8: Complex

- Architecture changes (new layer, new abstraction, structural refactor)
- Multiple systems touched (e.g., API + queue + cache)
- Significant testing surface (many edge cases, external dependencies to mock)
- Changes affect behaviour that other features depend on

Examples: replace a synchronous operation with an async queue, add multi-tenancy
to a single-tenant service, migrate a data model that existing records use.

### 9–10: Very Complex

- Distributed changes across many systems
- Performance-critical path (latency or throughput SLAs)
- Security-sensitive (auth, secrets, access control, encryption)
- Scope is unclear or depends on unknowns
- Failure is hard to reverse (data migrations, schema changes in production,
  third-party integrations with no sandbox)

Examples: re-architect the authentication system, add real-time pub/sub to
replace polling, design a multi-region data replication strategy.

## Scoring Factors (adjust up or down)

| Factor | Adjust |
|--------|--------|
| No existing pattern to follow | +1 |
| Touches a security boundary | +1 to +2 |
| External API with poor docs or rate limits | +1 |
| Test setup is already scaffolded | -1 |
| Change is fully isolated to one feature folder | -1 |
| Scope is crystal-clear with acceptance criteria | -1 |
| Breaking change to a public interface | +2 |

## Gate Thresholds (summary)

| Score | Required Action |
|-------|----------------|
| 1–6   | Proceed |
| 7–8   | Split into subtasks, re-score each |
| 9–10  | Write design spec first (`design-first-gate` skill) |
