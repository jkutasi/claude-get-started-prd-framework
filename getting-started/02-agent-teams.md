# Step 2: Agent Teams Architecture

> Part of the [Getting Started](INDEX.md) roadmap. Load only this file when working on setting up Agent Teams architecture.

This project uses Claude Code's **Agent Teams** for multi-agent orchestration.

**Enable:** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

### How Agent Teams Works

- **CTO Orchestrator** is the team **lead** (Opus, Delegate Mode)
- **Teammates** are persistent for the session and can **message each other horizontally** (peer-to-peer)
- Teammates spawn **ephemeral sub-agents** for focused tasks (explore, implement, review) — these do their task and die
- **One team per session, one fixed lead, no nested teams**
- Recommended: 3-5 teammates, 5-6 tasks each

### Team Structure

```
CTO Orchestrator (Lead — Opus, Delegate Mode)
│
├── Teammates (persistent, can message each other horizontally)
│   ├── Architect              — designs approach, reviews interfaces
│   ├── Backend Engineer       — backend implementation via ephemeral sub-agents
│   ├── Frontend Engineer      — frontend implementation via ephemeral sub-agents
│   └── QA Lead                — coordinates ALL QA (see below)
│
├── Optional Teammates (add based on project needs)
│   ├── Data Engineer          — for data-heavy projects (pipelines, ETL, schemas)
│   └── Documentation Scribe   — for doc-heavy projects (otherwise CTO/Architect handles)
│
├── Quality Gate Agents (ephemeral, spawned by teammates per phase)
│   ├── Peer Review: Gemini, OpenAI Codex, Grok reviewers (+ Greptile if configured)
│   ├── QA Swarm: Stats, Code Quality, Data Integrity, Security, UI/UX
│   ├── Red Team Reviewer       — 10 attack dimensions, pre-build gate
│   ├── Whiskey Team            — adversarial QA + implicit regression
│   ├── UX Sense Check          — persona-based browser testing
│   └── QA Manager              — formats findings (formatting sub-agent only)
│
└── Domain Specialists (ephemeral, on-demand per project)
    └── {Project-specific roles}
```

### QA Hierarchy (Everything Under QA Lead)

QA Lead coordinates ALL quality testing:

```
QA Lead (persistent teammate)
├── Test-Writer Sub-Agents -- write ALL tests in Phase B (separate from coders)
├── Standard QA Swarm -- Stats, Code Quality, Data Integrity, Security, UI/UX
├── Red Team Reviewer -- pre-build gate + QA escalation
├── Whiskey Team -- adversarial QA + implicit behavior regression
├── UX Sense Check -- persona-based browser testing
└── QA Manager -- formats findings into artifact (formatting sub-agent only)
```
