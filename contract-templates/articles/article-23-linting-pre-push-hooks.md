# Article 23: Linting & Pre-Push Hooks (Husky)

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.
>
> **Enforces:** Nuclear Rule 6 (No Hacking — No Lint Ignores)

## Tools by Language

- **Python:** Ruff for linting/formatting, mypy for type checking
- **TypeScript/JavaScript:** ESLint for linting, `tsc --noEmit` for type checking
- **Both languages are checked.** If the project has Python and TypeScript, both get linted and type checked on every push.

## Husky — Pre-Push Enforcement

Husky is a Git hooks manager that enforces quality gates automatically. It runs lint and type check on every push to GitHub. If either check fails, the push is blocked — Git literally refuses to send your code. Code that doesn't pass the linter never reaches the remote repository.

**Setup instructions for agents:**
1. Install Husky and configure pre-push hooks
2. Hooks must run lint check AND type check for all project languages on every push
3. Block the push if any check fails
4. Enable auto-linting in the project
5. Confirm Ruff pre-commit hooks are properly configured (Python)
6. Confirm ESLint + `tsc --noEmit` are wired into the same hooks (TypeScript)

## Why Pre-Push, Not Post-Commit

Commits are frequent, lightweight saves — gating every commit slows down the save-often workflow. The push is the moment code leaves your machine and hits GitHub. That's where the quality gate belongs. Commit freely, but nothing dirty gets pushed to the remote.

## Common Type Errors That Are Still Bugs

These are not ignorable — every one gets fixed properly (Nuclear Rule 6):

- `attr-defined` errors from broken re-exports
- Implicit `Optional` params (`def f(x: str = None)` needs `x: str | None = None`)
- `arg-type` mismatches (passing `None` where `str` is expected)
- Assignment type mismatches
- Wrong types passed to library integrations

## Secrets Scanning in Pre-Push Hooks

Pre-push hooks should also scan for accidentally staged secrets:
- Check for common secret patterns (`API_KEY=`, `token=`, `password=`, `secret=`, connection strings)
- Check for private keys and certificates (`PRIVATE_KEY`, `BEGIN PRIVATE KEY`, `BEGIN RSA`, `BEGIN CERTIFICATE`)
- Check for cloud provider credentials (`aws_access_key_id`, `aws_secret_access_key`, `GOOGLE_APPLICATION_CREDENTIALS`)
- Check for connection string URIs (`mongodb+srv://`, `postgresql://`, `mysql://`, `redis://`, `DATABASE_URL`)
- Check for OAuth/webhook secrets (`client_secret`, `client_id`, `webhook_secret`, `signing_key`)
- Check for hardcoded auth headers (`Authorization: Bearer`)
- Verify `.env` files are not staged
- Flag any file matching `*credential*`, `*secret*`, `*key*` patterns
- Block the push if any potential secret is detected

This is the automated enforcement of Nuclear Rule 4 (Repository Hygiene Before Push) and the Pre-Push Public Repo Checklist (SECURITY.md).

## Why This Matters

Husky is the automated gate that prevents dirty code from reaching GitHub. Without it, quality gates depend on agents remembering to lint — and they won't always remember. Husky makes it mechanical: if it fails, it doesn't ship. No human judgment required.
