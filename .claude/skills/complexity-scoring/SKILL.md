---
name: complexity-scoring
description: "Use when about to start implementing any task. Score complexity before writing a single line of code."
---

# Complexity Scoring

Score every task BEFORE implementation begins. This gate prevents under-scoped
work from turning into architectural surprises mid-slice.

## Protocol

### Step 1 — Score the task

Read the full task description, acceptance criteria, and any linked specs.
Apply the rubric in `scoring-rubric.md`. Output exactly:

```
Complexity score: N/10
Rationale: [2-3 sentences explaining the score]
```

### Step 2 — Gate check

| Score | Action |
|-------|--------|
| 1–6   | Proceed with implementation. |
| 7–8   | STOP. Break into subtasks first. Score each subtask individually. Resume only when all subtasks are 6 or below. |
| 9–10  | STOP. Write a design spec first. Invoke the `design-first-gate` skill before any other work. |

### Step 3 — Record the score

Add or update `complexityScore` in `.taskmaster/tasks.json` for the relevant
task before writing any code:

```json
{
  "id": "task-id",
  "title": "task title",
  "complexityScore": 5,
  "complexityRationale": "Brief rationale here"
}
```

## Rules

- Score BEFORE touching any file.
- Do not round down to avoid a gate. If it feels like a 7, score it 7.
- A subtask must be independently deliverable and testable to count as a split.
- Re-score after a significant scope change — do not carry forward a stale score.

See `scoring-rubric.md` for the full rubric with examples.
