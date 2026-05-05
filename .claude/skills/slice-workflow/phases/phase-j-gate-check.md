# Phase J: Gate Check + User Delivery + Playwright Regression Smoke

> Load this file when starting Phase J. This is the final phase before the slice is complete.
> For deploy-SHA preconditions see Article 39.

## Purpose

Mechanically verify all artifacts exist, run Playwright regression smoke (including assertions
on previously-shipped slices), deliver the completed slice to the user, push to GitHub, and
verify the deployment is healthy via relay-sentry.

## Section 1: Mechanical Gate Check

1. CTO runs: `python scripts/gate_check.py --all` (or `--slice N [--frontend]`)
2. The script auto-discovers slices and verifies ALL required artifacts exist on disk.
3. If **FAIL**: fix missing items. Do NOT start next slice.
4. If **PASS**: proceed to Playwright regression smoke.

### Required Artifacts Verified by gate_check.py

Consolidated review index (1 file per slice, <=150 lines):
- `reviews/slice-N.md` — must contain all 5 sections

Per-reviewer detail files (each <=150 lines) in `reviews/slice-N/`:
- Tests: `reviews/slice-N-test-spec.md`, `reviews/slice-N-test-review.md`
- Code Peer Review: detail files per reviewer
- QA + Runtime: `reviews/slice-N-qa-swarm.md`, per-check detail files
- Sentry summary in consolidated file

Additional: Gherkin feature file in `features/`, unit test files in `tests/` or `src/**/`, all tests pass.
Frontend slices: `reviews/slice-N-ux-sense-check.md` required.

## Section 2: Playwright Regression Smoke

5. Run the Playwright smoke test suite.
6. Smoke suite MUST include 3-5 assertions verifying behavior from previously-shipped slices:
   - Minimum: cover at least the last 2 completed slices.
   - Assertions should test user-visible behavior (not implementation details).
   - Examples: key page renders, critical API endpoints respond, auth flows work.
7. If any regression assertion fails: spawn fix agent, resolve, re-run smoke before delivery.
8. Playwright smoke green = prerequisite for user delivery.

## Section 3: User Delivery

**USER PRESENTATION RULE: present DONE work only — never a draft.**

After gate_check.py PASS and smoke green, CTO presents the completed slice to the user:
- What was built (summary + screenshots/demos if applicable)
- gate_check.py output as proof all artifacts exist
- QA results summary (peer review verdict, QA swarm results, Sentry clear)
- Playwright regression smoke result (X/Y assertions on prior slices passed)
- Any known limitations or trade-offs

If the user finds issues: spawn fix agents, run abbreviated QA, re-run gate_check.py, re-present.

## Section 4: Post-Push Verification (MANDATORY after every push)

After pushing, the CTO MUST verify the deployment is healthy via relay-sentry:

### 4.1: Poll Sentry via relay-sentry MCP

- Load skill: `/relay-sentry`
- Wait at least 2 minutes after push for error indexing propagation.
- Query for new errors in the last 15 minutes, this project + environment.
- Sentry-to-GitHub Issues integration surfaces critical errors automatically.
- If new errors found: treat as **CRITICAL** — spawn fix agent immediately.

### 4.2: Check Deployment Platform (Vercel/AWS/GCP/etc.)

- Verify the deployment succeeded (no build errors).
- Check function logs for runtime errors.
- If deployment failed or has runtime errors: revert or fix immediately.

## Gate

```
+------------------------------------------------------------------+
| PHASE J GATE: CTO must confirm:                                  |
| [] "gate_check.py --all returned PASS"                           |
| [] "All required artifacts exist on disk"                        |
| [] "Playwright smoke green (3-5 prior-slice assertions passed)"  |
| [] "User delivery completed -- presented DONE work with proof"   |
| [] "relay-sentry polled -- no new errors in last 10 minutes"     |
| [] "Deployment platform verified -- no build or runtime errors"  |
| [] "Function/service logs clean -- no new exceptions"            |
| If ANY check fails: fix immediately before starting new work.    |
+------------------------------------------------------------------+
```

## Artifacts

- Consolidated: `reviews/slice-{N}.md` (section: Gate Check + Smoke, Post-Push)

## Slice Complete

> **QMD SAVE** (non-blocking, conditional): If deployment issues were found, spawn `/relay-qmd` — save to `vault/projects/{PROJECT_NAME}/deployment-issues-slice-{N}.md`. Skip if no issues or QMD unavailable.

If all gates pass, the slice is DONE. Proceed to the next slice (Slice N+1) starting from Phase A.

**Remember Nuclear Rule 8:** Slice N must be fully complete before ANY work on Slice N+1.
