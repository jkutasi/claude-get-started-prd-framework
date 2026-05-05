# Article 20h: Migration Strategy

> Part of [Article 20: Code Architecture Standards](article-20-code-architecture.md). Load only when you need this specific subsection.

Existing projects refactor only when touching a file. Do **NOT** rewrite the entire codebase.

## Rules

- **Refactor only when you touch it.** When a bug fix or feature change requires touching an existing file, refactor it into the new pattern (feature folder, layer separation, error wrapping) at that time.
- **New features always use the new structure.** Any new feature created after adopting these standards uses feature-based folders from the start.
- **Over time, the codebase naturally migrates.** As files are touched, they move into the new pattern. After several slices, most active code lives in feature folders.
- **Security during refactoring.** Refactoring is **NOT** exempt from security review. When restructuring code, run the same security checks as new code: OWASP Top 10, secrets scan, dependency audit, auth/authz verification. Code that was secure in its original location may become insecure when moved (e.g., a function that relied on middleware validation in its old route may lack that protection in its new location).

See `contracts/ARCHITECTURE_STANDARDS.md` §8 for further detail.
