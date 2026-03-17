"""Tests for nemoclaw_governance.validate module.

Covers:
- Blueprint validation (valid, missing fields, invalid formats)
- Policy validation (valid, weak enforcement, missing TLS, wildcards, dangerous paths)
- File parsing (JSON, YAML, auto-detection)
- ValidationResult dataclass
"""

from __future__ import annotations

import json

import pytest

from nemoclaw_governance.validate import (
    ValidationResult,
    validate_blueprint,
    validate_file,
    validate_policy,
)

# ---------------------------------------------------------------------------
# Blueprint validation
# ---------------------------------------------------------------------------


class TestValidateBlueprint:
    """Test validate_blueprint()."""

    def test_valid_blueprint(self):
        data = {
            "version": "0.1.0",
            "profiles": {"default": {"model": "gpt-4o"}},
            "sandbox": {"image": "ghcr.io/nvidia/sandboxes/openclaw:latest"},
        }
        result = validate_blueprint(data)
        assert result.passed is True
        assert result.issues == []
        assert result.gate_type == "nemoclaw_blueprint"

    def test_missing_version(self):
        data = {
            "profiles": {"default": {"model": "test"}},
            "sandbox": {"image": "test:latest"},
        }
        result = validate_blueprint(data)
        assert result.passed is False
        assert any("BLUEPRINT_MISSING_VERSION" in i for i in result.issues)

    def test_invalid_version(self):
        data = {
            "version": "not-semver",
            "profiles": {"default": {"model": "test"}},
            "sandbox": {"image": "test:latest"},
        }
        result = validate_blueprint(data)
        assert result.passed is False
        assert any("BLUEPRINT_INVALID_VERSION" in i for i in result.issues)

    def test_missing_profiles(self):
        data = {"version": "0.1.0", "sandbox": {"image": "test:latest"}}
        result = validate_blueprint(data)
        assert result.passed is False
        assert any("BLUEPRINT_MISSING_PROFILES" in i for i in result.issues)

    def test_empty_profiles(self):
        data = {
            "version": "0.1.0",
            "profiles": {},
            "sandbox": {"image": "test:latest"},
        }
        result = validate_blueprint(data)
        assert result.passed is False
        assert any("BLUEPRINT_EMPTY_PROFILES" in i for i in result.issues)

    def test_profile_missing_model(self):
        data = {
            "version": "0.1.0",
            "profiles": {"default": {"provider_type": "nvidia"}},
            "sandbox": {"image": "test:latest"},
        }
        result = validate_blueprint(data)
        assert result.passed is False
        assert any("BLUEPRINT_PROFILE_MISSING_MODEL" in i for i in result.issues)

    def test_missing_sandbox(self):
        data = {
            "version": "0.1.0",
            "profiles": {"default": {"model": "test"}},
        }
        result = validate_blueprint(data)
        assert result.passed is False
        assert any("BLUEPRINT_MISSING_SANDBOX" in i for i in result.issues)

    def test_sandbox_missing_image(self):
        data = {
            "version": "0.1.0",
            "profiles": {"default": {"model": "test"}},
            "sandbox": {"ports": [8080]},
        }
        result = validate_blueprint(data)
        assert result.passed is False
        assert any("BLUEPRINT_MISSING_IMAGE" in i for i in result.issues)

    def test_invalid_min_version(self):
        data = {
            "version": "0.1.0",
            "min_openshell_version": "bad",
            "profiles": {"default": {"model": "test"}},
            "sandbox": {"image": "test:latest"},
        }
        result = validate_blueprint(data)
        assert result.passed is False
        assert any("BLUEPRINT_INVALID_MIN_OPENSHELL_VERSION" in i for i in result.issues)

    def test_multiple_profiles(self):
        data = {
            "version": "1.0.0",
            "profiles": {
                "default": {"model": "llama-3", "provider_type": "nvidia"},
                "agentgov": {"model": "gpt-4o", "provider_type": "openai-compatible"},
            },
            "sandbox": {"image": "test:latest"},
        }
        result = validate_blueprint(data)
        assert result.passed is True


# ---------------------------------------------------------------------------
# Policy validation
# ---------------------------------------------------------------------------


