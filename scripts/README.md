# Workflow Scripts

## Completion Gate

```text
python scripts/gate_check.py --change-id <id> --orchestrator fable
```

Options:

- `--orchestrator fable|sol`: required active orchestrator.
- `--risk auto|normal|high`: defaults to mechanical detection.
- `--base <revision>`: compare against a branch or commit.
- A user-approved risk downgrade must be committed at
  `reviews/<change-id>.downgrade.json`; `--downgrade-record` is retained only as
  a compatibility check and cannot point elsewhere.
- `--tokens-used <n>` and `--cost-usd <amount>`: required when corresponding
  configuration ceilings are set.
- `--no-metrics`: do not append to the gitignored metrics log.

The gate:

1. Loads `workflow.config.json` plus optional `workflow.config.local.json`.
2. Applies provider and retention policy.
3. Detects high-risk paths and diff content.
4. Rejects overlapping active ownership claims.
5. Runs normal checks and, for high-risk work, targeted checks.
6. Validates `reviews/<change-id>.json` for independent sign-off and rollback evidence.

Review records require a named author model. Untracked files larger than
1,000,000 bytes—or files that cannot be read—stop the gate and must be resolved;
they are never silently excluded from the review fingerprint.

## GPT-5.6 Sol Review

```text
python scripts/sol_review.py plan \
  --requirements requirements.md \
  --input plan.md

python scripts/sol_review.py diff \
  --requirements requirements.md \
  --input diff-and-checks.txt
```

`OPENAI_API_KEY` is required. The default comes from
`models.alternate_orchestrator`; `OPENAI_REVIEW_MODEL` or `--model` may explicitly
override it. Provider and retention policy is checked before transmission. Exit
codes: `0` approve, `2` changes requested, `3` refusal, `1` error.

## Markdown Links

```text
python scripts/check_markdown_links.py
```

Tracked and untracked Markdown files are checked. External links and placeholder
paths are skipped.
