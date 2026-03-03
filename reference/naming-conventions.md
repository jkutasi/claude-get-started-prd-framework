# Naming Conventions — Article 10

> Every name in this project must be **descriptive and human-readable**.
> This applies to files, directories, branches, variables, functions, classes,
> database tables, cloud jobs, and Gherkin features.

## The Rule

All names must clearly communicate **what the thing is or does**. No random
names, no auto-generated names, no cryptic abbreviations.

## Good vs Bad Examples

| Good (Descriptive) | Bad (Cryptic) | Why It's Bad |
|---|---|---|
| `project-implementation-plan.md` | `plan-v2.md` | What plan? Which version matters? |
| `user-auth-service.py` | `module2.py` | "module2" tells you nothing |
| `payment-processing.py` | `m3.py` | Completely opaque |
| `slice-2-data-validation.md` | `distributed-whistling-aurora.md` | Auto-generated nonsense |
| `feature/add-user-export` | `feature/fix-stuff` | "stuff" is not a description |
| `calculate_total_revenue()` | `calc2()` | What does it calculate? |
| `CustomerOrderHistory` | `DataObj` | Generic class name |
| `analytics_dashboard` | `db_tbl_7` | Table name should describe its content |

## Where This Applies

- **Markdown files** — Slice plans, review docs, learnings files
- **Code modules** — Python files, JavaScript modules, any source code
- **Git branches** — `feature/`, `fix/`, `slice-N/` prefixes with descriptive names
- **Database tables** — Table and column names describe their content
- **Cloud jobs** — Scheduled tasks, pipelines, Lambda functions
- **Gherkin features** — Scenario names read as plain English descriptions

## Enforcement

This convention is checked during **peer review**. Reviewers flag any name that
fails the "would a new team member understand this?" test.

If a reviewer has to ask "what does this name mean?" — rename it.
