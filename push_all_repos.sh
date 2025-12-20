#!/bin/bash

# Script to push all 10 product repositories to GitHub
# Requires: Repositories already created on GitHub

set -e

# Check for GitHub username
if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ Error: GITHUB_USERNAME environment variable not set"
    echo "Set it with: export GITHUB_USERNAME=your-username"
    exit 1
fi

BASE_DIR="./financial-products-repos"

if [ ! -d "$BASE_DIR" ]; then
    echo "❌ Error: $BASE_DIR not found"
    echo "Run ./setup_10_separate_repos.sh first"
    exit 1
fi

echo "🚀 Pushing all repositories to GitHub..."
echo "GitHub User: $GITHUB_USERNAME"
echo ""

# Repository names
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
    
    # Check if git is initialized
    if [ ! -d ".git" ]; then
        echo "  ⚠️  Git not initialized, initializing..."
        git init
        git branch -M main
        git add .
    fi
    
    # Check if remote exists
    if git remote | grep -q "^origin$"; then
        echo "  ✅ Remote already configured"
    else
        echo "  🔗 Adding remote..."
        git remote add origin "https://github.com/$GITHUB_USERNAME/$repo_name.git"
    fi
    
    # Commit if there are changes
    if [ -n "$(git status --porcelain)" ]; then
        echo "  💾 Committing changes..."
        git add .
        git commit -m "Initial commit: $(grep '^# ' README.md | head -1 | sed 's/# //')" || \
        git commit -m "Initial commit: $repo_name"
    else
        echo "  ✅ No changes to commit"
    fi
    
    # Push
    echo "  📤 Pushing to GitHub..."
    if git push -u origin main 2>&1; then
        echo "  ✅ Successfully pushed"
        echo "  🔗 https://github.com/$GITHUB_USERNAME/$repo_name"
    else
        echo "  ⚠️  Push failed (repository may not exist on GitHub)"
        echo "  💡 Create it first: https://github.com/new?name=$repo_name"
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
echo "📋 Summary:"
echo ""
for repo_name in "${REPOS[@]}"; do
    echo "  🔗 https://github.com/$GITHUB_USERNAME/$repo_name"
done
echo ""




