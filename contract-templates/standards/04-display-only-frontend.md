# §4 Display-Only Frontend

> Part of [Architecture Standards](../ARCHITECTURE-STANDARDS-TEMPLATE.md). Aligned with [Article 20d](../articles/article-20d-display-only-frontend.md).

Frontend components display data and report user actions. They do **NOT** contain business logic.

> **See also:** [Article 26](../articles/article-26-bff-pattern.md) for the Backend-for-Frontend (BFF) pattern — including API design, one-endpoint-per-view, and worked examples.

## Prohibited in Frontend Components

- Business calculations (totals, averages, scoring, ranking)
- Filtering or sorting by business rules
- Conditional business logic ("if user is premium, show X")
- Data transformation beyond display formatting

## Permitted in Frontend Components

- UI state management (modal open/close, loading indicators, form input values)
- Form input handling and client-side validation for UX feedback
- Display formatting (date formatting, number formatting, currency display)
- The four mandatory states (loading, error, empty, populated) per `coder-frontend.md` §3.1

## The Rule

If the frontend is computing, the API contract is wrong. The backend sends exactly what the frontend needs to render. If the frontend is filtering, sorting, or calculating, the API endpoint should be doing that work.

## Enforcement

- QA Code Quality agent checks for business logic in frontend components (P1 finding).
- Peer reviewers flag any calculation or conditional business rule in client code.
