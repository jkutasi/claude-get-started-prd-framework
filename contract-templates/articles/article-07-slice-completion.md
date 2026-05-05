# Article 7: Slice Completion Criteria

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

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
9. `reviews/slice-{N}.md` exists on disk — **consolidated review file** with sections:
   - Test Spec (Gherkin audit + test specification — Article 17)
   - Test Review (test code peer review findings — Article 18)
   - Peer Review (all reviewer findings — Article 03)
   - QA Swarm (all QA findings — Article 04)
   - Red Team Pre-Build (if Phase A.7 was run — Article 14a)
10. Detail files exist under `reviews/slice-{N}/` for each section (linked from the consolidated file)
11. Phase J gate command passed: `python scripts/gate_check.py --slice {N} --all`
    (`gate_check.py` verifies the consolidated `reviews/slice-{N}.md` and required sections)

**If any of these are incomplete, work on the next slice CANNOT begin. No file = no proof = slice is invalid.**

### Article 7b: Coder Self-Check (Pre-Peer-Review)

After the first code pass, every coder agent MUST re-read its own code, identify obvious issues,
and fix them before handing off to peer review. This is an inline step within Phase C — not a
separate phase. Phase D (standalone Self-Reflection) was dropped 2026-05-05 as redundant with
Phase E peer review.

### Article 7c: QA Red Team Protocol

QA agents are **adversaries**, not validators. Every QA skill file must include these four elements:

1. **Adversarial Framing:** The QA agent's prompt must frame the task as adversarial. The coder is talented but fallible. The QA agent's job is to find what they missed. If QA finds nothing, it was not thorough enough.

2. **Specificity of Expectations:** Each QA domain gets a concrete checklist of what to exhaust. Generic "review this code" produces generic results.

3. **Real-World Stakes:** Tell the QA agent what happens if bugs get through. Real consequences change how carefully it looks.

4. **Prior Coverage Report:** Before QA runs, the CTO provides a summary of what has already been checked. This tells the QA agent: the easy stuff is found — go deeper.

**The QA Manager's synthesis report includes:** Total findings per QA agent, categorized by what phase missed them (Phase C coder self-check miss, Phase E peer review miss, or net-new QA-only find). Net-new finds are the most valuable — they prove the QA layer is catching things the earlier phases cannot.

**Autonomous Fix Integration:** Under the Autonomous Defect Resolution Protocol (Article 17e), findings should be accompanied by their resolution status: FIXED (fix sub-agent resolved it), ESCALATED (requires architectural decision or infrastructure change), or FAILED (3 attempts exhausted, awaiting Red Team or owner). The QA Manager's synthesis report tracks autonomous fix success rates alongside finding categories.

### Article 7d: Peer Review Completion Gate

See Nuclear Rule 2. The CTO MUST NOT proceed past peer review until ALL assigned reviewers have returned their findings. No exceptions. If a reviewer is slow or fails, the CTO waits or retries — it does NOT continue with partial reviews.

### Article 7e: Dynamic Agent Creation

Starting roles are a floor, not a ceiling. The CTO spawns new specialist teammates or sub-agents as needed. If a task requires domain expertise not covered by the existing roster, create a new agent with an appropriate skill file.
