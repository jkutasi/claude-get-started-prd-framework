# Project Get-Started Template

> **Purpose:** This is the standard methodology template for bootstrapping any new project using Claude Code with multi-agent orchestration via Agent Teams. It defines the structure, contracts, QA process, and delivery model. Copy this entire `project-template/` folder into your new workspace and follow the steps below.
>
> **How to use:** This document is a sequential roadmap. Follow it from top to bottom. Each step references a subdocument — load ONLY that subdocument when you reach that step. Replace all `{PLACEHOLDER}` values with your project specifics. Delete instruction blocks when done.

---

## Nuclear Rules (Read First)

Three rules that override everything else. If you are Claude acting as the CTO Orchestrator, these are your hardcoded constraints. Violating any of them means the current slice fails and restarts.

| Rule | What It Means | Self-Check |
|------|--------------|------------|
| **1. CTO Never Writes Code** | All code is written by spawned sub-agents or teammates. The CTO orchestrates, delegates, and synthesizes. It does not implement. | "Am I about to write code? If yes, delegate to a teammate or spawn a sub-agent." |
| **2. Peer Review Is Mandatory** | Every slice, every time. All assigned reviewers must return findings before proceeding. No partial reviews. No skipping. Results saved to `reviews/slice-N-peer-review.md`. | "Have ALL reviewers reported back? Can I list each one's findings? Does the artifact file exist?" |
| **3. Slices Ship Complete** | A slice is not done until all Gherkin pass, all QA pass (including Whiskey Team + UX Sense Check), all peer review is resolved, Red Team pre-build gate passed, Goal Achievement Test passed via agent-browser, coverage ≥ 90% on business logic, docs updated, and ALL review artifact files exist on disk. | "Is Slice N completely done? Every gate passed? Do ALL review artifacts exist? If not, I cannot start Slice N+1." |

---

## Step 1: Planning Phase

Every project starts with a conversation between Claude and the owner to define scope.

### 1a. Write the User Story

```markdown
**Primary users:** {Who uses this? E.g., "Media buyers (day-to-day) and the owner (strategic oversight)"}

**Problem:** {What pain point are we solving? Be specific — include numbers if available.}

**Solution:** {One-paragraph description of what we're building.}

**Scope (this workspace):** {What's IN scope and what's explicitly OUT of scope.}

**Core workflow:**
1. {Step 1 — what triggers the system}
2. {Step 2 — what processing happens}
3. {Step 3 — what the user sees}
4. {Step 4 — what action the user takes}
5. {Step 5 — what happens after the action}
6. {Step 6 — how the feedback loop closes}

**Goal Achievement (binary test):** {What does "done" look like for the end user?
E.g., "A user can upload a CSV, run the scoring pipeline, and see ranked results
with recommendations on the dashboard." This becomes the Goal Achievement Test
that QA must pass via agent-browser for every slice.}
```

### 1b. Confirm Tech Stack with Owner

Claude asks these questions at project kickoff — don't assume the stack:

```markdown
**Frontend:** Framework? Styling? Charting/Viz?
**Backend:** Language? Framework? Task runner?
**Database:** Primary store? Cache? File storage?
**Infrastructure:** Hosting? CI/CD? Secrets management?
**Auth:** Provider? Role model?
**Browser Testing:** agent-browser (Vercel) is MANDATORY for QA. Confirm available.
**External Review Models:** Which API keys are available? (Gemini, OpenAI/Codex, Grok/xAI, Greptile optional)
**Codex CLI:** Installed? (`npm install -g @openai/codex` or `brew install codex`)
**Greptile (optional):** API key available? Greptile adds codebase-aware review as a 4th reviewer.
```

### 1c. Define Architecture

Document workspace layout, data flow, service accounts, and isolation boundaries.
If this is a sister workspace alongside existing infrastructure, define the hard rule:

> *The {project} workspace MUST NOT modify ANY existing workspace, database, table, cron job, worker, or code — unless specifically directed by the owner.*

### 1d. Define Vertical Slices

Projects are built in vertical slices — each slice is fully working end-to-end before moving to the next. Each slice must define:

```markdown
### Slice {N}: {Descriptive Name}
**Goal:** {One sentence — what does the user get when this ships?}
**Goal Achievement Test:** {Binary test: "A user can {do X} and see {Y result}"}
**Backend:** {files and what they do}
**Frontend:** {routes and what they show}
**Gherkin:** {key acceptance scenarios}
**Acceptance:** {measurable criteria}
**Dependencies:** Slice {X} must be complete first.
```

### 1e. Plan-Stage Peer Review

