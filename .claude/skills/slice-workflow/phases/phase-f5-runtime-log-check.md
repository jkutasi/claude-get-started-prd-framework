# Phase F.5: Runtime Log Check

> Load this file after Phase F completes. This is MANDATORY after every QA run. Complete the gate before proceeding to Phase G.

## Purpose

Check all available logs for errors that surfaced during QA testing but were not caught by test assertions. Runtime errors are real failures — not hypothetical.

## Steps

> **QMD QUERY** (non-blocking): Spawn `/relay-qmd` — query `"recurring runtime errors log patterns {SLICE_TOPIC}"` in `{PROJECT_NAME}`. Compare prior patterns against current logs. If QMD unavailable, proceed.

### 1. Check Sentry (via MCP or dashboard)

- Query for new errors triggered during this QA session.
- Check both frontend (browser SDK) and backend (server SDK) error feeds.
- Any new error = **CRITICAL** finding, added to the Phase G fix queue immediately.

### 2. Check Deployment/Server Logs (if staging environment)

- Vercel function logs, server logs, or equivalent.
- Look for unhandled exceptions, 500 errors, timeout failures.
- Any server error during QA = **CRITICAL**.

### 3. Check Database Logs (if DB access available)

- Failed queries, constraint violations, transaction rollbacks.
- Any DB error that occurred during QA testing = **CRITICAL**.

### 4. Add to Fix Queue

- CTO adds ALL log findings to the Phase G queue alongside QA agent findings.
- Log errors are treated as **CRITICAL** — they are real runtime failures, not hypothetical.

## Gate

```
+------------------------------------------------------------------+
| RUNTIME LOG GATE F.5: Before proceeding to Phase G:              |
| [] "Sentry checked — all new errors from this QA run logged"     |
| [] "Server/function logs checked (if staging environment)"       |
| [] "DB logs checked (if DB access available)"                    |
| [] "All log findings added to Phase G fix queue"                 |
+------------------------------------------------------------------+
```

## Next Phase

Proceed to **Phase G: Autonomous Fix Verification** (`phase-g-autonomous-fix.md`).
