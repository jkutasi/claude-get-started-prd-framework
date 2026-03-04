# Article 16: UX Sense Check & Persona-Based Testing

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

The UX Sense Check simulates non-technical users interacting with the system via **agent-browser** (Vercel). This catches usability issues that technical QA agents miss because they understand the system's internals.

**agent-browser is MANDATORY for all UX Sense Check testing. No exceptions.**

#### 16a. Role

The UX Sense Check agent simulates non-technical users by driving a real browser via agent-browser. It does NOT read source code. It interacts with the running application exactly as a real user would — clicking, typing, navigating, and judging whether the experience makes sense.

#### 16b. Generic Personas (3 Minimum)

Every UX Sense Check must test with at least these three personas:

| Persona | Description | What They Care About |
|---------|-------------|---------------------|
| **Non-Technical User** | {PERSONA_1_DESCRIPTION — e.g., "First-time user with no technical background, exploring the app without instructions"} | Can they figure out what to do? Is the UI self-explanatory? Do they understand the result? |
| **Power User in a Hurry** | {PERSONA_2_DESCRIPTION — e.g., "Experienced user who uses the app daily and wants maximum efficiency"} | Is the workflow fast? Are there unnecessary clicks? Can they skip what they already know? |
| **First-Time Visitor** | {PERSONA_3_DESCRIPTION — e.g., "Someone who just landed on the app from a link and has zero context"} | Is the purpose of the app obvious? Can they accomplish something useful on their first visit? |

> Customize these personas for your project. The three above are starting points — add project-specific personas as needed.

#### 16c. 7 Test Areas

The UX Sense Check agent MUST evaluate:

| # | Test Area | What to Evaluate |
|---|-----------|-----------------|
| 1 | **First Impression** | Does the user understand what this page/feature does within 5 seconds? Is the purpose obvious? |
| 2 | **Label Clarity** | Are labels, headings, and field names immediately understandable? Would a non-technical user know what "Reconciliation Status" or "Batch ID" means? |
| 3 | **Action Clarity** | Is it obvious what each button, link, and interactive element does BEFORE clicking it? Are CTAs distinguishable from decorative elements? |
| 4 | **Result Comprehension** | After an action completes, does the user understand what happened? Can they interpret the output, the confirmation, the data displayed? |
| 5 | **Error Recovery** | When the user makes a mistake, is it clear what went wrong and how to fix it? Are error messages written for humans, not developers? |
| 6 | **Flow Completeness** | Can the persona complete their primary task end-to-end without getting stuck, lost, or confused? Are there dead ends or missing steps? |
| 7 | **Jargon Detection** | Is there any text, label, tooltip, or message that uses technical jargon, internal terminology, or abbreviations that a non-technical user would not understand? |

#### 16d. Browser Agent Prompt Pattern

The UX Sense Check agent spawns a browser agent with this pattern:

```
You are {PERSONA_NAME}, a {PERSONA_DESCRIPTION}. You are using this
application for the first time. You do NOT know how the code works — you
only see what's on the screen.

Navigate to {URL} and try to {PRIMARY_TASK}.

As you use the app, note:
- Anything confusing or unclear
- Any label or term you don't understand
- Any button where you're not sure what it will do
- Any moment where you're not sure what happened after an action
- Any point where you don't know what to do next
- Any text that a non-technical person wouldn't understand

Score each of the 7 test areas (1-5 scale) and explain your reasoning.
Be honest — if something is confusing, say so. You are not trying to be
nice. You are trying to represent a real user.
```

The browser agent uses **agent-browser** (Vercel) to drive a real browser instance. See the Browser Testing Standard section in the core CLAUDE.md.

#### 16e. Artifact Location

UX Sense Check findings are saved to `reviews/slice-N-ux-sense-check.md`. This file includes:
- Per-persona test results with scores across all 7 test areas
- Screenshots or descriptions of confusing moments
- Prioritized list of UX fixes
- Overall usability score (average across personas and test areas)

#### 16f. Activation

The UX Sense Check runs on **frontend slices only** — any slice that includes UI components, pages, or user-facing changes. Backend-only slices are exempt.

The CTO determines whether a slice is "frontend" at the start of Phase A (Preparation). If any part of the slice touches the UI, the UX Sense Check is required.
