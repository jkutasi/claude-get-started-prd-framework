# Mermaid Diagram Templates

> Copy and adapt these diagrams for your project. Replace all `{PLACEHOLDER}` values with project-specific names. These render natively in GitHub, GitLab, Notion, Obsidian, and most modern Markdown viewers.

---

## 1. Agent Architecture Diagram

> Shows the CTO lead agent, teammate agents, and quality gates in the build pipeline.

```mermaid
flowchart TB
    subgraph LEAD["CTO Lead Agent"]
        CTO["CTO Agent<br/>{CTO_MODEL_NAME}"]
    end

    subgraph TEAM["Teammate Agents"]
        DEV1["{TEAMMATE_1_NAME}<br/>{TEAMMATE_1_ROLE}"]
        DEV2["{TEAMMATE_2_NAME}<br/>{TEAMMATE_2_ROLE}"]
        DEV3["{TEAMMATE_3_NAME}<br/>{TEAMMATE_3_ROLE}"]
        DEV4["{TEAMMATE_4_NAME}<br/>{TEAMMATE_4_ROLE}"]
    end

    subgraph QUALITY["Quality Gates"]
        PR["Peer Review<br/>(3 external models)"]
        RT["Red Team Review<br/>(external hostile model)"]
        QA["QA Swarm<br/>(5 specialist agents)"]
        WT["Whiskey Team<br/>(adversarial testing)"]
        UX["UX Sense Check<br/>(persona-based)"]
    end

    subgraph ARTIFACTS["Deliverables"]
        CODE["Production Code"]
        TESTS["Tests & Gherkin"]
        DOCS["Contracts & Reviews"]
    end

    CTO -->|delegates slices| DEV1
    CTO -->|delegates slices| DEV2
    CTO -->|delegates slices| DEV3
    CTO -->|delegates slices| DEV4

    DEV1 -->|code complete| PR
    DEV2 -->|code complete| PR
    DEV3 -->|code complete| PR
    DEV4 -->|code complete| PR

    PR -->|pass| RT
    RT -->|pass| QA
    QA -->|pass| WT
    WT -->|pass| UX
    UX -->|pass| CODE
    UX -->|pass| TESTS
    UX -->|pass| DOCS

    PR -->|fail| DEV1
    RT -->|fail| DEV1
    QA -->|fail| DEV1
    WT -->|fail| DEV1

    style LEAD fill:#1a1a2e,color:#fff
    style QUALITY fill:#16213e,color:#fff
    style ARTIFACTS fill:#0f3460,color:#fff
```

---

## 2. Data Flow / Feedback Loop Diagram

> Shows how data moves through the system and how feedback loops operate.

```mermaid
flowchart LR
    subgraph INPUT["Data Sources"]
        SRC1["{DATA_SOURCE_1}<br/>{FORMAT}"]
        SRC2["{DATA_SOURCE_2}<br/>{FORMAT}"]
        SRC3["{DATA_SOURCE_3}<br/>{FORMAT}"]
    end

    subgraph PROCESS["Processing Pipeline"]
        INGEST["Ingestion<br/>{INGEST_METHOD}"]
        VALIDATE["Validation<br/>{VALIDATION_RULES}"]
        TRANSFORM["Transformation<br/>{TRANSFORM_LOGIC}"]
        CALC["Calculation<br/>{CALCULATION_ENGINE}"]
    end

    subgraph STORAGE["Persistence"]
        DB[("{DATABASE_NAME}<br/>{DATABASE_TYPE}")]
        CACHE["Cache<br/>{CACHE_TYPE}"]
    end

    subgraph OUTPUT["Outputs"]
        UI["Frontend UI<br/>{FRAMEWORK}"]
        API["API Responses<br/>{API_FORMAT}"]
        REPORT["Reports<br/>{REPORT_FORMAT}"]
    end

    subgraph FEEDBACK["Feedback Loop"]
        MONITOR["Monitoring<br/>{MONITOR_TOOL}"]
        ALERT["Alerts<br/>{ALERT_CONDITIONS}"]
        LOG["Audit Log"]
    end

    SRC1 --> INGEST
    SRC2 --> INGEST
    SRC3 --> INGEST
    INGEST --> VALIDATE
    VALIDATE -->|valid| TRANSFORM
    VALIDATE -->|invalid| ALERT
    TRANSFORM --> CALC
    CALC --> DB
    CALC --> CACHE
    DB --> UI
    DB --> API
    DB --> REPORT
    CACHE --> UI

    UI --> MONITOR
    API --> MONITOR
    MONITOR --> ALERT
    MONITOR --> LOG
    ALERT -->|reprocess| INGEST
```

