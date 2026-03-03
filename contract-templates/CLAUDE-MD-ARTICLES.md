# CLAUDE.md Articles Reference — {PROJECT_NAME}

> **This is the articles reference appendix for the CLAUDE.md contract.** It contains the detailed definitions of Articles 1-19. The core CLAUDE.md file references these articles by number. Load this file on-demand when you need the full definition of a specific article -- do NOT load it by default at session start.
>
> **When to load this file:**
> - When you need to verify the exact rules for peer review (Article 3, 12b)
> - When you need QA swarm procedures (Article 4, 12c)
> - When you need Red Team details (Article 14)
> - When you need Whiskey Team details (Article 15)
> - When you need UX Sense Check details (Article 16)
> - When you need Test-First Specification Protocol details (Article 17)
> - When you need Test Peer Review Protocol details (Article 18)
> - When you need User Scope Confirmation details (Article 19)
> - When you need to verify slice completion criteria (Article 7)

---

## Articles

### Article 1: Code Authorship Prohibition

See Nuclear Rule 1. CTO (Opus) does NOT write code directly. All code via teammates and sub-agents.

**Emergency Protocol — REMOVED.** There are no exceptions to Nuclear Rule 1. If a P0 hotfix is needed, the CTO spawns a teammate or sub-agent with urgent priority. The time saved by the CTO writing code directly is negligible compared to the cost of bypassing peer review and QA. If you are tempted to invoke an "emergency" to write code yourself: that is exactly the failure mode this rule exists to prevent.

### Article 2: Sub-Agent Code Authorship

ALL code is written by Sonnet coder agents (teammates or their spawned sub-agents). Each agent gets ONE focused job (one function, one component, one review). Never a whole module in one agent. Keep tasks small and focused -- this preserves context quality and enables thorough review.

**Test-writer sub-agents are DISTINCT from implementation coders.** Test code (Phase B) is written by test-writer sub-agents spawned by the QA Lead. Implementation code (Phase C) is written by implementation coder sub-agents spawned by Engineers. The same agent MUST NOT write both the tests and the implementation for the same slice. This creates genuine independence -- test-writers design tests without knowing how the code will be implemented, and implementation coders write code to pass tests they did not design.

### Article 3: Multi-Model Peer Review

See Nuclear Rule 2. ALL code reviewed by independent models. ALL reviewers must return findings before proceeding. Consensus issues (flagged by 2+ reviewers) are mandatory fixes.

