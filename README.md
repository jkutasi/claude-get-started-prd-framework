# Frontier-Orchestrated Project Template

A lean software-development workflow led by Claude Fable 5 or GPT-5.6 Sol.
Routine work uses deterministic checks. Independent AI review is reserved for
changes with meaningful security, data, financial, infrastructure, or architectural risk.

The previous phase-based framework remains recoverable from Git commit
`e2f389fd939454302ecb59df8600ccb3dc2940c1`.

## Model Roles

| Model | Role |
|---|---|
| Claude Fable 5 | Default orchestrator |
| GPT-5.6 Sol | Alternate orchestrator and independent frontier reviewer |
| Claude Sonnet 5 | Bounded implementation worker |
| Claude Haiku 4.5 | Mechanically verifiable utility worker |

Sonnet and Haiku never approve completion or orchestrate other agents.

## Workflows

**Normal:** define acceptance criteria, implement, run configured checks, integrate,
and deliver. No AI-review artifact.

**High-risk:** the non-author frontier model reviews the plan and final diff, all
normal checks plus targeted checks run, rollback is demonstrated, and one consolidated
JSON record controls sign-off.

See [WORKFLOW.md](WORKFLOW.md) for the complete operating contract.

## Start a Project

1. Copy this template.
2. Customize [workflow.config.json](workflow.config.json):
   - verification commands;
   - provider and retention policy;
   - project-specific high-risk paths and diff patterns;
   - optional cost or token ceilings.
3. Use Fable 5 as orchestrator, or explicitly select GPT-5.6 Sol.
4. For high-risk work, copy [high-risk-review.example.json](high-risk-review.example.json)
   to `reviews/<change-id>.json` and replace every example value with evidence.
   The recorded diff SHA-256 must match the value printed by the gate.
5. Run the completion gate:

```text
python scripts/gate_check.py --change-id <id> --orchestrator fable
```

Use `--orchestrator sol` when Sol is active.

## Important Files

| File | Purpose |
|---|---|
| `WORKFLOW.md` | Single source of truth |
| `CLAUDE.md` | Claude entry instructions |
| `AGENTS.md` | Codex entry instructions |
| `workflow.config.json` | Models, privacy, risk, checks, and limits |
| `scripts/gate_check.py` | Risk-aware deterministic gate |
| `scripts/sol_review.py` | Direct GPT-5.6 Sol plan/diff reviewer |
| `workflow.handoff.example.json` | Cross-orchestrator handoff format |

## Safety Defaults

- A refusal stops for user review; it is never silently retried through another provider.
- A provider must be explicitly approved before repository content is sent to it.
- Fable is marked as incompatible with zero-data-retention projects by default.
- Parallel writers require separate worktrees and non-overlapping ownership.
- High-risk work cannot ship without non-author frontier sign-off.