class TestValidatePolicy:
    """Test validate_policy()."""

    def test_valid_policy(self):
        data = {
            "version": 1,
            "network_policies": {
                "proxy": {
                    "endpoints": [
                        {
                            "host": "proxy.local",
                            "port": 8787,
                            "enforcement": "enforce",
                            "rules": [{"allow": {"method": "POST", "path": "/v1/**"}}],
                        }
                    ],
                },
            },
        }
        result = validate_policy(data)
        assert result.passed is True
        assert result.gate_type == "nemoclaw_policy"

    def test_missing_version(self):
        data = {"network_policies": {"test": {"endpoints": []}}}
        result = validate_policy(data)
        assert any("POLICY_MISSING_VERSION" in i for i in result.issues)

    def test_missing_network_policies(self):
        data = {"version": 1}
        result = validate_policy(data)
        assert any("POLICY_MISSING_NETWORK" in i for i in result.issues)

    def test_weak_enforcement(self):
        data = {
            "version": 1,
            "network_policies": {
                "test": {
                    "endpoints": [
                        {
                            "host": "api.example.com",
                            "port": 443,
                            "enforcement": "monitor",
                            "tls": "terminate",
                        }
                    ],
                },
            },
        }
        result = validate_policy(data)
        assert any("POLICY_WEAK_ENFORCEMENT" in i for i in result.issues)

    def test_missing_tls_on_443(self):
        data = {
            "version": 1,
            "network_policies": {
                "test": {
                    "endpoints": [
                        {
                            "host": "api.example.com",
                            "port": 443,
                            "enforcement": "enforce",
                        }
                    ],
                },
            },
        }
        result = validate_policy(data)
        assert any("POLICY_MISSING_TLS" in i for i in result.issues)

    def test_wildcard_method(self):
        data = {
            "version": 1,
            "network_policies": {
                "test": {
                    "endpoints": [
                        {
                            "host": "api.example.com",
                            "port": 443,
                            "enforcement": "enforce",
                            "tls": "terminate",
                            "rules": [{"allow": {"method": "*", "path": "/**"}}],
                        }
                    ],
                },
            },
        }
        result = validate_policy(data)
        assert any("POLICY_WILDCARD_METHOD" in i for i in result.issues)

    def test_dangerous_writable_path(self):
        data = {
            "version": 1,
            "network_policies": {"test": {"endpoints": []}},
            "filesystem_policy": {"read_write": ["/sandbox", "/etc"]},
        }
        result = validate_policy(data)
        assert any("POLICY_DANGEROUS_WRITABLE" in i for i in result.issues)

    def test_safe_writable_paths(self):
        data = {
            "version": 1,
            "network_policies": {"test": {"endpoints": []}},
            "filesystem_policy": {"read_write": ["/sandbox", "/tmp"]},
        }
        result = validate_policy(data)
        assert result.passed is True


# ---------------------------------------------------------------------------
# File auto-detection
# ---------------------------------------------------------------------------


class TestValidateFile:
    """Test validate_file() auto-detection."""

    def test_auto_detect_blueprint_json(self, tmp_path):
        path = tmp_path / "blueprint.json"
        path.write_text(
            json.dumps(
                {
                    "version": "0.1.0",
                    "profiles": {"default": {"model": "test"}},
                    "sandbox": {"image": "test:latest"},
                }
            )
        )
        result = validate_file(str(path))
        assert result.passed is True
        assert result.gate_type == "nemoclaw_blueprint"

    def test_auto_detect_policy_json(self, tmp_path):
        path = tmp_path / "policy.json"
        path.write_text(
            json.dumps(
                {
                    "version": 1,
                    "network_policies": {"test": {"endpoints": []}},
                }
            )
        )
        result = validate_file(str(path))
        assert result.passed is True
        assert result.gate_type == "nemoclaw_policy"

    def test_auto_detect_blueprint_yaml(self, tmp_path):
        path = tmp_path / "blueprint.yaml"
        path.write_text(
            "version: '0.1.0'\n"
            "profiles:\n"
            "  default:\n"
            "    model: test\n"
            "sandbox:\n"
            "  image: test:latest\n"
        )
        result = validate_file(str(path))
        assert result.passed is True
        assert result.gate_type == "nemoclaw_blueprint"

    def test_unknown_file_type_raises(self, tmp_path):
        path = tmp_path / "unknown.json"
        path.write_text('{"foo": "bar"}')
        with pytest.raises(ValueError, match="Cannot determine file type"):
            validate_file(str(path))

    def test_missing_file_raises(self):
        with pytest.raises(ValueError, match="File not found"):
            validate_file("/nonexistent/file.json")


# ---------------------------------------------------------------------------
# ValidationResult
# ---------------------------------------------------------------------------


class TestValidationResult:
    """Test ValidationResult dataclass."""

    def test_passed_result(self):
        r = ValidationResult(passed=True)
        assert r.passed is True
        assert r.issues == []
        assert r.file_path is None

    def test_failed_result_with_issues(self):
        r = ValidationResult(
            passed=False,
            issues=["ISSUE_1", "ISSUE_2"],
            file_path="test.yaml",
            gate_type="nemoclaw_blueprint",
        )
        assert r.passed is False
        assert len(r.issues) == 2
        assert r.file_path == "test.yaml"
