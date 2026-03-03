# UX Sense Check Report — Slice {SLICE_NUMBER}: {SLICE_NAME}

## Metadata

| Field | Value |
|-------|-------|
| **Date** | {YYYY-MM-DD} |
| **Reviewer** | {REVIEWER_NAME_OR_AGENT} |
| **Slice Contract** | `contracts/slice-{SLICE_NUMBER}-contract.md` |
| **Pages Tested** | {COMMA_SEPARATED_LIST_OF_PAGES_OR_VIEWS} |
| **Personas Tested** | {COUNT} |

---

## Personas

> Each persona represents a real user archetype for this application. The UX Sense Check walks through the slice as each persona and records whether the interface makes sense to them — not whether it works technically, but whether a human with that persona's background would understand it.

---

## Persona 1: {PERSONA_NAME}

| Field | Value |
|-------|-------|
| **Role** | {JOB_TITLE_OR_ROLE — e.g., "Portfolio Manager", "Junior Analyst", "Operations Staff"} |
| **Technical Level** | {NON_TECHNICAL / SEMI_TECHNICAL / TECHNICAL} |
| **Domain Expertise** | {HIGH / MEDIUM / LOW} |
| **Usage Context** | {HOW_AND_WHEN_THEY_WOULD_USE_THIS — e.g., "Daily morning review", "Ad-hoc deep dives"} |

### Test Area Results

| # | Test Area | Result | Findings |
|---|----------|--------|----------|
| 1 | **First Impression** — Does the page immediately communicate its purpose? | {PASS/CONCERN/FAIL} | {WHAT_THE_PERSONA_WOULD_THINK_ON_FIRST_SEEING_THE_PAGE} |
| 2 | **Label Clarity** — Are all labels, headings, and column names self-explanatory? | {PASS/CONCERN/FAIL} | {AMBIGUOUS_LABELS, ACRONYMS_WITHOUT_EXPLANATION, UNCLEAR_HEADINGS} |
| 3 | **Action Clarity** — Is it obvious what to click, where to input, and what each button does? | {PASS/CONCERN/FAIL} | {BUTTONS_WITH_VAGUE_TEXT, HIDDEN_ACTIONS, UNCLEAR_CTAS} |
| 4 | **Result Comprehension** — After performing an action, does the user understand what happened? | {PASS/CONCERN/FAIL} | {MISSING_FEEDBACK, CONFUSING_SUCCESS_STATES, UNCLEAR_CHANGES} |
| 5 | **Error Recovery** — When something goes wrong, does the user know what to do? | {PASS/CONCERN/FAIL} | {UNHELPFUL_ERROR_MESSAGES, NO_GUIDANCE, DEAD_ENDS} |
| 6 | **Flow Completeness** — Can the user complete their task without leaving the page or guessing? | {PASS/CONCERN/FAIL} | {MISSING_STEPS, REQUIRED_EXTERNAL_KNOWLEDGE, BROKEN_FLOWS} |
| 7 | **Jargon Detection** — Are there terms this persona would not understand? | {PASS/CONCERN/FAIL} | {LIST_SPECIFIC_JARGON_TERMS_AND_WHERE_THEY_APPEAR} |

### Comprehension Score

> **{1-5}** / 5

| Score | Meaning |
|-------|---------|
| 5 | Persona would use this confidently with no help |
| 4 | Persona would figure it out after brief exploration |
| 3 | Persona would need some guidance or documentation |
| 2 | Persona would struggle and likely ask for help |
| 1 | Persona would be unable to complete the task |

### Key Quote

> "{WHAT_CONFUSED_THEM_MOST — write this as if the persona is speaking. e.g., 'I see a table of numbers but I have no idea what NAV means or why it is different from yesterday.'}"

---

## Persona 2: {PERSONA_NAME}

| Field | Value |
|-------|-------|
| **Role** | {JOB_TITLE_OR_ROLE} |
| **Technical Level** | {NON_TECHNICAL / SEMI_TECHNICAL / TECHNICAL} |
| **Domain Expertise** | {HIGH / MEDIUM / LOW} |
| **Usage Context** | {HOW_AND_WHEN_THEY_WOULD_USE_THIS} |

### Test Area Results

