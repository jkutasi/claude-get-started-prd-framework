# QA Lead — Operational Checklist

Execute in order every QA phase:

- [ ] **QMD QUERY** (non-blocking): Spawn `/relay-qmd` — `"QA failures root causes {SLICE_TOPIC}"` in `{PROJECT_NAME}` before starting QA
- [ ] Read `QA_LEARNINGS.md`
- [ ] Read slice spec — identify surfaces touched
- [ ] Determine activation set (which agents to spawn)
- [ ] Run Gherkin Audit (Phase B.1) — completeness + quality, max 3 cycles
- [ ] Spawn test-writer sub-agents (Phase B.2) — ALL tests RED
- [ ] Verify all tests RED (import errors or assertion failures)
- [ ] Coordinate test peer review (Phase B.3) — 3+ external models (+ Greptile if configured)
- [ ] Verify `reviews/slice-{N}-test-spec.md` EXISTS on disk
- [ ] Verify `reviews/slice-{N}-test-review.md` EXISTS on disk
- [ ] Spawn Red Team Pre-Build Gate (Phase A.7) — before any code
- [ ] Spawn Professor Pre-Build Review (Phase A.7) — minimum 2 professors
- [ ] Verify Professor verdict is APPROVE or addressed REVISE
- [ ] Spawn Standard QA Swarm after implementation (Phase F)
- [ ] Spawn Whiskey Team after implementation (Phase F)
- [ ] Spawn UX Sense Check if frontend-touching (Phase F)
- [ ] Verify Whiskey Team ran all 6 implicit regression categories
- [ ] Verify Whiskey Team ran Goal Achievement Test
- [ ] Collect all findings
- [ ] Verify all QA agents applied Autonomous Defect Resolution Protocol (Phase F)
- [ ] Verify all FIXED items: test + fix committed, regression suite green
- [ ] Collect ESCALATED items (architectural/infrastructure/3x-failed)
- [ ] Package FAILED items for Red Team escalation (Article 14b)
- [ ] Handle Red Team escalations (max 3 autonomous fix attempts per defect)
- [ ] Handle Professor escalations (P0 findings = BLOCK)
- [ ] Produce QA Roll-Up (include autonomous fix results)
- [ ] Write new learnings to `QA_LEARNINGS.md`
- [ ] **QMD SAVE** (non-blocking): Save novel QA findings to `/relay-qmd` in `{PROJECT_NAME}` — defect patterns, root causes, fix strategies
- [ ] Verify `reviews/slice-{N}-professor-pre-build.md` EXISTS on disk
- [ ] Verify `reviews/slice-{N}-professor.md` EXISTS on disk (if escalation triggered)
- [ ] Deliver verdict to CTO via QA Manager

## QA Roll-Up Template

```
## QA Roll-Up — Slice {N}: {SLICE_TITLE}

### Summary
- Total findings: {COUNT}
- P0 (blocking): {COUNT} / P1 (high): {COUNT} / P2 (medium): {COUNT} / P3 (low): {COUNT}

### Agent Reports
| Agent | Findings | P0 | P1 | Status |
|---|---|---|---|---|
| Stats QA | ... | .. | .. | PASS / FAIL |
| Code Quality | ... | .. | .. | PASS / FAIL |
| Data Integrity | ... | .. | .. | PASS / FAIL |
| Security QA | ... | .. | .. | PASS / FAIL |
| UI/UX QA | ... | .. | .. | PASS / FAIL |
| Red Team | ... | .. | .. | APPROVE / REVISE / BLOCK |
| Whiskey Team | ... | .. | .. | PASS / FAIL |
| UX Sense Check | ... | .. | .. | PASS / FAIL / N/A |

### Goal Achievement Test
- Result: PASS / FAIL

### QA Verdict
- [ ] PASS — All P0 resolved, Goal Achievement passes, no BLOCK from Red Team
- [ ] FAIL — Blocking issues remain
```
