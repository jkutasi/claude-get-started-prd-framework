# Phase A: Preparation

> Load this file when starting Phase A of a slice. Complete all steps and the gate before proceeding to Phase A.5.

## Purpose

Research, read existing code, understand scope, and create per-slice detailed diagrams before any implementation begins.

## Steps

### A.0: QMD Context Retrieval (Non-Blocking)

1. CTO spawns QMD relay with query: slice topic + key technologies.
2. Search `template-decisions` and project-specific collections.
3. If relevant ADRs found, note them for the slice plan.
4. If QMD is not configured, proceed — this step is informational.

### A.1: Review Slice Requirements

1. Read the slice contract (`contracts/slice-N-contract.md`).
2. Read all Gherkin acceptance criteria for this slice.
3. Identify which user stories and acceptance criteria are in scope.
4. Note any dependencies on prior slices or external systems.

### A.2: Research and Gather Context

5. Researcher agent gathers relevant documentation, API docs, library docs.
6. Build or update skills files with any new patterns or libraries needed.
7. Read existing codebase files that this slice will touch or depend on.
8. Identify existing patterns (naming, structure, error handling) to follow.

> **QMD QUERY** (non-blocking): Spawn `/relay-qmd` — query `"prior context {SLICE_TOPIC} patterns gotchas"` in `{PROJECT_NAME}` + `vault`. Include findings in research summary. If QMD unavailable, proceed.

### A.3: Create Per-Slice Diagrams

9. Architect creates per-slice detailed diagrams:
   - **Sequence diagram** — showing the flow for this slice's primary use case.
   - **Focused ER diagram** — showing only the data entities this slice touches.
10. Diagrams go in the project's `docs/diagrams/` directory.

## File Structure Planning (Nuclear Rule 9)

11. Define the exact file structure BEFORE any code:
    - Which files to CREATE (new files for this slice).
    - Which files to MODIFY (existing files that need changes).
    - Which files to NOT TOUCH (explicitly list files that are off-limits).
12. Every sub-agent must know which files it owns. No improvisation.

## Gate

```
+------------------------------------------------------------------+
| PREPARATION GATE A: Before proceeding to Phase A.5:              |
| [] Slice contract read and understood                            |
| [] Gherkin acceptance criteria reviewed                          |
| [] Existing codebase read (relevant files)                       |
| [] Per-slice diagrams created (sequence + focused ER)            |
| [] File structure defined (create/modify/don't-touch lists)      |
| [] Dependencies on prior slices identified                       |
| [] Research complete — skills files updated if needed            |
| [] QMD context checked (or QMD not configured)                   |
+------------------------------------------------------------------+
```

## Next Phase

Proceed to **Phase A.5: Doc Bootstrap** (`phase-a5-doc-bootstrap.md`).
