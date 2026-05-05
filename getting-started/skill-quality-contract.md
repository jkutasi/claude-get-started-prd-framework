# Skill Quality Contract

> Part of the [Getting Started](INDEX.md) roadmap. Load when creating a new skill, auditing an existing one, or scoping which skills a project needs.

## Purpose

This contract defines what makes a Claude Code skill **robust enough for an agent to invoke without supervision**. It applies to every new skill created in this template and is the audit bar for every existing skill in the library. After a project's stack is scoped, every required skill is enumerated and every gap is filled before any feature code is written. A skill that does not meet this bar is **non-conforming** and must be upgraded or split before next use. See [skill-quality-contract-appendix.md](skill-quality-contract-appendix.md) for the full anti-pattern catalogue, the example skill, and the audit script outline.

## The 8 Required Sections

Every `SKILL.md` MUST contain all eight sections below. A missing or thin section fails the audit.

| # | Section | Required Content | Why |
|---|---------|------------------|-----|
| 1 | **Trigger / When-to-use** | Explicit "Use when X" AND "Do not use when Y" clauses | Prevents the wrong skill firing on ambiguous prompts |
| 2 | **Inputs** | What context, files, or parameters the calling agent must supply | Eliminates guesswork; surfaces missing context up front |
| 3 | **Procedure** | Numbered atomic steps — one verb, one action per step | Makes the skill replayable, debuggable, auditable |
| 4 | **Outputs** | Exact shape of the produced artifact (report, diff, recommendation) | Calling agent knows what to expect and how to consume it |
| 5 | **Tool surface** | Which tools the skill is allowed to use (`Read`, `Edit`, `Bash`, MCP refs, etc.) | Mirrors the `allowed-tools` frontmatter and bounds blast radius |
| 6 | **Anti-patterns** | At least 3 named failure modes the skill must refuse | Encodes hard-won lessons; stops repeat mistakes |
| 7 | **Examples** | At least 1 concrete invocation + expected output | Removes ambiguity in trigger interpretation |
| 8 | **Verification checklist** | How the calling agent confirms the skill ran correctly | Closes the loop — the caller can self-check, no human needed |

## Frontmatter Requirements

Every `SKILL.md` MUST open with YAML frontmatter containing at minimum:

    ---
    name: kebab-case-name           # MUST match folder name exactly
    description: "Use when ..."     # MUST start with "Use when"; ≤1024 chars; trigger-only
    allowed-tools: Read, Grep, Bash # Comma-separated; bounds tool surface
    ---

Optional fields (`custom-agent`, `context: fork`, `agent`, `disable-model-invocation`) follow the patterns in [skill-v2-creation-guide.md](skill-v2-creation-guide.md). The `description` field carries the **trigger** and is what Claude Code uses for auto-discovery — it is NOT a role summary.

## Structural Rules

| Rule | Enforcement |
|------|-------------|
| **150-line file limit** | Applies to `SKILL.md` itself. If the skill needs more, split into `SKILL.md` (≤150) plus companion files (`TOOLS.md`, `PATTERNS.md`, `PROTOCOL.md`) cross-linked with relative paths. |
| **Atomic — one skill = one job** | Megaskills are forbidden. If a skill's procedure spans more than one outcome, split it. A skill that "does QA AND deploys AND notifies" is three skills. |
| **Self-contained** | Skills MUST NOT depend on undocumented external scripts. Any helper script (`gate_check.py`, `verify.sh`, etc.) must be listed in the **Tool surface** section and live alongside `SKILL.md` or in the project's documented script directory. |
| **No external secrets in skill body** | API keys, tokens, and DSNs live in `.env` and are referenced by variable name only. |
| **Frontmatter parses** | YAML must be valid. `name` must match folder. `description` must start with `Use when`. |

## Authoring Procedure (use this order)

1. Write the **trigger** first. If you cannot express it as one "Use when X" sentence plus one "Do not use when Y" sentence, the skill is not atomic — split it.
2. List the **inputs** the caller must supply. If any input is "the agent figures it out," promote it to an explicit input.
3. Write the **procedure** as numbered atomic steps. One verb per step. No conditional branches inside a single step — split into two.
4. Specify the **output** shape with a literal example block (e.g., the JSON, the markdown table, the diff fences).
5. Declare the **tool surface** and mirror it exactly in the YAML `allowed-tools`.
6. Enumerate **anti-patterns** — at least 3, drawn from real failure modes (see appendix catalogue).
7. Add at least one **example** invocation showing the trigger context and the verbatim expected output.
8. Write the **verification checklist** as a bulleted list the caller can mechanically tick off.
9. Run the audit checklist (below). Fix any gaps before committing.

## Audit Checklist (use to gate new skills AND audit existing ones)

- [ ] All 8 required sections present and non-empty
- [ ] Frontmatter has `name`, `description` (starts with `Use when`), `allowed-tools`
- [ ] `name` matches folder name; folder lives under `~/.claude/skills/` or `.claude/skills/`
- [ ] `SKILL.md` is ≤150 lines; oversized content lives in companion files
- [ ] Skill is atomic — one trigger, one job, one output shape
- [ ] At least 3 named anti-patterns
- [ ] At least 1 concrete example with verbatim expected output
- [ ] Verification checklist is mechanical (caller can tick boxes without judgment calls)
- [ ] No undocumented external scripts referenced
- [ ] `CREATION-LOG.md` exists in the skill folder (see [skill-creation-log-convention.md](skill-creation-log-convention.md))

A skill failing **any** checkbox is non-conforming. Do not invoke it; upgrade or split it first.

## When to Use This Contract

| Trigger | Action |
|---------|--------|
| Project stack is scoped, skill list being enumerated | Every required skill must conform before any feature code is written |
| Existing skill triggers but produces inconsistent output | Audit against the 8 sections; the failure is almost always a missing one |
| Drafting a new skill | Follow the Authoring Procedure in order; do not skip steps |
| Two skills overlap or one skill grew megaskill scope | Split using the atomicity rule |

## Canonical Examples

The Vercel, Railway, and Sentry skills built later in this template will be the canonical reference implementations. Once they exist, link them here. Until then, see [skill-quality-contract-appendix.md](skill-quality-contract-appendix.md) for an abstract skeleton example.

## Related

- [skill-v2-creation-guide.md](skill-v2-creation-guide.md) — frontmatter and body structure reference
- [skill-creation-log-convention.md](skill-creation-log-convention.md) — required `CREATION-LOG.md` format
- [skill-lifecycle-workflow.md](skill-lifecycle-workflow.md) — find / create / promote / combine skills
- [skill-description-audit.md](skill-description-audit.md) — historical audit of the `description` field rule
