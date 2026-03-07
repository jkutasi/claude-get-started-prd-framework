# Article 24: Sub-Agent Separation of Concerns

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.
>
> **Enforces:** Nuclear Rule 5 (One Concern Per Sub-Agent — Then It Dies)

When multiple things need fixing, don't pile them into one sub-agent. Split by concern.

## Example — Lint + Type Check Session

- Sub-agent 1: Run `lint type check` — find and report all errors
- Sub-agent 2: Fix all lint errors properly (no ignores)
- Once both complete — dismiss both sub-agents

## Example — Feature with Multiple Concerns

- Sub-agent 1: Database migration
- Sub-agent 2: API endpoint logic
- Sub-agent 3: Input validation
- Each completes its concern independently — dismiss all when done

See Nuclear Rule 5 — each sub-agent has a single job. It does that job and dies.

## Why This Matters

This is Nuclear Rule 5 applied in practice. When a sub-agent works on multiple things, it carries stale context from the first job into the second. That stale context causes hallucinated file states, phantom bugs, and compounding errors that are nearly impossible to trace. The examples above — two sub-agents for lint check vs. lint fix, three agents for three parts of a feature — make the abstract rule concrete and actionable.
