# Article 20a: Feature-Based Folder Organization & Slice Isolation

> Part of [Article 20: Code Architecture Standards](article-20-code-architecture.md). Load only when you need this specific subsection.

All source code is organized in feature-based (vertical-slice) folders under `src/`. Each feature folder contains route, service, repository, test, and optionally types files. Tests live alongside the code they test. See `contracts/ARCHITECTURE_STANDARDS.md` §1 for the full directory structure template.

## Slice Isolation — Hard Contract

Slice isolation is **hard contract**, not a code-smell heuristic. The three rules below MUST be enforced; violations block merge.

### Rule 1 — Slices never import from each other

`features/A/` cannot import from `features/B/`. If two slices need the same code, that code goes into `shared/`. `shared/` is treated as **public API**: changes require review, versioning, and back-compat. A breaking change in `shared/` requires a coordinated migration of every consuming slice in the same PR (or a versioned deprecation path).

### Rule 2 — Slices own their own DB access

Each slice's `{entity}-repository.{EXT}` is the **only** module that reads or writes that entity's rows. Other slices that need the data MUST call this slice's API or subscribe to its events — they MUST NOT reach into the database directly. This keeps schema changes contained to the owning slice and prevents implicit coupling through shared tables.

### Rule 3 — Every slice ships behind a feature flag

Every slice has a feature flag (e.g., `slice_name_v2`). Code merges to `main` continuously, but the slice is dark in production until the flag is flipped. This is what allows multiple developers (or multiple Claude Code agents) to have multiple PRs touching different slices, all merging without stepping on each other. The feature flag MUST be registered in the central flag registry before the slice's first PR.

## Enforcement

- **CODEOWNERS protects `shared/`.** The `shared/` directory requires explicit human review on any PR that touches it. CODEOWNERS file at the repo root assigns this to the senior owner.
- **CI flags multi-slice PRs.** Any pull request that touches more than one slice folder is auto-flagged for elevated review. The default expectation is that one PR equals one slice. Multi-slice PRs are allowed but require a written justification in the PR description.
- **Agent guardrails.** Each slice's `CLAUDE.md` forbids modifications outside `features/{my-slice}/`. If an agent needs something in `shared/`, it proposes the change in a comment and stops — it does NOT silently refactor shared code.
- **Repository module is a structural rule.** A QA agent or static check verifies that no module outside `features/{slice}/` imports the slice's repository module directly.

## Rationale

The previous "cross-feature imports are a code smell — flag in review" was too soft for a system that supports parallel slice development by multiple humans and agents. A code-smell warning relies on reviewers catching imports late and on agents having the discipline to refuse "helpful" cross-slice refactors. Hard rules + CODEOWNERS + CI checks make those failure modes mechanical to detect, not advisory.
