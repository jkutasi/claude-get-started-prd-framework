# Test Code Peer Review — Slice {N}: {SLICE_NAME}

> **Phase B.3 artifact.** This file documents the peer review of test code by 3 external models. Test code gets the same multi-model review as implementation code. Created after test-writer sub-agents complete Phase B.2.

---

## Review Summary

| Reviewer | Model | Findings | Critical | High | Medium | Low |
|---|---|---|---|---|---|---|
| Reviewer Gemini | {MODEL_VERSION} | {TOTAL} | {COUNT} | {COUNT} | {COUNT} | {COUNT} |
| Reviewer OpenAI Codex | {MODEL_VERSION} | {TOTAL} | {COUNT} | {COUNT} | {COUNT} | {COUNT} |
| Reviewer Grok | {MODEL_VERSION} | {TOTAL} | {COUNT} | {COUNT} | {COUNT} | {COUNT} |
| Reviewer Greptile (optional) | Greptile (codebase-aware) | {TOTAL} | {COUNT} | {COUNT} | {COUNT} | {COUNT} |

> **Delete the Greptile row if `GREPTILE_API_KEY` is not configured for this project.**

**Consensus issues (2+ reviewers agree):** {COUNT} mandatory fixes
**Single-reviewer issues:** {COUNT} recommended fixes (CTO judgment)

---

## Review Criteria

Each reviewer evaluates the test code against:

1. **Test Quality** — Are assertions specific and meaningful? Do they test behavior, not implementation details?
2. **Coverage Gaps** — Are there user story elements, edge cases, or Gherkin scenarios without corresponding tests?
3. **Assertion Specificity** — Do tests assert exact expected values, or do they use vague checks (e.g., `assert result is not None`)?
4. **Mock Correctness** — Do mocks match real behavior? Are mocks simpler than reality (producing false confidence)?
5. **Test Independence** — Can tests run in any order? Do they share state that could cause flaky failures?
6. **Red Phase Validity** — Are all tests genuinely RED for the right reason (missing implementation), not RED due to test bugs?
7. **Gherkin Alignment** — Does each test clearly trace back to a Gherkin scenario?

---

## Reviewer Gemini Findings

### Finding G-1: {TITLE}
**Severity:** {CRITICAL / HIGH / MEDIUM / LOW}
**File:** `{TEST_FILE_PATH}`
**Issue:** {DESCRIPTION}
**Recommendation:** {FIX}

### Finding G-2: {TITLE}
...

---

## Reviewer OpenAI Codex Findings

### Finding O-1: {TITLE}
**Severity:** {CRITICAL / HIGH / MEDIUM / LOW}
**File:** `{TEST_FILE_PATH}`
**Issue:** {DESCRIPTION}
**Recommendation:** {FIX}

### Finding O-2: {TITLE}
...

---

## Reviewer Grok Findings

### Finding X-1: {TITLE}
**Severity:** {CRITICAL / HIGH / MEDIUM / LOW}
**File:** `{TEST_FILE_PATH}`
**Issue:** {DESCRIPTION}
**Recommendation:** {FIX}

### Finding X-2: {TITLE}
...

---

## Reviewer Greptile Findings (Optional — only if `GREPTILE_API_KEY` is configured)

> **Delete this entire section if Greptile is not configured for this project.**

### Finding GR-1: {TITLE}
**Severity:** {CRITICAL / HIGH / MEDIUM / LOW}
**File:** `{TEST_FILE_PATH}`
**Issue:** {DESCRIPTION}
**Recommendation:** {FIX}

### Finding GR-2: {TITLE}
...

---

## CTO Synthesis

### Mandatory Fixes (2+ reviewers agree)

| # | Issue | Reviewers | Severity | Assigned To | Status |
|---|---|---|---|---|---|
| 1 | {ISSUE} | {WHICH_REVIEWERS} | {SEVERITY} | {AGENT_NAME} | OPEN / FIXED |
| 2 | {ISSUE} | {WHICH_REVIEWERS} | {SEVERITY} | {AGENT_NAME} | OPEN / FIXED |
| ... | ... | ... | ... | ... | ... |

### Recommended Fixes (1 reviewer, CTO judgment)

| # | Issue | Reviewer | Severity | CTO Decision | Rationale |
|---|---|---|---|---|---|
| 1 | {ISSUE} | {REVIEWER} | {SEVERITY} | FIX / DEFER / DISMISS | {REASON} |
| ... | ... | ... | ... | ... | ... |

---

## Post-Review Status

- [ ] All mandatory fixes completed by test-writer sub-agents
- [ ] Fixed tests re-validated (still RED against skeletal interfaces)
- [ ] This file saved to `reviews/slice-{N}-test-review.md`
- [ ] Ready to proceed to Phase C (Implementation)
