#!/usr/bin/env bash
# sentry-release.sh — Wire a new release into Sentry: create, link commits,
# upload sourcemaps (optional), and finalize.
#
# Required env vars:
#   SENTRY_AUTH_TOKEN  — CLI auth token (mint at sentry.io/settings/account/api/auth-tokens/)
#   SENTRY_ORG         — organization slug (e.g., "acme")
#   SENTRY_PROJECT     — project slug (e.g., "my-app-backend")
#
# Optional env vars:
#   RELEASE            — release identifier (defaults to current git SHA)
#   SOURCEMAP_DIR      — path to sourcemap build output; skip upload if unset
#
# Usage:
#   SENTRY_AUTH_TOKEN=xxx SENTRY_ORG=acme SENTRY_PROJECT=my-app \
#     SOURCEMAP_DIR=dist/static ./scripts/sentry-release.sh

set -euo pipefail

# ---------------------------------------------------------------------------
# Validate required env vars
# ---------------------------------------------------------------------------
missing=()
[[ -z "${SENTRY_AUTH_TOKEN:-}" ]] && missing+=("SENTRY_AUTH_TOKEN")
[[ -z "${SENTRY_ORG:-}"        ]] && missing+=("SENTRY_ORG")
[[ -z "${SENTRY_PROJECT:-}"    ]] && missing+=("SENTRY_PROJECT")

if [[ ${#missing[@]} -gt 0 ]]; then
  echo "ERROR: Missing required env vars: ${missing[*]}"
  echo "  SENTRY_AUTH_TOKEN — CLI token from sentry.io/settings/account/api/auth-tokens/"
  echo "  SENTRY_ORG        — org slug"
  echo "  SENTRY_PROJECT    — project slug"
  exit 1
fi

# ---------------------------------------------------------------------------
# Resolve release string
# ---------------------------------------------------------------------------
RELEASE="${RELEASE:-$(git rev-parse HEAD)}"
echo "==> Sentry release: $RELEASE (org: $SENTRY_ORG, project: $SENTRY_PROJECT)"

# ---------------------------------------------------------------------------
# Step 1: Create the release
# ---------------------------------------------------------------------------
echo "==> [1/4] Creating release..."
sentry-cli releases new "$RELEASE" \
  --org "$SENTRY_ORG" \
  --project "$SENTRY_PROJECT"

# ---------------------------------------------------------------------------
# Step 2: Link commits
# ---------------------------------------------------------------------------
echo "==> [2/4] Linking commits..."
sentry-cli releases set-commits --auto "$RELEASE" \
  --org "$SENTRY_ORG"

# ---------------------------------------------------------------------------
# Step 3: Upload sourcemaps (optional)
# ---------------------------------------------------------------------------
if [[ -n "${SOURCEMAP_DIR:-}" ]]; then
  echo "==> [3/4] Uploading sourcemaps from: $SOURCEMAP_DIR"
  sentry-cli sourcemaps upload \
    --release "$RELEASE" \
    --org "$SENTRY_ORG" \
    --project "$SENTRY_PROJECT" \
    "$SOURCEMAP_DIR"
else
  echo "==> [3/4] SOURCEMAP_DIR not set — skipping sourcemap upload."
fi

# ---------------------------------------------------------------------------
# Step 4: Finalize the release
# ---------------------------------------------------------------------------
echo "==> [4/4] Finalizing release..."
sentry-cli releases finalize "$RELEASE" \
  --org "$SENTRY_ORG"

echo "==> Done. Release '$RELEASE' is live in Sentry."
