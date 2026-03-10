# Security Contract -- {PROJECT_NAME}

## API Key Management

### Production Environment

All secrets are stored in **{SECRET_MANAGER_PROVIDER}** (e.g., GCP Secret Manager, AWS Secrets Manager, Azure Key Vault). No secrets in code, config files, environment variables on servers, or CI/CD logs.

| Secret | Secret Manager Key | Rotation Schedule | Owner |
|--------|-------------------|-------------------|-------|
| `{SECRET_1_NAME}` | `{SECRET_1_KEY}` | {ROTATION_SCHEDULE} | {OWNER} |
| `{SECRET_2_NAME}` | `{SECRET_2_KEY}` | {ROTATION_SCHEDULE} | {OWNER} |
| `{SECRET_3_NAME}` | `{SECRET_3_KEY}` | {ROTATION_SCHEDULE} | {OWNER} |

### Development Environment

For local development ONLY, secrets are stored in `.env` files. These files are gitignored and MUST NEVER be committed.

```
# .env (local dev only — NEVER commit this file)
{SECRET_1_NAME}={DEV_VALUE}
{SECRET_2_NAME}={DEV_VALUE}
{SECRET_3_NAME}={DEV_VALUE}
{ERROR_TRACKING_DSN}={DEV_VALUE}
```

`.env` MUST be listed in `.gitignore`. If `.env` appears in a diff or commit, it is a CRITICAL security violation.

---

## Peer Review API Keys

These keys are used by the multi-model peer review system (Article 3). They are REQUIRED for the development workflow and must be available in `.env` for local dev:

| Key | Purpose | Provider | Required For |
|-----|---------|----------|-------------|
| `GEMINI_API_KEY` | Peer reviewer #1 | Google AI | Peer review (Article 3, 12b) |
| `OPENAI_API_KEY` | Peer reviewer #2 | OpenAI Codex | Peer review (Article 3, 12b) |
| `XAI_API_KEY` | Peer reviewer #3 | xAI (Grok) | Peer review (Article 3, 12b) |
| `GREPTILE_API_KEY` | Peer reviewer #4 (optional) | Greptile | Peer review (Article 3, 12b) — codebase-aware review |

The first 3 keys are NOT optional. Without them, peer review cannot run, and peer review is a Nuclear Rule. `GREPTILE_API_KEY` is optional — if configured, Greptile runs as a 4th reviewer alongside Gemini, Codex, and Grok. See Article 12b for how to run peer review step-by-step.

---

## Service Accounts and Access Levels

| Service Account | Purpose | Access Level | Data Access | Environment |
|----------------|---------|-------------|-------------|-------------|
| `{SERVICE_ACCOUNT_1}` | {PURPOSE} | {READ/WRITE/ADMIN} | {WHAT_DATA} | {PROD/DEV/BOTH} |
| `{SERVICE_ACCOUNT_2}` | {PURPOSE} | {READ/WRITE/ADMIN} | {WHAT_DATA} | {PROD/DEV/BOTH} |
| `{SERVICE_ACCOUNT_3}` | {PURPOSE} | {READ/WRITE/ADMIN} | {WHAT_DATA} | {PROD/DEV/BOTH} |

**Principle of least privilege:** Each service account has the MINIMUM access required for its function. No shared accounts. No wildcard permissions.

---

## Data Access Boundaries (Article 9)

> This section applies when the project is a sister workspace to an existing master project.

- This project MUST NOT modify any existing workspace, database, table, cron job, worker, or code in existing workspaces -- unless specifically directed by the owner.
- NO writes to: {EXISTING_DATA_STORES}
- NO modifications to: {EXISTING_SERVICES}
- The ONLY data stores this project writes to: {NEW_DATA_STORES}
- If the project discovers issues with existing infrastructure: REPORT to the owner. Do NOT fix.
- The owner may override any boundary with explicit direction.

---

## External API Security

| External API | Rate Limit | Auth Method | Token Rotation | Failure Mode |
|-------------|-----------|-------------|----------------|-------------|
| `{API_1_NAME}` | {REQUESTS_PER_MINUTE} | {API_KEY/OAUTH/JWT} | {ROTATION_SCHEDULE} | {RETRY/CIRCUIT_BREAKER/FALLBACK} |
| `{API_2_NAME}` | {REQUESTS_PER_MINUTE} | {API_KEY/OAUTH/JWT} | {ROTATION_SCHEDULE} | {RETRY/CIRCUIT_BREAKER/FALLBACK} |
| `{API_3_NAME}` | {REQUESTS_PER_MINUTE} | {API_KEY/OAUTH/JWT} | {ROTATION_SCHEDULE} | {RETRY/CIRCUIT_BREAKER/FALLBACK} |

**Rate limit enforcement:** All external API calls MUST implement rate limiting on the client side. Do not rely on the provider's rate limit response -- proactively throttle.

**Token rotation:** All API tokens MUST be rotated on the schedule above. Rotation is automated via {ROTATION_METHOD}.

---

## OWASP Top 10 Checklist

