# Phase E: Peer Review (3+ Models, Parallel)

> Load this file when starting Phase E. Complete all steps and the gate before proceeding to Phase F.

## Purpose

Three external models review the implementation code in parallel. Consensus findings (2+ reviewers agree) are mandatory fixes.

**NOTE:** Peer review applies to ALL code changes including refactoring. Refactoring is not exempt. Moving code between files can introduce security regressions.

## Reviewers

| Reviewer | Focus Area |
|----------|-----------|
| **Gemini** | Architecture, correctness, design patterns |
| **OpenAI Codex** | Edge cases, error handling, code quality |
| **Grok** | Security, attack surfaces, input validation |
| **Greptile** (optional) | Cross-file consistency, dependency impact |

## Steps

1. CTO prepares the review package: all new/modified files from Phases C-D.
2. Spawn 3 reviewer sub-agents in parallel (+ Greptile if configured).
3. Each reviewer receives the code and the Error & Rescue Registry from Phase D.
4. Each reviewer returns findings using `review-templates/PEER-REVIEW-TEMPLATE.md`.
5. **ALL reviewers must return findings before proceeding.** No partial reviews.

## CTO Synthesis

6. CTO synthesizes findings:
   - **Consensus issues** (2+ reviewers) = **mandatory fixes**.
   - **Non-consensus issues** (1 reviewer) = CTO decides: FIX / DEFER / DISMISS.
7. CTO checks Article 20 architecture compliance in the synthesis.
8. Mandatory fixes are assigned to coder teammates (not CTO).

## Artifact

- `reviews/slice-N-peer-review.md`

## Gate

```
+------------------------------------------------------------------+
| NUCLEAR GATE E: CTO must confirm:                                |
| [] "ALL reviewers returned findings before proceeding"           |
| [] "Consensus issues (2+ reviewers) identified as mandatory"     |
| [] "reviews/slice-N-peer-review.md EXISTS on disk"               |
| [] "All mandatory fixes assigned to teammates"                   |
+------------------------------------------------------------------+
```

## Next Phase

Proceed to **Phase F: QA Swarm** (`phase-f-qa-swarm.md`).
