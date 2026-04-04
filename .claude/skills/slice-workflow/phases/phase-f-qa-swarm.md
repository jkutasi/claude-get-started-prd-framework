# Phase F: QA Swarm + Whiskey Team + UX Sense Check

> Load this file when starting Phase F. Complete all steps before proceeding to Phase F.5.

## Purpose

Full autonomous QA cycle. QA agents find bugs and fix them inline using the Autonomous Defect Resolution Protocol. The Whiskey Team runs adversarial testing. UX Sense Check validates the user experience.

## F.1: QA Swarm

> **QMD QUERY** (non-blocking): Spawn `/relay-qmd` — query `"QA failures root causes regressions {SLICE_TOPIC}"` in `{PROJECT_NAME}`. Share prior failure patterns with QA agents before they begin. If QMD unavailable, proceed.

1. QA Lead coordinates 5 QA agents running in parallel:
   - **Stats Verification** — numerical accuracy, calculation correctness.
   - **Code Quality** — structure, maintainability, error handling, type safety.
   - **Data Integrity** — data flow, persistence, transformation accuracy.
   - **Security** — auth, input sanitization, secrets, dependency vulnerabilities.
   - **UI/UX Browser Testing** — rendering, responsiveness, accessibility.

2. Each agent applies the **Autonomous Defect Resolution Protocol** (Article 17e):
   - Find bug → spawn fix sub-agent → AUDIT → RED → GREEN → REGRESSION → CLASS SCAN → COMMIT.

3. Use `review-templates/QA-SWARM-TEMPLATE.md` for the output format.

## F.2: Whiskey Team

4. Whiskey Team runs adversarial QA on 8 scope items:
   - API Round-Trip, API-to-Schema, Action Buttons, Frontend Pages, State Management, Early Termination, Data Integrity, **Goal Achievement Test**.
5. **MANDATORY:** Implicit behavior regression on 6 categories:
   - State Transition Gaps, Cross-Component Interactions, Data Flow Assumptions, Race Conditions, Silent Failures, Edge Case Combinations.
6. Whiskey Team applies the same autonomous fix protocol.
7. Use `review-templates/WHISKEY-TEAM-TEMPLATE.md` for the output format.

## F.3: UX Sense Check (frontend slices only)

8. 3 personas navigate the UI via agent-browser.
9. Each persona evaluates: first impression, label clarity, action clarity, result comprehension, error recovery, flow completeness, jargon.
10. Use `review-templates/UX-SENSE-CHECK-TEMPLATE.md` for the output format.

## F.4: Synthesis

11. QA Manager synthesizes ALL findings + autonomous fix results.
12. Professor Review also runs post-QA on aggregate findings.

> **QMD SAVE** (non-blocking): Spawn `/relay-qmd` — save novel QA findings and root causes to `vault/projects/{PROJECT_NAME}/qa-findings-slice-{N}.md`. If QMD unavailable, skip.

## Artifacts

- `reviews/slice-N-qa-swarm.md`
- `reviews/slice-N-whiskey-team.md`
- `reviews/slice-N-ux-sense-check.md` (if frontend)

## Next Phase

Proceed to **Phase F.5: Runtime Log Check** (`phase-f5-runtime-log-check.md`).
