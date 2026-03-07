# Article 31: Parallel Execution Rule

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.
>
> **Enforces:** Nuclear Rule 8 (Slices Ship One at a Time)

See Nuclear Rule 8 for enforcement. This article explains the mechanics.

## Parallel Sub-Agents Within One Slice — Good

Each sub-agent is in a different layer touching different files. The database sub-agent can't step on the API sub-agent because they're working on completely different files. There's no overlap, no race condition, no stale reads. This is the 6-agent QA sweep (Article 25), the lint + type check split (Article 24), and the feature decomposition pattern (Article 29) all working as designed.

## Parallel Across Slices — Bad

Slice 2 might depend on something Slice 1 changed. A sub-agent in Slice 2 reads a file that a sub-agent in Slice 1 is actively modifying. Now you've got agents building on top of code that's about to change out from under them. The result is merge conflicts, stale assumptions, and bugs that neither slice's QA process will catch because each slice only verified its own work.

## The Fast-Food Model

A fast-food line doesn't have two teams building different orders using the same grill at the same time. One order gets assembled, verified, and sent to the window. Then the next order starts. Each station (sub-agent) works in parallel on that one order. That's the model.

## Why This Matters

The team needs to understand why parallel within a slice works and parallel across slices doesn't, so they don't try to "speed things up" by running multiple slices at once — which creates the exact bugs that take the longest to find. Serial slices are slower but they eliminate an entire category of bugs that are extremely expensive to debug.
