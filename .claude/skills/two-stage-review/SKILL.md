---
name: two-stage-review
description: "Use when a subagent reports it has finished implementing a task. Run both review stages before marking the task complete."
---

# Two-Stage Review Gate

> **Both stages must PASS before a task is marked done.**
> A FAIL at either stage sends the work back to the implementer.

## When to Activate

Activate this skill when:
- A coder subagent reports implementation complete
- A fix agent reports a bug resolved
- Any agent reports "done" on a task that involves code changes

Do not activate for documentation-only changes or spec writing.

## Stage 1 — Spec Compliance Review

Spawn a spec-compliance reviewer using the prompt in
`two-stage-review/spec-compliance-prompt.md`.

Provide:
- Path to the spec file (`docs/specs/YYYY-MM-DD-{topic}-design.md`)
- List of files modified or created by the implementer
- Summary of what the implementer claims was done

The reviewer checks whether the implementation matches the spec.

**Output:** PASS or FAIL with line-level feedback.

If FAIL: return to implementer with the specific failure items.
Do not run Stage 2. The implementer fixes and re-submits.

If PASS: proceed to Stage 2.

## Stage 2 — Code Quality Review

Only runs after Stage 1 PASS.

Spawn a code-quality reviewer using the prompt in
`two-stage-review/code-quality-prompt.md`.

Provide:
- List of files modified or created
- Language/framework (so reviewer applies correct style rules)

The reviewer checks structural and quality properties of the code.

**Output:** PASS or FAIL with specific findings.

If FAIL: return to implementer with the specific findings.
The implementer fixes and re-submits both stages from Stage 1.

If PASS: the task is complete. Mark it done.

## Re-Submission Rules

- A FAIL at Stage 1 resets the entire gate — both stages run again
- A FAIL at Stage 2 resets the entire gate — both stages run again
- Max 3 re-submission cycles before escalating to the CTO
- Escalation message must include all FAIL findings from all cycles

## Anti-Patterns

- Do not skip Stage 2 because Stage 1 passed — both are mandatory
- Do not accept "mostly PASS" — it is PASS or FAIL, no partial credit
- Do not re-run only the failing stage — always restart from Stage 1
- Do not let the implementer argue about findings — fix first, dispute later
