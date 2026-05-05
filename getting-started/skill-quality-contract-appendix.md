# Skill Quality Contract — Appendix

> Companion to [skill-quality-contract.md](skill-quality-contract.md). Anti-pattern catalogue, abstract example skeleton, and audit script outline.

## Anti-Pattern Catalogue (use to populate Section 6 of any skill)

Every skill must name at least 3 anti-patterns. Pull from this catalogue or write project-specific ones.

| Anti-Pattern | What It Looks Like | Why It Fails |
|--------------|--------------------|--------------|
| **Megaskill drift** | One skill that builds, tests, deploys, and notifies | Atomicity violated — caller cannot reason about scope or verify output |
| **Implicit input** | Procedure references "the spec" or "the config" without naming it as an input | Caller supplies wrong artifact; skill silently picks something stale |
| **Vague trigger** | Description reads "Use when working on the backend" | Fires on every backend prompt, crowds out specific skills |
| **Missing "do not use when"** | Trigger only states positive case | Skill fires on adjacent-but-wrong scenarios |
| **Branching procedure step** | "Step 3: If X, do A; else do B; else if Y, do C" | Step is not atomic — split into separate numbered steps or separate skills |
| **Free-form output** | Output section says "produce a summary" with no shape | Caller cannot programmatically consume; downstream skills break |
| **Unbounded tool surface** | `allowed-tools` is empty or lists every tool | Skill can mutate state outside its job; blast radius unbounded |
| **External script not declared** | Procedure runs `./scripts/magic.sh` not listed in Tool surface | Skill is not self-contained; breaks on fresh checkout |
| **Secrets in body** | Procedure embeds an API key, DSN, or token literal | Security violation; rotate-and-rewrite required |
| **No verification step** | Skill ends without telling caller how to confirm success | Silent failures; caller assumes success because no error raised |
| **Description as role summary** | "Backend engineer agent. Writes server code." | Auto-discovery breaks; skill never matches a real prompt |
| **Stale example** | Example output references files or APIs that no longer exist | Caller follows the example, hits a 404, loses trust in the skill |
| **No anti-patterns listed** | Section 6 is missing or says "use common sense" | Lessons-learned not encoded; same bug ships twice |

## Abstract Skeleton Example

This skeleton shows the shape every conforming `SKILL.md` follows. Replace placeholders with project specifics. Do not ship this file as-is — it is illustrative only.

    ---
    name: example-skill
    description: "Use when {specific trigger condition}. Do not use when {adjacent scenario that should route elsewhere}."
    allowed-tools: Read, Grep, Bash
    ---

    # Example Skill

    ## 1. Trigger / When-to-use
    - Use when: {one concrete situation, naming the artifact or signal that fires it}.
    - Do not use when: {adjacent scenario}, {another adjacent scenario} — those route to {other-skill}.

    ## 2. Inputs
    - `target_path` (required) — absolute path to the file or directory to operate on.
    - `mode` (required) — one of `audit | fix | report`.
    - `context_doc` (optional) — path to relevant contract document.

    ## 3. Procedure
    1. Read `target_path` and confirm it exists; abort with error if missing.
    2. Parse `mode`; reject any value outside the allowed set.
    3. Run the single-purpose check defined for this skill.
    4. Format the result per the Outputs section.
    5. Emit the result; do not mutate state outside the declared tool surface.

    ## 4. Outputs
    Markdown report with this exact shape:

        ## Result
        - Status: PASS | FAIL
        - Findings: <bulleted list, one per finding>
        - Next action: <single sentence>

    ## 5. Tool Surface
    - `Read` — to load `target_path` and `context_doc`.
    - `Grep` — to scan for the specific pattern this skill checks.
    - `Bash` — only to run `scripts/check.sh` (lives in repo, declared here).
    - No `Write` / `Edit` — this skill is read-only.

    ## 6. Anti-Patterns
    - Megaskill drift: do not also fix what is found; emit a report only.
    - Implicit input: refuse to run if `target_path` is unset.
    - Free-form output: refuse to deviate from the Outputs shape.

    ## 7. Examples
    Invocation: caller passes `target_path=src/api/users.ts`, `mode=audit`.
    Expected output:

        ## Result
        - Status: FAIL
        - Findings:
          - Missing input validation on POST /users body
          - Error response not wrapped with shared error class
        - Next action: Hand off to backend-engineer skill with these two findings.

    ## 8. Verification Checklist
    - [ ] Output matches the exact shape in Section 4
    - [ ] Status is one of `PASS` or `FAIL` (not `PARTIAL`, `UNKNOWN`, etc.)
    - [ ] Findings are concrete and actionable (not "consider improving X")
    - [ ] No files were modified (skill is read-only per Tool Surface)

## Audit Script Outline

A mechanical audit can be implemented as `scripts/audit_skills.py`. Sketch:

1. Walk every `SKILL.md` under `.claude/skills/` and `~/.claude/skills/`.
2. For each: parse YAML frontmatter; assert `name`, `description` (starts with `Use when`), `allowed-tools` are present.
3. Assert file is ≤150 lines.
4. Assert each of the 8 section headings is present (case-insensitive H2 match).
5. Assert at least 3 bullets under "Anti-Patterns".
6. Assert at least 1 fenced example block under "Examples".
7. Emit a CSV: `skill_name,status,failing_section_or_rule`.
8. Exit non-zero if any non-conforming skill is found — wire into pre-push hook for the skills repo.

## Notes for Auditors

- Do not "soft-pass" a skill that is close. The bar exists because borderline skills compound: 99 borderline skills become 99 silent failures.
- When in doubt, split. Two atomic skills are always better than one ambiguous one.
- Every audit failure becomes a learning entry — log it per [skill-creation-log-convention.md](skill-creation-log-convention.md).
