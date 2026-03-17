"""Tests for NemoClaw policy presets.

Validates that agentgov-proxy.yaml follows NemoClaw preset conventions
and passes security checks.
"""

from __future__ import annotations

import json
import os

import pytest
import yaml

from nemoclaw_governance.validate import validate_blueprint, validate_file, validate_policy

PRESET_DIR = os.path.join(os.path.dirname(__file__), "..", "nemoclaw-presets")
EXAMPLE_DIR = os.path.join(os.path.dirname(__file__), "..", "examples")


class TestAgentgovPresetStructure:
    """Validate agentgov-proxy.yaml preset structure."""

    @pytest.fixture()
    def preset_data(self):
        path = os.path.join(PRESET_DIR, "agentgov-proxy.yaml")
        with open(path) as f:
            return yaml.safe_load(f)

    def test_has_preset_section(self, preset_data):
        assert "preset" in preset_data
        assert preset_data["preset"]["name"] == "agentgov-proxy"
        assert "description" in preset_data["preset"]

    def test_has_network_policies(self, preset_data):
        assert "network_policies" in preset_data
        policies = preset_data["network_policies"]
        assert len(policies) >= 1

    def test_endpoints_have_enforcement(self, preset_data):
        for name, policy in preset_data["network_policies"].items():
            for ep in policy.get("endpoints", []):
                assert "enforcement" in ep, f"{name}: endpoint missing enforcement"
                assert ep["enforcement"] == "enforce", f"{name}: not enforced"

    def test_endpoints_have_rules(self, preset_data):
        for name, policy in preset_data["network_policies"].items():
            for ep in policy.get("endpoints", []):
                assert "rules" in ep, f"{name}: endpoint missing rules"
                assert len(ep["rules"]) > 0, f"{name}: endpoint has no rules"

    def test_tls_endpoints_have_terminate(self, preset_data):
        for name, policy in preset_data["network_policies"].items():
            for ep in policy.get("endpoints", []):
                if ep.get("port") == 443:
                    assert ep.get("tls") == "terminate", f"{name}: port 443 missing tls=terminate"

    def test_no_wildcard_methods(self, preset_data):
        for name, policy in preset_data["network_policies"].items():
            for ep in policy.get("endpoints", []):
                for rule in ep.get("rules", []):
                    allow = rule.get("allow", {})
                    assert allow.get("method") != "*", f"{name}: wildcard method rule"


class TestAgentgovPresetSecurity:
    """Run policy security audit on preset."""

    def test_policy_gate_passes(self):
        """The agentgov preset passes the nemoclaw_policy gate."""
        path = os.path.join(PRESET_DIR, "agentgov-proxy.yaml")
        with open(path) as f:
            data = yaml.safe_load(f)
        data["version"] = 1
        result = validate_policy(data)
        assert result.passed, f"Policy audit failed: {result.issues}"


class TestExampleValidation:
    """Validate example files pass their respective gates."""

    def test_example_blueprint_passes(self):
        path = os.path.join(EXAMPLE_DIR, "blueprint-with-agentgov.yaml")
        with open(path) as f:
            data = yaml.safe_load(f)
        result = validate_blueprint(data)
        assert result.passed, f"Blueprint validation failed: {result.issues}"

    def test_example_policy_passes(self):
        path = os.path.join(EXAMPLE_DIR, "policy-with-agentgov.yaml")
        with open(path) as f:
            data = yaml.safe_load(f)
        result = validate_policy(data)
        assert result.passed, f"Policy validation failed: {result.issues}"

    def test_validate_file_auto_detects_blueprint(self):
        path = os.path.join(EXAMPLE_DIR, "blueprint-with-agentgov.yaml")
        result = validate_file(path)
        assert result.passed
        assert result.gate_type == "nemoclaw_blueprint"

    def test_validate_file_auto_detects_policy(self):
        path = os.path.join(EXAMPLE_DIR, "policy-with-agentgov.yaml")
        result = validate_file(path)
        assert result.passed
        assert result.gate_type == "nemoclaw_policy"


class TestInferenceProfileValid:
    """Validate agentgov inference profile JSON."""

    def test_profile_is_valid_json(self):
        path = os.path.join(PRESET_DIR, "agentgov-inference-profile.json")
        with open(path) as f:
            data = json.load(f)
        assert data["type"] == "openai-compatible"
        assert "endpoint_url" in data
        assert "model" in data
