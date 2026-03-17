"""Tests for nemoclaw_governance.cli module."""

from __future__ import annotations

import os

import pytest

from nemoclaw_governance.cli import main

EXAMPLE_DIR = os.path.join(os.path.dirname(__file__), "..", "examples")


class TestCLIValidate:
    """Test CLI validate command."""

    def test_validate_valid_blueprint(self):
        path = os.path.join(EXAMPLE_DIR, "blueprint-with-agentgov.yaml")
        with pytest.raises(SystemExit) as exc_info:
            main(["validate", path])
        assert exc_info.value.code == 0

    def test_validate_valid_policy(self):
        path = os.path.join(EXAMPLE_DIR, "policy-with-agentgov.yaml")
        with pytest.raises(SystemExit) as exc_info:
            main(["validate", path])
        assert exc_info.value.code == 0

    def test_validate_invalid_file(self, tmp_path):
        bad = tmp_path / "bad.json"
        bad.write_text('{"version": "not-semver", "profiles": {"x": {}}, "sandbox": {}}')
        with pytest.raises(SystemExit) as exc_info:
            main(["validate", str(bad)])
        assert exc_info.value.code == 1

    def test_validate_multiple_files(self):
        bp = os.path.join(EXAMPLE_DIR, "blueprint-with-agentgov.yaml")
        pol = os.path.join(EXAMPLE_DIR, "policy-with-agentgov.yaml")
        with pytest.raises(SystemExit) as exc_info:
            main(["validate", bp, pol])
        assert exc_info.value.code == 0

    def test_validate_no_files(self):
        with pytest.raises(SystemExit) as exc_info:
            main(["validate"])
        assert exc_info.value.code == 1

    def test_validate_all_examples(self):
        with pytest.raises(SystemExit) as exc_info:
            main(["validate", "--all", EXAMPLE_DIR])
        # Should pass since all example YAML files are valid
        assert exc_info.value.code == 0


class TestCLIPresets:
    """Test CLI presets command."""

    def test_presets_list(self):
        with pytest.raises(SystemExit) as exc_info:
            main(["presets", "list"])
        assert exc_info.value.code == 0

    def test_presets_path(self):
        with pytest.raises(SystemExit) as exc_info:
            main(["presets", "path", "agentgov-proxy"])
        assert exc_info.value.code == 0

    def test_presets_show(self):
        with pytest.raises(SystemExit) as exc_info:
            main(["presets", "show", "agentgov-proxy"])
        assert exc_info.value.code == 0

    def test_presets_unknown(self):
        with pytest.raises(SystemExit) as exc_info:
            main(["presets", "path", "nonexistent"])
        assert exc_info.value.code == 1


class TestCLIVersion:
    """Test CLI version command."""

    def test_version(self):
        with pytest.raises(SystemExit) as exc_info:
            main(["version"])
        assert exc_info.value.code == 0
