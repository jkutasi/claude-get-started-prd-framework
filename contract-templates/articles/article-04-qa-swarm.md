# Article 4: QA Swarm Requirement

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

ALL code passes specialized QA swarm after peer review (Phase F). The QA swarm includes these
mandatory agents, each invoked via `python scripts/openai_code.py qa --check <type>`:

1. **QA Stats** — validates math correctness, algorithm logic, edge cases
   `python scripts/openai_code.py qa --check stats`
2. **QA Code Quality** — clean code, patterns, DRY, naming (Article 10)
   `python scripts/openai_code.py qa --check code-quality`
3. **QA Data Integrity** — query correctness, schemas, data validation
   `python scripts/openai_code.py qa --check data-integrity`
4. **QA Security** — OWASP, API key exposure, injection vectors
   `python scripts/openai_code.py qa --check security`
5. **QA UI/UX + Browser** — accessibility, responsive design, browser compat (frontend slices only)
   `python scripts/openai_code.py qa --check uiux`

All QA agents run on **OpenAI 5.5** via the `openai_code.py qa` subcommand. Prompts must
cover the anti-patterns cataloged in Articles 36/38 (production failures, DB smoke patterns).

**UX Sense Check** (Article 16) remains available for frontend slices as an optional add-on;
it is no longer a mandatory swarm member.

QA solutions themselves are peer-reviewed by QA agents from different models.

**Autonomous Fix Mandate (Article 17e):** When any QA agent discovers a defect, the agent
applies the Autonomous Defect Resolution Protocol: spawn a fix sub-agent, execute
AUDIT/RED/GREEN/REGRESSION/CLASS SCAN/COMMIT, verify the fix, and report the resolution (not
just the finding) in its output. Escalate to user only when the fix requires architectural
decisions, touches infrastructure outside the workspace, or has failed 3 times.

**If QA has not been run, the code DOES NOT SHIP. Period.**
