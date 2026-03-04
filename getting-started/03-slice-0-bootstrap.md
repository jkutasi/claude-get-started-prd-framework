# Step 3: Slice 0 Bootstrap (Create EVERYTHING Before Writing Code)

> Part of the [Getting Started](INDEX.md) roadmap. Load only this file when working on creating Slice 0 infrastructure.

Slice 0 creates every file, directory, skill, template, and script so that when Slice 1 starts, the infrastructure for compliance already exists. The CTO loads ONE subdocument at a time for each step.

### 3a. Create CLAUDE.md Contract

> Load `contract-templates/CLAUDE-MD-TEMPLATE.md` (core, ~400 lines) and customize for your project.
> Also copy `contract-templates/articles/ directory (one file per article, loaded on demand)` — this is loaded on demand, NOT at session start.

The core contract contains:
- CTO role definition (Delegate Mode, never writes code)
- Nuclear Rules with verification gates
- Agent Teams structure
- Per-slice workflow with all phases
- Articles quick-reference table (points to the appendix for full details)

The articles appendix contains the full definitions of Articles 1-18 (code authorship, peer review, QA, Red Team, Whiskey Team, UX Sense Check, Test-First Specification Protocol, Test Peer Review Protocol). Agents load it on demand when they need a specific article's details.

### 3b. Create Contract Documents

Load and customize each:
- `contract-templates/CONTRIBUTING-TEMPLATE.md` — Code authorship, naming, commit convention
- `contract-templates/SECURITY-TEMPLATE.md` — API keys, OWASP, access levels
- `contract-templates/DATA-CONTRACT-TEMPLATE.md` — Schemas, versioning, migration
- `contract-templates/ARCHITECTURE-STANDARDS-TEMPLATE.md` — Feature-based architecture, layer separation, 150-line limit, observability, error wrapping (Article 20)
- `contract-templates/TESTING-PYRAMID-TEMPLATE.md` — Test pyramid, coverage, Gherkin, edge cases
- `contract-templates/TESTING-PROCEDURES-TEMPLATE.md` — Test-first protocol, peer review, QA procedures
- `contract-templates/TESTING-GATES-TEMPLATE.md` — Defect resolution, browser testing, gate checklist

### 3c. Create Agent Skill Files

Load and customize each from `skill-templates/`:

**Core teammates:**
- `cto-orchestrator.md` — CTO lead skill file
- `coder-backend.md` — Backend coder
- `coder-frontend.md` — Frontend coder

**Peer reviewers:**
- `reviewer-gemini.md`, `reviewer-openai.md`, `reviewer-grok.md`

**QA team (all report to QA Lead):**
- `qa-lead.md` — QA Lead coordinator
- `qa-stats.md`, `qa-code-quality.md`, `qa-data-integrity.md`, `qa-security.md`, `qa-uiux-browser.md`
- `qa-manager.md` — QA findings synthesizer
- `red-team-reviewer.md` — 10 attack dimensions, pre-build gate
- `whiskey-team-adversarial-qa.md` — Adversarial QA + implicit regression + Goal Achievement Test
- `ux-sense-check.md` — Persona-based UX browser testing (3 generic personas)

**Support:**
- `researcher.md`, `documentation-scribe.md`
- `relay-mcp-pattern.md` — Duplicate once per MCP server

### 3d. Create Review Artifact Templates

Copy from `review-templates/` into your project's `reviews/` directory:
- `TEST-SPEC-TEMPLATE.md` -- Gherkin audit + test specification (Article 17)
- `TEST-REVIEW-TEMPLATE.md` -- Test code peer review (Article 18)
- `PEER-REVIEW-TEMPLATE.md`
- `QA-SWARM-TEMPLATE.md`
- `RED-TEAM-REVIEW-TEMPLATE.md`
- `WHISKEY-TEAM-TEMPLATE.md`
- `UX-SENSE-CHECK-TEMPLATE.md`

### 3e. Create Gate Check Script

Copy `examples/gate_check.py` to your project root. This script mechanically verifies ALL artifacts exist before allowing the next slice.

### 3f. Create Supporting Infrastructure

- `PROJECT.md` — Full architecture + implementation details (source of truth)
- `DOCS_MAP.md` — Documentation index (every agent reads this first)
- `AGENT_REGISTRY.md` — Who does what (use `reference/agent-registry-template.md`)
- `config/default.yaml` + `config/CONFIG_SCHEMA.md` (use `reference/config-schema-template.md`)
- Create directories: `features/`, `tests/integration/`, `src/shared/errors/`, `src/shared/logging/`, `src/shared/middleware/`, `output/`, `diary/`, `slices/`, `learnings/`
- Initialize `diary/PROJECT_DIARY.md`
- Initialize `learnings/` files (use `persistence/learnings-folder-template/`)
- Set up `.env` with API keys for peer review models

### 3g. Set Up Persistence (Choose Your Approach)

Read `persistence/PERSISTENCE-PATTERNS.md` and choose:
- **Option A:** Plain Markdown files in `learnings/` (recommended starting point)
- **Option B:** Obsidian + Obsidian MCP (for linked knowledge graphs)
- **Option C:** Mem0 (for automatic AI memory retrieval)
- **Option D:** Markdown + Mem0 or Obsidian (belt and suspenders)

For advanced persona simulation enhancements, see `persistence/TINYTROUPE-PATTERNS.md`.
