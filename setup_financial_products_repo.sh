#!/bin/bash

# Setup Script for Financial Products Repository
# This script prepares all files for a new GitHub repository

set -e

echo "🚀 Setting up Financial Products Repository..."
echo ""

# Configuration
REPO_NAME="agentic-ai-security-suite"
TARGET_DIR="./financial-products-suite"

# Check if target directory exists
if [ -d "$TARGET_DIR" ]; then
    echo "⚠️  Directory $TARGET_DIR already exists."
    read -p "Do you want to remove it and start fresh? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$TARGET_DIR"
        echo "✅ Removed existing directory"
    else
        echo "❌ Exiting. Please remove $TARGET_DIR manually or choose a different name."
        exit 1
    fi
fi

# Create directory
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

echo "📁 Created directory: $TARGET_DIR"
echo ""

# Copy all financial product files
echo "📋 Copying files..."

# Main documentation files
cp ../README_FINANCIAL_INSTITUTIONS.md . 2>/dev/null || echo "⚠️  README_FINANCIAL_INSTITUTIONS.md not found"
cp ../QUICK_REFERENCE_G-SIBs.md . 2>/dev/null || echo "⚠️  QUICK_REFERENCE_G-SIBs.md not found"
cp ../FINANCIAL_PRODUCTS_SUMMARY.md . 2>/dev/null || echo "⚠️  FINANCIAL_PRODUCTS_SUMMARY.md not found"
cp ../PRODUCT_INDEX.md . 2>/dev/null || echo "⚠️  PRODUCT_INDEX.md not found"

# Product specification files
for i in {1..10}; do
    if [ -f "../product-$i-"*.md ]; then
        cp ../product-$i-*.md . 2>/dev/null || true
    fi
done

# Check if product-1 exists (might be named differently)
if [ -f "../product-1-agentguard.md" ]; then
    cp ../product-1-agentguard.md . 2>/dev/null || true
fi

echo "✅ Files copied"
echo ""

# Create main README.md
echo "📝 Creating main README.md..."

cat > README.md << 'EOF'
# Agentic AI Security Suite for Financial Institutions

> Enterprise-ready security platform to prevent agentic AI financial disruption in 2026

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-complete-brightgreen.svg)](README_FINANCIAL_INSTITUTIONS.md)

## 🎯 Target Institutions

This suite is designed specifically for **Global Systemically Important Banks (G-SIBs)**:

- **JPMorgan Chase & Co.**
- **Morgan Stanley**
- **Bank of America**
- **Citigroup Inc.**
- **Goldman Sachs**
- **Wells Fargo**
- **U.S. Bancorp**
- Other G-SIBs globally

## 📚 Documentation

### Quick Start
- **[Main Documentation](README_FINANCIAL_INSTITUTIONS.md)** ⭐ - Comprehensive guide for G-SIBs
- **[Quick Reference](QUICK_REFERENCE_G-SIBs.md)** ⭐ - Executive summary and ROI calculator
- **[Product Summary](FINANCIAL_PRODUCTS_SUMMARY.md)** - Complete documentation overview

### Product Index
- **[Product Index](PRODUCT_INDEX.md)** - All 10 products with implementation priorities

## 🛡️ The 10-Product Suite

### Foundation Layer (Deploy First)
1. **[AgentGuard](product-1-agentguard.md)** - Unified AI Agent Security & Governance
2. **[CodeShield AI](product-2-codeshield-ai.md)** - Secure Development Gateway
3. **[IdentityVault for Agents](product-8-identityvault-agents.md)** - Non-Human IAM Platform

### Operations Layer (Deploy Second)
4. **[PaymentSentinel](product-3-paymentsentinel.md)** - Real-Time Transaction Defense
5. **[LegacyBridge](product-4-legacybridge-ai-gateway.md)** - Legacy Core Banking Protection
6. **[PromptShield](product-7-promptshield.md)** - Customer-Facing Agent Protection

