# Step 4: Per-Slice Workflow

> Part of the [Getting Started](INDEX.md) roadmap. Load only this file when working on running phases A-J for each slice.

**Every phase is MANDATORY. Skipping any phase is a CONTRACT VIOLATION.**

**USER PRESENTATION RULE: The user ONLY sees finished, fully-vetted work. ALL phases (peer review, QA swarm, whiskey team, red team, regression, UX sense check) must complete autonomously BEFORE presenting results to the user. Never defer QA to "after user reviews." Never say "contingent on user review." The CTO presents a DONE slice — not a draft waiting for validation.**

```
PHASE A: PREPARATION
1. CTO reviews slice requirements + Gherkin acceptance criteria
2. Researcher (skill: /researcher) gathers docs, builds/updates skills files
3. Architect creates per-slice detailed diagrams (sequence + focused ER)

PHASE A.5: DOC BOOTSTRAP + DIAGRAM REVIEW
   Slice 0: CTO delegates to Scribe for PROJECT.md, DOCS_MAP.md, contract stubs.
   Architect creates high-level overview diagrams (System Architecture, Data Model ER,
   User Flow, Slice Dependency Graph) for user review.
   Slices 1+: Per-slice detailed diagrams created in Phase A (non-blocking).

PHASE A.6: USER SCOPE CONFIRMATION (Article 19) -- MANDATORY
4. CTO presents slice scope to user: summary, Gherkin scenarios, diagrams, Goal Achievement Test
5. If scope changed from original plan, highlight what changed and why
6. User responds: APPROVE (proceed) or REVISE (provide feedback, CTO adjusts, re-presents)

   +-----------------------------------------------------------------+
   | USER SCOPE GATE A.6: Before proceeding to Red Team:             |
   | [] "User reviewed slice scope (summary + Gherkin + diagrams)"   |
   | [] "User responded APPROVE"                                     |
   | [] "Any scope changes from original plan were highlighted"       |
   +-----------------------------------------------------------------+

PHASE A.7: RED TEAM + PROFESSOR PRE-BUILD GATE
7. QA Lead spawns Red Team Reviewer (skill: /red-team-reviewer) on user-confirmed slice plan (10 attack dimensions)
8. Red Team sends plan to {EXTERNAL_MODEL} with hostile prompt
9. Verdict: APPROVE / REVISE / BLOCK
   If BLOCK: cannot proceed. Max 3 iterations before owner escalation.
   Artifact: reviews/slice-N-red-team-pre-build.md
10. Professor Review runs in parallel with Red Team (domain expert review)
    Professors evaluate architecture, testing strategy, security posture, etc.
    Verdict: APPROVE / REVISE / BLOCK
    Artifact: reviews/slice-N-professor-pre-build.md

   +-----------------------------------------------------------------+
   | RED TEAM GATE: Before proceeding, CTO must confirm:             |
   | [] "Red Team Reviewer returned verdict: APPROVE or REVISE"      |
   | [] "reviews/slice-N-red-team-pre-build.md EXISTS on disk"       |
   | [] "Verdict is NOT BLOCK (or BLOCK findings were addressed)"    |
   +-----------------------------------------------------------------+

   +-----------------------------------------------------------------+
   | PROFESSOR GATE: Before proceeding, CTO must confirm:            |
   | [] "Professor Review returned verdict: APPROVE or REVISE"       |
   | [] "reviews/slice-N-professor-pre-build.md EXISTS on disk"      |
   | [] "Verdict is NOT BLOCK (or BLOCK findings were addressed)"    |
   +-----------------------------------------------------------------+

PHASE B: GHERKIN AUDIT + TEST SPECIFICATION + TEST PEER REVIEW (Article 17, 18)

   B.1: GHERKIN AUDIT (max 3 cycles)
   11. QA Lead audits Gherkin for completeness (traceability matrix) + quality
   12. Every user story element must map to at least one Gherkin scenario
   13. Quality: unambiguous, concrete values, testable outcomes, NFR coverage

   B.2: TEST SPECIFICATION (different agents from implementation coders)
   14. Architect defines skeletal interfaces (function sigs, class stubs)
   15. QA Lead spawns test-writer sub-agents (NOT implementation coders)
   16. Test-writers write ALL tests: unit, integration, E2E definitions
   17. ALL tests must be RED (import errors or assertion failures)

   B.3: TEST PEER REVIEW (3+ models, parallel)
   18. 3 peer reviewers (+ Greptile if configured) review test code in parallel
   19. Consensus (2+) = mandatory test fixes before proceeding

   +-----------------------------------------------------------------+
   | TEST SPEC GATE B: CTO must confirm:                             |
   | [] "Gherkin Audit PASSED (completeness + quality)"              |
   | [] "All tests written by test-writer sub-agents (not coders)"   |
   | [] "All tests are RED"                                          |
   | [] "Test code peer-reviewed by 3+ external models"              |
   | [] "reviews/slice-N-test-spec.md EXISTS on disk"                |
   | [] "reviews/slice-N-test-review.md EXISTS on disk"              |
   | [] "CTO did NOT write any test code directly"                   |
   +-----------------------------------------------------------------+

PHASE C: IMPLEMENTATION
20. CTO assigns implementation to coder teammates (skills: /coder-backend, /coder-frontend) (NOT itself -- Nuclear Rule 1)
21. Coders receive failing tests + spec, write code until tests PASS

   +-----------------------------------------------------------------+
   | NUCLEAR GATE C: CTO must confirm:                               |
   | [] "I did NOT write any code myself in this phase"              |
   | [] "All code was produced by teammates or their sub-agents"     |
   | [] "All tests from Phase B now PASS"                            |
   | [] "All code follows Article 20: feature folders, layer separation, 150-line limit, structured logging, error wrapping" |
   +-----------------------------------------------------------------+

PHASE D: SELF-REFLECTION (mandatory)
22. Each coder re-reads their code, identifies issues, proposes improvements

PHASE E: PEER REVIEW (3+ models, parallel)
NOTE: Peer review applies to ALL code changes including refactoring.
Refactoring is not exempt from peer review, QA, or security review.
Moving code between files can introduce security regressions.
23. 3 peer reviewers (skills: /reviewer-gemini, /reviewer-openai, /reviewer-grok + /reviewer-greptile if configured) run in parallel

   +-----------------------------------------------------------------+
   | NUCLEAR GATE E: CTO must confirm:                               |
   | [] "ALL reviewers returned findings before proceeding"          |
   | [] "Consensus issues (2+ reviewers) identified as mandatory"    |
   +-----------------------------------------------------------------+

24. CTO synthesizes: consensus (2+) = mandatory fixes

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

PHASE F.5: RUNTIME LOG CHECK (after every QA run — MANDATORY)
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
    Log errors are treated as CRITICAL — they are real runtime failures, not hypothetical.

   +-----------------------------------------------------------------+
   | RUNTIME LOG GATE F.5: Before proceeding to Phase G:            |
   | [] "Sentry checked — all new errors from this QA run logged"   |
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

PHASE I.5: USER DELIVERY (only after ALL prior phases complete)
44. CTO presents completed slice to user:
    - What was built (summary + screenshots/demos if applicable)
    - All QA results (peer review verdict, QA swarm results, whiskey team verdict)
    - Any known limitations or trade-offs
45. User tests and provides feedback
46. If user finds issues: CTO spawns fix agents, runs abbreviated QA, then re-presents

   +-----------------------------------------------------------------+
   | USER DELIVERY GATE I.5: Before presenting to user, CTO confirms:|
   | [] "Peer review completed — verdict is not 'pending'"           |
   | [] "QA swarm completed — all agents reported"                   |
   | [] "Whiskey team completed — all CRITICAL/HIGH resolved"        |
   | [] "Red Team post-QA completed (if escalation triggered)"       |
   | [] "Professor Review completed (if escalation triggered)"       |
   | [] "Regression check passed"                                    |
   | [] "Goal Achievement Test passed"                               |
   | [] "I am presenting DONE work, not a draft"                     |
   +-----------------------------------------------------------------+

PHASE J: MECHANICAL GATE CHECK
47. CTO runs: python gate_check.py --slice N [--frontend]
48. Script verifies ALL artifacts exist on disk (10 review files per slice)
49. If FAIL: fix missing items. Do NOT start next slice.
50. If PASS: push to GitHub, then run POST-PUSH VERIFICATION.

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

   +-----------------------------------------------------------------+
   | POST-PUSH GATE: CTO must confirm after every push:              |
   | [] "Error tracker checked — no new errors in last 10 minutes"    |
   | [] "Deployment platform verified — no build or runtime errors"  |
   | [] "Function/service logs clean — no new exceptions"            |
   | [] "Greptile scan completed (if configured) — findings reviewed"|
   | If ANY check fails: fix immediately before starting new work.   |
   +-----------------------------------------------------------------+
```
