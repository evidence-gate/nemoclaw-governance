# NemoClaw Analysis (2026-03-17)

## Overview

NVIDIA NemoClaw: open-source agent sandbox (GTC 2026, March 16). Two components:
- **OpenShell** — containerized sandbox runtime with deny-by-default policy (fs, network, process, inference)
- **Privacy Router** — inference routing (NVIDIA Cloud / NIM / vLLM)

## Architecture

TypeScript plugin (`nemoclaw/src/`) + Python blueprint (`nemoclaw-blueprint/`) + JS CLI wrapper (`bin/nemoclaw.js`).

### 4 Protection Layers

| Layer | Mechanism | Mutability |
|-------|-----------|------------|
| Network | Deny-by-default egress, TLS-terminating, HTTP method+path rules, binary-scoped | Hot-reloadable |
| Filesystem | Landlock LSM, R/W only to /sandbox, /tmp | Locked at creation |
| Process | sandbox:sandbox user, no privilege escalation | Locked at creation |
| Inference | All model calls intercepted by OpenShell gateway, rerouted to configured provider | Hot-reloadable |

### Inference Flow

```
Agent (inside sandbox)
  → HTTP call to model API (intercepted by OpenShell)
  → OpenShell Gateway routes based on active profile
  → Provider: default (NVIDIA Cloud), ncp, nim-local, vllm, ollama, custom
```

Agent is **unaware** of routing. Profile switching at launch (`--profile`) or runtime (`openshell inference set`).

### HITL Mechanism

- TUI-only (`openshell term` / `nemoclaw term`)
- Blocked outbound connections shown for operator approve/deny
- Approval is **session-scoped** — not persisted to policy file
- No API, no webhook, no programmatic approval channel
- For permanent allow: edit `openclaw-sandbox.yaml` manually

### Configuration System

- **blueprint.yaml** — version, min versions, profiles (provider type, endpoint, model, credential_env), sandbox image
- **openclaw.plugin.json** — config schema (blueprintVersion, registry, sandboxName, inferenceProvider)
- **openclaw-sandbox.yaml** — network_policies (named groups with endpoint/rule specs), filesystem_policy, process config
- **Policy presets** — 9 YAML files (discord, docker, huggingface, jira, npm, outlook, pypi, slack, telegram)
- **State** — `~/.nemoclaw/state/nemoclaw.json` (file-based, no DB)

### Extension Points

1. Policy presets: drop YAML in `policies/presets/`
2. Inference providers: `openshell provider create --type openai-compatible`
3. OpenClaw plugin system via `openclaw.plugin.json`
4. Blueprint artifacts (versioned, digest-verified)
5. Slash commands in chat TUI
6. Endpoint types: build, ncp, nim-local, vllm, ollama, **custom**

### Key Gap: No Cost Controls

- No token counting, no spend tracking, no budget limits
- No cost-per-request metering, no rate limiting
- Inference passthrough — costs = whatever upstream charges
- **This is exactly where agentgov fills the gap**

## Integration Seams for agentgov

1. **Network policy endpoint**: Add agentgov proxy to `openclaw-sandbox.yaml` network_policies
2. **Inference provider**: Register as `openai-compatible` via `openshell provider create`
3. **Onboard system**: `nemoclaw onboard --endpoint custom --endpoint-url https://agentgov.example.com`
4. **TLS-terminating proxy**: agentgov as the proxy OpenShell routes through
5. **Programmatic HITL**: Replace/augment manual TUI approval for CI/production

## Integration Seams for evidence-gate-action

1. **Policy YAML schema validation** — existing test suite validates presets
2. **Blueprint integrity** — SHA-256 digest verification
3. **Version compatibility** — min_openshell_version / min_openclaw_version checks
4. **Policy completeness** — all required services have allowlist entries
5. **Endpoint security audit** — no overly-broad rules, TLS enforcement
6. **Machine-readable status** — `openclaw nemoclaw status --json`

## TypeScript API Surface

Key exports: `BlueprintAction`, `BlueprintRunOptions`, `BlueprintRunResult`, `NemoClawState`, `ResolvedBlueprint`, `BlueprintManifest`, `OpenClawConfig`, `NemoClawConfig`.

Key functions: `register()`, `resolveBlueprint()`, `execBlueprint()`, `verifyBlueprintDigest()`, `checkCompatibility()`, `loadState()`, `saveState()`.
