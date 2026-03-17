# Phase I: Documentation Update

> Load this file when starting Phase I. Complete all steps before proceeding to Phase I.5.

## Purpose

Update all project documentation to reflect the completed slice. Keep docs accurate and current.

## Steps

### I.1: Update Affected Docs

1. Documentation Scribe updates all docs affected by this slice:
   - API documentation (if endpoints changed).
   - Data model documentation (if schema changed).
   - Architecture documentation (if new components added).
   - User-facing documentation (if new features visible).
2. Update PROJECT.md if the slice changed overall architecture.
3. Update DOCS_MAP.md if new doc files were created.

### I.2: Update Learnings Files

4. Update learnings files with new patterns discovered during this slice:
   - New coding patterns or conventions adopted.
   - Gotchas or pitfalls encountered.
   - Library-specific insights.
   - Performance findings.

### I.3: Update Diagrams

5. If any discovery during implementation invalidated earlier diagrams, update them now.
6. Verify all diagrams in `docs/diagrams/` are still accurate.

### I.4: Contract Completion

7. Mark the slice contract as COMPLETE.
8. Update any cross-references in other slice contracts.

## Gate

```
+------------------------------------------------------------------+
| DOCUMENTATION GATE I: Before proceeding to Phase I.5:            |
| [] "All affected docs updated"                                   |
| [] "Learnings files updated with new patterns"                   |
| [] "Diagrams verified/updated for accuracy"                      |
| [] "Slice contract marked COMPLETE"                              |
| [] "DOCS_MAP.md is current"                                      |
+------------------------------------------------------------------+
```

## Next Phase

Proceed to **Phase I.5: User Delivery** (`phase-i5-user-delivery.md`).
