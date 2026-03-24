---
name: decision-journal
description: "Use when creating, updating, or searching Architecture Decision Records (ADRs) for framework or project decisions."
disable-model-invocation: true
---

# Decision Journal Skill

## Purpose

Manage Architecture Decision Records (ADRs) — the narrative history of **why** each architectural choice was made, what it replaced, and what we learned.

## When to Create an ADR

Create an ADR when any of these occur during a slice:

- **Architectural choice** that changes file structure, data flow, or component boundaries
- **Tool replacement** — swapping one dependency, service, or pattern for another
- **New pattern** introduced that other slices should follow
- **Nuclear Rule change** — adding, modifying, or removing a hardcoded constraint
- **Phase or workflow change** — altering how slices are executed
- **Failed approach** — documenting what didn't work and why (prevents re-trying)

## ADR Format

Use `decision-journal/adr-template.md` as the base. Required fields:

```yaml
---
type: adr
status: accepted | superseded | deprecated
date: YYYY-MM-DD
supersedes: null | NNN  # ADR number this replaces
tags: [relevant, tags]
---
```

Sections: Context, Decision, Alternatives Considered, Consequences, Lessons.

## Naming Convention

`adr-NNN-kebab-case-title.md`

- Numbers are zero-padded to 3 digits (001, 002, ... 099, 100)
- Use descriptive kebab-case titles (e.g., `adr-016-rate-limit-strategy.md`)
- Never reuse a number, even if the ADR is superseded

## Save Locations

| Scope | Vault Path | QMD Collection |
|-------|-----------|----------------|
| Framework decisions | `template-decisions/` | `template-decisions` |
| Project-specific | `projects/{PROJECT}/decisions/` | `{PROJECT}` |

## Superseding an ADR

When a decision replaces a prior one:

1. Create the new ADR with `supersedes: NNN` in frontmatter.
2. Update the old ADR: set `status: superseded` and add `superseded_by: NNN`.
3. Reference the old ADR in the new one's Context section.

## Integration with Slice Workflow

### Phase A (Preparation)

- CTO queries QMD for ADRs related to the slice topic (step A.0).
- If relevant ADRs exist, incorporate lessons into the slice plan.
- If overriding a prior ADR, note it for Phase D.

### Phase D (Self-Reflection)

- Review architectural choices made during implementation.
- Create ADRs for any decisions that meet the "When to Create" criteria.
- If overriding a prior ADR, create a superseding ADR with full rationale.

### Phase I (Documentation)

- Scribe verifies all Phase D ADRs were saved to the vault.
- Update `_index.md` if new ADRs were added.

## QMD Queries for ADR Search

```
# Find decisions about a specific topic
Tool: query
Parameters: { "query": "authentication rate limiting", "collection": "template-decisions" }

# Find project-specific decisions
Tool: query
Parameters: { "query": "database schema migration", "collection": "{PROJECT}" }

# Find superseded decisions (to understand evolution)
Tool: query
Parameters: { "query": "replaced deprecated superseded", "collection": "template-decisions" }
```

## Anti-Patterns

- Do not create ADRs for trivial choices (variable names, formatting).
- Do not duplicate information already in contract articles — reference the article instead.
- Do not create ADRs retroactively for decisions you can't explain the "why" for.
- Do not skip the Alternatives section — if there were no alternatives, the decision wasn't architectural.
