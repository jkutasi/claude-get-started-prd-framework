# Decision Journal

Architecture Decision Records (ADRs) capturing **why** each framework decision was made — not just what the architecture looks like today.

## Purpose

When Claude starts a new project, it sees current state but lacks narrative context: what failed, what was replaced, what prompted each Nuclear Rule. This journal provides that history via semantic search through QMD.

## How It Works

1. **Seed ADRs** in this directory capture the framework's founding decisions.
2. **`seed-vault.sh`** splits them into individual files in your Obsidian vault.
3. **QMD** indexes the vault for semantic search.
4. **CTO orchestrator** queries QMD at Phase A start to retrieve relevant prior decisions.

## Seeding Your Vault

```bash
# Default vault location
bash decision-journal/seed-vault.sh

# Custom vault location
bash decision-journal/seed-vault.sh ~/MyVault
```

This creates `$VAULT_PATH/template-decisions/` with individual ADR files and registers the QMD collection.

## Adding New ADRs

Use the template in `adr-template.md`. Follow these conventions:

- **Naming:** `adr-NNN-kebab-case-title.md` (e.g., `adr-016-new-decision.md`)
- **Framework decisions** go in `template-decisions/` in the vault
- **Project-specific decisions** go in `projects/{PROJECT}/decisions/` in the vault
- **Superseded ADRs:** Set `status: superseded` and add `superseded_by: NNN` in frontmatter

## When to Create an ADR

Create an ADR when you:
- Change framework structure (new phase, new article, new Nuclear Rule)
- Replace a tool or dependency
- Introduce a new pattern or convention
- Make a decision after evaluating alternatives
- Learn something that changes how you'll approach future work

## Integration

The `decision-journal` skill (`.claude/skills/decision-journal/`) defines the full workflow for creating and managing ADRs during slice execution.
