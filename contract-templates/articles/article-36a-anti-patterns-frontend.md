# Article 36a: Anti-Patterns from Production — Frontend Patterns (#1–#4)

> Sub-article of [Article 36](article-36-anti-patterns-from-production.md).
> **Cross-references:** Article 17 (Test-First), Article 18 (Test Peer Review),
> Article 35 (Error & Rescue Registry)

Every slice that ships UI changes MUST be checked against these patterns before
Phase E peer review. The corresponding regression test is mandatory — not optional.

---

## 1. Server Data Interpolated into Inline JS

**BAD:** `onclick="addItem('{{ item.name }}')"` — HTML-escaped `&#39;` is decoded by
the browser before JS runs; apostrophes break the literal; crafted payloads execute.

**FIX:** `onclick='addItem({{ item.name | tojson }})'` — `tojson` produces safe JS
literals. Prefer `data-*` + event listener over any inline handler.

**Regression test:** render with `name = "O'Brien <script>alert(1)</script>"`; assert
no raw apostrophe or `<script>` survives in the attribute.

---

## 2. Hidden-Field vs. Visual-Chip Drift

**BAD:** `addChip()` renders the chip but never updates the backing hidden `<input>`;
the server receives stale JSON.

**FIX:** every chip widget needs an `update<Foo>Json()` helper called from both
`add<Foo>` AND `remove<Foo>`, plus an `htmx:configRequest` listener that mutates
`evt.detail.parameters` (not just the DOM).

**Regression test:** Playwright — call `addChip(...)`, read the hidden field's
`.value`, assert it contains the added entry.

---

## 3. Pre-Applied Defaults That Violate Cross-Field Invariants

**BAD:** a default value is pre-filled that the upstream API forbids in combination
with other user selections (e.g., overlapping geo-targeting tiers → `code=100`).

**FIX:** match the upstream API's empty-state; leave optional fields empty.
Never pre-fill a default that can violate a cross-field constraint.

**Regression test:** load the form fresh; assert no chips or defaults are pre-applied.

---

## 4. Status Defaults That Break UI Promises

**BAD:** new entities are created with `status=ACTIVE` in the server payload
despite the UI explicitly promising `PAUSED` status.

**FIX:** UI promises MUST match the server payload. Default newly-created
entities to the promised status and pin it with a unit test on the param
builder.

```python
def test_build_params_defaults_status_paused():
    params = _build_params(...)
    assert params["status"] == "PAUSED"
```

---

**Continue to [article-36b-anti-patterns-backend.md](article-36b-anti-patterns-backend.md) for patterns #5–#10.**
