# Step 3 (continued): Slice 0 Tooling Install

> Companion to [03-slice-0-bootstrap.md](03-slice-0-bootstrap.md). Load this file when executing tooling install steps (Sentry SDK, Sentry CLI, structured logging, linter, MCP servers).

---

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

---

#### 3g-ii. Install Sentry CLI (required for CI release tagging)

Install the CLI globally so CI can create releases, link commits, and upload sourcemaps:

```bash
npm install -g @sentry/cli
# or: curl -sL https://sentry.io/get-cli/ | bash
```

Verify auth works (export `SENTRY_AUTH_TOKEN` first):
```bash
export SENTRY_AUTH_TOKEN=<token-from-sentry.io/settings/account/api/auth-tokens/>
sentry-cli info    # must succeed before proceeding
```

Wire `scripts/sentry-release.sh` into every CI deploy job (after build, before smoke tests). The script runs all four CLI commands in the correct order and skips sourcemap upload when `SOURCEMAP_DIR` is unset. See `contract-templates/SENTRY-CLI-TEMPLATE.md` for full CLI details.

---

### 3h. Set Up Persistence (Choose Your Approach)

Choose a cross-session memory strategy:
- **Option A (recommended):** QMD + Obsidian vault — on-device semantic search over markdown files stored in Obsidian. No cloud dependency. Install [QMD MCP](https://github.com/tobi/qmd), point it at your Obsidian vault.
- **Option B:** Plain Markdown files in `learnings/` — simplest approach, no search, just file organization.

---

### 3i. Verify UserPromptSubmit Hook (Nuclear Rule 10)

> Full check script and JSON template: [`03a-userpromptsubmit-hook.md`](03a-userpromptsubmit-hook.md)

Verify `~/.claude/settings.json` has a `UserPromptSubmit` hook that reminds Claude to delegate all implementation to sub-agents. If missing, add it using the template in the companion file.

**Gate:** Do NOT proceed past Slice 0 until the hook check returns `OK`.
