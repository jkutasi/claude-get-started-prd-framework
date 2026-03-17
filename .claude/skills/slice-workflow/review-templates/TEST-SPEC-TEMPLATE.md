# Test Specification — Slice {N}: {SLICE_NAME}

> **Phase B artifact.** Created during Phase B (Gherkin Audit + Test Specification). Test-writer sub-agents write the actual test code. Implementation coders are firewalled from this phase.

---

## B.1: Gherkin Audit

### Traceability Matrix

Every user story element MUST map to at least one Gherkin scenario. Gaps = audit FAIL.

| # | User Story Element | Gherkin Scenario(s) | Feature File | Status |
|---|---|---|---|---|
| 1 | {STORY_ELEMENT_1} | {SCENARIO_NAME} | `features/slice-{N}-{feature}.feature` | COVERED / GAP |

### Edge Case Coverage

| # | Edge Case | Gherkin Scenario | Status |
|---|---|---|---|
| 1 | Empty input / empty dataset | {SCENARIO_NAME} | COVERED / GAP |
| 2 | Maximum length / volume | {SCENARIO_NAME} | COVERED / GAP |
| 3 | Special characters / unicode | {SCENARIO_NAME} | COVERED / GAP |
| 4 | Zero / negative values | {SCENARIO_NAME} | COVERED / GAP |
| 5 | Duplicate submissions | {SCENARIO_NAME} | COVERED / GAP |
| 6 | External service timeout / unavailable | {SCENARIO_NAME} | COVERED / GAP |
| 7 | Concurrent modification | {SCENARIO_NAME} | COVERED / GAP |
| 8 | {PROJECT_SPECIFIC_EDGE_CASE} | {SCENARIO_NAME} | COVERED / GAP |

### Quality Checklist

- [ ] Each scenario is **unambiguous** (one interpretation, not multiple)
- [ ] Each scenario uses **concrete values** (not "a valid input")
- [ ] Each expected outcome is **testable and specific**
- [ ] NFR gaps checked (performance, security criteria have scenarios where applicable)
- [ ] Goal Achievement Test scenario exists (`@goal-achievement @critical`)

### Audit Cycles

| Cycle | Gaps Found | Gaps Fixed | Result |
|---|---|---|---|
| 1 | {COUNT} | {COUNT} | PASS / FAIL |
| 2 | {COUNT} | {COUNT} | PASS / FAIL |
| 3 | {COUNT} | {COUNT} | PASS / FAIL or OWNER SIGN-OFF |

**Max 3 cycles.** If gaps remain after 3 cycles, owner sign-off is required.

---

## B.2: Test Specification

### Skeletal Interfaces

| Module | Interface / Function | Stub Type | File Path |
|---|---|---|---|
| {MODULE_1} | `{function_name}({params}) -> {return_type}` | `raise NotImplementedError` | `{FILE_PATH}` |

- [ ] All skeletal interfaces created
- [ ] All interfaces importable without errors
- [ ] All methods raise `NotImplementedError` or return `pass`

### Unit Tests

| # | Test File | What It Tests | Gherkin Scenario(s) | Status |
|---|---|---|---|---|
| 1 | `src/{feature}/{feature}.test.{ext}` | {DESCRIPTION} | {SCENARIO_REF} | RED / PASS (bad) |

### Integration Tests

| # | Test File | What It Tests | Components Involved | Status |
|---|---|---|---|---|
| 1 | `tests/integration/test_{feature}.py` | {DESCRIPTION} | {COMPONENTS} | RED / PASS (bad) |

### E2E Test Definitions

| # | Workflow | Gherkin Scenario | Browser Required | Status |
|---|---|---|---|---|
| 1 | {WORKFLOW_NAME} | {SCENARIO_REF} | Yes / No | Defined / Deferred to Phase F |

---

## Red Phase Validation

All tests MUST be RED before proceeding to Phase C.

| Test Category | Total Tests | RED (valid) | PASS (bad) | ERROR (harness) |
|---|---|---|---|---|
| Unit | {COUNT} | {COUNT} | {COUNT} | {COUNT} |
| Integration | {COUNT} | {COUNT} | {COUNT} | {COUNT} |
| **Total** | **{COUNT}** | **{COUNT}** | **{COUNT}** | **{COUNT}** |

- [ ] All tests are RED (import errors or assertion failures)
- [ ] Zero tests PASS (any passing test = bad test)
- [ ] Zero harness errors

---

## Test Spec Gate Checklist

```
+------------------------------------------------------------------+
| TEST SPEC GATE B: Before proceeding to Phase C:                  |
| [] Gherkin Audit PASSED (completeness + quality)                 |
| [] All tests written by test-writer sub-agents (not coders)      |
| [] All tests are RED (import errors or assertion failures)       |
| [] Skeletal interfaces exist for all tested modules              |
| [] Test code peer-reviewed by 3 external models (Phase B.3)     |
| [] reviews/slice-N-test-spec.md EXISTS on disk (this file)       |
| [] reviews/slice-N-test-review.md EXISTS on disk                 |
| [] CTO did NOT write any test code directly (Nuclear Rule 1)    |
+------------------------------------------------------------------+
```
