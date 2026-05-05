# Per-Slice Development Workflow

> **Loaded from CLAUDE.md on demand.** This file is the index for the full phase-by-phase workflow for each slice. The CTO loads the relevant sub-file at the start of each phase group and follows it step by step.

**CRITICAL: Every phase is MANDATORY. Skipping any phase is a CONTRACT VIOLATION.**
**REMINDER: You are the CTO Orchestrator. You spawn teammates and sub-agents for ALL implementation.**

**USER PRESENTATION RULE: The user ONLY sees finished, fully-vetted work. ALL phases (peer review, QA swarm, whiskey team, red team, regression, UX sense check) must complete autonomously BEFORE presenting results to the user. Never defer QA to "after user reviews." Never say "contingent on user review." The CTO presents a DONE slice — not a draft waiting for validation.**

## Phase Overview

Each phase has nuclear gates. No phase may be skipped. The gate check script at Phase J is the mechanical enforcement mechanism — run it.

## Sub-Files (load by phase group)

| File | Phases | Description |
|------|--------|-------------|
| [PER-SLICE-WORKFLOW-PHASES-A-D.md](PER-SLICE-WORKFLOW-PHASES-A-D.md) | A, A.5, A.6, A.7, B, C, D | Preparation, doc bootstrap, user scope confirmation, red team pre-build, Gherkin audit, test spec, implementation, self-reflection |
| [PER-SLICE-WORKFLOW-PHASES-E-H.md](PER-SLICE-WORKFLOW-PHASES-E-H.md) | E, F, F.5, G, H | Peer review (4 models), QA swarm + Whiskey Team + UX sense check, runtime log check, autonomous fix verification, regression check |
| [PER-SLICE-WORKFLOW-PHASES-I-POST-PUSH.md](PER-SLICE-WORKFLOW-PHASES-I-POST-PUSH.md) | I, J, Post-Push | Documentation update, gate check + user delivery, post-push error tracker verification |

## Quick Phase Reference

```
A    → Preparation (requirements review, researcher, diagrams)
A.5  → Doc Bootstrap + Diagram Review (Slice 0 only: Scribe skeleton)
A.6  → User Scope Confirmation -- MANDATORY gate (Article 19)
A.7  → Red Team + Professor Pre-Build Gate (Article 14a) -- MANDATORY
B    → Gherkin Audit + Test Specification + Test Peer Review (Articles 17, 18)
C    → Implementation (coders only -- Nuclear Rule 1)
D    → Self-Reflection + Error & Rescue Registry (Article 35)
E    → Peer Review (4 models, adversarial, parallel)
F    → QA Swarm + Whiskey Team + UX Sense Check (Autonomous Fix)
F.5  → Runtime Log Check (Sentry + server + DB logs) -- MANDATORY
G    → Autonomous Fix Verification + Red Team Escalation
H    → Regression Check + Implicit Behavior Regression (Nuclear Gate H)
I    → Documentation Update
J    → Gate Check + User Delivery + Post-Push
Post → Post-Push Verification (error tracker + deployment logs)
```

**If you are reading this and considering skipping the gate check script: DON'T. The script exists specifically because the CTO has demonstrated a tendency to skip reviews and move forward. The script is a mechanical check that cannot be rationalized away. Run it.**
