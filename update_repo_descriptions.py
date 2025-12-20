#!/usr/bin/env python3
"""
Update GitHub repository descriptions for all 10 financial products.
"""

import os
import sys
import requests

# Repository descriptions
REPOS = {
    "agentguard": "Unified AI Agent Security & Governance Platform. Guardrails for autonomous AI agents with human-in-the-loop approval workflows.",
    "codeshield-ai": "AI-Powered Code Security. Find vulnerabilities, secrets, and compliance issues before deployment. OWASP Top 10 detection.",
    "paymentsentinel": "Real-Time Fraud Detection. ML-powered payment fraud prevention. Stop fraud while approving 99% of legitimate transactions.",
    "legacybridge-ai-gateway": "AI-Powered Mainframe Integration. Don't rewrite your mainframe—bridge it. Modern APIs for legacy systems using AI translation.",
    "modelwatch": "ML Model Monitoring & Governance. Real-time drift detection, bias monitoring, and SR 11-7 compliance for financial ML models.",
    "fleetcommand": "Multi-Cloud Infrastructure Management. Unified control plane for AWS, Azure, GCP. Reduce cloud costs by 30-40%.",
    "promptshield": "AI Prompt Injection Defense. The first line of defense for enterprise AI. Block prompt injection attacks in real-time.",
    "identityvault-agents": "AI-Powered Zero-Trust IAM. Next-generation identity and access management with AI agents. Stop account takeovers before they happen.",
    "supplychainguard": "Supply Chain Security & Risk Platform. Graph-based vendor risk assessment and SBOM generation. Prevent the next SolarWinds.",
    "complianceiq": "Automated Regulatory Compliance Monitoring. Enterprise-grade regulatory intelligence platform. Automate 80% of compliance workload with AI."
}

GITHUB_USERNAME = "yksanjo"
BASE_URL = "https://api.github.com"

def update_repo_description(repo_name, description, token):
    """Update repository description via GitHub API."""
    url = f"{BASE_URL}/repos/{GITHUB_USERNAME}/{repo_name}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "description": description
    }
    
    response = requests.patch(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print(f"✅ Updated {repo_name}")
        return True
    else:
        print(f"❌ Failed to update {repo_name}: {response.status_code} - {response.text}")
        return False

def main():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ Error: GITHUB_TOKEN environment variable not set")
        print("   Set it with: export GITHUB_TOKEN=ghp_your_token_here")
        sys.exit(1)
    
    print("🚀 Updating repository descriptions...")
    print("")
    
    success_count = 0
    for repo_name, description in REPOS.items():
        if update_repo_description(repo_name, description, token):
            success_count += 1
    
    print("")
    print(f"✅ Successfully updated {success_count}/{len(REPOS)} repositories")

if __name__ == "__main__":
    main()



