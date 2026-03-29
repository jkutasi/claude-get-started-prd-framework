# Skill Lifecycle Workflow

> When you need to find, create, promote, or combine a skill — follow this flowchart.

## Two Skill Levels

| | User-Level | Workspace-Level |
|---|---|---|
| **Location** | `~/.claude/skills/` | `.claude/skills/` |
| **Scope** | All projects on this machine | This project only |
| **Discovery** | `SKILLS-INDEX.md` or `/list-skills` | Directory listing |
| **Count** | 94+ skills (canonical library) | Varies per project |
| **Managed by** | `/refresh-index` | Manual or template bootstrap |

User-level is the **canonical library** — shared across every project.
Workspace-level holds project-specific skills or template seed copies.

## Decision Flowchart

### Step 1: Check User-Level First

Read `~/.claude/skills/SKILLS-INDEX.md` or run `/list-skills`.

- **Found?** → Use it directly. Done.
- **Not found?** → Continue to Step 2.

### Step 2: Check Workspace-Level

Look in `.claude/skills/` for the skill.

- **Found at workspace but not user-level?** → Evaluate for promotion (see below).
- **Found at both levels?** → User-level takes precedence. Keep workspace copy only if it has project-specific additions.
- **Not found at either?** → Continue to Step 3.

### Step 3: Similar Skill Exists?

Search both levels for skills with overlapping purpose.

- **>70% overlap in purpose?** → Extend the existing skill rather than creating a duplicate.
- **Distinct purpose?** → Create a new skill. Continue to Step 4.

### Step 4: Create From Scratch

Follow [skill-v2-creation-guide.md](skill-v2-creation-guide.md) for the full v2 format.

1. Create directory: `~/.claude/skills/{skill-name}/`
2. Write `SKILL.md` with YAML frontmatter + markdown body
3. Write `CREATION-LOG.md` (see [skill-creation-log-convention.md](skill-creation-log-convention.md))
4. Run `/refresh-index` to update `SKILLS-INDEX.md`

## Promotion Criteria

**When to promote** (workspace → user-level):

| Promote | Don't Promote |
|---------|--------------|
| Reusable across 2+ projects | Contains project-specific paths |
| General-purpose behavior | Thin wrapper around project config |
| Not tied to a specific tech stack | References project-specific contracts |
| Useful for future projects | One-time or experimental |

**How to promote:**

1. Copy the skill directory to `~/.claude/skills/{skill-name}/`
2. Remove any project-specific references from the copy
3. Run `/refresh-index`
4. Optionally remove the workspace copy (or keep for project overrides)

## After Any Skill Change

- [ ] Run `/refresh-index` to update `SKILLS-INDEX.md`
- [ ] Write `CREATION-LOG.md` if new (see [skill-creation-log-convention.md](skill-creation-log-convention.md))
- [ ] Verify description starts with "Use when..." (see [skill-description-audit.md](skill-description-audit.md))
- [ ] If user-level skill was updated, remember it applies to ALL future projects
- [ ] If workspace skill diverges from user-level, document why in the workspace copy
