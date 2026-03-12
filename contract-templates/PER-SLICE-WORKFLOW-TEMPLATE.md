# Per-Slice Development Workflow

> **Loaded from CLAUDE.md on demand.** This file contains the full phase-by-phase workflow for each slice. The CTO loads this file at the start of each slice and follows it step by step.

**CRITICAL: Every phase is MANDATORY. Skipping any phase is a CONTRACT VIOLATION.**
**REMINDER: You are the CTO Orchestrator. You spawn teammates and sub-agents for ALL implementation.**

**USER PRESENTATION RULE: The user ONLY sees finished, fully-vetted work. ALL phases (peer review, QA swarm, whiskey team, red team, regression, UX sense check) must complete autonomously BEFORE presenting results to the user. Never defer QA to "after user reviews." Never say "contingent on user review." The CTO presents a DONE slice — not a draft waiting for validation.**

```
PHASE A: PREPARATION
1. CTO reviews slice requirements + Gherkin acceptance criteria
2. Researcher gathers docs, builds/updates skills files
3. CTO determines whether slice is frontend-touching (for UX Sense Check activation)
4. Architect creates per-slice detailed diagrams (sequence + focused ER) -- non-blocking

PHASE A.5: DOC BOOTSTRAP + DIAGRAM REVIEW
   Slice 0: CTO delegates to Scribe to create initial skeleton (DOCS_MAP.md,
   PROJECT.md, contract stubs). Architect creates high-level overview diagrams
   (System Architecture, Data Model ER, User Flow, Slice Dependency Graph) for
   user review. Runs BEFORE any coder agents are spawned.
   Slices 1+: Per-slice detailed diagrams created in Phase A (non-blocking).

PHASE A.6: USER SCOPE CONFIRMATION (Article 19) -- MANDATORY
5. CTO presents slice scope to user: summary, Gherkin scenarios, diagrams, Goal Achievement Test
6. If scope changed from original plan due to learnings from prior slices, highlight what changed and why
7. User responds: APPROVE (proceed) or REVISE (provide feedback, CTO adjusts, re-presents)
8. No iteration limit -- user decides when they are satisfied

   +------------------------------------------------------------------+
   | USER SCOPE GATE A.6: Before proceeding to Red Team:              |
   | [] "User reviewed slice scope (summary + Gherkin + diagrams)"    |
   | [] "User responded APPROVE"                                      |
   | [] "Any scope changes from original plan were highlighted"        |
   +------------------------------------------------------------------+

PHASE A.7: RED TEAM + PROFESSOR PRE-BUILD GATE (Article 14a) -- MANDATORY
9. Red Team sub-agent reviews the USER-CONFIRMED slice plan and architecture
10. Red Team evaluates all 10 attack dimensions
11. Red Team submits plan to external model for hostile review
12. Red Team issues verdict: APPROVE / REVISE / BLOCK
13. If BLOCK: implementation HALTS. Owner must override or plan must change.
14. If REVISE: address required actions, re-submit to Red Team.
15. If APPROVE: proceed to Phase B.
    Artifact: reviews/slice-N-red-team-pre-build.md
16. Professor Review runs in parallel with Red Team (domain expert review)
    Professors evaluate architecture, testing strategy, security posture, etc.
    Verdict: APPROVE / REVISE / BLOCK
    Artifact: reviews/slice-N-professor-pre-build.md

   +------------------------------------------------------------------+
   | PROFESSOR GATE: Before proceeding, CTO must confirm:             |
   | [] "Professor Review returned verdict: APPROVE or REVISE"        |
   | [] "reviews/slice-N-professor-pre-build.md EXISTS on disk"       |
   | [] "Verdict is NOT BLOCK (or BLOCK findings were addressed)"     |
   +------------------------------------------------------------------+

PHASE B: GHERKIN AUDIT + TEST SPECIFICATION + TEST PEER REVIEW (Article 17, 18)

   B.1: GHERKIN AUDIT (max 3 cycles)
   17. QA Lead audits Gherkin for completeness (traceability matrix) + quality
   18. Every user story element must map to at least one Gherkin scenario
   19. Quality check: unambiguous, concrete values, testable outcomes, NFR coverage
   20. If gaps: write missing Gherkin, re-audit (max 3 cycles, then owner sign-off)

   B.2: TEST SPECIFICATION (different agents from implementation coders)
   21. Architect defines skeletal interfaces (function sigs, class stubs, type stubs)
   22. QA Lead spawns test-writer sub-agents (NOT implementation coders)
   23. Test-writers write ALL tests: unit, integration, E2E definitions
   24. ALL tests must be RED (import errors or assertion failures)
   25. Tests that PASS = bad test, must be fixed

   B.3: TEST PEER REVIEW (3+ models, parallel)
   26. 3 peer reviewers review test code in parallel (same process as code review)
   27. Consensus issues (2+ reviewers) = mandatory test fixes
   28. Fixed tests re-validated: still RED against skeletal interfaces

   +------------------------------------------------------------------+
   | TEST SPEC GATE B: Before proceeding to implementation:           |
   | [] "Gherkin Audit PASSED (completeness + quality)"               |
   | [] "All tests written by test-writer sub-agents (not coders)"    |
   | [] "All tests are RED (import errors or assertion failures)"     |
   | [] "Skeletal interfaces exist for all tested modules"            |
   | [] "Test code peer-reviewed by 3+ external models"               |
   | [] "reviews/slice-N-test-spec.md EXISTS on disk"                 |
   | [] "reviews/slice-N-test-review.md EXISTS on disk"               |
   | [] "CTO did NOT write any test code directly (Nuclear Rule 1)"   |
   +------------------------------------------------------------------+

PHASE C: IMPLEMENTATION
29. CTO assigns implementation coder teammates with focused module scope
30. Coders receive failing tests + spec, write code until all tests PASS
31. Coders do NOT modify tests (only implementation code)

   +-------------------------------------------------------------+
   | NUCLEAR GATE C: Before proceeding, CTO must confirm:        |
   | [] "I did NOT write any code myself in this phase"           |
   | [] "All code was produced by spawned teammates/sub-agents"   |
   | [] "I can name each agent and what they produced"            |
   | [] "All tests from Phase B now PASS"                         |
   | [] "All code follows Article 20 architecture standards"      |
   | If any box is unchecked: STOP. Violation of Nuclear          |
   | Rule 1. Report to owner and re-do Phase C correctly.         |
   +-------------------------------------------------------------+

PHASE D: SELF-REFLECTION + ERROR REGISTRY (mandatory, before peer review)
32. Each coder re-reads their code, identifies issues, proposes improvements
32b. Each coder produces Error & Rescue Registry for their module (Article 35)
32c. CTO checks for CRITICAL GAPS (no rescue + no test + silent). Any found = fix before Phase E
33. CTO reviews reflection, assigns self-identified fixes
    Artifact: reviews/slice-N-error-rescue-registry.md

PHASE E: PEER REVIEW (3+ models, parallel)
NOTE: Peer review applies to ALL code changes including refactoring.
Refactoring is not exempt from peer review, QA, or security review.
Moving code between files can introduce security regressions.
34. 3 peer reviewers run in parallel, return findings

   +--------------------------------------------------------------+
   | NUCLEAR GATE E: Before proceeding, CTO must confirm:         |
   | [] "Reviewer 1 ({model}) returned findings: {summary}"       |
   | [] "Reviewer 2 ({model}) returned findings: {summary}"       |
   | [] "Reviewer 3 ({model}) returned findings: {summary}"       |
   | [] "ALL reviewers have reported. I am not proceeding with     |
   |     partial reviews."                                         |
   | If any box is unchecked: STOP. Violation of Nuclear           |
   | Rule 2. Wait, retry, or report to owner. Do NOT continue.    |
   +--------------------------------------------------------------+

35. CTO synthesizes: consensus issues (2+ reviewers) = mandatory fixes

PHASE F: QA SWARM + WHISKEY TEAM + UX SENSE CHECK (AUTONOMOUS FIX)
36. Standard QA swarm runs in parallel (red team framing -- Article 7c):
    - QA Stats, QA Code Quality, QA Data Integrity, QA Security, QA UI/UX
    - Each QA agent applies Autonomous Defect Resolution Protocol (Article 17e):
      find bug -> spawn fix sub-agent -> AUDIT/RED/GREEN/REGRESSION/CLASS SCAN/COMMIT
37. Whiskey Team adversarial QA runs (all 8 test categories -- Article 15)
    - Whiskey Team applies same autonomous fix protocol for all findings
38. Implicit Behavior Regression check runs (all 6 categories -- Article 15b)
39. UX Sense Check runs via agent-browser with all personas
    (Article 16 -- frontend slices only)
40. QA Manager synthesizes all findings + autonomous fix results into report
    Professor Review also runs post-QA on aggregate findings

PHASE F.5: RUNTIME LOG CHECK (after every QA run — MANDATORY)
After the QA swarm and Whiskey Team complete, the CTO checks all available logs
for errors that surfaced during testing but weren't caught by the test assertions.

41. CHECK SENTRY (via MCP or dashboard):
    - Query for new errors triggered during this QA session
    - Check both frontend (browser SDK) and backend (server SDK) error feeds
    - Any new error = CRITICAL finding, added to the Phase G fix queue immediately
42. CHECK DEPLOYMENT/SERVER LOGS (if running on staging/preview environment):
    - Vercel function logs, server logs, or equivalent
    - Look for unhandled exceptions, 500 errors, timeout failures
43. CHECK DATABASE LOGS (if DB access available):
    - Failed queries, constraint violations, transaction rollbacks
    - Any DB error that occurred during QA testing
44. CTO adds all log findings to the Phase G queue alongside QA agent findings.
    Log errors are treated as CRITICAL — they are real runtime failures, not hypothetical.

   +------------------------------------------------------------------+
   | RUNTIME LOG GATE F.5: Before proceeding to Phase G:             |
   | [] "Sentry checked — all new errors from this QA run logged"    |
   | [] "Server/function logs checked (if staging environment)"       |
   | [] "DB logs checked (if DB access available)"                    |
   | [] "All log findings added to Phase G fix queue"                 |
   +------------------------------------------------------------------+

PHASE G: AUTONOMOUS FIX VERIFICATION + RED TEAM ESCALATION
45. CTO reviews autonomous fix results from Phase F:
    - Verify all FIXED items: test + fix committed, regression suite green
    - Review ESCALATED items: assign to coder teammates if architectural
      (NOT itself -- Nuclear Rule 1)
    - Review FAILED items (3 attempts exhausted): escalate to Red Team
46. Escalated fixes go through abbreviated peer review
47. Red Team Post-QA review runs (Article 14b):
    - Targets QA coverage gaps, interaction effects, inherited assumptions
    - Reviews aggregate impact of all autonomous fixes
    - Issues verdict: APPROVE / REVISE / BLOCK
48. Professor Review also runs on aggregate changes (domain expert review alongside Red Team)
    Artifact: reviews/slice-N-professor.md (if escalation triggered)
49. If Red Team issues BLOCK: escalate to project owner
50. Autonomous Defect Resolution Protocol (Article 17e):
    - Any NEW defect found during Phase G: finding agent applies protocol
      (AUDIT/RED/GREEN/REGRESSION/CLASS SCAN/COMMIT)
    - Escalate to user only when fix requires architectural decision,
      modifies infrastructure outside workspace, or has failed 3 times

PHASE H: REGRESSION CHECK + IMPLICIT BEHAVIOR REGRESSION
51. Abbreviated QA re-run on fixed areas only
    - Any regressions found: apply Autonomous Defect Resolution Protocol
      (AUDIT/RED/GREEN/REGRESSION/CLASS SCAN/COMMIT -- Article 17e)
52. Implicit Behavior Regression re-check (all 6 categories)
53. Goal Achievement Test re-run if any fixes touched user-facing workflows

   +--------------------------------------------------------------+
   | NUCLEAR GATE H: Before moving to next slice, CTO must        |
   | confirm ALL of the following or the slice HAS NOT SHIPPED:    |
   |                                                               |
   | [] "Gherkin audit passed (completeness + quality)"            |
   | [] "All tests written by test-writer sub-agents (not coders)" |
   | [] "All Gherkin scenarios pass"                               |
   | [] "All peer reviewers reviewed and approved"                 |
   | [] "All QA agents ran and passed"                             |
   | [] "Runtime Log Check completed (Sentry + server + DB logs)" |
   | [] "Red Team Pre-Build review completed (Article 14a)"       |
   | [] "Red Team Post-QA review completed (Article 14b)"         |
   | [] "Whiskey Team review completed (Article 15)"               |
   | [] "UX Sense Check completed (Article 16, if frontend)"      |
   | [] "Goal Achievement Test = PASS"                             |
   | [] "Implicit Behavior Regression -- all 6 categories checked" |
   | [] "Article 20 architecture standards verified (feature      |
   |     folders, 3-layer, 150-line, observability, error wrap)"  |
   | [] "Unit test coverage >= 90% business logic + public APIs"   |
   | [] "Documentation updated (Scribe or Architect)"              |
   | [] "CTO did NOT write any code or test code this slice"       |
   | [] "reviews/slice-N-test-spec.md EXISTS on disk"              |
   | [] "reviews/slice-N-test-review.md EXISTS on disk"            |
   | [] "reviews/slice-N-peer-review.md EXISTS on disk"            |
   | [] "reviews/slice-N-qa-swarm.md EXISTS on disk"               |
   | [] "reviews/slice-N-red-team-pre-build.md EXISTS on disk"     |
   | [] "reviews/slice-N-red-team.md EXISTS on disk"               |
   | [] "reviews/slice-N-professor-pre-build.md EXISTS"            |
   | [] "reviews/slice-N-professor.md EXISTS (if Professor escalation triggered in Phase G)" |
   | [] "reviews/slice-N-whiskey-team.md EXISTS on disk"           |
   | [] "reviews/slice-N-error-rescue-registry.md EXISTS on disk"  |
   | [] "reviews/slice-N-ux-sense-check.md EXISTS (if frontend)"   |
   |                                                               |
   | If ANY box is unchecked: STOP. This slice is NOT complete.    |
   | Violation of Nuclear Rule 3. Do NOT start the next slice.     |
   | Finish this one first.                                        |
   +--------------------------------------------------------------+

PHASE I: DOCUMENTATION UPDATE
54. CTO delegates doc updates to Documentation Scribe (if available) or Architect
55. Designated agent updates affected docs via DOCS_MAP
56. If a discovery in this slice invalidates earlier diagrams, update them here

PHASE I.5: USER DELIVERY (only after ALL prior phases complete)
57. CTO presents completed slice to user:
    - What was built (summary + screenshots/demos if applicable)
    - All QA results (peer review verdict, QA swarm results, whiskey team verdict)
    - Any known limitations or trade-offs
58. User tests and provides feedback
59. If user finds issues: CTO spawns fix agents, runs abbreviated QA, then re-presents

   +------------------------------------------------------------------+
   | USER DELIVERY GATE I.5: Before presenting to user, CTO confirms: |
   | [] "Peer review completed — verdict is not 'pending'"            |
   | [] "QA swarm completed — all agents reported"                    |
   | [] "Whiskey team completed — all CRITICAL/HIGH resolved"         |
   | [] "Red Team post-QA completed"                                  |
   | [] "Professor Review completed (if escalation triggered)"        |
   | [] "Regression check passed"                                     |
   | [] "Goal Achievement Test passed"                                |
   | [] "I am presenting DONE work, not a draft"                      |
   +------------------------------------------------------------------+

PHASE J: MECHANICAL GATE CHECK (Article 12 enforcement)
60. CTO runs the gate check script:
    $ python gate_check.py --slice N
61. Script mechanically verifies ALL artifacts exist on disk:
    - reviews/slice-N-test-spec.md exists and is non-empty
    - reviews/slice-N-test-review.md exists and is non-empty
    - reviews/slice-N-peer-review.md exists and is non-empty
    - reviews/slice-N-qa-swarm.md exists and is non-empty
    - reviews/slice-N-red-team-pre-build.md exists and is non-empty
    - reviews/slice-N-red-team.md exists and is non-empty
    - reviews/slice-N-whiskey-team.md exists and is non-empty
    - reviews/slice-N-error-rescue-registry.md exists and is non-empty
    - reviews/slice-N-ux-sense-check.md exists (frontend slices)
    - Gherkin feature file exists in features/
    - Unit test files exist in tests/ or src/**/
    - All tests pass
62. Script returns PASS or FAIL with specific missing items listed.
63. If FAIL: CTO fixes missing items. Does NOT start next slice.
64. If PASS: push to GitHub, then run POST-PUSH VERIFICATION.

POST-PUSH VERIFICATION (after every push to GitHub — MANDATORY)

After pushing, the CTO MUST verify the deployment is healthy:

1. CHECK ERROR TRACKER (Sentry or project-equivalent — via MCP, API, or dashboard):
   - Wait at least 2 minutes after push for error indexing propagation
   - Query for new errors in the last 15 minutes
   - Filter by the project and environment (preview/production)
   - If new errors found: treat as CRITICAL — spawn fix agent immediately

2. CHECK DEPLOYMENT PLATFORM (Vercel/AWS/GCP/etc. — via dashboard or CLI):
   - Verify the deployment succeeded (no build errors)
   - Check function logs for runtime errors
   - If deployment failed or has runtime errors: revert or fix immediately

3. CHECK GREPTILE (if configured — via MCP):
   - Run a codebase-aware scan on the pushed changes
   - Review cross-file consistency findings
   - Consensus findings = mandatory fixes (same as peer review rules)

   +------------------------------------------------------------------+
   | POST-PUSH GATE: CTO must confirm after every push:               |
   | [] "Error tracker checked — no new errors in last 10 minutes"     |
   | [] "Deployment platform verified — no build or runtime errors"   |
   | [] "Function/service logs clean — no new exceptions"             |
   | [] "Greptile scan completed (if configured) — findings reviewed" |
   | If ANY check fails: fix immediately before starting new work.    |
   +------------------------------------------------------------------+
```

**If you are reading this and considering skipping the gate check script: DON'T. The script exists specifically because the CTO has demonstrated a tendency to skip reviews and move forward. The script is a mechanical check that cannot be rationalized away. Run it.**
