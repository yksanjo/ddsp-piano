#!/bin/bash

# Setup Script for 10 Separate Financial Product Repositories
# Creates individual repos for each of the 10 products

set -e

echo "🚀 Setting up 10 Separate Product Repositories..."
echo ""

# Product configurations (using arrays instead of associative arrays for compatibility)
PRODUCT_KEYS=("1-agentguard" "2-codeshield-ai" "3-paymentsentinel" "4-legacybridge" "5-modelwatch" "6-fleetcommand" "7-promptshield" "8-identityvault" "9-supplychainguard" "10-complianceiq")
PRODUCT_NAMES=("AgentGuard Enterprise Platform" "CodeShield AI" "PaymentSentinel" "LegacyBridge AI Gateway" "ModelWatch" "FleetCommand" "PromptShield" "IdentityVault for Agents" "SupplyChainGuard" "ComplianceIQ")
PRODUCT_TAGLINES=("Unified AI Agent Security & Governance Suite" "Secure Development Gateway for AI-Generated Code" "Real-Time Transaction Defense for AI Agents" "Secure Integration Layer for Legacy Core Banking" "AI Integrity Monitoring Platform for Financial Services" "Multi-Agent Orchestration Platform" "AI Agent Input Validation System" "Non-Human IAM Platform" "AI Development Tool Security" "AI Governance & Reporting Suite")
REPO_NAMES=("agentguard" "codeshield-ai" "paymentsentinel" "legacybridge-ai-gateway" "modelwatch" "fleetcommand" "promptshield" "identityvault-agents" "supplychainguard" "complianceiq")

BASE_DIR="./financial-products-repos"
mkdir -p "$BASE_DIR"

echo "📁 Creating repositories in: $BASE_DIR"
echo ""

