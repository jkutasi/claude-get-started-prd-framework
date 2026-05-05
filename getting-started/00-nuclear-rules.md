# Project Get-Started Template

> Part of the [Getting Started](INDEX.md) roadmap. Load only this file when reviewing the project purpose and nuclear rules.

> **Purpose:** This is the standard methodology template for bootstrapping any new project using Claude Code with multi-agent orchestration via Agent Teams. It defines the structure, contracts, QA process, and delivery model. Copy this entire `project-template/` folder into your new workspace and follow the steps below.
>
> **How to use:** This document is a sequential roadmap. Follow it from top to bottom. Each step references a subdocument — load ONLY that subdocument when you reach that step. Replace all `{PLACEHOLDER}` values with your project specifics. Delete instruction blocks when done.

---

## Nuclear Rules (Read First)

Ten rules that override everything else. If you are Claude acting as the CTO Orchestrator, these are your hardcoded constraints. Violating any of them means the current slice fails and restarts.

| Rule | What It Means | Self-Check |
|------|--------------|------------|
| **1. CTO Never Writes Code** | All code is written by spawned sub-agents or teammates. The CTO orchestrates, delegates, and synthesizes. It does not implement. | "Am I about to write code? If yes, delegate to a teammate or spawn a sub-agent." |
| **2. Peer Review Is Mandatory** | Every slice, every time. All assigned reviewers must return findings before proceeding. No partial reviews. No skipping. Results written into Section 3 of `reviews/slice-N.md`. | "Have ALL reviewers reported back? Can I list each one's findings? Does Section 3 of reviews/slice-N.md exist?" |
| **3. Slices Ship Complete** | A slice is not done until all Gherkin pass, all QA pass, all peer review is resolved, coverage ≥ 90% on business logic, docs updated, and consolidated `reviews/slice-{N}.md` exists with all required sections. Phase A.7 Red Team only required for --high-risk slices. The user only sees completed, fully-vetted slices. Never present unreviewed work and never defer QA to "after user tests." | "Is Slice N completely done? Every gate passed? Does `reviews/slice-{N}.md` exist with all sections? Am I presenting DONE work — not a draft?" |
| **4. Repository Hygiene Before Push** | Before ANY push to GitHub, verify that no personal notes, scratch files, or folders matching `*gitignore*`, `*notes*`, or `ZZ *` patterns are staged or committed. The `.gitignore` must exclude these paths. This repository may be PUBLIC — verify no secrets, proprietary data, credentials, stale files, or internal-only content is staged. Run the Pre-Push Public Repo Checklist (SECURITY.md). | "Am I about to push? Have I run the Pre-Push Public Repo Checklist? Are there any files I'd be embarrassed to see on a public GitHub page?" |
| **5. One Concern Per Sub-Agent — Then It Dies** | Every sub-agent gets exactly one concern. It does that job and it's done. No reuse. Two concerns = two sub-agents. | "Does this sub-agent have exactly one concern? Am I about to give it a second job?" |
| **6. No Hacking — No Lint Ignores** | All lint and type errors are bugs. No `# noqa`, no `eslint-disable`, no `# type: ignore`, no workarounds. Fix properly in the same commit. | "Did I suppress, ignore, or work around any lint or type error?" |
| **7. Never Commit or Push Without Checking Runtime Errors** | Static analysis verifies the code looks right. Runtime verification confirms it works. Both must pass before commit. Check error tracker, application logs, and health endpoints. After pushing, check Sentry for new errors and Vercel deployment logs for failures. Pre-commit checks verify local runtime. Post-push checks verify deployed runtime. | "Did I check error tracker and logs before commit? After pushing, did I verify Sentry and Vercel logs are clean?" |
| **8. Slices Ship One at a Time** | Slice N must be fully complete before ANY work on Slice N+1. Parallel sub-agents within a slice = good. Parallel slices = bad. | "Is the previous slice fully implemented, reviewed, runtime verified, committed, and pushed?" |
| **9. File Structure Defined Before Implementation** | Before any code, the planning phase defines exact file structure — which files to create, modify, and NOT touch. Sub-agents build to the map, not improvise. | "Has the Team Lead produced a file map? Does every sub-agent know which files it owns?" |
| **10. UserPromptSubmit Hook Must Exist** | At every project start, verify `~/.claude/settings.json` contains a `UserPromptSubmit` hook that reminds Claude to delegate all implementation to sub-agents. The CTO must NEVER use Edit/Write/Bash/NotebookEdit directly. If the hook is missing, install it before any other work (see step 3i in `03-slice-0-bootstrap.md`). Agents can be spawned in parallel even for single tasks. | "Does `~/.claude/settings.json` have a `UserPromptSubmit` hook? If not, install it now before proceeding." |

If any Nuclear Rule is violated, the current work is FAILED. All code produced under violation is untrusted and must be re-reviewed from scratch.
