# Frontier-Orchestrated Development Workflow

This is the single source of truth for AI-assisted work in this repository.
Provider-specific instruction files may summarize it, but may not override it.

## 1. Authority

- Exactly one orchestrator is active at a time.
- The orchestrator must be Claude Fable 5 or GPT-5.6 Sol.
- Fable 5 is the default.
- Sol becomes orchestrator only when the user selects it, Fable is unavailable,
  or the data policy disallows Fable but permits Sol.
- The editor or terminal in which a session starts does not choose the orchestrator.
- Sonnet and Haiku are workers. They may flag risk, but may not delegate, approve,
  downgrade risk, or declare completion.

## 2. Model Routing

| Model | Use |
|---|---|
| Claude Fable 5 | Default orchestration, architecture, ambiguity, integration, high-consequence decisions, difficult debugging, and final delivery |
| GPT-5.6 Sol | Alternate orchestration, independent frontier review, and user-approved fallback |
| Claude Sonnet 5 | Clear, bounded implementation, tests, fixes, and refactors that follow established patterns |
| Claude Haiku 4.5 | Search, summarization, inventories, log reduction, formatting, and small edits whose correctness is mechanically provable |

Escalate from a worker after two total attempts. Use a frontier model directly when
judgment, ambiguity, or consequence dominates the task.

## 3. Risk Classification

The orchestrator classifies risk before implementation. `scripts/gate_check.py`
also scans changed paths and diff content using `workflow.config.json`.

High-risk work includes:

- authentication, authorization, permissions, secrets, or cryptography;
- payments, financial calculations, or private data;
- schema changes, migrations, destructive SQL, or irreversible operations;
- infrastructure, deployments, CI permissions, or public API contracts;
- broad cross-system architecture.

Workers may raise a risk flag at any time. A mechanical trigger always upgrades the
change to high-risk. Only the user may downgrade it, and the orchestrator must not
solicit a downgrade. The reason must be recorded.

The downgrade record must be committed at
`reviews/<change-id>.downgrade.json`; copy `risk-downgrade.example.json`.

## 4. Normal Workflow

1. Orchestrator states the goal, acceptance criteria, allowed paths, and checks.
2. Orchestrator performs the work or assigns a bounded task to Sonnet or Haiku.
3. Run every command in `checks.normal`.
4. Orchestrator reconciles the diff and check results against the acceptance criteria.
5. Deliver. Do not create an AI-review artifact.

Metrics may be written to the gitignored path configured in `records.metrics_file`.

## 5. High-Risk Workflow

1. Orchestrator records requirements, triggers, failure modes, and rollback steps.
2. The other frontier model reviews the original requirements without the author's
   narrative or conclusions.
3. Implementation proceeds with one writer per worktree.
4. Run all normal checks plus all `checks.high_risk` commands.
5. The non-author frontier model reviews the raw diff and raw verification output.
6. That reviewer controls sign-off. The author or orchestrator cannot override it.
7. Unresolved disagreement goes to the user.
8. Save one JSON record in the configured high-risk review directory.

The high-risk record must identify the author and reviewer models, contain approved
plan and diff verdicts, bind approval to the current diff SHA-256, include verification
results, and contain demonstrated rollback evidence.

An author model cannot be blank. Untracked files larger than 1,000,000 bytes, or
untracked files that cannot be read, stop the gate instead of being omitted from
the review fingerprint.

## 6. Refusals, Outages, and Privacy

- A refusal is not an outage. Stop, show the refusal to the user, and do not retry
  through another provider without explicit user approval.
- On an outage, orchestration may transfer after a verified handoff.
- If both frontier models are unavailable, freeze the state and stop before any
  irreversible operation. Human continuation requires explicit user authorization.
- Apply the data policy before sending repository content to a provider.
- If no approved frontier satisfies the retention policy, stop for human direction.

## 7. Handoffs and Parallel Work

A handoff records: goal, acceptance criteria, decision rationale, completed and open
work, changed and uncommitted files, worktree ownership, commands and results, risks,
and refusal/outage state.

The receiving orchestrator must compare the handoff with the repository diff and
rerun relevant checks before continuing. Remove the handoff file after reconciliation
is accepted so it cannot affect later work.

Parallel writers must use separate worktrees and non-overlapping path ownership.
The orchestrator owns merge order. After integration, rerun the full applicable gate.

## 8. Rollback

- Normal code-only changes use commit reversion or a verified feature-flag off path.
- High-risk work must demonstrate rollback in a safe environment before release.
- A forward-only migration requires a tested recovery procedure instead of a fictional
  down migration.
- Failed deployment, failed smoke test, or a new critical runtime error triggers
  rollback unless the user explicitly directs otherwise.

## 9. Cost Controls

- Normal work: one worker attempt plus one retry; no frontier peer review.
- High-risk work: one plan review, one final-diff review, and at most one scoped
  follow-up.
- Do not rerun a full review when only a corrected area needs verification.
- Stop at any configured token or monetary ceiling and report the current state.

## 10. Completion

Completion means:

- acceptance criteria are satisfied;
- the applicable gate passes;
- no worker is claiming orchestration or approval;
- high-risk work has independent non-author frontier sign-off;
- rollback and handoff requirements are satisfied where applicable.
