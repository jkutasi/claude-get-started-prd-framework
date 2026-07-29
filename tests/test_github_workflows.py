from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from check_github_workflows import failures  # noqa: E402


class GitHubWorkflowTests(unittest.TestCase):
    def test_no_retired_claude_action_inputs(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        self.assertEqual(failures(repo_root), [])

    def test_yaml_extension_is_checked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workflow_dir = root / ".github" / "workflows"
            workflow_dir.mkdir(parents=True)
            (workflow_dir / "unsafe.yaml").write_text(
                "uses: anthropics/claude-code-action@beta\n"
                "direct_prompt: unsafe\n",
                encoding="utf-8",
            )
            problems = failures(root)
        self.assertTrue(any("unsafe.yaml" in item for item in problems))


if __name__ == "__main__":
    unittest.main()
