"""Bundled NemoClaw policy presets.

Provides access to built-in policy preset YAML files shipped with
the nemoclaw-governance package.
"""

from __future__ import annotations

import os
from typing import Any

_PRESET_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "nemoclaw-presets")

# Fallback for installed package (presets bundled as package_data)
if not os.path.isdir(_PRESET_DIR):
    _PRESET_DIR = os.path.join(os.path.dirname(__file__), "presets")


PRESETS = {
    "agentgov-proxy": "agentgov-proxy.yaml",
}


def list_presets() -> list[str]:
    """List available preset names."""
    return sorted(PRESETS.keys())


def get_preset_path(name: str) -> str:
    """Get absolute path to a preset YAML file.

    Args:
        name: Preset name (e.g., 'agentgov-proxy').

    Returns:
        Absolute file path.

    Raises:
        ValueError: If preset name is not recognized.
    """
    if name not in PRESETS:
        valid = ", ".join(sorted(PRESETS.keys()))
        raise ValueError(f"Unknown preset '{name}'. Available: {valid}")
    return os.path.abspath(os.path.join(_PRESET_DIR, PRESETS[name]))


def load_preset(name: str) -> dict[str, Any]:
    """Load and parse a preset YAML file.

    Args:
        name: Preset name (e.g., 'agentgov-proxy').

    Returns:
        Parsed YAML data as dict.

    Raises:
        ValueError: If preset not found or PyYAML not installed.
    """
    path = get_preset_path(name)
    if not os.path.isfile(path):
        raise ValueError(f"Preset file not found: {path}")

    try:
        import yaml
    except ImportError as err:
        raise ValueError(
            "YAML support requires PyYAML: pip install nemoclaw-governance[yaml]"
        ) from err

    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)
