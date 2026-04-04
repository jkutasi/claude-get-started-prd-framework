# Phase J: Mechanical Gate Check + Post-Push Verification

> Load this file when starting Phase J. This is the final phase before the slice is complete.

## Purpose

Mechanically verify all artifacts exist, push to GitHub, and verify the deployment is healthy.

## Section 1: Mechanical Gate Check

1. CTO runs: `python gate_check.py --slice N [--frontend]`
2. The script verifies ALL artifacts exist on disk (10 review files per slice).
3. If **FAIL**: fix missing items. Do NOT start next slice.
4. If **PASS**: push to GitHub, then run Post-Push Verification.

## Section 2: Post-Push Verification (MANDATORY after every push)

After pushing, the CTO MUST verify the deployment is healthy:

### 2.1: Check Error Tracker (Sentry or equivalent)

5. Wait at least 2 minutes after push for error indexing propagation.
6. Query for new errors in the last 15 minutes.
7. Filter by project and environment (preview/production).
8. If new errors found: treat as **CRITICAL** — spawn fix agent immediately.

### 2.2: Check Deployment Platform (Vercel/AWS/GCP/etc.)

9. Verify the deployment succeeded (no build errors).
10. Check function logs for runtime errors.
11. If deployment failed or has runtime errors: revert or fix immediately.

### 2.3: Check Greptile (if configured)

12. Run a codebase-aware scan on the pushed changes.
13. Review cross-file consistency findings.
14. Consensus findings = mandatory fixes (same as peer review rules).

## Post-Push Gate

```
+------------------------------------------------------------------+
| POST-PUSH GATE: CTO must confirm after every push:               |
| [] "Error tracker checked — no new errors in last 10 minutes"    |
| [] "Deployment platform verified — no build or runtime errors"   |
| [] "Function/service logs clean — no new exceptions"             |
| [] "Greptile scan completed (if configured) — findings reviewed" |
| If ANY check fails: fix immediately before starting new work.    |
+------------------------------------------------------------------+
```

## Slice Complete

> **QMD SAVE** (non-blocking, conditional): If any deployment issues were found during post-push verification, spawn `/relay-qmd` — save them to `vault/projects/{PROJECT_NAME}/deployment-issues-slice-{N}.md`. Only save if issues occurred. If QMD unavailable, skip.

If all gates pass, the slice is DONE. You may now proceed to the next slice (Slice N+1), starting from Phase A.

**Remember Nuclear Rule 8:** Slice N must be fully complete before ANY work on Slice N+1.
