# Professor Review — Slice {SLICE_NUMBER}: {SLICE_NAME}

## Context

| Field | Value |
|-------|-------|
| **Review Type** | {PRE_BUILD_GATE / QA_ESCALATION} |
| **Date** | {YYYY-MM-DD} |
| **Professors Activated** | {LIST_OF_PROFESSORS} |
| **Slice Contract** | `contracts/slice-{SLICE_NUMBER}-contract.md` |
| **Code Under Review** | {FILES_OR_MODULES_REVIEWED} |
| **Trigger** | {WHAT_TRIGGERED_THIS_REVIEW} |

---

## Professor Selection

> Minimum 2 professors per review. Select those relevant to the slice's domain.

| Professor | Activated | Rationale |
|-----------|-----------|-----------|
| Architecture | {YES/NO} | {WHY} |
| Testing | {YES/NO} | {WHY} |
| Security | {YES/NO} | {WHY} |
| Code Craft | {YES/NO} | {WHY} |
| Observability | {YES/NO} | {WHY} |
| Data | {YES/NO} | {WHY} |
| Performance | {YES/NO} | {WHY} |
| DevOps | {YES/NO} | {WHY} |
| Refactoring | {YES/NO} | {WHY} |
| API Design | {YES/NO} | {WHY} |
| Frontend | {YES/NO} | {WHY} |
| Resilience | {YES/NO} | {WHY} |
| Distributed Systems | {YES/NO} | {WHY} |
| Functional Design | {YES/NO} | {WHY} |
| UX Engineering | {YES/NO} | {WHY} |

---

## Professor Findings

### {PROFESSOR_NAME} — Findings

#### FINDING #{NUMBER}

- **Severity:** P0 (blocking) | P1 (high) | P2 (medium) | P3 (low)
- **Category:** {DOMAIN_SPECIFIC_CATEGORY}
- **File:Line:** {FILE_PATH}:{LINE_NUMBER}
- **Issue:** {WHAT_IS_WRONG}
- **Principle Violated:** {NAME_OF_PRINCIPLE}
- **Book Reference:** {BOOK_TITLE}, {CHAPTER_OR_CONCEPT}
- **Teaching Note:** {WHY_THIS_PRINCIPLE_EXISTS}
- **Recommendation:** {HOW_TO_FIX}

> Repeat finding block per finding. Repeat professor section per activated professor.

---

## Findings Summary

| Professor | Findings | P0 | P1 | P2 | P3 |
|-----------|----------|----|----|----|----|
| {PROFESSOR_1} | {COUNT} | {COUNT} | {COUNT} | {COUNT} | {COUNT} |
| **Total** | **{TOTAL}** | **{TOTAL}** | **{TOTAL}** | **{TOTAL}** | **{TOTAL}** |

### Consensus Findings

> Issues flagged by 2+ professors are mandatory fixes.

| # | Issue | Professors | Severity | Status |
|---|-------|------------|----------|--------|
| 1 | {ISSUE_DESCRIPTION} | {PROFESSOR_LIST} | {P0/P1/P2/P3} | {OPEN/FIXED} |

---

## Verdict

> **{APPROVE / REVISE / BLOCK}**

| Verdict | Meaning |
|---------|---------|
| **APPROVE** | No P0 findings. All consensus findings addressed. |
| **REVISE** | P1 or consensus findings exist. Must address before proceeding. |
| **BLOCK** | P0 findings exist. MUST NOT proceed as designed. |

### Rationale

{EXPLAIN_THE_VERDICT_IN_2-3_SENTENCES.}

---

## Required Actions

| # | Action | Professor | Book Reference | Priority | Owner | Status |
|---|--------|-----------|---------------|----------|-------|--------|
| 1 | {FIX_REQUIRED} | {PROFESSOR} | {BOOK, CHAPTER} | {PRIORITY} | {OWNER} | {STATUS} |

---

## Sign-Off

| Role | Name/Agent | Date | Signature |
|------|-----------|------|-----------|
| Professor Review Lead | {NAME_OR_AGENT} | {YYYY-MM-DD} | {APPROVED/REJECTED} |
| CTO / Project Lead | {NAME_OR_AGENT} | {YYYY-MM-DD} | {ACKNOWLEDGED/OVERRIDE} |
