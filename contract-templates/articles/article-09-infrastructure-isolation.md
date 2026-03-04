# Article 9: Existing Infrastructure Isolation (SISTER PROJECTS ONLY)

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

> **This article applies ONLY when the new project is a sister workspace to an existing master project.** If this is a standalone project, this article may be removed. Owner can override with explicit direction.

The {PROJECT_NAME} workspace MUST NOT modify ANY existing workspace, database, table, cron job, worker, or code in existing workspaces — unless specifically directed by the owner.

Specifically:
- NO writes to {EXISTING_DATA_STORES}
- NO modifications to existing {EXISTING_SERVICES}
- NO modifications to existing {EXISTING_FRONTEND} — new additions only
- The ONLY existing files we modify are: {ALLOWED_MODIFICATIONS}
- The ONLY data stores we write to are: {NEW_DATA_STORES}
- If the project discovers issues with existing infrastructure, REPORT to the owner — do NOT fix
- The owner may override any of the above with explicit direction
