# Agent Teams Architecture — {PROJECT_NAME}

> **Loaded on demand.** The CTO loads this file at session start to understand the team structure. Do not keep in memory after internalizing the roster.

This project uses **Claude Code Agent Teams** with the environment variable:

```
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

Agent Teams enables **persistent teammates** that run as parallel Claude Code instances. Teammates can message each other **horizontally** — they do not need to route all communication through the CTO. This is fundamentally different from flat sub-agent spawning.

## Agents vs. Skills

**Agents are WHO** — thin role shells in `.claude/agents/` that define identity, model, and tool permissions.

**Skills are HOW** — behavior modules in `.claude/skills/` that define protocols, checklists, anti-patterns, and output formats.

When the CTO spawns a teammate or sub-agent, it picks an **agent** (for identity/permissions) and a **skill** (for behavior/instructions). The agent file's `skills:` field lists which skills that agent is designed to run. Skills carry the substance; agents carry the shell.

## How to Spawn Teammates and Sub-Agents

**Teammates (persistent):**
- Teammates are persistent agents that remain active across the session
- They can send messages to each other directly (horizontal communication)
- Use teammates for ongoing roles: Architect, Backend Engineer, Frontend Engineer, etc.
- Teammates maintain their own context and state

**Sub-agents (ephemeral):**
- Sub-agents are spawned by teammates (or the CTO) for one-shot focused tasks
- They complete their task, return a result, and are destroyed
- Use sub-agents for: single function implementation, single review, single QA check
- Sub-agents do NOT persist and cannot be messaged after completion

Every implementation task follows this pattern:

1. Define the task scope (one function, one component, one query — keep it small)
2. Assign to the appropriate teammate, or have the teammate spawn a sub-agent with:
   - The relevant skill file from `.claude/skills/`
   - The relevant slice spec from `slices/`
   - Clear acceptance criteria
3. Teammate/sub-agent implements (Phase C) or writes tests (Phase B), returns completion report
4. CTO reviews the report, NOT the raw code (context window conservation)
5. If issues found, assign fix to a teammate or have them spawn a new sub-agent (do NOT fix directly)

## Teammate Roster

Opus is reserved EXCLUSIVELY for the CTO. All teammates and sub-agents use Sonnet.

| Teammate | Model | Persistent? | Primary Skills | Purpose |
|----------|-------|-------------|---------------|---------|
| **CTO Orchestrator** | Opus | Yes (main session) | `/cto-orchestrator`, `/slice-workflow` | Orchestration, decisions, synthesis (YOU) |
| **Architect** | Sonnet | Yes | `/prof-architecture` | System design, schema decisions, dependency management |
| **Backend Engineer** | Sonnet | Yes | `/coder-backend` | Backend modules, queries, business logic, API endpoints |
| **Frontend Engineer** | Sonnet | Yes | `/coder-frontend` | UI components, pages, client-side logic, styling |
| **QA Lead** | Sonnet | Yes | `/qa-lead` | Coordinates QA swarm, synthesizes findings, manages QA sub-agents |

**Optional teammates** (add based on project needs — recommended for data-heavy or doc-heavy projects):

| Teammate | Model | When to Add |
|----------|-------|-------------|
| **Data Engineer** | Sonnet | Projects with complex data pipelines, ETL, query optimization, or dedicated schema management |
| **Documentation Scribe** | Sonnet | Projects with extensive documentation requirements. Otherwise, the CTO or Architect handles doc updates. |

**Note:** The default team is 4 persistent teammates + CTO (within the recommended 3-5 range). Teammates can message each other horizontally. For example, the Backend Engineer can message the Architect directly about a schema question without routing through the CTO. Sub-agents spawned BY teammates are ephemeral — they complete one focused task and are destroyed.

## Quality Gate Agents (Ephemeral Sub-Agents — Spawned by Teammates)

| Sub-Agent | Spawned By | Model | Purpose |
|-----------|-----------|-------|---------|
| **Peer Review Coordinator** | CTO / QA Lead | Sonnet | Orchestrates parallel peer review across external models |
| **Reviewer Gemini** | Peer Review Coordinator | Sonnet + Gemini API | Peer review perspective #1 |
| **Reviewer OpenAI Codex** | Peer Review Coordinator | Sonnet + OpenAI Codex CLI | Peer review perspective #2 |
| **Reviewer Grok** | Peer Review Coordinator | Sonnet + Grok API | Peer review perspective #3 |
| **Reviewer Greptile** (optional) | Peer Review Coordinator | Sonnet + Greptile API | Codebase-aware peer review #4 (only if `GREPTILE_API_KEY` configured) |
| **QA Stats** | QA Lead | Sonnet | Math correctness, algorithm validation |
| **QA Code Quality** | QA Lead | Sonnet | Patterns, linting, DRY, naming |
| **QA Data Integrity** | QA Lead | Sonnet + data MCP | Queries, schemas, data correctness |
| **QA Security** | QA Lead | Sonnet | OWASP, keys, injection, XSS |
| **QA UI/UX + Browser** | QA Lead | Sonnet + agent-browser | Accessibility, responsive, browser compat |
| **Red Team Reviewer** | QA Lead | Sonnet + external model | 10-dimension adversarial review (Article 14) |
| **Whiskey Team** | QA Lead | Sonnet + agent-browser | Adversarial QA, 8 test areas, implicit regression (Article 15) |
| **UX Sense Check** | QA Lead | Sonnet + agent-browser | Persona-based UX testing (Article 16) |

## Domain Specialists (Ephemeral — Spawned On Demand)

| Sub-Agent | Spawned By | Model | Purpose |
|-----------|-----------|-------|---------|
| **Coder Backend** (per module) | Backend Engineer | Sonnet | One function, one module, one fix |
| **Coder Frontend** (per component) | Frontend Engineer | Sonnet | One component, one page, one fix |
| **Researcher** | CTO / Architect | Sonnet + web tools | Doc discovery, skills files |
| **Relay: {MCP_NAME}** | CTO | Sonnet + MCP | Query data stores, summarize for CTO |

This roster is a floor, not a ceiling. Spawn additional specialist sub-agents as needed.

## MCP Agent Architecture

The CTO and teammates do NOT interact with MCP servers directly. All MCP queries go through **relay agents** — ephemeral sub-agents that query the MCP, summarize results to ≤30 lines, and report back. This protects the CTO's context window from raw MCP output.

> See `.claude/skills/relay-mcp-pattern/SKILL.md` for the generic relay template. Pre-filled templates exist for common MCPs (e.g., `.claude/skills/relay-qmd/SKILL.md` for QMD on-device knowledge search).

## Browser Testing Standard

**agent-browser** (Vercel) is **MANDATORY** for all browser-based QA. This includes QA UI/UX testing (Article 4), UX Sense Check (Article 16), and any test requiring browser interaction.

**Playwright** is permitted ONLY for automated regression scripts in CI/CD — not as a substitute for agent-browser during QA.

| Tool | Use Case | When |
|------|----------|------|
| **agent-browser (Vercel)** | All interactive browser QA, persona testing, exploratory testing | MANDATORY during slice development |
| **Playwright** | Automated regression scripts, CI/CD pipeline checks | OPTIONAL, regression only |
