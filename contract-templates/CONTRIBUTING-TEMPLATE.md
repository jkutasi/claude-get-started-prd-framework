# Contributing to {PROJECT_NAME}

## Code Authorship Model

The CTO Orchestrator (Opus) does NOT write code. All implementation is performed by teammates and sub-agents (Sonnet). The CTO delegates, reviews, and synthesizes. If you are the CTO and about to write code: STOP. Spawn a teammate or sub-agent.

This is not a suggestion. The entire architecture -- context window management, peer review, QA -- depends on the CTO delegating to teammates and sub-agents. Writing code directly burns the CTO's context window on implementation details, skips peer review, skips QA, and produces lower-quality output.

---

## Code Standards

- **Type hints:** All function signatures MUST include type hints. No untyped public functions.
- **Docstrings:** Every module, class, and public function MUST have a docstring explaining purpose, parameters, and return values.
- **Linting:** All code MUST pass the project linter ({LINTER_NAME}) with zero warnings before peer review.
- **Formatting:** All code MUST be formatted with {FORMATTER_NAME}. No manual formatting debates.
- **Language:** {PRIMARY_LANGUAGE} {VERSION}. No other languages unless explicitly approved by the owner.
- **Feature folders (Article 20a):** All production code lives in `src/{feature-name}/` folders. Each feature contains its route, service, repository, test, and types files. No flat `src/` dumps.
- **Three-layer separation (Article 20b):** Route files handle HTTP only (~20-30 lines). Service files handle business logic only (~80-150 lines). Repository files handle data access only (~50-100 lines). No layer violations.
- **150-line file limit (Article 20c):** Every production source file must stay under 150 lines (excluding comments and blank lines). Files exceeding this limit have too many concerns and must be split.
- **Structured logging (Article 20e):** No `console.log`, `print()`, or equivalent in committed code. Use the project's structured logger (`{STRUCTURED_LOGGER}`). All log entries are structured JSON with level, message, and context.
- **Error wrapping (Article 20f):** All errors must be wrapped with AppError (or project equivalent) including context (operation, parameters, cause). No bare `throw new Error()` or `raise Exception()`.
- **Display-only frontend (Article 20d):** Frontend components render data from the API. No business calculations, filtering by business rules, or conditional business logic in client components.
- **No lint suppression (Nuclear Rule 6):** No `# noqa`, `eslint-disable`, `# type: ignore`, or any other lint/type suppression comments. All lint and type errors are real bugs and must be fixed properly.
- **Runtime verification required (Nuclear Rule 7):** Before every commit, check the error tracker, application logs, and health endpoints. After every push, check Sentry for new errors and Vercel deployment logs for failures. No code ships without confirming runtime is clean.

---

## Naming Convention (Article 10)

ALL files, directories, branches, variables, functions, and classes MUST be named descriptively. No random or auto-generated names. No abbreviations without context. Names must be self-documenting.

| Good | Bad | Why |
|------|-----|-----|
| `user_auth_service.py` | `module2.py` | Says what it does |
| `slice-2-data-validation.md` | `distributed-whistling-aurora.md` | No auto-generated names |
| `calculate_portfolio_nav()` | `calc()` | Self-documenting |
| `{EXAMPLE_GOOD_NAME}` | `{EXAMPLE_BAD_NAME}` | {EXAMPLE_REASON} |

Naming violations are flagged as mandatory fixes during peer review.

---

## Commit Convention (Article 12g)

Every commit MUST include proof of review:

```
[Slice N] Brief description of what changed

- Detail 1
- Detail 2

Co-Authored-By: {AGENT_NAME} ({MODEL})
Reviewed-By: Reviewer Gemini, Reviewer OpenAI Codex, Reviewer Grok
QA-Passed: QA Stats, QA Code Quality, QA Data Integrity, QA Security, QA UI/UX
Red-Team: Passed (reviews/slice-N-red-team.md)
Professor-Review: Passed (reviews/slice-N-professor.md)
Whiskey-Team: Passed (reviews/slice-N-whiskey-team.md)
```

Commits WITHOUT `Reviewed-By` and `QA-Passed` lines are CONTRACT VIOLATIONS.

---

## Review Requirements (Articles 3, 4, 12)

1. **Peer Review (Article 3):** All code is reviewed by 4 independent external models (Gemini, OpenAI 5.5, Opus 4.7, Grok). Issues flagged by 2+ reviewers are mandatory fixes. Results saved to `reviews/slice-N-peer-review.md`.
2. **QA Swarm (Article 4):** All code passes a 5-agent QA swarm after peer review. Results saved to `reviews/slice-N-qa-swarm.md`.
3. **Red Team (Article 14):** Adversarial security review. Results saved to `reviews/slice-N-red-team.md`.
4. **Professor Review:** Domain expert review by selected professors (Architecture, Testing, Security, etc.). Results saved to `reviews/slice-N-professor.md`.
5. **Whiskey Team (Article 15):** Adversarial QA + implicit regression. Results saved to `reviews/slice-N-whiskey-team.md`.
6. **UX Sense Check (Article 16):** Persona-based browser testing for frontend slices. Results saved to `reviews/slice-N-ux-sense-check.md`.

No review may be skipped. No partial reviews. All reviewers must return findings before proceeding.

---

## PR / Per-Slice Workflow

Each slice follows the mandatory workflow phases:

