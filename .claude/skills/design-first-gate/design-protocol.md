# Design-First Gate — Detailed Protocol

## Step 1: Spec Existence Check

Before any implementation work, check:

```
docs/specs/YYYY-MM-DD-{topic}-design.md
```

Use Glob to search: `docs/specs/*{topic}*-design.md`

If a matching file exists, verify:
- [ ] Spec covers the current request's scope
- [ ] Spec has not been superseded by scope changes from the user
- [ ] Spec has reviewer approval recorded (look for `APPROVED` at the bottom)

If all three pass, skip to Step 5 (hand off to implementation).

If the spec exists but scope has changed, treat it as missing — go to Step 2.

## Step 2: Brainstorm Mode (Spec Does Not Exist)

Enter brainstorm mode. Do not start writing code. Do not write a spec yet.

**Rules for brainstorm mode:**
- Ask ONE question per turn. Never bundle questions.
- Prefer multiple-choice answers. Reduce cognitive load.
- Apply YAGNI ruthlessly: "Do we actually need this now?" is always a valid question.
- Stop asking when you can answer: What is the problem? What is the solution boundary?
  What does done look like? What is explicitly out of scope?

**Minimum information before writing the spec:**
1. Problem statement — what breaks or is missing today?
2. Solution boundary — what will this change, and what will it NOT touch?
3. Success criteria — how do we know it worked? (Must be measurable.)
4. Out-of-scope items — at least two things explicitly excluded.
5. Tech approach — which files, which patterns, which dependencies?

## Step 3: Write the Spec

File path: `docs/specs/YYYY-MM-DD-{topic}-design.md`

Use this structure:

```markdown
# {Topic} Design

**Date:** YYYY-MM-DD
**Status:** DRAFT

## Problem
One paragraph. What is broken or missing?

## Solution Boundary
**In scope:**
- Item 1
- Item 2

**Out of scope:**
- Item A
- Item B

## Success Criteria
- [ ] Criterion 1 (measurable)
- [ ] Criterion 2 (measurable)

## Tech Approach
Which files are created, modified, or deleted. Which patterns are used.
No more than 10 bullet points. YAGNI: if unsure, leave it out.

## Open Questions
List any remaining unknowns. Leave empty if none.

---
_Reviewer verdict:_ (filled in by spec-reviewer subagent)
```

## Step 4: Spec Review

Spawn a spec-reviewer subagent using the prompt in
`design-first-gate/spec-reviewer-prompt.md`.

Pass the spec file path as input. The reviewer returns either:
- `APPROVED` — proceed to Step 5
- `NEEDS_REVISION: {items}` — revise the spec and re-run the reviewer

**Max 3 review rounds.** If still NEEDS_REVISION after round 3, escalate
to the project owner with the blocking items clearly listed.

After approval, update the spec's `_Reviewer verdict:_` line to `APPROVED`.

## Step 5: Hand Off to Implementation

Only after a spec file exists with `APPROVED` verdict:
- Reference the spec file path when spawning implementation agents
- Implementation agents must stay within the spec's scope
- Any out-of-scope request during implementation is a new feature —
  it requires its own spec
