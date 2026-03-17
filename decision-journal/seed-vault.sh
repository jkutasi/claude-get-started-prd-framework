#!/usr/bin/env bash
# seed-vault.sh — Split seed ADRs into individual files in an Obsidian vault
# Usage: bash decision-journal/seed-vault.sh [VAULT_PATH]

set -euo pipefail

VAULT_PATH="${1:-$HOME/ObsidianVault}"
TARGET_DIR="$VAULT_PATH/template-decisions"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Decision Journal Vault Seeder ==="
echo "Vault path: $VAULT_PATH"
echo "Target dir: $TARGET_DIR"
echo ""

# Create target directory
mkdir -p "$TARGET_DIR"

# ADR definitions: number|title|tags|seed-file|section-header
ADRS=(
  "001|Contract-Based Architecture|architecture, contracts, enforcement|seed-adrs-core.md|ADR-001"
  "002|Three-Model Peer Review|peer-review, quality, multi-model|seed-adrs-core.md|ADR-002"
  "003|Autonomous QA Pipeline|qa, automation, pipeline|seed-adrs-core.md|ADR-003"
  "004|MCP Relay Pattern|mcp, relay, context-management|seed-adrs-core.md|ADR-004"
  "005|Repository Hygiene as Nuclear Rule|nuclear-rules, git, hygiene|seed-adrs-core.md|ADR-005"
  "006|Workflow Consolidation (9 Nuclear Rules + Articles)|nuclear-rules, articles, consolidation|seed-adrs-core.md|ADR-006"
  "007|Mandatory Observability Gates|observability, sentry, pino, gates|seed-adrs-evolution.md|ADR-007"
  "008|Professor Review System|review, professors, domain-expertise|seed-adrs-evolution.md|ADR-008"
  "009|Error & Rescue Registry|error-handling, registry, article-35|seed-adrs-evolution.md|ADR-009"
  "010|Mem0 to QMD Migration|knowledge, qmd, mem0, privacy|seed-adrs-evolution.md|ADR-010"
  "011|Skills v2 (YAML Frontmatter)|skills, yaml, discovery|seed-adrs-evolution.md|ADR-011"
  "012|Agent/Skill Separation|agents, skills, separation-of-concerns|seed-adrs-evolution.md|ADR-012"
  "013|UserPromptSubmit Hook (Nuclear Rule 10)|hooks, enforcement, file-size|seed-adrs-config.md|ADR-013"
  "014|Codex Model Version Pinning|models, codex, version-pinning|seed-adrs-config.md|ADR-014"
  "015|Settings.json Permission Structure|settings, permissions, security|seed-adrs-config.md|ADR-015"
)

count=0
for entry in "${ADRS[@]}"; do
  IFS='|' read -r num title tags source_file section <<< "$entry"
  kebab=$(echo "$title" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
  filename="adr-${num}-${kebab}.md"
  source_path="$SCRIPT_DIR/$source_file"

  # Extract section from seed file (from ## header to next ## or end)
  content=$(sed -n "/^## ${section}:/,/^## ADR-/p" "$source_path" | head -n -1)
  if [ -z "$content" ]; then
    # Last section in file — extract to end
    content=$(sed -n "/^## ${section}:/,\$p" "$source_path")
  fi

  # Write individual ADR file with frontmatter
  cat > "$TARGET_DIR/$filename" << ADREOF
---
type: adr
status: accepted
date: $(echo "$content" | grep -oP '(?<=\*\*Date:\*\* ).*' | head -1)
supersedes: null
tags: [$tags]
---

# ADR-${num}: ${title}

$(echo "$content" | sed '1,/^\*\*Tags:\*\*/d' | sed '1d')
ADREOF

  count=$((count + 1))
  echo "  Created: $filename"
done

# Create index file
cat > "$TARGET_DIR/_index.md" << 'IDXEOF'
# Template Framework Decision Journal

Architecture Decision Records for the Claude Code template framework.

## Index

IDXEOF

for entry in "${ADRS[@]}"; do
  IFS='|' read -r num title tags source_file section <<< "$entry"
  kebab=$(echo "$title" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
  echo "- [[adr-${num}-${kebab}|ADR-${num}: ${title}]]" >> "$TARGET_DIR/_index.md"
done

echo ""
echo "=== Done: $count ADR files created in $TARGET_DIR ==="
echo ""
echo "Register with QMD by running:"
echo ""
echo "  qmd collection add $TARGET_DIR --name template-decisions"
echo "  qmd context add qmd://template-decisions \"Architecture decisions for the Claude Code template framework\""
echo ""
echo "Verify with:"
echo "  qmd status"
echo "  qmd query \"why three model peer review\""
