# Article 19: User Scope Confirmation Protocol (Phase A.6)

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

Before Red Team reviews the plan (Phase A.7) and before any tests are written (Phase B), the CTO MUST present the slice scope to the user for explicit confirmation. This ensures the user's vision — not the AI's interpretation — drives what gets built.

#### 19a. What the CTO Presents

The CTO presents the following to the user at the end of Phase A preparation:

1. **Slice summary** — one paragraph: what this slice delivers and why
2. **Gherkin scenarios** — the acceptance scenarios in plain English (what will be tested)
3. **Per-slice diagrams** — sequence diagram(s) and focused ER diagram (if applicable)
4. **Goal Achievement Test** — the binary test that proves the slice works
5. **What changed** — if learnings from previous slices altered this slice's scope vs. the original plan, highlight what changed and why

#### 19b. User Response

- **APPROVE** → proceed to Phase A.7 (Red Team Pre-Build Gate)
- **REVISE** → user provides feedback, CTO adjusts scope and re-presents
- No iteration limit — the user decides when they are satisfied
- The user does NOT need to review test code. The Gherkin scenarios are the user-facing contract; test code quality is validated by 3-model peer review in Phase B.3.

#### 19c. Slice 0 Special Case

For Slice 0, the User Scope Confirmation covers the full project plan: user story, all slice definitions, high-level diagrams, and the overall architecture. This formalizes the Step 1e plan sign-off as a mechanical gate.

#### 19d. Why Before Red Team

If the user says "that's not what I want," Red Team has not yet wasted time reviewing the wrong plan. Red Team (Phase A.7) reviews a **user-confirmed** scope, not a speculative one. This ordering is intentional.
