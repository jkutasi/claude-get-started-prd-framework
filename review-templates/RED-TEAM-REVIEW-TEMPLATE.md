# Red Team Review — Slice {SLICE_NUMBER}: {SLICE_NAME}

## Context

| Field | Value |
|-------|-------|
| **Review Type** | {PRE_BUILD_GATE / QA_ESCALATION} |
| **Date** | {YYYY-MM-DD} |
| **Reviewer** | {REVIEWER_NAME_OR_AGENT} |
| **External Model Used** | {EXTERNAL_MODEL_NAME_AND_VERSION} |
| **Slice Contract** | `contracts/slice-{SLICE_NUMBER}-contract.md` |
| **Code Under Review** | {FILES_OR_MODULES_REVIEWED} |
| **Trigger** | {WHAT_TRIGGERED_THIS_REVIEW — e.g., pre-build gate, QA iteration failure, manual escalation} |

---

## Attack Dimension Ratings

Rate each dimension **1-5**.

- **1** — No concern. Solid.
- **2** — Minor concern. Acceptable risk.
- **3** — Moderate concern. Should be addressed but not blocking.
- **4** — Serious concern. Must be addressed before proceeding.
- **5** — Critical. This will fail. BLOCK.

| # | Attack Dimension | Rating | Findings |
|---|-----------------|--------|----------|
| 1 | **Wrong Assumptions** | {1-5} | {What is this plan assuming that might not be true? What "obvious" things are actually unverified?} |
| 2 | **Scaling Failures** | {1-5} | {What breaks at 10x load? 100x data? What is O(n^2) hiding in this design?} |
| 3 | **Dependency Risks** | {1-5} | {What external services, libraries, or APIs could fail, change, or disappear? What has no fallback?} |
| 4 | **Simpler Alternatives** | {1-5} | {Is this overengineered? Could a simpler approach achieve 90% of the value at 10% of the complexity?} |
| 5 | **Missing Edge Cases** | {1-5} | {What inputs, states, or sequences were not considered? What happens at boundaries?} |
| 6 | **Security Gaps** | {1-5} | {What attack surfaces are exposed? What is not validated, not sanitized, not authenticated?} |
| 7 | **Cost Spirals** | {1-5} | {What could cause costs to grow unexpectedly? Unbounded queries, unthrottled API calls, storage bloat?} |
| 8 | **Integration Fragility** | {1-5} | {How tightly coupled is this to other components? What breaks when an adjacent system changes?} |
| 9 | **Completeness Gaps** | {1-5} | {What was promised in the spec but not addressed in the plan? What was hand-waved?} |
| 10 | **Wrong Tool for Job** | {1-5} | {Is the chosen technology/pattern/library the right one? Or was it chosen out of familiarity, not fitness?} |

**Average Rating:** {AVERAGE}
**Highest Risk Dimensions:** {LIST_DIMENSIONS_RATED_4_OR_5}

---

## External Model Hostile Review

> The following is the unedited response from **{EXTERNAL_MODEL_NAME_AND_VERSION}** when given the slice code/contract and prompted to find weaknesses, attack vectors, and failure modes.

### Prompt Given

```
{PASTE_THE_EXACT_PROMPT_SENT_TO_THE_EXTERNAL_MODEL}
```

### External Model Response

```
{PASTE_THE_FULL_UNEDITED_RESPONSE_FROM_THE_EXTERNAL_MODEL}
```

### Assessment of External Model Findings

| Finding from External Model | Valid? | Already Covered? | Action Required |
|----------------------------|--------|-----------------|-----------------|
| {FINDING_1} | {YES/NO/PARTIAL} | {YES — dimension #X / NO} | {DESCRIBE_ACTION_OR_N/A} |
| {FINDING_2} | {YES/NO/PARTIAL} | {YES — dimension #X / NO} | {DESCRIBE_ACTION_OR_N/A} |
| {FINDING_N} | {YES/NO/PARTIAL} | {YES — dimension #X / NO} | {DESCRIBE_ACTION_OR_N/A} |

---

## Verdict

> **{APPROVE / REVISE / BLOCK}**

| Verdict | Meaning |
|---------|---------|
| **APPROVE** | All dimensions rated 1-2. Risks are acceptable. Proceed. |
| **REVISE** | One or more dimensions rated 3-4. Must address required actions before proceeding. |
| **BLOCK** | Any dimension rated 5. Implementation MUST NOT proceed as designed. Owner override required. |

### Rationale

{EXPLAIN_THE_VERDICT_IN_2-3_SENTENCES. Reference specific dimensions and findings that drove the decision.}

---

## Required Actions

> Complete this section if verdict is **REVISE** or **BLOCK**. Remove if **APPROVE**.

| # | Action | Dimension | Priority | Owner | Status |
|---|--------|-----------|----------|-------|--------|
| 1 | {DESCRIBE_SPECIFIC_FIX_REQUIRED} | {DIMENSION_NUMBER_AND_NAME} | {CRITICAL/HIGH/MEDIUM} | {AGENT_OR_PERSON} | {OPEN/IN_PROGRESS/RESOLVED} |
| 2 | {DESCRIBE_SPECIFIC_FIX_REQUIRED} | {DIMENSION_NUMBER_AND_NAME} | {CRITICAL/HIGH/MEDIUM} | {AGENT_OR_PERSON} | {OPEN/IN_PROGRESS/RESOLVED} |
| N | {DESCRIBE_SPECIFIC_FIX_REQUIRED} | {DIMENSION_NUMBER_AND_NAME} | {CRITICAL/HIGH/MEDIUM} | {AGENT_OR_PERSON} | {OPEN/IN_PROGRESS/RESOLVED} |

---

## Escalation History

> Complete this section when review type is **QA Escalation**. This tracks the fix-review cycle. Remove if this is a Pre-Build Gate review.

| Iteration | Date | Fix Attempted | Files Changed | Red Team Response | Remaining Issues |
|-----------|------|--------------|---------------|-------------------|-----------------|
| 1 | {YYYY-MM-DD} | {DESCRIBE_WHAT_WAS_FIXED} | {FILE_LIST} | {PASS/STILL_FAILING — summary} | {LIST_OR_NONE} |
| 2 | {YYYY-MM-DD} | {DESCRIBE_WHAT_WAS_FIXED} | {FILE_LIST} | {PASS/STILL_FAILING — summary} | {LIST_OR_NONE} |
| N | {YYYY-MM-DD} | {DESCRIBE_WHAT_WAS_FIXED} | {FILE_LIST} | {PASS/STILL_FAILING — summary} | {LIST_OR_NONE} |

---

## Sign-Off

| Role | Name/Agent | Date | Signature |
|------|-----------|------|-----------|
| Red Team Lead | {NAME_OR_AGENT} | {YYYY-MM-DD} | {APPROVED/REJECTED} |
| CTO / Project Lead | {NAME_OR_AGENT} | {YYYY-MM-DD} | {ACKNOWLEDGED/OVERRIDE} |
