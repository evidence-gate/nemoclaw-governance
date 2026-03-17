"""Tests for nemoclaw_governance.presets module."""

from __future__ import annotations

import os

import pytest

from nemoclaw_governance.presets import get_preset_path, list_presets, load_preset


class TestListPresets:
    """Test list_presets()."""

    def test_returns_list(self):
        result = list_presets()
        assert isinstance(result, list)
        assert len(result) >= 1

    def test_includes_agentgov_proxy(self):
        result = list_presets()
        assert "agentgov-proxy" in result


class TestGetPresetPath:
    """Test get_preset_path()."""

    def test_valid_preset_returns_path(self):
        path = get_preset_path("agentgov-proxy")
        assert path.endswith("agentgov-proxy.yaml")
        assert os.path.isabs(path)

    def test_preset_file_exists(self):
        path = get_preset_path("agentgov-proxy")
        assert os.path.isfile(path)

    def test_unknown_preset_raises(self):
        with pytest.raises(ValueError, match="Unknown preset"):
            get_preset_path("nonexistent")


class TestLoadPreset:
    """Test load_preset()."""

    def test_loads_agentgov_proxy(self):
        data = load_preset("agentgov-proxy")
        assert isinstance(data, dict)
        assert "preset" in data
        assert "network_policies" in data

    def test_unknown_preset_raises(self):
        with pytest.raises(ValueError, match="Unknown preset"):
            load_preset("nonexistent")
