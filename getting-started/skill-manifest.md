# Skill Manifest

> Part of the [Getting Started](INDEX.md) roadmap. Load after stack scoping is complete and before Slice 0 bootstrap begins.

## Purpose

The **skill manifest** is a per-project artifact that enumerates every Claude Code skill the project will rely on, identifies which already exist in `~/.claude/skills/`, and flags every gap. It is produced **once per project, after the stack is scoped and before Slice 0 starts**. The manifest is the gate that prevents a project from beginning feature work with missing capabilities — every skill must either EXIST and pass [skill-quality-contract.md](skill-quality-contract.md), or be explicitly deferred with a written reason. The manifest lives at the project root as `SKILL-MANIFEST.md` and is updated whenever the stack changes.

## Manifest Format

The manifest is a single markdown table. Use this exact column shape:

    | Tool / Layer | Required Skill | Status | Notes |
    |--------------|----------------|--------|-------|
    | Vercel       | vercel-specialist | EXISTS | Conforms to quality contract |
    | Railway      | railway-specialist | GAP | Author before Slice 0 |
    | Supabase (read) | relay-supabase | EXISTS | MCP relay agent |
    | Supabase (schema) | db-specialist | EXISTS | Shared with BigQuery work |

**Columns:**
- **Tool / Layer** — the external tool, service, or architectural layer the skill covers (one row per tool; split rows when one tool needs multiple skills, e.g., Supabase needs both `relay-supabase` for queries and `db-specialist` for schema).
- **Required Skill** — canonical kebab-case skill name (see Canonical Mappings below).
- **Status** — exactly one of `EXISTS` or `GAP`. No third state. Deferred gaps are still `GAP` with the deferral reason in Notes.
- **Notes** — one short sentence: conformance status if EXISTS, authoring plan or explicit deferral reason if GAP.

## Gap Rule

**No slice begins with open gaps.** When the manifest is produced, every row marked `GAP` MUST be resolved by one of two actions before Slice 0 starts:

1. **Author the skill** — follow [skill-quality-contract.md](skill-quality-contract.md) and the authoring procedure. Mark the row `EXISTS` only after the audit checklist passes.
2. **Explicitly defer** — leave the row `GAP` and write a one-line deferral reason in Notes (e.g., "Deferred: not used until Slice 3; will author in that slice's preflight"). A deferred gap is a written commitment, not a TODO. The slice that needs the skill MUST author it as the first step of that slice.

Silent deferral — leaving a `GAP` with no Notes entry — is forbidden. The manifest is the contract; an empty Notes cell on a GAP row fails the manifest audit.

## Canonical Mappings

Use these canonical skill names. Do not invent variants — the names below are the discovery keys.

| Tool / Service | Canonical Skill(s) | Purpose |
|----------------|--------------------|---------|
| Vercel | `vercel-specialist` | Deploy, domain, env, log triage |
| Railway | `railway-specialist` | Deploy, service config, log triage |
| Supabase | `relay-supabase` + `db-specialist` | MCP relay for queries; schema/migrations via db-specialist |
| Sentry | `sentry-specialist` (impl) + `relay-sentry` (query) | SDK install/config; MCP relay for error queries |
| BigQuery | `db-specialist` | Schema, partitioning, query optimization, load jobs |
| Cloud Run | `log-monitor` | Real-time error detection during/after deploys |
| Obsidian | `obsidian-agent` | Vault bootstrap, knowledge save, search, sync |

If a tool is not in this table, choose a canonical kebab-case name and add it to this table in the same PR that adds the skill.

## Process

Follow these steps in order. Do not skip:

1. **Enumerate the stack** — list every external tool, service, framework, and architectural layer the project will touch (output of stack scoping).
2. **Look up canonical names** — for each item, find the canonical skill name in the table above. If absent, propose a new canonical name and add it to the table.
3. **Glob the skill library** — run `ls ~/.claude/skills/` (or equivalent glob) and confirm each canonical name exists as a folder containing a conforming `SKILL.md`.
4. **Mark EXISTS or GAP** — fill the Status column. EXISTS requires both folder presence AND quality-contract conformance; if the folder exists but the skill fails the audit, it is still GAP.
5. **Resolve gaps** — for each GAP, either author the skill (preferred) or write a one-line deferral reason. Re-audit and update Status.
6. **Start Slice 0** — only when the manifest has zero unresolved gaps (every row is EXISTS or GAP-with-deferral-reason).

## Related

- [skill-quality-contract.md](skill-quality-contract.md) — the bar every EXISTS skill must clear
- `skill-manifester` meta-skill (forthcoming) — automates steps 1–4 of the Process; produces the manifest from a stack list
- [skill-lifecycle-workflow.md](skill-lifecycle-workflow.md) — find / create / promote / combine workflow used to resolve gaps
