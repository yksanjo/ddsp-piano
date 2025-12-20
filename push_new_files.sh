#!/bin/bash

# Script to push new files to all 10 repositories

set -e

BASE_DIR="./financial-products-repos"
GITHUB_USERNAME="yksanjo"

# Files to add to each repo
NEW_FILES=(
    "CURSOR_AI_PROMPTS_COMPLETE.md"
    "EXECUTIVE_BRIEF.md"
    "ASSESSMENT_FOR_BANKERS.md"
)

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

echo "🚀 Pushing new files to all repositories..."
echo ""

# Function to push files to a repo
push_files() {
    local repo_name=$1
    local repo_dir="$BASE_DIR/$repo_name"
    
    if [ ! -d "$repo_dir" ]; then
        echo "⚠️  Directory not found: $repo_dir"
        return
    fi
    
    echo "📦 Updating: $repo_name"
    cd "$repo_dir"
    
    # Check if git is initialized
    if [ ! -d ".git" ]; then
        echo "  ⚠️  Git not initialized"
        cd - > /dev/null
        return
    fi
    
    # Copy new files from base directory if they exist
    for file in "${NEW_FILES[@]}"; do
        if [ -f "../$file" ]; then
            cp "../$file" . 2>/dev/null && echo "  ✅ Added $file"
        fi
    done
    
    # Add all files
    git add . 2>/dev/null || true
    
    # Check if there are changes
    if [ -n "$(git status --porcelain)" ]; then
        echo "  💾 Committing changes..."
        git commit -m "Add executive documentation and Cursor AI prompts

- Executive Brief for C-Suite
- Assessment for Bankers
- Complete Cursor AI prompts for all 10 products" 2>/dev/null || \
        git commit -m "Update documentation" 2>/dev/null || true
    else
        echo "  ✅ No changes to commit"
    fi
    
    # Push
    echo "  📤 Pushing to GitHub..."
    if git push origin main 2>&1; then
        echo "  ✅ Successfully pushed"
    else
        echo "  ⚠️  Push failed or no changes"
    fi
    
    cd - > /dev/null
    echo ""
}

# Push to all repositories
for repo_name in "${REPOS[@]}"; do
    push_files "$repo_name"
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Push Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""



