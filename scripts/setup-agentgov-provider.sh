#!/usr/bin/env bash
# Register agentgov as a NemoClaw inference provider
#
# Usage:
#   ./setup-agentgov-provider.sh [agentgov-url] [model]
#
# Defaults:
#   URL:   http://localhost:8787/v1  (Docker Compose)
#   Model: gpt-4o
#
# Prerequisites:
#   - NemoClaw installed and sandbox running
#   - agentgov proxy running (docker compose -f docker/compose.yml up -d)

set -euo pipefail

AGENTGOV_URL="${1:-http://localhost:8787/v1}"
MODEL="${2:-gpt-4o}"

echo "=== agentgov + NemoClaw Setup ==="
echo ""
echo "Proxy URL: ${AGENTGOV_URL}"
echo "Model:     ${MODEL}"
echo ""

# Step 1: Verify agentgov is running
echo "Step 1: Checking agentgov proxy health..."
HEALTH_URL="${AGENTGOV_URL%/v1}/health"
if curl -sf "${HEALTH_URL}" > /dev/null 2>&1; then
    echo "  ✓ agentgov proxy is healthy"
else
    echo "  ✗ agentgov proxy not reachable at ${HEALTH_URL}"
    echo "  Start it with: docker compose -f docker/compose.yml up -d"
    exit 1
fi

# Step 2: Register inference provider
echo ""
echo "Step 2: Registering agentgov as inference provider..."
openshell provider create \
    --name agentgov \
    --type openai-compatible \
    --endpoint-url "${AGENTGOV_URL}" \
    --model "${MODEL}"
echo "  ✓ Provider 'agentgov' registered"

# Step 3: Apply network policy preset
echo ""
echo "Step 3: Applying agentgov network policy preset..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRESET_PATH="${SCRIPT_DIR}/../nemoclaw-presets/agentgov-proxy.yaml"

if [ -f "${PRESET_PATH}" ]; then
    openshell policy set "${PRESET_PATH}"
    echo "  ✓ Network policy applied"
else
    echo "  ⚠ Preset not found at ${PRESET_PATH}"
    echo "  Apply manually: openshell policy set agentgov-proxy.yaml"
fi

# Step 4: Switch inference to agentgov
echo ""
echo "Step 4: Switching inference to agentgov provider..."
openshell inference set --provider agentgov --model "${MODEL}"
echo "  ✓ Inference routed through agentgov"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "All agent inference calls now route through agentgov."
echo "Budget enforcement, HITL approval, and audit logging are active."
echo ""
echo "To switch back to direct inference:"
echo "  openshell inference set --provider default"
