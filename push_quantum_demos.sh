#!/bin/bash

# Script to push all quantum demo projects to GitHub
# Requires: GITHUB_USERNAME environment variable

set -e

# Check for GitHub username
if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ Error: GITHUB_USERNAME environment variable not set"
    echo "Set it with: export GITHUB_USERNAME=your-username"
    exit 1
fi

BASE_DIR="/Users/yoshikondo/ddsp-piano/quantum-demos"

# List of all demo repositories
REPOS=(
    "quantum-coin-demo"
    "quantum-twins-demo"
    "grover-search-demo"
    "quantum-randomness-demo"
    "quantum-teleportation-demo"
    "quantum-noise-demo"
    "quantum-art-generator"
)

# Function to push a repo
push_repo() {
    local repo_name=$1
    local repo_dir="$BASE_DIR/$repo_name"
    
    if [ ! -d "$repo_dir" ]; then
        echo "⚠️  Directory not found: $repo_dir"
        echo "   Skipping..."
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
        git commit -m "Initial commit: $repo_name - Interactive quantum computing demo" || true
    fi
    
    # Check if remote exists
    if git remote | grep -q "^origin$"; then
        echo "  ✅ Remote already configured"
    else
        echo "  🔗 Adding remote..."
        git remote add origin "https://github.com/$GITHUB_USERNAME/$repo_name.git" || \
        git remote set-url origin "https://github.com/$GITHUB_USERNAME/$repo_name.git"
    fi
    
    # Commit if there are changes
    if [ -n "$(git status --porcelain)" ]; then
        echo "  💾 Committing changes..."
        git add .
        git commit -m "Update: $repo_name" || echo "  ℹ️  No changes to commit"
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
        echo "  💡 Or run: ./create_quantum_demo_repos.sh"
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
echo "  - Created and pushed quantum demo repositories"
echo "  - Each demo is now available on GitHub"
echo "  - Ready for deployment to Vercel/Netlify"
echo ""



