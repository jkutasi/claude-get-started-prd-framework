# Seed ADRs: Framework Evolution

These ADRs track how the framework evolved in response to real failures and new requirements.

---

## ADR-007: Mandatory Observability Gates

- **Status:** accepted
- **Date:** 2026-03-01
- **Tags:** observability, sentry, pino, gates

**Context:** Documentation said "install Sentry and Pino" but 8 slices shipped across multiple projects without either being configured. Docs alone don't create compliance.

**Decision:** Added `gate_check.py` that verifies Sentry is receiving errors and Pino/structlog is producing structured logs. Gate blocks Phase J if observability is missing. Slice 0 must install these before Slice 1 begins.

**Alternatives:** Documentation-only (already failed), manual verification (forgotten), optional setup (skipped).

**Consequences:** Every project now has observability from Slice 1. Trade-off: Slice 0 takes longer, but runtime errors are now visible immediately.

**Lessons:** If a tool is important enough to document, it's important enough to gate. Documentation without enforcement is decoration.

---

## ADR-008: Professor Review System

- **Status:** accepted
- **Date:** 2026-03-05
- **Tags:** review, professors, domain-expertise

**Context:** Red Team review caught security and adversarial issues but missed domain-specific problems — incorrect business logic, wrong data models, UI anti-patterns. Needed depth beyond security.

**Decision:** 15 domain-expert "Professor" agents review during Phase A.7, each specializing in an area (database design, API patterns, accessibility, etc.). Professors can BLOCK a slice.

**Alternatives:** More Red Team members (same blind spot), human domain review (too slow), expanded peer review (already 3 models).

**Consequences:** Domain-specific issues caught before implementation begins. Trade-off: more agents, more time in A.7, but prevents costly rework in later phases.

**Lessons:** Security review and domain review are different disciplines. Don't expect one system to cover both.

---

## ADR-009: Error & Rescue Registry

- **Status:** accepted
- **Date:** 2026-03-10
- **Tags:** error-handling, registry, article-35

**Context:** Code shipped with unhandled failure paths. Agents would implement the happy path but leave error scenarios as TODO or generic catch-all handlers.

**Decision:** Article 35 requires an Error & Rescue Registry — every known error maps to a specific handler, recovery strategy, and test. Phase D (Self-Reflection) must produce this registry.

**Alternatives:** Generic error boundaries (masks issues), lint rules for try/catch (too shallow), error documentation only (not enforced).

**Consequences:** Every error path is explicitly designed and tested. Trade-off: more upfront work in Phase D, but eliminates "silent failure" class of bugs.

**Lessons:** Error handling is architecture, not cleanup. Design it during reflection, not as an afterthought.

---

## ADR-010: Mem0 to QMD Migration

- **Status:** accepted
- **Date:** 2026-03-17
- **Tags:** knowledge, qmd, mem0, privacy

**Context:** Mem0 stored project knowledge in the cloud. This created privacy concerns and dependency on an external service. Knowledge retrieval was also slow due to network latency.

**Decision:** Migrate to QMD — on-device semantic search using node-llama-cpp with GGUF models. Indexes markdown files in an Obsidian vault. BM25 + vector + LLM reranking, all local.

**Alternatives:** Continue Mem0 (privacy risk), local SQLite FTS (no semantic search), Chroma (heavier setup, still local).

**Consequences:** All knowledge stays on-device. Faster retrieval. Trade-off: requires local compute for embeddings, but modern machines handle this easily.

**Lessons:** On-device > cloud for project knowledge. The privacy and speed benefits outweigh the setup cost.

---

## ADR-011: Skills v2 (YAML Frontmatter)

- **Status:** accepted
- **Date:** 2026-03-17
- **Tags:** skills, yaml, discovery

**Context:** Flat `skill-templates/` directory had no metadata. Skills were just markdown files with no way to programmatically discover, filter, or validate them.

**Decision:** Skills v2: each skill lives in its own directory under `.claude/skills/` with a `SKILL.md` file containing YAML frontmatter (name, description, custom-agent binding, disable-model-invocation flag).

**Alternatives:** JSON skill manifests (harder to read), database registry (overkill), naming conventions only (fragile).

**Consequences:** Skills are discoverable via frontmatter parsing. Agent-skill binding is explicit. Trade-off: more directories, but each skill is self-contained.

**Lessons:** Metadata should live with the content it describes, not in a separate registry.

---

## ADR-012: Agent/Skill Separation

- **Status:** accepted
- **Date:** 2026-03-17
- **Tags:** agents, skills, separation-of-concerns

**Context:** Agent definitions accumulated behavior — prompts, rules, workflows. This made agents hard to maintain and impossible to compose. Changing a workflow meant editing an agent.

**Decision:** Agents are thin shells (WHO) — just identity, model, tools, and skill references. Skills are rich behavior (HOW) — workflows, rules, templates. Agents load skills at runtime.

**Alternatives:** Monolithic agents (current pain), shared libraries (no identity), plugin system (over-engineered).

**Consequences:** Agent files are ~15 lines. Skills can be shared across agents. Trade-off: indirection (agent -> skill), but composability is worth it.

**Lessons:** Separate identity from behavior. When agents get complex, extract the behavior into skills.
