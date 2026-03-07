# Testing Procedures — {PROJECT_NAME}

> Part of the testing contract. See also: [Testing Pyramid](TESTING-PYRAMID-TEMPLATE.md) and [Testing Gates](TESTING-GATES-TEMPLATE.md).

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

Test code gets the same 3+-model peer review as implementation code:

1. Spawn Reviewer Gemini, Reviewer OpenAI Codex, Reviewer Grok in parallel (+ Reviewer Greptile if `GREPTILE_API_KEY` is configured)
2. Each reviews the test code for: test quality, coverage gaps, assertion specificity, mock correctness, test independence, red phase validity, Gherkin alignment
3. Consensus issues (2+ reviewers agree) = mandatory test fixes before proceeding
4. Single-reviewer issues = recommended fixes (CTO judgment)
5. Findings saved to `reviews/slice-N-test-review.md`

See `review-templates/TEST-REVIEW-TEMPLATE.md` for the full template.

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

Peer review uses 3+ external model APIs. API keys must be in `.env`:

```
GEMINI_API_KEY={YOUR_KEY}
OPENAI_API_KEY={YOUR_KEY}
XAI_API_KEY={YOUR_KEY}
GREPTILE_API_KEY={YOUR_KEY}   # Optional — enables 4th reviewer
```

**Steps (CTO executes):**

1. Collect all code files changed in the current slice
2. Spawn 3+ reviewer sub-agents in parallel:
   - **Reviewer Gemini:** Reads the code, sends to Gemini API with review prompt, returns structured findings
   - **Reviewer OpenAI Codex:** Executes Codex CLI in read-only sandbox with review prompt, returns structured findings
   - **Reviewer Grok:** Reads the code, sends to Grok/xAI API with review prompt, returns structured findings
   - **Reviewer Greptile (optional):** Sends code to Greptile API for codebase-aware review, returns structured findings. Only spawned if `GREPTILE_API_KEY` is configured.
3. Wait for ALL reviewers to return. Do NOT proceed with partial reviews.
4. CTO synthesizes all findings:
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

For suspected cross-cutting backend issues, the 6-Agent Backend QA Sweep (Article 25) provides a structured diagnostic protocol with domain-scoped agents.

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
