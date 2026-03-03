# Project Diary -- {PROJECT_NAME}

> A running log of decisions, progress, blockers, and lessons learned. Updated after every significant event. The diary is append-only -- never edit or delete previous entries.

---

## How to Use This Diary

1. **Add a new entry** at the top of the Entries section after each significant event (slice completion, major decision, blocker encountered, review completed).
2. **Be honest.** Record what actually happened, not what you wish happened. Include mistakes and dead ends.
3. **Record decisions with rationale.** Future you (or a teammate) will want to know *why*, not just *what*.
4. **Flag blockers immediately.** Do not bury blockers inside narrative paragraphs.
5. **Link to artifacts.** Reference specific files, commits, slices, and review documents.
6. **Update after every significant event:** slice completion, peer review round, QA swarm results, owner decision, blocker resolution, architecture change.

---

## Project Overview

| Field | Value |
|-------|-------|
| **Project Name** | {PROJECT_NAME} |
| **Started** | {YYYY-MM-DD} |
| **Goal** | {ONE_SENTENCE_PROJECT_GOAL} |
| **Tech Stack** | {LANGUAGES, FRAMEWORKS, DATABASES} |
| **Repository** | {REPO_URL_OR_PATH} |
| **Team** | {TEAM_MEMBERS_OR_AGENTS} |

---

## Entries

> Newest entries first. Each entry follows the format below.

---

### Entry {ENTRY_NUMBER} -- {YYYY-MM-DD}

**Phase / Slice:** {PHASE_LETTER} of Slice {N} -- {SLICE_NAME}

**Session focus:** {ONE_LINE_DESCRIPTION_OF_WHAT_THIS_SESSION_WAS_ABOUT}

#### Decisions Made

| # | Decision | Rationale | Alternatives Considered |
|---|----------|-----------|------------------------|
| 1 | {WHAT_WAS_DECIDED} | {WHY} | {WHAT_ELSE_WAS_CONSIDERED_AND_WHY_IT_WAS_REJECTED} |

#### Discoveries

- {DISCOVERY_1 -- something unexpected learned during implementation, review, or testing}
- {DISCOVERY_2 -- a technical insight, a data quirk, a dependency behavior}

#### Blockers

| # | Blocker | Impact | Status |
|---|---------|--------|--------|
| 1 | {DESCRIBE_BLOCKER} | {WHAT_IT_PREVENTS} | {OPEN / RESOLVED -- how it was resolved} |

> If no blockers, write: No blockers.

#### Peer Review Summary

- **Reviewers:** {LIST -- e.g., Gemini, OpenAI Codex, Grok}
- **Consensus issues (2+ reviewers):** {COUNT} mandatory fixes
- **Key findings:** {BRIEF_SUMMARY_OF_TOP_FINDINGS}
- **Artifact:** `reviews/slice-{N}-peer-review.md`

> If peer review has not yet run for this entry, write: Peer review pending.

#### QA Highlights

- **QA agents run:** {LIST -- e.g., QA Stats, QA Code Quality, QA Data Integrity, QA Security, QA UI/UX}
- **Critical/High findings:** {COUNT}
- **Key findings:** {BRIEF_SUMMARY_OF_TOP_FINDINGS}
- **Whiskey Team:** {RUN / PENDING} -- {KEY_FINDINGS_IF_RUN}
- **UX Sense Check:** {RUN / PENDING / N/A (backend slice)} -- {KEY_FINDINGS_IF_RUN}
- **Artifact:** `reviews/slice-{N}-qa-swarm.md`

> If QA has not yet run for this entry, write: QA pending.

#### Lessons Learned

- {LESSON_1 -- something that will save time in future sessions}
- {LESSON_2}

#### Owner Decisions Needed

- {DECISION_1 -- describe what the owner needs to decide and why the team cannot proceed without it}
- {DECISION_2}

> If no owner decisions are needed, write: No owner decisions needed.

#### Artifacts Produced

- {ARTIFACT_TYPE}: `{FILE_PATH}` -- {BRIEF_DESCRIPTION}
- {ARTIFACT_TYPE}: `{FILE_PATH}` -- {BRIEF_DESCRIPTION}

---

### Entry {ENTRY_NUMBER} -- {YYYY-MM-DD}

> Copy the entry block above for each new session.

---

## Running Summary

> Updated periodically (not every entry). High-level project health.

| Metric | Value |
|--------|-------|
| **Total slices planned** | {COUNT} |
| **Slices completed** | {COUNT} |
| **Slices in progress** | {COUNT} |
| **Slices blocked** | {COUNT} |
| **Overall quality gate pass rate** | {PERCENTAGE}% |
| **Total open blockers** | {COUNT} |
| **Owner decisions pending** | {COUNT} |
| **Estimated completion** | {DATE_OR_RANGE} |

---

## Decision Log Index

> Quick reference for key decisions. Link to the diary entry for full context.

| # | Date | Decision | Entry # |
|---|------|----------|---------|
| 1 | {YYYY-MM-DD} | {SHORT_DECISION_DESCRIPTION} | Entry {N} |
| 2 | {YYYY-MM-DD} | {SHORT_DECISION_DESCRIPTION} | Entry {N} |

---

## Blocker History

> All blockers encountered during the project, including resolved ones.

| # | Date Opened | Blocker | Impact | Date Resolved | Resolution |
|---|-------------|---------|--------|---------------|------------|
| 1 | {YYYY-MM-DD} | {DESCRIPTION} | {IMPACT} | {YYYY-MM-DD_OR_OPEN} | {HOW_IT_WAS_RESOLVED_OR_PENDING} |
