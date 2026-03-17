**English** | [日本語](README.ja.md)

# NemoClaw Governance Integration

Three-layer governance for AI agents: infrastructure isolation (NemoClaw) + cost control (agentgov) + CI quality gates (evidence-gate-action).

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![CI](https://github.com/evidence-gate/nemoclaw-governance/actions/workflows/ci.yml/badge.svg)](https://github.com/evidence-gate/nemoclaw-governance/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## The Problem

NVIDIA NemoClaw provides sandboxed execution for AI agents with network, filesystem, and process isolation. But it has **no cost controls** -- a sandboxed agent can still burn through hundreds of dollars in inference costs with no way to stop it.

This project bridges the gap:

- **agentgov** sits between the sandbox and the LLM provider, enforcing per-agent budgets with hold/settle cost control
- **evidence-gate-action** validates NemoClaw blueprints and policies in CI before deployment
- **nemoclaw-governance** ties them together with presets, CLI tools, and examples

## Quick Start

### Install

```bash
pip install nemoclaw-governance[yaml]
```

This installs the `nemoclaw-gov` CLI and the Python validation library.

### Validate Your NemoClaw Configs

```bash
# Validate a blueprint
nemoclaw-gov validate blueprint.yaml

# Validate a policy
nemoclaw-gov validate openclaw-sandbox.yaml

# Validate all configs in a directory
nemoclaw-gov validate --all nemoclaw/
```

### Use as a Python Library

```python
from nemoclaw_governance import validate_blueprint, validate_policy, validate_file

# Auto-detect file type and validate
result = validate_file("blueprint.yaml")
print(result.passed)    # True/False
print(result.issues)    # List of issues (empty if passed)
print(result.gate_type) # "nemoclaw_blueprint" or "nemoclaw_policy"

# Validate parsed data directly
import yaml
with open("blueprint.yaml") as f:
    data = yaml.safe_load(f)
result = validate_blueprint(data)
```

### Add agentgov to NemoClaw

```bash
# 1. Start agentgov proxy
cd /path/to/agentgov
docker compose -f docker/compose.yml up -d

# 2. Register agentgov as inference provider + apply network policy
./scripts/setup-agentgov-provider.sh

# Or step by step:
openshell provider create --name agentgov --type openai-compatible \
  --endpoint-url http://localhost:8787/v1 --model gpt-4o
nemoclaw policy-add nemoclaw-presets/agentgov-proxy.yaml
openshell inference set --provider agentgov --model gpt-4o
```

### Add CI Gates

```yaml
# .github/workflows/nemoclaw-gate.yml
- name: Validate NemoClaw Blueprint
  uses: evidence-gate/evidence-gate-action@v1
  with:
    gate_type: nemoclaw_blueprint
    phase_id: deploy
    evidence_files: /tmp/blueprint.json

- name: Validate NemoClaw Policy
  uses: evidence-gate/evidence-gate-action@v1
  with:
    gate_type: nemoclaw_policy
    phase_id: deploy
    evidence_files: /tmp/policy.json
```

## Architecture

```
┌─────────────────────────────────────────────────┐
│  CI/CD Layer (evidence-gate-action)              │
│  Validates before deploy:                        │
│  - Blueprint structure (nemoclaw_blueprint gate) │
│  - Policy security (nemoclaw_policy gate)        │
│  - nemoclaw-baseline preset for full validation  │
└─────────┬───────────────────────────────────────┘
          │ deploy
          ▼
┌─────────────────────────────────────────────────┐
│  Infrastructure Layer (NemoClaw / OpenShell)     │
│  Enforces at runtime:                            │
│  - Filesystem isolation (Landlock LSM)           │
│  - Network: deny-by-default, agentgov-only      │
│  - Process sandboxing (no privilege escalation)  │
└─────────┬───────────────────────────────────────┘
          │ inference requests → agentgov proxy
          ▼
┌─────────────────────────────────────────────────┐
│  Application Layer (agentgov proxy)              │
│  Enforces per-request:                           │
│  - Budget gate (Hold/Settle pattern)             │
│  - HITL approval (Slack/webhook)                 │
│  - Audit log (SHA-256 hash chain)                │
└─────────┬───────────────────────────────────────┘
          │ governed LLM call
          ▼
┌─────────────────────────────────────────────────┐
│  LLM Provider (OpenAI / Anthropic / Gemini)      │
└─────────────────────────────────────────────────┘
```

This follows the enterprise standard established by Cisco + NVIDIA OpenShell: infrastructure isolation (Layer 1) + application governance (Layer 2) + CI validation (Layer 3).

## What's Included

### Python Package (`pip install nemoclaw-governance[yaml]`)

| Feature | Description |
|---------|-------------|
| `validate_blueprint()` | Validate NemoClaw blueprint.yaml structure |
| `validate_policy()` | Security audit of OpenShell policy YAML |
| `validate_file()` | Auto-detect file type and validate |
| `nemoclaw-gov` CLI | Command-line validation and preset management |

### Gate Types for evidence-gate-action

| Gate Type | What It Validates |
|-----------|-------------------|
| `nemoclaw_blueprint` | version (semver), profiles (model required), sandbox (image), version constraints |
| `nemoclaw_policy` | enforcement=enforce, TLS on port 443, no wildcard methods, no dangerous writable paths |
| `nemoclaw-baseline` preset | All of the above + `security` + `build` |

### Policy Presets for NemoClaw

| File | Purpose |
|------|---------|
| `agentgov-proxy.yaml` | Network policy allowing sandbox egress only to agentgov proxy |
| `agentgov-inference-profile.json` | Provider config for `openshell provider create` |

## CLI Reference

### `nemoclaw-gov validate`

Validate one or more NemoClaw configuration files:

```bash
# Single file
nemoclaw-gov validate blueprint.yaml

# Multiple files
nemoclaw-gov validate blueprint.yaml policy.yaml

# Scan directory
nemoclaw-gov validate --all configs/
```

Output:

```
NemoClaw Governance Validation (2 file(s))
==================================================
  [PASS] blueprint.yaml (nemoclaw_blueprint)
  [FAIL] policy.yaml (nemoclaw_policy)
    - POLICY_WEAK_ENFORCEMENT: test.endpoints[0] has enforcement='monitor', expected 'enforce'
    - POLICY_MISSING_TLS: test.endpoints[0] on port 443 should have tls='terminate'

1/2 file(s) failed with 2 issue(s).
```

Exit code: `0` if all passed, `1` if any failed.

### `nemoclaw-gov presets`

Manage bundled policy presets:

```bash
# List available presets
nemoclaw-gov presets list

# Show preset contents
nemoclaw-gov presets show agentgov-proxy

# Get file path (for copying or applying)
nemoclaw-gov presets path agentgov-proxy
```

### `nemoclaw-gov version`

```bash
nemoclaw-gov version
# nemoclaw-governance 0.1.0
```

## Validation Details

### nemoclaw_blueprint

Validates NemoClaw `blueprint.yaml` structure:

| Check | Issue Code | Description |
|-------|-----------|-------------|
| Version exists | `BLUEPRINT_MISSING_VERSION` | `version` field is required |
| Version format | `BLUEPRINT_INVALID_VERSION` | Must be valid semver (X.Y.Z) |
| Profiles exist | `BLUEPRINT_MISSING_PROFILES` | `profiles` section is required |
| Profiles non-empty | `BLUEPRINT_EMPTY_PROFILES` | At least one profile required |
| Profile model | `BLUEPRINT_PROFILE_MISSING_MODEL` | Each profile needs `model` field |
| Sandbox exists | `BLUEPRINT_MISSING_SANDBOX` | `sandbox` section is required |
| Sandbox image | `BLUEPRINT_MISSING_IMAGE` | `sandbox.image` is required |
| Version constraints | `BLUEPRINT_INVALID_MIN_*` | Optional min versions must be semver |

### nemoclaw_policy

Security audit of NemoClaw `openclaw-sandbox.yaml`:

| Check | Issue Code | Description |
|-------|-----------|-------------|
| Version exists | `POLICY_MISSING_VERSION` | `version` field is required |
| Network policies | `POLICY_MISSING_NETWORK` | `network_policies` section required |
| Enforcement mode | `POLICY_WEAK_ENFORCEMENT` | All endpoints must use `enforcement: enforce` |
| TLS on 443 | `POLICY_MISSING_TLS` | Port 443 endpoints must have `tls: terminate` |
| No wildcards | `POLICY_WILDCARD_METHOD` | No `method: "*"` rules allowed |
| Safe filesystem | `POLICY_DANGEROUS_WRITABLE` | No write access to `/usr`, `/etc`, `/lib`, etc. |

## Workflow Recipes

### Recipe 1: Validate on Pull Request

```yaml
name: NemoClaw Governance Gate
on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install validator
        run: pip install nemoclaw-governance[yaml]

      - name: Validate all NemoClaw configs
        run: nemoclaw-gov validate --all nemoclaw/
```

### Recipe 2: evidence-gate-action with Preset

```yaml
name: NemoClaw Quality Gates
on: [pull_request]

jobs:
  gates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Convert YAML to JSON
        run: |
          pip install pyyaml
          python -c "
          import yaml, json
          for src, dst in [
              ('nemoclaw/blueprint.yaml', '/tmp/blueprint.json'),
              ('policies/openclaw-sandbox.yaml', '/tmp/policy.json'),
          ]:
              with open(src) as f: data = yaml.safe_load(f)
              with open(dst, 'w') as f: json.dump(data, f)
          "

      - name: NemoClaw Governance Gate
        uses: evidence-gate/evidence-gate-action@v1
        with:
          gate_preset: nemoclaw-baseline
          phase_id: deploy
          evidence_files: /tmp/blueprint.json,/tmp/policy.json
          sticky_comment: true
```

### Recipe 3: Validate + Deploy with agentgov

```yaml
name: Deploy with Governance
on:
  push:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install validator
        run: pip install nemoclaw-governance[yaml]

      - name: Validate configs
        run: |
          nemoclaw-gov validate nemoclaw/blueprint.yaml
          nemoclaw-gov validate policies/openclaw-sandbox.yaml

  deploy:
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy NemoClaw sandbox
        run: |
          nemoclaw launch --profile agentgov
```

### Recipe 4: Observe Mode (Dry Run)

```yaml
- name: NemoClaw Gate (Observe)
  uses: evidence-gate/evidence-gate-action@v1
  with:
    gate_preset: nemoclaw-baseline
    phase_id: deploy
    evidence_files: /tmp/blueprint.json,/tmp/policy.json
    mode: observe
```

## Troubleshooting

### "YAML files require PyYAML"

Install with YAML support:

```bash
pip install nemoclaw-governance[yaml]
```

Or install PyYAML separately: `pip install pyyaml`

### "Cannot determine file type"

The validator auto-detects blueprints (have `profiles`/`sandbox`) vs policies (have `network_policies`). If your file doesn't match either pattern, specify the check manually:

```python
from nemoclaw_governance import validate_blueprint
import yaml

with open("my-config.yaml") as f:
    data = yaml.safe_load(f)
result = validate_blueprint(data)
```

### "File not found" when using evidence-gate-action

evidence-gate-action requires JSON evidence files. Convert YAML first:

```bash
python -c "import yaml, json; data=yaml.safe_load(open('blueprint.yaml')); json.dump(data, open('/tmp/blueprint.json','w'))"
```

### CLI exits with code 1

Exit code 1 means at least one file failed validation. Check the output for specific issue codes and fix the listed problems.

## Project Structure

```
nemoclaw-governance/
  src/
    nemoclaw_governance/
      __init__.py          # Public API: validate_*, ValidationResult
      validate.py          # Blueprint + policy validation logic
      presets.py           # Bundled preset management
      cli.py               # nemoclaw-gov CLI
  nemoclaw-presets/
    agentgov-proxy.yaml    # NemoClaw network policy preset
    agentgov-inference-profile.json
  examples/
    blueprint-with-agentgov.yaml
    policy-with-agentgov.yaml
    ci-workflow.yml
  scripts/
    setup-agentgov-provider.sh
  tests/                   # 55 tests
  .github/
    workflows/ci.yml       # Lint + test (3.11/3.12/3.13) + CLI smoke
    dependabot.yml
```

## Related Projects

| Project | Role | Link |
|---------|------|------|
| **agentgov** | Runtime budget enforcement proxy | [evidence-gate/agentgov](https://github.com/evidence-gate/agentgov) |
| **evidence-gate-action** | CI quality gate enforcement | [evidence-gate/evidence-gate-action](https://github.com/evidence-gate/evidence-gate-action) |
| **NemoClaw** | Agent sandbox (NVIDIA) | [NVIDIA/NemoClaw](https://github.com/NVIDIA/NemoClaw) |

## Links

- [Changelog](CHANGELOG.md)
- [NemoClaw Documentation](https://github.com/NVIDIA/NemoClaw)
- [agentgov Quick Start](https://github.com/evidence-gate/agentgov#quick-start)
- [evidence-gate-action Marketplace](https://github.com/marketplace/actions/evidence-gate-action)

## License

Apache License 2.0. Copyright 2026 AllNew LLC. See [LICENSE](LICENSE) for details.
