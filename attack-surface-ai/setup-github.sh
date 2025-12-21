#!/bin/bash

# Setup script for pushing attack-surface-ai to GitHub
# Usage: ./setup-github.sh <your-github-username>

if [ -z "$1" ]; then
    echo "Usage: ./setup-github.sh <your-github-username>"
    echo "Example: ./setup-github.sh yksanjo"
    exit 1
fi

GITHUB_USER=$1
REPO_NAME="attack-surface-ai"

echo "🚀 Setting up GitHub repository for $REPO_NAME"
echo ""
echo "Step 1: Create a new repository on GitHub"
echo "   Go to: https://github.com/new"
echo "   Repository name: $REPO_NAME"
echo "   Description: AI-native Attack Surface Intelligence platform"
echo "   Visibility: Choose Public or Private"
echo "   DO NOT initialize with README, .gitignore, or license"
echo ""
read -p "Press Enter after you've created the repository on GitHub..."

echo ""
echo "Step 2: Adding remote and pushing..."
git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git" 2>/dev/null || git remote set-url origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
git push -u origin main

echo ""
echo "✅ Done! Your repository is now at:"
echo "   https://github.com/$GITHUB_USER/$REPO_NAME"