# Function to create README for a product
create_product_readme() {
    local product_num=$1
    local product_key=$2
    local product_name=$3
    local product_tagline=$4
    local repo_name=$5
    
    cat > "$BASE_DIR/$repo_name/README.md" << EOF
# $product_name

> $product_tagline

[![License](https://img.shields.io/badge/license-Proprietary-blue.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-complete-brightgreen.svg)](product-specification.md)

## 🎯 Overview

$product_name is part of the **Agentic AI Security Suite for Financial Institutions** - a comprehensive platform designed to prevent agentic AI financial disruption in 2026.

## 📚 Documentation

- **[Product Specification](product-specification.md)** - Complete product documentation
- **[Suite Overview](../README_FINANCIAL_INSTITUTIONS.md)** - Full suite documentation for G-SIBs
- **[Quick Reference](../QUICK_REFERENCE_G-SIBs.md)** - Executive summary

## 🏦 Target Institutions

This product is designed for **Global Systemically Important Banks (G-SIBs)**:

- JPMorgan Chase & Co.
- Morgan Stanley
- Bank of America
- Citigroup Inc.
- Goldman Sachs
- Wells Fargo
- U.S. Bancorp
- Other G-SIBs globally

## 🚀 Quick Start

1. **Review** the [Product Specification](product-specification.md)
2. **Schedule** an executive briefing
3. **Request** a technical assessment
4. **Begin** proof-of-concept discussion

## 💰 Pricing

### Starter Edition
Starting at \$75K-200K/year depending on product

### Professional Edition
Starting at \$250K-600K/year

### Enterprise Edition
\$750K-3M/year (custom pricing for G-SIBs)

### PE Portfolio License
Custom pricing for portfolio-wide deployment

## 📋 Features

See [Product Specification](product-specification.md) for complete feature list.

## 🔗 Related Products

This product is part of a 10-product suite:

1. [AgentGuard](../agentguard) - Unified AI Agent Security
2. [CodeShield AI](../codeshield-ai) - Secure Development Gateway
3. [PaymentSentinel](../paymentsentinel) - Real-Time Transaction Defense
4. [LegacyBridge](../legacybridge-ai-gateway) - Legacy Core Protection
5. [ModelWatch](../modelwatch) - AI Model Integrity Monitoring
6. [FleetCommand](../fleetcommand) - Multi-Agent Orchestration
7. [PromptShield](../promptshield) - Input Validation System
8. [IdentityVault](../identityvault-agents) - Non-Human IAM
9. [SupplyChainGuard](../supplychainguard) - Development Tool Security
10. [ComplianceIQ](../complianceiq) - Regulatory Reporting

## 📞 Contact

- **Enterprise Sales**: [Contact Information]
- **Technical Assessment**: [Contact Information]
- **Regulatory Advisory**: [Contact Information]

## 📄 License

Proprietary - Enterprise License Required

---

**Part of the Agentic AI Security Suite - Purpose-Built for G-SIBs**
EOF
}

# Function to create product repo
create_product_repo() {
    local product_num=$1
    local product_key=$2
    local product_info=$3
    
    # Parse product info
    IFS='|' read -r product_name product_tagline repo_name <<< "$product_info"
    
    echo "📦 Creating repository for: $product_name"
    
    # Create directory
    local repo_dir="$BASE_DIR/$repo_name"
    mkdir -p "$repo_dir"
    
    # Copy product specification
    local spec_file="product-$product_key.md"
    if [ -f "$spec_file" ]; then
        cp "$spec_file" "$repo_dir/product-specification.md"
        echo "  ✅ Copied product specification"
    else
        echo "  ⚠️  Product specification not found: $spec_file"
    fi
    
    # Create README
    create_product_readme "$product_num" "$product_key" "$product_name" "$product_tagline" "$repo_name"
    echo "  ✅ Created README.md"
    
    # Create .gitignore
    cat > "$repo_dir/.gitignore" << 'EOF'
# OS files
.DS_Store
Thumbs.db

# Editor files
.vscode/
.idea/
*.swp
*.swo
*~

# Temporary files
*.tmp
*.log
*.cache

# Personal notes
NOTES.md
TODO.md
*.personal
EOF
    echo "  ✅ Created .gitignore"
    
    # Initialize git
    cd "$repo_dir"
    if [ ! -d ".git" ]; then
        git init
        git branch -M main
        git add .
        echo "  ✅ Git initialized"
    fi
    cd - > /dev/null
    
    echo "  ✅ Repository ready: $repo_name"
    echo ""
}

# Create all product repos
for i in "${!PRODUCT_KEYS[@]}"; do
    product_key="${PRODUCT_KEYS[$i]}"
    product_name="${PRODUCT_NAMES[$i]}"
    product_tagline="${PRODUCT_TAGLINES[$i]}"
    repo_name="${REPO_NAMES[$i]}"
    product_num=$(echo "$product_key" | cut -d'-' -f1)
    product_info="${product_name}|${product_tagline}|${repo_name}"
    create_product_repo "$product_num" "$product_key" "$product_info"
done

# Copy suite documentation to base directory
echo "📋 Copying suite documentation..."
cp README_FINANCIAL_INSTITUTIONS.md "$BASE_DIR/" 2>/dev/null || echo "  ⚠️  README_FINANCIAL_INSTITUTIONS.md not found"
cp QUICK_REFERENCE_G-SIBs.md "$BASE_DIR/" 2>/dev/null || echo "  ⚠️  QUICK_REFERENCE_G-SIBs.md not found"
cp FINANCIAL_PRODUCTS_SUMMARY.md "$BASE_DIR/" 2>/dev/null || echo "  ⚠️  FINANCIAL_PRODUCTS_SUMMARY.md not found"
cp PRODUCT_INDEX.md "$BASE_DIR/" 2>/dev/null || echo "  ⚠️  PRODUCT_INDEX.md not found"
echo "✅ Suite documentation copied"
echo ""

# Create main suite README in base directory
cat > "$BASE_DIR/README.md" << 'EOF'
# Agentic AI Security Suite for Financial Institutions

> 10 Enterprise-Ready Products to Prevent Agentic AI Financial Disruption in 2026

## 🎯 Target Institutions

- JPMorgan Chase & Co.
- Morgan Stanley
- Bank of America
- Citigroup Inc.
- Goldman Sachs
- Wells Fargo
- U.S. Bancorp
- Other G-SIBs globally

## 📚 Documentation

- **[Main Documentation](README_FINANCIAL_INSTITUTIONS.md)** ⭐ - Comprehensive guide for G-SIBs
- **[Quick Reference](QUICK_REFERENCE_G-SIBs.md)** ⭐ - Executive summary
- **[Product Index](PRODUCT_INDEX.md)** - All 10 products overview

## 🛡️ The 10 Products

Each product has its own repository:

1. **[AgentGuard](agentguard/)** - Unified AI Agent Security & Governance
2. **[CodeShield AI](codeshield-ai/)** - Secure Development Gateway
3. **[PaymentSentinel](paymentsentinel/)** - Real-Time Transaction Defense
4. **[LegacyBridge](legacybridge-ai-gateway/)** - Legacy Core Banking Protection
5. **[ModelWatch](modelwatch/)** - AI Model Integrity Monitoring
6. **[FleetCommand](fleetcommand/)** - Multi-Agent Orchestration
7. **[PromptShield](promptshield/)** - Customer-Facing Agent Protection
8. **[IdentityVault](identityvault-agents/)** - Non-Human IAM Platform
9. **[SupplyChainGuard](supplychainguard/)** - Development Tool Security
10. **[ComplianceIQ](complianceiq/)** - Regulatory Reporting & Governance

## 🚀 Getting Started

1. Review the [Main Documentation](README_FINANCIAL_INSTITUTIONS.md)
2. Explore individual product repositories
3. Schedule an executive briefing
4. Request a technical assessment

## 📞 Contact

- **Enterprise Sales**: [Contact Information]
- **Technical Assessment**: [Contact Information]
- **Regulatory Advisory**: [Contact Information]

---

**Purpose-Built for G-SIBs. Enterprise-Ready. Regulatory-Compliant.**
EOF

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📦 Created 10 separate repositories:"
echo ""
for i in "${!REPO_NAMES[@]}"; do
    repo_name="${REPO_NAMES[$i]}"
    product_name="${PRODUCT_NAMES[$i]}"
    echo "  ✅ $repo_name - $product_name"
done
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Next Steps:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Create GitHub repositories (one for each product):"
echo ""
for product_key in "${!PRODUCTS[@]}"; do
    IFS='|' read -r product_name product_tagline repo_name <<< "${PRODUCTS[$product_key]}"
    echo "   - $repo_name"
done
echo ""
echo "   Go to: https://github.com/new"
echo "   For each repo:"
echo "   - Name: [repo-name]"
echo "   - Description: [product tagline]"
echo "   - DO NOT initialize with README, .gitignore, or license"
echo ""
echo "2. Push each repository:"
echo ""
echo "   cd $BASE_DIR/[repo-name]"
echo "   git remote add origin https://github.com/YOUR_USERNAME/[repo-name].git"
echo "   git commit -m 'Initial commit: [Product Name]'"
echo "   git push -u origin main"
echo ""
echo "3. Configure each repository on GitHub:"
echo "   - Add topics: financial-services, ai-security, banking, [product-specific]"
echo "   - Update description"
echo "   - Pin product-specification.md"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

