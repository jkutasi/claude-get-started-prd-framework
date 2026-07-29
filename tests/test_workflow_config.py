from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from workflow_config import (  # noqa: E402
    load_config,
    provider_policy_failures,
    validate_config,
)


class WorkflowConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[1]
        self.config = load_config(self.repo_root)

    def test_repository_config_is_valid(self) -> None:
        validate_config(self.config)

    def test_fable_is_blocked_when_zdr_is_required(self) -> None:
        config = copy.deepcopy(self.config)
        config["data_policy"]["requires_zero_data_retention"] = True
        failures = provider_policy_failures(config, "fable")
        self.assertTrue(any("zero-data retention" in item for item in failures))

    def test_unconfirmed_sol_zdr_is_blocked(self) -> None:
        config = copy.deepcopy(self.config)
        config["data_policy"]["requires_zero_data_retention"] = True
        failures = provider_policy_failures(config, "sol")
        self.assertTrue(any("zero-data retention" in item for item in failures))


if __name__ == "__main__":
    unittest.main()
