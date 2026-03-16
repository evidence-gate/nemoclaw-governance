# evidence-gate-action Analysis (2026-03-17)

## Overview

Fail-closed quality gate enforcement for GitHub Actions CI/CD. Anti-gaming: Blind Gates, Evidence Trust Levels (L1-L4), fail-closed semantics.

**License:** Apache 2.0 | **Language:** Python 3.11+ | **Dependencies:** Zero runtime (stdlib only)

## Architecture (5 files)

| File | Role | LOC |
|------|------|-----|
| `src/entrypoint.py` | GH Actions adapter, recommendations | ~450 |
| `src/core.py` | API client, evidence hashing, fail-closed | ~200 |
| `src/local_evaluator.py` | Free mode evaluation (schema, thresholds) | ~190 |
| `src/presets.py` | Gate preset bundles | ~40 |
| `src/sticky_comment.py` | PR comment management | ~130 |

## Inputs/Outputs

12 inputs (gate_type, phase_id, api_key, evidence_files, api_base, mode, gate_preset, sticky_comment, debug, version, dashboard_base_url, evidence_url).

12 outputs (passed, mode, run_id, major_issue_count, missing_evidence, suggested_actions, json_output, trace_url, evidence_url, dashboard_url, github_run_url, observe_would_pass).

## Gate Types

**Free mode (local):** file existence, JSON validity, JSON schema, numeric thresholds, SHA-256 hashes.

**Pro/Enterprise (API):** blind_gate, quality_state, remediation, composite, wave.

**Presets:**
- `web-app-baseline`: test_coverage, security, dependency, build
- `enterprise-compliance`: 10 gates
- `api-service`: 7 gates
- `supply-chain`: security, dependency, compliance, build

## Extension Points for NemoClaw

1. **New gate type in `local_evaluator.py`**: Add `check_blueprint_*()` functions, wire to `evaluate_local()` with `gate_type == "nemoclaw_blueprint"`
2. **New preset in `presets.py`**: `"nemoclaw-baseline": ["nemoclaw_blueprint", "nemoclaw_policy", "security", "build"]`
3. **Pro/Enterprise Blind Gate**: Register `nemoclaw_blueprint` server-side for anti-gaming
4. **Evidence chain**: NemoClaw budget/policy decisions as SHA-256 hashed evidence files
5. **Recommendation table**: Add `("nemoclaw_*", "...")` entries in `entrypoint.py`

**Minimal change surface:** 2-3 files (local_evaluator.py, presets.py, optionally entrypoint.py).
