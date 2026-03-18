#!/usr/bin/env bash
# install-hooks.sh — Install git hooks for this repo
# Usage: bash scripts/install-hooks.sh

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOK_DIR="$REPO_DIR/.git/hooks"

# Create post-commit hook
cat > "$HOOK_DIR/post-commit" << 'HOOKEOF'
#!/usr/bin/env bash
# Post-commit hook: sync template repo content to Obsidian vault
# Installed by scripts/install-hooks.sh

REPO_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
SYNC_SCRIPT="$REPO_DIR/scripts/sync-to-vault.sh"

if [ -f "$SYNC_SCRIPT" ]; then
  bash "$SYNC_SCRIPT" &
  echo "[post-commit] Vault sync started in background."
else
  echo "[post-commit] Warning: sync-to-vault.sh not found."
fi
HOOKEOF

chmod +x "$HOOK_DIR/post-commit"
echo "Installed post-commit hook at $HOOK_DIR/post-commit"
