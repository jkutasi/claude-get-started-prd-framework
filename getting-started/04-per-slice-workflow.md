# Step 4: Per-Slice Workflow

> Part of the [Getting Started](INDEX.md) roadmap. This is the index file. Load the sub-file for the phase group you are currently running.

**Every phase is MANDATORY. Skipping any phase is a CONTRACT VIOLATION.**

**USER PRESENTATION RULE: The user ONLY sees finished, fully-vetted work. ALL phases (peer review, QA swarm, UX sense check, A.7 red team if --high-risk) must complete autonomously BEFORE presenting results to the user. Never defer QA to "after user reviews." Never say "contingent on user review." The CTO presents a DONE slice — not a draft waiting for validation.**

## Phase Overview

Each phase has nuclear gates. No phase may be skipped.

## Sub-Files (load by phase group)

| File | Phases | Description |
|------|--------|-------------|
| [04a-per-slice-workflow-phases-A-C.md](04a-per-slice-workflow-phases-A-C.md) | A, A.5, A.6, A.7, B, C | Preparation, doc bootstrap, user scope confirmation, red team pre-build (optional --high-risk), test spec + peer review, implementation |
| [04b-per-slice-workflow-phases-E-POST-PUSH.md](04b-per-slice-workflow-phases-E-POST-PUSH.md) | E, F, F.5, I, J, Post-Push | Peer review, QA swarm + UX sense check, automated Sentry check, documentation update, gate check + user delivery + Playwright regression, post-push Sentry verification |

## Quick Phase Reference

```
A    → Preparation (requirements review, researcher, diagrams)
A.5  → Doc Bootstrap + Diagram Review (Slice 0 only: Scribe skeleton)
A.6  → User Scope Confirmation -- MANDATORY gate (Article 19)
A.7  → Red Team + Professor Pre-Build Gate -- OPTIONAL (--high-risk only)
B    → Gherkin Audit + Test Specification + Test Peer Review (Articles 17, 18)
C    → Implementation (coders only -- Nuclear Rule 1)
E    → Peer Review (4 models, adversarial, parallel)
F    → QA Swarm + UX Sense Check (Autonomous Fix via OpenAI 5.5)
F.5  → Automated Sentry Check (relay-sentry MCP polling) -- MANDATORY
I    → Documentation Update
J    → Gate Check + User Delivery + Playwright Regression Smoke
Post → Post-Push Verification (relay-sentry MCP + deployment logs)
```
