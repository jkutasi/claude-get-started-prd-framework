# Article 3: Multi-Model Peer Review

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

See Nuclear Rule 2. ALL code reviewed by independent models. ALL reviewers must return findings before proceeding. Consensus issues (flagged by 2+ reviewers) are mandatory fixes.

API keys for peer review are stored in `.env` (local dev) or Secret Manager (prod):
- `GEMINI_API_KEY` — Gemini (reviewer #1)
- `OPENAI_API_KEY` — OpenAI Codex (reviewer #2)
- `XAI_API_KEY` — Grok/xAI (reviewer #3)
- `GREPTILE_API_KEY` — Greptile (reviewer #4, **optional**) — codebase-aware AI review

**Minimum 3 reviewers required.** If `GREPTILE_API_KEY` is configured, Greptile runs as a 4th reviewer in parallel. If not configured, the 3-reviewer workflow is unchanged.

**If peer review has not been run, the code DOES NOT SHIP. Period.**

**Peer review runs autonomously as part of the pipeline.** It is NEVER deferred until "after user reviews" or "contingent on user approval." The reviewers issue definitive verdicts (APPROVED / APPROVED_WITH_FIXES / REQUIRES_REWORK). If a reviewer's verdict includes language like "pending user review" or "contingent on user testing," that verdict is INVALID — re-run the review with clear instructions.

**Security is always in scope.** Every peer review — whether for new features or refactoring — must include security as a review dimension. Reviewers must check for: injection vectors, auth/authz gaps, secrets exposure, OWASP Top 10 violations, and dependency vulnerabilities. This applies to refactoring work equally — restructuring code can introduce security regressions.
