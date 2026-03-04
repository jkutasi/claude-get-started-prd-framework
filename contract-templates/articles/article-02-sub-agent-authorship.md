# Article 2: Sub-Agent Code Authorship

> Part of the [Contract Articles](INDEX.md). Load only when you need this specific article.

ALL code is written by Sonnet coder agents (teammates or their spawned sub-agents). Each agent gets ONE focused job (one function, one component, one review). Never a whole module in one agent. Keep tasks small and focused -- this preserves context quality and enables thorough review.

**Test-writer sub-agents are DISTINCT from implementation coders.** Test code (Phase B) is written by test-writer sub-agents spawned by the QA Lead. Implementation code (Phase C) is written by implementation coder sub-agents spawned by Engineers. The same agent MUST NOT write both the tests and the implementation for the same slice. This creates genuine independence -- test-writers design tests without knowing how the code will be implemented, and implementation coders write code to pass tests they did not design.
