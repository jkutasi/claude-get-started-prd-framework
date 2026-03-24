---
name: run-artifacts
description: "Use when starting a new work session or when a significant action is taken. Records what Claude does for audit and debugging purposes."
---

# Run Artifacts

Record every work session in a structured log so sessions are auditable and
debuggable after the fact.

## When to Use

- At the START of any work session (task, slice, or multi-step operation)
- After any significant action during the session
- At the END of the session before returning the completion report

## Session Start Protocol

1. Determine the current timestamp in `YYYY-MM-DD-HH-MM` format.
2. Create the run directory: `.artifacts/runs/{YYYY-MM-DD-HH-MM}/`
3. Write `manifest.json` with the schema below — `endTime` and
   `tasksCompleted`, `filesChanged`, `blockers` start empty.
4. Write the first `log.jsonl` entry with `action: "session_start"`.

### manifest.json Schema

```json
{
  "sessionId": "YYYY-MM-DD-HH-MM",
  "goal": "one-sentence description of what this session will accomplish",
  "startTime": "ISO 8601 timestamp",
  "endTime": null,
  "model": "model identifier (e.g. claude-sonnet-4-6)",
  "tasksPlanned": ["task description 1", "task description 2"],
  "tasksCompleted": [],
  "filesChanged": [],
  "blockers": []
}
```

## During Session: Log Entries

Append one JSON line to `log.jsonl` after each significant action.
Significant actions include: file created, file modified, file deleted,
test run, decision made, tool call issued, error encountered.

### log.jsonl Format

Each line is a single JSON object (no trailing comma, no array wrapper):

```json
{"time": "ISO 8601", "action": "file_created", "detail": "src/auth/login.ts"}
{"time": "ISO 8601", "action": "test_run", "detail": "12 passed, 0 failed"}
{"time": "ISO 8601", "action": "decision", "detail": "used JWT over sessions — stateless requirement"}
{"time": "ISO 8601", "action": "error", "detail": "TypeError: cannot read property 'id' of undefined"}
```

Valid `action` values: `file_created`, `file_modified`, `file_deleted`,
`test_run`, `decision`, `error`, `session_start`, `session_end`.

## Session End Protocol

1. Append a `session_end` entry to `log.jsonl`.
2. Update `manifest.json`:
   - Set `endTime` to current ISO timestamp.
   - Populate `tasksCompleted` with descriptions of what was finished.
   - Populate `filesChanged` with all file paths touched.
   - Populate `blockers` with anything unresolved (empty array if none).

## Directory Layout

```
.artifacts/
  runs/
    2026-03-24-14-30/
      manifest.json
      log.jsonl
    2026-03-24-16-00/
      manifest.json
      log.jsonl
```

`.artifacts/` is git-ignored. It is local-only audit data.

## Rules

- Never modify a past run's `manifest.json` or `log.jsonl`.
- Never delete run directories.
- One manifest per session. Multiple log entries per session is expected.
- If a session is interrupted, leave `endTime` as `null` — do not fabricate it.
- `filesChanged` must list absolute paths from the project root.
