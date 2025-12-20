#!/bin/bash

# Script to create and push Oracle tools repos to GitHub
# Usage: ./create_oracle_tools_repos.sh

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# GitHub username (update this)
GITHUB_USER="${GITHUB_USER:-yourusername}"

# List of repos to create
REPOS=(
    "oracle-license-optimizer"
    "oracle-performance-analyzer"
    "oracle-cloud-cost-optimizer"
    "oracle-postgres-migrator"
    "oracle-security-auditor"
)

echo -e "${BLUE}Creating Oracle Tools Repositories${NC}"
echo "=================================="
echo ""

# Function to create and push a repo
create_repo() {
    local repo_name=$1
    local repo_path="./${repo_name}"
    
    echo -e "${YELLOW}Processing: ${repo_name}${NC}"
    
    if [ ! -d "$repo_path" ]; then
        echo -e "${YELLOW}  Directory not found: ${repo_path}${NC}"
        return
    fi
    
    cd "$repo_path"
    
    # Initialize git if not already
    if [ ! -d ".git" ]; then
        git init
        echo -e "${GREEN}  ✓ Initialized git repository${NC}"
    fi
    
    # Add all files
    git add .
    
    # Check if there are changes
    if git diff --staged --quiet; then
        echo -e "${YELLOW}  No changes to commit${NC}"
    else
        git commit -m "Initial commit: ${repo_name}"
        echo -e "${GREEN}  ✓ Committed changes${NC}"
    fi
    
    # Create GitHub repo (requires gh CLI)
    if command -v gh &> /dev/null; then
        # Check if repo already exists
        if gh repo view "${GITHUB_USER}/${repo_name}" &> /dev/null; then
            echo -e "${YELLOW}  Repository already exists on GitHub${NC}"
        else
            gh repo create "${repo_name}" --public --source=. --remote=origin --push
            echo -e "${GREEN}  ✓ Created and pushed to GitHub${NC}"
        fi
    else
        echo -e "${YELLOW}  GitHub CLI (gh) not found. Please create repo manually:${NC}"
        echo -e "    https://github.com/new?name=${repo_name}"
        echo -e "    Then run: git remote add origin https://github.com/${GITHUB_USER}/${repo_name}.git"
        echo -e "    Then run: git push -u origin main"
    fi
    
    cd ..
    echo ""
}

# Process each repo
for repo in "${REPOS[@]}"; do
    create_repo "$repo"
done

echo -e "${GREEN}Done!${NC}"
echo ""
echo "Next steps:"
echo "1. Update GITHUB_USER variable in this script"
echo "2. Install GitHub CLI: brew install gh (or apt-get install gh)"
echo "3. Authenticate: gh auth login"
echo "4. Run this script again to push to GitHub"
echo ""
echo "Or manually create repos at: https://github.com/new"

