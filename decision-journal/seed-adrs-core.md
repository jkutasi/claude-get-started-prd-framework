# Seed ADRs: Core Architecture

These are the foundational architecture decisions for the Claude Code template framework. Each should be split into an individual ADR file by `seed-vault.sh`.

---

## ADR-001: Contract-Based Architecture

- **Status:** accepted
- **Date:** 2025-12-01
- **Tags:** architecture, contracts, enforcement

**Context:** Early agent orchestration relied on verbal agreements — "the CTO agent will enforce X." Agents frequently ignored or forgot constraints mid-conversation.

**Decision:** Replace verbal agreements with numbered written articles (contract-templates/articles/). Each article is a binding reference that agents cite by number when enforcing rules.

**Alternatives:** Prompt-only enforcement (too fragile), hardcoded logic (too rigid), per-project rules (inconsistent).

**Consequences:** Enforcement became mechanical — agents cite "Article 14b" instead of re-explaining rules. Trade-off: more files to maintain, but violations are now objectively detectable.

**Lessons:** Agents respect structure they can reference. Implicit rules get ignored; explicit numbered articles get followed.

---

## ADR-002: Three-Model Peer Review

- **Status:** accepted
- **Date:** 2026-01-15
- **Tags:** peer-review, quality, multi-model

**Context:** Single-model review (Claude only) consistently missed entire bug categories. Architecture issues, edge cases, and security vulnerabilities each require different analytical strengths.

**Decision:** Mandatory 3-model review: Gemini (architecture + patterns), Codex (edge cases + correctness), Grok (security + attack surface). All three must report before a slice ships.

**Alternatives:** Single-model with multiple passes (same blind spots), human-only review (too slow), random model selection (inconsistent coverage).

**Consequences:** Bug detection improved significantly across categories. Trade-off: slower review cycle, higher token cost, but catches issues that would otherwise reach production.

**Lessons:** Model diversity is a feature, not overhead. Each model has genuine blind spots that others cover.

---

## ADR-003: Autonomous QA Pipeline

- **Status:** accepted
- **Date:** 2026-01-20
- **Tags:** qa, automation, pipeline

**Context:** Manual QA handoffs lost context between phases. QA agents didn't know what had been tested, what failed, or what was already fixed.

**Decision:** 6-step QA pipeline (functional, integration, edge-case, regression, UX, whiskey test) with structured roll-up reports. Max 3 autonomous fix retries before escalation.

**Alternatives:** Manual QA checklist (context loss), single QA pass (insufficient coverage), unlimited retries (infinite loops).

**Consequences:** QA became predictable and thorough. The 3-retry cap prevents infinite fix loops. Trade-off: rigid pipeline may over-test trivial slices.

**Lessons:** Bounded autonomy (max retries + escalation) prevents agents from spinning. Structure the pipeline, not just the tests.

---

## ADR-004: MCP Relay Pattern

- **Status:** accepted
- **Date:** 2026-02-01
- **Tags:** mcp, relay, context-management

**Context:** Direct MCP tool calls from the CTO agent polluted its context window with raw API responses (JSON blobs, full error traces, verbose metadata).

**Decision:** Relay agents act as translators between MCP servers and the team. They query MCP tools, summarize results to 30 lines max, and return structured reports.

**Alternatives:** Direct MCP access (context pollution), shared MCP cache (stale data), manual summaries (slow).

**Consequences:** CTO context stays clean. Relay agents absorb the verbosity. Trade-off: extra agent spawns, but context clarity is worth the cost.

**Lessons:** Raw tool output is never appropriate for orchestrator context. Always have a translator layer.

---

## ADR-005: Repository Hygiene as Nuclear Rule

- **Status:** accepted
- **Date:** 2026-02-10
- **Tags:** nuclear-rules, git, hygiene

**Context:** Scratch files, debug logs, and personal notes kept getting committed to the repository. Agents would stage everything without checking.

**Decision:** Repository hygiene is Nuclear Rule 4 — violating it means the slice fails and restarts. `.gitignore` must exclude scratch files, and agents must verify staging before commit.

**Alternatives:** Pre-commit hooks only (agents bypassed them), post-commit cleanup (damage already done), warnings (ignored).

**Consequences:** Nuclear Rule status means agents treat hygiene as non-negotiable. Trade-off: slice restart is harsh, but it eliminated the problem completely.

**Lessons:** If agents keep ignoring a guideline, escalate it to a Nuclear Rule. The cost of restart creates genuine compliance.

---

## ADR-006: Workflow Consolidation (9 Nuclear Rules + Articles)

- **Status:** accepted
- **Date:** 2026-02-15
- **Tags:** nuclear-rules, articles, consolidation

**Context:** Rules were scattered across multiple documents — some in CLAUDE.md, some in skill files, some in ad-hoc notes. Enforcement was inconsistent because agents couldn't find the authoritative source.

**Decision:** Consolidate into 9 Nuclear Rules (hardcoded constraints) and 35 numbered articles (detailed policies). Nuclear Rules are in every orchestrator prompt. Articles are in contract-templates/.

**Alternatives:** Single mega-document (too long), per-agent rules (inconsistent), wiki-style (agents can't browse).

**Consequences:** Single source of truth for enforcement. Agents cite rule numbers. Trade-off: maintaining article numbering requires discipline when adding new policies.

**Lessons:** Scattered rules create selective compliance. Numbered, centralized rules create mechanical enforcement.
