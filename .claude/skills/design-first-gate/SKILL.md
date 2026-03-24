---
name: design-first-gate
description: "Use when about to implement a new feature, refactor, or any change touching more than one file. Enforces design-before-code discipline."
---

# Design-First Gate

> **Hard gate. No implementation begins until a spec exists and has been approved.**

## What Counts as Non-Trivial

Block on spec if ANY of these apply:
- Change touches more than 1 file
- User description leaves open questions that would require guessing
- New endpoint, new data model, new UI component, or cross-cutting concern
- Refactor that changes interfaces or moves responsibilities

Single-file typo fixes and isolated string changes are exempt.

## Protocol

Full protocol is in `design-first-gate/design-protocol.md`.

**Short version:**

1. Check for spec at `docs/specs/YYYY-MM-DD-{topic}-design.md`
2. No spec? Enter brainstorm mode — one question at a time, YAGNI applied
3. Write spec to `docs/specs/YYYY-MM-DD-{topic}-design.md`
4. Spawn spec-reviewer subagent (prompt: `design-first-gate/spec-reviewer-prompt.md`)
5. Iterate on spec (max 3 rounds) until reviewer returns APPROVED
6. Hand off to implementation only after APPROVED

## Gate Conditions That BLOCK Implementation

| Condition | Action |
|-----------|--------|
| No spec file exists | Create one — do not skip |
| Spec exists, reviewer not yet run | Run spec reviewer |
| Spec exists, reviewer returned NEEDS_REVISION | Revise and re-review |
| Spec is from a prior session, scope has changed | Update spec, re-review |

## Spec File Naming

```
docs/specs/YYYY-MM-DD-{topic}-design.md
```

Use today's date. Use kebab-case for topic. Examples:
- `docs/specs/2026-03-24-user-auth-design.md`
- `docs/specs/2026-03-24-payment-webhook-design.md`

## Anti-Patterns

- Do not start writing code and say "I'll document later"
- Do not skip the spec reviewer because the spec "seems obvious"
- Do not accept a vague user description as a spec
- Do not ask multiple questions at once — one question per turn
- Do not over-engineer the spec — YAGNI is mandatory, not optional
