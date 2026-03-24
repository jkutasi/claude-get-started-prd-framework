# CREATION-LOG — design-first-gate

## Problem

Agents were jumping directly from a vague user request to implementation,
making assumptions about scope, approach, and acceptance criteria. This
produced code that solved the wrong problem or over-engineered a simple
one. Rework was expensive because the misalignment was only visible after
implementation was complete.

## Observed Failures Before This Skill

- Agent built a full pagination system when the user wanted "show 10 rows."
- Refactor created new abstraction layers that weren't in the original request,
  causing downstream agents to fail against unexpectedly changed interfaces.
- User said "add auth" — agent implemented OAuth2 + RBAC when a session cookie
  would have been sufficient.
- Scope crept mid-implementation when agent encountered something "while I'm
  in there anyway."

## Approaches Tried and Rejected

**Approach: Rely on user to write spec before asking.**
Rejected: Users rarely write specs unprompted. The gate only works if the
agent enforces it, not if it depends on user discipline.

**Approach: Ask all clarifying questions at once.**
Rejected: Multi-question prompts overwhelm users and produce low-quality
answers. One question per turn with a preferred multiple-choice format
produces better signal.

**Approach: Allow implementation to proceed while spec is being written.**
Rejected: Parallel spec + code produces code that then shapes the spec,
defeating the purpose. The gate must be hard.

## Design Decisions

1. Hard gate, not advisory: the skill explicitly blocks implementation, not
   just recommends slowing down. The BLOCK language is intentional.
2. YAGNI as a mandatory lens, not a nice-to-have: applied during brainstorm
   AND reviewed by the spec-reviewer.
3. Max 3 review rounds: prevents infinite spec-polishing loops. After round 3,
   escalate to owner.
4. Scope change invalidates approval: a spec approved in a previous session
   is not valid if the user has changed what they want.

## Pressure Scenarios This Skill Handles

- "Just make a quick change" — still non-trivial if it touches multiple files.
- "We discussed this yesterday, just do it" — spec still required; memory is
  not a spec.
- "I'll describe the rest as we go" — brainstorm mode surfaces the unknowns
  before code starts, not during.
- "The spec is in my head, trust me" — the spec must be in a file at
  `docs/specs/`. Agent trust is not a substitute.
