# Phase F.5: Automated Sentry Check

> Load this file after Phase F completes. This is MANDATORY after every QA run.
> This phase is AUTOMATED via relay-sentry MCP polling. No manual log scanning required.

## Purpose

relay-sentry polls Sentry automatically for errors that surfaced during QA testing but
were not caught by test assertions. Sentry-to-GitHub Issues integration surfaces critical
errors as GitHub issues automatically.

## Steps

### 1. Poll Sentry via relay-sentry MCP

Load skill: `/relay-sentry`

- Query window: errors in the last 30 minutes, this project + environment.
- Check both frontend (browser SDK) and backend (server SDK) error feeds.
- Sentry-to-GitHub Issues integration will surface critical errors as GitHub issues.
- Any new error = **CRITICAL** finding, must be resolved before Phase I.

### 2. Review relay-sentry Summary

- CTO reviews the summary returned by relay-sentry.
- Assign CRITICAL findings to coder teammates for fix (not CTO — Nuclear Rule 1).
- Log errors are real runtime failures — they take priority over hypothetical issues.

### 3. Verify Structured Logger Is Used

- Grep for raw `console.log`/`console.error`/`console.warn` or `print()` in `src/`
  (excluding `tests/` directory).
- Any raw console output found = **CRITICAL** finding: route must use structured logger.
- This check catches "Sentry configured but logger never actually used" failures.

## Gate

```
+------------------------------------------------------------------+
| RUNTIME LOG GATE F.5: Before proceeding to Phase I:             |
| [] "relay-sentry MCP polled -- summary reviewed"                |
| [] "All CRITICAL Sentry errors from this QA session resolved"   |
| [] "No raw console.log/error/warn or print() in src/ code"      |
| [] "All findings added to consolidated reviews/slice-{N}.md"    |
+------------------------------------------------------------------+
```

## Artifacts

- Consolidated in `reviews/slice-{N}.md` (section: QA + Runtime, F.5 subsection).

## Next Phase

Proceed to **Phase I: Documentation Update** (`phase-i-documentation.md`).
