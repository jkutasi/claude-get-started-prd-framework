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
| **Trigger** | {WHAT_TRIGGERED_THIS_REVIEW} |

---

## Attack Dimension Ratings

Rate each dimension **1-5** (1=solid, 5=critical/BLOCK).

| # | Attack Dimension | Rating | Findings |
|---|-----------------|--------|----------|
| 1 | **Wrong Assumptions** | {1-5} | {FINDINGS} |
| 2 | **Scaling Failures** | {1-5} | {FINDINGS} |
| 3 | **Dependency Risks** | {1-5} | {FINDINGS} |
| 4 | **Simpler Alternatives** | {1-5} | {FINDINGS} |
| 5 | **Missing Edge Cases** | {1-5} | {FINDINGS} |
| 6 | **Security Gaps** | {1-5} | {FINDINGS} |
| 7 | **Cost Spirals** | {1-5} | {FINDINGS} |
| 8 | **Integration Fragility** | {1-5} | {FINDINGS} |
| 9 | **Completeness Gaps** | {1-5} | {FINDINGS} |
| 10 | **Wrong Tool for Job** | {1-5} | {FINDINGS} |

**Average Rating:** {AVERAGE}
**Highest Risk Dimensions:** {LIST_DIMENSIONS_RATED_4_OR_5}

---

## External Model Hostile Review

### Prompt Given

```
{PASTE_THE_EXACT_PROMPT_SENT_TO_THE_EXTERNAL_MODEL}
```

### External Model Response

```
{PASTE_THE_FULL_UNEDITED_RESPONSE}
```

### Assessment of External Model Findings

| Finding from External Model | Valid? | Already Covered? | Action Required |
|----------------------------|--------|-----------------|-----------------|
| {FINDING_1} | {YES/NO/PARTIAL} | {YES/NO} | {ACTION_OR_N/A} |

---

## Verdict

> **{APPROVE / REVISE / BLOCK}**

| Verdict | Meaning |
|---------|---------|
| **APPROVE** | All dimensions rated 1-2. Risks acceptable. |
| **REVISE** | One or more dimensions rated 3-4. Must address before proceeding. |
| **BLOCK** | Any dimension rated 5. MUST NOT proceed as designed. |

### Rationale

{EXPLAIN_THE_VERDICT_IN_2-3_SENTENCES.}

---

## Required Actions

| # | Action | Dimension | Priority | Owner | Status |
|---|--------|-----------|----------|-------|--------|
| 1 | {FIX_REQUIRED} | {DIMENSION} | {PRIORITY} | {OWNER} | {STATUS} |

---

## Escalation History

> Complete for QA Escalation reviews. Remove for Pre-Build Gate reviews.

| Iteration | Date | Fix Attempted | Files Changed | Red Team Response | Remaining Issues |
|-----------|------|--------------|---------------|-------------------|-----------------|
| 1 | {YYYY-MM-DD} | {DESCRIPTION} | {FILE_LIST} | {PASS/STILL_FAILING} | {LIST_OR_NONE} |

---

## Sign-Off

| Role | Name/Agent | Date | Signature |
|------|-----------|------|-----------|
| Red Team Lead | {NAME_OR_AGENT} | {YYYY-MM-DD} | {APPROVED/REJECTED} |
| CTO / Project Lead | {NAME_OR_AGENT} | {YYYY-MM-DD} | {ACKNOWLEDGED/OVERRIDE} |
