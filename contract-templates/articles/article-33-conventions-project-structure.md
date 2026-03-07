# Article 33: Conventions & Project Structure

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

If a convention isn't written down, it doesn't exist. Agents will not infer your preferred folder structure from existing code. Every project needs explicit documentation of where things go, how things are named, and what patterns to follow. Without it, every sub-agent invents its own style.

## What Must Be Defined Per Project

### 1. Folder Structure Convention

Feature-based (recommended) or layer-based.

**Feature-based** means each feature folder contains its own routes, services, repos, validation, and components:
```
src/{feature}/routes/       # Route layer
src/{feature}/services/     # Business logic
src/{feature}/repos/        # Database access
src/{feature}/validation/   # Input validation
src/{feature}/components/   # Frontend components
src/{feature}/types/        # Types/interfaces
src/shared/                 # Cross-cutting (3+ features only)
```

**Layer-based** means `src/routes/`, `src/services/`, `src/repos/` where each layer folder contains files for all features. Feature-based aligns better with separation of concerns and vertical slices.

### 2. Naming Conventions

- **Files:** descriptive, lowercase, hyphen or underscore separated (e.g., `copy_campaign.py`, `campaign-detail.tsx`). No random, auto-generated, or abbreviated names.
- **Functions/methods:** verb-first, descriptive (e.g., `copy_campaign()`, `validate_duplication_params()`, not `process()` or `handle()`)
- **Variables:** descriptive, no single letters outside of loops
- **Components:** PascalCase for React (`CampaignDetail.tsx`), descriptive of what they render

### 3. Where Things Go

| What | Where |
|------|-------|
| Routes/controllers | `src/{feature}/routes/` |
| Business logic/services | `src/{feature}/services/` |
| Database access/repos | `src/{feature}/repos/` |
| Input validation | `src/{feature}/validation/` |
| Frontend components | `src/{feature}/components/` |
| Types/interfaces | `src/{feature}/types/` |
| Cross-cutting utilities | `src/shared/` (only if used by 3+ features) |

### 4. Where Conventions Live

- **Company-wide** (naming, 150-line rule, no console.log) — Engineering Standards doc
- **Project-specific** (folder structure, tech stack, API patterns) — Project CLAUDE.md
- Both loaded by every agent at session start

## Why This Matters

Every agent needs to know — before it writes anything — how this project is organized. Without explicit conventions, each sub-agent invents its own patterns. Over time, the codebase becomes an inconsistent mess of conflicting styles that no one — human or AI — can navigate efficiently. The meta-rule: if a convention isn't written down, it doesn't exist.
