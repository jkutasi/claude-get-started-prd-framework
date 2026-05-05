# Per-Slice Workflow: Phases A through C

> Sub-file of [PER-SLICE-WORKFLOW-TEMPLATE.md](PER-SLICE-WORKFLOW-TEMPLATE.md). Contains Phases A, A.5, A.6, A.7 (optional), B, C.

```
PHASE A: PREPARATION
1. CTO reviews slice requirements + Gherkin acceptance criteria
2. Researcher (skill: /researcher) gathers docs, builds/updates skills files
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
   | USER SCOPE GATE A.6: Before proceeding:                          |
   | [] "User reviewed slice scope (summary + Gherkin + diagrams)"    |
   | [] "User responded APPROVE"                                      |
   | [] "Any scope changes from original plan were highlighted"        |
   +------------------------------------------------------------------+

PHASE A.7: RED TEAM + PROFESSOR PRE-BUILD GATE -- OPTIONAL (--high-risk only)
   Skip this phase unless the slice is flagged --high-risk. Default: SKIP.
9. Red Team sub-agent (skill: /red-team-reviewer) reviews the USER-CONFIRMED slice plan
10. Red Team evaluates all 10 attack dimensions
11. Red Team submits plan to external model for hostile review
12. Verdict: APPROVE / REVISE / BLOCK
    If BLOCK: implementation HALTS. Owner must override or plan must change.
    Artifact: reviews/slice-N-red-team-pre-build.md
13. Professor Review runs in parallel (domain expert review)
    Verdict: APPROVE / REVISE / BLOCK
    Artifact: reviews/slice-N-professor-pre-build.md

   +------------------------------------------------------------------+
   | A.7 GATE (if --high-risk): Before proceeding to Phase B:         |
   | [] "Red Team returned verdict: APPROVE or REVISE"                |
   | [] "Professor Review returned verdict: APPROVE or REVISE"        |
   | [] "reviews/slice-N-red-team-pre-build.md EXISTS on disk"        |
   | [] "reviews/slice-N-professor-pre-build.md EXISTS on disk"       |
   +------------------------------------------------------------------+

PHASE B: GHERKIN AUDIT + TEST SPECIFICATION + TEST PEER REVIEW (Article 17, 18)

   B.1: GHERKIN AUDIT (max 3 cycles)
   14. QA Lead audits Gherkin for completeness (traceability matrix) + quality
   15. Every user story element must map to at least one Gherkin scenario
   16. Quality check: unambiguous, concrete values, testable outcomes, NFR coverage
   17. If gaps: write missing Gherkin, re-audit (max 3 cycles, then owner sign-off)

   B.2: TEST SPECIFICATION (different agents from implementation coders)
   18. Architect defines skeletal interfaces (function sigs, class stubs, type stubs)
   19. QA Lead spawns test-writer sub-agents (NOT implementation coders)
   20. Test-writers write ALL tests: unit, integration, E2E definitions
   21. ALL tests must be RED (import errors or assertion failures)

   B.3: TEST PEER REVIEW (4 models, parallel -- Article 18; folded into Phase B)
   22. 4 peer reviewers (Gemini, OpenAI 5.5, Claude Opus 4.7, Grok) review test code in parallel
   23. Consensus issues (2+ reviewers) = mandatory test fixes
   24. Fixed tests re-validated: still RED against skeletal interfaces

   +------------------------------------------------------------------+
   | TEST SPEC GATE B: Before proceeding to implementation:           |
   | [] "Gherkin Audit PASSED (completeness + quality)"               |
   | [] "All tests written by test-writer sub-agents (not coders)"    |
   | [] "All tests are RED (import errors or assertion failures)"     |
   | [] "Skeletal interfaces exist for all tested modules"            |
   | [] "Test code peer-reviewed by 4 external models"                |
   | [] "reviews/slice-N-test-spec.md EXISTS on disk"                 |
   | [] "reviews/slice-N-test-review.md EXISTS on disk"               |
   | [] "CTO did NOT write any test code directly (Nuclear Rule 1)"   |
   +------------------------------------------------------------------+

PHASE C: IMPLEMENTATION
25. CTO assigns implementation coder teammates (skills: /coder-backend, /coder-frontend)
26. Coders receive failing tests + spec, write code until all tests PASS
27. Coders do NOT modify tests (only implementation code)

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
```
