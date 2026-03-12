# Article 34: Error Diagnosis Protocol

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.
>
> **Enforces:** Nuclear Rule 7 (Never Commit Without Checking Runtime Errors)
>
> **Cross-references:** Article 28 (Service Log Inventory), Article 35 (Error & Rescue Registry)

## The Rule

When an error is reported, the FIRST action is ALWAYS to check the logs. Never edit code before reading runtime data. Agents default to guessing at code fixes instead of reading the logs. This is backwards — you can't fix what you haven't diagnosed.

## 5-Step Diagnosis Flow

1. Read the error report
2. Check primary log source (use Service Log Inventory — Article 28)
3. Read actual error data — stack traces, timestamps, request context
4. Check upstream/downstream services if needed
5. Only AFTER understanding the runtime failure do you touch code

## Triage by Error Type

| Symptom | Check First | Then Check |
|---------|------------|------------|
| Frontend crash | Frontend runtime logs | Error tracker — backend API logs |
| API 500 | Error tracker — API service logs | Database logs |
| Wrong/missing data | Database logs — queries | Backend service logs |
| External API failure | Error tracker — API wrapper logs | External error codes / rate limits |
| Slow performance | Performance tracing | Cloud logging — query times |
| Auth issues | Error tracker — auth service logs | Auth provider logs |

## No Logs = P0 Gap

If you attempt diagnosis and discover the service has no accessible logs, report that as a P0 gap immediately. Diagnosis is paused until logging is added. An unobservable service cannot be properly debugged.

## QA Expansion

Every QA agent must check logs as part of its standard process. QA is not "does the code look right" — it's "does the code work right, and can I prove it from runtime data."

## Why This Matters

When an error is reported, agents default to guessing at code fixes instead of reading the logs. This is backwards — you can't fix what you haven't diagnosed. Forces agents to check runtime data before touching code, and flags missing log sources as P0 gaps. Logs first, code second, always.