API keys for peer review are stored in `.env` (local dev) or Secret Manager (prod):
- `GEMINI_API_KEY` — Gemini (reviewer #1)
- `OPENAI_API_KEY` — OpenAI Codex (reviewer #2)
- `XAI_API_KEY` — Grok/xAI (reviewer #3)
- `GREPTILE_API_KEY` — Greptile (reviewer #4, **optional**) — codebase-aware AI review

**Minimum 3 reviewers required.** If `GREPTILE_API_KEY` is configured, Greptile runs as a 4th reviewer in parallel. If not configured, the 3-reviewer workflow is unchanged.

**If peer review has not been run, the code DOES NOT SHIP. Period.**

### Article 4: QA Swarm Requirement

ALL code passes specialized QA swarm after peer review. The QA swarm includes these mandatory agents:

1. **QA Stats** — validates math correctness, algorithm logic, edge cases
2. **QA Code Quality** — clean code, patterns, DRY, naming (Article 10)
3. **QA Data Integrity** — query correctness, schemas, data validation
4. **QA Security** — OWASP, API key exposure, injection vectors
5. **QA UI/UX + Browser** — accessibility, responsive design, browser compat

Plus mandatory additional QA layers:
6. **Whiskey Team** — adversarial QA + implicit behavior regression (Article 15)
7. **UX Sense Check** — persona-based testing via agent-browser (Article 16, frontend slices only)

QA solutions themselves are peer-reviewed by QA agents from different models.

**Autonomous Fix Mandate (Article 17e):** When any QA agent discovers a defect during the swarm, the agent applies the Autonomous Defect Resolution Protocol: spawn a fix sub-agent, execute AUDIT/RED/GREEN/REGRESSION/CLASS SCAN/COMMIT, verify the fix, and report the resolution (not just the finding) in its output. Escalate to user only when the fix requires architectural decisions, touches infrastructure outside the workspace, or has failed 3 times.

**If QA has not been run, the code DOES NOT SHIP. Period.**

### Article 5: Context Window Management

CTO delegates to teammates and sub-agents; receives summaries, not raw output. Ant colony architecture: many small agents doing small focused tasks, rolling up to managers. No agent loads the full project documentation — use DOCS_MAP.md to find relevant files.

**DOCS_MAP first:** Every agent reads `DOCS_MAP.md` before loading any other documentation. Load ONLY the files relevant to your current task. No grep/bash searching for documentation.

### Article 6: Contract Enforcement

Violations of any article are logged with timestamp and description; the owner is notified. Repeated violations result in the offending agent being replaced. The violation log is maintained in `reviews/contract-violations.md`.

### Article 7: Slice Completion Criteria

See Nuclear Rule 3. This is a **hard gate** — no exceptions, no deferral, no "we'll finish it later."

All of the following must be true before a slice ships:

1. Gherkin audit passed (completeness + quality) -- Article 17
2. All tests written by test-writer sub-agents (not implementation coders) -- Article 17
3. All Gherkin scenarios pass
4. All peer reviewers have reviewed and approved (or consensus issues resolved)
5. All QA agents have run and passed
6. Unit test coverage >= 90% for business logic and public interfaces (exemptions for generated code, defensive branches, and bootstrap scaffolding must be documented in the QA roll-up)
7. Documentation updated (via Scribe teammate or Architect)
8. CTO did not write any code or test code itself during the entire slice (Nuclear Rule 1)
9. `reviews/slice-N-test-spec.md` exists on disk with Gherkin audit + test specification (Article 17)
10. `reviews/slice-N-test-review.md` exists on disk with test code peer review findings (Article 18)
11. `reviews/slice-N-peer-review.md` exists on disk with all reviewer findings
12. `reviews/slice-N-qa-swarm.md` exists on disk with all QA findings
13. `reviews/slice-N-red-team-pre-build.md` exists on disk with pre-build gate findings (Article 14a)
14. `reviews/slice-N-red-team.md` exists on disk with post-QA adversarial findings (Article 14b)
15. `reviews/slice-N-whiskey-team.md` exists on disk with whiskey team findings (Article 15)
16. `reviews/slice-N-ux-sense-check.md` exists on disk (frontend slices only -- Article 16)
17. Goal Achievement Test = PASS (Article 15)

**If any of these are incomplete, work on the next slice CANNOT begin. No file = no proof = slice is invalid.**

### Article 7b: Mandatory Self-Reflection

After the first code pass, every coder agent MUST self-reflect before peer review. The agent re-reads its own code, identifies issues, proposes improvements, and returns a self-reflection report. The CTO reviews the reflection and assigns self-identified fixes to a teammate or sub-agent.

### Article 7c: QA Red Team Protocol

QA agents are **adversaries**, not validators. Every QA skill file must include these four elements:

1. **Adversarial Framing:** The QA agent's prompt must frame the task as adversarial. The coder is talented but fallible. The QA agent's job is to find what they missed. If QA finds nothing, it was not thorough enough.

2. **Specificity of Expectations:** Each QA domain gets a concrete checklist of what to exhaust. Generic "review this code" produces generic results.

3. **Real-World Stakes:** Tell the QA agent what happens if bugs get through. Real consequences change how carefully it looks.

4. **Prior Coverage Report:** Before QA runs, the CTO provides a summary of what has already been checked. This tells the QA agent: the easy stuff is found — go deeper.

**The QA Manager's synthesis report includes:** Total findings per QA agent, categorized by what phase missed them (coder self-reflection miss, peer review miss, or net-new QA-only find). Net-new finds are the most valuable — they prove the QA layer is catching things the earlier phases cannot.

**Autonomous Fix Integration:** Under the Autonomous Defect Resolution Protocol (Article 17e), findings should be accompanied by their resolution status: FIXED (fix sub-agent resolved it), ESCALATED (requires architectural decision or infrastructure change), or FAILED (3 attempts exhausted, awaiting Red Team or owner). The QA Manager's synthesis report tracks autonomous fix success rates alongside finding categories.

### Article 7d: Peer Review Completion Gate

See Nuclear Rule 2. The CTO MUST NOT proceed past peer review until ALL assigned reviewers have returned their findings. No exceptions. If a reviewer is slow or fails, the CTO waits or retries — it does NOT continue with partial reviews.

### Article 7e: Dynamic Agent Creation

Starting roles are a floor, not a ceiling. The CTO spawns new specialist teammates or sub-agents as needed. If a task requires domain expertise not covered by the existing roster, create a new agent with an appropriate skill file.

### Article 8: Model Right-Sizing

Opus is reserved EXCLUSIVELY for the CTO Orchestrator. ALL teammates and sub-agents use Sonnet. No exceptions. This ensures the CTO retains maximum context capacity for orchestration and synthesis while sub-agents handle implementation efficiently.

### Article 9: Existing Infrastructure Isolation (SISTER PROJECTS ONLY)

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

### Article 10: Descriptive Naming Convention

ALL files, directories, branches, variables, functions, classes MUST be named descriptively. No random/auto-generated names. No abbreviations without context. Names should be self-documenting.

| Good | Bad | Why |
|------|-----|-----|
| `user-auth-service.py` | `module2.py` | Says what it does |
| `slice-2-data-validation.md` | `distributed-whistling-aurora.md` | No auto-generated names |
| `payment-processing.py` | `m3.py` | Self-documenting |

Enforced in peer review. Violations flagged as mandatory fixes.

### Article 11: Documentation Navigation & Context Window Conservation

All agents read `DOCS_MAP.md` first. Load ONLY relevant files. No grep/bash searching for documentation. The DOCS_MAP is the authoritative index — every agent follows it to find what they need.

### Article 12: NUCLEAR RULE ENFORCEMENT — SUPREME DIRECTIVE (OWNER MANDATE)

**This article overrides ALL other considerations including speed, convenience, context window pressure, and "getting things done quickly."**

**WHY THIS EXISTS:** In a prior project, the CTO (Opus) bypassed the entire multi-agent system — writing ALL code directly as a single agent with ZERO sub-agents, ZERO peer review, and ZERO QA across 6 consecutive slices. This burned context windows, degraded code quality, and violated the contract the owner approved. This must never happen again.

#### 12a. Review Artifacts Are Proof

Before ANY code is considered "done", these artifacts MUST exist on disk:

- `reviews/slice-N-test-spec.md` -- Gherkin audit traceability matrix + test specification + red phase validation (Article 17)
- `reviews/slice-N-test-review.md` -- test code peer review findings from 3 external models (Article 18)
- `reviews/slice-N-peer-review.md` -- findings from all external model reviewers + CTO synthesis + list of mandatory fixes
- `reviews/slice-N-qa-swarm.md` -- findings from all QA agents + QA Manager synthesis + prioritized fix plan
- `reviews/slice-N-red-team-pre-build.md` -- pre-build architecture review (Article 14a)
- `reviews/slice-N-red-team.md` -- post-QA adversarial red team findings (Article 14b)
- `reviews/slice-N-whiskey-team.md` -- whiskey team findings + implicit behavior regression (Article 15)
- `reviews/slice-N-ux-sense-check.md` -- UX sense check findings (Article 16, frontend slices only)

**No file = no proof = slice is invalid.** These files are the PROOF that the process was followed. Verbal claims of "I did the review" without artifact files are not acceptable.

#### 12b. How to Run Peer Review

The CTO spawns 3 sub-agents in parallel (4 if Greptile is configured), each calling one external model/service:

1. **Gemini reviewer:** Sub-agent reads the code, sends to Gemini API, returns structured findings
2. **OpenAI Codex reviewer:** Sub-agent prepares review prompt, executes Codex CLI in read-only sandbox, returns structured findings
3. **Grok reviewer:** Sub-agent reads the code, sends to Grok/xAI API, returns structured findings
4. **Greptile reviewer (optional):** Sub-agent submits code to Greptile API for codebase-aware review, returns structured findings. Only runs if `GREPTILE_API_KEY` is configured.

CTO synthesizes all findings. Issues flagged by 2+ reviewers = MANDATORY fixes. All findings + synthesis saved to `reviews/slice-N-peer-review.md`.

API keys are stored in `.env` (local dev) or Secret Manager (production). They are AVAILABLE. There is NO excuse for skipping this step.

#### 12c. How to Run QA Swarm

The CTO (or QA Lead teammate) spawns QA sub-agents in parallel (red team framing — see Article 7c):

1. QA Stats — validates math correctness, algorithm logic, edge cases
2. QA Code Quality — clean code, patterns, DRY, naming (Article 10)
3. QA Data Integrity — query correctness, schemas, data validation
4. QA Security — OWASP, API key exposure, injection vectors
5. QA UI/UX + Browser — accessibility, responsive design, browser compat (via agent-browser)

Plus the mandatory additional QA layers:
6. Whiskey Team — adversarial QA + implicit behavior regression (Article 15)
7. UX Sense Check — persona-based browser testing (Article 16, frontend slices only)

QA Manager formats all findings into prioritized fix plan. All findings + synthesis saved to `reviews/slice-N-qa-swarm.md`.

#### 12d. Context Window Is NOT an Excuse

The multi-agent system EXISTS to protect context windows. The CTO spawns small, focused sub-agents that each handle one task. This PRESERVES the CTO's context for synthesis and decision-making. Writing all code as a single agent is the OPPOSITE of context conservation — it burns the CTO's context window on implementation details that sub-agents should handle.

If context is running low:
- Assign remaining work to a teammate
- Have them spawn sub-agents and return summaries
- NEVER skip peer review to "save context"

#### 12e. Session Start Checklist

At the START of every new session, before ANY implementation work:

1. Read CLAUDE.md (core contract — start from the top)
2. Check `.env` — verify API keys exist for peer review models
3. Run `python gate_check.py --slice {LATEST_SLICE} --all` to verify all completed slices
4. If ANY slice returns FAIL, run RETROACTIVE REVIEW on that slice first
5. Only then proceed with new work

#### 12f. Retroactive Review Process

If any slice shipped WITHOUT peer review (contract violation), the next session MUST:

1. Check `reviews/` directory for missing artifact files
2. Run retroactive peer review on each unreviewed slice (spawn reviewer sub-agents)
3. Run retroactive QA swarm on each unreviewed slice (spawn QA sub-agents)
4. Save artifacts to `reviews/`
5. Fix any mandatory issues found
6. Only then proceed with new work

ALL code written without peer review is considered UNVALIDATED and SUSPECT. The owner MUST be notified immediately that the process was bypassed.

#### 12g. Commit Convention

Commits MUST include proof of review:

```
[Slice N] Brief description of what changed

- Detail 1
- Detail 2

Co-Authored-By: {AGENT_NAME} ({MODEL})
Reviewed-By: Reviewer Gemini, Reviewer OpenAI Codex, Reviewer Grok
QA-Passed: QA Stats, QA Code Quality, QA Data Integrity, QA Security, QA UI/UX
Red-Team: Passed (reviews/slice-N-red-team.md)
Whiskey-Team: Passed (reviews/slice-N-whiskey-team.md)
```

Commits WITHOUT Reviewed-By and QA-Passed lines are CONTRACT VIOLATIONS.

### Article 13: Background Agent Management & Notification Handling

#### 13a. Foreground vs Background Agent Selection

- **Foreground (default):** Use for agents whose results are needed before proceeding. This includes all coder agents, researcher agents, and any agent whose output feeds the next step.
- **Background (`run_in_background: true`):** Use ONLY when the CTO can meaningfully continue other work while waiting. Examples: parallel peer reviewers (all 3 launched together), parallel QA swarm agents.
- **Rule:** If you launch background agents, you MUST collect ALL their results before declaring that phase complete. Do not move to the next phase while background agents are still running.

#### 13b. Draining Background Agents Before Phase Transition

Before transitioning between workflow phases (e.g., Phase D to Phase E):
1. List all background agents spawned in the current phase
2. Collect results from each (or confirm already collected)
3. Only AFTER all agents are drained may the CTO declare the phase complete

#### 13c. Handling Stale Task Notifications

When a notification arrives for an agent whose results have ALREADY been synthesized:
1. Do NOT respond to the user. The notification is an internal system event.
2. Do NOT acknowledge it individually. Silently note it and continue.
3. If multiple stale notifications arrive, acknowledge them ONCE in a single brief sentence, then stop.

#### 13d. Notification Batching Rule

When the CTO receives multiple notifications in sequence with no user message between them:
- Respond AT MOST ONCE with a brief batch summary
- Never produce more than one response per batch of system notifications
- If the notifications are for already-completed work, a single "These are from the previous phase — already handled." suffices

### Article 14: Red Team Adversarial Review

The Red Team is a dedicated adversarial review layer that operates independently from the standard QA swarm. Its purpose is to find vulnerabilities, design flaws, and failure modes that constructive reviewers miss because they are implicitly trying to confirm the code works.

#### 14a. Pre-Build Gate (Phase A.7 — Architecture Red Team)

Before implementation begins on any slice, the CTO spawns a Red Team sub-agent to review the slice's architecture and design:

- Attack the API design: can endpoints be abused? Are there missing auth checks?
- Attack the data model: can data be corrupted? Are there race conditions?
- Attack the assumptions: what happens when dependencies fail, data is malformed, or load exceeds expectations?
- Attack the integration points: where modules connect, where data crosses boundaries, where trust boundaries exist

Findings are documented. Critical findings BLOCK implementation until resolved.

This gate runs at **Phase A.7** — after preparation is complete, BEFORE any code is written. It is a mandatory gate for every slice.

#### 14b. QA Escalation Gate (Post-Implementation Red Team)

After the standard QA swarm completes, the Red Team runs a second pass specifically targeting:

- Issues that QA agents flagged as LOW that might actually be HIGH in adversarial conditions
- Interaction effects between QA findings (two "low" issues combining into a critical exploit)
- Gaps in QA coverage — areas that no QA agent tested
- Assumptions that QA agents inherited from the coder without challenging

**Escalation Protocol (Autonomous Fix Model):**
```
Attempt 1: Finding agent spawns fix sub-agent -> Autonomous fix protocol
           (AUDIT/RED/GREEN/REGRESSION/CLASS SCAN/COMMIT) -> Finding agent re-tests
Attempt 2: Fix failed or regression -> New fix sub-agent -> Protocol re-run -> Re-test
Attempt 3: STILL fails -> Escalate to Red Team Reviewer (QA Escalation Gate)
If Red Team issues BLOCK -> Escalate to project owner
```

**Escalate to user (bypassing Red Team) when:**
- Fix requires an architectural decision
- Fix modifies infrastructure outside current workspace
- Fix has failed 3 times

**Maximum 3 autonomous fix attempts** before Red Team escalation. Do not let fix loops run indefinitely.

#### 14c. 10 Attack Dimensions

The Red Team MUST evaluate the code across all 10 of these dimensions:

| # | Dimension | What to Attack |
|---|-----------|---------------|
| 1 | **Input Validation** | Malformed inputs, boundary values, type coercion, injection |
| 2 | **Authentication & Authorization** | Privilege escalation, missing auth checks, token handling |
| 3 | **Data Integrity** | Race conditions, partial writes, corruption paths, silent data loss |
| 4 | **Error Handling** | Unhandled exceptions, error swallowing, misleading error messages |
| 5 | **Resource Exhaustion** | Memory leaks, unbounded loops, connection pool exhaustion, disk fill |
| 6 | **Dependency Failures** | External API down, database timeout, network partition, stale cache |
| 7 | **Concurrency** | Race conditions, deadlocks, stale reads, double processing |
| 8 | **Configuration** | Missing config, wrong defaults, secrets in code, environment mismatches |
| 9 | **Business Logic** | Edge cases that produce silently wrong results, rounding errors, off-by-one |
| 10 | **Observability** | Missing logs, misleading metrics, inability to diagnose production issues |

#### 14d. External Model Hostile Prompt

The Red Team sub-agent sends the code to an external model with an explicitly hostile prompt:

```
You are a hostile security researcher who has been hired to find every flaw
in this code. Your reputation depends on finding critical issues. The
developers believe this code is production-ready — prove them wrong. Focus
on: security vulnerabilities, data corruption paths, denial-of-service
vectors, logic errors that produce silently wrong results, and any way a
malicious user could abuse this system.
```

#### 14e. Verdict System

Every Red Team review concludes with exactly one verdict:

| Verdict | Meaning | Effect |
|---------|---------|--------|
| **APPROVE** | Plan/fix is sound. Risks are acceptable. Proceed. | Implementation continues. |
| **REVISE** | Significant issues found. Must address required actions before proceeding. | Return to planning/fixing. |
| **BLOCK** | Critical flaws found. Implementation MUST NOT proceed as designed. | **Halts implementation.** Owner override required. |

**BLOCK is serious.** Only the project owner can override a BLOCK. The override must be documented with the owner's rationale.

#### 14f. Artifact Locations

Red Team findings are saved to:
- **Pre-build:** `reviews/slice-N-red-team-pre-build.md`
- **Post-QA:** `reviews/slice-N-red-team.md`

Both files must exist for the slice to ship. The post-QA red team file is the one referenced in the slice completion criteria (Article 7).

### Article 15: Whiskey Team Adversarial QA & Implicit Behavior Regression

The Whiskey Team is a dedicated adversarial QA layer that tests the system from a "drunk user" perspective — clumsy inputs, wrong order of operations, abandoned workflows, and unexpected usage patterns. It also runs a MANDATORY implicit behavior regression check every session.

#### 15a. Whiskey Team Testing Scope (8 MANDATORY Areas)

The Whiskey Team MUST test all of the following:

| # | Test Category | What to Test |
|---|--------------|-------------|
| 1 | **API Round-Trip Verification** | Send valid, invalid, and malicious payloads to every API endpoint the slice touches. Verify response schema, status code, and data correctness against the data store. |
| 2 | **API-to-Schema Verification** | Compare every API response against the DATA_CONTRACT schemas. Every field must match. Any drift = P0. |
| 3 | **Action Button Verification** | Click every single button on the page. Verify network request, response, UI update, disabled state, and double-click behavior. Zero exceptions. |
| 4 | **Frontend Page Verification** | Load every page the slice touches. Check console errors, interactive elements, keyboard navigation, empty sessions, loading states, error states. |
| 5 | **State Management** | Test flickering, persistence across refresh, error clearing, loading resolution, silent failures, stale state across tabs. |
| 6 | **Early Termination & Partial Completion** | Test early convergence, partial success, zero results, timeout behavior, and re-entry after abandonment. |
| 7 | **Data Integrity** | Verify UI-to-data-store match for every number, string, date. Check number formatting, special characters, null handling, timezone handling. |
| 8 | **Goal Achievement Test** | Navigate the full user workflow end-to-end via agent-browser. Can a user achieve the stated goal? Binary PASS/FAIL. FAIL = P0 = slice cannot ship. |

#### 15b. Implicit Behavior Regression (MANDATORY Every Session — 6 Categories)

This check is MANDATORY at the start of EVERY session and after EVERY slice completion. It catches behaviors that silently change when code is modified — things that no test explicitly covers because they were "obviously correct" before.

| # | Category | What to Verify |
|---|----------|---------------|
| 1 | **State Transition Gaps** | Are there states the system can enter but not exit? Can the user get stuck? |
| 2 | **Cross-Component Interactions** | Does changing component A affect component B in unexpected ways? |
| 3 | **Data Flow Assumptions** | Are there assumptions about data shape that could silently fail? |
| 4 | **Race Conditions** | Can concurrent user actions produce inconsistent state? |
| 5 | **Silent Failures** | Are there operations that fail without any visible error? |
| 6 | **Edge Case Combinations** | What happens when multiple edge cases combine? |

**This is not optional.** Implicit behavior regression is the single most common source of "it works but something feels wrong" bugs. All 6 categories MUST be checked every session.

#### 15c. WHISKEY FINDING Format

Every Whiskey Team finding follows this format:

```
### WHISKEY FINDING #{N}: {Title}
**Category:** {one of the 8 test categories or one of the 6 regression categories}
**Severity:** {CRITICAL / HIGH / MEDIUM / LOW}
**Steps to Reproduce:**
1. {step}
2. {step}
3. {step}
**Expected:** {what should happen}
**Actual:** {what actually happened}
**Impact:** {what this means for the user}
**Roast:** {one-sentence cynical commentary — MANDATORY}
```

#### 15d. Activation & Rules

- The Whiskey Team runs on EVERY slice. No exceptions. Even backend-only slices may have implicit behavior regressions.
- Whiskey Team findings classified as CRITICAL or HIGH are blocking — they must be fixed before the slice ships.
- The Goal Achievement Test (area #8) is a hard gate: if the system does not achieve its stated goal, the slice FAILS regardless of all other tests passing.
- Findings are saved to `reviews/slice-N-whiskey-team.md`.

### Article 16: UX Sense Check & Persona-Based Testing

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

### Article 19: User Scope Confirmation Protocol (Phase A.6)

Before Red Team reviews the plan (Phase A.7) and before any tests are written (Phase B), the CTO MUST present the slice scope to the user for explicit confirmation. This ensures the user's vision — not the AI's interpretation — drives what gets built.

#### 19a. What the CTO Presents

The CTO presents the following to the user at the end of Phase A preparation:

1. **Slice summary** — one paragraph: what this slice delivers and why
2. **Gherkin scenarios** — the acceptance scenarios in plain English (what will be tested)
3. **Per-slice diagrams** — sequence diagram(s) and focused ER diagram (if applicable)
4. **Goal Achievement Test** — the binary test that proves the slice works
5. **What changed** — if learnings from previous slices altered this slice's scope vs. the original plan, highlight what changed and why

#### 19b. User Response

- **APPROVE** → proceed to Phase A.7 (Red Team Pre-Build Gate)
- **REVISE** → user provides feedback, CTO adjusts scope and re-presents
- No iteration limit — the user decides when they are satisfied
- The user does NOT need to review test code. The Gherkin scenarios are the user-facing contract; test code quality is validated by 3-model peer review in Phase B.3.

#### 19c. Slice 0 Special Case

For Slice 0, the User Scope Confirmation covers the full project plan: user story, all slice definitions, high-level diagrams, and the overall architecture. This formalizes the Step 1e plan sign-off as a mechanical gate.

#### 19d. Why Before Red Team

If the user says "that's not what I want," Red Team has not yet wasted time reviewing the wrong plan. Red Team (Phase A.7) reviews a **user-confirmed** scope, not a speculative one. This ordering is intentional.

---

### Article 17: Test-First Specification Protocol

The Test-First Specification Protocol ensures that all tests are written BEFORE implementation code, by DIFFERENT agents than those who write the implementation. This creates genuine independence and makes the test suite the source of truth for correctness.

#### 17a. Gherkin Audit (Phase B.1)

Before any test code is written, the QA Lead audits all Gherkin scenarios for the current slice:

**Completeness check:**
- Every user story element must map to at least one Gherkin scenario
- Every required edge case must map to at least one Gherkin scenario
- A traceability matrix is produced showing the mapping

**Quality check:**
- Each scenario is unambiguous (one interpretation, not multiple)
- Each scenario uses concrete values (not "a valid input")
- Each expected outcome is testable and specific
- NFR gaps checked (performance, security criteria have scenarios where applicable)

**Max 3 audit cycles.** If gaps remain after 3 cycles, owner sign-off is required to proceed.

#### 17b. Skeletal Interfaces

Before test-writers write tests, the Architect defines skeletal interfaces for all modules the slice will create or modify:

- Function signatures with type annotations and `raise NotImplementedError`
- Class outlines with method stubs returning `pass` or `raise NotImplementedError`
- Type stubs / interfaces for data structures

This allows tests to import modules cleanly. Both import errors and assertion failures are valid red states, but clean assertion failures are preferred for diagnostic clarity.

#### 17c. Test Specification (Phase B.2)

Test-writer sub-agents (spawned by QA Lead) write ALL test code:

- **Unit tests** -- individual functions, methods, classes in isolation
- **Integration tests** -- module interactions, database queries, API endpoints
- **E2E test definitions** -- full workflow definitions (actual browser E2E runs in Phase F)

Test-writers receive: Gherkin scenarios + slice spec + data contracts + skeletal interfaces. They write tests WITHOUT knowing how the code will be implemented.

**All tests must be RED** (failing) before proceeding. Tests that PASS against skeletal interfaces are bad tests -- they must be fixed.

#### 17d. Agent Separation

| Responsibility | Agent | Phase |
|---|---|---|
| Audit Gherkin completeness + quality | **QA Lead** | B.1 |
| Write test code | **Test-writer sub-agents** (spawned by QA Lead) | B.2 |
| Review test code | **Reviewer Gemini, OpenAI Codex, Grok** | B.3 |
| Write implementation code | **Implementation coder sub-agents** (spawned by Engineers) | C |

The same agent MUST NOT write both tests and implementation for the same slice. This is enforced by Nuclear Rule 1 gate: "CTO did NOT write any test code directly."

#### 17e. Autonomous Defect Resolution Protocol

Any agent that discovers a defect OWNS the fix lifecycle. The finding agent does not report and wait — it drives the defect to resolution by spawning a fix sub-agent and verifying the result. This applies in ALL testing phases (F, G, H, E2E Browser Testing, Peer Review).

**Fix Ownership Rule:** The agent that finds the bug spawns a **fix sub-agent** (ephemeral coder) to execute the protocol below. The finding agent verifies each step. The finding agent does NOT write production code itself — it delegates to the fix sub-agent and validates the outcome. This preserves role separation (QA agents do not write production code) while eliminating the bottleneck of routing every fix through the CTO.

Triggered by ANY source: user bug report, QA finding, security scan, Whiskey Team finding, peer review consensus finding, regression detection.

```
Step 1: AUDIT THE TEST
  Find the test that SHOULD have caught this defect.
  - Test exists but didn't catch it -> FIX THE TEST FIRST
  - No test exists -> Add Gherkin scenario first, then write test

Step 2: RED
  Run the corrected/new test against current (buggy) code. It MUST FAIL.
  - If it passes -> test still wrong, go back to Step 1

Step 3: GREEN
  Fix sub-agent fixes the production code until the test passes.

Step 4: REGRESSION
  Run the FULL test suite. Zero regressions allowed.
  - If regressions found -> fix sub-agent addresses them before proceeding

Step 5: CLASS SCAN
  Determine if the defect reveals a CATEGORY of missing coverage.
  - If yes: scan the ENTIRE codebase for all instances of the same pattern
  - Write tests for ALL instances (not just the one that was found)
  - Fix ALL instances in the same pass
  - Example: if a null-check was missing on one API endpoint, check ALL
    endpoints for the same missing null-check and fix them all

Step 6: COMMIT
  Test + fix committed together as an atomic unit.
  Commit message references the finding ID and the class scan scope.
```

**The test is always the source of truth.** A bug means the test was incomplete or wrong. Fix the test first, then fix the code. This ensures every bug found once is caught forever.

**Escalate to the user ONLY when:**
- The fix requires an architectural decision that changes the system design
- The fix modifies infrastructure outside the current workspace
- The fix has failed 3 times (3 fix sub-agent attempts, not 3 reporting cycles)

All other defects are resolved autonomously. The CTO is notified of completed fixes in the QA roll-up but does not need to approve each one individually.

#### 17f. Artifact

The test specification is saved to `reviews/slice-N-test-spec.md`. This file must exist on disk before Phase C (Implementation) can begin. See `review-templates/TEST-SPEC-TEMPLATE.md` for the full template.

### Article 18: Test Peer Review Protocol

Test code receives the same multi-model peer review as implementation code. This ensures test quality, coverage completeness, and assertion specificity are validated by independent models before implementation begins.

#### 18a. Review Process (Phase B.3)

After test-writer sub-agents complete Phase B.2, the CTO spawns 3 reviewer sub-agents in parallel (4 if Greptile is configured):

1. **Reviewer Gemini** -- reads test code, sends to Gemini API with test review prompt, returns structured findings
2. **Reviewer OpenAI Codex** -- reads test code, executes Codex CLI in read-only sandbox with test review prompt, returns structured findings
3. **Reviewer Grok** -- reads test code, sends to Grok/xAI API with test review prompt, returns structured findings
4. **Reviewer Greptile (optional)** -- submits test code to Greptile API for codebase-aware review, returns structured findings. Only if `GREPTILE_API_KEY` is configured.

ALL mandatory reviewers (minimum 3) must return before proceeding. No partial reviews.

#### 18b. Review Criteria

Each reviewer evaluates the test code against:

1. **Test Quality** -- Are assertions specific and meaningful? Do they test behavior, not implementation details?
2. **Coverage Gaps** -- Are there user story elements, edge cases, or Gherkin scenarios without corresponding tests?
3. **Assertion Specificity** -- Do tests assert exact expected values, or vague checks (e.g., `assert result is not None`)?
4. **Mock Correctness** -- Do mocks match real behavior? Are mocks simpler than reality?
5. **Test Independence** -- Can tests run in any order? Do they share state?
6. **Red Phase Validity** -- Are all tests genuinely RED for the right reason?
7. **Gherkin Alignment** -- Does each test clearly trace back to a Gherkin scenario?

#### 18c. Consensus Rules

- Issues flagged by 2+ reviewers = **mandatory test fixes** before proceeding to Phase C
- Issues flagged by 1 reviewer = **recommended fixes** (CTO judgment)
- Mandatory fixes are assigned to test-writer sub-agents (not implementation coders)
- Fixed tests must be re-validated: still RED against skeletal interfaces

#### 18d. Artifact

Test peer review findings are saved to `reviews/slice-N-test-review.md`. This file must exist on disk before Phase C (Implementation) can begin. See `review-templates/TEST-REVIEW-TEMPLATE.md` for the full template.
