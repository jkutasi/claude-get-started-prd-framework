# Phase E: Peer Review (4 Models, Adversarial, Parallel)

> Load this file when starting Phase E. Complete all steps and the gate before proceeding to Phase F.
> Canonical procedure: see Article 03.

## Purpose

Four external models review the implementation code in parallel. Consensus findings (2+ reviewers agree) are mandatory fixes. Round 2 is mandatory after fixes.

**NOTE:** Peer review applies to ALL code changes including refactoring. Refactoring is not exempt. Moving code between files can introduce security regressions.

## Reviewers (smartest-of-each-provider)

| Reviewer | Focus Area | How to Call |
|----------|-----------|-------------|
| **Gemini** (smartest available) | Architecture, correctness, design patterns | via MCP or API |
| **OpenAI 5.5** (reflection mode) | Invariants, silent failures, security, 150-line | Responses API: `POST /v1/responses` body `{"model":"gpt-5.5","input":"..."}` — response field `output_text` |
| **Claude Opus 4.7** | Independent review (separate context) | Spawn sub-agent |
| **Grok** (smartest available) | Security, attack surfaces, edge cases, input validation | via API |

## Steps

> **QMD QUERY** (non-blocking): Spawn `/relay-qmd` — query `"peer review findings patterns {SLICE_TOPIC}"` in `{PROJECT_NAME}`. Share relevant prior findings with reviewers as context. If QMD unavailable, proceed.

1. CTO prepares the review package: all new/modified files from Phases C-D.
2. Invoke the [peer-review-orchestrator skill](../../peer-review-orchestrator/SKILL.md) to dispatch
   all four reviewers and produce the consolidated `reviews/slice-{N}-peer-review.md` artifact in
   one operation. Opus 4.7 review = CTO own review pass. No separate `reviewer-opus` skill exists.
3. Each reviewer receives the code and the Error & Rescue Registry from Phase D.
4. Each reviewer returns findings using `review-templates/PEER-REVIEW-TEMPLATE.md`.
5. **ALL 4 reviewers must return findings before proceeding.** No partial reviews.

## CTO Synthesis

6. CTO synthesizes findings:
   - **Consensus issues** (2+ reviewers) = **mandatory fixes**.
   - **Non-consensus issues** (1 reviewer) = CTO decides: FIX / DEFER / DISMISS.
7. CTO checks Article 20 architecture compliance in the synthesis.
8. Mandatory fixes are assigned to coder teammates (not CTO).
9. **Round 2 (mandatory after fixes):** Re-run all 4 reviewers on patched code. Confirm no new consensus issues before proceeding.

## Artifact

- `reviews/slice-N-peer-review.md`

## Gate

```
+------------------------------------------------------------------+
| NUCLEAR GATE E: CTO must confirm:                                |
| [] "ALL 4 reviewers returned findings before proceeding"         |
| [] "Consensus issues (2+ reviewers) identified as mandatory"     |
| [] "Mandatory fixes assigned to coder teammates (not CTO)"       |
| [] "Round 2 completed after fixes — no new consensus issues"     |
| [] "reviews/slice-N-peer-review.md EXISTS on disk"               |
+------------------------------------------------------------------+
```

## Next Phase

Proceed to **Phase F: QA Swarm** (`phase-f-qa-swarm.md`).
