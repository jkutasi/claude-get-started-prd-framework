# Per-Slice Workflow: Phases I, J, and Post-Push

> Sub-file of [PER-SLICE-WORKFLOW-TEMPLATE.md](PER-SLICE-WORKFLOW-TEMPLATE.md). Contains Phases I, J, and Post-Push Verification.

```
PHASE I: DOCUMENTATION UPDATE
55. CTO delegates doc updates to Documentation Scribe (if available) or Architect
56. Designated agent updates affected docs via DOCS_MAP
57. If a discovery in this slice invalidates earlier diagrams, update them here

PHASE J: GATE CHECK + USER DELIVERY + POST-PUSH (Article 12 enforcement)
58. CTO runs: $ python scripts/gate_check.py --all (or --slice N [--frontend])
    Script auto-discovers slices and verifies ALL required artifacts exist on disk.
59. Required artifacts (always -- 7 per slice):
    - reviews/slice-N-test-spec.md, reviews/slice-N-test-review.md
    - reviews/slice-N-peer-review.md, reviews/slice-N-qa-swarm.md
    - reviews/slice-N-red-team-pre-build.md, reviews/slice-N-red-team.md
    - reviews/slice-N-whiskey-team.md
    Strict (from scripts/gate_check_artifacts.py):
    - reviews/slice-N-error-rescue-registry.md
    - reviews/slice-N-ux-sense-check.md (frontend slices)
    Plus: Gherkin feature file in features/, unit tests in tests/ or src/**/, all tests pass.
60. Script returns PASS or FAIL with specific missing items listed.
61. If FAIL: CTO fixes missing items. Does NOT start next slice.
62. If PASS: CTO presents completed slice to user (DONE work only -- never draft):
    - gate_check.py output as proof all artifacts exist
    - What was built (summary + screenshots/demos if applicable)
    - QA results (peer review verdict, QA swarm results, whiskey team verdict)
    - Any known limitations or trade-offs
    If user finds issues: spawn fix agents, run abbreviated QA, re-run gate_check.py, re-present.
63. Push to GitHub, then run POST-PUSH VERIFICATION.

POST-PUSH VERIFICATION (after every push to GitHub -- MANDATORY)

After pushing, the CTO MUST verify the deployment is healthy:

1. CHECK ERROR TRACKER (Sentry or project-equivalent -- via MCP, API, or dashboard):
   - Wait at least 2 minutes after push for error indexing propagation
   - Query for new errors in the last 15 minutes
   - Filter by the project and environment (preview/production)
   - If new errors found: treat as CRITICAL -- spawn fix agent immediately

2. CHECK DEPLOYMENT PLATFORM (Vercel/AWS/GCP/etc. -- via dashboard or CLI):
   - Verify the deployment succeeded (no build errors)
   - Check function logs for runtime errors
   - If deployment failed or has runtime errors: revert or fix immediately

   +------------------------------------------------------------------+
   | POST-PUSH GATE: CTO must confirm after every push:               |
   | [] "Error tracker checked -- no new errors in last 10 minutes"   |
   | [] "Deployment platform verified -- no build or runtime errors"  |
   | [] "Function/service logs clean -- no new exceptions"            |
   | If ANY check fails: fix immediately before starting new work.    |
   +------------------------------------------------------------------+
```

**If you are reading this and considering skipping the gate check script: DON'T. The script exists specifically because the CTO has demonstrated a tendency to skip reviews and move forward. The script is a mechanical check that cannot be rationalized away. Run it.**
