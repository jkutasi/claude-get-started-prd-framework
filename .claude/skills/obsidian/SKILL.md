---
name: obsidian
description: "Use when reading, writing, or searching the project's Obsidian vault — incident notes, learnings, slice journals. For on-device semantic search over the same vault, use relay-qmd instead."
disable-model-invocation: true
---

# Obsidian Vault Skill

## 1. Role Identity

This skill operates the Obsidian vault holding project incident notes, learnings, and
slice journals for projects bootstrapped from this template. It uses MCP `mcp__obsidian__*`
tools for direct file operations — create, read, edit, move, delete, tag, search. For
semantic or hybrid search across the vault (when you do not know the exact path), use
`relay-qmd` instead.

## 2. MCP Setup

Add to `.claude/settings.local.json`:

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-obsidian", "--vault", "~/ObsidianVault"]
    }
  }
}
```

Available tools: `read-note`, `create-note`, `edit-note`, `move-note`, `delete-note`,
`add-tags`, `remove-tags`, `rename-tag`, `search-vault`, `list-available-vaults`,
`create-directory`.

## 3. Standard Vault Structure

```
~/ObsidianVault/
  projects/{PROJECT_NAME}/
    incidents/    YYYY-MM-DD-<slug>.md   — one file per fix attempt
    learnings/    <topic>.md             — forward-looking rules from incidents
    slices/       slice-N-summary.md     — one file per shipped slice
    decisions/    <adr-slug>.md          — project-specific ADRs
```

Bootstrap these directories on project start:

```
mcp__obsidian__create-directory  projects/{PROJECT_NAME}/incidents
mcp__obsidian__create-directory  projects/{PROJECT_NAME}/learnings
mcp__obsidian__create-directory  projects/{PROJECT_NAME}/slices
mcp__obsidian__create-directory  projects/{PROJECT_NAME}/decisions
```

## 4. When to Use vs. Siblings

| Task | Skill |
|------|-------|
| Direct file read / write / tag / search by path | **obsidian** (this skill) |
| Semantic search — don't know the path | `relay-qmd` |
| Write a structured incident note end-to-end | `troubleshooting-log` (uses this skill) |
| Search past incidents before a high-stakes fix | `troubleshooting-recall` (uses this skill + relay-qmd) |

## 5. Incident Note Template

Path: `projects/{PROJECT_NAME}/incidents/YYYY-MM-DD-<slug>.md`

```markdown
---
date: <YYYY-MM-DD>
project: {PROJECT_NAME}
slice: <slice-id>
outcome: worked | failed | deferred
tags: [incident, troubleshooting]
severity: P0 | P1 | P2
---

# Incident: <one-line title>

## Symptom
<what user/operator saw>

## Hypothesis
<what we suspected before investigating>

## Fix Attempted
- Files: <list>
- Summary: <one paragraph>

## Outcome
worked | failed | deferred

## Root Cause
<the actual mechanism, in plain English>

## Commit
<SHA or n/a>

## Lesson Link
[[../learnings/<topic>#section]]

## Verification
<what proved it worked>
```

If `outcome: worked` and the lesson generalizes, also append a forward-looking rule to
`projects/{PROJECT_NAME}/learnings/<topic>.md` and link back to the incident.

## 6. Cross-Linking Discipline

- Incident note links to its learning note (`[[../learnings/<topic>]]`).
- Learning note links back to the incident (`[[../incidents/<date>-<slug>]]`).
- Git commit message references the incident path in its body.
- `MEMORY.md` references commit SHA + incident path when the lesson is project-scoped.

## 7. Anti-Patterns

- Writing the incident note days later. Memory decays. Write same-day.
- Combining multiple incidents in one note. One incident per note; cross-link if related.
- Documenting only successes. Failures and deferrals carry the highest-value lessons.
- Storing secrets (API keys, tokens, connection strings) in vault notes.

## 8. See Also

- `.claude/skills/relay-qmd/SKILL.md` — semantic search over this vault
- `decision-journal/seed-vault.sh` — bootstrap ADRs into the vault on project init
- `scripts/sync-to-vault.sh` — sync canonical files into the vault mirror
- `contract-templates/articles/article-20e-1-logging-and-errors.md` — error observability
