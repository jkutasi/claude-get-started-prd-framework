# Troubleshooting Workflow

> Part of the [Getting Started](INDEX.md) roadmap. Load before any non-trivial fix attempt, and always after one — success or failure.

## Purpose

Stop reattempting failed fixes. Build institutional incident memory across the project. Every bug fix attempt — and especially every **failed** attempt — is the highest-value training data the project produces. If it is not captured, the next agent (or future-you) will rediscover the dead end at full cost.

This workflow defines a **closed loop**: consult memory before you guess, write to memory after you act. Two skills carry the loop:

- `troubleshooting-recall` — searches the memory cascade for prior attempts at the current symptom.
- `troubleshooting-log` — records the symptom, hypothesis, attempt, outcome, and root cause.

A fix attempt without these two bookends is a leak. Leaks compound.

## The Closed Loop

```
   ┌──────────────────────────────────────┐
   │  Symptom observed                     │
   └──────────────────┬───────────────────┘
                      │
                      ▼
   ┌──────────────────────────────────────┐
   │  BEFORE: invoke troubleshooting-recall│
   │  (per trigger threshold below)        │
   └──────────────────┬───────────────────┘
                      │
                      ▼
   ┌──────────────────────────────────────┐
   │  Form hypothesis → attempt fix        │
   └──────────────────┬───────────────────┘
                      │
                      ▼
   ┌──────────────────────────────────────┐
   │  AFTER: invoke troubleshooting-log    │
   │  MANDATORY — success OR failure       │
   └──────────────────────────────────────┘
```

Failures are mandatory to log. They are the entries with the highest future value because they encode dead ends a fresh agent cannot see from the code alone.

## Trigger Threshold for `troubleshooting-recall`

| Situation | Recall required? |
|-----------|------------------|
| Second attempt at the same problem (any stakes) | **Yes** |
| First attempt on a high-stakes problem (production, deployment, data integrity, auth, billing) | **Yes** |
| First attempt on a low-stakes/local issue (dev-only, cosmetic, isolated unit) | Optional |

If unsure, call recall. The cost of one extra search is trivial; the cost of repeating a failed fix is hours.

## Memory Cascade for Recall

`troubleshooting-recall` searches in this order and **stops at the first hit**. Do not skip tiers.

| Tier | Source | Scope | Shape | Read by |
|------|--------|-------|-------|---------|
| 0 | In-conversation context | Current session | Free text | Agent |
| 1 | `~/.claude/memory/MEMORY.md` | User-scoped, all projects | Linear file | Agent |
| 2 | `mcp__memory__*` | In-session knowledge graph (if configured) | Entities + relations | Agent |
| 3 | Obsidian vault | Project-scoped, vectorized | Narrative notes | Humans (and agent via MCP) |
If a tier is not configured for the project, skip it and continue down the cascade. If the cascade finds a prior attempt at the same symptom, surface it to the calling agent **before** any new hypothesis is formed.

## What `troubleshooting-log` Records

Every entry — success or failure — captures the same six fields. Missing fields make the entry near-useless to future search.

1. **Symptom** — what was broken (error message, observed behavior, failing test name).
2. **Hypothesis** — why we thought it broke (the model that drove the attempt).
3. **Fix attempted** — files touched, summary of the change, commit/PR reference if available.
4. **Outcome** — `worked` / `didn't work` / `partial`. Be honest. "Partial" is a real and useful outcome.
5. **Root cause** — if known. Mark `unknown` if not. Do not guess; an unknown root cause that is later resolved upgrades the entry.
6. **Date / project / slice context** — date, project name, current slice or feature being worked on.

## Where Logs Go

| Destination | Status | Form | Why |
|-------------|--------|------|-----|
| Obsidian vault (project notes) | **Mandatory** | Narrative markdown | Humans read these; the vault is the durable record |

## Failure Mode This Workflow Prevents

The classic agent failure: agent attempts fix A, it fails, agent attempts fix B, it fails, agent attempts fix A again under a slightly different framing because the failure of A was never written down. The closed loop forecloses this. If recall is run before every retry, and log is written after every attempt, A-failed-already is always visible before A is retried.

## Verification Checklist

The calling agent confirms a troubleshooting cycle is complete when:

- [ ] `troubleshooting-recall` was invoked before the fix attempt (when threshold required it)
- [ ] Recall results were surfaced and considered before forming the hypothesis
- [ ] `troubleshooting-log` was invoked after the attempt, regardless of outcome
- [ ] The log entry contains all six fields (symptom, hypothesis, fix, outcome, root cause, context)
- [ ] The Obsidian entry exists and is readable

A cycle missing any checkbox is incomplete. Do not move to the next bug.

## Related

- [memory-layers.md](memory-layers.md) — full guide to all 4 tiers, decision trees, and when each tier wins
- [skill-quality-contract.md](skill-quality-contract.md) — the bar the two skills themselves must meet
