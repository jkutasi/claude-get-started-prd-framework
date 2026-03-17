# Phase B: Gherkin Audit + Test Specification + Test Peer Review

> Load this file when starting Phase B. Complete all three sub-phases and the gate before proceeding to Phase C.

## Purpose

Write all tests BEFORE any implementation code. Tests are written by test-writer sub-agents (NOT implementation coders). All tests must be RED.

## B.1: Gherkin Audit (max 3 cycles)

1. QA Lead audits Gherkin for completeness using a traceability matrix.
2. Every user story element must map to at least one Gherkin scenario.
3. Quality checks: unambiguous, concrete values, testable outcomes, NFR coverage.
4. Max 3 audit cycles. If gaps remain after 3, owner sign-off required.

## B.2: Test Specification

5. Architect defines skeletal interfaces (function signatures, class stubs).
6. QA Lead spawns **test-writer sub-agents** (NOT implementation coders — firewalled).
7. Test-writers write ALL tests: unit, integration, E2E definitions.
8. ALL tests must be **RED** (import errors or assertion failures).
   - `ImportError` / `ModuleNotFoundError` = valid red.
   - Assertion failure against stub = valid red.
   - Tests that PASS = bad test (testing nothing) — MUST be fixed.

Use `review-templates/TEST-SPEC-TEMPLATE.md` for the output format.

## B.3: Test Peer Review (3+ models, parallel)

9. 3 peer reviewers (+ Greptile if configured) review test code in parallel.
10. Consensus (2+ reviewers agree) = mandatory test fixes before proceeding.
11. Use `review-templates/TEST-REVIEW-TEMPLATE.md` for the output format.

## Artifacts

- `reviews/slice-N-test-spec.md` — Test specification document.
- `reviews/slice-N-test-review.md` — Test code peer review results.

## Gate

```
+------------------------------------------------------------------+
| TEST SPEC GATE B: CTO must confirm:                              |
| [] "Gherkin Audit PASSED (completeness + quality)"               |
| [] "All tests written by test-writer sub-agents (not coders)"    |
| [] "All tests are RED"                                           |
| [] "Test code peer-reviewed by 3+ external models"               |
| [] "reviews/slice-N-test-spec.md EXISTS on disk"                 |
| [] "reviews/slice-N-test-review.md EXISTS on disk"               |
| [] "CTO did NOT write any test code directly"                    |
+------------------------------------------------------------------+
```

## Next Phase

Proceed to **Phase C: Implementation** (`phase-c-implementation.md`).