Every slice MUST be evaluated against the OWASP Top 10 during QA Security review (Article 4, agent #4):

| # | Vulnerability | Status | Mitigation |
|---|--------------|--------|-----------|
| A01 | Broken Access Control | {PASS/FAIL/NA} | {MITIGATION_DESCRIPTION} |
| A02 | Cryptographic Failures | {PASS/FAIL/NA} | {MITIGATION_DESCRIPTION} |
| A03 | Injection | {PASS/FAIL/NA} | {MITIGATION_DESCRIPTION} |
| A04 | Insecure Design | {PASS/FAIL/NA} | {MITIGATION_DESCRIPTION} |
| A05 | Security Misconfiguration | {PASS/FAIL/NA} | {MITIGATION_DESCRIPTION} |
| A06 | Vulnerable Components | {PASS/FAIL/NA} | {MITIGATION_DESCRIPTION} |
| A07 | Auth Failures | {PASS/FAIL/NA} | {MITIGATION_DESCRIPTION} |
| A08 | Data Integrity Failures | {PASS/FAIL/NA} | {MITIGATION_DESCRIPTION} |
| A09 | Logging & Monitoring Failures | {PASS/FAIL/NA} | {MITIGATION_DESCRIPTION} |
| A10 | SSRF | {PASS/FAIL/NA} | {MITIGATION_DESCRIPTION} |

---

## Absolute Prohibitions

1. **No secrets in code.** No API keys, passwords, tokens, or connection strings hardcoded in any source file. Ever.
2. **No secrets in logs.** Logging statements MUST NOT include secrets, tokens, passwords, or PII. Sanitize all log output.
3. **No secrets in error messages.** Error messages returned to users or written to logs MUST NOT expose internal secrets, stack traces with credentials, or connection strings.
4. **No secrets in commits.** If a secret is accidentally committed, it is considered COMPROMISED and must be rotated immediately -- even if the commit is reverted.
5. **No secrets in CI/CD output.** Build logs, test output, and deployment logs MUST NOT contain secrets.
6. **No secrets in ANY file pushed to GitHub.** Before every push, verify that no file containing API keys, tokens, passwords, connection strings, or credentials is staged. This includes `.env` files, API key reference docs, credential dumps, and any file with literal key values. The `.gitignore` MUST exclude: `.env*`, `*.local`, `API Keys/`, and any path containing credentials. If in doubt, do NOT push — ask first.

---

## Pre-Push Public Repository Checklist

**This repository may be PUBLIC.** Before every push to GitHub, the CTO (or pushing agent) MUST verify:

| # | Check | How to Verify |
|---|-------|---------------|
| 1 | No secrets in any staged file | Husky pre-push hook (automated) + `git diff origin/{main}..HEAD` — scan for API keys, tokens, passwords, connection strings, hardcoded URLs with credentials (`user:pass@host`), OAuth tokens in test fixtures, secrets in comments (`// password was...`), connection string URIs |
| 2 | No `.env` files staged | `git status` — `.env*` must be in `.gitignore` |
| 3 | No proprietary business data | No client names, financial data, internal strategies, or trade secrets |
| 4 | No unnecessary files | No scratch files, temp files, `ZZ *` folders, personal notes |
| 5 | No credential reference docs | No files listing "where to find the API key" with actual values |
| 6 | `.gitignore` is comprehensive | Must exclude: `.env*`, `*.local`, `output/`, `ZZ *`, `API Keys/`, `*credentials*`, `*secrets*` |
| 7 | No stale/dead files | Files no longer used by the project should be deleted, not left in the repo |
| 8 | No internal-only documentation | Meeting notes, internal memos, proprietary process docs not meant for public |

**If ANY check fails: DO NOT PUSH. Fix first, then re-verify.**

> This checklist applies to EVERY push, not just slice completion pushes. Quick fixes, doc updates, and template changes all go through this gate.

---

## Nuclear Rules Reminder

These nine rules override everything else. Violation = immediate stop.

1. **CTO Never Writes Code.** All code via teammates and sub-agents. No exceptions.
2. **Peer Review Is Mandatory.** Every slice, every time. All reviewers must report. No partial reviews.
3. **Slices Ship Complete.** All gates passed, all artifacts on disk, or the slice is invalid. The user only sees completed, fully-vetted slices. Never present unreviewed work and never defer QA to "after user tests."
4. **Repository Hygiene Before Push.** Before ANY push, verify no personal notes, scratch files, or `ZZ *` folders are staged. `.gitignore` must exclude these paths. This repository may be PUBLIC — verify no secrets, proprietary data, credentials, stale files, or internal-only content is staged. Run the Pre-Push Public Repo Checklist (above).
5. **One Concern Per Sub-Agent — Then It Dies.** Every sub-agent gets one concern, does it, and is dismissed. No reuse.
6. **No Hacking — No Lint Ignores.** All lint/type errors are bugs. No `# noqa`, `eslint-disable`, `# type: ignore`. Fix properly.
7. **Never Commit or Push Without Checking Runtime Errors.** Check error tracker, logs, and health endpoints before commit. After push: check Sentry for new errors, Vercel deployment logs for failures, and Greptile for codebase-aware findings.
8. **Slices Ship One at a Time.** Slice N fully complete before Slice N+1. Parallel within a slice = good. Parallel slices = bad.
9. **File Structure Defined Before Implementation.** Planning phase defines exact file map. Sub-agents build to the map.

Security is enforced at every layer: code review (Article 3), QA Security agent (Article 4), Red Team (Article 14), and this contract. If a security issue is found at any layer, it is a blocking fix.
