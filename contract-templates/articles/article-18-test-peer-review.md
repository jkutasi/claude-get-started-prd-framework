# Article 18: Test Peer Review Protocol

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

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
