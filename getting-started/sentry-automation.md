# Sentry Automation — Hands-Free Error Monitoring

Three options for wiring Sentry so Claude doesn't need a manual "go check Sentry" prompt.

---

## Option 1: Sentry to GitHub Issues (recommended for solo dev)

Configured entirely inside Sentry's UI — no custom code needed.

**Setup (5 steps):**
1. In Sentry: Settings > Integrations > GitHub > Install.
2. Enable "Create a GitHub issue for every new Sentry issue" in the integration settings.
3. Map the Sentry project to the correct GitHub repo.
4. Set alert rules: "New issue" or "First seen in release" triggers the issue.
5. Claude Code (or any scheduled agent) polls `gh issue list --label sentry` to pick up new errors.

**Tradeoffs:**
- Cleanest for solo dev — no hosted endpoint required.
- GitHub Issues are permanent; noisy if Sentry fires often.
- Requires GitHub integration permission in your Sentry org.

---

## Option 2: /schedule running relay-sentry MCP poll

Runs a periodic in-Claude-Code agent that calls `relay-sentry` to check for new issues.

**Setup (3 steps):**
1. Ensure `relay-sentry` skill is installed and `SENTRY_AUTH_TOKEN` is exported.
2. Open Claude Code and run:
   `/schedule every 30m "Use relay-sentry to check for new Sentry issues on project my-project and report any new errors since the last check."`
3. Claude will wake up on the schedule, query Sentry, and surface any new issues inline.

**Tradeoffs:**
- Fully in-Claude-Code — no external webhook endpoint needed.
- Interval is configurable (30 min is a good default during active development).
- Only fires while Claude Code is running; does not persist across restarts without a cron.

---

## Option 3: Sentry Webhook to Custom Intake (advanced)

Sentry POSTs to a hosted function; the function writes to a queue Claude polls.

**Setup (4 steps):**
1. Deploy a small Cloud Run or Vercel function that accepts POST from Sentry and writes
   `incoming-issues/<timestamp>.md` to the repo (via GitHub API or direct file write).
2. In Sentry: Settings > Integrations > Webhooks > Add webhook URL pointing at your function.
3. Set the webhook to fire on "issue created" and "issue regression" events.
4. Schedule a Claude agent (via `/schedule`) to poll `incoming-issues/` and triage new files.

**Tradeoffs:**
- Most robust — works even when Claude Code is not running.
- Requires a hosted endpoint (Cloud Run, Vercel serverless, etc.) and HTTPS.
- Adds infra complexity; overkill for solo dev unless you need 24/7 coverage.

---

## Default Recommendation for This Template

Use **Option 1 + Option 2** together:

- Option 1 (Sentry to GitHub Issues) gives a permanent, searchable record of every error.
- Option 2 (scheduled relay-sentry poll) surfaces errors interactively while you develop.

Together they provide hands-free monitoring with no hosted infrastructure required.
Set the schedule interval to 30 minutes during active sprints; increase to 2 hours otherwise.
