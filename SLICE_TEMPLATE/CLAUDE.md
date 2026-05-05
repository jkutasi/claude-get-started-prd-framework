# Slice-scoped agent rules — `features/{slice-name}/`

These rules apply to any Claude Code agent operating inside this slice. They override anything more permissive in the repo-root `CLAUDE.md`.

## The hard rules (Article 20a)

1. **Never modify files outside `features/{slice-name}/`.**
   If you believe a change in `shared/`, another slice, or repo-root config is required, propose it in a PR comment and **STOP**. Do not silently refactor cross-slice code. The shared directory is gated by CODEOWNERS — your edit will not pass review.

2. **Never import from another slice.**
   `features/{slice-name}/` cannot import from `features/{other-slice}/`. If two slices need the same code, that code lives in `shared/` and is reached via its public API. (Article 20a Rule 1)

3. **DB access for this slice goes through `db/{entity}-repository.{EXT}` only.**
   Do not add SQL or DB client calls anywhere else inside this slice. Other slices that need this data MUST call this slice's API or subscribe to its events. (Article 20a Rule 2)

4. **Ship behind the feature flag declared in `slice.config.{EXT}`.**
   New code paths MUST be guarded by the slice's `featureFlag`. Verify the flag is registered in the central flag registry before opening the first PR. (Article 20a Rule 3)

## The spec is the `.feature` file

`{slice-name}.feature` is your spec. Implementation is complete only when **every scenario passes**. If a scenario is ambiguous, ask in a PR comment — do not invent behavior. The Gherkin file is the QA gate.

## Sentry contract (Article 20e-2)

- Every `captureException` in this slice MUST go through `withSliceContext()` in `sentry.{EXT}`.
- Every API route handler under `api/` opens a `withScope` and sets the `route`, `layer`, `slice` tags.
- Every public method in `db/{entity}-repository.{EXT}` is wrapped in `Sentry.startSpan({ op: 'db.query', name: '{entity}.{operation}' }, ...)`.
- Every step body in `steps/` opens a `Sentry.startSpan({ op: 'test.step', ... })`.

## File-size budget

Keep each file ≤150 lines. Split long modules along the natural seams (one query per file, one component per file) before any single file crosses the cap.

## What to do when blocked

- Need cross-slice code → PR comment, then STOP.
- Need a new shared utility → PR comment with proposed API + use cases, then STOP.
- Need to bump a slice dependency's version → PR comment listing the migration plan, then STOP.

Do **not** attempt to "be helpful" by silently refactoring across the slice boundary. That is the failure mode this contract exists to prevent.
