# Phase H: Regression Check + Implicit Behavior Regression

> Load this file when starting Phase H. Complete the gate before proceeding to Phase I.

## Purpose

Verify that fixes from Phase G did not break anything. Run abbreviated QA, Whiskey Team implicit regression, and UX re-check.

## Steps

### H.1: Abbreviated QA Re-Run

1. Run targeted QA on the areas that were fixed in Phase G.
2. Focus on the specific files and functions that changed.
3. Verify all original tests still pass (no regressions).

### H.2: Whiskey Team Implicit Behavior Regression (MANDATORY)

> **QMD QUERY** (non-blocking): Spawn `/relay-qmd` — query `"implicit behavior catalog regression patterns"` in `{PROJECT_NAME}`. Compare prior regression findings before running. If QMD unavailable, proceed.

4. Whiskey Team runs the 6-category implicit behavior regression:
   - **State Transition Gaps** — Do state machines still work correctly?
   - **Cross-Component Interactions** — Do components that talk to each other still work?
   - **Data Flow Assumptions** — Is data still flowing correctly through the pipeline?
   - **Race Conditions** — Any new timing issues introduced?
   - **Silent Failures** — Are there errors being swallowed without logging?
   - **Edge Case Combinations** — Do boundary conditions still hold?

### H.3: UX Sense Check Re-Run (frontend slices only)

5. UX Sense Check re-runs on changed frontend pages.
6. Verify that fixes did not degrade the user experience.

## Nuclear Gate H

This is the comprehensive gate that verifies the entire slice is ready.

```
+------------------------------------------------------------------+
| NUCLEAR GATE H: Before starting next slice, CTO must confirm:    |
| [] "Gherkin audit passed (completeness + quality)"               |
| [] "All tests written by test-writer sub-agents (not coders)"    |
| [] "All Gherkin scenarios pass"                                   |
| [] "All peer reviewers reviewed and approved"                     |
| [] "All QA agents ran and passed"                                 |
| [] "Runtime Log Check completed (Sentry + server + DB logs)"     |
| [] "Whiskey Team ran — all CRITICAL/HIGH findings resolved"      |
| [] "Goal Achievement Test PASSED via agent-browser"               |
| [] "Implicit behavior regression completed (6/6 categories)"     |
| [] "Article 20 architecture standards verified"                   |
| [] "UX Sense Check ran (if frontend slice)"                       |
| [] "Unit test coverage >= 90% on business logic"                  |
| [] "CTO did NOT write any code or test code this slice"           |
| [] "All review artifact files exist on disk"                      |
+------------------------------------------------------------------+
```

## Required Review Artifacts

- `reviews/slice-N-test-spec.md`
- `reviews/slice-N-test-review.md`
- `reviews/slice-N-peer-review.md`
- `reviews/slice-N-qa-swarm.md`
- `reviews/slice-N-red-team-pre-build.md`
- `reviews/slice-N-professor-pre-build.md`
- `reviews/slice-N-whiskey-team.md`
- `reviews/slice-N-ux-sense-check.md` (if frontend)
- `reviews/slice-N-red-team.md` (if escalation in Phase G)
- `reviews/slice-N-professor.md` (if escalation in Phase G)

## Next Phase

Proceed to **Phase I: Documentation** (`phase-i-documentation.md`).
