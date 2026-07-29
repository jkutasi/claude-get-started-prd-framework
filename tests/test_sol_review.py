from __future__ import annotations

import sys
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from sol_review import _extract_text, select_model  # noqa: E402
from workflow_config import load_config  # noqa: E402


class SolReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[1]
        self.config = load_config(self.repo_root)

    def test_extracts_raw_responses_api_text(self) -> None:
        response = {
            "output": [
                {
                    "type": "message",
                    "content": [
                        {"type": "output_text", "text": '{"verdict":"APPROVE"}'}
                    ],
                }
            ]
        }
        self.assertEqual(_extract_text(response), '{"verdict":"APPROVE"}')

    def test_refusal_is_not_treated_as_outage(self) -> None:
        response = {
            "output": [
                {
                    "type": "message",
                    "content": [{"type": "refusal", "refusal": "declined"}],
                }
            ]
        }
        with self.assertRaises(PermissionError):
            _extract_text(response)

    def test_default_model_comes_from_config(self) -> None:
        config = deepcopy(self.config)
        config["models"]["alternate_orchestrator"] = "configured-sol"
        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual(select_model(config, None), "configured-sol")

    def test_explicit_model_overrides_config(self) -> None:
        self.assertEqual(select_model(self.config, "explicit-sol"), "explicit-sol")


if __name__ == "__main__":
    unittest.main()