Before any code, the full plan goes through multi-model peer review:
1. Claude self-reflects on the plan
2. Plan sent to Gemini, OpenAI Codex, Grok for independent review
3. Consensus issues (2+ models agree) = mandatory fixes
4. Owner signs off on final plan

---

## Step 2: Agent Teams Architecture

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

---

## Step 3: Slice 0 Bootstrap (Create EVERYTHING Before Writing Code)

Slice 0 creates every file, directory, skill, template, and script so that when Slice 1 starts, the infrastructure for compliance already exists. The CTO loads ONE subdocument at a time for each step.

### 3a. Create CLAUDE.md Contract

> Load `contract-templates/CLAUDE-MD-TEMPLATE.md` (core, ~400 lines) and customize for your project.
> Also copy `contract-templates/CLAUDE-MD-ARTICLES.md` (articles reference, ~500 lines) — this is loaded on demand, NOT at session start.

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
- `contract-templates/TESTING-CONTRACT-TEMPLATE.md` — Test pyramid, Gherkin, QA procedures, browser testing

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
- Create directories: `features/`, `tests/`, `src/`, `output/`, `diary/`, `slices/`, `learnings/`
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

---

## Step 4: Per-Slice Workflow

**Every phase is MANDATORY. Skipping any phase is a CONTRACT VIOLATION.**

