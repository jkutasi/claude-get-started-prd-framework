# Task Manager — Extended Protocol

Supporting detail for `SKILL.md`. Load this file when you need subtask rules, the full status FSM, or file-write procedures.

## File Write Procedure

`.taskmaster/tasks.json` is the single source of truth.

1. Read the current file into memory.
2. Make the change (add task, update field, add subtask).
3. Write the full JSON back — never partial writes.
4. Pretty-print with 2-space indent.

Example structure after two tasks are created:

```json
{
  "version": "1.0",
  "tag": "master",
  "tasks": [
    {
      "id": 1,
      "title": "Bootstrap Sentry error tracking",
      "description": "Install and configure Sentry SDK. Must receive at least one test error before Slice 1 begins.",
      "status": "done",
      "priority": "high",
      "dependencies": [],
      "testStrategy": "Given Sentry is installed and the SDK is initialised\nWhen a deliberate exception is thrown at app startup\nThen the error appears in the Sentry dashboard within 60 seconds\nAnd the event includes the correct environment tag",
      "complexityScore": 3,
      "subtasks": [],
      "createdAt": "2026-03-24T09:00:00Z",
      "updatedAt": "2026-03-24T11:30:00Z"
    },
    {
      "id": 2,
      "title": "Implement user authentication",
      "description": "JWT-based login and refresh flow with rate limiting.",
      "status": "in-progress",
      "priority": "high",
      "dependencies": [1],
      "testStrategy": "Given the /auth/login endpoint exists\nWhen called with valid credentials\nThen a signed JWT is returned with status 200\nAnd when called with invalid credentials the response is 401\nAnd when called 11 times rapidly the 11th response is 429",
      "complexityScore": 8,
      "subtasks": [
        {
          "id": "2.1",
          "title": "Create /auth/login endpoint",
          "status": "done",
          "testStrategy": "Given a POST to /auth/login with valid credentials\nWhen the handler runs\nThen a signed JWT is returned with status 200",
          "createdAt": "2026-03-24T11:31:00Z",
          "updatedAt": "2026-03-24T13:00:00Z"
        },
        {
          "id": "2.2",
          "title": "Create /auth/refresh endpoint",
          "status": "in-progress",
          "testStrategy": "Given a valid refresh token is sent to /auth/refresh\nWhen the handler runs\nThen a new access token is returned with status 200\nAnd when an expired token is sent the response is 401",
          "createdAt": "2026-03-24T11:31:00Z",
          "updatedAt": "2026-03-24T13:00:00Z"
        }
      ],
      "createdAt": "2026-03-24T11:31:00Z",
      "updatedAt": "2026-03-24T13:00:00Z"
    }
  ]
}
```

## Gherkin Validation Rule

Before saving any task or subtask, verify `testStrategy`:

1. Contains at least one `Given`, one `When`, one `Then`
2. Multi-step scenarios (3+ Given/When/Then/And lines) must include `# Step N/M` comments

**BAD** (rejected — multi-step without numbers):
```
Given a checkout form is displayed
When the user submits with card '0000'
Then the form shows 'Invalid card number'
And the API is not called
```

**GOOD** (accepted):
```
Given a checkout form is displayed            # Step 1/4
When the user submits with card '0000'        # Step 2/4
Then the form shows 'Invalid card number'     # Step 3/4
And the API is not called                     # Step 4/4
```

Single-step scenarios (1 Given + 1 When + 1 Then) do not require step numbers.

## Subtask Rules

Trigger subtask breakdown when `complexityScore >= 7`.

- Subtask IDs use dot notation: `"2.1"`, `"2.2"`, etc.
- Each subtask requires `title`, `status`, `testStrategy` (Gherkin format), `createdAt`, `updatedAt`.
- No nesting beyond one level (no `2.1.1`).
- Parent task status follows subtasks: all subtasks `done` → parent moves to `review`.
- Subtasks do not need their own `dependencies` field (they inherit the parent's).

## Priority Assignment Guide

| Priority | Use when |
|----------|---------|
| high | Blocking other tasks OR on the critical path for the current slice |
| medium | Needed this slice but not immediately blocking |
| low | Nice-to-have, can defer to a future slice |

## Blocked Task Handling

When a dependency is unfinished:

1. Set task `status` to `"blocked"`.
2. Append to `description`: `" [BLOCKED: waiting on task #N]"`.
3. Update `updatedAt`.
4. Surface it in the session-start table with a BLOCKED label.

When the blocker resolves:

1. Set `status` back to `"pending"` (not directly to `"in-progress"` — let the next session start the work consciously).
2. Remove the BLOCKED note from `description`.
3. Update `updatedAt`.

## Integration with Slice Workflow

- **Phase A (Preparation):** Load tasks.json, surface pending/in-progress. Create new tasks for this slice with full `testStrategy` before any code is written. Enumerate all task IDs before starting (see Enumeration Protocol in SKILL.md).
- **Phase C (Implementation):** Move task to `in-progress`, score complexity, break into subtasks if score >= 7.
- **Phase D (Self-Reflection):** Move task to `review`. Verify `testStrategy` was satisfied.
- **Phase F (QA Swarm):** QA confirms `testStrategy` criteria pass. If yes, move to `done`.
- **Phase J (Gate Check):** All tasks for this slice must be `done` or `cancelled` before gate passes.

## config.json Usage

The `config.json` file maps logical roles to models. When spawning sub-agents, reference this file:

- `models.main` — coder agents (Phase C implementation)
- `models.research` — architecture decisions, ADR drafting
- `models.fallback` — mechanical tasks (file renames, boilerplate generation)
