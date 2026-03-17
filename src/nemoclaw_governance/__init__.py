"""NemoClaw Governance Integration.

Validate NemoClaw blueprints and policies, apply agentgov proxy presets.

Usage:
    from nemoclaw_governance import validate_blueprint, validate_policy

CLI:
    nemoclaw-gov validate blueprint.yaml
    nemoclaw-gov validate policy.yaml
    nemoclaw-gov presets list
    nemoclaw-gov presets show agentgov-proxy
"""

from __future__ import annotations

__version__ = "0.1.0"

from nemoclaw_governance.validate import (
    ValidationResult,
    validate_blueprint,
    validate_file,
    validate_policy,
)

__all__ = [
    "validate_blueprint",
    "validate_policy",
    "validate_file",
    "ValidationResult",
    "__version__",
]