1. **Phase A:** CTO reviews requirements, researcher gathers docs, Architect creates per-slice diagrams
2. **Phase A.5:** Doc bootstrap (Slice 0) + high-level diagram review. Per-slice diagrams (Slices 1+, non-blocking).
3. **Phase A.6:** User Scope Confirmation — user reviews and approves slice scope
4. **Phase A.7:** Red Team pre-build gate (10 attack dimensions) + Professor pre-build review (domain experts)
5. **Phase B:** Gherkin audit (B.1) + test-writer sub-agents write ALL tests (B.2, must be RED) + test peer review (B.3)
6. **Phase C:** CTO assigns implementation to coder teammates. Coders write code until tests PASS.
7. **Phase D:** Each coder self-reflects on their own code before peer review
8. **Phase E:** 4 peer reviewers run in parallel (Gemini, OpenAI 5.5, Opus, Grok). CTO synthesizes consensus findings
9. **Phase F:** QA swarm + Whiskey Team + UX Sense Check run in parallel. Each QA agent applies Autonomous Defect Resolution Protocol (Article 17e) for any defect found. QA Manager formats findings + fix results.
10. **Phase G:** CTO verifies autonomous fixes from Phase F. Handles escalated items (architectural/infrastructure/3x-failed). Red Team post-QA review of aggregate changes.
11. **Phase H:** Regression check + implicit behavior regression (6 categories)
12. **Phase I:** Documentation Scribe updates all affected docs
13. **Phase I.5:** User Delivery — CTO presents DONE slice to user with all QA results. User only sees fully-vetted work, never a draft.
14. **Phase J:** Mechanical gate check (`python gate_check.py --slice N`)
15. **Post-Push:** After every push — check Sentry (new errors?), Vercel deployment logs (build/runtime failures?). Fix before starting new work.

---

## Gate Verification Checklist

Before a slice ships, ALL of the following must be confirmed:

- [ ] Gherkin audit passed (completeness + quality) -- Article 17
- [ ] All tests written by test-writer sub-agents (not implementation coders)
- [ ] All Gherkin scenarios pass
- [ ] All 3+ peer reviewers reviewed and approved (or consensus fixes resolved)
- [ ] All QA agents ran and passed
- [ ] Red Team review completed (Article 14)
- [ ] Professor Review completed
- [ ] Whiskey Team review completed (Article 15)
- [ ] UX Sense Check completed (Article 16, if frontend slice)
- [ ] Unit test coverage >= 90% on business logic + public interfaces (exemptions documented)
- [ ] Documentation Scribe has updated all affected docs
- [ ] CTO did NOT write any code or test code during this entire slice
- [ ] `reviews/slice-N-test-spec.md` EXISTS on disk
- [ ] `reviews/slice-N-test-review.md` EXISTS on disk
- [ ] `reviews/slice-N-peer-review.md` EXISTS on disk
- [ ] `reviews/slice-N-qa-swarm.md` EXISTS on disk
- [ ] `reviews/slice-N-red-team-pre-build.md` EXISTS on disk
- [ ] `reviews/slice-N-red-team.md` EXISTS on disk
- [ ] `reviews/slice-N-professor-pre-build.md` EXISTS on disk
- [ ] `reviews/slice-N-professor.md` EXISTS on disk
- [ ] `reviews/slice-N-whiskey-team.md` EXISTS on disk
- [ ] `reviews/slice-N-ux-sense-check.md` EXISTS on disk (if frontend)
- [ ] Lint/type zero suppressions — no `# noqa`, `eslint-disable`, `# type: ignore` anywhere in codebase
- [ ] Runtime verification clean — error tracker, logs, and health endpoints checked before commit
- [ ] `python gate_check.py --slice N` returns PASS

**If ANY box is unchecked, the slice has NOT shipped. Do NOT start the next slice.**

---

## Nuclear Rules Reminder

These nine rules override everything else. Violation = immediate stop.

1. **CTO Never Writes Code.** All code via teammates and sub-agents. No exceptions.
2. **Peer Review Is Mandatory.** Every slice, every time. All reviewers must report. No partial reviews.
3. **Slices Ship Complete.** All gates passed, all artifacts on disk, or the slice is invalid. The user only sees completed, fully-vetted slices. Never present unreviewed work and never defer QA to "after user tests."
4. **Repository Hygiene Before Push.** Before ANY push, verify no personal notes, scratch files, or `ZZ *` folders are staged. `.gitignore` must exclude these paths. This repository may be PUBLIC — verify no secrets, proprietary data, credentials, stale files, or internal-only content is staged. Run the Pre-Push Public Repo Checklist (SECURITY.md).
5. **One Concern Per Sub-Agent — Then It Dies.** Every sub-agent gets one concern, does it, and is dismissed. No reuse.
6. **No Hacking — No Lint Ignores.** All lint/type errors are bugs. No `# noqa`, `eslint-disable`, `# type: ignore`. Fix properly.
7. **Never Commit or Push Without Checking Runtime Errors.** Check error tracker, logs, and health endpoints before commit. After push: check Sentry for new errors and Vercel deployment logs for failures.
8. **Slices Ship One at a Time.** Slice N fully complete before Slice N+1. Parallel within a slice = good. Parallel slices = bad.
9. **File Structure Defined Before Implementation.** Planning phase defines exact file map. Sub-agents build to the map.
