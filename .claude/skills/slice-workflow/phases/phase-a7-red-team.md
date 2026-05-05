# Phase A.7: Red Team + Professor Pre-Build Gate (OPTIONAL — --high-risk only)

> Load this file ONLY when the slice is flagged --high-risk. Default: SKIP this phase.
> If not --high-risk, proceed directly to Phase B.

## Purpose

Adversarial review of the user-confirmed slice plan before any tests or code are written.
Both reviews run in parallel: Red Team and Professor Review.

## When to Run

Only when any of the following apply:
- Slice touches authentication, payments, or PII handling
- Slice introduces a new external integration
- Slice has been explicitly flagged --high-risk by the project owner

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

- **REVISE:** Address required actions, then re-submit for review.
- **BLOCK:** Implementation MUST NOT proceed as designed. Max 3 iterations, then escalate.

## Gate (only checked if --high-risk)

```
+------------------------------------------------------------------+
| A.7 GATE (--high-risk only): Before proceeding to Phase B:       |
| [] "Red Team returned verdict: APPROVE or REVISE"                |
| [] "Professor Review returned verdict: APPROVE or REVISE"        |
| [] "reviews/slice-N-red-team-pre-build.md EXISTS on disk"        |
| [] "reviews/slice-N-professor-pre-build.md EXISTS on disk"       |
+------------------------------------------------------------------+
```

## Next Phase

Proceed to **Phase B: Test Specification** (`phase-b-test-spec.md`).
