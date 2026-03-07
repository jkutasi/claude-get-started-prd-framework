# Article 21: Commit vs. Push

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

These are not the same thing.

- **Commit** = "Save." It groups the code changes you just made into a single, traceable unit. The changes are written to your local Git history but have NOT been sent to GitHub yet.
- **Push** = "Send." It uploads your committed changes to the remote repository (the central copy on GitHub that the whole team shares).

If a commit is garbage, you can roll it back locally before it ever hits the remote. Commits are frequent, lightweight saves. Pushes are quality-gated exports. Never conflate the two.

## Why This Matters

If the team doesn't understand the difference, they lose the ability to roll back bad work cleanly. Conflating commit and push means every save goes straight to GitHub with no local safety net. Understanding this distinction is foundational to the entire workflow.
