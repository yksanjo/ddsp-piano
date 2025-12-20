#!/bin/bash

# Script to push all 10 product repositories to existing GitHub repos
# Repositories already exist at: https://github.com/yksanjo/[repo-name]

set -e

BASE_DIR="./financial-products-repos"
GITHUB_USERNAME="yksanjo"

# Repository names matching your GitHub repos
REPOS=(
    "agentguard"
    "codeshield-ai"
    "paymentsentinel"
    "legacybridge-ai-gateway"
    "modelwatch"
    "fleetcommand"
    "promptshield"
    "identityvault-agents"
    "supplychainguard"
    "complianceiq"
)

echo "🚀 Pushing all repositories to GitHub..."
echo "GitHub User: $GITHUB_USERNAME"
echo ""

# Copy missing product files
echo "📋 Checking for missing product specifications..."
if [ -f "product-1-agentguard.md" ]; then
    cp product-1-agentguard.md "$BASE_DIR/agentguard/product-specification.md" 2>/dev/null && echo "  ✅ Copied product-1-agentguard.md"
fi
if [ -f "product-4-legacybridge-ai-gateway.md" ]; then
    cp product-4-legacybridge-ai-gateway.md "$BASE_DIR/legacybridge-ai-gateway/product-specification.md" 2>/dev/null && echo "  ✅ Copied product-4-legacybridge-ai-gateway.md"
fi
if [ -f "product-8-identityvault-agents.md" ]; then
    cp product-8-identityvault-agents.md "$BASE_DIR/identityvault-agents/product-specification.md" 2>/dev/null && echo "  ✅ Copied product-8-identityvault-agents.md"
fi
echo ""

# Function to push a repo
push_repo() {
    local repo_name=$1
    local repo_dir="$BASE_DIR/$repo_name"
    
    if [ ! -d "$repo_dir" ]; then
        echo "⚠️  Directory not found: $repo_dir"
        return
    fi
    
    echo "📦 Pushing: $repo_name"
    cd "$repo_dir"
    
    # Rename branch to main if needed
    if git branch | grep -q "master"; then
        git branch -m master main 2>/dev/null || true
    fi
    
    # Check if git is initialized
    if [ ! -d ".git" ]; then
        echo "  ⚠️  Git not initialized, initializing..."
        git init
        git branch -M main
        git add .
    fi
    
    # Add all files
    git add . 2>/dev/null || true
    
    # Check if remote exists
    if git remote | grep -q "^origin$"; then
        echo "  ✅ Remote already configured"
        git remote set-url origin "https://github.com/$GITHUB_USERNAME/$repo_name.git"
    else
        echo "  🔗 Adding remote..."
        git remote add origin "https://github.com/$GITHUB_USERNAME/$repo_name.git"
    fi
    
    # Commit if there are changes
    if [ -n "$(git status --porcelain)" ] || [ -z "$(git log --oneline 2>/dev/null)" ]; then
        echo "  💾 Committing changes..."
        product_name=$(grep '^# ' README.md | head -1 | sed 's/# //' || echo "$repo_name")
        git commit -m "Initial commit: $product_name

- Product specification and documentation
- README with quick start guide
- Complete product details for financial institutions" 2>/dev/null || \
        git commit -m "Initial commit: $repo_name" 2>/dev/null || true
    else
        echo "  ✅ Already committed"
    fi
    
    # Push
    echo "  📤 Pushing to GitHub..."
    if git push -u origin main 2>&1; then
        echo "  ✅ Successfully pushed"
        echo "  🔗 https://github.com/$GITHUB_USERNAME/$repo_name"
    else
        # Try with force if needed (for empty repos)
        echo "  ⚠️  Standard push failed, trying force push..."
        if git push -u origin main --force 2>&1; then
            echo "  ✅ Successfully pushed (force)"
            echo "  🔗 https://github.com/$GITHUB_USERNAME/$repo_name"
        else
            echo "  ❌ Push failed"
            echo "  💡 Check repository exists: https://github.com/$GITHUB_USERNAME/$repo_name"
        fi
    fi
    
    cd - > /dev/null
    echo ""
}

# Push all repositories
for repo_name in "${REPOS[@]}"; do
    push_repo "$repo_name"
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Push Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Summary - All repositories:"
echo ""
for repo_name in "${REPOS[@]}"; do
    echo "  🔗 https://github.com/$GITHUB_USERNAME/$repo_name"
done
echo ""




