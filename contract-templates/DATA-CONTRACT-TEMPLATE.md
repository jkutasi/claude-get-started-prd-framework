# Data Contract -- {PROJECT_NAME}

## Schema Definitions

### {TABLE_OR_COLLECTION_1_NAME}

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `{COLUMN_1}` | `{TYPE}` | No | -- | {DESCRIPTION} |
| `{COLUMN_2}` | `{TYPE}` | No | -- | {DESCRIPTION} |
| `{COLUMN_3}` | `{TYPE}` | Yes | `{DEFAULT}` | {DESCRIPTION} |
| `{COLUMN_4}` | `{TYPE}` | No | `{DEFAULT}` | {DESCRIPTION} |
| `run_id` | `{TYPE}` | No | -- | Pipeline run identifier for traceability |
| `created_at` | `TIMESTAMP` | No | `NOW()` | Row creation timestamp |
| `updated_at` | `TIMESTAMP` | No | `NOW()` | Last modification timestamp |

### {TABLE_OR_COLLECTION_2_NAME}

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `{COLUMN_1}` | `{TYPE}` | No | -- | {DESCRIPTION} |
| `{COLUMN_2}` | `{TYPE}` | No | -- | {DESCRIPTION} |
| `{COLUMN_3}` | `{TYPE}` | Yes | `{DEFAULT}` | {DESCRIPTION} |
| `run_id` | `{TYPE}` | No | -- | Pipeline run identifier for traceability |
| `created_at` | `TIMESTAMP` | No | `NOW()` | Row creation timestamp |

> Add additional tables as needed. Every table MUST include `run_id` and `created_at` at minimum.

---

## Versioning Rules

### Run IDs for Pipeline Traceability

Every pipeline execution MUST generate a unique `run_id` that is attached to all rows written during that run. This enables:

- **Traceability:** Any row can be traced back to the exact pipeline run that created it.
- **Rollback:** If a run produces bad data, all its rows can be identified and removed by `run_id`.
- **Debugging:** Comparing outputs across runs to identify when a regression was introduced.

**Run ID format:** `{RUN_ID_FORMAT}` (e.g., `{PROJECT_SHORT_NAME}-YYYYMMDD-HHMMSS-{RANDOM_SUFFIX}` or UUID v4)

### Schema Version Tracking

| Version | Date | Change | Migration Script | Backward Compatible |
|---------|------|--------|-----------------|---------------------|
| 1.0.0 | {YYYY-MM-DD} | Initial schema | -- | -- |
| {VERSION} | {YYYY-MM-DD} | {CHANGE_DESCRIPTION} | `migrations/{MIGRATION_FILE}` | {YES/NO} |

---

## Migration Rules

1. **All schema changes require a migration script.** No manual DDL changes in production. Every change is scripted, versioned, and reviewable.
2. **Migrations are forward-only.** Rollback scripts are written alongside forward migrations but are only used in emergencies.
3. **Migration scripts live in `migrations/`.** Named as: `{VERSION}_{DESCRIPTION}.sql` (e.g., `002_add_status_column.sql`).
4. **Test migrations on a copy first.** All migrations are tested against a copy of production data before applying to production.
5. **Backward compatibility preferred.** Additive changes (new columns, new tables) are preferred over destructive changes (column renames, type changes). If a breaking change is required, document the migration path.
6. **No data loss.** Migrations MUST NOT silently drop data. If data must be removed, it is archived first and the archive location is documented.

---

## Query Patterns

### Retrieving Latest Data

To retrieve the most recent data for a given entity, always use `run_id` ordering:

```sql
-- Latest run for a specific entity
SELECT *
FROM {TABLE_NAME}
WHERE {ENTITY_COLUMN} = '{ENTITY_VALUE}'
ORDER BY created_at DESC
LIMIT 1;

-- All data from the most recent pipeline run
SELECT *
FROM {TABLE_NAME}
WHERE run_id = (
    SELECT run_id
    FROM {TABLE_NAME}
    ORDER BY created_at DESC
    LIMIT 1
);
```

