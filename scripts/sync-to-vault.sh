#!/usr/bin/env bash
# sync-to-vault.sh — Mirror template repo content into the Obsidian vault
# Usage: bash scripts/sync-to-vault.sh [VAULT_PATH]
# Called automatically by the post-commit git hook.

set -euo pipefail

VAULT_PATH="${1:-C:\Users\jkuta\Cheviot Capital Dropbox\Jason Kutasi\!SkyHouse - AI\!Cursor\ObsidianVault}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_NAME="$(basename "$REPO_DIR")"

# Map repo name to vault subdirectory
if echo "$REPO_NAME" | grep -qi "refactor"; then
  VAULT_SUBDIR="$VAULT_PATH/template-refactor"
else
  VAULT_SUBDIR="$VAULT_PATH/template-get-started"
fi

echo "[sync-to-vault] Syncing $REPO_NAME → $VAULT_SUBDIR"

# Directories to sync (relative to repo root)
SYNC_DIRS=(
  ".claude/agents"
  ".claude/skills"
  "contract-templates"
  "decision-journal"
  "getting-started"
  "reference"
)

# Clean and recreate vault subdirectory
rm -rf "$VAULT_SUBDIR"
mkdir -p "$VAULT_SUBDIR"

for dir in "${SYNC_DIRS[@]}"; do
  src="$REPO_DIR/$dir"
  if [ -d "$src" ]; then
    # Flatten .claude/ prefix for vault readability
    dest_dir=$(echo "$dir" | sed 's|^\.claude/||')
    mkdir -p "$VAULT_SUBDIR/$dest_dir"
    # Copy only markdown, yaml, and shell files (skip binaries)
    find "$src" -type f \( -name "*.md" -o -name "*.yaml" -o -name "*.yml" -o -name "*.sh" \) | while read -r file; do
      rel="${file#$src/}"
      mkdir -p "$VAULT_SUBDIR/$dest_dir/$(dirname "$rel")"
      cp "$file" "$VAULT_SUBDIR/$dest_dir/$rel"
    done
  fi
done

# Create index file for vault navigation
cat > "$VAULT_SUBDIR/_index.md" << EOF
# $REPO_NAME

Auto-synced from template repo on $(date +%Y-%m-%d\ %H:%M).

## Contents

EOF

for dir in "${SYNC_DIRS[@]}"; do
  dest_dir=$(echo "$dir" | sed 's|^\.claude/||')
  if [ -d "$VAULT_SUBDIR/$dest_dir" ]; then
    count=$(find "$VAULT_SUBDIR/$dest_dir" -type f | wc -l)
    echo "- **$dest_dir/** ($count files)" >> "$VAULT_SUBDIR/_index.md"
  fi
done

total=$(find "$VAULT_SUBDIR" -type f -name "*.md" | wc -l)
echo "" >> "$VAULT_SUBDIR/_index.md"
echo "_${total} markdown files indexed._" >> "$VAULT_SUBDIR/_index.md"

echo "[sync-to-vault] Done: $total files synced to $VAULT_SUBDIR"
