# Requirements — NemoClaw Governance Integration v1.0

## evidence-gate-action NemoClaw Gates

### EGA-01: NemoClaw Blueprint Gate Type
**What:** `nemoclaw_blueprint` gate type in `local_evaluator.py` that validates NemoClaw `blueprint.yaml` structure.
**Acceptance:** Gate passes valid blueprint YAML (version, profiles, sandbox config). Gate fails on: missing required fields, invalid version constraints, missing credential_env, undefined profiles. Free mode (local evaluation, no API needed).
**Priority:** Must

### EGA-02: NemoClaw Policy Gate Type
**What:** `nemoclaw_policy` gate type that validates OpenShell `openclaw-sandbox.yaml` security posture.
**Acceptance:** Gate validates: all endpoints have TLS enforcement, no wildcard method rules on sensitive endpoints, binary scoping present, no overly-broad `access: full` entries. Produces actionable `suggested_actions` on failure.
**Priority:** Must

### EGA-03: NemoClaw Baseline Preset
**What:** `nemoclaw-baseline` preset in `presets.py` bundling NemoClaw-specific + standard gates.
**Acceptance:** Preset includes: `nemoclaw_blueprint`, `nemoclaw_policy`, `security`, `build`. Usable via `gate_preset: nemoclaw-baseline` in GitHub Actions.
**Priority:** Must

### EGA-04: NemoClaw Recommendation Table
**What:** Recommendation entries in `entrypoint.py` for NemoClaw gate failures.
**Acceptance:** Covers: blueprint schema errors, policy security gaps, missing presets, version incompatibility. Priority-sorted, human-readable repair steps.
**Priority:** Should

### EGA-05: NemoClaw Evidence Schema
**What:** JSON Schema definitions for NemoClaw evidence files (blueprint validation results, policy audit results).
**Acceptance:** Schema validates evidence structure. SHA-256 hashing via existing `build_evidence_ref()`. Compatible with L4 trust level.
**Priority:** Should

## agentgov NemoClaw Integration

### AGV-01: NemoClaw Policy Preset
**What:** `agentgov-proxy.yaml` policy preset file compatible with NemoClaw's `policies/presets/` format.
**Acceptance:** Configures network_policies to allow sandbox egress to agentgov proxy (configurable host:port). TLS enforcement, proper binary scoping. Follows NemoClaw preset YAML schema exactly. Installable via `nemoclaw policy-add`.
**Priority:** Must

### AGV-02: agentgov Inference Provider Registration
**What:** Documentation + helper script to register agentgov as NemoClaw inference provider.
**Acceptance:** `openshell provider create --type openai-compatible --config <agentgov-url>` works. Agent inside sandbox transparently routes through agentgov. Budget enforcement confirmed via hold/settle. Supports all 3 LLM providers (OpenAI, Anthropic, Gemini via agentgov).
**Priority:** Must

### AGV-03: NemoClaw Onboard Integration
**What:** Integration with NemoClaw's `nemoclaw onboard` flow for agentgov setup.
**Acceptance:** `nemoclaw onboard --endpoint custom --endpoint-url <agentgov-proxy>` configures both inference routing and network policy. Agent-id header injection documented.
**Priority:** Should

### AGV-04: Programmatic HITL Bridge
**What:** Bridge between agentgov's webhook/Slack HITL and NemoClaw's TUI HITL for unified approval flow.
**Acceptance:** Network-level blocks from OpenShell trigger agentgov HITL webhook. Approval/denial propagated back. Single approval queue for both network and inference governance.
**Priority:** Could

## Integration & Documentation

### INT-01: Example NemoClaw Blueprint with agentgov
**What:** Reference `blueprint.yaml` with agentgov as inference provider + corresponding policy.
**Acceptance:** Complete working example: blueprint.yaml, openclaw-sandbox.yaml with agentgov preset, .env template. Copy-paste deployable.
**Priority:** Must

### INT-02: GitHub Actions Workflow Example
**What:** Example CI workflow using evidence-gate-action NemoClaw gates.
**Acceptance:** `.github/workflows/nemoclaw-governance.yml` validates blueprint + policy before deployment. Uses `nemoclaw-baseline` preset. Includes sticky PR comment.
**Priority:** Must

### INT-03: Integration Test Suite
**What:** Tests validating agentgov + evidence-gate-action + NemoClaw interoperability.
**Acceptance:** Blueprint validation tests (valid/invalid YAML), policy validation tests (secure/insecure configs), preset installation tests. CI-runnable without NemoClaw runtime (static analysis only).
**Priority:** Must

### INT-04: Architecture Documentation
**What:** Technical documentation of the 3-layer governance architecture.
**Acceptance:** Explains: CI layer (evidence-gate-action) → Infrastructure layer (NemoClaw) → Application layer (agentgov). Includes architecture diagram, data flow, configuration reference. Published as README.md in this repo.
**Priority:** Should

---

## Summary

| Category | Must | Should | Could | Total |
|----------|------|--------|-------|-------|
| evidence-gate-action | 3 | 2 | 0 | 5 |
| agentgov | 2 | 1 | 1 | 4 |
| Integration | 3 | 1 | 0 | 4 |
| **Total** | **8** | **4** | **1** | **13** |
