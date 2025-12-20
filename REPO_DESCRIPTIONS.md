# Repository Descriptions to Update

## How to Update Descriptions

### Option 1: Using GitHub Token (Automated)

1. **Create a GitHub Personal Access Token**:
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scope: `repo` (full control of private repositories)
   - Copy the token

2. **Set the token and run the script**:
   ```bash
   export GITHUB_TOKEN=ghp_your_token_here
   cd /Users/yoshikondo/ddsp-piano
   python3 update_repo_descriptions.py
   ```

### Option 2: Manual Update via GitHub Web UI

For each repository, go to Settings → General → Description and paste the description below:

---

## Descriptions for Each Repository

### 1. AgentGuard
```
Unified AI Agent Security & Governance Platform. Guardrails for autonomous AI agents with human-in-the-loop approval workflows.
```

### 2. CodeShield AI
```
AI-Powered Code Security. Find vulnerabilities, secrets, and compliance issues before deployment. OWASP Top 10 detection.
```

### 3. PaymentSentinel
```
Real-Time Fraud Detection. ML-powered payment fraud prevention. Stop fraud while approving 99% of legitimate transactions.
```

### 4. LegacyBridge AI Gateway
```
AI-Powered Mainframe Integration. Don't rewrite your mainframe—bridge it. Modern APIs for legacy systems using AI translation.
```

### 5. ModelWatch
```
ML Model Monitoring & Governance. Real-time drift detection, bias monitoring, and SR 11-7 compliance for financial ML models.
```

### 6. FleetCommand
```
Multi-Cloud Infrastructure Management. Unified control plane for AWS, Azure, GCP. Reduce cloud costs by 30-40%.
```

### 7. PromptShield
```
AI Prompt Injection Defense. The first line of defense for enterprise AI. Block prompt injection attacks in real-time.
```

### 8. IdentityVault-Agents
```
AI-Powered Zero-Trust IAM. Next-generation identity and access management with AI agents. Stop account takeovers before they happen.
```

### 9. SupplyChainGuard
```
Supply Chain Security & Risk Platform. Graph-based vendor risk assessment and SBOM generation. Prevent the next SolarWinds.
```

### 10. ComplianceIQ
```
Automated Regulatory Compliance Monitoring. Enterprise-grade regulatory intelligence platform. Automate 80% of compliance workload with AI.
```

---

## Quick Links to Update Each Repo

1. [AgentGuard Settings](https://github.com/yksanjo/agentguard/settings)
2. [CodeShield AI Settings](https://github.com/yksanjo/codeshield-ai/settings)
3. [PaymentSentinel Settings](https://github.com/yksanjo/paymentsentinel/settings)
4. [LegacyBridge Settings](https://github.com/yksanjo/legacybridge-ai-gateway/settings)
5. [ModelWatch Settings](https://github.com/yksanjo/modelwatch/settings)
6. [FleetCommand Settings](https://github.com/yksanjo/fleetcommand/settings)
7. [PromptShield Settings](https://github.com/yksanjo/promptshield/settings)
8. [IdentityVault Settings](https://github.com/yksanjo/identityvault-agents/settings)
9. [SupplyChainGuard Settings](https://github.com/yksanjo/supplychainguard/settings)
10. [ComplianceIQ Settings](https://github.com/yksanjo/complianceiq/settings)

---

## Using the Python Script (If you have a token)

The script `update_repo_descriptions.py` is ready to use. Just set your token:

```bash
export GITHUB_TOKEN=ghp_your_token_here
python3 update_repo_descriptions.py
```

This will update all 10 repositories automatically.



