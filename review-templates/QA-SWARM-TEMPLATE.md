# QA Swarm — Slice {SLICE_NUMBER}: {SLICE_NAME}

## Metadata

| Field | Value |
|-------|-------|
| **Date** | {YYYY-MM-DD} |
| **QA Manager** | {QA_MANAGER_AGENT} |
| **Slice Contract** | `contracts/slice-{SLICE_NUMBER}-contract.md` |
| **Build/Branch** | {BRANCH_NAME_OR_COMMIT_HASH} |
| **Prior Reviews Referenced** | {PEER_REVIEW_DATE, RED_TEAM_DATE — to avoid duplicate findings} |

---

## QA Agent: Stats Verification

| Field | Value |
|-------|-------|
| **Agent** | {AGENT_NAME} |
| **Scope** | Numerical accuracy, calculation correctness, statistical methods, data aggregation |
| **Files Reviewed** | {FILE_LIST} |
| **Prior Coverage Checked** | {YES — peer review finding #X already covers Y / NO prior findings in this area} |

### Findings

> Findings are framed with red team thinking — the agent actively tries to produce incorrect results, not just verify the happy path.

#### STATS-QA-001: {FINDING_TITLE}

| Field | Value |
|-------|-------|
| **Severity** | **{CRITICAL/HIGH/MEDIUM/LOW}** |
| **Net-New?** | {YES — not found in prior reviews / NO — duplicate of peer review #X} |
| **Attack Vector** | {HOW_THE_AGENT_TRIED_TO_BREAK_IT} |
| **Expected** | {CORRECT_BEHAVIOR} |
| **Actual** | {WHAT_HAPPENED} |
| **Evidence** | `{CODE_SNIPPET, LOG, OR_DATA}` |
| **Fix Recommendation** | {SPECIFIC_FIX} |

#### STATS-QA-002: {FINDING_TITLE}

> Repeat finding block as needed.

### Agent Summary

> {1-2_SENTENCES — overall assessment of statistical/calculation correctness.}

---

## QA Agent: Code Quality

| Field | Value |
|-------|-------|
| **Agent** | {AGENT_NAME} |
| **Scope** | Code structure, maintainability, error handling, type safety, standards compliance |
| **Files Reviewed** | {FILE_LIST} |
| **Prior Coverage Checked** | {YES/NO — reference specific prior findings} |

### Findings

#### CODE-QA-001: {FINDING_TITLE}

| Field | Value |
|-------|-------|
| **Severity** | **{CRITICAL/HIGH/MEDIUM/LOW}** |
| **Net-New?** | {YES/NO} |
| **Category** | {ERROR_HANDLING / TYPE_SAFETY / MAINTAINABILITY / STANDARDS / OTHER} |
| **File:Line** | `{FILE_PATH}:{LINE_NUMBER}` |
| **Issue** | {DESCRIPTION} |
| **Fix Recommendation** | {SPECIFIC_FIX} |

#### CODE-QA-002: {FINDING_TITLE}

> Repeat finding block as needed.

### Agent Summary

> {1-2_SENTENCES — overall assessment of code quality.}

---

## QA Agent: Data Integrity

| Field | Value |
|-------|-------|
| **Agent** | {AGENT_NAME} |
| **Scope** | Data flow correctness, persistence, transformation accuracy, schema validation |
| **Files Reviewed** | {FILE_LIST} |
| **Prior Coverage Checked** | {YES/NO — reference specific prior findings} |

### Findings

#### DATA-QA-001: {FINDING_TITLE}

| Field | Value |
|-------|-------|
| **Severity** | **{CRITICAL/HIGH/MEDIUM/LOW}** |
| **Net-New?** | {YES/NO} |
| **Data Path** | {SOURCE → TRANSFORMATION → DESTINATION} |
| **Attack Vector** | {HOW_DATA_INTEGRITY_WAS_TESTED — e.g., malformed input, missing fields, type coercion} |
| **Expected** | {CORRECT_DATA_STATE} |
| **Actual** | {WHAT_HAPPENED} |
| **Fix Recommendation** | {SPECIFIC_FIX} |

#### DATA-QA-002: {FINDING_TITLE}

> Repeat finding block as needed.

### Agent Summary

> {1-2_SENTENCES — overall assessment of data integrity.}

---

## QA Agent: Security

| Field | Value |
|-------|-------|
| **Agent** | {AGENT_NAME} |
| **Scope** | Authentication, authorization, input sanitization, secrets management, dependency vulnerabilities |
| **Files Reviewed** | {FILE_LIST} |
| **Prior Coverage Checked** | {YES/NO — reference red team findings specifically} |

### Findings

#### SEC-QA-001: {FINDING_TITLE}

| Field | Value |
|-------|-------|
| **Severity** | **{CRITICAL/HIGH/MEDIUM/LOW}** |
| **Net-New?** | {YES/NO — critical to avoid duplicating red team findings} |
| **OWASP Category** | {IF_APPLICABLE — e.g., A01:2021 Broken Access Control} |
| **Attack Vector** | {HOW_THE_VULNERABILITY_WAS_TESTED} |
| **Impact** | {WHAT_COULD_HAPPEN_IF_EXPLOITED} |
| **Fix Recommendation** | {SPECIFIC_FIX} |

#### SEC-QA-002: {FINDING_TITLE}

> Repeat finding block as needed.

### Agent Summary

> {1-2_SENTENCES — overall assessment of security posture.}

---

## QA Agent: UI/UX Browser Testing

| Field | Value |
|-------|-------|
| **Agent** | {AGENT_NAME} |
| **Scope** | Visual rendering, responsiveness, accessibility, browser compatibility, interaction correctness |
| **Pages Tested** | {PAGE_LIST} |
| **Browsers Tested** | {BROWSER_LIST} |
| **Prior Coverage Checked** | {YES/NO — reference UX sense check findings if applicable} |

### Findings

#### UI-QA-001: {FINDING_TITLE}

| Field | Value |
|-------|-------|
| **Severity** | **{CRITICAL/HIGH/MEDIUM/LOW}** |
| **Net-New?** | {YES/NO} |
| **Category** | {RENDERING / RESPONSIVENESS / ACCESSIBILITY / INTERACTION / BROWSER_COMPAT} |
| **Page** | {PAGE_OR_COMPONENT} |
| **Steps to Reproduce** | {NUMBERED_STEPS} |
| **Expected** | {CORRECT_APPEARANCE_OR_BEHAVIOR} |
| **Actual** | {WHAT_HAPPENED} |
| **Screenshot/Evidence** | {PATH_OR_DESCRIPTION} |
| **Fix Recommendation** | {SPECIFIC_FIX} |

#### UI-QA-002: {FINDING_TITLE}

> Repeat finding block as needed.

### Agent Summary

> {1-2_SENTENCES — overall assessment of UI/UX quality.}

---

## QA Manager Synthesis

### Prioritized Fix Plan

> All findings across all QA agents, deduplicated and prioritized. This is the single source of truth for what needs to be fixed.

| Priority | ID | Finding | Agent | Severity | Net-New? | Status |
|----------|----|---------|-------|----------|----------|--------|
| 1 | {STATS/CODE/DATA/SEC/UI-QA-NNN} | {FINDING_SUMMARY} | {AGENT_NAME} | {CRITICAL} | {YES/NO} | {OPEN/FIXED/DEFERRED} |
| 2 | {ID} | {FINDING_SUMMARY} | {AGENT_NAME} | {HIGH} | {YES/NO} | {OPEN/FIXED/DEFERRED} |
| 3 | {ID} | {FINDING_SUMMARY} | {AGENT_NAME} | {MEDIUM} | {YES/NO} | {OPEN/FIXED/DEFERRED} |
| N | {ID} | {FINDING_SUMMARY} | {AGENT_NAME} | {LOW} | {YES/NO} | {OPEN/FIXED/DEFERRED} |

### Net-New Findings Summary

> Findings that were **not** caught by prior peer review, red team review, or other quality gates. These represent gaps in earlier review coverage.

| # | ID | Finding | Agent | Why It Was Missed Earlier |
|---|----|---------|-------|--------------------------|
| 1 | {ID} | {FINDING_SUMMARY} | {AGENT_NAME} | {EXPLANATION — e.g., "Peer review focused on architecture, not edge-case input handling"} |
| 2 | {ID} | {FINDING_SUMMARY} | {AGENT_NAME} | {EXPLANATION} |
| N | {ID} | {FINDING_SUMMARY} | {AGENT_NAME} | {EXPLANATION} |

### Overall Metrics

| Metric | Value |
|--------|-------|
| **Total Findings (All Agents)** | {COUNT} |
| **Net-New Findings** | {COUNT} |
| **Duplicate/Prior Coverage** | {COUNT} |
| **Critical** | {COUNT} |
| **High** | {COUNT} |
| **Medium** | {COUNT} |
| **Low** | {COUNT} |
| **QA Verdict** | **{PASS / PASS_WITH_FIXES / FAIL}** |

### QA Manager Verdict

> {2-3_SENTENCES. State whether the slice passes QA, what must be fixed before merge, and whether any net-new findings indicate a gap in the review pipeline that should be addressed.}

---

## Sign-Off

| Role | Name/Agent | Date |
|------|-----------|------|
| QA Manager | {NAME_OR_AGENT} | {YYYY-MM-DD} |
