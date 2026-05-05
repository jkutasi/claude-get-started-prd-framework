# `{slice-name}` slice

One vertical feature, cut top-to-bottom through client, API, and DB. Owned by `{owner}`. Shipped behind feature flag `{slice_name}_v2`.

## The spec lives in the `.feature` file

Open [`{slice-name}.feature`](./{slice-name}.feature). That Gherkin file is the contract. Implementation is complete only when **every scenario passes**. If something feels ambiguous, the spec wins — update the spec first, then the code.

## Folder map

```
{slice-name}/
|-- {slice-name}.feature          # Gherkin spec - write FIRST
|-- client/                       # UI components for this slice only
|-- api/                          # Route handlers for this slice only
|-- db/
|   `-- {entity}-repository.{EXT} # The ONLY DB access for this slice
|-- steps/
|   `-- {slice-name}.steps.{EXT}  # Gherkin step definitions
|-- sentry.{EXT}                  # withSliceContext() wrapper
|-- slice.config.{EXT}            # name, version, owner, featureFlag, tags
|-- CLAUDE.md                     # Agent rules scoped to this slice
`-- README.md                     # You are here
```

## The three slice-isolation rules (Article 20a)

1. **Slices never import from each other.** If two slices need the same code, it lives in `shared/`. Cross-slice imports are blocked at review.
2. **Slices own their own DB access.** `db/{entity}-repository.{EXT}` is the only module in this repo that reads or writes `{entity}` rows. Other slices reach this data via this slice's API or events — never the database directly.
3. **Slices ship behind feature flags.** New code paths are dark in production until `{slice_name}_v2` flips. Multiple slices can merge to `main` in parallel without colliding.

## Sentry contract (Article 20e-2)

- Every `captureException` flows through `withSliceContext()` in [`sentry.{EXT}`](./sentry.{EXT}). That attaches the `slice`, `slice_version`, and `feature_flag` context automatically.
- API handlers under `api/` set `route`, `layer`, and `slice` Sentry tags before any code that can throw runs.
- DB methods in `db/` are wrapped in `Sentry.startSpan({ op: 'db.query', ... })`.
- Step bodies in `steps/` open `Sentry.startSpan({ op: 'test.step', ... })` so test traces match production trace shape.

## Filing changes against this slice

- Open one PR per slice. Multi-slice PRs are auto-flagged for elevated review.
- Need code in `shared/` or another slice? Leave a PR comment proposing the change and stop. Do not silently refactor.
- Bumping `version` in `slice.config.{EXT}` is a breaking change for any consumer; coordinate the migration in the same PR.

## Quick links

- Slice metadata: [`slice.config.{EXT}`](./slice.config.{EXT})
- Agent rules: [`CLAUDE.md`](./CLAUDE.md)
- Repository module: [`db/{entity}-repository.{EXT}`](./db/{entity}-repository.{EXT})
- Sentry wrapper: [`sentry.{EXT}`](./sentry.{EXT})
- Step definitions: [`steps/{slice-name}.steps.{EXT}`](./steps/{slice-name}.steps.{EXT})
