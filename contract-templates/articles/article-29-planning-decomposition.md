# Article 29: Planning-Phase Decomposition

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.
>
> **Enforces:** Nuclear Rule 9 (File Structure Defined Before Implementation)

LLMs are bad at vertical slices. A vertical slice cuts through every layer of the app — database, API, business logic, frontend — and LLMs struggle to hold all those layers in context simultaneously. The wider the slice, the more context the agent needs, and the more things get missed or broken.

The fix: decompose before anyone writes code. The human is the architect. The agents are the builders.

## The Decomposition Flow

1. **Macro user story** — the big-picture feature ("add campaign duplication")
2. **Vertical slices** — break the macro story into shippable increments. Each slice delivers a thin, working piece of the feature end-to-end.
3. **Narrow concerns (sub-stories)** — decompose each slice further into single-layer concerns. Each concern touches one layer, one file (or a small group of related files), and has one job. This is where the work becomes LLM-friendly.

## Example — "Add Campaign Duplication"

Macro story: "Add campaign duplication"

Slice 1: "Duplicate a campaign with its adsets and ads"

Narrow concerns within Slice 1:

| Concern | Layer | File |
|---------|-------|------|
| Database copy function | Repository | `src/campaigns/repos/copy_campaign.py` |
| API endpoint | Route | `src/campaigns/routes/campaign_routes.py` |
| Input validation | Validation | `src/campaigns/validation/duplicate_params.py` |
| Service logic | Service | `src/campaigns/services/duplicate_service.py` |
| Frontend button | Component | `src/campaigns/components/CampaignDetail.tsx` |

Each concern → one sub-agent. Each sub-agent gets only the files relevant to its concern. The sub-agent doesn't need to understand the whole system — just its piece.

## Context Window Bombs

The narrower the concern, the less context the agent needs, and the less can go wrong. "Add the database query that copies a campaign row" is almost impossible to screw up. "Build campaign duplication" is a context window bomb — it overloads the AI's working memory and the AI starts forgetting, hallucinating, and making mistakes.

**This decomposition happens during planning, not during implementation.** The Team Lead or CTO agent decomposes the work. The sub-agents receive their narrow concern and execute. If a sub-agent is being asked to touch multiple layers or think about the whole feature, the decomposition wasn't narrow enough.

## Why This Matters

LLMs choke on wide vertical slices because they can't hold multiple layers in context simultaneously. Decomposing each slice into narrow, single-layer concerns before coding is the single biggest lever for getting good output from AI agents. Skip this and agents produce context-window bombs that drift, hallucinate, and break.
