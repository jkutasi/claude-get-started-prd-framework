# Article 30: Pre-Implementation File Map

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.
>
> **Enforces:** Nuclear Rule 9 (File Structure Defined Before Implementation)

See Nuclear Rule 9 for enforcement. This article provides the implementation pattern.

## File Map Format

After decomposing a slice into narrow concerns (see Article 29), the Team Lead defines:

1. **New files to create** — exact path, exact filename, single responsibility
2. **Existing files to modify** — which files, what kind of change (add a function, extend a class, update a config)
3. **Files NOT to touch** — explicit boundaries so sub-agents don't wander

## Example File Map

| Concern | Action | File |
|---------|--------|------|
| Database copy | Create | `src/campaigns/repos/copy_campaign.py` |
| API endpoint | Modify | `src/campaigns/routes/campaign_routes.py` |
| Validation | Create | `src/campaigns/validation/duplicate_params.py` |
| Service logic | Create | `src/campaigns/services/duplicate_service.py` |
| Frontend button | Modify | `src/campaigns/components/CampaignDetail.tsx` |

Each file stays under 150 lines. Each file does one thing. The structure is decided before a single line of code is written.

**The file map must also include "files NOT to touch"** — explicit boundaries so sub-agents don't wander into shared utilities, unrelated modules, or infrastructure code that isn't part of this slice.

This file map is included in each sub-agent's task assignment. The sub-agent does NOT decide where to put code. The plan tells it. If a sub-agent needs to create or modify a file that isn't on the map, it stops and reports back to the Team Lead — it does not improvise.

## Why This Matters

Without a predefined file map, every sub-agent makes its own decisions about where to put code. Over time, the codebase fills with inconsistent patterns, files in the wrong directories, and multiple concerns crammed into single files. The file map table format gives agents zero ambiguity about where to create files, what to modify, and what not to touch. Without it, agents improvise and the codebase drifts.
