"""Load and validate the lean workflow configuration."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any


class ConfigError(ValueError):
    """Raised when workflow configuration is missing or invalid."""


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigError(f"configuration not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ConfigError(f"configuration root must be an object: {path}")
    return value


def load_config(repo_root: Path, config_path: Path | None = None) -> dict[str, Any]:
    """Load base config and optional gitignored local overrides."""
    base_path = config_path or repo_root / "workflow.config.json"
    config = _read_json(base_path)
    local_path = repo_root / "workflow.config.local.json"
    if local_path.is_file() and local_path.resolve() != base_path.resolve():
        config = _deep_merge(config, _read_json(local_path))
    validate_config(config)
    return config


def validate_config(config: dict[str, Any]) -> None:
    """Validate fields required by the gate."""
    if config.get("version") != 1:
        raise ConfigError("workflow configuration version must be 1")

    required_models = {
        "default_orchestrator",
        "alternate_orchestrator",
        "implementation_worker",
        "mechanical_worker",
    }
    models = config.get("models")
    if not isinstance(models, dict) or not required_models.issubset(models):
        raise ConfigError("models must define both orchestrators and both workers")

    checks = config.get("checks")
    if not isinstance(checks, dict):
        raise ConfigError("checks must be an object")
    for name in ("normal", "high_risk"):
        commands = checks.get(name)
        if not isinstance(commands, list) or not all(
            isinstance(command, str) and command.strip() for command in commands
        ):
            raise ConfigError(f"checks.{name} must be a list of non-empty commands")
    if not checks["normal"]:
        raise ConfigError("checks.normal must contain at least one command")

    risk = config.get("risk")
    if not isinstance(risk, dict):
        raise ConfigError("risk must be an object")
    if not isinstance(risk.get("path_patterns"), list):
        raise ConfigError("risk.path_patterns must be a list")
    if not isinstance(risk.get("diff_patterns"), list):
        raise ConfigError("risk.diff_patterns must be a list")
    try:
        for pattern in risk["path_patterns"]:
            re.compile(pattern)
        for item in risk["diff_patterns"]:
            re.compile(item["pattern"])
    except (re.error, KeyError, TypeError) as exc:
        raise ConfigError(f"invalid risk pattern: {exc}") from exc

    data_policy = config.get("data_policy")
    if not isinstance(data_policy, dict) or not isinstance(
        data_policy.get("providers"), dict
    ):
        raise ConfigError("data_policy.providers must be an object")

    records = config.get("records")
    required_records = {
        "high_risk_dir",
        "downgrade_dir",
        "ownership_file",
        "handoff_file",
        "metrics_file",
    }
    if not isinstance(records, dict) or not required_records.issubset(records):
        raise ConfigError("records is missing required paths")


def orchestrator_model(config: dict[str, Any], orchestrator: str) -> str:
    if orchestrator == "fable":
        return str(config["models"]["default_orchestrator"])
    if orchestrator == "sol":
        return str(config["models"]["alternate_orchestrator"])
    raise ConfigError(f"unsupported orchestrator: {orchestrator}")


def orchestrator_provider(orchestrator: str) -> str:
    return {"fable": "anthropic", "sol": "openai"}[orchestrator]


def provider_policy_failures(
    config: dict[str, Any], orchestrator: str
) -> list[str]:
    """Return privacy/provider failures for the chosen orchestrator."""
    provider = orchestrator_provider(orchestrator)
    policy = config["data_policy"]["providers"].get(provider)
    if not isinstance(policy, dict):
        return [f"data policy is missing provider: {provider}"]
    failures: list[str] = []
    if policy.get("allowed") is not True:
        failures.append(f"provider is not approved: {provider}")
    if config["data_policy"].get("requires_zero_data_retention"):
        if policy.get("supports_zero_data_retention") is not True:
            failures.append(
                f"{provider} is not confirmed for required zero-data retention"
            )
    return failures
