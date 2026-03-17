# Test Code Peer Review — Slice {N}: {SLICE_NAME}

> **Phase B.3 artifact.** Peer review of test code by 3 external models. Created after test-writer sub-agents complete Phase B.2.

---

## Review Summary

| Reviewer | Model | Findings | Critical | High | Medium | Low |
|---|---|---|---|---|---|---|
| Reviewer Gemini | {MODEL_VERSION} | {TOTAL} | {COUNT} | {COUNT} | {COUNT} | {COUNT} |
| Reviewer OpenAI Codex | {MODEL_VERSION} | {TOTAL} | {COUNT} | {COUNT} | {COUNT} | {COUNT} |
| Reviewer Grok | {MODEL_VERSION} | {TOTAL} | {COUNT} | {COUNT} | {COUNT} | {COUNT} |
| Reviewer Greptile (optional) | Greptile (codebase-aware) | {TOTAL} | {COUNT} | {COUNT} | {COUNT} | {COUNT} |

> **Delete the Greptile row if `GREPTILE_API_KEY` is not configured.**

**Consensus issues (2+ reviewers agree):** {COUNT} mandatory fixes
**Single-reviewer issues:** {COUNT} recommended fixes (CTO judgment)

---

## Review Criteria

1. **Test Quality** — Are assertions specific and meaningful?
2. **Coverage Gaps** — Are there user story elements without tests?
3. **Assertion Specificity** — Do tests assert exact expected values?
4. **Mock Correctness** — Do mocks match real behavior?
5. **Test Independence** — Can tests run in any order?
6. **Red Phase Validity** — Are tests genuinely RED for the right reason?
7. **Gherkin Alignment** — Does each test trace back to a Gherkin scenario?

---

## Reviewer Gemini Findings

### Finding G-1: {TITLE}
**Severity:** {CRITICAL / HIGH / MEDIUM / LOW}
**File:** `{TEST_FILE_PATH}`
**Issue:** {DESCRIPTION}
**Recommendation:** {FIX}

---

## Reviewer OpenAI Codex Findings

### Finding O-1: {TITLE}
**Severity:** {CRITICAL / HIGH / MEDIUM / LOW}
**File:** `{TEST_FILE_PATH}`
**Issue:** {DESCRIPTION}
**Recommendation:** {FIX}

---

## Reviewer Grok Findings

### Finding X-1: {TITLE}
**Severity:** {CRITICAL / HIGH / MEDIUM / LOW}
**File:** `{TEST_FILE_PATH}`
**Issue:** {DESCRIPTION}
**Recommendation:** {FIX}

---

## Reviewer Greptile Findings (Optional)

> **Delete this section if Greptile is not configured.**

### Finding GR-1: {TITLE}
**Severity:** {CRITICAL / HIGH / MEDIUM / LOW}
**File:** `{TEST_FILE_PATH}`
**Issue:** {DESCRIPTION}
**Recommendation:** {FIX}

---

## CTO Synthesis

### Mandatory Fixes (2+ reviewers agree)

| # | Issue | Reviewers | Severity | Assigned To | Status |
|---|---|---|---|---|---|
| 1 | {ISSUE} | {WHICH_REVIEWERS} | {SEVERITY} | {AGENT_NAME} | OPEN / FIXED |

### Recommended Fixes (1 reviewer, CTO judgment)

| # | Issue | Reviewer | Severity | CTO Decision | Rationale |
|---|---|---|---|---|---|
| 1 | {ISSUE} | {REVIEWER} | {SEVERITY} | FIX / DEFER / DISMISS | {REASON} |

---

## Post-Review Status

- [ ] All mandatory fixes completed by test-writer sub-agents
- [ ] Fixed tests re-validated (still RED against skeletal interfaces)
- [ ] This file saved to `reviews/slice-{N}-test-review.md`
- [ ] Ready to proceed to Phase C (Implementation)
