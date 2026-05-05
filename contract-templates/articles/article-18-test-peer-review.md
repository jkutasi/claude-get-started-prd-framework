# Article 18: Test Peer Review Protocol

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

Test code receives the same multi-model peer review as implementation code. This ensures test quality, coverage completeness, and assertion specificity are validated by independent models before implementation begins.

#### 18a. Review Process (Part of Phase B — no separate B.3)

> **As of 2026-05-05, Test Peer Review is integrated into Phase B.** There is no separate Phase
> B.3. After test-writer sub-agents complete test specification (Phase B), the CTO spawns the
> 4-model adversarial reviewer lineup in parallel (same as Phase E — see Article 03):

1. **Reviewer Gemini** -- reads test code, sends to Gemini (smartest) API with test review prompt, returns structured findings
2. **Reviewer OpenAI 5.5** -- reads test code, calls OpenAI 5.5 via Responses API (reflection pass), returns structured findings
3. **Reviewer Claude Opus 4.7** -- reads test code, CTO own review pass, returns structured findings
4. **Reviewer Grok** -- reads test code, sends to Grok (smartest) API with test review prompt, returns structured findings

ALL 4 reviewers must return before proceeding. No partial reviews.

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

Test peer review findings are saved as a section in the consolidated `reviews/slice-{N}.md` file,
with detail in `reviews/slice-{N}/test-review.md`. The consolidated file must exist before Phase C
(Implementation) can begin. See `review-templates/TEST-REVIEW-TEMPLATE.md` for the section template.
