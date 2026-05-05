# Per-Slice Workflow: Phases I, J, and Post-Push

> Sub-file of [PER-SLICE-WORKFLOW-TEMPLATE.md](PER-SLICE-WORKFLOW-TEMPLATE.md). Contains Phases I, J, and Post-Push Verification.

```
PHASE I: DOCUMENTATION UPDATE
37. CTO delegates doc updates to Documentation Scribe (if available) or Architect
38. Designated agent updates affected docs via DOCS_MAP
39. If a discovery in this slice invalidates earlier diagrams, update them here

PHASE J: GATE CHECK + USER DELIVERY + PLAYWRIGHT REGRESSION (Article 12 enforcement)
40. CTO runs: $ python scripts/gate_check.py --all (or --slice N [--frontend])
    Script auto-discovers slices and verifies ALL required artifacts exist on disk.
41. Required artifacts (always -- consolidated file per slice):
    - reviews/slice-N.md (consolidated index, <=150 lines)
    Sections verified inside: Tests (B), Code Peer Review (E), QA + Runtime (F + F.5)
    Gate Check + Smoke (J), Post-Push (Sentry alert summary)
    Per-reviewer detail files in reviews/slice-N/ subdirectory.
    Plus: Gherkin feature file in features/, unit tests in tests/ or src/**/, all tests pass.
42. Script returns PASS or FAIL with specific missing items listed.
43. If FAIL: CTO fixes missing items. Does NOT start next slice.
44. PLAYWRIGHT REGRESSION SMOKE:
    - Run Playwright smoke test suite including 3-5 assertions on previously-shipped slices.
    - Assertions must verify behavior from at least the last 2 completed slices.
    - Any regression = fix before user delivery.
45. If PASS + smoke green: CTO presents completed slice to user (DONE work only):
    - gate_check.py output as proof all artifacts exist
    - What was built (summary + screenshots/demos if applicable)
    - QA results (peer review verdict, QA swarm results, Sentry clear)
    - Any known limitations or trade-offs
    If user finds issues: spawn fix agents, run abbreviated QA, re-run gate_check.py, re-present.
46. Push to GitHub, then run POST-PUSH VERIFICATION.

POST-PUSH VERIFICATION (after every push to GitHub -- MANDATORY)

After pushing, the CTO MUST verify the deployment is healthy via automated relay-sentry:

1. relay-sentry MCP POLL (load skill: /relay-sentry):
   - Wait at least 2 minutes after push for error indexing propagation
   - Query for new errors in the last 15 minutes
   - Filter by the project and environment (preview/production)
   - Sentry-to-GitHub Issues integration surfaces critical errors automatically
   - If new errors found: treat as CRITICAL -- spawn fix agent immediately

2. CHECK DEPLOYMENT PLATFORM (Vercel/AWS/GCP/etc. -- via dashboard or CLI):
   - Verify the deployment succeeded (no build errors)
   - Check function logs for runtime errors
   - If deployment failed or has runtime errors: revert or fix immediately

   +------------------------------------------------------------------+
   | POST-PUSH GATE: CTO must confirm after every push:               |
   | [] "relay-sentry polled -- no new errors in last 10 minutes"     |
   | [] "Deployment platform verified -- no build or runtime errors"  |
   | [] "Function/service logs clean -- no new exceptions"            |
   | If ANY check fails: fix immediately before starting new work.    |
   +------------------------------------------------------------------+
```

**If you are reading this and considering skipping the gate check script: DON'T. The script exists specifically because the CTO has demonstrated a tendency to skip reviews and move forward. The script is a mechanical check that cannot be rationalized away. Run it.**
