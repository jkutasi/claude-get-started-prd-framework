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

Check which of the 8 Whiskey Team testing areas were applicable to this slice. Not every area applies to every slice — mark N/A where the slice has no surface for that test type.

| # | Testing Area | Applied? | Rationale if N/A |
|---|-------------|----------|-----------------|
| 1 | **API Round-Trip Verification** | {YES/N/A} | {WHY_NOT_APPLICABLE_IF_NA} |
| 2 | **API-to-Schema Verification** | {YES/N/A} | {WHY_NOT_APPLICABLE_IF_NA} |
| 3 | **Action Button Verification** | {YES/N/A} | {WHY_NOT_APPLICABLE_IF_NA} |
| 4 | **Frontend Page Verification** | {YES/N/A} | {WHY_NOT_APPLICABLE_IF_NA} |
| 5 | **State Management** | {YES/N/A} | {WHY_NOT_APPLICABLE_IF_NA} |
| 6 | **Early Termination & Partial Completion** | {YES/N/A} | {WHY_NOT_APPLICABLE_IF_NA} |
| 7 | **Data Integrity** | {YES/N/A} | {WHY_NOT_APPLICABLE_IF_NA} |
| 8 | **Goal Achievement Test** | {YES/N/A} | {WHY_NOT_APPLICABLE_IF_NA} |

---

## Goal Achievement Test

> The Goal Achievement Test is the single most important test. It answers: **Can a user complete the full intended workflow from start to finish?** This is a binary PASS/FAIL — there is no partial credit.

| Field | Value |
|-------|-------|
| **Result** | **{PASS / FAIL}** |
| **Goal Tested** | {DESCRIBE_THE_END_TO_END_GOAL — e.g., "User can upload a CSV, see it validated, and receive a summary report"} |
| **Steps Executed** | {NUMBERED_LIST_OF_STEPS_TAKEN} |
| **Evidence** | {SCREENSHOT_PATH, LOG_SNIPPET, OR_DESCRIPTION_OF_OBSERVABLE_OUTCOME} |
| **Failure Point (if FAIL)** | {EXACT_STEP_WHERE_IT_BROKE_AND_WHAT_HAPPENED} |

---

## Findings

> Each finding follows the WHISKEY FINDING format. Findings are adversarial — the Whiskey Team actively tries to break things, not just verify the happy path.

### WHISKEY FINDING #1

| Field | Value |
|-------|-------|
| **Severity** | **{P0 / P1 / P2 / P3}** |
| **Area** | {TESTING_AREA_FROM_SCOPE — e.g., API Round-Trip Verification} |
| **Location** | {FILE_PATH:LINE_NUMBER or UI_LOCATION} |
| **Summary** | {ONE_LINE_DESCRIPTION} |

**What I did:**

1. {STEP_1}
2. {STEP_2}
3. {STEP_N}

**What I expected:**

{WHAT_SHOULD_HAVE_HAPPENED}

**What actually happened:**

{WHAT_ACTUALLY_HAPPENED}

**Evidence:**

```
{LOG_OUTPUT, ERROR_MESSAGE, SCREENSHOT_PATH, OR_DATA_SNIPPET}
```

**Roast:**

> {WHISKEY_TEAM_EDITORIAL — a blunt, honest, one-sentence assessment of why this is unacceptable. The Whiskey Team does not sugarcoat.}

**Resolution:** {FIXED (fix sub-agent resolved) | ESCALATED (architectural/infrastructure) | FAILED (3 attempts, awaiting Red Team)}

**Fix Details:** {IF_FIXED: test file + production file changed, class scan scope. IF_ESCALATED: why. IF_FAILED: what was attempted}

---

### WHISKEY FINDING #2

| Field | Value |
|-------|-------|
| **Severity** | **{P0 / P1 / P2 / P3}** |
| **Area** | {TESTING_AREA_FROM_SCOPE} |
| **Location** | {FILE_PATH:LINE_NUMBER or UI_LOCATION} |
| **Summary** | {ONE_LINE_DESCRIPTION} |

**What I did:**

1. {STEP_1}
2. {STEP_2}
3. {STEP_N}

**What I expected:**

{WHAT_SHOULD_HAVE_HAPPENED}

**What actually happened:**

{WHAT_ACTUALLY_HAPPENED}

**Evidence:**

```
{LOG_OUTPUT, ERROR_MESSAGE, SCREENSHOT_PATH, OR_DATA_SNIPPET}
```

**Roast:**

> {WHISKEY_TEAM_EDITORIAL}

**Resolution:** {FIXED | ESCALATED | FAILED}

**Fix Details:** {DETAILS}

---

### WHISKEY FINDING #N

> Copy the finding block above for each additional finding.

---

## Implicit Behavior Regression Results

> The Whiskey Team checks that existing behavior has not been broken by the new slice. These are things that **should still work** even though they were not part of this slice's scope.

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
| **Medium** | {COUNT} |
| **Low** | {COUNT} |
| **Goal Achievement Test** | **{PASS/FAIL}** |
| **Implicit Regression Checks** | **{X}/6 PASS** |
| **Overall Assessment** | **{PASS — Ship It / REVISE — Fix Before Merge / BLOCK — Do Not Ship}** |

### Whiskey Team Verdict

> {2-3_SENTENCES. Be direct. State whether the slice is ready, what must be fixed, and whether the issues are showstoppers or polish items. The Whiskey Team is the last line of defense before the user sees this code.}

---

## Sign-Off

| Role | Name/Agent | Date |
|------|-----------|------|
| Whiskey Team Lead | {NAME_OR_AGENT} | {YYYY-MM-DD} |
