"""Tests for NemoClaw policy presets.

Validates that agentgov-proxy.yaml follows NemoClaw preset conventions
and passes evidence-gate-action policy security checks.
"""

from __future__ import annotations

import json
import os
import sys

import pytest
import yaml

# Add evidence-gate-action src to path for imports
EGA_SRC = os.path.join(
    os.path.dirname(__file__),
    "..",
    "repos",
    "evidence-gate-action",
    "src",
)
sys.path.insert(0, os.path.abspath(EGA_SRC))

from local_evaluator import _check_policy, _parse_yaml_or_json


PRESET_DIR = os.path.join(os.path.dirname(__file__), "..", "nemoclaw-presets")


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
                    assert ep.get("tls") == "terminate", (
                        f"{name}: port 443 missing tls=terminate"
                    )

    def test_no_wildcard_methods(self, preset_data):
        for name, policy in preset_data["network_policies"].items():
            for ep in policy.get("endpoints", []):
                for rule in ep.get("rules", []):
                    allow = rule.get("allow", {})
                    assert allow.get("method") != "*", (
                        f"{name}: wildcard method rule"
                    )


class TestAgentgovPresetSecurity:
    """Run evidence-gate-action policy security audit on preset."""

    def test_policy_gate_passes(self):
        """The agentgov preset passes the nemoclaw_policy gate."""
        path = os.path.join(PRESET_DIR, "agentgov-proxy.yaml")
        with open(path) as f:
            data = yaml.safe_load(f)

        # Policy gate validates network_policies + version
        # Add version since presets don't include it
        data["version"] = 1
        issues = _check_policy(data)
        assert issues == [], f"Policy audit failed: {issues}"


class TestExampleBlueprintValidation:
    """Validate example blueprint passes blueprint gate."""

    def test_example_blueprint_passes(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "examples", "blueprint-with-agentgov.yaml"
        )
        with open(path) as f:
            data = yaml.safe_load(f)

        from local_evaluator import _check_blueprint
        issues = _check_blueprint(data)
        assert issues == [], f"Blueprint validation failed: {issues}"

    def test_example_policy_passes(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "examples", "policy-with-agentgov.yaml"
        )
        with open(path) as f:
            data = yaml.safe_load(f)

        issues = _check_policy(data)
        assert issues == [], f"Policy validation failed: {issues}"


class TestInferenceProfileValid:
    """Validate agentgov inference profile JSON."""

    def test_profile_is_valid_json(self):
        path = os.path.join(PRESET_DIR, "agentgov-inference-profile.json")
        with open(path) as f:
            data = json.load(f)
        assert data["type"] == "openai-compatible"
        assert "endpoint_url" in data
        assert "model" in data