---

## 3. Slice Dependency Graph

> Shows the build order and dependencies between slices.

```mermaid
flowchart TD
    S0["Slice 0<br/>{SLICE_0_NAME}<br/>Foundation"]
    S1["Slice 1<br/>{SLICE_1_NAME}"]
    S2["Slice 2<br/>{SLICE_2_NAME}"]
    S3["Slice 3<br/>{SLICE_3_NAME}"]
    S4["Slice 4<br/>{SLICE_4_NAME}"]
    S5["Slice 5<br/>{SLICE_5_NAME}"]
    S6["Slice 6<br/>{SLICE_6_NAME}"]
    S7["Slice 7<br/>{SLICE_7_NAME}"]

    S0 --> S1
    S0 --> S2
    S1 --> S3
    S2 --> S3
    S1 --> S4
    S3 --> S5
    S4 --> S5
    S5 --> S6
    S6 --> S7

    classDef done fill:#27ae60,color:#fff,stroke:#27ae60
    classDef active fill:#f39c12,color:#fff,stroke:#f39c12
    classDef blocked fill:#e74c3c,color:#fff,stroke:#e74c3c
    classDef pending fill:#95a5a6,color:#fff,stroke:#95a5a6

    %% Update classes as slices progress:
    %% class S0 done
    %% class S1 active
    %% class S2 active
    %% class S3 blocked
    %% class S4,S5,S6,S7 pending
```

---

## 4. Infrastructure Diagram

> Shows existing infrastructure vs. new components being added.

```mermaid
flowchart TB
    subgraph EXISTING["Existing Infrastructure"]
        direction TB
        EX_DB[("{EXISTING_DATABASE}<br/>{DB_TYPE}")]
        EX_API["Existing API<br/>{EXISTING_API_FRAMEWORK}"]
        EX_AUTH["Auth Provider<br/>{AUTH_PROVIDER}"]
        EX_STORAGE["File Storage<br/>{STORAGE_PROVIDER}"]
    end

    subgraph NEW["New Components (This Project)"]
        direction TB
        NEW_BE["Backend Service<br/>{BACKEND_FRAMEWORK}<br/>{LANGUAGE}"]
        NEW_FE["Frontend App<br/>{FRONTEND_FRAMEWORK}"]
        NEW_DB[("{NEW_DATABASE}<br/>{NEW_DB_TYPE}")]
        NEW_WORKER["Background Worker<br/>{WORKER_FRAMEWORK}"]
    end

    subgraph EXTERNAL["External Services"]
        EXT_API1["{EXTERNAL_SERVICE_1}<br/>{PURPOSE}"]
        EXT_API2["{EXTERNAL_SERVICE_2}<br/>{PURPOSE}"]
    end

    subgraph USERS["Users"]
        BROWSER["Browser Client"]
    end

    BROWSER -->|HTTPS| NEW_FE
    NEW_FE -->|API calls| NEW_BE
    NEW_BE -->|read/write| NEW_DB
    NEW_BE -->|auth| EX_AUTH
    NEW_BE -->|legacy data| EX_DB
    NEW_BE -->|files| EX_STORAGE
    NEW_BE -->|fetch| EXT_API1
    NEW_BE -->|fetch| EXT_API2
    NEW_WORKER -->|process| NEW_DB
    NEW_WORKER -->|fetch| EXT_API1
    EX_API -.->|migration path| NEW_BE

    style EXISTING fill:#2c3e50,color:#fff
    style NEW fill:#1a5276,color:#fff
    style EXTERNAL fill:#7d3c98,color:#fff
```

