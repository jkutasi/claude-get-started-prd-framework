# §3 150-Line File Limit

> Part of [Architecture Standards](../ARCHITECTURE-STANDARDS-TEMPLATE.md). Aligned with [Article 20c](../articles/article-20c-150-line-file-limit.md).

**Every production source file MUST stay under 150 lines** (excluding comments and blank lines).

## Why

A 500-line file doing multiple things forces any agent — human or AI — to understand too much context. An 80-line file doing one thing is almost impossible to get wrong. This rule eliminates context-window problems at the architectural level.

## Relationship to Function Limits

The 150-line file limit complements the existing 40-line function limit (QA Code Quality §4.7). A 150-line file holds at most 3-4 functions at maximum length. If a file exceeds this, it has too many concerns — split it.

## Test Files

Test files SHOULD stay under 150 lines. If tests grow beyond this, split into multiple test files per feature:

- `{feature-name}.test.{EXT}` — core tests
- `{feature-name}.edge-cases.test.{EXT}` — edge case tests

This is a SHOULD, not a hard gate failure. The priority is comprehensive test coverage.

## Enforcement

- QA Code Quality agent checks file length as a P1 finding.
- Peer reviewers flag files approaching the limit.
- Files exceeding 150 lines are mandatory fixes before the slice ships.
