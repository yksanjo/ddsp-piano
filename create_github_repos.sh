#!/bin/bash

# Script to create all 10 GitHub repositories using GitHub API
# Requires: GITHUB_TOKEN environment variable

set -e

# Check for GitHub token
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: GITHUB_TOKEN environment variable not set"
    echo ""
    echo "To get a token:"
    echo "1. Go to: https://github.com/settings/tokens"
    echo "2. Generate new token (classic)"
    echo "3. Select scope: repo (full control)"
    echo "4. Set token: export GITHUB_TOKEN=ghp_your_token_here"
    exit 1
fi

# Get GitHub username
if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ Error: GITHUB_USERNAME environment variable not set"
    echo "Set it with: export GITHUB_USERNAME=your-username"
    exit 1
fi

echo "🚀 Creating 10 GitHub Repositories..."
echo "GitHub User: $GITHUB_USERNAME"
echo ""

# Product configurations
declare -A PRODUCTS=(
    ["agentguard"]="AgentGuard Enterprise Platform|Unified AI Agent Security & Governance Suite for Financial Institutions"
    ["codeshield-ai"]="CodeShield AI|Secure Development Gateway for AI-Generated Code in Banking"
    ["paymentsentinel"]="PaymentSentinel|Real-Time Transaction Defense System for AI Agent Payments"
    ["legacybridge-ai-gateway"]="LegacyBridge AI Gateway|Secure Integration Layer for Legacy Core Banking Systems"
    ["modelwatch"]="ModelWatch|AI Integrity Monitoring Platform for Financial Services (SR 11-7 Compliance)"
    ["fleetcommand"]="FleetCommand|Multi-Agent Orchestration Platform for Financial Institutions"
    ["promptshield"]="PromptShield|AI Agent Input Validation System - Enterprise-Grade Prompt Injection Defense"
    ["identityvault-agents"]="IdentityVault for Agents|Non-Human IAM Platform for AI Agents in Banking"
    ["supplychainguard"]="SupplyChainGuard|AI Development Tool Security for Financial Services"
    ["complianceiq"]="ComplianceIQ|AI Governance & Reporting Suite for Regulatory Compliance"
)

# Topics for all repos
TOPICS="financial-services,ai-security,banking,regulatory-compliance,enterprise-software,ai-governance,cybersecurity,fintech,g-sib,agentic-ai"

# Function to create a GitHub repo
create_repo() {
    local repo_name=$1
    local product_name=$2
    local description=$3
    
    echo "📦 Creating: $repo_name"
    
    # Check if repo already exists
    response=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        "https://api.github.com/repos/$GITHUB_USERNAME/$repo_name")
    
    if [ "$response" = "200" ]; then
        echo "  ⚠️  Repository already exists, skipping..."
        return
    fi
    
    # Create repository
    response=$(curl -s -w "\n%{http_code}" \
        -X POST \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        -H "Content-Type: application/json" \
        -d "{
            \"name\": \"$repo_name\",
            \"description\": \"$description\",
            \"private\": false,
            \"has_issues\": true,
            \"has_projects\": false,
            \"has_wiki\": false,
            \"auto_init\": false
        }" \
        "https://api.github.com/user/repos")
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "201" ]; then
        echo "  ✅ Repository created successfully"
        
        # Add topics
        echo "  📌 Adding topics..."
        curl -s -X PUT \
            -H "Authorization: token $GITHUB_TOKEN" \
            -H "Accept: application/vnd.github.mercy-preview+json" \
            -H "Content-Type: application/json" \
            -d "{\"names\": [$(echo $TOPICS | sed 's/,/","/g' | sed 's/^/"/' | sed 's/$/"/')]}" \
            "https://api.github.com/repos/$GITHUB_USERNAME/$repo_name/topics" > /dev/null
        
        echo "  ✅ Topics added"
        echo "  🔗 https://github.com/$GITHUB_USERNAME/$repo_name"
    else
        echo "  ❌ Failed to create repository"
        echo "  Response: $body"
    fi
    echo ""
}

# Create all repositories
for repo_name in "${!PRODUCTS[@]}"; do
    IFS='|' read -r product_name description <<< "${PRODUCTS[$repo_name]}"
    create_repo "$repo_name" "$product_name" "$description"
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ All repositories created!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Push code to each repository:"
echo "   cd financial-products-repos/[repo-name]"
echo "   git remote add origin https://github.com/$GITHUB_USERNAME/[repo-name].git"
echo "   git commit -m 'Initial commit: [Product Name]'"
echo "   git push -u origin main"
echo ""
echo "2. Or use the push script:"
echo "   ./push_all_repos.sh"
echo ""




