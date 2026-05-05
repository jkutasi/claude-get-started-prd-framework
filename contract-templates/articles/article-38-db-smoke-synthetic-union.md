# Article 38: DB Smoke — Synthetic UNION ALL Injection

> Part of the [Contract Articles](INDEX.md). Load only when you need this article.
>
> **Cross-references:** Article 17 (Test-First), Article 36 (Anti-Patterns),
> Article 39 (Deploy SHA Verification)

## The Rule

For any query whose `ORDER BY` or ranking logic ships to users, the test suite
MUST include a synthetic-row injection that proves expected results rank correctly
against a known dataset. Running the query against real data alone is not
sufficient — real data can silently mask wrong ordering when all ranking columns
hold the same value (NULL tiebreaker collapse).

The synthetic test MUST:

1. Inject at least two rows that should rank differently under the correct logic.
2. Assert the expected row appears at the exact position (e.g. index 0), not just
   "anywhere in the result set."
3. Run on the same database engine used in production — not a local mock.

## Why It Matters

A ranking column that is NULL for every row in the table produces a dead
tiebreaker: all rows tie, and secondary sort order (often implicit or absent)
determines output unpredictably. Every unit and integration test can pass because
the fallback path returns a non-empty list; manual smoke tests appear green
because _some_ matching row appears first — just not the correct one. The bug
can run undetected until a test asserts the _specific_ expected row at position 0.

The synthetic UNION ALL technique below is the diagnostic that confirms ranking
SQL is broken before any production data is examined.

## The Pattern

```sql
WITH staging AS (
  -- Synthetic anchor rows with known ranking values
  SELECT '<expected_first>'   AS <name_col>, <rank_value_high> AS <rank_col>
  UNION ALL
  SELECT '<expected_second>',               <rank_value_low>
  UNION ALL
  -- Real table rows for the same search term
  SELECT <name_col>, <rank_col>
  FROM   <schema>.<real_table>
  WHERE  <name_col> LIKE '<search_prefix>%'
)
SELECT   <name_col>
FROM     staging
ORDER BY <rank_col> DESC, <name_col> ASC   -- match production ORDER BY exactly
LIMIT    5;
```

**Assertion:** `result[0].<name_col> == '<expected_first>'`

If the synthetic row does not appear first, the `ORDER BY` is wrong. Adjust until
the assertion passes, then apply the same fix to production SQL.

## Engine Notes

| Engine     | Escape in LIKE              | NULL in ORDER BY (ASC)   |
|------------|-----------------------------|--------------------------|
| BigQuery   | `ESCAPE` clause unsupported — escape special characters in Python before the query reaches the engine | NULLs sort last |
| PostgreSQL | `LIKE E'...' ESCAPE '\'`    | NULLs sort last (default); use `NULLS FIRST` / `NULLS LAST` explicitly |
| MySQL      | `LIKE '...' ESCAPE '\'`     | NULLs sort first in ASC  |

**NULL tiebreakers are the most common silent failure.** When a ranking column
is NULL for every row, all rows tie and the secondary sort (often implicit or
absent) determines output order unpredictably across engines and query planners.
Always add a non-nullable secondary sort key.

For BigQuery: perform wildcard escaping in the application layer (Python, Go,
etc.) before building the query string. Do not rely on a SQL `ESCAPE` clause.

## When to Run

| Trigger                                  | Required?    |
|------------------------------------------|--------------|
| Every CI build                           | Yes          |
| After schema migration                   | Yes          |
| Phase F.5 runtime log check (materialized table) | Yes — run on live connection, not fixture |
| After ranking-column backfill or ETL job | Yes          |

Phase F.5 is the Runtime Log Check phase that follows every QA run. The
synthetic-union smoke MUST execute against the real materialized table in that
phase, not a seeded test database.

## Cross-References

- **Article 36, Anti-Pattern #5** — Database parser quirks silently alter query
  semantics; always test on the target engine.
- **Article 36, Anti-Pattern #9** — NULL `ORDER BY` columns produce
  non-deterministic row order; add a non-nullable tiebreaker.
