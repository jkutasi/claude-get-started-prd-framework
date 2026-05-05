---
name: peer-review-orchestrator
description: "Use during Phase E to run the 4-model adversarial peer review (Gemini + OpenAI 5.5 + Grok in parallel + Opus/CTO own review) and write results into Section 3 of the consolidated reviews/slice-{N}.md artifact."
allowed-tools: Read, Grep, Glob, Bash, Agent
---

# Peer Review Orchestrator

## §1 Role Identity

This skill orchestrates the Phase E peer review. It does not perform the review itself; it
dispatches the three external reviewer skills in parallel and instructs the CTO to do its own
review pass, then merges all four reports into one consolidated artifact. The CTO is the Opus 4.7
reviewer — no separate `reviewer-opus` skill exists or is needed.

## §2 Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `SLICE_N` | Yes | Slice number (e.g. `3`) |
| `diff_or_files` | Yes | The diff or list of changed files to review |
| `spec` | Yes | The slice's Gherkin / acceptance criteria for reviewer context |
| `round` | No | `1` (default) or `2` (post-fix re-review) |

## §3 Procedure

### Step 1 — Read the slice diff and spec

Load the diff (or file list) and the slice spec into context. Confirm both are present before
proceeding. If either is missing, stop and request them from the caller.

### Step 2 — Spawn three external reviewer sub-agents IN PARALLEL

In a **single Agent tool call block** (multiple agent invocations at once), spawn:

- `reviewer-gemini` — Architecture, design patterns, scalability
- `reviewer-openai` — Invariants, silent failures, security, 150-line compliance
- `reviewer-grok` — Security, edge cases, adversarial inputs

Each sub-agent receives:
- The diff / changed files
- The slice spec and acceptance criteria
- The Standard Review Prompt Template (§5 below)

Do NOT spawn them sequentially. All three must launch simultaneously.

### Step 3 — CTO does its own review pass

While the external sub-agents run, the CTO (Opus 4.7) reviews the same diff using the Standard
Review Prompt Template. This is the fourth reviewer in the 4-model lineup. No API call needed —
the CTO reads the diff and produces its findings directly.

### Step 4 — Collect all four reports and cross-check

Wait for all three external sub-agents to return. Then cross-check across all four reports:

- **Consensus issues**: 2+ reviewers flag the same finding — mark `[MANDATORY]`.
- **Single-reviewer findings**: mark `[ADVISORY]` unless data-correctness or security
  (those are always mandatory regardless of consensus count).
- **Security issues**: always escalate immediately, never advisory.

If any reviewer's API call fails, do NOT silently proceed — see §7 Failure Handling.

### Step 5 — Merge into consolidated artifact

Write results into **Section 3 (Code Peer Review)** of `reviews/slice-{N}.md` (round 1) with:

1. **Summary** — verdict, round number, date, reviewers who ran
2. **Consensus Issues** (`[MANDATORY]`) — 2+ reviewer agreement; must fix before ship
3. **Single-Reviewer Findings** (`[ADVISORY]`) — 1 reviewer; team decides (exceptions above)
4. **Per-Reviewer Reports** — Gemini, OpenAI 5.5, Grok sub-sections; CTO/Opus 4.7 review written inline (no separate detail file)

Per-reviewer detail files go to `reviews/slice-{N}/peer-review-{gemini,openai,grok}.md` (linked from Section 3).
The CTO's own Opus 4.7 review pass is written directly into Section 3 — no separate detail file.

### Step 6 — Return verdict

One of:
- `APPROVE` — no issues found by any reviewer
- `APPROVE_WITH_NITS` — advisory issues only, no mandatory fixes
- `REQUEST_CHANGES` — one or more mandatory issues; do not ship until resolved

## §4 Round 2 Protocol

After mandatory fixes from round 1 are applied, run again with `round=2`. Round 2 always runs
after fixes — it is never optional. Round 2 updates **Section 3 of the same `reviews/slice-{N}.md`
in-place** with a "Round-2 verdict" sub-section appended below the original findings. A separate
pass-2 file is NOT created. Round 2 must return `APPROVE` or `APPROVE_WITH_NITS` before the slice
proceeds to Phase F.

## §5 Standard Review Prompt Template

Pass this block verbatim to each reviewer (fill in `{SLICE_N}`, `{diff}`, `{spec}`):

```
You are reviewing Slice {SLICE_N}. Code diff / changed files below. Slice spec below.
Evaluate on these dimensions — address ALL of them, even if no issue found:
1. Correctness and invariant violations
2. Silent failure modes (swallowed errors, missing null checks)
3. Security: injection, auth/authz gaps, secrets exposure, OWASP Top 10
4. 150-line file compliance (Article 20c)
5. Architecture alignment with the slice spec
6. Edge cases and adversarial inputs
7. Test coverage adequacy
8. Related code paths that may be affected but are not in the diff

For each finding: Severity (P0–P3), File:Line, Issue, Recommendation.
State explicitly what was checked for each dimension, even if it passed.
End your response with a single line: VERDICT: APPROVE | APPROVE_WITH_NITS | REQUEST_CHANGES
```

## §6 See Also

- Article 03 (`contract-templates/articles/article-03-peer-review.md`) — consensus rules, verdict format
- Article 18 — security escalation policy
- `phase-e-peer-review.md` — Phase E gate checklist

## §7 Failure Handling

If any external reviewer's API call fails or the sub-agent returns an error:

1. Do NOT silently continue with a 3-of-4 review.
2. Report the failure clearly: which reviewer failed, the error message.
3. Halt and ask the user explicitly: "Reviewer {X} failed. Proceed with 3-of-4, or retry?"
4. Only continue if the user explicitly acknowledges and approves the degraded run.
