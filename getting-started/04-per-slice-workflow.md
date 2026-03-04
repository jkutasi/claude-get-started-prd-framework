# Step 4: Per-Slice Workflow

> Part of the [Getting Started](INDEX.md) roadmap. Load only this file when working on running phases A-J for each slice.

**Every phase is MANDATORY. Skipping any phase is a CONTRACT VIOLATION.**

```
PHASE A: PREPARATION
1. CTO reviews slice requirements + Gherkin acceptance criteria
2. Researcher gathers docs, builds/updates skills files
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

PHASE A.7: RED TEAM PRE-BUILD GATE
7. QA Lead spawns Red Team Reviewer on user-confirmed slice plan (10 attack dimensions)
8. Red Team sends plan to {EXTERNAL_MODEL} with hostile prompt
9. Verdict: APPROVE / REVISE / BLOCK
   If BLOCK: cannot proceed. Max 3 iterations before owner escalation.
   Artifact: reviews/slice-N-red-team-pre-build.md

   +-----------------------------------------------------------------+
   | RED TEAM GATE: Before proceeding, CTO must confirm:             |
   | [] "Red Team Reviewer returned verdict: APPROVE or REVISE"      |
   | [] "reviews/slice-N-red-team-pre-build.md EXISTS on disk"       |
   | [] "Verdict is NOT BLOCK (or BLOCK findings were addressed)"    |
   +-----------------------------------------------------------------+

PHASE B: GHERKIN AUDIT + TEST SPECIFICATION + TEST PEER REVIEW (Article 17, 18)

   B.1: GHERKIN AUDIT (max 3 cycles)
   7.  QA Lead audits Gherkin for completeness (traceability matrix) + quality
   8.  Every user story element must map to at least one Gherkin scenario
   9.  Quality: unambiguous, concrete values, testable outcomes, NFR coverage

   B.2: TEST SPECIFICATION (different agents from implementation coders)
   10. Architect defines skeletal interfaces (function sigs, class stubs)
   11. QA Lead spawns test-writer sub-agents (NOT implementation coders)
   12. Test-writers write ALL tests: unit, integration, E2E definitions
   13. ALL tests must be RED (import errors or assertion failures)

   B.3: TEST PEER REVIEW (3+ models, parallel)
   14. 3 peer reviewers (+ Greptile if configured) review test code in parallel
   15. Consensus (2+) = mandatory test fixes before proceeding

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
16. CTO assigns implementation to coder teammates (NOT itself -- Nuclear Rule 1)
17. Coders receive failing tests + spec, write code until tests PASS

   +-----------------------------------------------------------------+
   | NUCLEAR GATE C: CTO must confirm:                               |
   | [] "I did NOT write any code myself in this phase"              |
   | [] "All code was produced by teammates or their sub-agents"     |
   | [] "All tests from Phase B now PASS"                            |
   | [] "All code follows Article 20: feature folders, layer separation, 150-line limit, structured logging, error wrapping" |
   +-----------------------------------------------------------------+

PHASE D: SELF-REFLECTION (mandatory)
18. Each coder re-reads their code, identifies issues, proposes improvements

PHASE E: PEER REVIEW (3+ models, parallel)
19. 3 peer reviewers (+ Greptile if configured) run in parallel, return findings

   +-----------------------------------------------------------------+
   | NUCLEAR GATE E: CTO must confirm:                               |
   | [] "ALL reviewers returned findings before proceeding"          |
   | [] "Consensus issues (2+ reviewers) identified as mandatory"    |
   +-----------------------------------------------------------------+

20. CTO synthesizes: consensus (2+) = mandatory fixes

PHASE F: QA SWARM + WHISKEY TEAM + UX SENSE CHECK (AUTONOMOUS FIX)
21. Standard QA swarm -- Stats, Code Quality, Data Integrity, Security, UI/UX
    Each agent applies Autonomous Defect Resolution Protocol (Article 17e):
    find bug -> spawn fix sub-agent -> AUDIT/RED/GREEN/REGRESSION/CLASS SCAN/COMMIT
22. Whiskey Team -- adversarial QA (8 scope items incl. Goal Achievement Test)
    + MANDATORY implicit behavior regression (6 categories)
    Whiskey Team applies same autonomous fix protocol
23. UX Sense Check -- 3 personas navigate via agent-browser (frontend slices)
    All run under QA Lead coordination.
24. QA Manager synthesizes ALL findings + autonomous fix results

PHASE G: AUTONOMOUS FIX VERIFICATION + RED TEAM ESCALATION
25. CTO reviews autonomous fix results from Phase F (QA agents fix bugs inline)
26. Escalated fixes (architectural/infrastructure/3x-failed) assigned to teammates
27. Autonomous Defect Resolution Protocol (Article 17e):
    AUDIT test -> RED -> GREEN -> REGRESSION -> CLASS SCAN -> COMMIT
28. IF fix escalated to Red Team: verdict APPROVE / REVISE / BLOCK (Article 14b)
    Max 3 autonomous fix attempts before Red Team escalation

PHASE H: REGRESSION CHECK + IMPLICIT BEHAVIOR REGRESSION
29. Abbreviated QA re-run on fixed areas
30. Whiskey Team runs MANDATORY implicit behavior regression (6 categories)
31. UX Sense Check re-runs on changed frontend pages

   +-----------------------------------------------------------------+
   | NUCLEAR GATE H: Before starting next slice, CTO must confirm:   |
   |                                                                   |
   | [] "Gherkin audit passed (completeness + quality)"              |
   | [] "All tests written by test-writer sub-agents (not coders)"   |
   | [] "All Gherkin scenarios pass"                                  |
   | [] "All peer reviewers reviewed and approved"                    |
   | [] "All QA agents ran and passed"                                |
   | [] "Whiskey Team ran -- all CRITICAL/HIGH findings resolved"     |
   | [] "Goal Achievement Test PASSED via agent-browser"              |
   | [] "Implicit behavior regression completed (6/6 categories)"    |
   | [] "UX Sense Check ran (if frontend slice)"                      |
   | [] "Unit test coverage >= 90% on business logic"                 |
   | [] "CTO did NOT write any code or test code this slice"          |
   | [] "reviews/slice-N-test-spec.md EXISTS"                         |
   | [] "reviews/slice-N-test-review.md EXISTS"                       |
   | [] "reviews/slice-N-peer-review.md EXISTS"                       |
   | [] "reviews/slice-N-qa-swarm.md EXISTS"                          |
   | [] "reviews/slice-N-red-team-pre-build.md EXISTS"                |
   | [] "reviews/slice-N-red-team.md EXISTS"                          |
   | [] "reviews/slice-N-whiskey-team.md EXISTS"                      |
   | [] "reviews/slice-N-ux-sense-check.md EXISTS (if frontend)"      |
   +-----------------------------------------------------------------+

PHASE I: DOCUMENTATION UPDATE
32. Documentation Scribe updates affected docs
33. Learnings files updated with new patterns discovered
34. If a discovery invalidated earlier diagrams, update them here

PHASE J: MECHANICAL GATE CHECK
35. CTO runs: python gate_check.py --slice N [--frontend]
36. Script verifies ALL artifacts exist on disk (8 review files per slice)
37. If FAIL: fix missing items. Do NOT start next slice.
38. If PASS: begin Slice N+1.
```
