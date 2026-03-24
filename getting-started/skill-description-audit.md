# Skill Description Audit

**Date:** 2026-03-24
**Rule:** Every skill `description` field MUST start with "Use when..." and contain ONLY triggering conditions, not workflow summaries. Max 1024 characters.
**Skills audited:** 41 (skills with SKILL.md files)

---

## GOOD — Already Follows the Rule

These two descriptions start with "Use when..." and contain only triggering conditions:

| Skill | Description |
|-------|-------------|
| design-first-gate | "Use when about to implement a new feature, refactor, or any change touching more than one file. Enforces design-before-code discipline." |
| task-manager | "Use when starting a new work session, creating tasks, tracking progress, or checking what needs to be done next." |

---

## NEEDS FIX — Descriptions That Are Role/Workflow Summaries

### Pattern A: Role label first, "Use when..." tacked on at the end

These descriptions open with a role label and workflow summary, then append a "Use when..." clause at the end. The fix is to promote the "Use when..." clause to the front and drop the role label.

| Skill | Current (broken) | Fix |
|-------|-----------------|-----|
| cto-orchestrator | "CTO orchestrator agent. Coordinates vertical slice execution, delegates to specialist agents, enforces Nuclear Rules and phase gates. Use when orchestrating a slice or coordinating agent teams." | Start with: "Use when orchestrating a vertical slice or coordinating agent teams." |
| prof-api-design | "API design professor. Reviews endpoint naming, REST conventions, versioning, error responses, and contract clarity. Use when evaluating API surfaces." | Start with: "Use when evaluating or reviewing API surfaces, endpoint naming, REST conventions, versioning, or error response design." |
| prof-architecture | "Architecture professor. Reviews system design, module boundaries, coupling, cohesion, and architectural patterns. Use when evaluating or planning system architecture." | Start with: "Use when evaluating or planning system architecture, module boundaries, coupling, or cohesion." |
| prof-code-craft | "Code craft professor. Reviews naming, readability, SOLID principles, and clean code practices. Use when evaluating code quality and maintainability." | Start with: "Use when evaluating code quality, naming, readability, SOLID principles, or maintainability." |
| prof-data | "Data professor. Reviews database design, migrations, query patterns, and data modeling. Use when evaluating data layer architecture." | Start with: "Use when evaluating data layer architecture, database design, migrations, or query patterns." |
| prof-devops | "DevOps professor. Reviews CI/CD pipelines, deployment strategies, infrastructure configuration, and release processes. Use when evaluating operational practices." | Start with: "Use when evaluating CI/CD pipelines, deployment strategies, infrastructure configuration, or release processes." |
| prof-distributed-systems | "Distributed systems professor. Reviews consistency models, partitioning, replication, consensus, and CAP trade-offs. Use when evaluating distributed architecture." | Start with: "Use when evaluating distributed architecture, consistency models, partitioning, replication, or CAP trade-offs." |
| prof-frontend | "Frontend professor. Reviews component architecture, state management, rendering patterns, and accessibility. Use when evaluating frontend code." | Start with: "Use when evaluating frontend code, component architecture, state management, rendering patterns, or accessibility." |
| prof-functional-design | "Functional design professor. Reviews pure functions, immutability, composition, and side-effect isolation. Use when evaluating functional programming patterns." | Start with: "Use when evaluating functional programming patterns, pure functions, immutability, or side-effect isolation." |
| prof-observability | "Observability professor. Reviews logging, metrics, tracing, alerting, and monitoring setup. Use when evaluating operational visibility." | Start with: "Use when evaluating operational visibility, logging, metrics, tracing, alerting, or monitoring setup." |
| prof-performance | "Performance professor. Reviews latency, throughput, caching, lazy loading, and resource optimization. Use when evaluating application performance." | Start with: "Use when evaluating application performance, latency, throughput, caching, or resource optimization." |
| prof-refactoring | "Refactoring professor. Reviews code transformation safety, incremental migration patterns, and behavior preservation. Use when planning or reviewing refactors." | Start with: "Use when planning or reviewing a refactor, code transformation safety, or incremental migration." |
| prof-resilience | "Resilience professor. Reviews error handling, retry logic, circuit breakers, graceful degradation, and fault tolerance. Use when evaluating system reliability." | Start with: "Use when evaluating system reliability, error handling, retry logic, circuit breakers, or fault tolerance." |
| prof-security | "Security professor. Reviews authentication, authorization, encryption, input validation, and threat modeling. Use when evaluating security posture." | Start with: "Use when evaluating security posture, authentication, authorization, encryption, or input validation." |
| prof-testing | "Testing professor. Reviews test strategy, coverage, pyramid balance, and test quality. Use when evaluating or improving test suites." | Start with: "Use when evaluating or improving test suites, test strategy, coverage, or pyramid balance." |
| prof-ux-engineering | "UX engineering professor. Reviews interaction design, micro-interactions, animation performance, and user experience implementation. Use when evaluating UX code quality." | Start with: "Use when evaluating UX code quality, interaction design, micro-interactions, or animation performance." |
| relay-mcp-pattern | "MCP relay pattern. Defines how to call external APIs through MCP server tools for peer review, search, and third-party integrations. Use when integrating external services." | Start with: "Use when integrating external services via MCP server tools for peer review, search, or third-party API calls." |
| relay-qmd | "QMD persistent knowledge relay. Indexes and searches project knowledge stored as markdown files in an Obsidian vault via on-device semantic search. Use when storing or retrieving cross-session knowledge." | Start with: "Use when storing or retrieving cross-session project knowledge via the on-device QMD semantic search vault." |
| ship-release | "Ship and release coordinator. Manages pre-push checklist, git push, post-push verification, and deployment monitoring. Use when ready to push a completed slice." | Start with: "Use when ready to push a completed slice through pre-push checklist, git push, and post-push verification." |
| slice-workflow | "Per-slice workflow orchestrator. Manages Phases A through J with gates, checklists, and Nuclear Rules enforcement. Use when starting or continuing a vertical slice." | Start with: "Use when starting or continuing a vertical slice through Phases A through J." |

