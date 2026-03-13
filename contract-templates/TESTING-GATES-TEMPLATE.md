# Testing Gates & Enforcement — {PROJECT_NAME}

> Part of the testing contract. See also: [Testing Pyramid](TESTING-PYRAMID-TEMPLATE.md) and [Testing Procedures](TESTING-PROCEDURES-TEMPLATE.md).

## Autonomous Defect Resolution Protocol

**Applies to ALL testing phases:**
- **Phase F (QA Swarm):** QA agents fix bugs inline via fix sub-agents
- **Phase G (Fix Verification):** CTO verifies autonomous fixes, handles escalations
- **Phase H (Regression Check):** Regressions found are fixed autonomously
- **E2E Browser Testing:** Write regression test + fix component via fix sub-agent
- **Peer Review (Phase E):** Mandatory-fix findings — implementing agent applies protocol

Triggered by ANY source: user bug report, QA finding, security scan, Whiskey Team finding, peer review consensus finding, regression detection.

**Fix Ownership Rule:** The agent that finds the defect owns the fix lifecycle. It spawns a **fix sub-agent** (ephemeral coder) to execute the steps below, verifies each step, and reports the resolution. The finding agent does NOT write production code itself. This preserves role separation while eliminating the bottleneck of routing every fix through the CTO.

```
Step 1: AUDIT THE TEST
  Find the test that SHOULD have caught this defect.
  - Test exists but didn't catch it -> FIX THE TEST FIRST
  - No test exists -> Add Gherkin scenario first, then write test

Step 2: RED
  Run the corrected/new test against current (buggy) code. It MUST FAIL.
  - If it passes -> test still wrong, go back to Step 1

Step 3: GREEN
  Fix sub-agent fixes the production code until the test passes.

Step 4: REGRESSION
  Run the FULL test suite. Zero regressions allowed.

Step 5: CLASS SCAN
  Does this defect reveal a CATEGORY of missing coverage?
  - If yes: scan the ENTIRE codebase for all instances of the same pattern
  - Write tests for ALL instances, fix ALL instances in the same pass
  - Example: missing null-check on one endpoint -> check ALL endpoints

Step 6: COMMIT
  Test + fix committed together as an atomic unit.
  Commit message references the finding ID and class scan scope.
```

**The test is always the source of truth.** A bug means the test was incomplete or wrong. Fix the test first, then fix the code. This ensures every bug found once is caught forever.

**Escalate to the user ONLY when:**
- The fix requires an architectural decision that changes the system design
- The fix modifies infrastructure outside the current workspace
- The fix has failed 3 times (3 fix sub-agent attempts)

---

## Browser Testing Protocol

| Tool | Use Case | When |
|------|----------|------|
| **agent-browser (Vercel)** | All interactive browser QA, persona testing, exploratory testing, visual checks | MANDATORY for all browser QA during slice development |
| **Playwright** | Automated regression scripts, CI/CD pipeline checks, headless screenshot comparison | OPTIONAL, for regression automation only |

**agent-browser is not optional.** If a QA agent or UX Sense Check agent needs to interact with a browser, it uses agent-browser. No exceptions.

---

## Slice 0 Tooling Gate (Blocks Slice 1)

Before ANY feature code is written, the following tooling infrastructure must exist. Run `gate_check.py --slice 0` to verify mechanically. **If any check fails, Slice 1 CANNOT start.**

| # | Check | How gate_check.py Verifies |
|---|-------|---------------------------|
| 1 | **Structured logger file exists** | `src/shared/logging/logger.{EXT}` is a non-empty file |
| 2 | **Sentry DSN configured** | `.env` contains `SENTRY_DSN=` with a non-empty value |
| 3 | **Sentry receives test event** | Manual verification during Slice 0 (documented in bootstrap) |
| 4 | **Linter config exists** | `pyproject.toml [tool.ruff]` (Python) or `.eslintrc*`/`eslint.config.*` (JS/TS) |
| 5 | **Pre-push hook exists** | `.husky/pre-push` exists and is executable |
| 6 | **No raw console output** | Zero `console.log/error/warn` or `print()` calls in `src/` (excluding tests) |

