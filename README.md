# Claude Get-Started PRD Framework

A multi-agent project template for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with [Agent Teams](https://docs.anthropic.com/en/docs/claude-code/agent-teams). It defines the structure, contracts, QA process, and delivery model for building software with AI agents that orchestrate, code, review, and test — with enforced separation of concerns.

## What This Is

This is a **methodology template**, not a code library. Copy the entire folder into a new project workspace, replace the `{PLACEHOLDER}` values with your project specifics, and Claude Code uses it as its operating contract.

The framework enforces:

- **CTO Orchestrator** (Opus) delegates all work — never writes code directly
- **Test-first workflow** — tests are written by independent agents before any implementation code
- **Multi-model peer review** — every slice reviewed by Gemini, OpenAI Codex, Grok, and optionally Greptile independently
- **Adversarial QA** — Red Team, Professors, Whiskey Team, and UX Sense Check run on every slice
- **10-phase slice lifecycle** (A through J) with mechanical gate checks at each transition

## Quick Start

1. **Copy** this entire folder into your new project workspace
2. **Open** `getting-started/INDEX.md` — it's the sequential roadmap, follow it step by step
3. **Replace** all `{PLACEHOLDER}` values with your project specifics (tech stack, project name, paths, etc.)
4. **Set up** `.env` with API keys for peer review models (Gemini, OpenAI/Codex, Grok/xAI)
5. **Enable** Agent Teams: set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
6. **Start** Claude Code — it reads the contracts and operates within them

## Repository Structure

```
.
├── getting-started/                     # Roadmap — start with INDEX.md
│   ├── INDEX.md                        # Table of contents
│   ├── 00-nuclear-rules.md            # Nine rules that override everything
│   ├── 01-planning-phase.md           # Step 1: User story, tech stack, slices
│   ├── 02-agent-teams.md             # Step 2: Agent Teams architecture
│   ├── 03-slice-0-bootstrap.md       # Step 3: Create everything before code
│   ├── 04-per-slice-workflow.md      # Step 4: Phases A-J
│   ├── 05-browser-testing.md         # Step 5: Browser testing + session checklist
│   └── 06-appendix.md               # File structure reference + naming
│
├── contract-templates/                  # The rules of engagement
│   ├── CLAUDE-MD-TEMPLATE.md          # Core contract (loaded at session start)
│   ├── ARCHITECTURE-STANDARDS-TEMPLATE.md  # Feature folders, layers, 150-line, observability
│   ├── CONTRIBUTING-TEMPLATE.md       # Code standards, commit convention
│   ├── SECURITY-TEMPLATE.md          # API keys, OWASP, access control
│   ├── DATA-CONTRACT-TEMPLATE.md     # Schemas, versioning, migration
│   ├── TESTING-PYRAMID-TEMPLATE.md   # Testing pyramid, coverage, Gherkin, edge cases
│   ├── TESTING-PROCEDURES-TEMPLATE.md # Test-first protocol, peer review, QA procedures
│   ├── TESTING-GATES-TEMPLATE.md     # Defect resolution, browser testing, gate checklist
│   └── articles/                      # One file per contract article
│       ├── INDEX.md                   # Article listing
│       ├── article-01-code-authorship.md
│       ├── ...                        # Articles 02-20
│       ├── article-20-code-architecture.md
│       ├── article-21-commit-push.md
│       ├── ...                        # Articles 22-33
│       └── article-34-error-diagnosis.md
│
├── skill-templates/                    # Agent role definitions (one file per agent)
│   ├── cto-orchestrator.md           # Tier 1: CTO — orchestrates everything
│   ├── qa-lead.md                    # Tier 1: QA Lead — coordinates all QA
│   ├── coder-backend.md              # Tier 2: Backend coder
│   ├── coder-frontend.md             # Tier 2: Frontend coder
│   ├── reviewer-{gemini,openai,grok,greptile}.md  # Peer reviewers (3 required + 1 optional)
│   ├── red-team-reviewer.md          # Adversarial review (10 attack dimensions)
│   ├── whiskey-team-adversarial-qa.md # Adversarial end-to-end QA
│   ├── ux-sense-check.md             # Persona-based UX testing
│   ├── qa-{stats,code-quality,data-integrity,security,uiux-browser}.md  # QA specialists
│   ├── qa-manager.md                 # QA synthesis formatter
│   ├── documentation-scribe.md       # Documentation updates
│   ├── researcher.md                 # External research
│   ├── relay-{mcp-pattern,qmd}.md    # MCP relay patterns
│   └── prof-*.md                     # 15 Professor domain-expert agents
│
├── review-templates/                   # Artifact templates for review outputs
│   ├── TEST-SPEC-TEMPLATE.md         # Gherkin audit + test specification
│   ├── TEST-REVIEW-TEMPLATE.md       # Test code peer review findings
│   ├── PEER-REVIEW-TEMPLATE.md       # Implementation code peer review
│   ├── QA-SWARM-TEMPLATE.md          # QA swarm synthesis
│   ├── RED-TEAM-REVIEW-TEMPLATE.md   # Red team findings
│   ├── PROFESSOR-REVIEW-TEMPLATE.md  # Professor domain-expert findings
│   ├── WHISKEY-TEAM-TEMPLATE.md      # Whiskey team findings
│   └── UX-SENSE-CHECK-TEMPLATE.md    # UX sense check findings
│
├── examples/                           # Reference examples
│   ├── mermaid-diagrams.md           # Mermaid diagram templates (7 types)
│   ├── gherkin-examples.md           # Gherkin scenario examples
│   ├── gate_check.py                 # Mechanical gate check script
│   └── project-diary-template.md     # Project diary format
│
└── reference/                          # Supporting reference docs
    ├── agent-registry-template.md    # Agent role assignments
    ├── config-schema-template.md     # Configuration schema
    └── naming-conventions.md         # Article 10 naming rules
```

## Per-Slice Workflow (Phases A–J)

Every vertical slice follows this mandatory sequence:

| Phase | Name | What Happens |
|-------|------|-------------|
| **A** | Preparation | CTO reviews requirements, researcher gathers docs |
| **A.5** | Doc Bootstrap + Diagrams | Slice 0: docs + high-level diagrams. Slices 1+: per-slice diagrams |
| **A.6** | User Scope Confirmation | User reviews and approves slice scope before Red Team and tests |
| **A.7** | Red Team + Professor Pre-Build | Adversarial + domain-expert review of the user-confirmed plan before any code is written |
| **B** | Test Specification | B.1: Gherkin audit. B.2: Test-writer agents write all tests (must be RED). B.3: Test peer review |
| **C** | Implementation | Coder agents write code until all tests from Phase B pass |
| **D** | Self-Reflection | Each coder re-reads their own code as a reviewer |
| **E** | Peer Review | 3+ independent external models review in parallel (+ Greptile if configured) |
| **F** | QA Swarm | Standard QA + Whiskey Team + UX Sense Check in parallel |
| **F.5** | Runtime Log Check | Check Sentry, server logs, DB logs for errors surfaced during QA |
| **G** | Autonomous Fix Verification | Autonomous Defect Resolution Protocol — QA agents fix inline, CTO verifies + handles escalations |
| **H** | Regression | Full regression check + implicit behavior regression (6 categories) |
| **I** | Documentation | Scribe updates all affected docs |
| **I.5** | User Delivery | CTO presents DONE slice to user with all QA results — user only sees fully-vetted work |
| **J** | Gate Check | Mechanical verification that all artifacts exist |
| **Post-Push** | Post-Push Verification | Check error tracker, deployment logs, and Greptile after every push |

## Key Concepts

- **Nuclear Rules**: Nine rules that override everything — CTO never writes code, peer review is mandatory, slices ship complete
- **Operational Workflow (Articles 21-34)**: Git workflow, lint enforcement, sub-agent separation, QA sweep, BFF pattern, observability operations, planning decomposition, error diagnosis
- **Test-First (Articles 17-18)**: Tests are written by independent test-writer agents *before* implementation. Different agents write tests vs. code. Test code also gets 3-model peer review
- **Autonomous Defect Resolution Protocol**: Bug found → finding agent spawns fix sub-agent → AUDIT test → RED (must fail) → GREEN (fix code) → REGRESSION (full suite) → CLASS SCAN (fix all instances of same category) → COMMIT (atomic). Escalate to user only for architectural decisions, infrastructure changes, or 3x failure
- **Skeletal Interfaces**: Architect defines function signatures and class stubs (`raise NotImplementedError`) so test-writers can import cleanly before implementation exists
- **10 Review Artifacts Per Slice**: test-spec, test-review, peer-review, qa-swarm, red-team-pre-build, red-team, professor-pre-build, professor, whiskey-team, ux-sense-check (if frontend)
- **Code Architecture Standards (Article 20)**: Feature-based folder organization (20a), three-layer separation (20b), 150-line file limit (20c), display-only frontend (20d), structured logging (20e), error wrapping with context chaining (20f), P0/P1/P2 test priority (20g), and migration strategy (20h). These structural rules are the primary quality mechanism — when code is small and concerns are isolated, agents work better automatically

## Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed
- Agent Teams enabled (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)
- API keys for peer review models (at least 3 of: Gemini, OpenAI/Codex, Grok/xAI, Greptile)
- [OpenAI Codex CLI](https://developers.openai.com/codex) installed (`npm install -g @openai/codex`)
- [Greptile](https://www.greptile.com) API key (optional — adds codebase-aware 4th reviewer)
- `agent-browser` (Vercel) available for browser-based QA testing

## License

Private — for internal team use only.
