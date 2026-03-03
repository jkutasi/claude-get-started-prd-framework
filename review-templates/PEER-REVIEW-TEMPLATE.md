# Peer Review — Slice {SLICE_NUMBER}: {SLICE_NAME}

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
| 2 | {CRITICAL/HIGH/MEDIUM/LOW/INFO} | {DESCRIPTION_OF_ISSUE} | `{FILE_PATH}:{LINE_NUMBER}` | {SPECIFIC_FIX_RECOMMENDATION} |
| N | {CRITICAL/HIGH/MEDIUM/LOW/INFO} | {DESCRIPTION_OF_ISSUE} | `{FILE_PATH}:{LINE_NUMBER}` | {SPECIFIC_FIX_RECOMMENDATION} |

### Summary

> {GEMINI_OVERALL_ASSESSMENT — 2-3 sentences on code quality, architecture concerns, and top recommendation.}

---

## Reviewer 2: OpenAI Codex

| Field | Value |
|-------|-------|
| **Model** | {CODEX_MODEL_VERSION — e.g., gpt-5.2-codex} |
| **Date** | {YYYY-MM-DD} |
| **Code Reviewed** | {FILES_AND_LINE_RANGES_PROVIDED_TO_MODEL} |
| **Prompt Focus** | {WHAT_THE_REVIEWER_WAS_ASKED_TO_FOCUS_ON} |

### Findings

| # | Severity | Finding | File:Line | Recommendation |
|---|----------|---------|-----------|----------------|
| 1 | {CRITICAL/HIGH/MEDIUM/LOW/INFO} | {DESCRIPTION_OF_ISSUE} | `{FILE_PATH}:{LINE_NUMBER}` | {SPECIFIC_FIX_RECOMMENDATION} |
| 2 | {CRITICAL/HIGH/MEDIUM/LOW/INFO} | {DESCRIPTION_OF_ISSUE} | `{FILE_PATH}:{LINE_NUMBER}` | {SPECIFIC_FIX_RECOMMENDATION} |
| N | {CRITICAL/HIGH/MEDIUM/LOW/INFO} | {DESCRIPTION_OF_ISSUE} | `{FILE_PATH}:{LINE_NUMBER}` | {SPECIFIC_FIX_RECOMMENDATION} |

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
| 2 | {CRITICAL/HIGH/MEDIUM/LOW/INFO} | {DESCRIPTION_OF_ISSUE} | `{FILE_PATH}:{LINE_NUMBER}` | {SPECIFIC_FIX_RECOMMENDATION} |
| N | {CRITICAL/HIGH/MEDIUM/LOW/INFO} | {DESCRIPTION_OF_ISSUE} | `{FILE_PATH}:{LINE_NUMBER}` | {SPECIFIC_FIX_RECOMMENDATION} |

### Summary

> {GROK_OVERALL_ASSESSMENT — 2-3 sentences on code quality, architecture concerns, and top recommendation.}

---

## CTO Synthesis

### Consensus Issues (Mandatory Fixes)

> Issues flagged by **2 or more reviewers**. These are mandatory fixes — multiple independent models agree something is wrong.

| # | Issue | Reviewers Who Flagged | Severity | File:Line | Required Action |
|---|-------|----------------------|----------|-----------|-----------------|
| 1 | {ISSUE_DESCRIPTION} | {Gemini, Codex / Gemini, Grok / Codex, Grok / All} | {CRITICAL/HIGH/MEDIUM} | `{FILE_PATH}:{LINE_NUMBER}` | {WHAT_MUST_BE_DONE} |
| 2 | {ISSUE_DESCRIPTION} | {REVIEWER_LIST} | {CRITICAL/HIGH/MEDIUM} | `{FILE_PATH}:{LINE_NUMBER}` | {WHAT_MUST_BE_DONE} |
| N | {ISSUE_DESCRIPTION} | {REVIEWER_LIST} | {CRITICAL/HIGH/MEDIUM} | `{FILE_PATH}:{LINE_NUMBER}` | {WHAT_MUST_BE_DONE} |

### Non-Consensus Issues (Review & Decide)

> Issues flagged by **only 1 reviewer**. CTO evaluates whether to fix, defer, or dismiss.

| # | Issue | Flagged By | Severity | CTO Decision | Rationale |
|---|-------|-----------|----------|--------------|-----------|
| 1 | {ISSUE_DESCRIPTION} | {Gemini/Codex/Grok} | {SEVERITY} | {FIX/DEFER/DISMISS} | {WHY} |
| 2 | {ISSUE_DESCRIPTION} | {Gemini/Codex/Grok} | {SEVERITY} | {FIX/DEFER/DISMISS} | {WHY} |
| N | {ISSUE_DESCRIPTION} | {Gemini/Codex/Grok} | {SEVERITY} | {FIX/DEFER/DISMISS} | {WHY} |

### Overall Verdict

| Metric | Value |
|--------|-------|
| **Total Findings** | {COUNT} |
| **Consensus Issues** | {COUNT} |
| **Non-Consensus Issues** | {COUNT} |
| **Mandatory Fixes** | {COUNT} |
| **Verdict** | **{APPROVED / APPROVED_WITH_FIXES / REQUIRES_REWORK}** |

> {CTO_SUMMARY — 2-3 sentences on overall code health, key risks, and next steps.}

---

## Sign-Off

| Role | Name/Agent | Date |
|------|-----------|------|
| CTO / Synthesis Lead | {NAME_OR_AGENT} | {YYYY-MM-DD} |
