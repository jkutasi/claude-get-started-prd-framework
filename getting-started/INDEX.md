# Getting Started — Index

> **Purpose:** This directory contains the project setup roadmap, split into focused documents. Load ONLY the file relevant to your current step — do not load the entire directory.

| File | When to Load |
|------|-------------|
| [00-nuclear-rules.md](00-nuclear-rules.md) | Always — read first at every session |
| [01-planning-phase.md](01-planning-phase.md) | Step 1: Defining project scope and tech stack |
| [02-agent-teams.md](02-agent-teams.md) | Step 2: Setting up Agent Teams architecture |
| [03-slice-0-bootstrap.md](03-slice-0-bootstrap.md) | Step 3: Creating Slice 0 infrastructure |
| [04-per-slice-workflow.md](04-per-slice-workflow.md) | Step 4: Running phases A-J for each slice |
| [05-browser-testing.md](05-browser-testing.md) | Step 5: Browser testing + session checklist |
| [06-appendix.md](06-appendix.md) | Reference: file structure + naming conventions |

## Task Tracking

Every project uses `.taskmaster/` for durable task storage that survives across Claude sessions.

- **Skill:** `.claude/skills/task-manager/SKILL.md` — load at the start of every work session
- **Database:** `.taskmaster/tasks.json` — read this to see pending and in-progress tasks
- **Config:** `.taskmaster/config.json` — model role assignments

At every session start, load the `task-manager` skill and read `.taskmaster/tasks.json` BEFORE doing any work. Create tasks with `testStrategy` before writing code. See `.taskmaster/README.md` for schema details.
