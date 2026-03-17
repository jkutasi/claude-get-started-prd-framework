# Phase A.6: User Scope Confirmation (Article 19)

> **HUMAN CHECKPOINT.** Load this file when starting Phase A.6. You MUST present to the user and receive APPROVE before proceeding.

## Purpose

Present the slice scope to the user for confirmation before any adversarial review or implementation begins. This is a mandatory human gate.

## What to Present

The CTO presents the following to the user:

1. **Slice summary** — What this slice will build, in plain language.
2. **Gherkin scenarios** — The acceptance criteria that define "done."
3. **Diagrams** — Sequence diagram and focused ER diagram from Phase A.
4. **Goal Achievement Test** — The end-to-end test that proves the slice works.
5. **Scope changes** — If scope changed from the original plan, highlight what changed and why.

## User Response

The user responds with one of:

- **APPROVE** — Proceed to Phase A.7 (Red Team).
- **REVISE** — User provides feedback. CTO adjusts the plan and re-presents.

## Re-Presentation Loop

If the user says REVISE:

1. Read the user's feedback carefully.
2. Adjust the slice contract, Gherkin, and/or diagrams.
3. Re-present the updated scope.
4. Repeat until the user says APPROVE.

There is no maximum iteration limit on this gate — the user decides when the scope is right.

## Gate

```
+------------------------------------------------------------------+
| USER SCOPE GATE A.6: Before proceeding to Red Team:              |
| [] "User reviewed slice scope (summary + Gherkin + diagrams)"    |
| [] "User responded APPROVE"                                      |
| [] "Any scope changes from original plan were highlighted"       |
+------------------------------------------------------------------+
```

## Next Phase

Proceed to **Phase A.7: Red Team + Professor Pre-Build Gate** (`phase-a7-red-team.md`).
