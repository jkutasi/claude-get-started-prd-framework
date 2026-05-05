# §1 Feature-Based Folder Organization & Slice Isolation

> Part of [Architecture Standards](../ARCHITECTURE-STANDARDS-TEMPLATE.md). Aligned with [Article 20a](../articles/article-20a-feature-modules.md).

All source code is organized by feature (vertical slice), not by type. Each feature is self-contained in its own folder.

## Directory Structure

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

## Co-location Rules

- **Tests alongside code.** Unit tests live in the feature folder next to the service file they test. The `tests/` directory is ONLY for cross-feature integration tests.
- **Self-contained features.** Everything about a feature lives in one folder. To understand a feature, look at one folder. To remove a feature, delete one folder.
- **Shared utilities** go in `src/shared/` ONLY when they serve 3+ features. Do not prematurely extract utilities.

## Slice Isolation — Hard Contract (3 rules)

The following rules are **hard contract**, not advisory. Violations block merge.

### Rule 1 — Slices never import from each other

`features/A/` cannot import from `features/B/`. Shared code goes into `shared/`, treated as **public API** with review, versioning, and back-compat. Breaking changes in `shared/` require a coordinated migration of every consuming slice in the same PR.

### Rule 2 — Slices own their own DB access

Each slice's `{entity}-repository.{EXT}` is the ONLY module that reads or writes that entity's rows. Other slices that need the data MUST call this slice's API or subscribe to its events — they MUST NOT reach into the database directly.

### Rule 3 — Every slice ships behind a feature flag

Every slice has a feature flag (e.g., `slice_name_v2`). Code merges to `main` continuously, dark in production until the flag flips. The flag MUST be registered in the central flag registry before the slice's first PR.

## Enforcement

- **CODEOWNERS** protects `shared/` — any PR that modifies it requires explicit human review.
- **CI** flags any PR that touches more than one slice folder. Multi-slice PRs require a written justification in the description.
- **Per-slice CLAUDE.md** forbids agents from modifying files outside `features/{my-slice}/`.

## Escape Hatches

- **CLI tools:** Replace route → service → repository with command handler → service → data access.
- **Frontend-only projects:** The display-only rule (§4) still applies. State management replaces the route layer.
- **Workers / background jobs:** Replace route with job handler. Service and repository layers remain the same.
