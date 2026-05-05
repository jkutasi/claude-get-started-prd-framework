# Article 39: Deploy SHA Verification

> Part of the [Contract Articles](INDEX.md). Load only when you need this article.
>
> **Cross-references:** Article 7 (Slice Completion), Article 27 (Post-Work Hygiene),
> Article 38 (DB Smoke — Synthetic UNION ALL)

## The Rule

Phase J and Post-Push smoke tests MUST verify that the deploy provider's
reported running commit SHA matches `git rev-parse HEAD` BEFORE running any
smoke assertion. A SHA mismatch means the smoke is testing the wrong code.
When a mismatch is detected, abort the smoke and investigate — do not proceed.

## Why It Matters

`git push` is not a deploy. Three common failure modes silently leave the wrong
code running in production:

1. **CI build skipped or failed** — the push triggered no build, so the
   previous image kept serving traffic.
2. **Provider auto-rollback** — the new deploy crashed on startup and the
   platform rolled back to the last healthy release.
3. **Multi-environment confusion** — the smoke URL points to staging while the
   push targeted production, or vice versa.

In all three cases, smoke assertions that pass produce false confidence: every
check is green, but none of it applies to the commit you just shipped.

## Generic Pattern

```bash
verify_deploy_sha() {
  local EXPECTED_SHA="$1"          # typically: $(git rev-parse HEAD)
  local PROVIDER_SHA_CMD="$2"      # shell expression that prints the running SHA

  local RUNNING_SHA
  RUNNING_SHA=$(eval "$PROVIDER_SHA_CMD")

  if [ "$RUNNING_SHA" != "$EXPECTED_SHA" ]; then
    echo "ERROR: deploy SHA mismatch"
    echo "  expected : $EXPECTED_SHA"
    echo "  running  : $RUNNING_SHA"
    exit 1
  fi

  echo "SHA verified: $RUNNING_SHA"
}

# Usage
verify_deploy_sha "$(git rev-parse HEAD)" "<provider-specific command below>"
```

Pass `$EXPECTED_SHA` explicitly so the function is testable in CI without a
live git context.

## Provider-Specific Recipes

**Railway (GraphQL)**
```bash
curl -s -H "Authorization: Bearer $RAILWAY_TOKEN" \
  https://backboard.railway.app/graphql/v2 \
  -d '{"query":"{ deployments(first:1){ edges{ node{ meta } } } }"}' \
  | jq -r '.data.deployments.edges[0].node.meta.commitHash'
```

**Vercel (REST)**
```bash
curl -s -H "Authorization: Bearer $VERCEL_TOKEN" \
  "https://api.vercel.com/v6/deployments?projectId=$VERCEL_PROJECT_ID&limit=1" \
  | jq -r '.deployments[0].meta.githubCommitSha'
```

**Render (REST)**
```bash
curl -s -H "Authorization: Bearer $RENDER_API_KEY" \
  "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys?limit=1" \
  | jq -r '.[0].deploy.commit.id'
```

**Fly (REST)**
```bash
curl -s -H "Authorization: Bearer $FLY_API_TOKEN" \
  "https://api.fly.io/v1/apps/$FLY_APP_NAME/releases?per_page=1" \
  | jq -r '.[0].version'   # Fly exposes image tag; map to git SHA via image label
```

**GitHub Pages (commit polling)**
```bash
curl -s "https://api.github.com/repos/$GH_OWNER/$GH_REPO/pages/builds?per_page=1" \
  -H "Authorization: Bearer $GH_TOKEN" | jq -r '.[0].commit'
```

Adapt field paths as provider APIs evolve. The contract is: query the provider,
extract a SHA or equivalent identifier, compare to `git rev-parse HEAD`.

## Failure Mode

When SHA mismatch persists after a retry:

1. **Check the provider dashboard** — confirm the latest deploy status
   (building, failed, rolled back, or active).
2. **Confirm the push reached origin** — run `git log origin/<branch> -1`; if
   the remote tip does not match local HEAD, the push did not complete.
3. **Check CI logs** — a failed build step leaves the previous image running;
   fix the build before re-smoking.
4. **Do not mark smoke as passed.** A smoke run that skipped SHA verification
   has no validity and must be re-run after the SHA aligns.

## Cross-References

- **phase-j-gate-check.md** — Phase J gate requires SHA verification before
  any acceptance assertion.
- **Article 27 (Post-Work Hygiene)** — Post-Push routine repeats SHA
  verification each time Sentry or deploy logs indicate a new release event.
