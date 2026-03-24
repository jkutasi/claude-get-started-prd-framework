#!/usr/bin/env bash
# hooks/session-start.sh
# Fires on SessionStart (startup, clear, compact) events.
# Injects nuclear rules and a skill-load reminder into every session.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
NUCLEAR_RULES_FILE="$PROJECT_ROOT/getting-started/00-nuclear-rules.md"

REMINDER="You are operating inside the SkyHouse AI project template. Load your assigned skill(s) and follow them exactly."

if [ -f "$NUCLEAR_RULES_FILE" ]; then
  echo "<EXTREMELY_IMPORTANT>"
  cat "$NUCLEAR_RULES_FILE"
  echo ""
  echo "$REMINDER"
  echo "</EXTREMELY_IMPORTANT>"
else
  echo "<EXTREMELY_IMPORTANT>"
  echo "$REMINDER"
  echo "</EXTREMELY_IMPORTANT>"
fi
