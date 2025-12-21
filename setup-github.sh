#!/bin/bash

# Script to set up GitHub repository for a product
# Usage: ./setup-github.sh <product-name> <description>

set -e

PRODUCT_NAME=$1
DESCRIPTION=$2
GITHUB_USERNAME=${GITHUB_USERNAME:-"your-username"}

if [ -z "$PRODUCT_NAME" ]; then
  echo "Error: Product name required"
  echo "Usage: ./setup-github.sh <product-name> <description>"
  exit 1
fi

if [ -z "$DESCRIPTION" ]; then
  DESCRIPTION="Security product for SMBs"
fi

PRODUCT_DIR="$PRODUCT_NAME"

if [ ! -d "$PRODUCT_DIR" ]; then
  echo "Error: Directory $PRODUCT_DIR does not exist"
  exit 1
fi

cd "$PRODUCT_DIR"

echo "🚀 Setting up GitHub repository for $PRODUCT_NAME..."

# Check if git is already initialized
if [ -d ".git" ]; then
  echo "⚠️  Git repository already initialized"
  read -p "Continue anyway? (y/n) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
else
  git init
  echo "✅ Git repository initialized"
fi

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: $PRODUCT_NAME - $DESCRIPTION" || {
  echo "⚠️  No changes to commit (or commit already exists)"
}

# Set up remote
REMOTE_URL="https://github.com/$GITHUB_USERNAME/$PRODUCT_NAME.git"

if git remote | grep -q "^origin$"; then
  echo "⚠️  Remote 'origin' already exists"
  read -p "Update remote URL? (y/n) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    git remote set-url origin "$REMOTE_URL"
    echo "✅ Remote URL updated"
  fi
else
  git remote add origin "$REMOTE_URL"
  echo "✅ Remote added: $REMOTE_URL"
fi

# Set default branch
git branch -M main

echo ""
echo "📋 Next steps:"
echo "1. Create repository on GitHub: https://github.com/new"
echo "   - Name: $PRODUCT_NAME"
echo "   - Description: $DESCRIPTION"
echo "   - Do NOT initialize with README"
echo ""
echo "2. Push to GitHub:"
echo "   cd $PRODUCT_DIR"
echo "   git push -u origin main"
echo ""
echo "3. Add topics on GitHub:"
echo "   - security"
echo "   - typescript"
echo "   - nextjs"
echo "   - [product-specific topics]"
echo ""

read -p "Push to GitHub now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  git push -u origin main || {
    echo "❌ Push failed. Make sure:"
    echo "   1. Repository exists on GitHub"
    echo "   2. You have push access"
    echo "   3. GitHub credentials are configured"
  }
fi

echo "✅ Setup complete!"