### Pattern B: No "Use when..." clause at all — description is pure role/phase label

These descriptions describe what the agent does or when it's used by phase number but never use the "Use when..." trigger form.

| Skill | Current (broken) | Fix |
|-------|-----------------|-----|
| coder-backend | "Backend implementation agent. Writes server-side code following project architecture standards, testing patterns, and security requirements. Use during Phase C implementation for backend work." | "Use when implementing backend server-side code during Phase C of a vertical slice." |
| coder-frontend | "Frontend implementation agent. Writes client-side code following project UI/UX standards, component patterns, and accessibility requirements. Use during Phase C implementation for frontend work." | "Use when implementing frontend client-side code during Phase C of a vertical slice." |
| decision-journal | "Architecture Decision Record (ADR) management. Create, update, and search ADRs that capture why framework and project decisions were made. Integrates with QMD for semantic search." | "Use when creating, updating, or searching Architecture Decision Records (ADRs) for framework or project decisions." |
| documentation-scribe | "Documentation scribe agent. Writes and maintains project documentation, API docs, changelogs, and architecture diagrams. Use during Phase I documentation." | "Use when writing or updating project documentation, API docs, changelogs, or architecture diagrams during Phase I." |
| qa-code-quality | "Code quality QA specialist. Reviews naming, decomposition, control flow, duplication, and adherence to project conventions. Use during Phase F QA swarm." | "Use when running the Phase F QA swarm to review code quality, naming, decomposition, or adherence to conventions." |
| qa-data-integrity | "Data integrity QA specialist. Validates data flows, schema consistency, migration safety, and constraint enforcement. Use during Phase F QA swarm." | "Use when running the Phase F QA swarm to validate data flows, schema consistency, or migration safety." |
| qa-lead | "QA lead coordinator. Orchestrates the QA swarm by delegating to specialist QA agents and synthesizing results. Use during Phase F QA swarm." | "Use when orchestrating the Phase F QA swarm by delegating to specialist QA agents and synthesizing results." |
| qa-manager | "QA synthesis manager. Collects and formats results from all QA specialists into a unified report. Use at the end of Phase F QA swarm." | "Use when collecting and formatting results from all Phase F QA specialists into a unified QA report." |
| qa-security | "Security QA specialist. Tests for OWASP top 10 vulnerabilities, auth bypasses, injection vectors, and secret exposure. Use during Phase F QA swarm." | "Use when running the Phase F QA swarm to test for OWASP top 10 vulnerabilities, auth bypasses, or injection vectors." |
| qa-stats | "Statistical correctness QA specialist. Validates calculations, aggregations, rounding, and numerical accuracy. Use during Phase F QA swarm for data-heavy slices." | "Use when running the Phase F QA swarm on data-heavy slices to validate calculations, aggregations, or numerical accuracy." |
| qa-uiux-browser | "UI/UX browser QA specialist. Tests responsive layout, accessibility, visual consistency, and cross-browser behavior. Use during Phase F QA swarm for frontend slices." | "Use when running the Phase F QA swarm on frontend slices to test responsive layout, accessibility, or cross-browser behavior." |
| red-team-reviewer | "Adversarial red team reviewer. Attempts to break the implementation through attack vectors, edge cases, and abuse scenarios. Use during Phase A.7 red team review." | "Use when conducting the Phase A.7 red team review to probe attack vectors, edge cases, and abuse scenarios." |
| researcher | "Research agent. Investigates technical questions, evaluates libraries, and gathers context from codebase and external sources. Use during Phase A preparation or ad-hoc research." | "Use when investigating technical questions, evaluating libraries, or gathering codebase context during Phase A or ad-hoc research." |
| reviewer-gemini | "Gemini architecture peer reviewer. Analyzes code for structural patterns, coupling, and design issues via Gemini API. Use during Phase E peer review." | "Use when running Phase E peer review to analyze code for structural patterns, coupling, or design issues via Gemini." |
| reviewer-greptile | "Greptile codebase-aware reviewer. Analyzes code changes against full repository context via Greptile API. Use during Phase E or post-push verification." | "Use when running Phase E peer review or post-push verification with codebase-aware analysis via Greptile." |
| reviewer-grok | "Grok security peer reviewer. Analyzes code for security vulnerabilities, injection risks, and auth weaknesses via xAI API. Use during Phase E peer review." | "Use when running Phase E peer review to analyze code for security vulnerabilities, injection risks, or auth weaknesses via Grok." |
| reviewer-openai | "OpenAI Codex peer reviewer. Analyzes code for edge cases, error handling, and correctness via OpenAI API. Use during Phase E peer review." | "Use when running Phase E peer review to analyze code for edge cases, error handling, or correctness via OpenAI Codex." |
| ux-sense-check | "UX sense check reviewer. Evaluates user flows from multiple persona perspectives for usability, clarity, and friction. Use during Phase F QA swarm for user-facing slices." | "Use when running the Phase F QA swarm on user-facing slices to evaluate user flows for usability, clarity, and friction." |
| whiskey-team | "Whiskey Team adversarial QA. Performs end-to-end destructive testing with malformed inputs, race conditions, and boundary violations. Use during Phase F QA swarm." | "Use when running the Phase F QA swarm to perform destructive end-to-end testing with malformed inputs, race conditions, or boundary violations." |

---

## Summary

| Category | Count |
|----------|-------|
| Already correct (starts with "Use when...") | 2 |
| Pattern A fix (role label + trailing "Use when...") | 20 |
| Pattern B fix (no "Use when..." at all) | 19 |
| **Total needing fix** | **39** |

All 39 broken descriptions have been fixed directly in their SKILL.md files (description field only).
