# 3i Detail: UserPromptSubmit Hook Setup

> Companion to [03-slice-0-bootstrap.md](03-slice-0-bootstrap.md) step 3i.

## Check Script

```bash
python3 -c "
import json, pathlib, sys
p = pathlib.Path.home() / '.claude' / 'settings.json'
if not p.exists():
    print('MISSING: ~/.claude/settings.json does not exist')
    sys.exit(1)
s = json.loads(p.read_text())
hooks = s.get('hooks', {})
if 'UserPromptSubmit' not in hooks:
    print('MISSING: UserPromptSubmit hook not found')
    sys.exit(1)
print('OK: UserPromptSubmit hook present')
"
```

## Hook Template

If missing, open `~/.claude/settings.json` (create if needed) and add under `hooks`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'ORCHESTRATOR RULE: You are CTO only. NEVER use Edit/Write/Bash/NotebookEdit directly. Spawn a sub-agent for ALL implementation, large file reads, reviews, QA, and execution. Use Read/Glob/Grep only for lightweight planning. If context is growing, you are doing too much directly — delegate more.'"
          }
        ]
      }
    ]
  }
}
```

If `settings.json` already has content, merge `hooks.UserPromptSubmit` into the existing JSON — do not overwrite the file.
