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
| 1 | **Goal Achievement (End-to-End)** | {YES/N/A} | {WHY_NOT_APPLICABLE_IF_NA} |
| 2 | **Input Boundary Testing** | {YES/N/A} | {WHY_NOT_APPLICABLE_IF_NA} |
| 3 | **Error Path Validation** | {YES/N/A} | {WHY_NOT_APPLICABLE_IF_NA} |
| 4 | **Data Integrity Verification** | {YES/N/A} | {WHY_NOT_APPLICABLE_IF_NA} |
| 5 | **Performance Under Load** | {YES/N/A} | {WHY_NOT_APPLICABLE_IF_NA} |
| 6 | **State Transition Correctness** | {YES/N/A} | {WHY_NOT_APPLICABLE_IF_NA} |
| 7 | **Integration Point Testing** | {YES/N/A} | {WHY_NOT_APPLICABLE_IF_NA} |
| 8 | **Implicit Behavior Regression** | {YES/N/A} | {WHY_NOT_APPLICABLE_IF_NA} |

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
| **Severity** | **{CRITICAL / HIGH / MEDIUM / LOW}** |
| **Area** | {TESTING_AREA_FROM_SCOPE — e.g., Input Boundary Testing} |
| **Summary** | {ONE_LINE_DESCRIPTION} |

**Steps to Reproduce:**

1. {STEP_1}
2. {STEP_2}
3. {STEP_N}

**Expected Result:**

{WHAT_SHOULD_HAVE_HAPPENED}

**Actual Result:**

{WHAT_ACTUALLY_HAPPENED}

**Evidence:**

```
{LOG_OUTPUT, ERROR_MESSAGE, SCREENSHOT_PATH, OR_DATA_SNIPPET}
```

**Roast:**

> {WHISKEY_TEAM_EDITORIAL — a blunt, honest, one-sentence assessment of why this is unacceptable. The Whiskey Team does not sugarcoat.}

---

### WHISKEY FINDING #2

| Field | Value |
|-------|-------|
| **Severity** | **{CRITICAL / HIGH / MEDIUM / LOW}** |
| **Area** | {TESTING_AREA_FROM_SCOPE} |
| **Summary** | {ONE_LINE_DESCRIPTION} |

**Steps to Reproduce:**

1. {STEP_1}
2. {STEP_2}
3. {STEP_N}

**Expected Result:**

{WHAT_SHOULD_HAVE_HAPPENED}

**Actual Result:**

{WHAT_ACTUALLY_HAPPENED}

**Evidence:**

```
{LOG_OUTPUT, ERROR_MESSAGE, SCREENSHOT_PATH, OR_DATA_SNIPPET}
```

**Roast:**

> {WHISKEY_TEAM_EDITORIAL}

---

### WHISKEY FINDING #N

> Copy the finding block above for each additional finding.

---

## Implicit Behavior Regression Results

> The Whiskey Team checks that existing behavior has not been broken by the new slice. These are things that **should still work** even though they were not part of this slice's scope.

| # | Regression Category | Result | Findings |
|---|-------------------|--------|----------|
| 1 | **Existing pages/routes still load** | {PASS/FAIL} | {DESCRIPTION_OR_NONE} |
| 2 | **Existing data is not corrupted or lost** | {PASS/FAIL} | {DESCRIPTION_OR_NONE} |
| 3 | **Existing API endpoints still respond correctly** | {PASS/FAIL} | {DESCRIPTION_OR_NONE} |
| 4 | **No new console errors or warnings** | {PASS/FAIL} | {DESCRIPTION_OR_NONE} |
| 5 | **No performance degradation on existing features** | {PASS/FAIL} | {DESCRIPTION_OR_NONE} |
| 6 | **Authentication and authorization unchanged** | {PASS/FAIL} | {DESCRIPTION_OR_NONE} |

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
