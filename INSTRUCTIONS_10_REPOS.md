# Instructions: Creating 10 Separate GitHub Repositories

## Overview

This guide will help you create **10 separate GitHub repositories**, one for each financial product.

---

## Step 1: Run Setup Script

This creates all 10 local repositories with proper structure:

```bash
./setup_10_separate_repos.sh
```

**What it does:**
- Creates 10 separate directories in `financial-products-repos/`
- Each repo has:
  - `README.md` (product-specific)
  - `product-specification.md` (full product doc)
  - `.gitignore`
  - Git initialized

**Output:**
```
financial-products-repos/
├── agentguard/
├── codeshield-ai/
├── paymentsentinel/
├── legacybridge-ai-gateway/
├── modelwatch/
├── fleetcommand/
├── promptshield/
├── identityvault-agents/
├── supplychainguard/
└── complianceiq/
```

---

## Step 2: Create GitHub Repositories

### Option A: Automated (Recommended)

**Prerequisites:**
1. Get GitHub Personal Access Token:
   - Go to: https://github.com/settings/tokens
   - Generate new token (classic)
   - Select scope: **repo** (full control)
   - Copy the token

2. Set environment variables:
   ```bash
   export GITHUB_TOKEN=ghp_your_token_here
   export GITHUB_USERNAME=your-username
   ```

3. Run the creation script:
   ```bash
   ./create_github_repos.sh
   ```

**What it does:**
- Creates all 10 repositories on GitHub
- Sets descriptions and topics automatically
- Skips if repository already exists

### Option B: Manual

Create each repository manually:

1. Go to: https://github.com/new
2. For each product, create a repository:

| Repository Name | Description |
|----------------|-------------|
| `agentguard` | AgentGuard Enterprise Platform - Unified AI Agent Security & Governance Suite for Financial Institutions |
| `codeshield-ai` | CodeShield AI - Secure Development Gateway for AI-Generated Code in Banking |
| `paymentsentinel` | PaymentSentinel - Real-Time Transaction Defense System for AI Agent Payments |
| `legacybridge-ai-gateway` | LegacyBridge AI Gateway - Secure Integration Layer for Legacy Core Banking Systems |
| `modelwatch` | ModelWatch - AI Integrity Monitoring Platform for Financial Services (SR 11-7 Compliance) |
| `fleetcommand` | FleetCommand - Multi-Agent Orchestration Platform for Financial Institutions |
| `promptshield` | PromptShield - AI Agent Input Validation System - Enterprise-Grade Prompt Injection Defense |
| `identityvault-agents` | IdentityVault for Agents - Non-Human IAM Platform for AI Agents in Banking |
| `supplychainguard` | SupplyChainGuard - AI Development Tool Security for Financial Services |
| `complianceiq` | ComplianceIQ - AI Governance & Reporting Suite for Regulatory Compliance |

**For each repo:**
- ✅ Name: [repository-name]
- ✅ Description: [as shown above]
- ✅ Public or Private (your choice)
- ❌ **DO NOT** initialize with README, .gitignore, or license

---

## Step 3: Push Code to GitHub

### Option A: Automated Push

```bash
export GITHUB_USERNAME=your-username
./push_all_repos.sh
```

**What it does:**
- Pushes all 10 repositories to GitHub
- Adds remote origin
- Creates initial commit
- Pushes to main branch

### Option B: Manual Push

For each repository:

```bash
cd financial-products-repos/[repo-name]

# Add remote (if not already added)
git remote add origin https://github.com/YOUR_USERNAME/[repo-name].git

# Commit (if not already committed)
git add .
git commit -m "Initial commit: [Product Name]"

# Push
git push -u origin main
```

**Example:**
```bash
cd financial-products-repos/agentguard
git remote add origin https://github.com/YOUR_USERNAME/agentguard.git
git add .
git commit -m "Initial commit: AgentGuard Enterprise Platform"
git push -u origin main
```

