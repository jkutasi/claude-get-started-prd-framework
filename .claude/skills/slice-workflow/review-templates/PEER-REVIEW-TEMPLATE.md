# Peer Review — Slice {SLICE_NUMBER}: {SLICE_NAME}

> **REVIEWER INSTRUCTION:** Issue a definitive verdict based on the code. Do NOT condition your verdict on user review, user testing, or user approval. Your job is to assess code quality independently. Verdicts like "approved contingent on user review" are invalid. Security must be evaluated as a review dimension for every review.

## Metadata

| Field | Value |
|-------|-------|
| **Date** | {YYYY-MM-DD} |
| **Slice Contract** | `contracts/slice-{SLICE_NUMBER}-contract.md` |
| **Code Under Review** | {FILES_OR_MODULES} |
| **Initiated By** | {CTO_AGENT_OR_LEAD} |

---

## Reviewer 1: Gemini

| Field | Value |
|-------|-------|
| **Model** | {GEMINI_MODEL_VERSION — e.g., Gemini 2.5 Pro} |
| **Date** | {YYYY-MM-DD} |
| **Code Reviewed** | {FILES_AND_LINE_RANGES_PROVIDED_TO_MODEL} |
| **Prompt Focus** | {WHAT_THE_REVIEWER_WAS_ASKED_TO_FOCUS_ON — e.g., architecture, correctness, edge cases} |

### Findings

| # | Severity | Finding | File:Line | Recommendation |
|---|----------|---------|-----------|----------------|
| 1 | {CRITICAL/HIGH/MEDIUM/LOW/INFO} | {DESCRIPTION_OF_ISSUE} | `{FILE_PATH}:{LINE_NUMBER}` | {SPECIFIC_FIX_RECOMMENDATION} |

### Summary

> {GEMINI_OVERALL_ASSESSMENT — 2-3 sentences on code quality, architecture concerns, and top recommendation.}

---

## Reviewer 2: OpenAI Codex

| Field | Value |
|-------|-------|
| **Model** | {CODEX_MODEL_VERSION — e.g., gpt-5.4-codex} |
| **Date** | {YYYY-MM-DD} |
| **Code Reviewed** | {FILES_AND_LINE_RANGES_PROVIDED_TO_MODEL} |
| **Prompt Focus** | {WHAT_THE_REVIEWER_WAS_ASKED_TO_FOCUS_ON} |

### Findings

| # | Severity | Finding | File:Line | Recommendation |
|---|----------|---------|-----------|----------------|
| 1 | {CRITICAL/HIGH/MEDIUM/LOW/INFO} | {DESCRIPTION_OF_ISSUE} | `{FILE_PATH}:{LINE_NUMBER}` | {SPECIFIC_FIX_RECOMMENDATION} |

### Summary

> {CODEX_OVERALL_ASSESSMENT — 2-3 sentences on code quality, architecture concerns, and top recommendation.}

---

## Reviewer 3: Grok

| Field | Value |
|-------|-------|
| **Model** | {GROK_MODEL_VERSION — e.g., Grok 3} |
| **Date** | {YYYY-MM-DD} |
| **Code Reviewed** | {FILES_AND_LINE_RANGES_PROVIDED_TO_MODEL} |
| **Prompt Focus** | {WHAT_THE_REVIEWER_WAS_ASKED_TO_FOCUS_ON} |

### Findings

| # | Severity | Finding | File:Line | Recommendation |
|---|----------|---------|-----------|----------------|
| 1 | {CRITICAL/HIGH/MEDIUM/LOW/INFO} | {DESCRIPTION_OF_ISSUE} | `{FILE_PATH}:{LINE_NUMBER}` | {SPECIFIC_FIX_RECOMMENDATION} |

### Summary

> {GROK_OVERALL_ASSESSMENT — 2-3 sentences on code quality, architecture concerns, and top recommendation.}

---

## Reviewer 4: Greptile (Optional — only if `GREPTILE_API_KEY` is configured)

> **Delete this entire section if Greptile is not configured for this project.**

| Field | Value |
|-------|-------|
| **Model** | Greptile (codebase-aware) |
| **Date** | {YYYY-MM-DD} |
| **Code Reviewed** | {FILES_AND_LINE_RANGES_PROVIDED_TO_MODEL} |
| **Prompt Focus** | Cross-file consistency, dependency impact, codebase convention compliance |

### Findings

| # | Severity | Finding | File:Line | Recommendation |
|---|----------|---------|-----------|----------------|
| 1 | {CRITICAL/HIGH/MEDIUM/LOW/INFO} | {DESCRIPTION_OF_ISSUE} | `{FILE_PATH}:{LINE_NUMBER}` | {SPECIFIC_FIX_RECOMMENDATION} |

### Summary

> {GREPTILE_OVERALL_ASSESSMENT — 2-3 sentences on cross-file consistency, dependency risks, and codebase convention compliance.}

---

## CTO Synthesis

### Consensus Issues (Mandatory Fixes)

> Issues flagged by **2 or more reviewers**. These are mandatory fixes.

| # | Issue | Reviewers Who Flagged | Severity | File:Line | Required Action |
|---|-------|----------------------|----------|-----------|-----------------|
| 1 | {ISSUE_DESCRIPTION} | {REVIEWER_LIST} | {CRITICAL/HIGH/MEDIUM} | `{FILE_PATH}:{LINE_NUMBER}` | {WHAT_MUST_BE_DONE} |

### Non-Consensus Issues (Review & Decide)

> Issues flagged by **only 1 reviewer**. CTO evaluates whether to fix, defer, or dismiss.

| # | Issue | Flagged By | Severity | CTO Decision | Rationale |
|---|-------|-----------|----------|--------------|-----------|
| 1 | {ISSUE_DESCRIPTION} | {REVIEWER} | {SEVERITY} | {FIX/DEFER/DISMISS} | {WHY} |

### Overall Verdict

| Metric | Value |
|--------|-------|
| **Total Findings** | {COUNT} |
| **Consensus Issues** | {COUNT} |
| **Non-Consensus Issues** | {COUNT} |
| **Mandatory Fixes** | {COUNT} |
| **Verdict** | **{APPROVED / APPROVED_WITH_FIXES / REQUIRES_REWORK}** |

### Architecture Compliance (Article 20)

| Check | Status | Notes |
|-------|--------|-------|
| Feature-folder structure (20a) | {PASS/FAIL/NA} | {NOTES} |
| Three-layer separation (20b) | {PASS/FAIL/NA} | {NOTES} |
| 150-line file limit (20c) | {PASS/FAIL/NA} | {NOTES} |
| Display-only frontend (20d) | {PASS/FAIL/NA} | {NOTES} |
| Structured logging — no console (20e) | {PASS/FAIL/NA} | {NOTES} |
| Error wrapping with AppError (20f) | {PASS/FAIL/NA} | {NOTES} |

---

## Sign-Off

| Role | Name/Agent | Date |
|------|-----------|------|
| CTO / Synthesis Lead | {NAME_OR_AGENT} | {YYYY-MM-DD} |
