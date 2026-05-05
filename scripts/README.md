# scripts

## gate_check.py

Auto-discovers slices and verifies required artifacts exist before declaring a slice shipped.

Usage:
- `python scripts/gate_check.py --all` — verify every slice
- `python scripts/gate_check.py --slice 1` — verify just slice 1
- `python scripts/gate_check.py --all --strict` — also require optional artifacts

Exit code: 0 = all pass, 1 = any failure.

### Optional configuration file

Copy `gate_check.config.example.json` (repo root) to `gate_check.config.json` and fill
in your values. The actual config file is gitignored — never commit it.

```
cp gate_check.config.example.json gate_check.config.json
```

If the config file is absent or a section is missing, that check is silently skipped.
Artifact and test checks always run regardless of config.

### Enabling the Sentry check

1. Add a `sentry` block to `gate_check.config.json`:

```json
{
  "sentry": {
    "org": "my-org",
    "project": "my-project",
    "release_query": "git rev-parse HEAD",
    "since_minutes": 60
  }
}
```

2. Export your Sentry internal-integration token:

```
export SENTRY_AUTH_TOKEN=sntrys_...
```

If `SENTRY_AUTH_TOKEN` is not set and the `sentry` key is present in the config,
gate_check returns a failure — it assumes the check was intentionally enabled.

### Enabling the deploy SHA check

Add a `deploy` block with a `query` field — any shell command that prints the running
commit SHA to stdout. See `gate_check.config.example.json` for Railway, Vercel, Render,
and Fly templates.

## Module layout

| File | Purpose |
|------|---------|
| `gate_check.py` | Entrypoint: argparse, slice discovery, result printing. |
| `gate_check_artifacts.py` | Checks for required `reviews/slice-N-*.md` files. |
| `gate_check_tests.py` | Runs `pytest -q` when pytest + a config file are present. |
| `gate_check_deploy.py` | Compares `git rev-parse HEAD` to the deployed SHA. |
| `gate_check_sentry.py` | Scans Sentry for new issues on the current release. |

## openai_code.py

OpenAI Responses API coder helper. Wraps `POST /v1/responses` with three subcommands.

**Environment variables:**

| Variable | Required | Default |
|----------|----------|---------|
| `OPENAI_API_KEY` | Yes | — |
| `OPENAI_CODE_MODEL` | No | `gpt-5.5` |

**Subcommands:**

```bash
# Generate code from a spec and write to --output
python scripts/openai_code.py draft \
    --spec docs/slices/slice-1/spec.md \
    --files src/feature/sibling.py,src/feature/types.py \
    --conventions contract-templates/CONVENTIONS.md \
    --output src/feature/new_module.py

# Self-review generated code; exit 2 if REVISE
python scripts/openai_code.py review \
    --code src/feature/new_module.py \
    --spec docs/slices/slice-1/spec.md

# Fix code given a failure log; writes corrected code back to --code path
python scripts/openai_code.py fix \
    --code src/feature/new_module.py \
    --failures logs/test-failure.txt
```

**Module layout:**

| File | Purpose |
|------|---------|
| `openai_code.py` | CLI entrypoint: argparse, dispatches to lib functions. |
| `openai_code_lib.py` | HTTP call, prompt builders (draft / review / fix). |

## Other scripts

| File | Purpose |
|------|---------|
| `install-hooks.sh` | Installs git hooks (post-commit vault sync). |
| `sync-to-vault.sh` | Copies template content to the Obsidian vault. |
