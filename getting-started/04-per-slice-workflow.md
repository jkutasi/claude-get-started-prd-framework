# Step 4: Per-Slice Workflow

> Part of the [Getting Started](INDEX.md) roadmap. This is the index file. Load the sub-file for the phase group you are currently running.

**Every phase is MANDATORY. Skipping any phase is a CONTRACT VIOLATION.**

**USER PRESENTATION RULE: The user ONLY sees finished, fully-vetted work. ALL phases (peer review, QA swarm, whiskey team, red team, regression, UX sense check) must complete autonomously BEFORE presenting results to the user. Never defer QA to "after user reviews." Never say "contingent on user review." The CTO presents a DONE slice — not a draft waiting for validation.**

## Phase Overview

Each phase has nuclear gates. No phase may be skipped.

## Sub-Files (load by phase group)

| File | Phases | Description |
|------|--------|-------------|
| [04a-per-slice-workflow-phases-A-D.md](04a-per-slice-workflow-phases-A-D.md) | A, A.5, A.6, A.7, B, C, D | Preparation, doc bootstrap, user scope confirmation, red team pre-build, Gherkin audit, test spec, implementation, self-reflection |
| [04b-per-slice-workflow-phases-E-J.md](04b-per-slice-workflow-phases-E-J.md) | E, F, F.5, G, H, I, J, Post-Push | Peer review, QA swarm + Whiskey Team + UX sense check, runtime log check, autonomous fix verification, regression check, documentation update, gate check + user delivery, post-push verification |

## Quick Phase Reference

```
A    → Preparation (requirements review, researcher, diagrams)
A.5  → Doc Bootstrap + Diagram Review (Slice 0 only: Scribe skeleton)
A.6  → User Scope Confirmation -- MANDATORY gate (Article 19)
A.7  → Red Team + Professor Pre-Build Gate -- MANDATORY
B    → Gherkin Audit + Test Specification + Test Peer Review (Articles 17, 18)
C    → Implementation (coders only -- Nuclear Rule 1)
D    → Self-Reflection (mandatory before peer review)
E    → Peer Review (4 models, adversarial, parallel)
F    → QA Swarm + Whiskey Team + UX Sense Check (Autonomous Fix)
F.5  → Runtime Log Check (Sentry + server + DB logs) -- MANDATORY
G    → Autonomous Fix Verification + Red Team Escalation
H    → Regression Check + Implicit Behavior Regression (Nuclear Gate H)
I    → Documentation Update
J    → Gate Check + User Delivery + Post-Push
Post → Post-Push Verification (error tracker + deployment logs)
```
