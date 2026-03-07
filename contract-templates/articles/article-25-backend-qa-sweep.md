# Article 25: 6-Agent Backend QA Sweep

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

When critical issues are suspected across the backend, launch a dedicated Agent Team in a fresh context.

**Prompt:**
> Launch a 6 person backend agent team to diagnose all P0 and P1 issues (P0 = system broken, P1 = important but workaround exists), double check they are in fact errors and patch them when complete, focus on breaking changes and core logic primarily

## Agent Scope Table

Define the scope table per project. Replace the example below with your project's actual domain boundaries.

| Agent | Scope | Focus |
|-------|-------|-------|
| 1 | {DOMAIN_1} | {FOCUS_AREAS} |
| 2 | {DOMAIN_2} | {FOCUS_AREAS} |
| 3 | {DOMAIN_3} | {FOCUS_AREAS} |
| 4 | {DOMAIN_4} | {FOCUS_AREAS} |
| 5 | {DOMAIN_5} | {FOCUS_AREAS} |
| 6 | {DOMAIN_6} | {FOCUS_AREAS} |

## Post-Patch Verification

After all 6 agents complete patches:
1. Spin up 2 code-review sub-agents to verify fixes
2. Spin up a verification sub-agent to check error tracker, application logs, health endpoints (Nuclear Rule 7)
3. All checks clean — commit
4. Dismiss all agents

Total time: ~10 minutes for full diagnostic + patch + review + runtime verification.

## Standing Orders for QA Agents

1. **Check the logs FIRST.** Before reviewing code, before guessing at fixes — read the relevant log sources (see Article 28 Service Log Inventory). Logs tell you what's actually broken.
2. Focus on P0 and P1 only — breaking changes and core logic. Not cosmetic issues.
3. Double-check flagged issues are real errors before patching. Don't fix what isn't broken.
4. Fix properly. No hacking, no lint ignores, no workarounds (Nuclear Rule 6).
5. Stay within assigned scope. Issues outside your domain — report, don't fix.
6. **If a service in your scope has no accessible logs, report that as a P0 gap.** An unobservable service cannot be properly QA'd.
7. Follow the Error Diagnosis Protocol (Article 34) — logs first, code second, always.

## Why This Matters

This is the deep-clean protocol for finding breaking changes and core logic bugs that lint can't see. Without it, P0/P1 issues accumulate silently until something catastrophic happens in production. The 10-minute sweep catches what static analysis misses.
