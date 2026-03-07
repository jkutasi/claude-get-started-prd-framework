# Article 32: Pre-Push Repo Hygiene Checklist

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.
>
> **Enforces:** Nuclear Rule 4 (Repository Hygiene Before Push)

The GitHub repository is the production source of truth. It contains exactly the code that runs the system and nothing else.

## Dead File Cleanup

- Before pushing, scan for files that aren't imported or referenced anywhere in the codebase
- Remove orphaned files — unused utilities, abandoned components, leftover test files, stale configs
- If a refactor made a file unnecessary, delete it in the same commit as the refactor. Don't leave corpses.

## .gitignore Discipline

The workspace may contain project files, research docs, meeting notes, scratch files, and other artifacts that are useful locally but have no business in the remote repository.

- The `.gitignore` must cover all non-code workspace files
- When adding new file types or directories to the workspace, update `.gitignore` in the same commit
- Folders matching `*gitignore*`, `*notes*`, or `ZZ *` are always excluded (Nuclear Rule 4)

## Pre-Push Checklist

1. Scan for unused imports and unreferenced files — remove them
2. Confirm `.gitignore` covers all non-code workspace artifacts
3. Run `git status` and verify no untracked workspace files are staged
4. Confirm no personal notes, scratch files, or `ZZ *` folders are staged
5. If dead files are found, remove them as part of the current commit — not a separate cleanup commit

## Why This Matters

Dead files and workspace artifacts in the repo create confusion — agents read orphaned files thinking they're active, and untracked project files leak into commits. Every file in the remote repository should have a reason to be there. If it doesn't run the system, document the system, or test the system, it doesn't belong. It's not catastrophic, but it's sloppy, and sloppy accumulates.
