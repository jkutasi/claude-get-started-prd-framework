---
name: frontier-workflow
description: "Apply the repository's normal/high-risk workflow, model routing, and deterministic gate."
disable-model-invocation: true
---

# Frontier Workflow

Read `WORKFLOW.md` and `workflow.config.json`. They are authoritative.

Before implementation:

1. Identify the active frontier orchestrator.
2. Apply provider data policy.
3. Run or inspect mechanical risk detection.
4. State acceptance criteria, owned paths, and verification commands.

Before delivery:

1. Run `python scripts/gate_check.py --change-id <id> --orchestrator <fable|sol>`.
2. For high-risk work, confirm the non-author frontier model signed the consolidated record.
3. Report the risk level, checks, rollback state, and any user-approved exception.
