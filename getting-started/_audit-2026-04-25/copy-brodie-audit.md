## Audit: copy-brodie — 2026-04-25
- File: C:\Users\jkuta\.claude\skills\copy-brodie\SKILL.md
- Line count: 62
- Status: NON_CONFORMING

### Findings
- §1 — Trigger / When-to-use section missing. No "Use when X" or "Do not use when Y" clause anywhere in the file. The file opens with Identity/Background sections that describe the persona, not invocation conditions.
- §2 — Inputs section missing. No declaration of what context, files, or parameters the calling agent must supply.
- §3 — Procedure section non-conforming. Sections §4 (Writing Protocol) and §5 (Critique Protocol) are persona operation protocols, not numbered atomic skill-invocation steps with one verb per step.
- §4 — Outputs section missing. No specification of the artifact shape the skill produces.
- §5 — Tool surface section missing from body. Allowed tools appear only in frontmatter; no dedicated body section mirrors or explains the tool surface.
- §7 — Examples section missing. No fenced invocation block with verbatim expected output.
- §8 — Verification checklist missing. No mechanical checkbox list for the calling agent to confirm correct execution.
- Frontmatter — description field does not start with "Use when". Current value: "Ian Brodie — Email Persuasion & Relationship Selling. Direct-response copywriting persona." Contract requires the description to be a trigger clause starting with "Use when".
- CREATION-LOG.md absent from C:\Users\jkuta\.claude\skills\copy-brodie\ (required by audit checklist item 10).

### Verdict
NON_CONFORMING. Eight distinct gaps: five missing required sections (§1 Trigger, §2 Inputs, §4 Outputs, §5 Tool surface body, §7 Examples), one missing required artifact (§8 Verification checklist), one malformed frontmatter description, and absent CREATION-LOG.md. Anti-patterns (§6) pass with 7 named items. Line count (62) is within the 150-line limit.
