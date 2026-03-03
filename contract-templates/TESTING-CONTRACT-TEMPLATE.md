# Testing Contract -- {PROJECT_NAME}

## Testing Pyramid

All slices are tested through a 6-layer pyramid. Every layer is mandatory unless explicitly noted.

| Layer | What It Tests | Tool | Who Runs It | When |
|-------|--------------|------|-------------|------|
| **1. Unit** | Individual functions, methods, classes in isolation | {TEST_FRAMEWORK -- e.g., pytest, vitest, jest} | Test-writer sub-agents (Phase B) | Phase B -- before code, must all be RED |
| **2. Integration** | Module interactions, database queries, API endpoints | {TEST_FRAMEWORK} + {DB_FIXTURES} | Test-writer sub-agents (Phase B) | Phase B -- before code, must all be RED |
| **3. E2E Browser** | Full user workflows through a real browser | **agent-browser (MANDATORY)**, Playwright for CI regression | QA UI/UX agent + UX Sense Check (Phase F) | During QA swarm phase |
| **4. Adversarial (Whiskey)** | Clumsy inputs, wrong order of operations, abandoned workflows, rapid actions, boundary conditions, state corruption, accessibility under stress | Whiskey Team sub-agent (black-box testing) | Whiskey Team (Phase F) | Parallel with standard QA swarm |
| **5. UX Sense-Check (Personas)** | Usability from non-technical user perspectives across 7 test areas | agent-browser + persona prompts | UX Sense Check agent (Phase F) | Frontend slices only, parallel with QA swarm |
| **6. Implicit Regression** | Default values, sort order, empty states, loading states, error messages, navigation flow | Whiskey Team regression check (6 categories) | Whiskey Team (Phase H) | Every session start + after every slice |

**agent-browser (Vercel) is MANDATORY for layers 3 and 5.** Playwright is permitted ONLY for automated CI/CD regression scripts. See the Browser Testing Protocol section below.

---

## Coverage Targets

| Scope | Target | Enforcement |
|-------|--------|-------------|
| Unit tests -- business logic + public interfaces | **≥ 90%** | Enforced at gate check (Phase J). Exemptions for generated code, defensive branches, and bootstrap scaffolding must be documented in the QA roll-up. |
| Integration tests | All critical paths covered | Reviewed during QA swarm. Gaps flagged as mandatory fixes. |
| Gherkin scenarios | At least 1 `.feature` file per slice | Enforced by `gate_check.py`. Missing = slice FAILS. |
| Edge cases | Minimum {MIN_EDGE_CASES} per slice | Enforced during QA swarm. Coder must identify edge cases; QA verifies completeness. |

---

## Gherkin Standards

All acceptance criteria are expressed as Gherkin feature files in the `features/` directory.

**File naming:** `features/slice-{N}-{feature-name}.feature`

**Format:**
```gherkin
@slice-{N} @{CATEGORY_TAG}
Feature: {Feature Name} -- {Category}
  As a {USER_ROLE}
  I want {ACTION_OR_CAPABILITY}
  So that {BUSINESS_VALUE}

  Background:
    Given {SHARED_PRECONDITION}

  Scenario: {Descriptive scenario name}
    Given {PRECONDITION}
    When {ACTION}
    Then {EXPECTED_OUTCOME}
    And {ADDITIONAL_ASSERTION}
```

**Rules:**
- One behavior per scenario. If you need "and then also," that is a second scenario.
- Business language, not code. Say what the user or system does, not how the code implements it.
- Concrete values, not vague descriptions. Say "the price is 105.50" not "the price is a number."
- Use `Scenario Outline` with `Examples` tables for data-driven tests.
- Tag every scenario: `@slice-N`, `@critical`, `@frontend`, `@edge-cases`, `@performance`, `@goal-achievement`.
- See `examples/gherkin-examples.md` for full templates.

---

## Edge Case Requirements

Every slice MUST include edge case scenarios covering at minimum:

1. Empty input / empty dataset
2. Maximum length / maximum volume input
3. Special characters and unicode
4. Zero and negative values (where numeric input applies)
5. Duplicate submissions
6. Network timeout or dependency failure
7. Concurrent modification (if multi-user)
8. {PROJECT_SPECIFIC_EDGE_CASE}

The test-writer sub-agents include edge case tests during Phase B. QA agents verify completeness and add missing cases during Phase F.

---

## Gherkin Audit Protocol (Phase B.1)

Before any test code is written, the QA Lead audits all Gherkin scenarios for completeness AND quality. This is a mandatory gate.

**Completeness check (traceability matrix):**
- Every user story element must map to at least one Gherkin scenario
- Every required edge case must map to at least one Gherkin scenario
- **FAIL** if gaps exist -- write missing Gherkin, then re-audit

**Quality check:**
- Each scenario is **unambiguous** (one interpretation, not multiple)
- Each scenario uses **concrete values** (not "a valid input")
- Each expected outcome is **testable and specific**
- No NFR gaps (performance, security criteria have scenarios where applicable)