**Rule:** Never assume the latest data is the only data. Always filter by `run_id` or `created_at` to get a consistent snapshot.

---

## Cleanup and Retention Policy

| Data Category | Retention Period | Cleanup Method | Archive Location |
|--------------|-----------------|---------------|-----------------|
| Current production data | Indefinite | -- | -- |
| Historical run data | {RETENTION_PERIOD} | {CLEANUP_METHOD} | `{ARCHIVE_LOCATION}` |
| Temporary/staging data | {RETENTION_PERIOD} | {CLEANUP_METHOD} | Deleted (no archive) |
| Audit logs | {RETENTION_PERIOD} | {CLEANUP_METHOD} | `{ARCHIVE_LOCATION}` |
| Backup snapshots | {RETENTION_PERIOD} | {CLEANUP_METHOD} | `{ARCHIVE_LOCATION}` |

**Cleanup automation:** Cleanup runs on schedule via {CLEANUP_MECHANISM}. Manual cleanup is NOT acceptable for production data.

---

## Data Validation Rules

All data entering the system MUST pass validation before being persisted:

| Field | Validation Rule | Error Behavior |
|-------|----------------|---------------|
| `{FIELD_1}` | {RULE — e.g., "Must be positive decimal, max 2 decimal places"} | {REJECT_ROW / SET_DEFAULT / LOG_AND_SKIP} |
| `{FIELD_2}` | {RULE — e.g., "Must match ISO 8601 date format"} | {REJECT_ROW / SET_DEFAULT / LOG_AND_SKIP} |
| `{FIELD_3}` | {RULE — e.g., "Must exist in reference table {REF_TABLE}"} | {REJECT_ROW / SET_DEFAULT / LOG_AND_SKIP} |
| `{FIELD_4}` | {RULE — e.g., "String length between 1 and {MAX_LENGTH}"} | {REJECT_ROW / SET_DEFAULT / LOG_AND_SKIP} |

**Validation failures are logged.** Every rejected row is written to the validation error log with: timestamp, run_id, field name, expected value, actual value, and error type.

**No silent data loss.** If validation rejects a row, the rejection MUST be visible in logs or monitoring. Data does not silently disappear.

---

## NULL Handling Policy

NULLs are a common source of silent bugs. This project follows these rules:

1. **Columns marked NOT NULL must never receive NULL.** The application layer validates this before the database layer. Do not rely on database constraints as the only defense.
2. **Nullable columns have explicit defaults.** If a column is nullable, the schema defines what NULL means in business terms (e.g., "not yet calculated," "not applicable," "unknown").
3. **NULLs in calculations produce NULL results.** If any input to a calculation is NULL, the output is NULL -- not zero, not an empty string, not a default value. The NULL propagates so it can be detected downstream.
4. **NULL-safe comparisons.** All queries that filter on nullable columns MUST use NULL-safe operators (e.g., `IS NULL`, `IS NOT NULL`, `COALESCE`). Never use `= NULL` (which always returns false in SQL).
5. **NULL is not zero.** NULL means "unknown" or "missing." Zero means "the value is zero." These are different. Do not conflate them.
6. **Display layer handles NULLs.** The frontend MUST display a meaningful indicator for NULL values (e.g., "N/A", "--", "Not available"). Never display the literal string "null" or "None" to users.

| Column | NULL Meaning | Display Value | Calculation Behavior |
|--------|-------------|--------------|---------------------|
| `{COLUMN_1}` | {BUSINESS_MEANING_OF_NULL} | {DISPLAY_TEXT} | {PROPAGATE_NULL / USE_DEFAULT / SKIP_ROW} |
| `{COLUMN_2}` | {BUSINESS_MEANING_OF_NULL} | {DISPLAY_TEXT} | {PROPAGATE_NULL / USE_DEFAULT / SKIP_ROW} |
