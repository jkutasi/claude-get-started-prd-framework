# Article 36b: Anti-Patterns from Production — Backend Patterns (#5–#10)

> Sub-article of [Article 36](article-36-anti-patterns-from-production.md).
> **Cross-references:** Article 17 (Test-First), Article 18 (Test Peer Review),
> Article 35 (Error & Rescue Registry)

Every slice that ships data-shape changes, external-API calls, or SQL changes MUST
be checked against these patterns before Phase E peer review. The corresponding
regression test is mandatory — not optional.

---

## 5. Database Parser Quirks — Non-Portable SQL Syntax

**BAD:** `LIKE '<pat>' ESCAPE '<char>'` — not supported by all engines. Unit tests
pass because SQL never runs against the real engine; the error is swallowed by a
fallback path.

**FIX:** escape special characters in Python before building the pattern;
omit the `ESCAPE` clause entirely.

```python
def _escape_like(s: str) -> str:
    return s.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
```

**Regression test:** run the actual query against the target engine in a
smoke test. If the engine raises `BadRequest`, fail loud.

---

## 6. Wrong API Endpoint or Model Identifier

**BAD:** calling `/v1/chat/completions` for a model that lives on a different
endpoint (e.g., `/v1/responses`), or using a model slug that the endpoint
does not recognize — causing a silent degradation to a fallback model.

**FIX:** verify endpoint + model + response-field names against the vendor
spec. Add a contract test that asserts the response schema matches what the
code parses.

---

## 7. Silent Fallback to a Degraded Model

**BAD:** on a primary-model error, code silently substitutes a lesser model
and continues — the audit trail now reflects the wrong model.

**FIX:** if the designated model fails, REPORT the error to the caller. Never
substitute silently. Degrading the model invalidates any peer-review audit
trail that depends on model identity.

---

## 8. Marking Issues Resolved Based on Event Silence

**BAD:** closing a Sentry issue because no events fired for several days —
the affected page was simply not visited; the bug recurred on first use.

**FIX:** never close an error tracker issue without (a) identified root cause,
(b) shipped fix, AND (c) a green smoke test that exercises the failing surface.

---

## 9. NULL-Tolerant ORDER BY with No Fallback Rank

**BAD:** `ORDER BY score` where `score` is NULL on most rows — tiebreaker is
a no-op; irrelevant small rows rank above the intended top results.

**FIX:** every ORDER BY tiebreaker must assume the column is populated.
Either backfill at write time or add a deterministic fallback:
`COALESCE(score, 0)`, a hardcoded tier column, or alphabetical.

**Regression test:** seed rows with NULL score; assert the deterministic
fallback produces the expected sort order.

---

## 10. Silent Fallback Paths Masking Exceptions

**BAD:** `try: primary() except Exception: fallback()` — the primary failure
is swallowed; the fallback hides a bug for days.

**FIX:** every fallback MUST log `error` (not `warning`) on primary failure,
with a unique Sentry fingerprint. Add an alert on that fingerprint.
Only transient, expected failures qualify for `warning`-level downgrade.
