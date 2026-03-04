# Article 12: NUCLEAR RULE ENFORCEMENT — SUPREME DIRECTIVE (OWNER MANDATE)

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

**This article overrides ALL other considerations including speed, convenience, context window pressure, and "getting things done quickly."**

**WHY THIS EXISTS:** In a prior project, the CTO (Opus) bypassed the entire multi-agent system — writing ALL code directly as a single agent with ZERO sub-agents, ZERO peer review, and ZERO QA across 6 consecutive slices. This burned context windows, degraded code quality, and violated the contract the owner approved. This must never happen again.

#### 12a. Review Artifacts Are Proof

Before ANY code is considered "done", these artifacts MUST exist on disk:

- `reviews/slice-N-test-spec.md` -- Gherkin audit traceability matrix + test specification + red phase validation (Article 17)
- `reviews/slice-N-test-review.md` -- test code peer review findings from 3 external models (Article 18)
- `reviews/slice-N-peer-review.md` -- findings from all external model reviewers + CTO synthesis + list of mandatory fixes
- `reviews/slice-N-qa-swarm.md` -- findings from all QA agents + QA Manager synthesis + prioritized fix plan
- `reviews/slice-N-red-team-pre-build.md` -- pre-build architecture review (Article 14a)
- `reviews/slice-N-red-team.md` -- post-QA adversarial red team findings (Article 14b)
- `reviews/slice-N-whiskey-team.md` -- whiskey team findings + implicit behavior regression (Article 15)
- `reviews/slice-N-ux-sense-check.md` -- UX sense check findings (Article 16, frontend slices only)

**No file = no proof = slice is invalid.** These files are the PROOF that the process was followed. Verbal claims of "I did the review" without artifact files are not acceptable.

#### 12b. How to Run Peer Review

The CTO spawns 3 sub-agents in parallel (4 if Greptile is configured), each calling one external model/service:

1. **Gemini reviewer:** Sub-agent reads the code, sends to Gemini API, returns structured findings
2. **OpenAI Codex reviewer:** Sub-agent prepares review prompt, executes Codex CLI in read-only sandbox, returns structured findings
3. **Grok reviewer:** Sub-agent reads the code, sends to Grok/xAI API, returns structured findings
4. **Greptile reviewer (optional):** Sub-agent submits code to Greptile API for codebase-aware review, returns structured findings. Only runs if `GREPTILE_API_KEY` is configured.

CTO synthesizes all findings. Issues flagged by 2+ reviewers = MANDATORY fixes. All findings + synthesis saved to `reviews/slice-N-peer-review.md`.

API keys are stored in `.env` (local dev) or Secret Manager (production). They are AVAILABLE. There is NO excuse for skipping this step.

#### 12c. How to Run QA Swarm

The CTO (or QA Lead teammate) spawns QA sub-agents in parallel (red team framing — see Article 7c):

1. QA Stats — validates math correctness, algorithm logic, edge cases
2. QA Code Quality — clean code, patterns, DRY, naming (Article 10)
3. QA Data Integrity — query correctness, schemas, data validation
4. QA Security — OWASP, API key exposure, injection vectors
5. QA UI/UX + Browser — accessibility, responsive design, browser compat (via agent-browser)

Plus the mandatory additional QA layers:
6. Whiskey Team — adversarial QA + implicit behavior regression (Article 15)
7. UX Sense Check — persona-based browser testing (Article 16, frontend slices only)

QA Manager formats all findings into prioritized fix plan. All findings + synthesis saved to `reviews/slice-N-qa-swarm.md`.

#### 12d. Context Window Is NOT an Excuse

The multi-agent system EXISTS to protect context windows. The CTO spawns small, focused sub-agents that each handle one task. This PRESERVES the CTO's context for synthesis and decision-making. Writing all code as a single agent is the OPPOSITE of context conservation — it burns the CTO's context window on implementation details that sub-agents should handle.

If context is running low:
- Assign remaining work to a teammate
- Have them spawn sub-agents and return summaries
- NEVER skip peer review to "save context"

#### 12e. Session Start Checklist

At the START of every new session, before ANY implementation work:

1. Read CLAUDE.md (core contract — start from the top)
2. Check `.env` — verify API keys exist for peer review models
3. Run `python gate_check.py --slice {LATEST_SLICE} --all` to verify all completed slices
4. If ANY slice returns FAIL, run RETROACTIVE REVIEW on that slice first
5. Only then proceed with new work

#### 12f. Retroactive Review Process

If any slice shipped WITHOUT peer review (contract violation), the next session MUST:

1. Check `reviews/` directory for missing artifact files
2. Run retroactive peer review on each unreviewed slice (spawn reviewer sub-agents)
3. Run retroactive QA swarm on each unreviewed slice (spawn QA sub-agents)
4. Save artifacts to `reviews/`
5. Fix any mandatory issues found
6. Only then proceed with new work

ALL code written without peer review is considered UNVALIDATED and SUSPECT. The owner MUST be notified immediately that the process was bypassed.

#### 12g. Commit Convention

Commits MUST include proof of review:

```
[Slice N] Brief description of what changed

- Detail 1
- Detail 2

Co-Authored-By: {AGENT_NAME} ({MODEL})
Reviewed-By: Reviewer Gemini, Reviewer OpenAI Codex, Reviewer Grok
QA-Passed: QA Stats, QA Code Quality, QA Data Integrity, QA Security, QA UI/UX
Red-Team: Passed (reviews/slice-N-red-team.md)
Whiskey-Team: Passed (reviews/slice-N-whiskey-team.md)
```

Commits WITHOUT Reviewed-By and QA-Passed lines are CONTRACT VIOLATIONS.
