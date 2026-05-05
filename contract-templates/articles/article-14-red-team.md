# Article 14: Red Team Adversarial Review

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

The Red Team is a dedicated adversarial review layer that operates independently from the standard QA swarm. Its purpose is to find vulnerabilities, design flaws, and failure modes that constructive reviewers miss because they are implicitly trying to confirm the code works.

#### 14a. Pre-Build Gate (Phase A.7 — Architecture Red Team) — OPTIONAL

> **Phase A.7 is OPTIONAL as of 2026-05-05.** It is skipped by default. Opt-in only for
> high-risk slices: `--high-risk` flag in the slice workflow. Examples of high-risk: new
> authentication surfaces, payment flows, data migration, or cross-service trust boundaries.

Before implementation begins on high-risk slices, the CTO spawns a Red Team sub-agent to review
the slice's architecture and design:

- Attack the API design: can endpoints be abused? Are there missing auth checks?
- Attack the data model: can data be corrupted? Are there race conditions?
- Attack the assumptions: what happens when dependencies fail, data is malformed, or load exceeds expectations?
- Attack the integration points: where modules connect, where data crosses boundaries, where trust boundaries exist

Findings are documented. Critical findings BLOCK implementation until resolved.

When run, this gate runs at **Phase A.7** — after preparation is complete, BEFORE any code is
written. If skipped, the `reviews/slice-{N}.md` Red Team Pre-Build section is marked N/A.

#### 14b. QA Escalation Gate (Post-Implementation Red Team)

> **Phase G (Red Team Post-Build) was dropped 2026-05-05.** It duplicated Phase E peer review.
> Post-build adversarial coverage is now handled by Phase E's 4-model adversarial lineup
> (Article 03). This section describes the escalation-only path when QA bugs refuse to die.

When a bug persists through 3 autonomous fix attempts, the Red Team runs a targeted pass:

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
| 10 | **Observability** | Missing structured logs, raw console output instead of structured logger, no error tracking integration, inability to trace errors across layers (route → service → repository), misleading metrics, missing error context in log entries |

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

Red Team findings are saved as sections within the consolidated review file:
- **Pre-build (if A.7 run):** section in `reviews/slice-{N}.md` + detail file `reviews/slice-{N}/red-team-pre-build.md`
- **QA escalation (if triggered):** section in `reviews/slice-{N}.md` + detail file `reviews/slice-{N}/red-team-escalation.md`

If Phase A.7 was skipped (default), the pre-build section is marked N/A. See Article 7 for
consolidated review file requirements.