**Why this gate exists:** A project ran through 8 slices with full QA and the process never caught that Pino, Ruff, and Sentry were never installed. The docs said the right things but nothing forced implementation. Documentation without enforcement is theater.

---

## Slice Gate Enforcement Checklist

Before a slice can ship, the gate check script (`python gate_check.py --slice N`) verifies:

- [ ] `reviews/slice-N-test-spec.md` exists and is non-empty
- [ ] `reviews/slice-N-test-review.md` exists and is non-empty
- [ ] `reviews/slice-N-peer-review.md` exists and is non-empty
- [ ] `reviews/slice-N-qa-swarm.md` exists and is non-empty
- [ ] `reviews/slice-N-red-team-pre-build.md` exists and is non-empty
- [ ] `reviews/slice-N-red-team.md` exists and is non-empty
- [ ] `reviews/slice-N-whiskey-team.md` exists and is non-empty
- [ ] `reviews/slice-N-ux-sense-check.md` exists (frontend slices, enabled with `--frontend`)
- [ ] At least one Gherkin feature file exists: `features/slice-N-*.feature`
- [ ] At least one unit test file exists: `tests/*slice_N*` or `tests/*slice-N*`
- [ ] All tests pass
- [ ] Unit test coverage ≥ 90% on business logic + public interfaces (exemptions documented)

**File location:** Unit tests live in the feature folder alongside the service file: `src/{feature-name}/{feature-name}.test.{EXT}`. Cross-feature integration tests live in `tests/integration/`. See Article 20a for the full directory structure.

**If the script returns FAIL, the slice has NOT shipped. Do NOT start the next slice.**

---

## Goal Achievement Test Requirement

Every slice MUST include a Goal Achievement Test (Article 15, item #1). This is a single Gherkin scenario tagged `@goal-achievement @critical` that validates the complete user workflow from start to finish.

The Goal Achievement Test is a **hard gate:** if the system does not achieve its stated goal, the slice FAILS regardless of all other tests passing. There is no partial credit -- the user either achieves their goal or they do not.

See `examples/gherkin-examples.md` Template 5 for the Goal Achievement Test format.

---

## Nuclear Rules Reminder

These nine rules override everything else. Violation = immediate stop.

1. **CTO Never Writes Code.** All code via teammates and sub-agents. No exceptions.
2. **Peer Review Is Mandatory.** Every slice, every time. All reviewers must report. No partial reviews.
3. **Slices Ship Complete.** All gates passed, all artifacts on disk, or the slice is invalid. No starting the next slice until this one is fully done.
4. **Repository Hygiene Before Push.** Before ANY push, verify no personal notes, scratch files, or `ZZ *` folders are staged. `.gitignore` must exclude these paths.
5. **One Concern Per Sub-Agent — Then It Dies.** Every sub-agent gets one concern, does it, and is dismissed. No reuse.
6. **No Hacking — No Lint Ignores.** All lint/type errors are bugs. No `# noqa`, `eslint-disable`, `# type: ignore`. Fix properly.
7. **Never Commit Without Checking Runtime Errors.** Check error tracker, logs, and health endpoints before commit.
8. **Slices Ship One at a Time.** Slice N fully complete before Slice N+1. Parallel within a slice = good. Parallel slices = bad.
9. **File Structure Defined Before Implementation.** Planning phase defines exact file map. Sub-agents build to the map.

Testing is not a phase you "get to later." Tests are written FIRST (Phase B) by independent test-writer sub-agents, before any implementation code exists (Phase C). Code without tests is incomplete. Tests without peer review are untrusted. QA without artifacts on disk is unproven.
