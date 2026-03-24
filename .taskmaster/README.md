# .taskmaster — Durable Task Store

Persists task tracking across Claude sessions. `TodoWrite` dies when the conversation ends; this directory survives in git.

## Files

| File | Purpose | Tracked in git? |
|------|---------|-----------------|
| `tasks.json` | Live task database for this project | Yes (start empty, accumulates over time) |
| `config.json` | Model role assignments | Yes (template default) |
| `README.md` | This file | Yes |

## Task Schema

Each entry in `tasks[].tasks` must have every field below:

```json
{
  "id": 1,
  "title": "Add payment card validation",
  "description": "Validate card number, expiry, and CVV before submission",
  "status": "pending",
  "priority": "high",
  "dependencies": [],
  "testStrategy": "Given a payment form exists\nWhen submitted with an expired card\nThen the API returns { valid: false, reason: 'card_expired' }\nAnd no charge is attempted",
  "complexityScore": null,
  "subtasks": [],
  "createdAt": "2026-03-24T00:00:00Z",
  "updatedAt": "2026-03-24T00:00:00Z"
}
```

`testStrategy` MUST be a Gherkin scenario using Given/When/Then. Prose is rejected. Minimum: one Given, one When, one Then. This scenario IS the acceptance test — task is done when it passes.

## Status Flow

```
pending → in-progress → review → done
              ↓
           blocked → in-progress
              ↓
          cancelled
```

## Complexity Scale

| Score | Label | Action Required |
|-------|-------|-----------------|
| 1–3 | Trivial | Implement directly |
| 4–6 | Moderate | Implement; note any surprises |
| 7–10 | Complex | MUST break into subtasks before coding |

## Subtask Shape

Subtasks live in `task.subtasks[]` and share the parent schema minus `subtasks` (no nesting beyond one level).

## Usage Rules (enforced by task-manager skill)

1. A task with no `testStrategy` must be rejected — add one before saving. The value must be a Gherkin scenario (Given/When/Then); prose descriptions are rejected.
2. Score complexity before touching any code.
3. Check that all IDs in `dependencies[]` have `status: "done"` before moving a task to `in-progress`.
4. If `complexityScore >= 7`, populate `subtasks` first, then begin.
5. At session start, read this file and surface every `pending` and `in-progress` task.

## config.json

Controls which Claude model handles each role. Edit to swap providers or models without touching skill files.
