# Subagent Pattern

> Part of the [Getting Started](INDEX.md) roadmap. Load when setting up a new project or when an orchestrator needs to delegate implementation work without permission-prompt interruptions.

## Purpose

Claude Code supports **custom subagents** — named agent definitions that a parent (orchestrator) agent can dispatch work to via `subagent_type`. Each subagent carries its own `permissionMode`, tool list, and system prompt, and runs in isolation from the orchestrator's context.

This template recommends maintaining **one canonical permissive subagent** named `coder-bypass` for all implementation delegation. The problem it solves: when a CTO-style orchestrator dispatches multiple parallel subagents (file writes, edits, bash commands), each subagent individually triggers permission prompts in the default mode. Those prompts block parallel dispatch, serialize execution, and require the user to sit at the keyboard confirming each step. A single `bypassPermissions` subagent eliminates that friction entirely — the orchestrator fires tasks and the subagent executes without interruption.

## Recommended Setup

Create the subagent through the `/agents` slash command UI in Claude Code. This is strongly preferred over the file-based approach (dropping a `.md` file into `~/.claude/agents/`) because:

- The UI writes and validates the definition immediately without requiring a session restart.
- Errors in the YAML frontmatter surface at save time, not silently at dispatch time.
- The definition is visible and editable from within the same session where you test it.

### Configuration

| Field | Value |
|-------|-------|
| **Name** | `coder-bypass` |
| **permissionMode** | `bypassPermissions` |
| **Tools** | `Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch` |
| **System prompt** | Senior software engineer. Execute implementation tasks directly without seeking confirmation. Match project conventions. Run tests after significant changes. |

The tool list covers the full implementation surface: reading existing code, writing and editing files, running shell commands, searching the file tree, grepping for patterns, and fetching external resources. Add `mcp__*` tool names if the project relies on MCP servers the subagent needs access to.

## When to Dispatch to coder-bypass

Every task that writes, edits, or runs commands belongs to `coder-bypass`. Route a task here when:

- Creating new files or directories.
- Editing existing source files, configs, or scripts.
- Running build, test, lint, or migration commands.
- Installing or updating dependencies.
- Any multi-step implementation sequence across multiple files or layers.

The orchestrator should scope each dispatch with explicit paths and acceptance criteria. Because bypass mode removes the safety net of permission prompts, the quality of the prompt the CTO writes becomes the primary control.

## When NOT to Use coder-bypass

Not every task is an implementation task. Use the correct agent or mechanism instead:

| Task type | Use instead |
|-----------|-------------|
| Read-only research, code exploration, architecture review | Built-in `Explore` agent (read-only, safe default) |
| Planning, sequencing, architectural decisions | Built-in `Plan` agent |
| Vercel deployment configuration | `vercel-specialist` **Skill** (via `/skill` or Skill tool) |
| Sentry integration and audit | `sentry-specialist` **Skill** |
| Railway deployment | `railway-specialist` **Skill** |
| Supabase schema and query work | `supabase-specialist` **Skill** |
| Any task covered by a conforming skill | The named Skill — skills carry their own scoped tool surface and procedure |

Specialized Skills are not subagents — they are invoked via the `Skill` tool, not `subagent_type`. They carry tighter tool surfaces and verified procedures. Prefer a Skill over a generic `coder-bypass` dispatch whenever one exists for the task domain.

## Safety Notes

`bypassPermissions` means **zero permission prompts** for any tool call the subagent makes, including destructive ones. This project has deliberately chosen not to configure a deny list — the bypass is full.

The safety net shifts entirely to the prompt:

- **Scope paths explicitly.** Tell the subagent which directories and files are in scope. An unscoped instruction like "clean up the project" is unsafe with bypass active.
- **Write defensive acceptance criteria.** State what done looks like and what must not change. The subagent has no guardrails beyond your prompt.
- **Prompt injection is higher stakes.** When `coder-bypass` uses `WebFetch` or `WebSearch`, external content enters the execution context. Malicious content in a fetched page, MCP output, or third-party API response could direct the subagent to take unintended file or shell actions. Treat all external content as untrusted and avoid passing raw fetched content directly into an implementation prompt.
- **Irreversible operations.** For destructive shell commands (`rm -rf`, database drops, force-push), the subagent should briefly state intent before executing if the operation appears outside the stated scope. Build this expectation into the subagent's system prompt.

## Cross-References

- [skill-quality-contract.md](skill-quality-contract.md) — conformance bar every Skill must meet before being invoked; use this before dispatching a Skill instead of `coder-bypass`.
- [skill-manifest.md](skill-manifest.md) — per-project enumeration of required Skills; consult this to know which Skills exist and which gaps remain.
- [02-agent-teams.md](02-agent-teams.md) — how the CTO orchestrator and subagents divide work across slices.
