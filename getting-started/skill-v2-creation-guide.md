# Skill V2 Creation Guide

> Step-by-step reference for building a SKILL.md from scratch in v2 format.

## Anatomy of a SKILL.md

Every skill has two parts: **YAML frontmatter** (metadata) and **markdown body** (behavior).

Minimal skeleton:

    ---
    name: my-skill
    description: "Use when starting a new database migration. Validates schema changes."
    ---

    # My Skill

    ## Instructions

    1. First step
    2. Second step

    ## Anti-Patterns

    - Do not skip validation

## YAML Frontmatter Reference

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Kebab-case identifier. **Must match folder name.** |
| `description` | Yes | string (≤1024 chars) | Trigger condition. **Must start with "Use when..."** |
| `custom-agent` | No | string | Binds to agent in `.claude/agents/`. Example: `cto` |
| `disable-model-invocation` | No | boolean | `true` = must call explicitly with `/skill-name` |
| `context` | No | `fork` | Runs in isolated context. Use for read-only reviewers |
| `agent` | No | string | Built-in agent type. Example: `Explore` |
| `allowed-tools` | No | comma-separated | Restricts tools. Example: `Read, Grep, Glob` |

## Common Frontmatter Patterns

**Minimal** — most skills need only name + description:

    ---
    name: complexity-scoring
    description: "Use when about to start implementing any task. Score complexity before writing a single line of code."
    ---

**Agent-bound** — runs only under a specific custom agent:

    ---
    name: cto-orchestrator
    description: "Use when orchestrating a vertical slice or coordinating agent teams."
    custom-agent: cto
    disable-model-invocation: true
    ---

**Forked read-only** — isolated context with restricted tools:

    ---
    name: prof-architecture
    description: "Use when evaluating or planning system architecture, module boundaries, coupling, or cohesion."
    context: fork
    agent: Explore
    allowed-tools: Read, Grep, Glob
    disable-model-invocation: true
    ---

## Writing the Description

The `description` field is the **trigger** — Claude Code uses it for auto-discovery.

**Rules:**
- MUST start with "Use when..."
- Max 1024 characters
- Contains ONLY triggering conditions (not role summaries)

| Good | Bad |
|------|-----|
| "Use when about to start implementing any task. Score complexity before writing code." | "Complexity scoring agent that helps developers assess task difficulty." |
| "Use when orchestrating a vertical slice or coordinating agent teams." | "CTO orchestrator for managing project workflows." |

## Markdown Body Structure

| Section | Purpose | Required? |
|---------|---------|-----------|
| `# Skill Title` | Human-readable name | Yes |
| `## Identity` | Category, tags, invocation, depth | Optional |
| `## Instructions` / `## Protocol` | Step-by-step behavior (numbered) | Yes |
| `## Rules` | Hard constraints and boundaries | Recommended |
| `## Anti-Patterns` | What NOT to do | Recommended |
| `## Output Format` | Expected output structure | Optional |

## Supporting Files

Skills can include additional files alongside `SKILL.md`:

| Type | Example | Purpose |
|------|---------|---------|
| Protocol | `design-protocol.md` | Multi-step procedure details |
| Rubric | `scoring-rubric.md` | Evaluation criteria and bands |
| Prompt | `spec-reviewer-prompt.md` | Sub-agent prompt templates |

Reference from SKILL.md: `See [scoring-rubric.md](scoring-rubric.md) for score bands.`

## Directory Layout

    ~/.claude/skills/{skill-name}/
      SKILL.md              # Required — frontmatter + behavior
      CREATION-LOG.md       # Required — why this skill exists
      {protocol}.md         # Optional — detailed procedures
      {rubric}.md           # Optional — scoring criteria
      {prompt}.md           # Optional — sub-agent prompts

## Pre-Commit Checklist

- [ ] `name` field matches folder name exactly
- [ ] `description` starts with "Use when..."
- [ ] Description is under 1024 characters
- [ ] `CREATION-LOG.md` exists (see [skill-creation-log-convention.md](skill-creation-log-convention.md))
- [ ] Instructions are numbered (not just bullets)
- [ ] Anti-patterns section exists for non-trivial skills
- [ ] Run `/refresh-index` to update `SKILLS-INDEX.md`
