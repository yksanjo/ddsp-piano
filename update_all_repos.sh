#!/bin/bash

# Script to run GitHub repo automation for all 10 financial products

REPOS=(
    "yksanjo/agentguard"
    "yksanjo/codeshield-ai"
    "yksanjo/paymentsentinel"
    "yksanjo/legacybridge-ai-gateway"
    "yksanjo/modelwatch"
    "yksanjo/fleetcommand"
    "yksanjo/promptshield"
    "yksanjo/identityvault-agents"
    "yksanjo/supplychainguard"
    "yksanjo/complianceiq"
)

cd github-repo-automation

echo "🚀 Running GitHub repo automation for all 10 repositories..."
echo ""

for repo in "${REPOS[@]}"; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📦 Processing: $repo"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    python3 github-repo-automation.py --repo "$repo" 2>&1
    echo ""
    sleep 2
done

echo "✅ Complete! All repositories have been updated."
