# Per-Slice Workflow: Phases E through H

> Sub-file of [PER-SLICE-WORKFLOW-TEMPLATE.md](PER-SLICE-WORKFLOW-TEMPLATE.md). Contains Phases E, F, F.5, G, H.

```
PHASE E: PEER REVIEW (4 models, adversarial, parallel)
NOTE: Peer review applies to ALL code changes including refactoring.
Refactoring is not exempt from peer review, QA, or security review.
Moving code between files can introduce security regressions.
34. 4 reviewers run in parallel (smartest-of-each-provider):
    - Gemini (smartest available) -- architecture
    - OpenAI 5.5 via Responses API (POST /v1/responses, field: output_text) -- invariants/security/150-line
    - Claude Opus 4.7 (independent sub-agent) -- independent review
    - Grok (smartest available) -- security/edge-case

   +--------------------------------------------------------------+
   | NUCLEAR GATE E: Before proceeding, CTO must confirm:         |
   | [] "Gemini returned findings: {summary}"                     |
   | [] "OpenAI 5.5 returned findings: {summary}"                 |
   | [] "Claude Opus 4.7 returned findings: {summary}"            |
   | [] "Grok returned findings: {summary}"                       |
   | [] "ALL 4 reviewers reported. Not proceeding with partial."  |
   | [] "Round 2 completed after fixes -- no new consensus issues"|
   | If any box is unchecked: STOP. Violation of Nuclear           |
   | Rule 2. Wait, retry, or report to owner. Do NOT continue.    |
   +--------------------------------------------------------------+

35. CTO synthesizes: consensus issues (2+ reviewers) = mandatory fixes. Round 2 mandatory after fixes.

PHASE F: QA SWARM + WHISKEY TEAM + UX SENSE CHECK (AUTONOMOUS FIX)
36. Standard QA swarm (skills: /qa-stats, /qa-code-quality, /qa-data-integrity, /qa-security, /qa-uiux-browser) runs in parallel (red team framing -- Article 7c):
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

PHASE F.5: RUNTIME LOG CHECK (after every QA run -- MANDATORY)
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
    Log errors are treated as CRITICAL -- they are real runtime failures, not hypothetical.
45. VERIFY STRUCTURED LOGGER IS INSTALLED AND USED:
    - Confirm src/shared/logging/logger.{EXT} exists and is imported by API routes
    - Grep for raw console.log/error/warn and print() in src/ (excluding tests)
    - Any raw console output found = CRITICAL finding: route must use the structured logger
    - This check catches "Sentry configured but logger never actually used" failures

   +------------------------------------------------------------------+
   | RUNTIME LOG GATE F.5: Before proceeding to Phase G:             |
   | [] "Sentry checked -- all new errors from this QA run logged"   |
   | [] "Server/function logs checked (if staging environment)"       |
   | [] "DB logs checked (if DB access available)"                    |
   | [] "Structured logger exists at src/shared/logging/logger.{EXT}"|
   | [] "No raw console.log/error/warn or print() in src/ code"      |
   | [] "API routes import and use the structured logger"             |
   | [] "All log findings added to Phase G fix queue"                 |
   +------------------------------------------------------------------+

PHASE G: AUTONOMOUS FIX VERIFICATION + RED TEAM ESCALATION
46. CTO reviews autonomous fix results from Phase F:
    - Verify all FIXED items: test + fix committed, regression suite green
    - Review ESCALATED items: assign to coder teammates if architectural
      (NOT itself -- Nuclear Rule 1)
    - Review FAILED items (3 attempts exhausted): escalate to Red Team
47. Escalated fixes go through abbreviated peer review
48. Red Team Post-QA review runs (Article 14b):
    - Targets QA coverage gaps, interaction effects, inherited assumptions
    - Reviews aggregate impact of all autonomous fixes
    - Issues verdict: APPROVE / REVISE / BLOCK
49. Professor Review also runs on aggregate changes (domain expert review alongside Red Team)
    Artifact: reviews/slice-N-professor.md (if escalation triggered)
50. If Red Team issues BLOCK: escalate to project owner
51. Autonomous Defect Resolution Protocol (Article 17e):
    - Any NEW defect found during Phase G: finding agent applies protocol
      (AUDIT/RED/GREEN/REGRESSION/CLASS SCAN/COMMIT)
    - Escalate to user only when fix requires architectural decision,
      modifies infrastructure outside workspace, or has failed 3 times

PHASE H: REGRESSION CHECK + IMPLICIT BEHAVIOR REGRESSION
52. Abbreviated QA re-run on fixed areas only
    - Any regressions found: apply Autonomous Defect Resolution Protocol
      (AUDIT/RED/GREEN/REGRESSION/CLASS SCAN/COMMIT -- Article 17e)
53. Implicit Behavior Regression re-check (all 6 categories)
54. Goal Achievement Test re-run if any fixes touched user-facing workflows

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
```
