# Article 27: Post-Work Hygiene

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.
>
> **Enforces:** Nuclear Rule 5 (One Concern Per Sub-Agent — Then It Dies)

After every completed unit of work:

| Situation | Action |
|-----------|--------|
| Sub-agent finished its concern | Dismiss it — don't reuse |
| Working in main Claude Code session | `/clear` to reset context |
| Large job complete | Code review → runtime verification → commit → dismiss all agents → push |
| Small job complete | Commit → dismiss or `/clear` → push |
| 6-agent QA sweep complete | 2 code-review agents verify → runtime verification sub-agent checks error tracker/logs/health → commit → dismiss all → push |
| Before ANY push | Run Pre-Push Public Repo Checklist (SECURITY.md). Verify no secrets, proprietary data, or stale files. |
| After ANY push | Check Sentry (new errors?), Vercel deployment logs (build/runtime failures?), and Greptile (codebase scan). Fix before starting new work. |

## Why This Matters

Stale context is where compounding errors come from. If an agent or session isn't dismissed after completing its job, leftover context from the previous task bleeds into the next one. When a sub-agent works on multiple things, it carries stale context from the first job into the second. That stale context causes hallucinated file states, phantom bugs, and compounding errors that are nearly impossible to trace.

**The principle:** Fresh context for every new concern. The hygiene table makes cleanup automatic, not optional.
