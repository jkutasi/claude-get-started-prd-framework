# Step 4b: Per-Slice Workflow — Phases E through Post-Push

> Sub-file of [04-per-slice-workflow.md](04-per-slice-workflow.md). Contains Phases E, F, F.5, G, H, I, J, and Post-Push Verification.

```
PHASE E: PEER REVIEW (4 models, adversarial, parallel)
NOTE: Peer review applies to ALL code changes including refactoring.
Refactoring is not exempt from peer review, QA, or security review.
Moving code between files can introduce security regressions.
23. 4 reviewers run in parallel (smartest-of-each-provider):
    - Gemini (smartest available) -- architecture
    - OpenAI 5.5 via Responses API (POST /v1/responses, field: output_text) -- invariants/security/150-line
    - Claude Opus 4.7 -- independent review
    - Grok (smartest available) -- security/edge-case

   +-----------------------------------------------------------------+
   | NUCLEAR GATE E: CTO must confirm:                               |
   | [] "ALL 4 reviewers returned findings before proceeding"        |
   | [] "Consensus issues (2+ reviewers) identified as mandatory"    |
   | [] "Round 2 completed after fixes -- no new consensus issues"   |
   +-----------------------------------------------------------------+

24. CTO synthesizes: consensus (2+) = mandatory fixes. Round 2 mandatory after fixes.

PHASE F: QA SWARM + WHISKEY TEAM + UX SENSE CHECK (AUTONOMOUS FIX)
25. Standard QA swarm (skills: /qa-stats, /qa-code-quality, /qa-data-integrity, /qa-security, /qa-uiux-browser)
    Each agent applies Autonomous Defect Resolution Protocol (Article 17e):
    find bug -> spawn fix sub-agent -> AUDIT/RED/GREEN/REGRESSION/CLASS SCAN/COMMIT
26. Whiskey Team -- adversarial QA (8 scope items incl. Goal Achievement Test)
    + MANDATORY implicit behavior regression (6 categories)
    Whiskey Team applies same autonomous fix protocol
27. UX Sense Check -- 3 personas navigate via agent-browser (frontend slices)
    All run under QA Lead coordination.
28. QA Manager synthesizes ALL findings + autonomous fix results
    Professor Review also runs post-QA on aggregate findings

PHASE F.5: RUNTIME LOG CHECK (after every QA run -- MANDATORY)
After the QA swarm and Whiskey Team complete, the CTO checks all available logs
for errors that surfaced during testing but weren't caught by the test assertions.

29. CHECK SENTRY (via MCP or dashboard):
    - Query for new errors triggered during this QA session
    - Check both frontend (browser SDK) and backend (server SDK) error feeds
    - Any new error = CRITICAL finding, added to the Phase G fix queue immediately
30. CHECK DEPLOYMENT/SERVER LOGS (if running on staging/preview environment):
    - Vercel function logs, server logs, or equivalent
    - Look for unhandled exceptions, 500 errors, timeout failures
31. CHECK DATABASE LOGS (if DB access available):
    - Failed queries, constraint violations, transaction rollbacks
    - Any DB error that occurred during QA testing
32. CTO adds all log findings to the Phase G queue alongside QA agent findings.
    Log errors are treated as CRITICAL -- they are real runtime failures, not hypothetical.

   +-----------------------------------------------------------------+
   | RUNTIME LOG GATE F.5: Before proceeding to Phase G:            |
   | [] "Sentry checked -- all new errors from this QA run logged"  |
   | [] "Server/function logs checked (if staging environment)"      |
   | [] "DB logs checked (if DB access available)"                   |
   | [] "All log findings added to Phase G fix queue"                |
   +-----------------------------------------------------------------+

PHASE G: AUTONOMOUS FIX VERIFICATION + RED TEAM ESCALATION
33. CTO reviews autonomous fix results from Phase F (QA agents fix bugs inline)
34. Escalated fixes (architectural/infrastructure/3x-failed) assigned to teammates
35. Autonomous Defect Resolution Protocol (Article 17e):
    AUDIT test -> RED -> GREEN -> REGRESSION -> CLASS SCAN -> COMMIT
36. IF fix escalated to Red Team: verdict APPROVE / REVISE / BLOCK (Article 14b)
    Max 3 autonomous fix attempts before Red Team escalation
37. Professor Review also runs on aggregate changes (domain expert review alongside Red Team)
    Artifact: reviews/slice-N-professor.md (if escalation triggered)

PHASE H: REGRESSION CHECK + IMPLICIT BEHAVIOR REGRESSION
38. Abbreviated QA re-run on fixed areas
39. Whiskey Team runs MANDATORY implicit behavior regression (6 categories)
40. UX Sense Check re-runs on changed frontend pages

   +-----------------------------------------------------------------+
   | NUCLEAR GATE H: Before starting next slice, CTO must confirm:   |
   |                                                                   |
   | [] "Gherkin audit passed (completeness + quality)"              |
   | [] "All tests written by test-writer sub-agents (not coders)"   |
   | [] "All Gherkin scenarios pass"                                  |
   | [] "All peer reviewers reviewed and approved"                    |
   | [] "All QA agents ran and passed"                                |
   | [] "Runtime Log Check completed (Sentry + server + DB logs)"    |
   | [] "Whiskey Team ran -- all CRITICAL/HIGH findings resolved"     |
   | [] "Goal Achievement Test PASSED via agent-browser"              |
   | [] "Implicit behavior regression completed (6/6 categories)"    |
   | [] "Article 20 architecture standards verified (feature          |
   |     folders, 3-layer, 150-line, observability, error wrap)"      |
   | [] "UX Sense Check ran (if frontend slice)"                      |
   | [] "Unit test coverage >= 90% on business logic + public interfaces" |
   | [] "CTO did NOT write any code or test code this slice"          |
   | [] "reviews/slice-N-test-spec.md EXISTS"                         |
   | [] "reviews/slice-N-test-review.md EXISTS"                       |
   | [] "reviews/slice-N-peer-review.md EXISTS"                       |
   | [] "reviews/slice-N-qa-swarm.md EXISTS"                          |
   | [] "reviews/slice-N-red-team-pre-build.md EXISTS"                |
   | [] "reviews/slice-N-red-team.md EXISTS (if Red Team escalation triggered in Phase G)" |
   | [] "reviews/slice-N-professor-pre-build.md EXISTS"              |
   | [] "reviews/slice-N-professor.md EXISTS (if Professor escalation triggered in Phase G)" |
   | [] "reviews/slice-N-whiskey-team.md EXISTS"                      |
   | [] "reviews/slice-N-ux-sense-check.md EXISTS (if frontend)"      |
   +-----------------------------------------------------------------+

PHASE I: DOCUMENTATION UPDATE
41. Documentation Scribe updates affected docs
42. Learnings files updated with new patterns discovered
43. If a discovery invalidated earlier diagrams, update them here

PHASE J: GATE CHECK + USER DELIVERY + POST-PUSH (see phase-j-gate-check.md)
44. CTO runs: python scripts/gate_check.py --all (or --slice N [--frontend])
    Script auto-discovers slices and verifies all required artifacts exist.
45. If FAIL: fix missing items. Do NOT start next slice.
46. If PASS: CTO presents completed slice to user (DONE work only, never draft):
    - gate_check.py output as proof all artifacts exist
    - What was built + QA results summary + known trade-offs
    If user finds issues: spawn fix agents, re-run gate_check.py, re-present.
47. Push to GitHub, then run POST-PUSH VERIFICATION.

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

   +-----------------------------------------------------------------+
   | POST-PUSH GATE: CTO must confirm after every push:              |
   | [] "Error tracker checked -- no new errors in last 10 minutes"  |
   | [] "Deployment platform verified -- no build or runtime errors" |
   | [] "Function/service logs clean -- no new exceptions"           |
   | If ANY check fails: fix immediately before starting new work.   |
   +-----------------------------------------------------------------+
```
