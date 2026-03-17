# Phase A.5: Doc Bootstrap + Diagram Review

> Load this file when starting Phase A.5. Complete all steps and the gate before proceeding to Phase A.6.

## Purpose

Create or update slice documentation. For Slice 0, this includes project-level docs. For Slices 1+, per-slice diagrams are created in Phase A (non-blocking).

## Slice 0 Only

If this is Slice 0, the CTO delegates to the Scribe agent:

1. **PROJECT.md** — Project overview, tech stack, architecture summary.
2. **DOCS_MAP.md** — Index of all documentation files and their purposes.
3. **Contract stubs** — Initial contract files for all planned slices.
4. **High-level overview diagrams** (Architect creates these for user review):
   - System Architecture diagram
   - Data Model ER diagram
   - User Flow diagram
   - Slice Dependency Graph

## Slices 1+

For slices after Slice 0:

5. Update PROJECT.md if this slice changes architecture or tech stack.
6. Update DOCS_MAP.md with any new documentation files.
7. Per-slice detailed diagrams were already created in Phase A (non-blocking).
8. Review diagrams for accuracy against the slice contract.

## Documentation Standards

- All docs use Markdown format.
- Diagrams use Mermaid syntax (inline in Markdown) or are saved as image files.
- Every doc file must be listed in DOCS_MAP.md.
- Replace all `{PLACEHOLDER}` values — no placeholders survive past this phase.

## Gate

```
+------------------------------------------------------------------+
| DOC BOOTSTRAP GATE A.5: Before proceeding to Phase A.6:         |
| [] PROJECT.md exists and is current                              |
| [] DOCS_MAP.md exists and lists all doc files                    |
| [] Slice contract is complete (no unfilled placeholders)         |
| [] Diagrams created and reviewed for accuracy                    |
| [] (Slice 0 only) High-level overview diagrams ready for user   |
+------------------------------------------------------------------+
```

## Next Phase

Proceed to **Phase A.6: User Scope Confirmation** (`phase-a6-user-scope.md`).
