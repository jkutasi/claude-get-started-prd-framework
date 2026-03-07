# Article 26: Backend for Frontend (BFF) Pattern

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.
>
> **Cross-references:** ARCHITECTURE-STANDARDS §2 (Three-Layer Separation) and §4 (Display-Only Frontend)

The frontend is dumb. Zero business logic. It only renders data that comes from the backend. All logic, validation, transformations, and decision-making live on the backend. The frontend is a display layer — nothing more.

## What BFF Means

**BFF (Backend for Frontend)** means the API layer is purpose-built to serve exactly what the frontend needs. Instead of generic "get all campaigns" endpoints that force the frontend to filter and reshape data, each API endpoint returns precisely the data a specific view or component requires — already shaped, already filtered, already computed.

## How BFF Works in Practice

- The frontend calls ONE endpoint per view and gets back exactly what it needs to render. No assembling data from multiple API calls on the client side.
- The backend does ALL the work — joining data, filtering, computing derived values, deciding what to show/hide — and delivers a response that maps directly to what the component needs to display.
- API routes are organized around what the frontend needs to see, not around database tables or domain entities.

## Example

A campaign dashboard component needs: campaign name, total spend, ROAS, and a status badge color.

**Without BFF (bad):** Frontend calls `/api/campaigns`, `/api/spend`, and `/api/metrics` separately, then joins and calculates everything client-side. Logic is now in the frontend. Bugs live in two places.

**With BFF (correct):** Frontend calls `/api/dashboard/campaigns` and gets back an array where each item already contains `name`, `totalSpend`, `roas`, and `badgeColor`. The component just renders it. Zero logic. Zero calculations. One fetch call.

## Three-Layer Backend Structure

| Layer | Responsibility | File size |
|-------|---------------|-----------|
| Route layer | Handles HTTP only. Receives request, calls service, sends response. | ~20-30 lines |
| Service layer | Business logic. Calculations, data transformations, decision-making. Knows nothing about HTTP. | Under 150 lines |
| Data / repository layer | Database access only. Queries, inserts, updates. No business logic. | Under 150 lines |

The flow is always: **Route → Service → Data.** Each layer is one concern, one file. When something breaks, the error tracker tells you which layer failed and you fix one small file.

## Rules

1. No business logic in React/frontend components. If a component is doing anything other than rendering data and sending user actions to the backend, it's wrong.
2. No data transformation on the client side. If the frontend is filtering, sorting, computing, or reshaping data, that logic belongs in the backend service layer.
3. API endpoints serve the frontend's exact needs. If a frontend component needs to make multiple API calls and combine the results, the API is missing a BFF endpoint.
4. All new API routes follow the Route → Service → Data pattern. No shortcuts.

## Why This Matters

When business logic creeps into the frontend, it becomes harder to test, harder to debug, and harder for backend agents to reason about. The frontend renders; the backend decides. The BFF pattern is the architecture that makes this work — including API design, one-endpoint-per-view, and the three-layer separation that keeps each file small, testable, and single-purpose.
