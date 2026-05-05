# Article 15: Whiskey Team Adversarial QA & Implicit Behavior Regression

> **DEPRECATED 2026-05-05.** Whiskey Team's adversarial QA was redundant with Phase E peer
> review and Phase F QA Swarm. Implicit regression duty moved to Phase J Playwright smoke.
> This article is retained for historical reference only. Do not invoke this workflow in new
> slices.

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

The Whiskey Team is a dedicated adversarial QA layer that tests the system from a "drunk user" perspective — clumsy inputs, wrong order of operations, abandoned workflows, and unexpected usage patterns. It also runs a MANDATORY implicit behavior regression check every session.

#### 15a. Whiskey Team Testing Scope (8 MANDATORY Areas)

The Whiskey Team MUST test all of the following:

| # | Test Category | What to Test |
|---|--------------|-------------|
| 1 | **API Round-Trip Verification** | Send valid, invalid, and malicious payloads to every API endpoint the slice touches. Verify response schema, status code, and data correctness against the data store. |
| 2 | **API-to-Schema Verification** | Compare every API response against the DATA_CONTRACT schemas. Every field must match. Any drift = P0. |
| 3 | **Action Button Verification** | Click every single button on the page. Verify network request, response, UI update, disabled state, and double-click behavior. Zero exceptions. |
| 4 | **Frontend Page Verification** | Load every page the slice touches. Check console errors, interactive elements, keyboard navigation, empty sessions, loading states, error states. |
| 5 | **State Management** | Test flickering, persistence across refresh, error clearing, loading resolution, silent failures, stale state across tabs. |
| 6 | **Early Termination & Partial Completion** | Test early convergence, partial success, zero results, timeout behavior, and re-entry after abandonment. |
| 7 | **Data Integrity** | Verify UI-to-data-store match for every number, string, date. Check number formatting, special characters, null handling, timezone handling. |
| 8 | **Goal Achievement Test** | Navigate the full user workflow end-to-end via agent-browser. Can a user achieve the stated goal? Binary PASS/FAIL. FAIL = P0 = slice cannot ship. |

#### 15b. Implicit Behavior Regression (MANDATORY Every Session — 6 Categories)

This check is MANDATORY at the start of EVERY session and after EVERY slice completion. It catches behaviors that silently change when code is modified — things that no test explicitly covers because they were "obviously correct" before.

| # | Category | What to Verify |
|---|----------|---------------|
| 1 | **State Transition Gaps** | Are there states the system can enter but not exit? Can the user get stuck? |
| 2 | **Cross-Component Interactions** | Does changing component A affect component B in unexpected ways? |
| 3 | **Data Flow Assumptions** | Are there assumptions about data shape that could silently fail? |
| 4 | **Race Conditions** | Can concurrent user actions produce inconsistent state? |
| 5 | **Silent Failures** | Are there operations that fail without any visible error? |
| 6 | **Edge Case Combinations** | What happens when multiple edge cases combine? |

**This is not optional.** Implicit behavior regression is the single most common source of "it works but something feels wrong" bugs. All 6 categories MUST be checked every session.

#### 15c. WHISKEY FINDING Format

Every Whiskey Team finding follows this format:

```
### WHISKEY FINDING #{N}: {Title}
**Category:** {one of the 8 test categories or one of the 6 regression categories}
**Severity:** {CRITICAL / HIGH / MEDIUM / LOW}
**Steps to Reproduce:**
1. {step}
2. {step}
3. {step}
**Expected:** {what should happen}
**Actual:** {what actually happened}
**Impact:** {what this means for the user}
**Roast:** {one-sentence cynical commentary — MANDATORY}
```

#### 15d. Activation & Rules

- The Whiskey Team runs on EVERY slice. No exceptions. Even backend-only slices may have implicit behavior regressions.
- Whiskey Team findings classified as CRITICAL or HIGH are blocking — they must be fixed before the slice ships.
- The Goal Achievement Test (area #8) is a hard gate: if the system does not achieve its stated goal, the slice FAILS regardless of all other tests passing.
- Findings are saved to `reviews/slice-N-whiskey-team.md`.
