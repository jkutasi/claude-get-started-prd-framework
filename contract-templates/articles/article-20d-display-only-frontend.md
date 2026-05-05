# Article 20d: Display-Only Frontend

> Part of [Article 20: Code Architecture Standards](article-20-code-architecture.md). Load only when you need this specific subsection.

Frontend components render data and report user actions. They do **NOT** contain business calculations, filtering by business rules, or conditional business logic.

## Permitted

- UI state management (modals, loading indicators, form input values)
- Form input handling and client-side validation for UX feedback
- Display formatting (dates, numbers, currency)
- The four mandatory states (loading, error, empty, populated)

## Prohibited

- Business calculations (totals, averages, scoring, ranking)
- Filtering or sorting by business rules
- Conditional business logic ("if user is premium, show X")
- Data transformation beyond display formatting

## The Rule

If the frontend is computing, the API contract is wrong. The backend sends exactly what the frontend needs to render.

See [Article 26](article-26-bff-pattern.md) for the Backend-for-Frontend pattern (one endpoint per view).

See `contracts/ARCHITECTURE_STANDARDS.md` §4 for the full enforcement rules.
