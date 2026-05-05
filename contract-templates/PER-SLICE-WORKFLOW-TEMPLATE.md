# Per-Slice Development Workflow

> **Loaded from CLAUDE.md on demand.** This file is the index for the full phase-by-phase workflow for each slice. The CTO loads the relevant sub-file at the start of each phase group and follows it step by step.

**CRITICAL: Every phase is MANDATORY. Skipping any phase is a CONTRACT VIOLATION.**
**REMINDER: You are the CTO Orchestrator. You spawn teammates and sub-agents for ALL implementation.**

**USER PRESENTATION RULE: The user ONLY sees finished, fully-vetted work. ALL phases (peer review, QA swarm, UX sense check, A.7 red team if --high-risk) must complete autonomously BEFORE presenting results to the user. Never defer QA to "after user reviews." Never say "contingent on user review." The CTO presents a DONE slice — not a draft waiting for validation.**

## Phase Overview

Each phase has nuclear gates. No phase may be skipped. The gate check script at Phase J is the mechanical enforcement mechanism — run it.

## Sub-Files (load by phase group)

| File | Phases | Description |
|------|--------|-------------|
| [PER-SLICE-WORKFLOW-PHASES-A-C.md](PER-SLICE-WORKFLOW-PHASES-A-C.md) | A, A.5, A.6, A.7, B, C | Preparation, doc bootstrap, user scope confirmation, red team pre-build (optional), test spec + peer review, implementation |
| [PER-SLICE-WORKFLOW-PHASES-E-F5.md](PER-SLICE-WORKFLOW-PHASES-E-F5.md) | E, F, F.5 | Peer review (4 models), QA swarm + UX sense check, automated Sentry log check |
| [PER-SLICE-WORKFLOW-PHASES-I-POST-PUSH.md](PER-SLICE-WORKFLOW-PHASES-I-POST-PUSH.md) | I, J, Post-Push | Documentation update, gate check + user delivery + Playwright regression, post-push Sentry verification |

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

**If you are reading this and considering skipping the gate check script: DON'T. The script exists specifically because the CTO has demonstrated a tendency to skip reviews and move forward. The script is a mechanical check that cannot be rationalized away. Run it.**
