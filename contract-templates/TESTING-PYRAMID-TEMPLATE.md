# Testing Pyramid & Standards — {PROJECT_NAME}

> Part of the testing contract. See also: [Testing Procedures](TESTING-PROCEDURES-TEMPLATE.md) and [Testing Gates](TESTING-GATES-TEMPLATE.md).

## Testing Pyramid

All slices are tested through a 6-layer pyramid. Every layer is mandatory unless explicitly noted.

| Layer | What It Tests | Tool | Who Runs It | When |
|-------|--------------|------|-------------|------|
| **1. Unit** | Individual functions, methods, classes in isolation | {TEST_FRAMEWORK -- e.g., pytest, vitest, jest} | Test-writer sub-agents (Phase B) | Phase B -- before code, must all be RED |
| **2. Integration** | Module interactions, database queries, API endpoints | {TEST_FRAMEWORK} + {DB_FIXTURES} | Test-writer sub-agents (Phase B) | Phase B -- before code, must all be RED |
| **3. E2E Browser** | Full user workflows through a real browser | **agent-browser (MANDATORY)**, Playwright for CI regression | QA UI/UX agent + UX Sense Check (Phase F) | During QA swarm phase |
| **4. Adversarial QA** | Edge cases, boundary conditions, security surfaces, silent failures | QA Security + QA Stats agents via `openai_code.py qa` | QA Swarm (Phase F) | Parallel with standard QA swarm |
| **5. UX Sense-Check (Personas)** | Usability from non-technical user perspectives across 7 test areas | agent-browser + persona prompts | UX Sense Check agent (Phase F) — optional, frontend only | Frontend slices only, parallel with QA swarm |
| **6. Implicit Regression** | Default values, sort order, empty states, loading states, error messages, navigation flow | Playwright smoke with regression assertions | Phase J gate | After every slice |

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

## Test Priority Classification (Article 20)

Features are classified by business criticality during planning (Step 1e). Classification determines coverage requirements.

| Priority | Definition | Coverage Requirement | When Tested |
|----------|-----------|---------------------|-------------|
| **P0** | If it breaks, everything is down. Revenue-critical. | 100% service-layer coverage | Tested FIRST in Phase B |
| **P1** | Important but not catastrophic | ≥ 90% service-layer coverage | Tested after P0 |
| **P2** | Nice-to-have | Best-effort coverage | Tested last |

P0 and P1 features MUST have test coverage. P0 is never deprioritized under time pressure.

---

## Service-Layer Testing Emphasis

Tests focus on the **service layer** — that is where business logic lives (Article 20b). The service layer is the primary target for unit test coverage.

- **Service tests:** Verify business logic correctness. Highest test density.
- **Route tests:** Minimal — verify HTTP plumbing (status codes, request parsing). ~2-3 tests per route.
- **Repository tests:** Use integration test fixtures. Verify queries return expected data.

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

Every slice MUST include edge case scenarios covering ALL 8 mandatory categories:

1. Empty input / empty dataset
2. Maximum length / maximum volume input
3. Special characters and unicode
4. Zero and negative values (where numeric input applies)
5. Duplicate submissions
6. External service timeout / unavailable (database connections, API endpoints, third-party services)
7. Concurrent modification (if multi-user)
8. {PROJECT_SPECIFIC_EDGE_CASE}

The test-writer sub-agents include edge case tests during Phase B. QA agents verify completeness and add missing cases during Phase F.

**File location:** Unit tests live in the feature folder alongside the service file: `src/{feature-name}/{feature-name}.test.{EXT}`. Cross-feature integration tests live in `tests/integration/`. See Article 20a for the full directory structure.
