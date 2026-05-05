# Step 1: Planning Phase

> Part of the [Getting Started](INDEX.md) roadmap. Load only this file when working on defining project scope and tech stack.

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
**External Review Models:** Which API keys are available? (Gemini, OpenAI o3/o4, Claude Opus 4.7, Grok — all 4 required for adversarial peer review)
**Observability:** Error tracking provider? (default: Sentry) Structured logger? (default: Pino / structlog) Logger transport? (default: pino-sentry-transport / sentry-sdk)
**Error Tracking MCP:** Available? (recommended for Claude Code integration)
```

### 1c. Configure MCP Integrations

After selecting your tech stack, search for and configure all available **MCP (Model Context Protocol) servers** for your chosen tools. MCPs give your AI assistant direct access to your external services — error tracking, database management, code review, etc.

**Required step:** For each tool in your tech stack, search `"[tool name] MCP server"` to check if an official MCP exists. Add all available MCPs to your `.claude/settings.local.json` file (see JSON format below).

#### Common MCPs by Category

| Category | Service | Endpoint | Auth | Tools |
|----------|---------|----------|------|-------|
| **Error Tracking** | Sentry | `https://mcp.sentry.dev/mcp` | OAuth | 16+ tools |
| **Database** | Supabase | `https://mcp.supabase.com/mcp?project_ref=YOUR_REF` | OAuth | — |
| **Knowledge Search** | QMD (`@tobi/qmd`) | `npx -y @tobi/qmd` | None (on-device) | On-device semantic search over Obsidian vault |

#### How to Find MCPs

1. Check the service's official docs for "MCP"
2. Browse [mcpservers.org](https://mcpservers.org)
3. GitHub search `"[service name] mcp server"`

#### Configuration Format

Add each MCP to `.claude/settings.local.json`:

```json
{
  "mcpServers": {
    "sentry": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.sentry.dev/mcp"],
      "env": {}
    }
  }
}
```

> See [relay-mcp-pattern.md](../skill-templates/relay-mcp-pattern.md) for the full relay agent skill template and connection details.

Add all relevant MCPs **before starting development.** Each MCP gets a corresponding relay agent (see [02-agent-teams.md](02-agent-teams.md) — MCP Agent Architecture).

### 1d. Define Architecture

Document workspace layout, data flow, service accounts, and isolation boundaries.
If this is a sister workspace alongside existing infrastructure, define the hard rule:

> *The {project} workspace MUST NOT modify ANY existing workspace, database, table, cron job, worker, or code — unless specifically directed by the owner.*

### 1e. Define Vertical Slices

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
**Priority:** P0 (revenue-critical) | P1 (important) | P2 (nice-to-have) — determines test coverage requirements (Article 20)
```

For each slice, define the exact file map before implementation begins (Nuclear Rule 9). See Article 30 for the file map format.

### 1f. Plan-Stage Peer Review

Before any code, the full plan goes through multi-model peer review:
1. Claude self-reflects on the plan
2. Plan sent to Gemini, OpenAI 5.5, Claude Opus 4.7, Grok for independent review
3. Consensus issues (2+ models agree) = mandatory fixes
4. Owner signs off on final plan
