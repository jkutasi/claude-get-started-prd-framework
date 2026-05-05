# Article 8: Model Right-Sizing

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

## Headline Rule: Smartest Available Per Provider

Always use the **smartest available model from each provider** for the assigned role. Do not
lock to version numbers as permanent choices — when a provider releases a smarter model, update
the model ID in the relevant script. The role assignment is permanent; the version is not.

## Role Assignments

| Role | Model | Rationale |
|------|-------|-----------|
| **CTO Orchestrator / Planner** | Claude Opus 4.7 (smartest Claude) | Maximum context capacity for orchestration, synthesis, and cross-slice decisions |
| **Coder Sub-Agent** | Sonnet shell → OpenAI 5.5 (smartest OpenAI) | Sonnet couriers the prompt; OpenAI writes the code. See Article 02. |
| **Peer Reviewer #1** | Gemini (smartest available) | Architecture and scalability lens |
| **Peer Reviewer #2** | OpenAI 5.5 reflection | Same model that wrote the code reviewing its own output |
| **Peer Reviewer #3** | Claude Opus 4.7 | Independent full-spectrum review |
| **Peer Reviewer #4** | Grok (smartest available) | Security and edge-case lens |

## Sonnet as Courier Shell

Sonnet sub-agents are cheaper than Opus and fast. Their role is NOT to write code — their role
is to:

1. Receive a focused task spec from Opus (the CTO).
2. Call OpenAI 5.5 via the Responses API (`POST https://api.openai.com/v1/responses`).
3. Run OpenAI self-review on the draft.
4. Write the verified code to disk.
5. Run verification (line count, lint, tests).
6. Retry up to 3 times on failure, then escalate to Opus.

Sonnet's generation capacity is not spent on code — it manages the API loop and verification.
This keeps Opus free for planning and keeps code quality anchored to the strongest coding model.

## Upgrading Models

When OpenAI releases a smarter coding model:
- Update the `model` field in `scripts/openai_code.py` (or wherever the Responses API call lives).
- The article's rule is "smartest available OpenAI coder" — the script is the only thing to change.

When Anthropic releases a smarter Claude:
- Update the CTO agent definition in `.claude/agents/cto.md`.
- The rule is "smartest available Claude" — the agent file is the only thing to change.

Same principle applies to Gemini and Grok.

## Hard Constraints

- Opus is reserved EXCLUSIVELY for the CTO Orchestrator. No teammate or sub-agent uses Opus
  except when Opus must intervene after a 3-failure escalation from a Sonnet coder agent.
- Sub-agents that implement code (Phase C) use the Sonnet-shell pattern. No exceptions.
- Sub-agents that write tests (Phase B) also use the Sonnet-shell pattern.
- Peer review (Phase E) uses all 4 adversarial reviewers. No model substitutions on failure —
  report the error instead.
