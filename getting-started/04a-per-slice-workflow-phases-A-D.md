# Step 4a: Per-Slice Workflow — Phases A through D

> Sub-file of [04-per-slice-workflow.md](04-per-slice-workflow.md). Contains Phases A, A.5, A.6, A.7, B, C, D.

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

   B.3: TEST PEER REVIEW (4 models, parallel -- Article 18)
   18. 4 peer reviewers (Gemini, OpenAI 5.5, Claude Opus 4.7, Grok) review test code in parallel
   19. Consensus (2+) = mandatory test fixes before proceeding

   +-----------------------------------------------------------------+
   | TEST SPEC GATE B: CTO must confirm:                             |
   | [] "Gherkin Audit PASSED (completeness + quality)"              |
   | [] "All tests written by test-writer sub-agents (not coders)"   |
   | [] "All tests are RED"                                          |
   | [] "Test code peer-reviewed by 4 external models"               |
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
```
