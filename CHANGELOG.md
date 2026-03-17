# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.1.0] - 2026-03-17

### Added

- Blueprint validation (`nemoclaw_blueprint` gate): version, profiles, sandbox, version constraints
- Policy security audit (`nemoclaw_policy` gate): enforcement mode, TLS, wildcard methods, filesystem safety
- `nemoclaw-baseline` preset for evidence-gate-action (blueprint + policy + security + build)
- agentgov proxy policy preset (`agentgov-proxy.yaml`) for NemoClaw sandbox network policy
- Inference provider config for registering agentgov with OpenShell
- CLI tool (`nemoclaw-gov`): validate files, manage presets
- Auto-detection of blueprint vs policy files
- Example blueprint, policy, and CI workflow
- Setup script for one-command agentgov + NemoClaw integration
- 10 integration tests + evidence-gate-action test suite (28 NemoClaw tests)

[Unreleased]: https://github.com/evidence-gate/nemoclaw-governance/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/evidence-gate/nemoclaw-governance/releases/tag/v0.1.0