---

## 5. Sequence Diagram

> Shows component interactions for a specific slice or feature. Create one per slice during Phase A preparation.

```mermaid
sequenceDiagram
    participant USER as {USER_TYPE}
    participant FE as Frontend<br/>{FRONTEND_FRAMEWORK}
    participant API as API Server<br/>{BACKEND_FRAMEWORK}
    participant AUTH as Auth Provider<br/>{AUTH_SERVICE}
    participant DB as Database<br/>{DATABASE_TYPE}
    participant EXT as {EXTERNAL_SERVICE}

    USER->>FE: {USER_ACTION}
    FE->>API: {API_REQUEST} {ENDPOINT}
    API->>AUTH: Verify token
    AUTH-->>API: Token valid

    API->>DB: {DB_QUERY}
    DB-->>API: {DB_RESPONSE}

    alt {SUCCESS_CONDITION}
        API->>EXT: {EXTERNAL_CALL}
        EXT-->>API: {EXTERNAL_RESPONSE}
        API-->>FE: 200 {SUCCESS_RESPONSE}
        FE-->>USER: {SUCCESS_UI_UPDATE}
    else {FAILURE_CONDITION}
        API-->>FE: {ERROR_CODE} {ERROR_RESPONSE}
        FE-->>USER: {ERROR_UI_UPDATE}
    end

    Note over API,DB: {IMPORTANT_NOTE}
```

---

## 6. Entity-Relationship Diagram

> Shows all data entities and their relationships. High-level version created in Slice 0; focused per-slice versions created during each slice's Phase A.

```mermaid
erDiagram
    {ENTITY_1} ||--o{ {ENTITY_2} : "{RELATIONSHIP_VERB}"
    {ENTITY_1} {
        {TYPE} {FIELD_1} PK
        {TYPE} {FIELD_2}
        {TYPE} {FIELD_3}
        {TYPE} created_at
        {TYPE} updated_at
    }

    {ENTITY_2} ||--|{ {ENTITY_3} : "{RELATIONSHIP_VERB}"
    {ENTITY_2} {
        {TYPE} {FIELD_1} PK
        {TYPE} {ENTITY_1}_id FK
        {TYPE} {FIELD_2}
        {TYPE} status
        {TYPE} created_at
    }

    {ENTITY_3} {
        {TYPE} {FIELD_1} PK
        {TYPE} {ENTITY_2}_id FK
        {TYPE} {FIELD_2}
        {TYPE} {FIELD_3}
    }

    {ENTITY_4} }o--|| {ENTITY_1} : "{RELATIONSHIP_VERB}"
    {ENTITY_4} {
        {TYPE} {FIELD_1} PK
        {TYPE} {ENTITY_1}_id FK
        {TYPE} {FIELD_2}
    }
```

**Relationship notation:**
- `||--||` = one to one
- `||--o{` = one to zero-or-many
- `||--|{` = one to one-or-many
- `}o--||` = zero-or-many to one

---

## 7. State Machine Diagram (OPTIONAL)

> For complex workflows with defined states and transitions. **Optional/reference only** — include when your project has UI wizards, multi-step processes, retry logic, or other stateful workflows. Not required for every project.