```
PHASE A: PREPARATION
1. CTO reviews slice requirements + Gherkin acceptance criteria
2. Researcher gathers docs, builds/updates skills files
3. Architect creates per-slice detailed diagrams (sequence + focused ER)

PHASE A.5: DOC BOOTSTRAP + DIAGRAM REVIEW
   Slice 0: CTO delegates to Scribe for PROJECT.md, DOCS_MAP.md, contract stubs.
   Architect creates high-level overview diagrams (System Architecture, Data Model ER,
   User Flow, Slice Dependency Graph) for user review.
   Slices 1+: Per-slice detailed diagrams created in Phase A (non-blocking).

PHASE A.6: USER SCOPE CONFIRMATION (Article 19) -- MANDATORY
4. CTO presents slice scope to user: summary, Gherkin scenarios, diagrams, Goal Achievement Test
5. If scope changed from original plan, highlight what changed and why
6. User responds: APPROVE (proceed) or REVISE (provide feedback, CTO adjusts, re-presents)

   +-----------------------------------------------------------------+
   | USER SCOPE GATE A.6: Before proceeding to Red Team:             |
   | [] "User reviewed slice scope (summary + Gherkin + diagrams)"   |
   | [] "User responded APPROVE"                                     |
   | [] "Any scope changes from original plan were highlighted"       |
   +-----------------------------------------------------------------+

PHASE A.7: RED TEAM PRE-BUILD GATE
7. QA Lead spawns Red Team Reviewer on user-confirmed slice plan (10 attack dimensions)
8. Red Team sends plan to {EXTERNAL_MODEL} with hostile prompt
9. Verdict: APPROVE / REVISE / BLOCK
   If BLOCK: cannot proceed. Max 3 iterations before owner escalation.
   Artifact: reviews/slice-N-red-team-pre-build.md

   +-----------------------------------------------------------------+
   | RED TEAM GATE: Before proceeding, CTO must confirm:             |
   | [] "Red Team Reviewer returned verdict: APPROVE or REVISE"      |
   | [] "reviews/slice-N-red-team-pre-build.md EXISTS on disk"       |
   | [] "Verdict is NOT BLOCK (or BLOCK findings were addressed)"    |
   +-----------------------------------------------------------------+

PHASE B: GHERKIN AUDIT + TEST SPECIFICATION + TEST PEER REVIEW (Article 17, 18)

   B.1: GHERKIN AUDIT (max 3 cycles)
   7.  QA Lead audits Gherkin for completeness (traceability matrix) + quality
   8.  Every user story element must map to at least one Gherkin scenario
   9.  Quality: unambiguous, concrete values, testable outcomes, NFR coverage

   B.2: TEST SPECIFICATION (different agents from implementation coders)
   10. Architect defines skeletal interfaces (function sigs, class stubs)
   11. QA Lead spawns test-writer sub-agents (NOT implementation coders)
   12. Test-writers write ALL tests: unit, integration, E2E definitions
   13. ALL tests must be RED (import errors or assertion failures)

   B.3: TEST PEER REVIEW (3+ models, parallel)
   14. 3 peer reviewers (+ Greptile if configured) review test code in parallel
   15. Consensus (2+) = mandatory test fixes before proceeding

   +-----------------------------------------------------------------+
   | TEST SPEC GATE B: CTO must confirm:                             |
   | [] "Gherkin Audit PASSED (completeness + quality)"              |
   | [] "All tests written by test-writer sub-agents (not coders)"   |
   | [] "All tests are RED"                                          |
   | [] "Test code peer-reviewed by 3+ external models"              |
   | [] "reviews/slice-N-test-spec.md EXISTS on disk"                |
   | [] "reviews/slice-N-test-review.md EXISTS on disk"              |
   | [] "CTO did NOT write any test code directly"                   |
   +-----------------------------------------------------------------+

PHASE C: IMPLEMENTATION
16. CTO assigns implementation to coder teammates (NOT itself -- Nuclear Rule 1)
17. Coders receive failing tests + spec, write code until tests PASS

   +-----------------------------------------------------------------+
   | NUCLEAR GATE C: CTO must confirm:                               |
   | [] "I did NOT write any code myself in this phase"              |
   | [] "All code was produced by teammates or their sub-agents"     |
   | [] "All tests from Phase B now PASS"                            |
   +-----------------------------------------------------------------+

PHASE D: SELF-REFLECTION (mandatory)
18. Each coder re-reads their code, identifies issues, proposes improvements

PHASE E: PEER REVIEW (3+ models, parallel)
19. 3 peer reviewers (+ Greptile if configured) run in parallel, return findings

   +-----------------------------------------------------------------+
   | NUCLEAR GATE E: CTO must confirm:                               |
   | [] "ALL reviewers returned findings before proceeding"          |
   | [] "Consensus issues (2+ reviewers) identified as mandatory"    |
   +-----------------------------------------------------------------+

20. CTO synthesizes: consensus (2+) = mandatory fixes

PHASE F: QA SWARM + WHISKEY TEAM + UX SENSE CHECK (parallel)
21. Standard QA swarm -- Stats, Code Quality, Data Integrity, Security, UI/UX
22. Whiskey Team -- adversarial QA (8 scope items incl. Goal Achievement Test)
    + MANDATORY implicit behavior regression (6 categories)
23. UX Sense Check -- 3 personas navigate via agent-browser (frontend slices)
    All run under QA Lead coordination.
24. QA Manager synthesizes ALL findings into prioritized fix plan

PHASE G: FIX REVIEW + RED TEAM ESCALATION + DEFECT RESOLUTION
25. CTO assigns fixes to teammates (NOT itself)
26. Fixes go through peer review
27. Defect Resolution Protocol (Article 17e): audit test first, fix test, then code
28. IF bug persists: QA Lead escalates to Red Team (Article 14b)
    Max 3 fix-review iterations before owner escalation

PHASE H: REGRESSION CHECK + IMPLICIT BEHAVIOR REGRESSION
29. Abbreviated QA re-run on fixed areas
30. Whiskey Team runs MANDATORY implicit behavior regression (6 categories)
31. UX Sense Check re-runs on changed frontend pages

   +-----------------------------------------------------------------+
   | NUCLEAR GATE H: Before starting next slice, CTO must confirm:   |
   |                                                                   |
   | [] "Gherkin audit passed (completeness + quality)"              |
   | [] "All tests written by test-writer sub-agents (not coders)"   |
   | [] "All Gherkin scenarios pass"                                  |
   | [] "All peer reviewers reviewed and approved"                    |
   | [] "All QA agents ran and passed"                                |
   | [] "Whiskey Team ran -- all CRITICAL/HIGH findings resolved"     |
   | [] "Goal Achievement Test PASSED via agent-browser"              |
   | [] "Implicit behavior regression completed (6/6 categories)"    |
   | [] "UX Sense Check ran (if frontend slice)"                      |
   | [] "Unit test coverage >= 90% on business logic"                 |
   | [] "CTO did NOT write any code or test code this slice"          |
   | [] "reviews/slice-N-test-spec.md EXISTS"                         |
   | [] "reviews/slice-N-test-review.md EXISTS"                       |
   | [] "reviews/slice-N-peer-review.md EXISTS"                       |
   | [] "reviews/slice-N-qa-swarm.md EXISTS"                          |
   | [] "reviews/slice-N-red-team-pre-build.md EXISTS"                |
   | [] "reviews/slice-N-red-team.md EXISTS"                          |
   | [] "reviews/slice-N-whiskey-team.md EXISTS"                      |
   | [] "reviews/slice-N-ux-sense-check.md EXISTS (if frontend)"      |
   +-----------------------------------------------------------------+

PHASE I: DOCUMENTATION UPDATE
32. Documentation Scribe updates affected docs
33. Learnings files updated with new patterns discovered
34. If a discovery invalidated earlier diagrams, update them here

PHASE J: MECHANICAL GATE CHECK
35. CTO runs: python gate_check.py --slice N [--frontend]
36. Script verifies ALL artifacts exist on disk (8 review files per slice)
37. If FAIL: fix missing items. Do NOT start next slice.
38. If PASS: begin Slice N+1.
```

