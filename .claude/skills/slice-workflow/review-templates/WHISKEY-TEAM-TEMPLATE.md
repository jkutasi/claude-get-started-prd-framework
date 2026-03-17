# Whiskey Team Report — Slice {SLICE_NUMBER}: {SLICE_NAME}

## Metadata

| Field | Value |
|-------|-------|
| **Date** | {YYYY-MM-DD} |
| **Tester** | {TESTER_NAME_OR_AGENT} |
| **Slice Contract** | `contracts/slice-{SLICE_NUMBER}-contract.md` |
| **Build/Branch** | {BRANCH_NAME_OR_COMMIT_HASH} |
| **Environment** | {LOCAL/STAGING/PRODUCTION} |

---

## Testing Scope Applied

| # | Testing Area | Applied? | Rationale if N/A |
|---|-------------|----------|-----------------|
| 1 | **API Round-Trip Verification** | {YES/N/A} | {WHY} |
| 2 | **API-to-Schema Verification** | {YES/N/A} | {WHY} |
| 3 | **Action Button Verification** | {YES/N/A} | {WHY} |
| 4 | **Frontend Page Verification** | {YES/N/A} | {WHY} |
| 5 | **State Management** | {YES/N/A} | {WHY} |
| 6 | **Early Termination & Partial Completion** | {YES/N/A} | {WHY} |
| 7 | **Data Integrity** | {YES/N/A} | {WHY} |
| 8 | **Goal Achievement Test** | {YES/N/A} | {WHY} |

---

## Goal Achievement Test

| Field | Value |
|-------|-------|
| **Result** | **{PASS / FAIL}** |
| **Goal Tested** | {END_TO_END_GOAL_DESCRIPTION} |
| **Steps Executed** | {NUMBERED_LIST} |
| **Evidence** | {SCREENSHOT_PATH_OR_LOG_SNIPPET} |
| **Failure Point (if FAIL)** | {EXACT_STEP_AND_WHAT_HAPPENED} |

---

## Findings

### WHISKEY FINDING #1

| Field | Value |
|-------|-------|
| **Severity** | **{P0 / P1 / P2 / P3}** |
| **Area** | {TESTING_AREA} |
| **Location** | {FILE_PATH:LINE_NUMBER or UI_LOCATION} |
| **Summary** | {ONE_LINE_DESCRIPTION} |

**What I did:** {NUMBERED_STEPS}
**What I expected:** {EXPECTED}
**What actually happened:** {ACTUAL}
**Evidence:** `{LOG_OR_DATA}`
**Roast:** > {BLUNT_ASSESSMENT}
**Resolution:** {FIXED | ESCALATED | FAILED}
**Fix Details:** {DETAILS}

> Repeat finding block for each additional finding.

---

## Implicit Behavior Regression Results

| # | Regression Category | Result | Findings |
|---|-------------------|--------|----------|
| 1 | **State Transition Gaps** | {PASS/FAIL} | {DESCRIPTION_OR_NONE} |
| 2 | **Cross-Component Interactions** | {PASS/FAIL} | {DESCRIPTION_OR_NONE} |
| 3 | **Data Flow Assumptions** | {PASS/FAIL} | {DESCRIPTION_OR_NONE} |
| 4 | **Race Conditions** | {PASS/FAIL} | {DESCRIPTION_OR_NONE} |
| 5 | **Silent Failures** | {PASS/FAIL} | {DESCRIPTION_OR_NONE} |
| 6 | **Edge Case Combinations** | {PASS/FAIL} | {DESCRIPTION_OR_NONE} |

---

## Summary

| Metric | Value |
|--------|-------|
| **Total Findings** | {COUNT} |
| **Critical** | {COUNT} |
| **High** | {COUNT} |
| **Goal Achievement Test** | **{PASS/FAIL}** |
| **Implicit Regression Checks** | **{X}/6 PASS** |
| **Overall Assessment** | **{PASS / REVISE / BLOCK}** |

### Whiskey Team Verdict

> {2-3_SENTENCES. Be direct.}

---

## Sign-Off

| Role | Name/Agent | Date |
|------|-----------|------|
| Whiskey Team Lead | {NAME_OR_AGENT} | {YYYY-MM-DD} |
