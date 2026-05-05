# Article 2: Sub-Agent Code Authorship

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

## Canonical Authorship Chain

The CTO Orchestrator (Claude Opus 4.7 — smartest available Claude) spawns **Sonnet sub-agents**
with focused, one-task specs. Sonnet sub-agents are **thin courier shells**: they do NOT write
code themselves. Their job is to call OpenAI 5.5 for code generation, run self-review, write
results to disk, verify, and retry on failure.

Each agent gets ONE focused job (one function, one component, one review). Never a whole module
in one agent. Keep tasks small and focused — this preserves context quality and enables thorough
review.

## Sonnet Sub-Agent Execution Protocol

Every implementation sub-agent follows this loop using `scripts/openai_code.py`
(stdlib only — no pip installs required).

```bash
# 1. Draft: call OpenAI Responses API; write returned code to output path
python scripts/openai_code.py draft \
    --spec docs/slices/slice-N/spec.md \
    --files src/feature/sibling.py,src/feature/types.py \
    --conventions contract-templates/CONVENTIONS.md \
    --output src/feature/target_file.py

# 2. Self-review: check invariants, silent failures, security, 150-line compliance
#    Exit 0 = APPROVE. Exit 2 = REVISE (issues printed; re-run draft with issues appended).
python scripts/openai_code.py review \
    --code src/feature/target_file.py \
    --spec docs/slices/slice-N/spec.md

# 3. Verify: line count + lint + unit tests
python -m pytest tests/ -q && python -c "
n = len(open('src/feature/target_file.py').readlines())
assert n <= 150, f'{n} lines — exceeds 150-line limit'
print(f'{n} lines OK')
"

# 4. On failure: fix using failure log. Retry cap = 3. After 3: escalate to Opus.
python scripts/openai_code.py fix \
    --code src/feature/target_file.py \
    --failures logs/test-failure.txt
```

Env vars: `OPENAI_API_KEY` (required), `OPENAI_CODE_MODEL` (optional, default `gpt-5.5`).

## Retry and Escalation Rules

- **Retry cap**: 3 attempts per sub-agent task.
- If all 3 attempts fail, the sub-agent reports failure and **escalates to Opus**.
- Opus receives the failure log and decides whether to re-spec the task, simplify scope,
  or intervene directly.
- Sub-agents do NOT silently swallow test failures or ignore lint errors.

## Test/Implementation Independence

**Test-writer sub-agents are DISTINCT from implementation coders.** Test code (Phase B) is
written by test-writer sub-agents spawned by the QA Lead. Implementation code (Phase C) is
written by implementation coder sub-agents spawned by Engineers. The same agent MUST NOT write
both the tests and the implementation for the same slice.

This creates genuine independence: test-writers design tests without knowing how the code will be
implemented, and implementation coders write code to pass tests they did not design.

## Why Sonnet-as-Shell

Sonnet is the courier shell because it is cheaper than Opus and fast. Its role is to manage the
OpenAI API call, handle retries, write results to disk, and report back. Sonnet does not consume
its own generation capacity for code — it couriers prompts to OpenAI 5.5 (smartest available
OpenAI) and returns the verified output.

When OpenAI releases a smarter coding model, update the `model` field in the API call. The
rule is "smartest available OpenAI coder", not "gpt-5.5" forever.