| # | Test Area | Result | Findings |
|---|----------|--------|----------|
| 1 | **First Impression** | {PASS/CONCERN/FAIL} | {FINDINGS} |
| 2 | **Label Clarity** | {PASS/CONCERN/FAIL} | {FINDINGS} |
| 3 | **Action Clarity** | {PASS/CONCERN/FAIL} | {FINDINGS} |
| 4 | **Result Comprehension** | {PASS/CONCERN/FAIL} | {FINDINGS} |
| 5 | **Error Recovery** | {PASS/CONCERN/FAIL} | {FINDINGS} |
| 6 | **Flow Completeness** | {PASS/CONCERN/FAIL} | {FINDINGS} |
| 7 | **Jargon Detection** | {PASS/CONCERN/FAIL} | {FINDINGS} |

### Comprehension Score

> **{1-5}** / 5

### Key Quote

> "{WHAT_CONFUSED_THEM_MOST}"

---

## Persona 3: {PERSONA_NAME}

> Copy the persona block above for each additional persona tested.

---

## Cross-Persona Analysis

> Issues found by **two or more personas** are high priority. They represent confusion that is not specific to one user type but is a systemic UX problem.

| # | Issue | Personas Affected | Severity | Pages/Components |
|---|-------|------------------|----------|-----------------|
| 1 | {DESCRIBE_THE_SHARED_ISSUE} | {PERSONA_1, PERSONA_2, ...} | {HIGH/MEDIUM} | {WHERE_IT_APPEARS} |
| 2 | {DESCRIBE_THE_SHARED_ISSUE} | {PERSONA_1, PERSONA_2, ...} | {HIGH/MEDIUM} | {WHERE_IT_APPEARS} |
| N | {DESCRIBE_THE_SHARED_ISSUE} | {PERSONA_1, PERSONA_2, ...} | {HIGH/MEDIUM} | {WHERE_IT_APPEARS} |

---

## Jargon / Clarity Findings

> All terms, labels, or phrases flagged by any persona as unclear.

| # | Term / Phrase | Where It Appears | Personas Who Flagged | Suggested Plain-English Alternative |
|---|--------------|------------------|---------------------|-------------------------------------|
| 1 | {JARGON_TERM} | {PAGE — COMPONENT — LOCATION} | {PERSONA_LIST} | {PLAIN_ENGLISH_SUGGESTION} |
| 2 | {JARGON_TERM} | {PAGE — COMPONENT — LOCATION} | {PERSONA_LIST} | {PLAIN_ENGLISH_SUGGESTION} |
| N | {JARGON_TERM} | {PAGE — COMPONENT — LOCATION} | {PERSONA_LIST} | {PLAIN_ENGLISH_SUGGESTION} |

---

## Recommendations

> Actionable improvements for plain-English clarity and UX comprehension.

| # | Recommendation | Priority | Affected Personas | Effort |
|---|---------------|----------|-------------------|--------|
| 1 | {SPECIFIC_ACTIONABLE_RECOMMENDATION} | {HIGH/MEDIUM/LOW} | {PERSONA_LIST} | {SMALL/MEDIUM/LARGE} |
| 2 | {SPECIFIC_ACTIONABLE_RECOMMENDATION} | {HIGH/MEDIUM/LOW} | {PERSONA_LIST} | {SMALL/MEDIUM/LARGE} |
| N | {SPECIFIC_ACTIONABLE_RECOMMENDATION} | {HIGH/MEDIUM/LOW} | {PERSONA_LIST} | {SMALL/MEDIUM/LARGE} |

---

## Overall Assessment

| Metric | Value |
|--------|-------|
| **Personas Tested** | {COUNT} |
| **Average Comprehension Score** | **{X.X}** / 5 |
| **Cross-Persona Issues** | {COUNT} |
| **Jargon Terms Flagged** | {COUNT} |
| **Recommendations** | {COUNT} |
| **Overall Verdict** | **{CLEAR — No major issues / NEEDS_WORK — Fix flagged items before ship / CONFUSING — Significant rework needed}** |

### Summary

> {2-3_SENTENCES. State whether the slice is understandable to its intended users. Highlight the most important finding and the single highest-priority recommendation.}

---

## Sign-Off

| Role | Name/Agent | Date |
|------|-----------|------|
| UX Reviewer | {NAME_OR_AGENT} | {YYYY-MM-DD} |
