# Step 3: Slice 0 Bootstrap (Create EVERYTHING Before Writing Code)

> Part of the [Getting Started](INDEX.md) roadmap. Load only this file when working on creating Slice 0 infrastructure.

Slice 0 creates every file, directory, skill, template, and script so that when Slice 1 starts, the infrastructure for compliance already exists. The CTO loads ONE subdocument at a time for each step.

### 3a. Create CLAUDE.md Contract

> Load `contract-templates/CLAUDE-MD-TEMPLATE.md` (core, ~90 lines) and customize for your project.
> Also load and deploy: `AGENT-TEAMS-TEMPLATE.md`, `ARTICLES-INDEX-TEMPLATE.md`, `PER-SLICE-WORKFLOW-TEMPLATE.md`.
> Copy `contract-templates/articles/ directory (one file per article, loaded on demand)` — articles are loaded on demand, NOT at session start.

The core contract contains:
- CTO role definition (Delegate Mode, never writes code)
- Nuclear Rules with verification gates
- Agent Teams structure
- Per-slice workflow with all phases
- Articles quick-reference table (points to the appendix for full details)

The articles appendix contains the full definitions of Articles 1-34 (code authorship, peer review, QA, Red Team, Professor Review, Whiskey Team, UX Sense Check, Test-First Specification Protocol, Test Peer Review, User Scope Confirmation, Code Architecture Standards). Agents load it on demand when they need a specific article's details.

**Path mapping:** Template files use `HYPHEN-TEMPLATE.md` naming (e.g., `ARCHITECTURE-STANDARDS-TEMPLATE.md`). When customized for your project, deploy to `contracts/` with underscore naming (e.g., `contracts/ARCHITECTURE_STANDARDS.md`). The articles directory copies as-is: `contract-templates/articles/` → `contracts/articles/`.

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
- Initialize `learnings/` files (one per domain: QA, BUILD, REVIEW, UX)
- Set up Husky pre-push hooks to run lint + type check on every push. See Article 23 for configuration.
- Set up `.env` with API keys for peer review models

### 3g. Install Observability Stack (MANDATORY — do not skip)

Three tools must be installed and working before any feature code is written:

**Sentry** — error tracking. Every error that occurs in the app — frontend or backend — gets captured automatically and appears in the Sentry dashboard. This is how we know what broke during QA: after every QA run, the CTO checks Sentry for new errors. No errors slipping through silently.

**Pino** (Node.js/TypeScript) or **structlog** (Python) — structured logger. Instead of scattered `console.log` statements that disappear, every log message is a structured JSON entry that Sentry can read. All code uses this shared logger — no raw `console.log` or `print()` anywhere.

**Ruff** (Python projects only) — linter. Automatically catches code quality issues before anything gets pushed. Wired into Husky pre-push hooks so bad Python code is blocked at the gate.

**Install steps (agent executes these):**

| Language | Packages to install |
|----------|-------------------|
| Node.js / TypeScript | `npm install pino pino-sentry-transport @sentry/node` |
| Python | `pip install structlog sentry-sdk ruff` + add to `requirements.txt` / `pyproject.toml` |
| Browser / SPA (frontend) | `npm install @sentry/browser` |

After installing:
1. Create `src/shared/logging/logger.{EXT}` — the single shared logger the whole codebase imports. It connects Pino/structlog to Sentry so errors flow through automatically.
2. Add `SENTRY_DSN` and `SENTRY_ENVIRONMENT` to `.env` using the project's Sentry credentials.
3. Send one test error through the logger and confirm it appears in the Sentry dashboard. If it doesn't show up, fix the connection before proceeding.

**Gate:** Do NOT start Slice 1 until ALL of the following are verified:

| # | Verification | How to Check |
|---|-------------|--------------|
| 1 | Sentry receiving errors | Send test error, confirm it appears in Sentry dashboard |
| 2 | Logger file exists | `ls src/shared/logging/logger.{EXT}` returns a file |
| 3 | No raw console calls | `grep -r "console\.\(log\|error\|warn\)" src/` returns zero matches |
| 4 | Linter configured | `pyproject.toml` has `[tool.ruff]` or `.eslintrc*` exists |
| 5 | Pre-push hook exists | `.husky/pre-push` file exists and blocks on lint failures |
| 6 | gate_check.py passes | `python gate_check.py --slice 0` returns PASS |

> **An error tracker configured "later" never gets configured. A linter installed "later" never gets installed. A logger created "later" means 8 slices of `console.log` that Sentry never sees.**

### 3i. Verify UserPromptSubmit Hook (Nuclear Rule 10)

Check whether `~/.claude/settings.json` contains a `UserPromptSubmit` hook. This hook fires on every prompt and reminds Claude to delegate all implementation to sub-agents, preserving the CTO's context window.

**Check (agent runs this):**
```bash
python3 -c "
import json, pathlib, sys
p = pathlib.Path.home() / '.claude' / 'settings.json'
if not p.exists():
    print('MISSING: ~/.claude/settings.json does not exist')
    sys.exit(1)
s = json.loads(p.read_text())
hooks = s.get('hooks', {})
if 'UserPromptSubmit' not in hooks:
    print('MISSING: UserPromptSubmit hook not found')
    sys.exit(1)
print('OK: UserPromptSubmit hook present')
"
```

**If missing, add the hook.** Open `~/.claude/settings.json` (create it if it doesn't exist) and add the following under `hooks`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'ORCHESTRATOR RULE: You are CTO only. NEVER use Edit/Write/Bash/NotebookEdit directly. Spawn a sub-agent for ALL implementation, large file reads, reviews, QA, and execution. Use Read/Glob/Grep only for lightweight planning. If context is growing, you are doing too much directly — delegate more.'"
          }
        ]
      }
    ]
  }
}
```

If `settings.json` already exists with other content, merge the `hooks.UserPromptSubmit` key into the existing JSON — do not overwrite the entire file.

**Gate:** Do NOT proceed past Slice 0 until the hook check returns `OK`.

### 3h. Set Up Persistence (Choose Your Approach)

Choose a cross-session memory strategy:
- **Option A:** Plain Markdown files in `learnings/` (recommended starting point)
- **Option B:** Obsidian + Obsidian MCP (for linked knowledge graphs)
- **Option C:** Mem0 (for automatic AI memory retrieval)
- **Option D:** Markdown + Mem0 or Obsidian (belt and suspenders)
