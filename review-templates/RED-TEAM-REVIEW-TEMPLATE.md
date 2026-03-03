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

Rate each dimension as **PASS**, **CONCERN**, or **FAIL**.

- **PASS** — No exploitable weakness found. Resilient under adversarial probing.
- **CONCERN** — Minor weakness or ambiguity that could become exploitable. Requires monitoring or minor fix.
- **FAIL** — Exploitable weakness confirmed. Must be resolved before approval.

| # | Attack Dimension | Rating | Findings |
|---|-----------------|--------|----------|
| 1 | **Input Validation & Injection** | {PASS/CONCERN/FAIL} | {Describe attempts to inject malicious input, SQL injection, XSS, command injection. What was tried, what happened.} |
| 2 | **Authentication & Authorization Bypass** | {PASS/CONCERN/FAIL} | {Describe attempts to access resources without proper auth, privilege escalation, token manipulation.} |
| 3 | **Data Leakage & Exposure** | {PASS/CONCERN/FAIL} | {Describe checks for sensitive data in logs, responses, error messages, URLs, local storage.} |
| 4 | **Business Logic Abuse** | {PASS/CONCERN/FAIL} | {Describe attempts to exploit business rules — duplicate submissions, race conditions, workflow skipping.} |
| 5 | **Error Handling & Information Disclosure** | {PASS/CONCERN/FAIL} | {Describe what happens when things break — stack traces exposed, verbose errors, unhandled exceptions.} |
| 6 | **Dependency & Supply Chain** | {PASS/CONCERN/FAIL} | {Describe checks for known CVEs, outdated packages, typosquatting, pinned versions.} |
| 7 | **Configuration & Secrets Management** | {PASS/CONCERN/FAIL} | {Describe checks for hardcoded secrets, default credentials, debug flags in production config.} |
| 8 | **Rate Limiting & Resource Exhaustion** | {PASS/CONCERN/FAIL} | {Describe attempts to overwhelm endpoints, large payloads, infinite loops, memory exhaustion.} |
| 9 | **State Management & Session Integrity** | {PASS/CONCERN/FAIL} | {Describe attempts to tamper with state, replay attacks, session fixation, CSRF.} |
| 10 | **Contract & Specification Deviation** | {PASS/CONCERN/FAIL} | {Describe deviations from the slice contract — missing acceptance criteria, undocumented behavior, scope creep.} |

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
| **APPROVE** | All dimensions PASS or CONCERN-only with documented mitigations. Safe to proceed. |
| **REVISE** | One or more CONCERN ratings require fixes before next gate. No FAIL ratings. |
| **BLOCK** | One or more FAIL ratings. Slice cannot proceed until failures are resolved and re-reviewed. |

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
