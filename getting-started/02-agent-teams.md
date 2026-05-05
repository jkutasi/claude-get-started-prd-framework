# Step 2: Agent Teams Architecture

> Part of the [Getting Started](INDEX.md) roadmap. Load only this file when working on setting up Agent Teams architecture.

This project uses Claude Code's **Agent Teams** for multi-agent orchestration. **Agents are thin role shells (WHO). Skills carry the behavior (HOW).** Agent files (`.claude/agents/`) define identity and permissions; skill files (`.claude/skills/`) define protocols and checklists.

**Enable:** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

### How Agent Teams Works

- **CTO Orchestrator** is the team **lead** (Opus, Delegate Mode)
- **Teammates** are persistent for the session and can **message each other horizontally** (peer-to-peer)
- Teammates spawn **ephemeral sub-agents** for focused tasks (explore, implement, review) — these do their task and die
- **One team per session, one fixed lead, no nested teams**
- Recommended: 3-5 teammates, 5-6 tasks each

### Team Structure

```
CTO Orchestrator (Lead — Opus, skills: cto-orchestrator, slice-workflow)
│
├── Teammates (persistent, can message each other horizontally)
│   ├── Architect              — skills: prof-architecture
│   ├── Backend Engineer       — agent: coder, skills: coder-backend
│   ├── Frontend Engineer      — agent: coder, skills: coder-frontend
│   └── QA Lead                — agent: qa-tester, skills: qa-lead
│
├── Optional Teammates (add based on project needs)
│   ├── Data Engineer          — for data-heavy projects (pipelines, ETL, schemas)
│   └── Documentation Scribe   — for doc-heavy projects (otherwise CTO/Architect handles)
│
├── Quality Gate Agents (ephemeral, spawned by teammates per phase)
│   ├── Peer Review: Gemini, OpenAI 5.5 (Responses API), Claude Opus 4.7, Grok (4 models, adversarial)
│   ├── QA Swarm: Stats, Code Quality, Data Integrity, Security, UI/UX
│   ├── Red Team Reviewer       — 10 attack dimensions, pre-build gate
│   ├── Professors              — domain expert review (Architecture, Testing, Security, etc.)
│   ├── Whiskey Team            — adversarial QA + implicit regression
│   ├── UX Sense Check          — persona-based browser testing
│   └── QA Manager              — formats findings (formatting sub-agent only)
│
└── Domain Specialists (ephemeral, on-demand per project)
    └── {Project-specific roles}
```

### MCP Agent Architecture

MCP calls **MUST** be delegated to subagents. Never call an MCP tool directly from the main conversation context.

**Why:** MCP responses can be massive (error traces, query results, full PR diffs). A subagent processes the raw data and returns only what matters — keeping the main agent's context clean for actual development work.

**Pattern:**
```
Main agent spawns subagent with specific question
  → Subagent calls the MCP tool
  → Subagent extracts the answer
  → Subagent returns concise summary (under 500 tokens) to parent
```

**Rules:**
1. **One MCP call per subagent** — keeps subagent context focused
2. **Subagent prompt must specify what to extract** — not open-ended queries
3. **Multiple MCP calls within one subagent are fine if related** (e.g., list then get details)
4. **Never pass raw MCP responses back to the parent** — always summarize

This follows the same pattern as the CTO orchestrator: **delegate, never do work yourself.**

> See `.claude/skills/relay-mcp-pattern/SKILL.md` for the full relay agent skill template.

### QA Hierarchy (Everything Under QA Lead)

QA Lead coordinates ALL quality testing:

```
QA Lead (persistent teammate)
├── Test-Writer Sub-Agents -- write ALL tests in Phase B (separate from coders)
├── Standard QA Swarm -- Stats, Code Quality, Data Integrity, Security, UI/UX
├── Red Team Reviewer -- pre-build gate + QA escalation
├── Professors -- domain expert review at pre-build + QA escalation gates
├── Whiskey Team -- adversarial QA + implicit behavior regression
├── UX Sense Check -- persona-based browser testing
└── QA Manager -- formats findings into artifact (formatting sub-agent only)
```
