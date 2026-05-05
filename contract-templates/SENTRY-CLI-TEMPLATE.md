# Sentry CLI Contract — {PROJECT_NAME}

> For SDK setup (three-layer init, redaction, boundary enrichment), see [SENTRY-TEMPLATE.md](SENTRY-TEMPLATE.md). The CLI complements the SDK; both are required.

The Sentry CLI handles release tagging, commit linking, and sourcemap upload. It is distinct from the SDK (runtime capture) covered in SENTRY-TEMPLATE.md.

---

## Install

```bash
npm install -g @sentry/cli
# or via one-liner: https://docs.sentry.io/cli/installation/
curl -sL https://sentry.io/get-cli/ | bash
```

---

## Auth

Export `SENTRY_AUTH_TOKEN` before any CLI command. Mint a token at:
`https://sentry.io/settings/account/api/auth-tokens/` (scope: `project:releases`, `org:read`).
Never hardcode the token.

```bash
export SENTRY_AUTH_TOKEN=<token>
export SENTRY_ORG=<your-org-slug>
export SENTRY_PROJECT=<your-project-slug>
```

Run `sentry-cli info` (with `SENTRY_AUTH_TOKEN` exported) to verify auth before CI wires these steps.

---

## Required CI Commands (run in this order on every deploy)

```bash
# 1. Create the release (RELEASE = git SHA, must match SDK release field)
sentry-cli releases new $RELEASE

# 2. Link commits so Sentry shows which commits are in the release
sentry-cli releases set-commits --auto $RELEASE

# 3. Upload sourcemaps (frontend only; skip if no build output)
sentry-cli sourcemaps upload --release $RELEASE <build-output-dir>

# 4. Finalize — marks the release as deployed
sentry-cli releases finalize $RELEASE
```

---

## Release String Tie-In Rule

The `$RELEASE` value used in all four commands MUST exactly match the `release` field
passed to `Sentry.init()` across all three SDK layers (see [SENTRY-TEMPLATE.md](SENTRY-TEMPLATE.md)
Required Behaviors row 10 and [Article 20e-2](articles/article-20e-2-distributed-tracing.md)).

A mismatch means Sentry cannot correlate sourcemaps and commits with captured events.

---

## Script Encapsulation

All four commands are encapsulated in `scripts/sentry-release.sh`. Wire that script into
your CI deploy job (after build, before smoke tests). The script skips sourcemap upload
when `SOURCEMAP_DIR` is unset.

---

## Verification

Run `sentry-cli info` after setting `SENTRY_AUTH_TOKEN` — must succeed before CI wires
these steps. After the first deploy, confirm in the Sentry UI that the release appears
with linked commits and (if applicable) sourcemaps.

---

Reference: https://docs.sentry.io/cli/
