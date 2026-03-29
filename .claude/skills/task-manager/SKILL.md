---
name: task-manager
description: "Use when starting a new work session, creating tasks, tracking progress, or checking what needs to be done next."
disable-model-invocation: true
---

# Task Manager Skill

Manages `.taskmaster/tasks.json` — a durable task store that persists across sessions. Full protocol details are in `task-manager-protocol.md` in this directory.

## Session Start (ALWAYS do this first)

1. Read `.taskmaster/tasks.json`.
2. Print a table of every task with `status: "pending"` or `status: "in-progress"`.
3. Highlight any blocked tasks and their blocking dependency IDs.
4. If the file is empty, say so and offer to create the first task.

## Creating a Task

Required fields — refuse to save without ALL of them:

- `title` — short imperative phrase
- `description` — what and why
- `status` — start as `"pending"`
- `priority` — `"high"`, `"medium"`, or `"low"`
- `dependencies` — array of IDs (empty `[]` if none)
- `testStrategy` — **MANDATORY. No task without this.** Must be a Gherkin scenario (Given/When/Then). Minimum: one Given, one When, one Then. This scenario IS the acceptance test — if it passes, the task is done.
- `complexityScore` — set after scoring (see below); `null` until scored
- `subtasks` — `[]` until broken down
- `createdAt` / `updatedAt` — ISO 8601

Assign the next sequential integer ID. Read the file, find `max(id)`, add 1.

## Complexity Scoring

Score BEFORE writing any code. Scale 1–10:

| Score | Meaning |
|-------|---------|
| 1–3 | Trivial — single file, obvious implementation |
| 4–6 | Moderate — multiple files, some design choices |
| 7–10 | Complex — cross-cutting, architecture decisions needed |

Write one sentence rationale alongside the score, e.g.:
`"complexityScore": 7, // touches auth, session store, and rate limiter`

If score is 7+, STOP. Populate `subtasks` first, then begin. See `task-manager-protocol.md` for subtask rules.

## Updating Status

Valid transitions:

```
pending → in-progress → review → done
in-progress → blocked
blocked → in-progress
any → cancelled
```

Before moving to `in-progress`: verify every ID in `dependencies[]` has `status: "done"`.
If a dependency is not done, set status to `"blocked"` and record the blocking ID in the task description.

Always update `updatedAt` when changing any field.

## Enumeration Protocol

Before starting work on any phase, enumerate ALL task and subtask IDs:

1. **Pre-flight:** List every ID — e.g., "Executing: 3, 3.1, 3.2, 4"
2. **Per-task:** After each, state "Task {ID} complete → proceeding to {next ID}"
3. **Gap detection:** If next ID is not sequential, explain why (e.g., "Skipping 3.3 — cancelled")
4. **Completion:** "All tasks complete: 3 ✓, 3.1 ✓, 3.2 ✓, 4 ✓"

## Anti-Patterns

- Do not create a task without `testStrategy` — return an error message to the user instead.
- Do not accept prose `testStrategy` — reject it and ask for Gherkin format.
- Do not start implementation before scoring complexity.
- Do not skip dependency checks — starting a task with unmet deps causes silent failures.
- Do not nest subtasks more than one level deep.
- Do not delete tasks — use `"cancelled"` instead (preserves history).

### testStrategy: BAD vs GOOD

BAD (prose — REJECT):
```
"Make sure the validation works correctly"
```

GOOD (Gherkin — ACCEPT):
```
"Given a checkout form is displayed
When the user submits with card number '0000000000000000'
Then the form shows 'Invalid card number'
And the API is not called"
```
