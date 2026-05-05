# Phase C: Implementation

> Load this file when starting Phase C. Complete all steps and the gate before proceeding to Phase E.

## Purpose

Write the code that makes all RED tests from Phase B turn GREEN. Code is written by coder teammates — the CTO NEVER writes code (Nuclear Rule 1).

## Steps

### C.0: QMD Context Retrieval

> **QMD QUERY** (non-blocking): Spawn `/relay-qmd` — query `"architecture patterns API quirks performance {SLICE_TOPIC}"` in `{PROJECT_NAME}` + `vault`. Incorporate findings before coders begin. If QMD unavailable, proceed.

1. CTO assigns implementation to **coder teammates** (NOT itself).
2. Coders receive the failing tests + spec from Phase B.
3. Coders write code until all tests PASS.
4. All code must follow Article 20 architecture standards:
   - **Feature folders** (20a) — code organized by feature, not by type.
   - **Three-layer separation** (20b) — presentation / business logic / data access.
   - **150-line file limit** (20c) — no file exceeds 150 lines.
   - **Display-only frontend** (20d) — frontend has no business logic.
   - **Structured logging** (20e) — use Pino/structlog, no `console.log`.
   - **Error wrapping** (20f) — all errors wrapped with `AppError` or equivalent.

## Nuclear Rule 1 Enforcement

The CTO orchestrates this phase but does NOT write any code:
- Delegates to teammates or spawns sub-agents.
- Reviews teammate output for architecture compliance.
- If a teammate is stuck, the CTO provides guidance but does NOT write the fix.

## File Structure Compliance (Nuclear Rule 9)

- Coders build to the file map defined in Phase A.
- No files created outside the plan without CTO approval.
- No files in the "don't touch" list are modified.

## Gate

```
+------------------------------------------------------------------+
| NUCLEAR GATE C: CTO must confirm:                                |
| [] "I did NOT write any code myself in this phase"               |
| [] "All code was produced by teammates or their sub-agents"      |
| [] "All tests from Phase B now PASS"                             |
| [] "All code follows Article 20: feature folders, layer          |
|     separation, 150-line limit, structured logging, error wrap"  |
+------------------------------------------------------------------+
```

## Next Phase

Proceed to **Phase E: Peer Review** (`phase-e-peer-review.md`).
