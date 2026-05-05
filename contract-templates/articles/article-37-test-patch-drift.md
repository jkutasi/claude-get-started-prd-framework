# Article 37: Test-Patch-Target Drift

> Part of the [Contract Articles](INDEX.md). Load only when you need this article.
>
> **Cross-references:** Article 17 (Test-First), Article 18 (Test Peer Review),
> Article 36 (Anti-Pattern Catalog)

## The Rule

When a module is split, every `mock.patch("module.x")` that targets a moved
symbol MUST be re-targeted to the new definition module, OR a facade-identity
test must be added that fails fast when the facade and the definition diverge.
Leaving a patch aimed at a re-export is a silent no-op — the test passes, but
the patch never touches the code under test.

## Why It Matters

Module splits routinely introduce silent test failures: existing patches resolve
against the facade (the symbol exists there) but never intercept the runtime
call, which now originates from the new definition module. The tests pass and
lie. Peer review may catch it; production will not.

## The Drift Pattern

```python
# service_facade.py (facade)
from src.module.helpers import _helper_fn  # re-export

# service_impl.py (definition)
from src.module.helpers import _helper_fn  # own import

# test.py — WRONG: patches the facade, not where service_impl resolves it
@mock.patch("src.module.service_facade._helper_fn")
def test_create_records(mock_fn, ...): ...  # patch is a silent no-op
```

## Fixes (pick one)

### Option 1 — Patch where defined, not where re-exported

```python
@mock.patch("src.module.service_impl._helper_fn")  # definition
def test_create_records_calls_helper(mock_fn, ...):
    ...
```

### Option 2 — Assert the patch was actually called

Add `assert mock_X.called` inside every test body that relies on a patch.
If the patch missed, the assertion fails immediately.

```python
@mock.patch("src.module.service_facade._helper_fn")
def test_create_records(mock_fn, ...):
    create_records(session_id="x")
    assert mock_fn.called  # fails if patch silently no-oped
```

### Option 3 — Facade-identity regression test

```python
def test_facade_helper_is_definition_helper():
    from src.module import service_facade, helpers
    assert service_facade._helper_fn is helpers._helper_fn
```

Add one such assertion per public symbol re-exported by the facade. Place in
a dedicated `test_facade_identity.py` so it runs in every CI pass.

## Module Split Checklist

Before merging any PR that splits a module:

- [ ] **Moved symbols** — list every moved symbol in the PR description.
- [ ] **Patch audit** — run `git grep -n 'mock.patch.*<old.module>'` in `tests/`;
      list every hit and confirm each is re-targeted or covered by Option 3.
- [ ] **Logger names** — `getLogger(__name__)` changes when a file moves;
      update any test assertions that check `caplog.records[n].name`.
- [ ] **Import-timing** — moving an import from inside a function to module
      top-level changes when it executes; adjust mocks that patch at runtime.
- [ ] **Behavior-preserving move tests** — capture output on N representative
      inputs before the split; replay after and assert identical output.
- [ ] **Facade-identity tests** — add or update `test_facade_identity.py` for
      every symbol the facade re-exports.
