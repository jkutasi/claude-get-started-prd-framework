# Article 3: Multi-Model Peer Review

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

See Nuclear Rule 2. ALL code is reviewed by independent models before it ships. ALL reviewers
must return findings before proceeding. **If peer review has not been run, the code DOES NOT
SHIP. Period.**

## 4-Model Adversarial Lineup (Phase E)

Run all four reviewers **in parallel**. No sequential chaining. To dispatch all four and produce
the consolidated artifact in one shot, use the
[peer-review-orchestrator skill](../../.claude/skills/peer-review-orchestrator/SKILL.md).

| Reviewer | Model | Lens |
|----------|-------|------|
| **Gemini** | Smartest available Gemini | Architecture, design patterns, scalability |
| **OpenAI 5.5 Reflection** | gpt-5.5 (same model that authored the code) | Invariants, silent failure modes, security surfaces, 150-line compliance |
| **Claude Opus 4.7** | CTO orchestrator itself — own review pass | Independent full-spectrum review using the same prompt template |
| **Grok** | Smartest available Grok/xAI | Security, edge cases, adversarial inputs |

The Opus 4.7 reviewer is the CTO orchestrator itself doing its own review pass — there is no
separate `reviewer-opus` skill. The other three reviewers are dispatched as external sub-agents.

**No fallback to lesser models on any provider failure.** If a provider is unreachable, report
the error and halt. Do NOT substitute a weaker model.

## API Keys

Store in `.env` (local dev) or Secret Manager (prod):

```
GEMINI_API_KEY    — Gemini reviewer
OPENAI_API_KEY    — OpenAI 5.5 reflection (Responses API)
ANTHROPIC_API_KEY — Claude Opus 4.7 reviewer
XAI_API_KEY       — Grok/xAI reviewer
```

OpenAI reviewer uses the same Responses API endpoint as Article 02:
`POST https://api.openai.com/v1/responses`, body `{"model":"gpt-5.5","input":"<review_prompt>"}`,
response field `output_text`.

## Consensus Rule

- **2+ reviewers flag the same issue** = mandatory fix before ship.
- **Single reviewer flags an issue** = advisory, team decides — EXCEPT data-correctness issues,
  which are **always mandatory** regardless of consensus count.
- Security issues flagged by any single reviewer are escalated immediately (never advisory).

## Round 2 Requirement

After mandatory fixes are applied, a **Round 2 review is required**. Run all 4 reviewers again
on the patched diff. Round 2 must return clean (no new mandatory issues) before the slice ships.

## Review Scope

Every peer review — whether for new features or refactoring — must cover:

1. Correctness and invariant violations
2. Silent failure modes (swallowed errors, missing null checks)
3. Security: injection vectors, auth/authz gaps, secrets exposure, OWASP Top 10
4. 150-line file compliance (Article 20c)
5. Architecture alignment with the slice spec

## Verdict Format

Reviewers issue definitive verdicts:

- `APPROVED` — no issues found
- `APPROVED_WITH_FIXES` — advisory issues only, ship after fixes
- `REQUIRES_REWORK` — mandatory issues; do not ship

Verdicts containing "pending user review" or "contingent on user testing" are **INVALID** —
re-run the review with clear instructions.

## Peer Review Is Autonomous

Peer review runs autonomously as part of the pipeline. It is NEVER deferred until "after user
reviews" or "contingent on user approval." The pipeline enforces this gate.

## Phase G (Red Team Post-Build) Absorbed Here

As of 2026-05-05, Phase G (Red Team Post-Build) was dropped from the workflow. Its adversarial
function is fully covered by this article's 4-model adversarial lineup: OpenAI 5.5 specifically
targets invariants, silent failure modes, and security surfaces, while Grok focuses on security
and adversarial inputs. Any post-build red-team concern should be raised as a mandatory finding in
Phase E peer review rather than a separate gate.