**Max 3 audit cycles.** If gaps remain after 3 cycles, owner sign-off is required to proceed.

The audit produces a traceability matrix saved in `reviews/slice-N-test-spec.md`. See `review-templates/TEST-SPEC-TEMPLATE.md` for the full template.

---

## Test-First Protocol (Phase B.2)

After the Gherkin audit passes, test-writer sub-agents write all test code BEFORE any implementation code exists. This is the core of the test-first workflow.

**Agent separation (critical):**

| Responsibility | Agent | Phase |
|---|---|---|
| Define WHAT must be tested | **QA Lead** | B.1-B.2 |
| Write test code | **Test-writer sub-agents** (spawned by QA Lead) | B.2 |
| Write implementation code | **Implementation coder sub-agents** (spawned by Engineers) | C |

Test-writer sub-agents receive the Gherkin scenarios + slice spec + data contracts. They write tests WITHOUT knowing how the code will be implemented. Implementation coders receive the failing tests + spec and write code to make them pass WITHOUT seeing how the tests were designed.

**What "RED" means:**
- Tests that crash on `ImportError` / `ModuleNotFoundError` = valid red state (module doesn't exist yet)
- Tests that fail on assertions = valid red state (stub returns wrong value)
- Tests that PASS = bad test (testing nothing) -- must be fixed before proceeding

**All tests must be RED before Phase C (Implementation) begins.**

---

## Skeletal Interfaces Requirement

Before test-writer sub-agents write tests, the Architect defines skeletal interfaces for all modules the slice will create or modify:

- **Function signatures** with type annotations and `raise NotImplementedError`
- **Class outlines** with method stubs returning `pass` or `raise NotImplementedError`
- **Type stubs** / interfaces for data structures

This allows tests to import modules cleanly and fail on assertions (not on import errors), providing cleaner diagnostic output. Both import errors and assertion failures are valid red states, but clean assertion failures are preferred.

---

## Test Peer Review (Phase B.3)

Test code gets the same 3-model peer review as implementation code:

1. Spawn Reviewer Gemini, Reviewer OpenAI, Reviewer Grok in parallel
2. Each reviews the test code for: test quality, coverage gaps, assertion specificity, mock correctness, test independence, red phase validity, Gherkin alignment
3. Consensus issues (2+ reviewers agree) = mandatory test fixes before proceeding
4. Single-reviewer issues = recommended fixes (CTO judgment)
5. Findings saved to `reviews/slice-N-test-review.md`

See `review-templates/TEST-REVIEW-TEMPLATE.md` for the full template.

---

## Defect Resolution Protocol

Triggered by ANY source: user bug report, QA finding, security scan, Whiskey Team finding. Runs during Phase G (Fix Review + Red Team Escalation).

```
Step 1: AUDIT THE TEST
  Find the test that SHOULD have caught this defect.
  - Test exists but didn't catch it -> FIX THE TEST FIRST
  - No test exists -> Add Gherkin scenario first, then write test

Step 2: VERIFY THE TEST FAILS
  Run the corrected/new test against current code. It MUST FAIL.
  - If it passes -> test still wrong, go back to Step 1

Step 3: FIX THE CODE
  Implementation coder fixes code until the test passes.
  ALL existing tests re-run (no regressions).
  Defect is permanently captured in the test suite.
```

**The test is always the source of truth.** A bug means the test was incomplete or wrong. Fix the test first, then fix the code. This ensures every bug that is found once is caught forever.

---

## Browser Testing Protocol

| Tool | Use Case | When |
|------|----------|------|
| **agent-browser (Vercel)** | All interactive browser QA, persona testing, exploratory testing, visual checks | MANDATORY for all browser QA during slice development |
| **Playwright** | Automated regression scripts, CI/CD pipeline checks, headless screenshot comparison | OPTIONAL, for regression automation only |

**agent-browser is not optional.** If a QA agent or UX Sense Check agent needs to interact with a browser, it uses agent-browser. No exceptions.

---

## Mock Strategy

| Dependency | Mock Method | When to Mock | When to Use Real |
|-----------|-------------|-------------|-----------------|
| External APIs | {MOCK_LIBRARY — e.g., responses, nock, msw} | Unit tests, integration tests | E2E browser tests only |
| Database | {STRATEGY — e.g., in-memory SQLite, test fixtures} | Unit tests | Integration + E2E tests |
| File system | {STRATEGY — e.g., tmp_path, memfs} | Unit tests | Integration tests |
| Time/dates | {STRATEGY — e.g., freezegun, vi.useFakeTimers} | Any test with time-dependent logic | Never in production |
| {DEPENDENCY} | {MOCK_METHOD} | {WHEN_MOCK} | {WHEN_REAL} |

**Rule:** Mocks must match real behavior. If the real API returns paginated results, the mock must too. If the real database enforces constraints, the mock must too. Mocks that are simpler than reality produce tests that pass but code that fails.

---

## How to Run Peer Review (Step-by-Step)

Peer review uses 3 external model APIs. API keys must be in `.env`:

```
GEMINI_API_KEY={YOUR_KEY}
OPENAI_API_KEY={YOUR_KEY}
XAI_API_KEY={YOUR_KEY}
```

**Steps (CTO executes):**

1. Collect all code files changed in the current slice
2. Spawn 3 reviewer sub-agents in parallel:
   - **Reviewer Gemini:** Reads the code, sends to Gemini API with review prompt, returns structured findings
   - **Reviewer OpenAI:** Reads the code, sends to OpenAI API with review prompt, returns structured findings
   - **Reviewer Grok:** Reads the code, sends to Grok/xAI API with review prompt, returns structured findings
3. Wait for ALL 3 reviewers to return. Do NOT proceed with partial reviews.
4. CTO synthesizes all 3 findings:
   - Issues flagged by 2+ reviewers = **mandatory fixes**
   - Issues flagged by 1 reviewer = **recommended fixes** (CTO judgment)
5. Save all findings + synthesis to `reviews/slice-N-peer-review.md`
6. Assign mandatory fixes to coder teammates. Do NOT fix them yourself.

---

## How to Run QA Swarm (Step-by-Step)

**Steps (CTO or QA Lead executes):**

1. Spawn QA sub-agents in parallel (red team framing -- Article 7c):
   - **QA Stats** -- validates math correctness, algorithm logic, edge cases
   - **QA Code Quality** -- clean code, patterns, DRY, naming (Article 10)
   - **QA Data Integrity** -- query correctness, schemas, data validation
   - **QA Security** -- OWASP, API key exposure, injection vectors
   - **QA UI/UX + Browser** -- accessibility, responsive design, browser compat (via agent-browser)
2. Wait for ALL QA agents to return findings
3. QA Manager synthesizes all findings into a prioritized fix plan
4. Save all findings + synthesis to `reviews/slice-N-qa-swarm.md`
5. Then run additional mandatory layers:
   - **Red Team post-QA** (Article 14b) -- save to `reviews/slice-N-red-team.md`
   - **Whiskey Team** (Article 15) -- save to `reviews/slice-N-whiskey-team.md`
   - **UX Sense Check** (Article 16, frontend only) -- save to `reviews/slice-N-ux-sense-check.md`

---

## Retroactive Review Process

If any slice shipped WITHOUT peer review or QA (contract violation), the next session MUST:

1. Check `reviews/` directory for missing artifact files
2. Run retroactive peer review on each unreviewed slice (spawn reviewer sub-agents)
3. Run retroactive QA swarm on each unreviewed slice (spawn QA sub-agents)
4. Save all artifacts to `reviews/`
5. Fix any mandatory issues found
6. Only then proceed with new work

All code written without peer review is considered UNVALIDATED and SUSPECT.

---

## Slice Gate Enforcement Checklist

Before a slice can ship, the gate check script (`python gate_check.py --slice N`) verifies:

- [ ] `reviews/slice-N-test-spec.md` exists and is non-empty
- [ ] `reviews/slice-N-test-review.md` exists and is non-empty
- [ ] `reviews/slice-N-peer-review.md` exists and is non-empty
- [ ] `reviews/slice-N-qa-swarm.md` exists and is non-empty
- [ ] `reviews/slice-N-red-team-pre-build.md` exists and is non-empty
- [ ] `reviews/slice-N-red-team.md` exists and is non-empty
- [ ] `reviews/slice-N-whiskey-team.md` exists and is non-empty
- [ ] `reviews/slice-N-ux-sense-check.md` exists (frontend slices, enabled with `--frontend`)
- [ ] At least one Gherkin feature file exists: `features/slice-N-*.feature`
- [ ] At least one unit test file exists: `tests/*slice_N*` or `tests/*slice-N*`
- [ ] All tests pass
- [ ] Unit test coverage ≥ 90% on business logic + public interfaces (exemptions documented)

**If the script returns FAIL, the slice has NOT shipped. Do NOT start the next slice.**

---

## Goal Achievement Test Requirement

Every slice MUST include a Goal Achievement Test (Article 15, item #1). This is a single Gherkin scenario tagged `@goal-achievement @critical` that validates the complete user workflow from start to finish.

The Goal Achievement Test is a **hard gate:** if the system does not achieve its stated goal, the slice FAILS regardless of all other tests passing. There is no partial credit -- the user either achieves their goal or they do not.

See `examples/gherkin-examples.md` Template 5 for the Goal Achievement Test format.

---

## Nuclear Rules Reminder

These three rules override everything else. Violation = immediate stop.

1. **CTO Never Writes Code.** All code via teammates and sub-agents. No exceptions.
2. **Peer Review Is Mandatory.** Every slice, every time. All reviewers must report. No partial reviews.
3. **Slices Ship Complete.** All gates passed, all artifacts on disk, or the slice is invalid. No starting the next slice until this one is fully done.

Testing is not a phase you "get to later." Tests are written FIRST (Phase B) by independent test-writer sub-agents, before any implementation code exists (Phase C). Code without tests is incomplete. Tests without peer review are untrusted. QA without artifacts on disk is unproven.
