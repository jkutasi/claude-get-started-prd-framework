---
name: slice-workflow
description: "Use when starting or continuing a vertical slice through Phases A through J."
custom-agent: cto
disable-model-invocation: true
---

# Slice Workflow Orchestrator

> **Every phase is MANDATORY. Skipping any phase is a CONTRACT VIOLATION.**

## Phase Sequence

```
A → A.5 → A.6 → A.7 → B → C → D → E → F → F.5 → G → H → I → I.5 → J → Post-Push
```

| Phase | Name | Sub-File | Human Checkpoint? |
|-------|------|----------|-------------------|
| A | Preparation | `phases/phase-a-preparation.md` | No |
| A.5 | Doc Bootstrap | `phases/phase-a5-doc-bootstrap.md` | No |
| A.6 | User Scope Confirmation | `phases/phase-a6-user-scope.md` | **YES** |
| A.7 | Red Team + Professor Pre-Build | `phases/phase-a7-red-team.md` | No |
| B | Test Specification | `phases/phase-b-test-spec.md` | No |
| C | Implementation | `phases/phase-c-implementation.md` | No |
| D | Self-Reflection | `phases/phase-d-self-reflection.md` | No |
| E | Peer Review | `phases/phase-e-peer-review.md` | No |
| F | QA Swarm | `phases/phase-f-qa-swarm.md` | No |
| F.5 | Runtime Log Check | `phases/phase-f5-runtime-log-check.md` | No |
| G | Autonomous Fix | `phases/phase-g-autonomous-fix.md` | No |
| H | Regression | `phases/phase-h-regression.md` | No |
| I | Documentation | `phases/phase-i-documentation.md` | No |
| I.5 | User Delivery | `phases/phase-i5-user-delivery.md` | **YES** |
| J | Gate Check | `phases/phase-j-gate-check.md` | No |
| Post-Push | Post-Push Verification | `phases/phase-j-gate-check.md` (section 2) | No |

## How to Use

1. **Load only the current phase's sub-file.** Do not read ahead.
2. Complete every checklist and gate in the phase file before moving on.
3. If a gate FAILS, stop. Fix the issue within that phase. Do not advance.
4. At Human Checkpoints (A.6, I.5), present to the user and wait for response.

## Between-Phase Rules

- **No skipping.** Every phase is mandatory. Skipping = contract violation.
- **Present summary.** After completing each phase, log a one-line status before loading the next phase file.
- **Stop on failure.** If any gate check fails, you remain in that phase until it passes. Max 3 retry cycles before escalating to user.
- **Autonomous completion.** The user only sees finished, fully-vetted work. All reviews, QA, and fixes complete autonomously BEFORE presenting to the user.

## Nuclear Rules Reference

The 10 Nuclear Rules in `getting-started/00-nuclear-rules.md` override everything. Key rules for the workflow:

- **Rule 1:** CTO never writes code — delegate to sub-agents/teammates.
- **Rule 2:** Peer review is mandatory — every slice, every time.
- **Rule 3:** Slices ship complete — all gates passed, all artifacts exist.
- **Rule 7:** Never commit without checking runtime errors.
- **Rule 8:** Slices ship one at a time — no parallel slices.

## Gate Check Requirements

Every phase with a gate block (`+---------+`) must have ALL items checked before proceeding. The final gate (Phase J) runs `gate_check.py` to mechanically verify all review artifacts exist on disk:

- `reviews/slice-N-test-spec.md`
- `reviews/slice-N-test-review.md`
- `reviews/slice-N-peer-review.md`
- `reviews/slice-N-qa-swarm.md`
- `reviews/slice-N-red-team-pre-build.md`
- `reviews/slice-N-professor-pre-build.md`
- `reviews/slice-N-whiskey-team.md`
- `reviews/slice-N-ux-sense-check.md` (if frontend)
- `reviews/slice-N-red-team.md` (if escalation triggered)
- `reviews/slice-N-professor.md` (if escalation triggered)

## Review Templates

Review output templates are in `review-templates/` within this skill directory. Use the appropriate template when producing review artifacts.

## User Presentation Rule

The user ONLY sees finished, fully-vetted work. ALL phases (peer review, QA swarm, whiskey team, red team, regression, UX sense check) must complete autonomously BEFORE presenting results. Never defer QA to "after user reviews." The CTO presents a DONE slice — not a draft.
