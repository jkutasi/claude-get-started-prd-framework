# Slice {N} — {Slice Name} — Consolidated Review

> Generated through the slice workflow. One file per slice. Detail reports under `reviews/slice-{N}/`.

---

## 1. Pre-Build Plan Review (Phase A.7)

Status: SKIPPED (default — slice not flagged --high-risk) | RAN

If RAN, summary: ...

Detail: `reviews/slice-{N}/red-team-pre-build.md`

---

## 2. Tests (Phase B)

- Test files written: <list>
- Test peer-review verdict: APPROVE | REQUEST_CHANGES
- Coverage: P0 >= 100%, P1 >= 90%

Detail: `reviews/slice-{N}/tests.md`

---

## 3. Code Peer Review (Phase E — 4-model adversarial)

| Reviewer | Verdict | Key findings |
|---|---|---|
| Gemini | APPROVE / NITS / REQUEST_CHANGES | ... |
| OpenAI 5.5 | APPROVE / NITS / REQUEST_CHANGES | ... |
| Grok | APPROVE / NITS / REQUEST_CHANGES | ... |
| Claude Opus 4.7 (CTO) | APPROVE / NITS / REQUEST_CHANGES | ... |

Note: The CTO's findings are recorded here directly — no separate file.

Consensus issues: <list or "None">

Round-1 verdict: APPROVE | REQUEST_CHANGES

Round-2 verdict (if needed): APPROVE | REQUEST_CHANGES

Detail: `reviews/slice-{N}/peer-review-gemini.md`, `peer-review-openai.md`, `peer-review-grok.md`

---

## 4. QA + Runtime (Phase F + F.5)

| QA check (OpenAI 5.5) | Verdict |
|---|---|
| api-contract | PASS / FAIL |
| backend | PASS / FAIL |
| routing | PASS / FAIL |
| data-integrity | PASS / FAIL |
| code-quality | PASS / FAIL |
| security | PASS / FAIL |
| uiux (frontend only) | PASS / FAIL / N/A |

UX Sense Check (frontend, optional): PASS / FAIL / N/A

F.5 Sentry scan (automated via relay-sentry): 0 new issues / N issues

Detail: `reviews/slice-{N}/qa-api-contract.md`, `qa-backend.md`, `qa-routing.md`,
`qa-data-integrity.md`, `qa-code-quality.md`, `qa-security.md`, `qa-uiux.md`

---

## 5. Gate Check + Smoke (Phase J)

- gate_check.py: PASS | FAIL
- Playwright smoke on live deploy URL:
  - Golden path for slice {N}: PASS | FAIL
  - Regression assertions on slices 1..{N-1}: PASS | FAIL
- Deploy SHA verified (Article 39): YES | NO
- Final verdict: SHIPPED | BLOCKED

Detail: `reviews/slice-{N}/smoke.md`

---

## 6. Post-Push (after merge + deploy)

- Sentry alert on release {SHA}: 0 new issues / N issues
- Deployment log scan: clean / errors

Detail: `reviews/slice-{N}/post-push.md`
