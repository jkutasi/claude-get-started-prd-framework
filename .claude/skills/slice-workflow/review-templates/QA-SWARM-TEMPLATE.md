# QA Swarm — Slice {SLICE_NUMBER}: {SLICE_NAME}

## Metadata

| Field | Value |
|-------|-------|
| **Date** | {YYYY-MM-DD} |
| **QA Manager** | {QA_MANAGER_AGENT} |
| **Slice Contract** | `contracts/slice-{SLICE_NUMBER}-contract.md` |
| **Build/Branch** | {BRANCH_NAME_OR_COMMIT_HASH} |
| **Prior Reviews Referenced** | {PEER_REVIEW_DATE, RED_TEAM_DATE} |

---

## QA Agent: Stats Verification

| Field | Value |
|-------|-------|
| **Scope** | Numerical accuracy, calculation correctness, data aggregation |
| **Files Reviewed** | {FILE_LIST} |

### Findings

#### STATS-QA-001: {FINDING_TITLE}

| Field | Value |
|-------|-------|
| **Severity** | **{CRITICAL/HIGH/MEDIUM/LOW}** |
| **Net-New?** | {YES/NO} |
| **Attack Vector** | {HOW_THE_AGENT_TRIED_TO_BREAK_IT} |
| **Expected** | {CORRECT_BEHAVIOR} |
| **Actual** | {WHAT_HAPPENED} |
| **Fix Recommendation** | {SPECIFIC_FIX} |

---

## QA Agent: Code Quality

| Field | Value |
|-------|-------|
| **Scope** | Code structure, maintainability, error handling, type safety |
| **Files Reviewed** | {FILE_LIST} |

### Findings

#### CODE-QA-001: {FINDING_TITLE}

| Field | Value |
|-------|-------|
| **Severity** | **{CRITICAL/HIGH/MEDIUM/LOW}** |
| **Net-New?** | {YES/NO} |
| **Category** | {ERROR_HANDLING / TYPE_SAFETY / MAINTAINABILITY / STANDARDS} |
| **File:Line** | `{FILE_PATH}:{LINE_NUMBER}` |
| **Issue** | {DESCRIPTION} |
| **Fix Recommendation** | {SPECIFIC_FIX} |

---

## QA Agent: Data Integrity

| Field | Value |
|-------|-------|
| **Scope** | Data flow, persistence, transformation accuracy, schema validation |
| **Files Reviewed** | {FILE_LIST} |

### Findings

#### DATA-QA-001: {FINDING_TITLE}

| Field | Value |
|-------|-------|
| **Severity** | **{CRITICAL/HIGH/MEDIUM/LOW}** |
| **Net-New?** | {YES/NO} |
| **Data Path** | {SOURCE -> TRANSFORMATION -> DESTINATION} |
| **Attack Vector** | {HOW_DATA_INTEGRITY_WAS_TESTED} |
| **Fix Recommendation** | {SPECIFIC_FIX} |

---

## QA Agent: Security

| Field | Value |
|-------|-------|
| **Scope** | Auth, input sanitization, secrets management, dependency vulnerabilities |
| **Files Reviewed** | {FILE_LIST} |

### Findings

#### SEC-QA-001: {FINDING_TITLE}

| Field | Value |
|-------|-------|
| **Severity** | **{CRITICAL/HIGH/MEDIUM/LOW}** |
| **Net-New?** | {YES/NO} |
| **OWASP Category** | {IF_APPLICABLE} |
| **Attack Vector** | {HOW_THE_VULNERABILITY_WAS_TESTED} |
| **Impact** | {WHAT_COULD_HAPPEN_IF_EXPLOITED} |
| **Fix Recommendation** | {SPECIFIC_FIX} |

---

## QA Agent: UI/UX Browser Testing

| Field | Value |
|-------|-------|
| **Scope** | Visual rendering, responsiveness, accessibility, interaction correctness |
| **Pages Tested** | {PAGE_LIST} |

### Findings

#### UI-QA-001: {FINDING_TITLE}

| Field | Value |
|-------|-------|
| **Severity** | **{CRITICAL/HIGH/MEDIUM/LOW}** |
| **Net-New?** | {YES/NO} |
| **Category** | {RENDERING / RESPONSIVENESS / ACCESSIBILITY / INTERACTION} |
| **Steps to Reproduce** | {NUMBERED_STEPS} |
| **Fix Recommendation** | {SPECIFIC_FIX} |

---

## QA Manager Synthesis

### Prioritized Fix Plan

| Priority | ID | Finding | Agent | Severity | Net-New? | Status |
|----------|----|---------|-------|----------|----------|--------|
| 1 | {ID} | {FINDING_SUMMARY} | {AGENT} | {SEVERITY} | {YES/NO} | {OPEN/FIXED/DEFERRED} |

### Overall Metrics

| Metric | Value |
|--------|-------|
| **Total Findings** | {COUNT} |
| **Net-New Findings** | {COUNT} |
| **Critical** | {COUNT} |
| **High** | {COUNT} |
| **QA Verdict** | **{PASS / PASS_WITH_FIXES / FAIL}** |

---

## Sign-Off

| Role | Name/Agent | Date |
|------|-----------|------|
| QA Manager | {NAME_OR_AGENT} | {YYYY-MM-DD} |
