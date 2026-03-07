# Article 28: Service Log Inventory & Observability Ops

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.
>
> **Cross-references:** ARCHITECTURE-STANDARDS §5 (Structured Logging & Observability)

Every service in the stack must have structured logging and a way for agents to access those logs. If a service doesn't have logging, that is a P0 gap — it gets fixed before any feature work. You cannot debug what you cannot see.

## Service Log Inventory Template

Define the inventory per project. Replace placeholders with your project's actual services.

| Service | Log Source | Agent Access Method |
|---------|-----------|-------------------|
| {SERVICE_NAME} | {LOG_SOURCE} | {AGENT_ACCESS_METHOD} |
| {SERVICE_NAME} | {LOG_SOURCE} | {AGENT_ACCESS_METHOD} |

**Example rows (adapt to your stack):**

| Service | Log Source | Agent Access Method |
|---------|-----------|-------------------|
| Backend API (Cloud Run) | Sentry + Pino → Google Cloud Logging | Sentry MCP + `gcloud logging read` |
| Frontend (Vercel) | Vercel Runtime Logs | Vercel CLI (`vercel logs`) or dashboard |
| Database (Supabase) | Supabase Dashboard / Postgres logs | Supabase MCP or dashboard API |
| Cron Jobs | Sentry + structured logger | Sentry MCP + Cloud Logging |

## The P0 Gap Rule

If you look at the inventory table and a service doesn't have a log source or an agent access method, that's not a "we'll get to it" item. That's a P0. Add logging to that service before building anything else on top of it. An unobservable service is a service that will break silently and cost you hours — or client money — to debug.

## Why This Matters

Without structured logging and error monitoring, we're blind. We don't know what's breaking, we don't know when it started, and we can't prove to a client that something is or isn't working. This is also what makes Nuclear Rule 7 (runtime verification) mechanically possible — no logging infrastructure means nothing for the verification agent to check.