```mermaid
stateDiagram-v2
    [*] --> {STATE_INITIAL}: {TRIGGER_EVENT}

    {STATE_INITIAL} --> {STATE_VALIDATING}: {ACTION_SUBMIT}
    {STATE_VALIDATING} --> {STATE_VALID}: validation passes
    {STATE_VALIDATING} --> {STATE_INVALID}: validation fails

    {STATE_INVALID} --> {STATE_INITIAL}: user corrects input

    {STATE_VALID} --> {STATE_PROCESSING}: {ACTION_PROCESS}
    {STATE_PROCESSING} --> {STATE_COMPLETE}: processing succeeds
    {STATE_PROCESSING} --> {STATE_ERROR}: processing fails

    {STATE_ERROR} --> {STATE_PROCESSING}: retry
    {STATE_ERROR} --> {STATE_FAILED}: max retries exceeded

    {STATE_COMPLETE} --> {STATE_REVIEWING}: {ACTION_REVIEW}
    {STATE_REVIEWING} --> {STATE_APPROVED}: reviewer approves
    {STATE_REVIEWING} --> {STATE_REJECTED}: reviewer rejects

    {STATE_REJECTED} --> {STATE_INITIAL}: restart workflow

    {STATE_APPROVED} --> [*]
    {STATE_FAILED} --> [*]

    note right of {STATE_PROCESSING}
        {PROCESSING_NOTE}
        Timeout: {TIMEOUT_DURATION}
        Max retries: {MAX_RETRIES}
    end note

    note right of {STATE_REVIEWING}
        {REVIEW_NOTE}
        Required approvers: {APPROVER_COUNT}
    end note
```

---

## Slice 0 Diagram Protocol

**During Slice 0 (Phase A.5),** the Architect creates these high-level overview diagrams for user review:

| # | Diagram | Template | What It Covers |
|---|---------|----------|---------------|
| 1 | System Architecture | Template 1 (Agent Architecture) or Template 4 (Infrastructure) | ALL components, boundaries, new vs existing |
| 2 | Data Model (ER) | Template 6 (ER Diagram) | ALL entities, relationships, cardinality |
| 3 | User Flow | Template 2 (Data Flow) | Full user journey, decision points, paths |
| 4 | Slice Dependency Graph | Template 3 (Slice Dependency) | Build order, slice dependencies |

The user reviews and approves the big picture. No detailed per-slice diagrams at this stage.

**During Slices 1+ (Phase A),** the Architect creates per-slice detailed diagrams:

| Diagram | Template | What It Covers |
|---------|----------|---------------|
| Sequence diagram(s) | Template 5 (Sequence) | This slice's component interactions, API calls, auth flows |
| Focused ER diagram | Template 6 (ER) | Just the entities this slice touches or modifies |

Per-slice diagrams are created as part of preparation, NOT as a blocking user gate. The CTO presents them if useful, but they do not halt the build.

**Saved to:**
- Slice 0 diagrams: `slices/architecture-diagrams.md`
- Per-slice diagrams: `slices/slice-N-diagrams.md`

---

## Usage Notes

1. **Rendering**: Paste these into any Markdown file. They render automatically on GitHub, GitLab, Obsidian, and in VS Code with the Markdown Preview Mermaid extension.

2. **Customization**: Replace all `{PLACEHOLDER}` values. Remove sections that do not apply. Add nodes and connections as needed.

3. **Slice Progress Tracking**: In the Slice Dependency Graph, uncomment and update the `class` lines to visually track which slices are done, active, blocked, or pending.

4. **Colors**: The `style` and `classDef` lines control colors. Adjust to match your project or team preferences.

5. **Live Editor**: Use [mermaid.live](https://mermaid.live) to preview and debug diagrams before committing.

6. **Diagram Lifecycle**: High-level diagrams are created once in Slice 0 and updated in Phase I (Documentation Update) if a later slice changes the architecture. Per-slice diagrams are created fresh for each slice during Phase A.

7. **State Diagrams**: Template 7 (State Machine) is optional. Include only when your project has stateful workflows (wizards, retry logic, multi-step processes). Not required by default.
