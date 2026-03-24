# Skill Creation Log Convention

> Part of the [Getting Started](INDEX.md) roadmap.

## What Is a CREATION-LOG?

Every skill directory should contain a `CREATION-LOG.md` alongside its `SKILL.md`.

The creation log is an honest account of why the skill was built, what went
wrong before it existed, and what design decisions were made (and rejected)
during its creation.

It is not a changelog. It is not a readme. It is a failure-mode record.

## Why This Convention Exists

Skills can be misunderstood, undermined, or deleted when future authors
do not know what problem they solve. A skill that looks "optional" or
"over-engineered" often has a specific failure mode behind it that is not
visible in the SKILL.md protocol alone.

The creation log prevents the cycle of:
1. Pain exists
2. Skill is created to address pain
3. Time passes, context is lost
4. Skill is removed as "unnecessary overhead"
5. Pain returns

## Required Sections

Every CREATION-LOG.md must include these four sections:

### Problem
What was broken, missing, or painful before this skill existed?
One to three paragraphs. Be specific — give examples of real failures, not
abstract descriptions of what could go wrong.

### Observed Failures
List the actual failure modes that were observed. Three to six concrete
examples. Each example should describe what happened, not just what could
happen.

### Design Decisions
For each significant decision in the skill's design, explain:
- What was decided
- What alternatives were considered and why they were rejected
- Why this approach was chosen

This section is especially important for rules that seem arbitrary or strict.
The "why" belongs here.

### Pressure Scenarios
List three to six specific scenarios where someone might be tempted to
bypass or skip this skill. For each, show what the outcome would be if
bypassed. These are the cases the skill was specifically designed to handle.

## Living Document Rule

A CREATION-LOG.md is updated whenever the skill is updated.

When you change a skill:
- Add a note under the relevant section about what changed and why
- If the change was triggered by a new observed failure, add it to
  Observed Failures
- If the change reversed an earlier design decision, document both the
  original reason and the reason for reversal

## Template

Use the template at `.claude/skills/CREATION-LOG-TEMPLATE.md` when creating
a new skill.

## Which Skills Need This

All skills in `.claude/skills/` that encode non-obvious rules or constraints.
Simple relay or utility skills (e.g., relay-qmd) may omit the log if the
skill is a thin wrapper with no behavioral rules.

When in doubt, write the log. The cost is low; the benefit is preserved context.
