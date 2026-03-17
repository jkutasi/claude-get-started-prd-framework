# Seed ADRs: Configuration Decisions

These ADRs cover tool configuration, model selection, and settings architecture.

---

## ADR-013: UserPromptSubmit Hook (Nuclear Rule 10)

- **Status:** accepted
- **Date:** 2026-03-15
- **Tags:** hooks, enforcement, file-size

**Context:** The 150-line file limit was documented but not enforced. Agents routinely created files exceeding 200-300 lines. Written rules without runtime enforcement were ignored.

**Decision:** A UserPromptSubmit hook runs on every prompt submission, checking file sizes and other constraints. This became the enforcement mechanism for Nuclear Rule 10 (150-line limit).

**Alternatives:** Pre-commit hooks only (too late — file already written), lint rules (agents disable them), manual review (missed consistently).

**Consequences:** File size violations are caught before code is even reviewed. Trade-off: hook adds latency to every prompt, but prevents the most common structural violation.

**Lessons:** Enforcement must happen at the earliest possible point. Catching violations after the fact is always more expensive.

---

## ADR-014: Codex Model Version Pinning

- **Status:** accepted
- **Date:** 2026-03-16
- **Tags:** models, codex, version-pinning

**Context:** Switched from gpt-5.3-codex to gpt-5.4-codex for peer review, then discovered 5.4 had regressions in code analysis. Switched back to 5.3, which remains the best version for code review tasks.

**Decision:** Pin Codex peer review to gpt-5.3-codex. Document the version in settings and the reason for pinning. Any version change requires testing against the peer review benchmark suite.

**Alternatives:** Always-latest (regressions), multiple versions in parallel (cost), no pinning (inconsistent results).

**Consequences:** Stable, predictable peer review quality. Trade-off: may miss improvements in newer versions, but stability is more valuable for review.

**Lessons:** Newer model versions are not always better for specific tasks. Pin versions and require evidence before upgrading.

---

## ADR-015: Settings.json Permission Structure

- **Status:** accepted
- **Date:** 2026-03-17
- **Tags:** settings, permissions, security

**Context:** Early settings were permissive — agents could use any tool. This led to accidental file deletions, unintended git operations, and tools being used outside their intended scope.

**Decision:** Locked-down permission structure in settings.json. Only explicitly approved tools and commands are allowed. Permissions are scoped by agent role (CTO gets read-only, coder gets write access, etc.).

**Alternatives:** Permissive defaults with audit log (damage already done), per-command approval (too slow), trust-based (already failed).

**Consequences:** Agents can only use tools they need. Accidental damage eliminated. Trade-off: new tools require explicit permission grants, adding friction to setup.

**Lessons:** Default-deny is the only sane permission model for autonomous agents. Trust must be earned per-tool, not granted globally.