### Advanced Layer (Deploy Third)
7. **[ModelWatch](product-5-modelwatch.md)** - AI Model Integrity Monitoring
8. **[FleetCommand](product-6-fleetcommand.md)** - Multi-Agent Orchestration
9. **[SupplyChainGuard](product-9-supplychainguard.md)** - Development Tool Security
10. **[ComplianceIQ](product-10-complianceiq.md)** - Regulatory Reporting & Governance

## 💰 ROI Analysis

### Annual Value
- **Risk Prevention**: $34.6M+ (incidents, fines, attacks, corruption)
- **Operational Savings**: $1.08M-2.16M (exam prep, automation, efficiency)
- **Business Value**: $3.5M-10M (faster deployment, scaling, M&A)

**Total Annual ROI**: $39.18M-46.76M

**Investment**: $9M-18M annually

**Net ROI**: $21.18M-37.76M annually (2-4x return)

## 🚀 Implementation Roadmap

### Phase 1: Foundation (Months 1-3)
- AgentGuard, CodeShield AI, IdentityVault
- **Investment**: $2M-4M annually

### Phase 2: Operations (Months 4-6)
- PaymentSentinel, LegacyBridge, PromptShield
- **Investment**: Additional $3M-6M annually

### Phase 3: Advanced (Months 7-12)
- ModelWatch, FleetCommand, SupplyChainGuard, ComplianceIQ
- **Investment**: Additional $4M-8M annually

## 📋 Regulatory Alignment

| Regulator | Requirement | Product Solution |
|-----------|-------------|------------------|
| OCC | SR 11-7 (Model Risk) | ModelWatch |
| FCA | SS1/23 (AI Governance) | ComplianceIQ |
| ECB | Payment System Risk | PaymentSentinel |
| Fed | SR 11-7 | ModelWatch |
| FFIEC | Authentication Guidance | PromptShield |

## 🔗 Quick Links

- **For Executives**: Start with [README_FINANCIAL_INSTITUTIONS.md](README_FINANCIAL_INSTITUTIONS.md)
- **For Technical Teams**: Review individual product specifications
- **For Sales**: Use [QUICK_REFERENCE_G-SIBs.md](QUICK_REFERENCE_G-SIBs.md) for briefings

## 📞 Next Steps

1. **Review** the main documentation
2. **Schedule** executive briefing
3. **Request** technical assessment
4. **Begin** proof-of-concept discussion

## 📄 License

[Add your license here - MIT, Proprietary, etc.]

## 🤝 Contributing

This is a product specification repository. For inquiries:
- Enterprise Sales: [Contact Information]
- Technical Assessment: [Contact Information]
- Regulatory Advisory: [Contact Information]

---

**Purpose-Built for G-SIBs. Enterprise-Ready. Regulatory-Compliant.**
EOF

echo "✅ Created README.md"
echo ""

# Create .gitignore
echo "📝 Creating .gitignore..."

cat > .gitignore << 'EOF'
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

echo "✅ Created .gitignore"
echo ""

# Initialize git
echo "🔧 Initializing git repository..."

if [ ! -d ".git" ]; then
    git init
    git branch -M main
    echo "✅ Git initialized"
else
    echo "⚠️  Git already initialized"
fi

# Add all files
git add .

echo ""
echo "✅ All files staged"
echo ""

# Show status
echo "📊 Repository Status:"
echo ""
git status --short

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Create GitHub repository:"
echo "   https://github.com/new"
echo "   Name: $REPO_NAME"
echo "   Description: Enterprise-ready Agentic AI Security Suite for G-SIBs"
echo "   DO NOT initialize with README, .gitignore, or license"
echo ""
echo "2. Add remote and push:"
echo "   cd $TARGET_DIR"
echo "   git remote add origin https://github.com/YOUR_USERNAME/$REPO_NAME.git"
echo "   git commit -m 'Initial commit: Agentic AI Security Suite for Financial Institutions'"
echo "   git push -u origin main"
echo ""
echo "3. Configure repository on GitHub:"
echo "   - Add topics: financial-services, ai-security, banking, regulatory-compliance"
echo "   - Update description"
echo "   - Pin README_FINANCIAL_INSTITUTIONS.md"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""




