from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from gate_check import (  # noqa: E402
    budget_failures,
    handoff_failures,
    ownership_failures,
    validate_downgrade,
    validate_high_risk_record,
)
from workflow_config import load_config  # noqa: E402


class GateCheckTests(unittest.TestCase):
    DIFF_SHA = "a" * 64

    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[1]
        self.config = load_config(self.repo_root)
        self.valid_record = {
            "change_id": "change-1",
            "risk_level": "high",
            "orchestrator_model": "claude-fable-5",
            "author_model": "claude-sonnet-5",
            "reviewer_model": "gpt-5.6-sol",
            "plan_review": {
                "verdict": "APPROVE",
                "requirements_source": "Raw user requirements",
            },
            "verification": {"status": "PASS"},
            "rollback": {"method": "revert", "evidence": "reverse patch checked"},
            "diff_review": {
                "verdict": "APPROVE",
                "scope": "Raw diff",
                "diff_sha256": self.DIFF_SHA,
            },
            "review_counts": {"plan": 1, "diff": 1, "scoped_followups": 0},
        }

    def _write_json(self, root: Path, name: str, value: dict) -> Path:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def test_valid_high_risk_record(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = self._write_json(Path(temp), "record.json", self.valid_record)
            self.assertEqual(
                validate_high_risk_record(
                    path,
                    "change-1",
                    self.config,
                    self.DIFF_SHA,
                ),
                [],
            )

    def test_author_cannot_review_own_work(self) -> None:
        record = copy.deepcopy(self.valid_record)
        record["author_model"] = "gpt-5.6-sol"
        with tempfile.TemporaryDirectory() as temp:
            path = self._write_json(Path(temp), "record.json", record)
            failures = validate_high_risk_record(
                path,
                "change-1",
                self.config,
                self.DIFF_SHA,
            )
        self.assertTrue(any("must not be the author" in item for item in failures))

    def test_author_model_cannot_be_blank(self) -> None:
        record = copy.deepcopy(self.valid_record)
        record["author_model"] = "   "
        with tempfile.TemporaryDirectory() as temp:
            path = self._write_json(Path(temp), "record.json", record)
            failures = validate_high_risk_record(
                path,
                "change-1",
                self.config,
                self.DIFF_SHA,
            )
        self.assertTrue(any("author_model is required" in item for item in failures))
        self.assertFalse(any("must not be the author" in item for item in failures))

    def test_stale_diff_review_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = self._write_json(Path(temp), "record.json", self.valid_record)
            failures = validate_high_risk_record(
                path,
                "change-1",
                self.config,
                "b" * 64,
            )
        self.assertTrue(any("current diff" in item for item in failures))

    def test_approved_review_count_cannot_be_zero(self) -> None:
        record = copy.deepcopy(self.valid_record)
        record["review_counts"]["diff"] = 0
        with tempfile.TemporaryDirectory() as temp:
            path = self._write_json(Path(temp), "record.json", record)
            failures = validate_high_risk_record(
                path,
                "change-1",
                self.config,
                self.DIFF_SHA,
            )
        self.assertTrue(any("must be at least 1" in item for item in failures))

    def test_user_downgrade_requires_rationale(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = self._write_json(
                Path(temp),
                "downgrade.json",
                {"approved_by": "user", "rationale": ""},
            )
            failures = validate_downgrade(path)
        self.assertTrue(any("rationale" in item for item in failures))

    def test_user_downgrade_change_id_must_match(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = self._write_json(
                Path(temp),
                "downgrade.json",
                {
                    "change_id": "wrong",
                    "approved_by": "user",
                    "rationale": "explicit decision",
                },
            )
            failures = validate_downgrade(path, "change-1")
        self.assertTrue(any("change_id" in item for item in failures))

    def test_overlapping_ownership_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            config = copy.deepcopy(self.config)
            config["records"]["ownership_file"] = "ownership.json"
            self._write_json(
                root,
                "ownership.json",
                {
                    "tasks": [
                        {"id": "a", "status": "active", "paths": ["src/auth"]},
                        {
                            "id": "b",
                            "status": "active",
                            "paths": ["src/auth/session.py"],
                        },
                    ]
                },
            )
            failures = ownership_failures(root, config)
        self.assertTrue(any("overlapping ownership" in item for item in failures))

    def test_ownership_overlap_is_case_insensitive(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            config = copy.deepcopy(self.config)
            config["records"]["ownership_file"] = "ownership.json"
            self._write_json(
                root,
                "ownership.json",
                {
                    "tasks": [
                        {"id": "a", "status": "active", "paths": ["src/Auth"]},
                        {
                            "id": "b",
                            "status": "active",
                            "paths": ["src/auth/session.py"],
                        },
                    ]
                },
            )
            failures = ownership_failures(root, config)
        self.assertTrue(any("overlapping ownership" in item for item in failures))

    def test_worker_attempt_limit_is_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            config = copy.deepcopy(self.config)
            config["records"]["ownership_file"] = "ownership.json"
            self._write_json(
                root,
                "ownership.json",
                {
                    "tasks": [
                        {
                            "id": "a",
                            "status": "active",
                            "attempts": config["limits"]["worker_attempts"] + 1,
                            "paths": ["src/auth"],
                        }
                    ]
                },
            )
            failures = ownership_failures(root, config)
        self.assertTrue(any("worker attempts exceeded" in item for item in failures))

    def test_handoff_requires_reconciliation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            config = copy.deepcopy(self.config)
            config["records"]["handoff_file"] = "handoff.json"
            self._write_json(
                root,
                "handoff.json",
                {
                    "task_id": "change-1",
                    "from_orchestrator": "claude-fable-5",
                    "to_orchestrator": "gpt-5.6-sol",
                    "reason": "provider outage",
                    "goal": "finish verification",
                    "repository_reconciled": False,
                    "reconciliation_commands": [],
                },
            )
            failures = handoff_failures(root, config, "gpt-5.6-sol")
        self.assertTrue(any("repository_reconciled" in item for item in failures))

    def test_configured_budget_requires_usage(self) -> None:
        config = copy.deepcopy(self.config)
        config["limits"]["max_total_tokens"] = 1000
        failures = budget_failures(config, None, None)
        self.assertTrue(any("tokens-used is required" in item for item in failures))

    def test_oversized_file_fails_cleanly_and_records_metrics(self) -> None:
        oversized = self.repo_root / f"gate-oversized-{uuid.uuid4().hex}.bin"
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            metrics = temp_root / "metrics.jsonl"
            config = copy.deepcopy(self.config)
            config["checks"] = {
                "normal": [
                    f'"{sys.executable}" -c "print(\'normal sentinel\')"'
                ],
                "high_risk": [
                    f'"{sys.executable}" -c "print(\'high sentinel\')"'
                ],
            }
            config["records"]["metrics_file"] = str(metrics)
            config_path = self._write_json(temp_root, "config.json", config)
            try:
                oversized.write_bytes(b"x" * 1_000_001)
                result = subprocess.run(
                    [
                        sys.executable,
                        str(SCRIPTS / "gate_check.py"),
                        "--change-id",
                        "oversized-test",
                        "--orchestrator",
                        "sol",
                        "--config",
                        str(config_path),
                    ],
                    cwd=self.repo_root,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                )
            finally:
                oversized.unlink(missing_ok=True)
            event = json.loads(metrics.read_text(encoding="utf-8").splitlines()[-1])

        self.assertEqual(result.returncode, 1)
        self.assertIn("classification incomplete", result.stdout)
        self.assertIn("PASS:", result.stdout)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(event["risk_level"], "high")
        self.assertFalse(event["passed"])


if __name__ == "__main__":
    unittest.main()
