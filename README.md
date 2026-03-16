# NemoClaw Governance Integration

Three-layer governance for AI agents: infrastructure isolation (NemoClaw) + cost control (agentgov) + CI quality gates (evidence-gate-action).

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

---

## The Problem

NVIDIA NemoClaw provides sandboxed execution for AI agents with network, filesystem, and process isolation. But it has **no cost controls** -- a sandboxed agent can still burn through hundreds of dollars in inference costs.

This project bridges the gap by integrating [agentgov](https://github.com/evidence-gate/agentgov) (budget enforcement) and [evidence-gate-action](https://github.com/evidence-gate/evidence-gate-action) (CI quality gates) with NemoClaw.

## Architecture

```
┌─────────────────────────────────────────────────┐
│  CI/CD Layer                                     │
│  evidence-gate-action validates:                 │
│  - Blueprint structure (nemoclaw_blueprint gate) │
│  - Policy security (nemoclaw_policy gate)        │
│  - nemoclaw-baseline preset for full validation  │
└─────────┬───────────────────────────────────────┘
          │ deploy
          ▼
┌─────────────────────────────────────────────────┐
│  Infrastructure Layer (NemoClaw/OpenShell)       │
│  - Filesystem isolation (Landlock LSM)           │
│  - Network: deny-by-default, agentgov-only      │
│  - Process sandboxing (no privilege escalation)  │
└─────────┬───────────────────────────────────────┘
          │ inference requests → agentgov proxy
          ▼
┌─────────────────────────────────────────────────┐
│  Application Layer (agentgov proxy)              │
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

## What's Included

### For evidence-gate-action (CI quality gates)

New gate types for validating NemoClaw configurations:

| Gate Type | What It Validates |
|-----------|-------------------|
| `nemoclaw_blueprint` | Blueprint structure: version, profiles, sandbox config |
| `nemoclaw_policy` | Policy security: TLS enforcement, no wildcards, safe filesystem |
| `nemoclaw-baseline` preset | All of the above + security + build |

### For agentgov (runtime governance)

| Artifact | Purpose |
|----------|---------|
| `agentgov-proxy.yaml` | NemoClaw policy preset -- allows sandbox egress only to agentgov |
| `agentgov-inference-profile.json` | Provider config for `openshell provider create` |
| `setup-agentgov-provider.sh` | One-command setup: register provider + apply policy |

### Examples

| File | Description |
|------|-------------|
| `blueprint-with-agentgov.yaml` | NemoClaw blueprint with agentgov as inference provider |
| `policy-with-agentgov.yaml` | OpenShell policy with agentgov-only egress |
| `ci-workflow.yml` | GitHub Actions workflow using NemoClaw gates |

## Quick Start

### 1. Add agentgov to NemoClaw

```bash
# Start agentgov proxy
cd /path/to/agentgov
docker compose -f docker/compose.yml up -d

# Register as NemoClaw inference provider
./scripts/setup-agentgov-provider.sh
# or manually:
openshell provider create --name agentgov --type openai-compatible \
  --endpoint-url http://localhost:8787/v1 --model gpt-4o
openshell inference set --provider agentgov --model gpt-4o
```

### 2. Apply network policy

```bash
# Allow sandbox to reach agentgov proxy only
nemoclaw policy-add nemoclaw-presets/agentgov-proxy.yaml
```

### 3. Add CI gates

```yaml
# .github/workflows/nemoclaw-gate.yml
- name: Validate Blueprint
  uses: evidence-gate/evidence-gate-action@v1
  with:
    gate_type: nemoclaw_blueprint
    phase_id: deploy
    evidence_files: /tmp/blueprint.json

- name: Validate Policy
  uses: evidence-gate/evidence-gate-action@v1
  with:
    gate_type: nemoclaw_policy
    phase_id: deploy
    evidence_files: /tmp/policy.json
```

## Gate Details

### nemoclaw_blueprint

Validates NemoClaw `blueprint.yaml` structure:

- `version` exists and is valid semver
- `profiles` has at least one entry with required fields (`model`)
- `sandbox` section with `image` field
- Optional version constraints (`min_openshell_version`, `min_openclaw_version`) are valid semver

### nemoclaw_policy

Security audit of NemoClaw `openclaw-sandbox.yaml`:

- All endpoints have `enforcement: enforce` (not `monitor`)
- Port 443 endpoints have `tls: terminate`
- No wildcard HTTP method rules (`method: "*"`)
- No dangerous writable filesystem paths (`/usr`, `/etc`, `/lib`, etc.)

### nemoclaw-baseline preset

Runs all four gates: `nemoclaw_blueprint` + `nemoclaw_policy` + `security` + `build`

## Project Structure

```
nemoclaw-workspace/
  nemoclaw-presets/
    agentgov-proxy.yaml              # NemoClaw policy preset
    agentgov-inference-profile.json  # Provider registration config
  examples/
    blueprint-with-agentgov.yaml     # Reference blueprint
    policy-with-agentgov.yaml        # Reference policy
    ci-workflow.yml                   # GitHub Actions example
  scripts/
    setup-agentgov-provider.sh       # One-command setup
  tests/
    test_policy_preset.py            # Integration tests
  repos/
    evidence-gate-action/            # Cloned repo with NemoClaw gates
    agentgov/                        # Cloned repo (reference)
```

## License

[Apache 2.0](LICENSE) -- Copyright 2026 AllNew LLC
