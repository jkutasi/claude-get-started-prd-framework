# CREATION-LOG — two-stage-review

## Problem

Subagents were marking tasks "done" without structured verification.
The CTO had no consistent protocol for accepting or rejecting completed
work — decisions were ad hoc, based on reading the code directly,
which didn't scale and produced inconsistent results. Spec drift and
code quality issues shipped together because there was no separation
between "did you build the right thing" and "did you build it well."

## Observed Failures Before This Skill

- Agent completed implementation, said "done," but had silently dropped
  one of the acceptance criteria because it was "too complex."
- Code quality issues (150-line violations, bare console.log) were only
  caught at the full peer review stage (Phase E), requiring rework after
  integration.
- Scope creep crept in during implementation — extra helper utilities were
  added that were not in the spec, creating undocumented surface area.
- Hardcoded localhost URL shipped in a file that passed code review because
  reviewers were focused on logic, not config hygiene.

## Approaches Tried and Rejected

**Approach: Single combined review.**
Rejected: Mixing "did you build the right thing" with "did you build it
well" produces unfocused reviews. Reviewers anchor on whichever concern
is easiest to find and may miss the other entirely.

**Approach: Code quality review only.**
Rejected: Clean code that solves the wrong problem is still wrong.
Spec compliance must be verified before code quality is even relevant.

**Approach: Reuse the Phase E peer review.**
Rejected: Phase E is multi-model and covers the full slice. This gate
is per-task and runs immediately when an agent reports done, before
integration. They serve different purposes at different scopes.

## Design Decisions

1. Sequential stages, not parallel: Stage 2 only runs if Stage 1 passes.
   No point evaluating code quality if the code doesn't match the spec.
2. Re-submission resets to Stage 1: prevents a situation where an implementer
   fixes Stage 2 issues in a way that breaks Stage 1 compliance.
3. Max 3 cycles before CTO escalation: prevents infinite loops on genuinely
   difficult fixes without requiring manual intervention on every failure.
4. Hardcoded secrets are CRITICAL regardless of other stage 2 results:
   a file with a hardcoded API key that otherwise passes all criteria must
   still result in FAIL.

## Pressure Scenarios This Skill Handles

- "I fixed the tests, can we just ship?" — Stage 1 still runs from scratch.
- "It's mostly right, just one criterion off" — PASS/FAIL only, no partial.
- "The scope creep is small, it's fine" — any unauthorized addition is a
  Stage 1 FAIL. Small scope creep compounds.
- "I'll add tests later" — Stage 2 criterion 5 requires tests to exist before
  the task is marked done.
