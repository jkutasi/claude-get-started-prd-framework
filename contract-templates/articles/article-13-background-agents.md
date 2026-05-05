# Article 13: Background Agent Management & Notification Handling

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

#### 13a. Foreground vs Background Agent Selection

- **Foreground (default):** Use for agents whose results are needed before proceeding. This includes all coder agents, researcher agents, and any agent whose output feeds the next step.
- **Background (`run_in_background: true`):** Use ONLY when the CTO can meaningfully continue other work while waiting. Examples: parallel peer reviewers (all 3 launched together), parallel QA swarm agents.
- **Rule:** If you launch background agents, you MUST collect ALL their results before declaring that phase complete. Do not move to the next phase while background agents are still running.

#### 13b. Draining Background Agents Before Phase Transition

Before transitioning between workflow phases (e.g., Phase C to Phase E):
1. List all background agents spawned in the current phase
2. Collect results from each (or confirm already collected)
3. Only AFTER all agents are drained may the CTO declare the phase complete

#### 13c. Handling Stale Task Notifications

When a notification arrives for an agent whose results have ALREADY been synthesized:
1. Do NOT respond to the user. The notification is an internal system event.
2. Do NOT acknowledge it individually. Silently note it and continue.
3. If multiple stale notifications arrive, acknowledge them ONCE in a single brief sentence, then stop.

#### 13d. Notification Batching Rule

When the CTO receives multiple notifications in sequence with no user message between them:
- Respond AT MOST ONCE with a brief batch summary
- Never produce more than one response per batch of system notifications
- If the notifications are for already-completed work, a single "These are from the previous phase — already handled." suffices