---

## Step 5: Browser Testing Standard

`agent-browser` (Vercel) is the **MANDATORY** tool for all browser-based QA testing. It works on ANY website. It visually sees the page like a human and reasons about layout, readability, and UX.

- **Whiskey Team, UX Sense Check, QA UI/UX:** MUST use `agent-browser`
- **Playwright:** Optional for automated regression scripts only. NOT sufficient for QA sign-off.
- All browser sessions use the `--session ab` flag

### Testing Pyramid

| Layer | What It Tests | Tool | Who | When |
|-------|-------------|------|-----|------|
| **Unit** | Functions, logic, parsers | pytest / jest / vitest | Test-writer sub-agents (Phase B) | Before code -- must be RED |
| **Integration** | Components together, API contracts | pytest / jest + test DB | Test-writer sub-agents (Phase B) | Before code -- must be RED |
| **E2E Browser** | Full user flows -- clicks, forms, navigation | `agent-browser` (MANDATORY) | Whiskey + QA UI/UX (Phase F) | Every frontend slice |
| **Adversarial** | Edge cases, race conditions, silent failures | `agent-browser` + API calls | Whiskey (Phase F) | Every slice |
| **UX Sense-Check** | "Does this make sense to a human?" | `agent-browser` + personas | UX Sense Check (Phase F) | Frontend slices |
| **Goal Achievement** | "Can a user complete the full workflow?" | `agent-browser` | Whiskey (Phase F) | Every slice |
| **Implicit Regression** | Untested state gaps, cross-component issues | `agent-browser` + code analysis | Whiskey (Phase H) | Every session |

**Rule:** Unit tests verify code *works*. Browser tests verify it works *for humans*. Both are mandatory. Passing unit tests with zero browser testing is NOT a shipped slice.

---

## Step 6: Session Start Checklist (Every New Session)

Before ANY implementation work:

- [ ] Read CLAUDE.md
- [ ] Verify API keys exist for peer review models
- [ ] Run `python gate_check.py --slice {latest} --all` to verify all completed slices
- [ ] If ANY slice returns FAIL, run retroactive review FIRST
- [ ] Read relevant learnings files (`learnings/QA_LEARNINGS.md`, etc.)
- [ ] Only then proceed with new work

---

## Appendix: File Structure Reference

```
{project-root}/
├── CLAUDE.md                           # Multi-agent contract (binding)
├── PROJECT.md                          # Full architecture + implementation details
├── DOCS_MAP.md                         # Documentation index
├── AGENT_REGISTRY.md                   # Who does what
├── gate_check.py                       # Mechanical gate enforcement
├── .claude/
│   ├── skills/                         # One file per agent role
│   ├── skills-index.md                 # Master index
│   └── settings.local.json             # MCP server config
├── contracts/
│   ├── CONTRIBUTING.md
│   ├── SECURITY.md
│   ├── DATA_CONTRACT.md
│   └── TESTING_CONTRACT.md
├── config/
│   ├── default.yaml
│   └── CONFIG_SCHEMA.md
├── slices/                             # One spec per slice (extracted from PROJECT.md)
├── reviews/                            # PROOF that all review layers ran
│   ├── TEST_SPEC_TEMPLATE.md
│   ├── TEST_REVIEW_TEMPLATE.md
│   ├── PEER_REVIEW_TEMPLATE.md
│   ├── QA_SWARM_TEMPLATE.md
│   ├── RED_TEAM_REVIEW_TEMPLATE.md
│   ├── WHISKEY_TEAM_TEMPLATE.md
│   └── UX_SENSE_CHECK_TEMPLATE.md
├── learnings/                          # Persistent agent learnings
│   ├── QA_LEARNINGS.md
│   ├── BUILD_LEARNINGS.md
│   ├── REVIEW_LEARNINGS.md
│   └── UX_LEARNINGS.md
├── features/                           # Gherkin specs
├── tests/                              # Unit + integration tests
├── src/                                # Source code
├── diary/
│   └── PROJECT_DIARY.md
└── output/                             # Generated artifacts (gitignored)
```

---

## Appendix: Naming Convention

Per the CLAUDE.md contract — all names must be descriptive by what they do. No random, auto-generated, or whimsical names.

| Good | Bad | Why |
|------|-----|-----|
| `user-auth-service.py` | `module2.py` | Says what it does |
| `slice-2-data-validation.md` | `distributed-whistling-aurora.md` | No auto-generated names |
| `payment-processing.py` | `m3.py` | Self-documenting |

This applies to: markdown files, code modules, git branches, database tables, cloud jobs, Gherkin features, and all other named artifacts.
