# AI Agent Sandbox Governance Best Practices (March 2026)

## Industry Consensus: Layered Proxy Governance

Three dominant patterns:

### Pattern A: Proxy-based governance
- agentgov, OpenShell, Gravitee MCP Proxy, Microsoft Agent Governance Toolkit
- Intercepts agent actions pre-execution, deterministic policy evaluation
- Microsoft: 0.012ms single-rule, 31K ops/sec — negligible vs LLM latency

### Pattern B: Defense-in-depth layers
- Cisco + OpenShell: infrastructure sandbox + application governance
- Microsoft: 4-ring privilege model
- Mayer Brown: design-time + pre-deployment + post-deployment controls

### Pattern C: Standards-driven
- NIST AI Agent Standards Initiative (Feb 2026)
- IMDA Singapore Model AI Governance Framework for Agentic AI
- OWASP Agentic Security Initiative Top 10

## Reference Architecture (Enterprise Standard)

```
CI/CD (evidence-gate-action)
  → validates budget limits, HITL tables, policy YAML
  → progressive rollout gates
Infrastructure (OpenShell/NemoClaw)
  → filesystem/network/process isolation
  → egress only to agentgov proxy
Application (agentgov proxy)
  → budget hold/settle, HITL approval, audit trail
  → credential injection
LLM Provider
```

## Cost Control Patterns

1. Per-agent budget caps with hold/settle (agentgov — most sophisticated found)
2. Token limits per call (Microsoft toolkit)
3. Per-second billing with resource limits (E2B, Daytona)
4. Cost-aware inference routing (OpenShell Privacy Router)
5. A/B cost testing in CI/CD

## HITL Best Practices

- Async approval is standard (HTTP 202 + polling)
- Decision outcomes: approve, reject, revise (conditional)
- Approval fatigue mitigation: risk-tiering, SLA queues
- Timeout defaults to deny (fail-closed)
- Every decision logged with actor, timestamp, reason

## Key Insight

agentgov's hold/settle pattern is ahead of most frameworks. NemoClaw has zero cost controls — this is THE integration opportunity.

## Enterprise Adopters (OpenShell/NemoClaw)

Adobe, IBM Red Hat, Box, Cadence, LangChain. Cisco AI Defense integration validates two-layer proxy model.
