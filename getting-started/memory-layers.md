# Memory Layers — Top-Level Guide

This template stack uses a five-tier memory model (Tier 0 through Tier 4). Each tier has a distinct scope, persistence, and writer. Use this guide to choose the right tier and avoid duplicating the same fact across multiple stores.

## The Tiers

### Tier 0 — In-session context (the conversation itself)
- **Scope:** current conversation only
- **Persistence:** clears at session end
- **Use for:** working memory of the current task

### Tier 1 — `~/.claude/memory/MEMORY.md` (file-based, linear)
- **Scope:** user-scoped (across all projects)
- **Persistence:** durable, file-based
- **Format:** linear markdown, plus per-topic files indexed in MEMORY.md
- **Vectorized:** NO — linear keyword search only
- **Use for:** user preferences, generic feedback, cross-project patterns
- **Auto-managed** by Claude per the auto-memory protocol

### Tier 2 — `mcp__memory__*` (in-session knowledge graph)
- **Scope:** session
- **Persistence:** ephemeral by default (some MCP memory servers persist)
- **Format:** knowledge graph (entities, relations, observations)
- **Vectorized:** depends on server implementation
- **Use for:** structured working memory during a single conversation

### Tier 3 — Obsidian (durable, project-scoped, narrative)
- **Scope:** per-project Obsidian vault
- **Persistence:** durable
- **Format:** markdown notes with wikilinks; narrative form
- **Vectorized:** yes (via Obsidian's plugins / `mcp__obsidian__search-vault`)
- **Use for:** project documentation, incident reports (human-readable), curated knowledge that humans review
- **Primary writer:** humans + the `troubleshooting-log` skill

### Tier 4 — Reserved
- Not currently used. If a structured agent-queryable memory tier is added, document it here.

## Decision Tree — Write Side

Pick exactly one tier per fact. Do not duplicate.

- User preference, generic feedback → **Tier 1**
- Session-scoped working memory → **Tier 0 / Tier 2**
- Project incident (after a fix attempt) → **Tier 3 (Obsidian) MANDATORY**
- Project documentation that humans read → **Tier 3**

## Decision Tree — Read Side (Cascade)

Search in order; stop at first hit. If exhausted, no prior context exists.

1. **Tier 0** (current session)
2. **Tier 1** (MEMORY.md grep)
3. **Tier 2** (`mcp__memory__*` if available)
4. **Tier 3** (Obsidian via `mcp__obsidian__search-vault`)

## Cross-References

- `troubleshooting-workflow.md` — the troubleshooting cascade specifically
- `skill-quality-contract.md` — the skills that interact with these tiers
