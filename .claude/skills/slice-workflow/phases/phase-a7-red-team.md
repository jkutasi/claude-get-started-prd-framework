# Phase A.7: Red Team + Professor Pre-Build Gate

> Load this file when starting Phase A.7. Both reviews run in parallel. Complete all steps and both gates before proceeding to Phase B.

## Purpose

Adversarial review of the user-confirmed slice plan before any tests or code are written. Two independent reviews run in parallel: Red Team and Professor Review.

## Red Team Review

1. QA Lead spawns the Red Team Reviewer on the user-confirmed slice plan.
2. Red Team evaluates 10 attack dimensions (see `review-templates/RED-TEAM-REVIEW-TEMPLATE.md`).
3. Red Team sends the plan to `{EXTERNAL_MODEL}` with a hostile prompt.
4. Verdict: **APPROVE** / **REVISE** / **BLOCK**.
5. If **BLOCK**: cannot proceed. Max 3 iterations before owner escalation.
6. Artifact: `reviews/slice-N-red-team-pre-build.md`

## Professor Review (runs in parallel with Red Team)

7. Professors evaluate architecture, testing strategy, security posture, etc.
8. CTO selects relevant professors (minimum 2) for this slice's domain.
9. See `review-templates/PROFESSOR-REVIEW-TEMPLATE.md` for the output format.
10. Verdict: **APPROVE** / **REVISE** / **BLOCK**.
11. Artifact: `reviews/slice-N-professor-pre-build.md`

## Handling REVISE or BLOCK

- **REVISE:** Address the required actions listed in the review, then re-submit for review.
- **BLOCK:** Implementation MUST NOT proceed as designed. Max 3 iterations. If still blocked after 3, escalate to the project owner.

## Red Team Gate

```
+------------------------------------------------------------------+
| RED TEAM GATE: Before proceeding, CTO must confirm:              |
| [] "Red Team Reviewer returned verdict: APPROVE or REVISE"       |
| [] "reviews/slice-N-red-team-pre-build.md EXISTS on disk"        |
| [] "Verdict is NOT BLOCK (or BLOCK findings were addressed)"     |
+------------------------------------------------------------------+
```

## Professor Gate

```
+------------------------------------------------------------------+
| PROFESSOR GATE: Before proceeding, CTO must confirm:             |
| [] "Professor Review returned verdict: APPROVE or REVISE"        |
| [] "reviews/slice-N-professor-pre-build.md EXISTS on disk"       |
| [] "Verdict is NOT BLOCK (or BLOCK findings were addressed)"     |
+------------------------------------------------------------------+
```

## Next Phase

Proceed to **Phase B: Test Specification** (`phase-b-test-spec.md`).
