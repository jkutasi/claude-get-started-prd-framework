# Phase B: Gherkin Audit + Test Specification + Test Peer Review

> Load this file when starting Phase B. Complete all three sub-phases and the gate before proceeding to Phase C.
> Test Peer Review is folded into Phase B — no separate B.3 phase.

## Purpose

Write all tests BEFORE any implementation code. Tests are written by test-writer sub-agents
(NOT implementation coders). All tests must be RED. Peer review of test code happens here,
not in a separate phase.

## B.1: Gherkin Audit (max 3 cycles)

1. QA Lead audits Gherkin for completeness using a traceability matrix.
2. Every user story element must map to at least one Gherkin scenario.
3. Quality checks: unambiguous, concrete values, testable outcomes, NFR coverage.
4. Max 3 audit cycles. If gaps remain after 3, owner sign-off required.

## B.2: Test Specification

> **QMD QUERY** (non-blocking): Spawn `/relay-qmd` — query `"test patterns edge cases failures {SLICE_TOPIC}"` in `{PROJECT_NAME}`. Incorporate findings into test scenarios before test-writers begin. If QMD unavailable, proceed.

5. Architect defines skeletal interfaces (function signatures, class stubs).
6. QA Lead spawns **test-writer sub-agents** (NOT implementation coders — firewalled).
7. Test-writers write ALL tests: unit, integration, E2E definitions.
8. ALL tests must be **RED** (import errors or assertion failures).
   - `ImportError` / `ModuleNotFoundError` = valid red.
   - Assertion failure against stub = valid red.
   - Tests that PASS = bad test (testing nothing) — MUST be fixed.

Use `review-templates/TEST-SPEC-TEMPLATE.md` for the output format.

## B.3: Test Peer Review (4 models, parallel — folded into Phase B)

See Article 18 for the canonical reviewer lineup and procedure.

9. All 4 peer reviewers (Gemini, OpenAI 5.5, Claude Opus 4.7, Grok) review test code in parallel.
10. Consensus (2+ reviewers agree) = mandatory test fixes before proceeding.
11. Fixed tests re-validated: still RED against skeletal interfaces.
12. Use `review-templates/TEST-REVIEW-TEMPLATE.md` for the output format.

## Artifacts

- `reviews/slice-N-test-spec.md` — Test specification document.
- `reviews/slice-N-test-review.md` — Test code peer review results.
- Consolidated in `reviews/slice-{N}.md` (section: Tests).

## Gate

```
+------------------------------------------------------------------+
| TEST SPEC GATE B: CTO must confirm:                              |
| [] "Gherkin Audit PASSED (completeness + quality)"               |
| [] "All tests written by test-writer sub-agents (not coders)"    |
| [] "All tests are RED"                                           |
| [] "Test code peer-reviewed by 4 external models"                |
| [] "Consensus fixes applied and tests re-validated still RED"    |
| [] "reviews/slice-N-test-spec.md EXISTS on disk"                 |
| [] "reviews/slice-N-test-review.md EXISTS on disk"               |
| [] "CTO did NOT write any test code directly"                    |
+------------------------------------------------------------------+
```

## Next Phase

Proceed to **Phase C: Implementation** (`phase-c-implementation.md`).
