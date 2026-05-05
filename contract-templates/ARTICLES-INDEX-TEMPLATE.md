# Articles Quick Reference — {PROJECT_NAME}

> **Loaded on demand.** The CTO loads this file when it needs to find which article covers a topic. Do not keep in memory — consult as needed.

Articles 1-35 define the detailed rules of engagement. They are stored individually in `contracts/articles/` — one file per article.

> **Full article definitions:** Start with `contracts/articles/INDEX.md` for the full listing.
> Load only the specific article file you need, not the entire directory.

## Article Index

| Article | Topic | When to Consult |
|---------|-------|-----------------|
| 1 | Code authorship prohibition (no exceptions) | When tempted to write code directly |
| 2 | Sub-agent code authorship (one task per agent) | When assigning implementation |
| 3 | Multi-model peer review (3+ external models) | When running peer review |
| 4 | QA swarm requirement (7 mandatory agents) | When running QA |
| 5 | Context window management (DOCS_MAP first) | When loading documentation |
| 6 | Contract enforcement (violation logging) | When a violation occurs |
| 7 | Slice completion criteria (17-point gate) | Before declaring a slice shipped |
| 7b-7e | Self-reflection, QA protocol, dynamic agents | During QA and implementation |
| 8 | Model right-sizing (Opus = CTO only) | When selecting models |
| 9 | Infrastructure isolation (sister projects) | When near existing systems |
| 10 | Descriptive naming convention | During code review |
| 11 | Documentation navigation | When searching for docs |
| 12 | Nuclear rule enforcement (supreme directive) | When reviewing process compliance |
| 13 | Background agent management | When running parallel agents |
| 14 | Red Team adversarial review (10 dimensions) | Phase A.7 only (optional --high-risk); QA escalation path |
| 15 | Whiskey Team (8 test areas + 6 regression) — **DEPRECATED 2026-05-05** | Historical reference only |
| 16 | UX Sense Check (3 personas, 7 test areas) | During Phase F (frontend slices) |
| 17 | Test-First Specification Protocol | During Phase B (Gherkin audit + test spec) |
| 18 | Test Peer Review Protocol | During Phase B.3 (test code peer review) |
| 19 | User Scope Confirmation Protocol | During Phase A.6 (user confirms slice scope) |
| 20 | Code Architecture Standards (8 subsections) | During implementation, code review, and QA |
| 21 | Commit vs. push + post-push verification | Commit vs. push workflow, post-push monitoring |
| 22 | Commit workflow job sizing | Review depth for a change |
| 23 | Linting, pre-push hooks + secrets scanning | Setting up Husky, diagnosing push failures, secrets scanning |
| 24 | Sub-agent separation | Spawning sub-agents for implementation |
| 25 | Backend QA sweep | Running backend QA sweep |
| 26 | BFF pattern | Designing API endpoints for frontend views |
| 27 | Post-work hygiene + push safety | Finishing a task, dismissing agents, pre-push and post-push verification |
| 28 | Service log inventory | Diagnosing missing logs or adding observability |
| 29 | Planning decomposition | Planning a slice (decomposing into concerns) |
| 30 | File map specification | Creating file maps before implementation |
| 31 | Parallel execution | Deciding whether to parallelize work |
| 32 | Repo hygiene checklist | Preparing to push to remote |
| 33 | Conventions and project structure | Defining project conventions or folder structure |
| 34 | Error diagnosis protocol | Diagnosing runtime errors |
| 35 | Error & Rescue Registry | Phase C self-check — mapping failure points, finding silent failures |

## Key Procedures

- **How to run peer review:** Article 12b — spawn 4 adversarial reviewer sub-agents (Gemini, OpenAI 5.5, Opus 4.7, Grok), synthesize, save artifact
- **How to run QA swarm:** Article 12c — spawn QA agents via `openai_code.py qa --check <type>`; UX Sense Check optional (frontend only)
- **Session start checklist:** Article 12e — read CLAUDE.md, check keys, run gate check
- **Commit convention:** Article 12g — include Reviewed-By and QA-Passed lines

## Required Review Artifacts (consolidated pattern)

**One consolidated file per slice:**
- `reviews/slice-N.md` — 5 sections: Test Spec, Test Review, Peer Review, QA + Runtime, Red Team (if A.7)

**Per-reviewer / per-check detail files under `reviews/slice-N/`:**
- `peer-review-gemini.md`, `peer-review-openai.md`, `peer-review-grok.md` (Articles 03, 18)
- `qa-code-quality.md`, `qa-data-integrity.md`, `qa-security.md`, `qa-uiux.md` (Article 04)
- `red-team-pre-build.md` (Article 14 — only if Phase A.7 run; else "N/A" in Section 5)
- `red-team-escalation.md` (Article 14b — only if QA escalation triggered)
- `professor-pre-build.md`, `professor.md` (if escalation triggered)
- `ux-sense-check.md` (Article 16 — frontend slices only)
