# Step 5: Browser Testing Standard + Session Checklist

> Part of the [Getting Started](INDEX.md) roadmap. Load only this file when working on browser testing and session checklist.

## Browser Testing Standard

`agent-browser` (Vercel) is the **MANDATORY** tool for all browser-based QA testing. It works on ANY website. It visually sees the page like a human and reasons about layout, readability, and UX.

- **Whiskey Team, UX Sense Check, QA UI/UX:** MUST use `agent-browser`
- **Playwright:** Optional for automated regression scripts only. NOT sufficient for QA sign-off.
- All browser sessions use the `--session ab` flag

### Testing Pyramid

| Layer | What It Tests | Tool | Who | When |
|-------|-------------|------|-----|------|
| **Unit** | Functions, logic, parsers | pytest / jest / vitest | Test-writer sub-agents (Phase B) | Before code -- must be RED |
| **Integration** | Components together, API contracts | pytest / jest + test DB | Test-writer sub-agents (Phase B) | Before code -- must be RED |
| **E2E Browser** | Full user flows -- clicks, forms, navigation | `agent-browser` (MANDATORY) | Whiskey + QA UI/UX (Phase F) | Every frontend slice |
| **Adversarial** | Edge cases, race conditions, silent failures | `agent-browser` + API calls | Whiskey (Phase F) | Every slice |
| **UX Sense-Check** | "Does this make sense to a human?" | `agent-browser` + personas | UX Sense Check (Phase F) | Frontend slices |
| **Goal Achievement** | "Can a user complete the full workflow?" | `agent-browser` | Whiskey (Phase F) | Every slice |
| **Implicit Regression** | Untested state gaps, cross-component issues | `agent-browser` + code analysis | Whiskey (Phase H) | Every session |

**Rule:** Unit tests verify code *works*. Browser tests verify it works *for humans*. Both are mandatory. Passing unit tests with zero browser testing is NOT a shipped slice.

---

## Step 6: Session Start Checklist (Every New Session)

Before ANY implementation work:

- [ ] Read CLAUDE.md
- [ ] Verify API keys exist for peer review models
- [ ] Run `python gate_check.py --slice {latest} --all` to verify all completed slices
- [ ] If ANY slice returns FAIL, run retroactive review FIRST
- [ ] Read relevant learnings files (`learnings/QA_LEARNINGS.md`, etc.)
- [ ] Only then proceed with new work