---

## Step 4: Configure Each Repository

After pushing, configure each repository on GitHub:

### 1. Add Topics/Tags

Go to each repository → Settings → Topics, and add:

**Common topics for all:**
- `financial-services`
- `ai-security`
- `banking`
- `regulatory-compliance`
- `enterprise-software`
- `ai-governance`
- `cybersecurity`
- `fintech`
- `g-sib`
- `agentic-ai`

**Product-specific topics:**

| Product | Additional Topics |
|---------|-------------------|
| agentguard | `security-monitoring`, `siem`, `compliance` |
| codeshield-ai | `devsecops`, `code-security`, `static-analysis` |
| paymentsentinel | `fraud-prevention`, `payment-security`, `transaction-monitoring` |
| legacybridge-ai-gateway | `core-banking`, `legacy-systems`, `api-gateway` |
| modelwatch | `ml-ops`, `model-validation`, `model-risk` |
| fleetcommand | `orchestration`, `multi-agent`, `coordination` |
| promptshield | `prompt-injection`, `input-validation`, `waf` |
| identityvault-agents | `iam`, `identity-management`, `access-control` |
| supplychainguard | `supply-chain-security`, `sbom`, `dependency-scanning` |
| complianceiq | `regulatory-reporting`, `compliance`, `governance` |

### 2. Pin Important Files

- Pin `product-specification.md` (if GitHub supports it)
- Or add to README as primary documentation link

### 3. Add Website (Optional)

If you have a product website or documentation site, add it in repository settings.

---

## Repository Structure

Each repository will have:

```
[repo-name]/
├── README.md                    # Product overview and quick start
├── product-specification.md     # Complete product documentation
└── .gitignore                   # Git ignore file
```

---

## Quick Reference: All 10 Repositories

| # | Repository Name | Product Name |
|---|----------------|--------------|
| 1 | `agentguard` | AgentGuard Enterprise Platform |
| 2 | `codeshield-ai` | CodeShield AI |
| 3 | `paymentsentinel` | PaymentSentinel |
| 4 | `legacybridge-ai-gateway` | LegacyBridge AI Gateway |
| 5 | `modelwatch` | ModelWatch |
| 6 | `fleetcommand` | FleetCommand |
| 7 | `promptshield` | PromptShield |
| 8 | `identityvault-agents` | IdentityVault for Agents |
| 9 | `supplychainguard` | SupplyChainGuard |
| 10 | `complianceiq` | ComplianceIQ |

---

## Complete Workflow

```bash
# 1. Setup local repositories
./setup_10_separate_repos.sh

# 2. Set GitHub credentials
export GITHUB_TOKEN=ghp_your_token_here
export GITHUB_USERNAME=your-username

# 3. Create GitHub repositories (automated)
./create_github_repos.sh

# 4. Push all repositories (automated)
./push_all_repos.sh

# 5. Configure each repository on GitHub
# - Add topics
# - Update descriptions if needed
# - Pin important files
```

---

## Troubleshooting

### Repository Already Exists
If a repository already exists, the scripts will skip it. You can:
- Delete the existing repo and recreate
- Or manually push to existing repo

### Push Fails
- Check that repository exists on GitHub
- Verify GITHUB_USERNAME is correct
- Check git remote is set correctly

### Missing Files
- Ensure you're in the `ddsp-piano` directory
- Check that product specification files exist (product-*.md)

---

## Next Steps After Setup

1. **Share repositories** with target institutions
2. **Update contact information** in each README.md
3. **Add license files** if needed
4. **Create releases** for versioning
5. **Set up GitHub Pages** for documentation websites (optional)

---

## Support

If you encounter issues:
1. Check that all scripts are executable: `chmod +x *.sh`
2. Verify environment variables are set
3. Check GitHub token has correct permissions
4. Review error messages for specific issues

---

**All 10 repositories will be ready for sharing with financial institutions!**




