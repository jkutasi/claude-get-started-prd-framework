# Agent Teams Architecture — {PROJECT_NAME}

> **Loaded on demand.** The CTO loads this file at session start to understand the team structure. Do not keep in memory after internalizing the roster.

This project uses **Claude Code Agent Teams** with the environment variable:

```
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

Agent Teams enables **persistent teammates** that run as parallel Claude Code instances.
Teammates can message each other **horizontally** — they do not need to route all communication
through the CTO. This is fundamentally different from flat sub-agent spawning.

## Agents vs. Skills

**Agents are WHO** — thin role shells in `.claude/agents/` that define identity, model, and tool
permissions.

**Skills are HOW** — behavior modules in `.claude/skills/` that define protocols, checklists,
anti-patterns, and output formats.

When the CTO spawns a teammate or sub-agent, it picks an **agent** (for identity/permissions)
and a **skill** (for behavior/instructions). The agent file's `skills:` field lists which skills
that agent is designed to run. Skills carry the substance; agents carry the shell.

## How to Spawn Teammates and Sub-Agents

**Teammates (persistent):** Persistent agents that remain active across the session. They can
send messages to each other directly (horizontal communication). Use teammates for ongoing roles.

**Sub-agents (ephemeral):** Spawned by teammates (or the CTO) for one-shot focused tasks. They
complete their task, return a result, and are destroyed. Use sub-agents for a single function,
single review, or single QA check.

Every implementation task follows this pattern:

1. Define the task scope (one function, one component, one query — keep it small).
2. Assign to the appropriate teammate, or have the teammate spawn a sub-agent with: the relevant
   skill file, the relevant slice spec, and clear acceptance criteria.
3. Teammate/sub-agent implements (Phase C) or writes tests (Phase B), returns completion report.
4. CTO reviews the report, NOT the raw code (context window conservation).
5. If issues found, assign fix to a teammate or have them spawn a new sub-agent (do NOT fix
   directly).

## Teammate Roster

Opus is reserved EXCLUSIVELY for the CTO. All teammates and sub-agents use Sonnet shells.

| Teammate | Model | Persistent? | Primary Skills | Purpose |
|----------|-------|-------------|----------------|---------|
| **CTO Orchestrator** | Opus 4.7 | Yes (main session) | `/cto-orchestrator`, `/slice-workflow` | Orchestration, decisions, synthesis (YOU) |
| **Architect** | Sonnet | Yes | `/prof-architecture` | System design, schema decisions, dependency management |
| **Backend Engineer** | Sonnet | Yes | `/coder-backend` | Backend modules, queries, business logic, API endpoints |
| **Frontend Engineer** | Sonnet | Yes | `/coder-frontend` | UI components, pages, client-side logic, styling |
| **QA Lead** | Sonnet | Yes | `/qa-lead` | Coordinates QA swarm, synthesizes findings, manages QA sub-agents |

**Optional teammates:**

| Teammate | Model | When to Add |
|----------|-------|-------------|
| **Data Engineer** | Sonnet | Complex data pipelines, ETL, query optimization, dedicated schema management |
| **Documentation Scribe** | Sonnet | Extensive documentation requirements. Otherwise CTO or Architect handles docs. |

## Coder Sub-Agent Pattern

Coder sub-agents (Backend, Frontend) are **Sonnet courier shells**: they call OpenAI 5.5 via the
Responses API (`POST https://api.openai.com/v1/responses`, field `output_text`), run OpenAI
self-review, write code to disk, verify (line count + lint + tests), and retry up to 3 times.
On 3 failures they escalate to Opus. See Article 02 for the full protocol.

## Quality Gate Agents — Phase E Peer Review (4 Models, Run in Parallel)

| Sub-Agent | Spawned By | Skill | Lens |
|-----------|-----------|-------|------|
| **Peer Review Coordinator** | CTO / QA Lead | `/peer-review-orchestrator` | Orchestrates the parallel 4-model review; CTO invokes this |
| **Reviewer Gemini** | Peer Review Coordinator | `/reviewer-gemini` | Architecture, scalability |
| **Reviewer OpenAI 5.5** | Peer Review Coordinator | `/reviewer-openai` | Invariants, silent failures, security, 150-line |
| **Reviewer Opus 4.7** | — | (CTO own review — no separate skill) | CTO does its own review pass; Opus 4.7 IS the CTO |
| **Reviewer Grok** | Peer Review Coordinator | `/reviewer-grok` | Security, edge cases, adversarial inputs |

Consensus rule: 2+ reviewers flag the same issue = mandatory fix. Single reviewer = advisory
(except data-correctness and security, which are always mandatory). Round 2 required after fixes.
No fallback to lesser models on provider failure — report the error.

## Other Quality Gate Sub-Agents

| Sub-Agent | Spawned By | Model | Purpose |
|-----------|-----------|-------|---------|
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
| **Coder Backend** (per module) | Backend Engineer | Sonnet shell → OpenAI 5.5 | One function, one module, one fix |
| **Coder Frontend** (per component) | Frontend Engineer | Sonnet shell → OpenAI 5.5 | One component, one page, one fix |
| **Researcher** | CTO / Architect | Sonnet + web tools | Doc discovery, skills files |
| **Relay: {MCP_NAME}** | CTO | Sonnet + MCP | Query data stores, summarize for CTO |

## MCP Agent Architecture

The CTO and teammates do NOT interact with MCP servers directly. All MCP queries go through
**relay agents** — ephemeral sub-agents that query the MCP, summarize results to ≤30 lines, and
report back. This protects the CTO's context window from raw MCP output.

> See `.claude/skills/relay-mcp-pattern/SKILL.md` for the generic relay template.

## Browser Testing Standard

**agent-browser** (Vercel) is **MANDATORY** for all browser-based QA. Playwright is permitted
ONLY for automated regression scripts in CI/CD — not as a substitute for agent-browser during QA.

| Tool | Use Case | When |
|------|----------|------|
| **agent-browser (Vercel)** | All interactive browser QA, persona testing, exploratory testing | MANDATORY during slice development |
| **Playwright** | Automated regression scripts, CI/CD pipeline checks | OPTIONAL, regression only |
