# Phase F: QA Swarm + UX Sense Check

> Load this file when starting Phase F. Complete all steps before proceeding to Phase F.5.

## Purpose

Full autonomous QA cycle. 7 QA agents call OpenAI 5.5 via openai_code.py to find bugs
and fix them inline using the Autonomous Defect Resolution Protocol. UX Sense Check
validates the user experience (frontend slices only).

## F.1: QA Swarm (7 agents, parallel via OpenAI 5.5)

> **QMD QUERY** (non-blocking): Spawn `/relay-qmd` — query `"QA failures root causes regressions {SLICE_TOPIC}"` in `{PROJECT_NAME}`. Share prior failure patterns with QA agents before they begin. If QMD unavailable, proceed.

All QA agents call OpenAI 5.5 via the script:
```
python scripts/openai_code.py qa --code <path> --check <type> --slice <N>
```

1. QA Lead coordinates 7 QA checks running in parallel:
   - `--check api-contract` — HTTP contract, request/response shape, status codes
   - `--check backend` — server logic, service layer, error handling
   - `--check routing` — Next.js App Router or equivalent routing correctness
   - `--check data-integrity` — data flow, persistence, transformation accuracy
   - `--check code-quality` — structure, maintainability, type safety, 150-line
   - `--check security` — auth, input sanitization, secrets, dependency vulns
   - `--check uiux` — rendering, responsiveness, accessibility

2. Each agent applies the **Autonomous Defect Resolution Protocol** (Article 17e):
   - Find bug → spawn fix sub-agent → AUDIT → RED → GREEN → REGRESSION → CLASS SCAN → COMMIT.

3. Use `review-templates/QA-SWARM-TEMPLATE.md` for the output format.

## F.2: UX Sense Check (frontend slices only)

4. 3 personas navigate the UI via agent-browser.
5. Each persona evaluates: first impression, label clarity, action clarity, result
   comprehension, error recovery, flow completeness, jargon.
6. Use `review-templates/UX-SENSE-CHECK-TEMPLATE.md` for the output format.

## F.3: Synthesis

7. QA Manager synthesizes ALL findings + autonomous fix results.

> **QMD SAVE** (non-blocking): Spawn `/relay-qmd` — save novel QA findings and root causes to `vault/projects/{PROJECT_NAME}/qa-findings-slice-{N}.md`. If QMD unavailable, skip.

## Artifacts

- `reviews/slice-N-qa-swarm.md`
- `reviews/slice-N-ux-sense-check.md` (if frontend)
- Consolidated in `reviews/slice-{N}.md` (section: QA + Runtime)
- Per-check detail: `reviews/slice-{N}/qa-{check-type}.md`

## Next Phase

Proceed to **Phase F.5: Automated Sentry Check** (`phase-f5-runtime-log-check.md`).
