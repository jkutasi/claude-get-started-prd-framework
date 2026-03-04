# Article 5: Context Window Management

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

CTO delegates to teammates and sub-agents; receives summaries, not raw output. Ant colony architecture: many small agents doing small focused tasks, rolling up to managers. No agent loads the full project documentation — use DOCS_MAP.md to find relevant files.

**DOCS_MAP first:** Every agent reads `DOCS_MAP.md` before loading any other documentation. Load ONLY the files relevant to your current task. No grep/bash searching for documentation.

**Structural Insight:** Blown-out context windows are a structural problem, not a tool problem. When production source files are small (under 150 lines per Article 20) and concerns are isolated (one responsibility per file), agents never need large context windows. The 150-line file limit and feature-based folder structure (Article 20) address context window management at the architectural level — not by managing the symptom (token limits) but by eliminating the cause (large, multi-concern files).
