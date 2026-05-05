# Step 4b: Per-Slice Workflow — Phases E through Post-Push

> Sub-file of [04-per-slice-workflow.md](04-per-slice-workflow.md). Contains Phases E, F, F.5, I, J, and Post-Push Verification.

```
PHASE E: PEER REVIEW (4 models, adversarial, parallel)
NOTE: Peer review applies to ALL code changes including refactoring.
Refactoring is not exempt from peer review, QA, or security review.
Moving code between files can introduce security regressions.
22. 4 reviewers run in parallel (smartest-of-each-provider):
    - Gemini (smartest available) -- architecture
    - OpenAI 5.5 via openai_code.py -- invariants/security/150-line
      python scripts/openai_code.py qa --code <path> --check code-quality --slice <N>
    - Claude Opus 4.7 -- independent review
    - Grok (smartest available) -- security/edge-case

   +-----------------------------------------------------------------+
   | NUCLEAR GATE E: CTO must confirm:                               |
   | [] "ALL 4 reviewers returned findings before proceeding"        |
   | [] "Consensus issues (2+ reviewers) identified as mandatory"    |
   | [] "Round 2 completed after fixes -- no new consensus issues"   |
   | [] "Section 3 of reviews/slice-N.md written and non-empty"     |
   +-----------------------------------------------------------------+

23. CTO synthesizes: consensus (2+) = mandatory fixes. Round 2 mandatory after fixes.
    Consolidated output: reviews/slice-{N}.md (section: Code Peer Review)

PHASE F: QA SWARM + UX SENSE CHECK (AUTONOMOUS FIX)
24. 7 QA agents run in parallel via OpenAI 5.5 script:
    python scripts/openai_code.py qa --code <path> --check <type> --slice <N>
    Types: api-contract | backend | routing | data-integrity | code-quality | security | uiux
    Each agent applies Autonomous Defect Resolution Protocol (Article 17e):
    find bug -> spawn fix sub-agent -> AUDIT/RED/GREEN/REGRESSION/CLASS SCAN/COMMIT
25. UX Sense Check -- 3 personas navigate via agent-browser (frontend slices only)
    All run under QA Lead coordination.
26. QA Manager synthesizes ALL findings + autonomous fix results
    Consolidated output: reviews/slice-{N}.md (section: QA + Runtime)

PHASE F.5: AUTOMATED SENTRY CHECK (relay-sentry MCP polling -- MANDATORY)
After the QA swarm completes, relay-sentry polls Sentry automatically.

27. Load skill /relay-sentry:
    - Query window: errors in last 30 minutes, this project + environment
    - Check both frontend (browser SDK) and backend (server SDK) feeds
    - Sentry-to-GitHub Issues integration surfaces critical errors automatically
    - Any new error = CRITICAL finding, must be resolved before Phase I
28. VERIFY STRUCTURED LOGGER IS USED:
    - Grep for raw console.log/error/warn or print() in src/ (excluding tests)
    - Any raw console output found = CRITICAL

   +-----------------------------------------------------------------+
   | RUNTIME LOG GATE F.5: Before proceeding to Phase I:            |
   | [] "relay-sentry MCP polled -- summary reviewed"               |
   | [] "All CRITICAL Sentry errors from QA session resolved"       |
   | [] "No raw console.log/error/warn or print() in src/ code"     |
   +-----------------------------------------------------------------+

PHASE I: DOCUMENTATION UPDATE
29. Documentation Scribe updates affected docs
30. Learnings files updated with new patterns discovered
31. If a discovery invalidated earlier diagrams, update them here

PHASE J: GATE CHECK + USER DELIVERY + PLAYWRIGHT REGRESSION SMOKE
32. CTO runs: python scripts/gate_check.py --all (or --slice N [--frontend])
    Script auto-discovers slices and verifies all required artifacts exist.
33. PLAYWRIGHT REGRESSION SMOKE:
    - Run Playwright smoke test suite
    - Must include 3-5 assertions on previously-shipped slices (last 2 completed)
    - Any regression = fix before user delivery
34. If FAIL: fix missing items. Do NOT start next slice.
35. If PASS + smoke green: CTO presents completed slice to user (DONE work only):
    - gate_check.py output as proof all artifacts exist
    - What was built + QA results summary + known trade-offs
    - Sentry clear confirmation
    If user finds issues: spawn fix agents, re-run gate_check.py, re-present.
36. Push to GitHub, then run POST-PUSH VERIFICATION.

POST-PUSH VERIFICATION (after every push to GitHub -- MANDATORY)

After pushing, the CTO MUST verify the deployment is healthy:

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

   +-----------------------------------------------------------------+
   | POST-PUSH GATE: CTO must confirm after every push:              |
   | [] "relay-sentry polled -- no new errors in last 10 minutes"   |
   | [] "Deployment platform verified -- no build or runtime errors" |
   | [] "Function/service logs clean -- no new exceptions"           |
   | If ANY check fails: fix immediately before starting new work.   |
   +-----------------------------------------------------------------+
```
