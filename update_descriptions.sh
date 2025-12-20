#!/bin/bash

# Update repository descriptions using the automation tool

cd github-repo-automation

REPOS=(
    "yksanjo/agentguard|Unified AI Agent Security & Governance Platform. Guardrails for autonomous AI agents with human-in-the-loop approval workflows."
    "yksanjo/codeshield-ai|AI-Powered Code Security. Find vulnerabilities, secrets, and compliance issues before deployment. OWASP Top 10 detection."
    "yksanjo/paymentsentinel|Real-Time Fraud Detection. ML-powered payment fraud prevention. Stop fraud while approving 99% of legitimate transactions."
    "yksanjo/legacybridge-ai-gateway|AI-Powered Mainframe Integration. Don't rewrite your mainframe—bridge it. Modern APIs for legacy systems using AI translation."
    "yksanjo/modelwatch|ML Model Monitoring & Governance. Real-time drift detection, bias monitoring, and SR 11-7 compliance for financial ML models."
    "yksanjo/fleetcommand|Multi-Cloud Infrastructure Management. Unified control plane for AWS, Azure, GCP. Reduce cloud costs by 30-40%."
    "yksanjo/promptshield|AI Prompt Injection Defense. The first line of defense for enterprise AI. Block prompt injection attacks in real-time."
    "yksanjo/identityvault-agents|AI-Powered Zero-Trust IAM. Next-generation identity and access management with AI agents. Stop account takeovers before they happen."
    "yksanjo/supplychainguard|Supply Chain Security & Risk Platform. Graph-based vendor risk assessment and SBOM generation. Prevent the next SolarWinds."
    "yksanjo/complianceiq|Automated Regulatory Compliance Monitoring. Enterprise-grade regulatory intelligence platform. Automate 80% of compliance workload with AI."
)

echo "🚀 Updating repository descriptions..."
echo ""

for repo_info in "${REPOS[@]}"; do
    IFS='|' read -r repo description <<< "$repo_info"
    echo "📦 Updating: $repo"
    python3 github-repo-automation.py --repo "$repo" --description "$description" 2>&1 | grep -E "(✅|❌|Error|Updated)" || echo "   (Check output above)"
    echo ""
done

echo "✅ Complete!"
