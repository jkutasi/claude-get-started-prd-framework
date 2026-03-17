# Phase G: Autonomous Fix Verification + Red Team Escalation

> Load this file when starting Phase G. Complete all steps before proceeding to Phase H.

## Purpose

Review autonomous fix results from Phase F, handle escalated fixes, and apply the Autonomous Defect Resolution Protocol for remaining issues.

## Steps

### G.1: Review Autonomous Fix Results

1. CTO reviews all fixes that QA agents applied inline during Phase F.
2. Verify each fix:
   - Does it actually resolve the finding?
   - Did it introduce any new issues?
   - Does it follow Article 20 architecture standards?

### G.2: Handle Escalated Fixes

3. Escalated fixes (architectural, infrastructure, or 3x-failed) are assigned to teammates.
4. Each fix follows the **Autonomous Defect Resolution Protocol** (Article 17e):
   - AUDIT the test → RED (write failing test) → GREEN (fix the code) → REGRESSION (run existing tests) → CLASS SCAN (check similar patterns) → COMMIT.

### G.3: Red Team Escalation (if needed)

5. If a fix has failed 3 autonomous attempts, escalate to Red Team.
6. Red Team verdict: **APPROVE** / **REVISE** / **BLOCK** (Article 14b).
7. Max 3 autonomous fix attempts before Red Team escalation.
8. Artifact (if triggered): `reviews/slice-N-red-team.md`

### G.4: Professor Review (if escalation triggered)

9. Professor Review also runs on aggregate changes during escalation.
10. Artifact (if triggered): `reviews/slice-N-professor.md`

### G.5: Runtime Log Findings

11. Address all CRITICAL findings from Phase F.5 runtime log check.
12. These are real runtime failures — they take priority over hypothetical issues.

## Gate

```
+------------------------------------------------------------------+
| FIX VERIFICATION GATE G: Before proceeding to Phase H:          |
| [] "All autonomous fixes from Phase F verified"                  |
| [] "All escalated fixes resolved by teammates"                   |
| [] "Red Team escalation completed (if triggered)"                |
| [] "Professor Review completed (if triggered)"                   |
| [] "All runtime log findings from F.5 addressed"                 |
| [] "All fixes follow Article 20 architecture standards"          |
+------------------------------------------------------------------+
```

## Next Phase

Proceed to **Phase H: Regression Check** (`phase-h-regression.md`).
