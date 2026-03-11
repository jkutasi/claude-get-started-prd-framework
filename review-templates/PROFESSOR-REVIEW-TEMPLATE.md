# Professor Review — Slice {SLICE_NUMBER}: {SLICE_NAME}

## Context

| Field | Value |
|-------|-------|
| **Review Type** | {PRE_BUILD_GATE / QA_ESCALATION} |
| **Date** | {YYYY-MM-DD} |
| **Professors Activated** | {LIST_OF_PROFESSORS — e.g., Architecture, Testing, Security, Code Craft} |
| **Slice Contract** | `contracts/slice-{SLICE_NUMBER}-contract.md` |
| **Code Under Review** | {FILES_OR_MODULES_REVIEWED} |
| **Trigger** | {WHAT_TRIGGERED_THIS_REVIEW — e.g., pre-build gate, QA escalation, on-demand} |

---

## Professor Selection

> Not all professors are needed for every slice. The CTO selects professors relevant to the slice's domain. Minimum 2 professors per review.

| Professor | Activated | Rationale |
|-----------|-----------|-----------|
| Architecture | {YES/NO} | {WHY — e.g., "New module boundaries introduced"} |
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

> Each activated professor produces findings in the standard format below. Every finding includes a Teaching Note with a book reference — this is the key differentiator from other review types.

### {PROFESSOR_NAME} — Findings

#### FINDING #{NUMBER}

- **Severity:** P0 (blocking) | P1 (high) | P2 (medium) | P3 (low)
- **Category:** {DOMAIN_SPECIFIC_CATEGORY}
- **File:Line:** {FILE_PATH}:{LINE_NUMBER}
- **Issue:** {WHAT_IS_WRONG}
- **Principle Violated:** {NAME_OF_PRINCIPLE}
- **Book Reference:** {BOOK_TITLE}, {CHAPTER_OR_CONCEPT}
- **Teaching Note:** {WHY_THIS_PRINCIPLE_EXISTS — explain the reasoning, connect to the book's teaching. Help the reader understand not just what to fix, but what to think about differently.}
- **Recommendation:** {HOW_TO_FIX}

> Repeat the finding block for each finding. Repeat the professor section for each activated professor.

---

## Findings Summary

| Professor | Findings | P0 | P1 | P2 | P3 |
|-----------|----------|----|----|----|----|
| {PROFESSOR_1} | {COUNT} | {COUNT} | {COUNT} | {COUNT} | {COUNT} |
| {PROFESSOR_2} | {COUNT} | {COUNT} | {COUNT} | {COUNT} | {COUNT} |
| {PROFESSOR_N} | {COUNT} | {COUNT} | {COUNT} | {COUNT} | {COUNT} |
| **Total** | **{TOTAL}** | **{TOTAL}** | **{TOTAL}** | **{TOTAL}** | **{TOTAL}** |

### Consensus Findings

> Issues flagged by 2+ professors are mandatory fixes (same consensus rule as peer review).

| # | Issue | Professors | Severity | Status |
|---|-------|------------|----------|--------|
| 1 | {ISSUE_DESCRIPTION} | {PROFESSOR_1, PROFESSOR_2} | {P0/P1/P2/P3} | {OPEN/FIXED} |
| N | {ISSUE_DESCRIPTION} | {PROFESSOR_LIST} | {P0/P1/P2/P3} | {OPEN/FIXED} |

---

## Verdict

> **{APPROVE / REVISE / BLOCK}**

| Verdict | Meaning |
|---------|---------|
| **APPROVE** | No P0 findings. All consensus findings addressed. Proceed. |
| **REVISE** | P1 or consensus findings exist. Must address required actions before proceeding. |
| **BLOCK** | P0 findings exist. Implementation MUST NOT proceed as designed. Owner override required. |

### Rationale

{EXPLAIN_THE_VERDICT_IN_2-3_SENTENCES. Reference specific professor findings and book principles that drove the decision.}

---

## Required Actions

> Complete this section if verdict is **REVISE** or **BLOCK**. Remove if **APPROVE**.

| # | Action | Professor | Book Reference | Priority | Owner | Status |
|---|--------|-----------|---------------|----------|-------|--------|
| 1 | {DESCRIBE_SPECIFIC_FIX_REQUIRED} | {PROFESSOR_NAME} | {BOOK, CHAPTER} | {CRITICAL/HIGH/MEDIUM} | {AGENT_OR_PERSON} | {OPEN/IN_PROGRESS/RESOLVED} |
| N | {DESCRIBE_SPECIFIC_FIX_REQUIRED} | {PROFESSOR_NAME} | {BOOK, CHAPTER} | {CRITICAL/HIGH/MEDIUM} | {AGENT_OR_PERSON} | {OPEN/IN_PROGRESS/RESOLVED} |

---

## Sign-Off

| Role | Name/Agent | Date | Signature |
|------|-----------|------|-----------|
| Professor Review Lead | {NAME_OR_AGENT} | {YYYY-MM-DD} | {APPROVED/REJECTED} |
| CTO / Project Lead | {NAME_OR_AGENT} | {YYYY-MM-DD} | {ACKNOWLEDGED/OVERRIDE} |
