# Article 17: Test-First Specification Protocol

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

The Test-First Specification Protocol ensures that all tests are written BEFORE implementation code, by DIFFERENT agents than those who write the implementation. This creates genuine independence and makes the test suite the source of truth for correctness.

#### 17a. Gherkin Audit (Phase B.1)

Before any test code is written, the QA Lead audits all Gherkin scenarios for the current slice:

**Completeness check:**
- Every user story element must map to at least one Gherkin scenario
- Every required edge case must map to at least one Gherkin scenario
- A traceability matrix is produced showing the mapping

**Quality check:**
- Each scenario is unambiguous (one interpretation, not multiple)
- Each scenario uses concrete values (not "a valid input")
- Each expected outcome is testable and specific
- NFR gaps checked (performance, security criteria have scenarios where applicable)

**Max 3 audit cycles.** If gaps remain after 3 cycles, owner sign-off is required to proceed.

#### 17b. Skeletal Interfaces

Before test-writers write tests, the Architect defines skeletal interfaces for all modules the slice will create or modify:

- Function signatures with type annotations and `raise NotImplementedError`
- Class outlines with method stubs returning `pass` or `raise NotImplementedError`
- Type stubs / interfaces for data structures

This allows tests to import modules cleanly. Both import errors and assertion failures are valid red states, but clean assertion failures are preferred for diagnostic clarity.

#### 17c. Test Specification (Phase B.2)

Test-writer sub-agents (spawned by QA Lead) write ALL test code:

- **Unit tests** -- individual functions, methods, classes in isolation
- **Integration tests** -- module interactions, database queries, API endpoints
- **E2E test definitions** -- full workflow definitions (actual browser E2E runs in Phase F)

Test-writers receive: Gherkin scenarios + slice spec + data contracts + skeletal interfaces. They write tests WITHOUT knowing how the code will be implemented.

**All tests must be RED** (failing) before proceeding. Tests that PASS against skeletal interfaces are bad tests -- they must be fixed.

#### 17d. Agent Separation

| Responsibility | Agent | Phase |
|---|---|---|
| Audit Gherkin completeness + quality | **QA Lead** | B.1 |
| Write test code | **Test-writer sub-agents** (spawned by QA Lead) | B.2 |
| Review test code | **Reviewer Gemini, OpenAI Codex, Grok** | B.3 |
| Write implementation code | **Implementation coder sub-agents** (spawned by Engineers) | C |

The same agent MUST NOT write both tests and implementation for the same slice. This is enforced by Nuclear Rule 1 gate: "CTO did NOT write any test code directly."

#### 17e. Autonomous Defect Resolution Protocol

Any agent that discovers a defect OWNS the fix lifecycle. The finding agent does not report and wait — it drives the defect to resolution by spawning a fix sub-agent and verifying the result. This applies in ALL testing phases (F, G, H, E2E Browser Testing, Peer Review).

**Fix Ownership Rule:** The agent that finds the bug spawns a **fix sub-agent** (ephemeral coder) to execute the protocol below. The finding agent verifies each step. The finding agent does NOT write production code itself — it delegates to the fix sub-agent and validates the outcome. This preserves role separation (QA agents do not write production code) while eliminating the bottleneck of routing every fix through the CTO.

Triggered by ANY source: user bug report, QA finding, security scan, Whiskey Team finding, peer review consensus finding, regression detection.

```
Step 1: AUDIT THE TEST
  Find the test that SHOULD have caught this defect.
  - Test exists but didn't catch it -> FIX THE TEST FIRST
  - No test exists -> Add Gherkin scenario first, then write test

Step 2: RED
  Run the corrected/new test against current (buggy) code. It MUST FAIL.
  - If it passes -> test still wrong, go back to Step 1

Step 3: GREEN
  Fix sub-agent fixes the production code until the test passes.

Step 4: REGRESSION
  Run the FULL test suite. Zero regressions allowed.
  - If regressions found -> fix sub-agent addresses them before proceeding

Step 5: CLASS SCAN
  Determine if the defect reveals a CATEGORY of missing coverage.
  - If yes: scan the ENTIRE codebase for all instances of the same pattern
  - Write tests for ALL instances (not just the one that was found)
  - Fix ALL instances in the same pass
  - Example: if a null-check was missing on one API endpoint, check ALL
    endpoints for the same missing null-check and fix them all

Step 6: COMMIT
  Test + fix committed together as an atomic unit.
  Commit message references the finding ID and the class scan scope.
```

**The test is always the source of truth.** A bug means the test was incomplete or wrong. Fix the test first, then fix the code. This ensures every bug found once is caught forever.

**Escalate to the user ONLY when:**
- The fix requires an architectural decision that changes the system design
- The fix modifies infrastructure outside the current workspace
- The fix has failed 3 times (3 fix sub-agent attempts, not 3 reporting cycles)

All other defects are resolved autonomously. The CTO is notified of completed fixes in the QA roll-up but does not need to approve each one individually.

#### 17f. Artifact

The test specification is saved to `reviews/slice-N-test-spec.md`. This file must exist on disk before Phase C (Implementation) can begin. See `review-templates/TEST-SPEC-TEMPLATE.md` for the full template.
