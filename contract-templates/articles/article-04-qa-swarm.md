# Article 4: QA Swarm Requirement

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

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
