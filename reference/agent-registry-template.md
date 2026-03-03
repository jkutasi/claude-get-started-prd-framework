# AGENT_REGISTRY.md — Template

> Copy this file to your project root as `AGENT_REGISTRY.md` during Slice 0.
> Lists every agent involved in the project, organized by function.

## Agent Registry — {PROJECT_NAME}

### Agent Teams

Agents are organized into **Teammates** (persistent, long-running agents that
participate across slices) and **ephemeral sub-agents** (spun up for a specific
task within a phase, then terminated).

- **Teammates** hold session state and accumulate context across a slice.
- **Sub-agents** are disposable — they receive a focused brief, execute, report
  back, and exit.

### Orchestration

| Agent | Tier | Model | Purpose | Skill File |
|---|---|---|---|---|
| CTO | Teammate | {MODEL_TIER_1} | Strategic oversight, blocker resolution, go/no-go decisions | `cto.md` |
| Architect | Teammate | {MODEL_TIER_1} | System design, slice planning, dependency mapping | `architect.md` |

### Implementation

| Agent | Tier | Model | Purpose | Skill File |
|---|---|---|---|---|
| Backend Engineer | Teammate | {MODEL_TIER_1} | Server-side code, APIs, data layer | `backend-engineer.md` |
| Frontend Engineer | Teammate | {MODEL_TIER_1} | UI components, client-side logic, styling | `frontend-engineer.md` |
| Data Engineer | Teammate | {MODEL_TIER_1} | Pipelines, transformations, schema design | `data-engineer.md` |

### Peer Review

| Agent | Tier | Model | Purpose | Skill File |
|---|---|---|---|---|
| Peer Reviewer | Sub-agent | {MODEL_TIER_1} | Code review against contract and standards | `peer-reviewer.md` |

### QA Swarm

| Agent | Tier | Model | Purpose | Skill File |
|---|---|---|---|---|
| QA Lead | Teammate | {MODEL_TIER_1} | Test strategy, swarm coordination, verdict | `qa-lead.md` |
| Happy Path Tester | Sub-agent | {MODEL_TIER_2} | Core workflow validation | `happy-path-tester.md` |
| Edge Case Tester | Sub-agent | {MODEL_TIER_2} | Boundary conditions, nulls, extremes | `edge-case-tester.md` |
| Security Tester | Sub-agent | {MODEL_TIER_2} | Input injection, auth bypass, data exposure | `security-tester.md` |
| Performance Tester | Sub-agent | {MODEL_TIER_2} | Load, latency, resource consumption | `performance-tester.md` |
| UX Sense Check | Sub-agent | {MODEL_TIER_2} | Persona-based usability evaluation | `ux-sense-check.md` |

### Data Access

| Agent | Tier | Model | Purpose | Skill File |
|---|---|---|---|---|
| Data Analyst | Sub-agent | {MODEL_TIER_2} | Query execution, data validation, reporting | `data-analyst.md` |

### Research

| Agent | Tier | Model | Purpose | Skill File |
|---|---|---|---|---|
| Research Agent | Sub-agent | {MODEL_TIER_2} | API docs, library evaluation, technical spikes | `research-agent.md` |

### Documentation

| Agent | Tier | Model | Purpose | Skill File |
|---|---|---|---|---|
| Scribe | Teammate | {MODEL_TIER_2} | Maintains CONFIG_SCHEMA, AGENT_REGISTRY, learnings files, session logs | `scribe.md` |
