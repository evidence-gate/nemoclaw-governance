"""Blueprint and policy validation for NemoClaw configurations.

Validates NemoClaw blueprint.yaml and OpenShell openclaw-sandbox.yaml
files against security and structural requirements.

Uses only stdlib + PyYAML. No other dependencies.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Any

_SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+")


@dataclass
class ValidationResult:
    """Result of a blueprint or policy validation.

    Attributes:
        passed: True if no issues were found.
        issues: List of issue strings with structured codes.
        file_path: Path to the validated file (if applicable).
        gate_type: The gate type used for validation.
    """

    passed: bool
    issues: list[str] = field(default_factory=list)
    file_path: str | None = None
    gate_type: str | None = None


def _load_file(path: str) -> dict[str, Any]:
    """Load a YAML or JSON file.

    Raises:
        ValueError: If the file cannot be parsed or is not a mapping.
    """
    abs_path = os.path.abspath(path)
    if not os.path.isfile(abs_path):
        raise ValueError(f"File not found: {abs_path}")

    with open(abs_path, encoding="utf-8") as f:
        content = f.read()

    if abs_path.endswith((".yaml", ".yml")):
        try:
            import yaml
        except ImportError as err:
            raise ValueError(
                "YAML files require PyYAML: pip install nemoclaw-governance[yaml]"
            ) from err
        data = yaml.safe_load(content)
    else:
        try:
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"Root must be a mapping, got {type(data).__name__}")
    return data


def validate_blueprint(data: dict[str, Any]) -> ValidationResult:
    """Validate NemoClaw blueprint structure.

    Checks:
    - version: required, semver format
    - profiles: required, at least one entry, each with 'model' field
    - sandbox: required, must have 'image' field
    - min_openshell_version / min_openclaw_version: if present, must be semver

    Args:
        data: Parsed blueprint data (dict).

    Returns:
        ValidationResult with issues list.
    """
    issues: list[str] = []

    # version
    version = data.get("version")
    if not version:
        issues.append("BLUEPRINT_MISSING_VERSION: 'version' field is required")
    elif not isinstance(version, str) or not _SEMVER_RE.match(version):
        issues.append(f"BLUEPRINT_INVALID_VERSION: version '{version}' is not valid semver")

    # profiles
    profiles = data.get("profiles")
    if profiles is None:
        issues.append("BLUEPRINT_MISSING_PROFILES: 'profiles' section is required")
    elif not isinstance(profiles, dict):
        issues.append("BLUEPRINT_INVALID_PROFILES: 'profiles' must be a mapping")
    elif len(profiles) == 0:
        issues.append("BLUEPRINT_EMPTY_PROFILES: at least one profile is required")
    else:
        for name, profile in profiles.items():
            if not isinstance(profile, dict):
                issues.append(f"BLUEPRINT_INVALID_PROFILE: profile '{name}' must be a mapping")
                continue
            if "model" not in profile:
                issues.append(f"BLUEPRINT_PROFILE_MISSING_MODEL: profile '{name}' missing 'model'")

    # sandbox
    sandbox = data.get("sandbox")
    if not sandbox:
        issues.append("BLUEPRINT_MISSING_SANDBOX: 'sandbox' section is required")
    elif not isinstance(sandbox, dict):
        issues.append("BLUEPRINT_INVALID_SANDBOX: 'sandbox' must be a mapping")
    elif "image" not in sandbox:
        issues.append("BLUEPRINT_MISSING_IMAGE: 'sandbox.image' is required")

    # optional version constraints
    for field_name in ("min_openshell_version", "min_openclaw_version"):
        val = data.get(field_name)
        if val is not None and (not isinstance(val, str) or not _SEMVER_RE.match(val)):
            issues.append(f"BLUEPRINT_INVALID_{field_name.upper()}: '{val}' is not valid semver")

    return ValidationResult(
        passed=len(issues) == 0,
        issues=issues,
        gate_type="nemoclaw_blueprint",
    )


def validate_policy(data: dict[str, Any]) -> ValidationResult:
    """Validate NemoClaw OpenShell policy security posture.

    Checks:
    - version: required
    - network_policies: required, properly structured
    - All endpoints: enforcement=enforce
    - Port 443 endpoints: tls=terminate
    - No wildcard HTTP method rules
    - No dangerous writable filesystem paths

    Args:
        data: Parsed policy data (dict).

    Returns:
        ValidationResult with issues list.
    """
    issues: list[str] = []

    if "version" not in data:
        issues.append("POLICY_MISSING_VERSION: 'version' field is required")

    policies = data.get("network_policies")
    if not policies:
        issues.append("POLICY_MISSING_NETWORK: 'network_policies' section is required")
    elif not isinstance(policies, dict):
        issues.append("POLICY_INVALID_NETWORK: 'network_policies' must be a mapping")
    else:
        for policy_name, policy in policies.items():
            if not isinstance(policy, dict):
                issues.append(f"POLICY_INVALID_ENTRY: '{policy_name}' must be a mapping")
                continue
            endpoints = policy.get("endpoints", [])
            if not isinstance(endpoints, list):
                issues.append(f"POLICY_INVALID_ENDPOINTS: '{policy_name}.endpoints' must be a list")
                continue

            for i, ep in enumerate(endpoints):
                if not isinstance(ep, dict):
                    continue
                ep_id = f"{policy_name}.endpoints[{i}] ({ep.get('host', '?')})"

                enforcement = ep.get("enforcement")
                if enforcement and enforcement != "enforce":
                    issues.append(
                        f"POLICY_WEAK_ENFORCEMENT: {ep_id} has "
                        f"enforcement='{enforcement}', expected 'enforce'"
                    )

                port = ep.get("port")
                tls = ep.get("tls")
                if port == 443 and tls != "terminate":
                    issues.append(
                        f"POLICY_MISSING_TLS: {ep_id} on port 443 should have tls='terminate'"
                    )

                rules = ep.get("rules", [])
                if isinstance(rules, list):
                    for rule in rules:
                        if isinstance(rule, dict):
                            allow = rule.get("allow", {})
                            if isinstance(allow, dict) and allow.get("method") == "*":
                                issues.append(
                                    f"POLICY_WILDCARD_METHOD: {ep_id} "
                                    f"has wildcard method rule (method='*')"
                                )

    # filesystem safety
    fs_policy = data.get("filesystem_policy")
    if isinstance(fs_policy, dict):
        dangerous = {"/usr", "/etc", "/lib", "/bin", "/sbin", "/var", "/root"}
        rw_paths = fs_policy.get("read_write", [])
        if isinstance(rw_paths, list):
            for rw_path in rw_paths:
                if isinstance(rw_path, str):
                    for d in dangerous:
                        if rw_path == d or rw_path.startswith(d + "/"):
                            issues.append(
                                f"POLICY_DANGEROUS_WRITABLE: filesystem allows write to '{rw_path}'"
                            )

    return ValidationResult(
        passed=len(issues) == 0,
        issues=issues,
        gate_type="nemoclaw_policy",
    )


def validate_file(path: str) -> ValidationResult:
    """Auto-detect file type and validate.

    Determines whether a file is a blueprint or policy based on content,
    then runs the appropriate validator.

    Args:
        path: Path to YAML or JSON file.

    Returns:
        ValidationResult.

    Raises:
        ValueError: If the file cannot be loaded or type cannot be determined.
    """
    data = _load_file(path)

    # Auto-detect: blueprints have 'profiles' and 'sandbox',
    # policies have 'network_policies'
    if "profiles" in data or "sandbox" in data:
        result = validate_blueprint(data)
    elif "network_policies" in data:
        result = validate_policy(data)
    elif "preset" in data:
        # Policy preset file -- validate as policy
        result = validate_policy(data)
    else:
        raise ValueError(
            f"Cannot determine file type for '{path}'. "
            "Expected 'profiles'/'sandbox' (blueprint) or "
            "'network_policies' (policy)."
        )

    result.file_path = path
    return result
