# Article 20c: 150-Line File Limit

> Part of [Article 20: Code Architecture Standards](article-20-code-architecture.md). Load only when you need this specific subsection.

Every production source file MUST stay under 150 lines (excluding comments and blank lines). This is a hard rule enforced in peer review and QA Code Quality checks. If a file is approaching the limit, the concern must be split.

This complements the existing 40-line function limit — a 150-line file holds at most 3-4 max-length functions.

## Test Files

Test files SHOULD stay under 150 lines but may be split into multiple test files per feature rather than gate-fail. The priority is comprehensive test coverage:

- `{feature-name}.test.{EXT}` — core tests
- `{feature-name}.edge-cases.test.{EXT}` — edge case tests

## Enforcement

- QA Code Quality agent checks file length as a P1 finding.
- Peer reviewers flag files approaching the limit.
- Files exceeding 150 lines are mandatory fixes before the slice ships.

See `contracts/ARCHITECTURE_STANDARDS.md` §3 for the full rationale.

## Tripwire test for split templates

When a template (Jinja, Handlebars, Mustache, or any partial-based system) is split into partials, a parent rename silently breaks every partial that still references the old variable name — no compiler error, no runtime crash until that code path is exercised. A `StrictUndefined`-style test that renders each partial under an exhaustive context dictionary catches this class of regression at CI time. Other engines have analogues: Handlebars `strict: true`, Mustache with a custom resolver that throws on missing keys.

```python
from jinja2 import Environment, FileSystemLoader, StrictUndefined

env = Environment(loader=FileSystemLoader("templates"), undefined=StrictUndefined)
ctx = {"age_min": 18, "locations": [], "interests": []}  # must be exhaustive
for partial in ["partials/_age.html", "partials/_locations.html", "partials/_interests.html"]:
    env.get_template(partial).render(**ctx)  # raises UndefinedError on any missing var
```
