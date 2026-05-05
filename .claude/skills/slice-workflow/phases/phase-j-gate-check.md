# Phase J: Gate Check + User Delivery + Post-Push Verification

> Load this file when starting Phase J. This is the final phase before the slice is complete.
> For deploy-SHA preconditions see Article 39.

## Purpose

Mechanically verify all artifacts exist, deliver the completed slice to the user (I.5 folded in here), push to GitHub, and verify the deployment is healthy.

## Section 1: Mechanical Gate Check

1. CTO runs: `python scripts/gate_check.py --all` (or `--slice N [--frontend]`)
2. The script auto-discovers slices and verifies ALL required artifacts exist on disk.
3. If **FAIL**: fix missing items. Do NOT start next slice.
4. If **PASS**: proceed to User Delivery (Section 2), then push.

### Required Artifacts Verified by gate_check.py

Always required (7 files per slice):
- `reviews/slice-N-test-spec.md`
- `reviews/slice-N-test-review.md`
- `reviews/slice-N-peer-review.md`
- `reviews/slice-N-qa-swarm.md`
- `reviews/slice-N-red-team-pre-build.md`
- `reviews/slice-N-red-team.md`
- `reviews/slice-N-whiskey-team.md`

Strict (from `scripts/gate_check_artifacts.py`):
- `reviews/slice-N-error-rescue-registry.md`
- `reviews/slice-N-ux-sense-check.md` (frontend slices only)

Additional: Gherkin feature file in `features/`, unit test files in `tests/` or `src/**/`, all tests pass.

## Section 2: User Delivery (folded from I.5)

**USER PRESENTATION RULE: present DONE work only — never a draft.**

After gate_check.py returns PASS, CTO presents the completed slice to the user:
- What was built (summary + screenshots/demos if applicable)
- gate_check.py output as proof all artifacts exist
- QA results summary (peer review verdict, QA swarm, whiskey team verdict)
- Any known limitations or trade-offs

If the user finds issues: spawn fix agents, run abbreviated QA, re-run gate_check.py, then re-present.

## Section 3: Post-Push Verification (MANDATORY after every push)

After pushing, the CTO MUST verify the deployment is healthy:

### 3.1: Check Error Tracker (Sentry or equivalent)

- Wait at least 2 minutes after push for error indexing propagation.
- Query for new errors in the last 15 minutes.
- Filter by project and environment (preview/production).
- If new errors found: treat as **CRITICAL** — spawn fix agent immediately.

### 3.2: Check Deployment Platform (Vercel/AWS/GCP/etc.)

- Verify the deployment succeeded (no build errors).
- Check function logs for runtime errors.
- If deployment failed or has runtime errors: revert or fix immediately.

## Gate

```
+------------------------------------------------------------------+
| PHASE J GATE: CTO must confirm:                                  |
| [] "gate_check.py --all returned PASS"                           |
| [] "All 7 always-required artifacts exist on disk"               |
| [] "Strict artifacts verified (error-rescue, ux-sense if fe)"    |
| [] "User delivery completed — presented DONE work with proof"    |
| [] "Error tracker checked — no new errors in last 10 minutes"    |
| [] "Deployment platform verified — no build or runtime errors"   |
| [] "Function/service logs clean — no new exceptions"             |
| If ANY check fails: fix immediately before starting new work.    |
+------------------------------------------------------------------+
```

## Slice Complete

> **QMD SAVE** (non-blocking, conditional): If deployment issues were found, spawn `/relay-qmd` — save to `vault/projects/{PROJECT_NAME}/deployment-issues-slice-{N}.md`. Skip if no issues or QMD unavailable.

If all gates pass, the slice is DONE. Proceed to the next slice (Slice N+1) starting from Phase A.

**Remember Nuclear Rule 8:** Slice N must be fully complete before ANY work on Slice N+1.
