# Per-Slice Workflow: Phases E through F.5

> Sub-file of [PER-SLICE-WORKFLOW-TEMPLATE.md](PER-SLICE-WORKFLOW-TEMPLATE.md). Contains Phases E, F, F.5.

```
PHASE E: PEER REVIEW (4 models, adversarial, parallel)
NOTE: Peer review applies to ALL code changes including refactoring.
Refactoring is not exempt from peer review, QA, or security review.
Moving code between files can introduce security regressions.
28. 4 reviewers run in parallel (smartest-of-each-provider):
    - Gemini (smartest available) -- architecture
    - OpenAI 5.5 via openai_code.py -- invariants/security/150-line
      python scripts/openai_code.py qa --code <path> --check code-quality --slice <N>
    - Claude Opus 4.7 (independent sub-agent) -- independent review
    - Grok (smartest available) -- security/edge-case

   +--------------------------------------------------------------+
   | NUCLEAR GATE E: Before proceeding, CTO must confirm:         |
   | [] "Gemini returned findings: {summary}"                     |
   | [] "OpenAI 5.5 returned findings: {summary}"                 |
   | [] "Claude Opus 4.7 returned findings: {summary}"            |
   | [] "Grok returned findings: {summary}"                       |
   | [] "ALL 4 reviewers reported. Not proceeding with partial."  |
   | [] "Round 2 completed after fixes -- no new consensus issues"|
   | [] "Section 3 of reviews/slice-N.md written and non-empty"   |
   | If any box is unchecked: STOP. Violation of Nuclear           |
   | Rule 2. Wait, retry, or report to owner. Do NOT continue.    |
   +--------------------------------------------------------------+

29. CTO synthesizes: consensus issues (2+ reviewers) = mandatory fixes. Round 2 mandatory.

   Consolidated output: reviews/slice-{N}.md (section: Code Peer Review)
   Per-reviewer detail: reviews/slice-{N}/peer-review-{model}.md

PHASE F: QA SWARM + UX SENSE CHECK (AUTONOMOUS FIX)
30. 7 QA agents run in parallel via OpenAI 5.5 script:
    python scripts/openai_code.py qa --code <path> --check <type> --slice <N>
    Types: api-contract | backend | routing | data-integrity | code-quality | security | uiux
    Each QA agent applies Autonomous Defect Resolution Protocol (Article 17e):
      find bug -> spawn fix sub-agent -> AUDIT/RED/GREEN/REGRESSION/CLASS SCAN/COMMIT
31. UX Sense Check runs via agent-browser with all personas
    (Article 16 -- frontend slices only)
32. QA Manager synthesizes all findings + autonomous fix results into report

   Consolidated output: reviews/slice-{N}.md (section: QA + Runtime)
   Per-check detail: reviews/slice-{N}/qa-{check-type}.md

PHASE F.5: AUTOMATED SENTRY CHECK (relay-sentry MCP polling -- MANDATORY)
After the QA swarm completes, relay-sentry polls Sentry automatically for errors that
surfaced during testing. This phase is automated -- no manual log scanning required.

33. relay-sentry MCP polls for new errors triggered during this QA session:
    - Load skill: /relay-sentry
    - Query window: errors in the last 30 minutes, this project + environment
    - Check both frontend (browser SDK) and backend (server SDK) feeds
    - Any new error = CRITICAL finding, must be resolved before Phase I
34. Sentry-to-GitHub Issues integration surfaces critical errors as issues automatically.
35. CTO reviews relay-sentry summary; assigns CRITICAL findings to fix agents.
36. VERIFY STRUCTURED LOGGER IS USED:
    - Grep for raw console.log/error/warn or print() in src/ (excluding tests)
    - Any raw console output found = CRITICAL finding

   +------------------------------------------------------------------+
   | RUNTIME LOG GATE F.5: Before proceeding to Phase I:             |
   | [] "relay-sentry MCP polled -- summary reviewed"                |
   | [] "All CRITICAL Sentry errors from QA session resolved"        |
   | [] "No raw console.log/error/warn or print() in src/ code"      |
   | [] "All findings added to consolidated reviews/slice-{N}.md"    |
   +------------------------------------------------------------------+

   Consolidated output: reviews/slice-{N}.md (section: QA + Runtime, F.5 subsection)
```
