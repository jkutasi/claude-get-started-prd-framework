# Codex Project Instructions

Read and follow [WORKFLOW.md](WORKFLOW.md). It is the single source of truth.

Only GPT-5.6 Sol or Claude Fable 5 may orchestrate. When this repository is opened
with another model, operate only as a bounded worker and do not approve completion.

Before changing files:

1. Classify the change as normal or high-risk using `workflow.config.json`.
2. Apply the provider data policy.
3. State acceptance criteria and verification commands.

Before delivery, run:

```text
python scripts/gate_check.py --change-id <id> --orchestrator sol
```

Use `--orchestrator fable` only when Claude Fable 5 is the active orchestrator.
