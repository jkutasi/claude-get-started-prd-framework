# CONFIG_SCHEMA.md — Template

> Copy this file to your project root as `CONFIG_SCHEMA.md` during Slice 0.
> Every configurable value in the project must be listed here.
> **No magic numbers.** If a value can change between environments or be tuned,
> it belongs in this schema.

## Config Schema — {PROJECT_NAME}

> Maintained by the Scribe agent. Created during Slice 0 and updated whenever
> a new configurable parameter is introduced.

### Parameters

| Parameter | Type | Default | Range | Description |
|---|---|---|---|---|
| `max_retries` | int | `3` | 1–10 | Maximum retry attempts for transient failures |
| `confidence_threshold` | float | `0.85` | 0.0–1.0 | Minimum confidence score to accept a result |
| `timeout_minutes` | int | `30` | 1–120 | Maximum execution time before a task is killed |
| `batch_size` | int | `100` | 1–10000 | Number of records processed per batch |
| `log_level` | string | `"INFO"` | DEBUG, INFO, WARN, ERROR | Logging verbosity |
| `{STRUCTURED_LOGGER_LEVEL}` | string | `"info"` | debug, info, warn, error | Structured logger verbosity level |
| `{STRUCTURED_LOGGER_PRETTY}` | boolean | `true` | true, false | Pretty-print logs in development (JSON in production) |
| `{ERROR_TRACKING_DSN}` | string | `""` | valid DSN URL | Error tracking service DSN (e.g., Sentry DSN) |

### Rules

1. **Every configurable value** in the codebase must have an entry here.
2. **No magic numbers** — if a numeric value appears in code and could
   reasonably be changed, extract it to config and document it above.
3. **Range column** defines valid boundaries. Code must validate inputs
   against these ranges.
4. **Default column** is what the system uses if no override is provided.
5. When adding a new parameter, also update the validation logic and
   any relevant environment-specific config files.

### Maintenance

- **Created by:** Scribe agent during Slice 0
- **Updated by:** Any agent that introduces a new configurable value
- **Reviewed by:** Peer reviewer checks that new parameters are documented here
