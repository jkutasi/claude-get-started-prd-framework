# Appendix: File Structure Reference + Naming Convention

> Part of the [Getting Started](INDEX.md) roadmap. Load only this file when referencing file structure and naming conventions.

## File Structure Reference

```
{project-root}/
├── CLAUDE.md                           # Multi-agent contract (binding)
├── PROJECT.md                          # Full architecture + implementation details
├── DOCS_MAP.md                         # Documentation index
├── AGENT_REGISTRY.md                   # Who does what
├── gate_check.py                       # Mechanical gate enforcement
├── .claude/
│   ├── skills/                         # One file per agent role
│   ├── skills-index.md                 # Master index
│   └── settings.local.json             # MCP server config
├── contracts/
│   ├── CONTRIBUTING.md
│   ├── SECURITY.md
│   ├── DATA_CONTRACT.md
│   ├── ARCHITECTURE_STANDARDS.md
│   ├── TESTING_PYRAMID.md
│   ├── TESTING_PROCEDURES.md
│   └── TESTING_GATES.md
├── config/
│   ├── default.yaml
│   └── CONFIG_SCHEMA.md
├── slices/                             # One spec per slice (extracted from PROJECT.md)
├── reviews/                            # PROOF that all review layers ran
│   ├── SLICE_REVIEW_TEMPLATE.md            # consolidated review file (all sections)
│   └── UX_SENSE_CHECK_TEMPLATE.md         # optional, frontend only
├── learnings/                          # Persistent agent learnings
│   ├── QA_LEARNINGS.md
│   ├── BUILD_LEARNINGS.md
│   ├── REVIEW_LEARNINGS.md
│   └── UX_LEARNINGS.md
├── features/                           # Gherkin specs
├── src/                                # Source code — feature-based folders (Article 20)
│   ├── {feature-name}/                 # One folder per feature
│   │   ├── {feature-name}.route.{EXT}
│   │   ├── {feature-name}.service.{EXT}
│   │   ├── {feature-name}.repository.{EXT}
│   │   ├── {feature-name}.test.{EXT}
│   │   └── {feature-name}.types.{EXT}
│   └── shared/                         # Cross-feature utilities
│       ├── errors/                     # AppError class hierarchy
│       ├── logging/                    # Structured logger setup
│       └── middleware/                 # Shared middleware
├── tests/
│   └── integration/                    # Cross-feature integration tests ONLY
├── diary/
│   └── PROJECT_DIARY.md
└── output/                             # Generated artifacts (gitignored)
```

---

## Naming Convention

Per the CLAUDE.md contract — all names must be descriptive by what they do. No random, auto-generated, or whimsical names.

| Good | Bad | Why |
|------|-----|-----|
| `user-auth-service.py` | `module2.py` | Says what it does |
| `slice-2-data-validation.md` | `distributed-whistling-aurora.md` | No auto-generated names |
| `payment-processing.py` | `m3.py` | Self-documenting |

This applies to: markdown files, code modules, git branches, database tables, cloud jobs, Gherkin features, and all other named artifacts.
