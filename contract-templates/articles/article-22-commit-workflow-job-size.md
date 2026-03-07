# Article 22: Commit Workflow by Job Size

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

Different job sizes need different levels of review before committing. The workflow ensures the review intensity matches the risk.

## Large Jobs (multi-file changes, feature builds, refactors)

1. Complete the work
2. Code review — spin up code-review sub-agents to review all changes before committing
3. Runtime verification — spin up a verification sub-agent to check error tracker, application logs, and health endpoints (Nuclear Rule 7)
4. Commit — group the changes with a descriptive message
5. Dismiss all sub-agents — context is done
6. Push to remote

## Small Jobs (single-file fixes, config tweaks, quick patches)

1. Complete the work
2. Commit immediately
3. Dismiss the sub-agent or `/clear` if working in main session
4. Push to remote

## Why This Matters

Large jobs without code review ship unverified code. The workflow ensures the review intensity matches the risk. Clean commits mean you never accidentally revert good work when rolling back bad work. Don't mingle poison with good code in the same save.
