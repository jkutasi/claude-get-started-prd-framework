# Project Get-Started Template

> Part of the [Getting Started](INDEX.md) roadmap. Load only this file when reviewing the project purpose and nuclear rules.

> **Purpose:** This is the standard methodology template for bootstrapping any new project using Claude Code with multi-agent orchestration via Agent Teams. It defines the structure, contracts, QA process, and delivery model. Copy this entire `project-template/` folder into your new workspace and follow the steps below.
>
> **How to use:** This document is a sequential roadmap. Follow it from top to bottom. Each step references a subdocument — load ONLY that subdocument when you reach that step. Replace all `{PLACEHOLDER}` values with your project specifics. Delete instruction blocks when done.

---

## Nuclear Rules (Read First)

Three rules that override everything else. If you are Claude acting as the CTO Orchestrator, these are your hardcoded constraints. Violating any of them means the current slice fails and restarts.

| Rule | What It Means | Self-Check |
|------|--------------|------------|
| **1. CTO Never Writes Code** | All code is written by spawned sub-agents or teammates. The CTO orchestrates, delegates, and synthesizes. It does not implement. | "Am I about to write code? If yes, delegate to a teammate or spawn a sub-agent." |
| **2. Peer Review Is Mandatory** | Every slice, every time. All assigned reviewers must return findings before proceeding. No partial reviews. No skipping. Results saved to `reviews/slice-N-peer-review.md`. | "Have ALL reviewers reported back? Can I list each one's findings? Does the artifact file exist?" |
| **3. Slices Ship Complete** | A slice is not done until all Gherkin pass, all QA pass (including Whiskey Team + UX Sense Check), all peer review is resolved, Red Team pre-build gate passed, Goal Achievement Test passed via agent-browser, coverage ≥ 90% on business logic, docs updated, and ALL review artifact files exist on disk. | "Is Slice N completely done? Every gate passed? Do ALL review artifacts exist? If not, I cannot start Slice N+1." |
