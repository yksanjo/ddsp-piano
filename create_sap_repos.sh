#!/bin/bash

# Script to create GitHub repos for all SAP tools
# Requires GITHUB_TOKEN environment variable

GITHUB_TOKEN=${GITHUB_TOKEN:?"GITHUB_TOKEN environment variable is required"}
GITHUB_USER="yksanjo"

REPOS=(
    "sap-whisper:AI-Powered Natural Language Interface for SAP"
    "sap-transaction-finder:Find SAP transaction codes instantly"
    "sap-license-optimizer:Optimize SAP license costs and usage"
    "sap-cost-calculator:Calculate true SAP total cost of ownership"
    "sap-data-extractor:Extract SAP data to CSV, Excel, or JSON"
    "sap-performance-analyzer:Monitor and optimize SAP system performance"
    "sap-migration-assistant:Plan and execute migrations from SAP"
    "sap-user-activity-monitor:Monitor SAP user activity and license usage"
    "sap-report-generator:Generate custom SAP reports with templates"
)

echo "🚀 Creating GitHub repositories for SAP tools..."
echo ""

for repo_info in "${REPOS[@]}"; do
    IFS=':' read -r repo_name repo_desc <<< "$repo_info"
    
    echo "📦 Creating: $repo_name"
    
    # Create repo on GitHub
    curl -X POST \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        https://api.github.com/user/repos \
        -d "{\"name\":\"$repo_name\",\"description\":\"$repo_desc\",\"private\":false}" \
        > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "  ✅ Repository created"
    else
        echo "  ⚠️  Repository may already exist or error occurred"
    fi
    
    # Initialize git and push
    if [ -d "$repo_name" ]; then
        cd "$repo_name"
        
        # Add .gitignore if missing
        if [ ! -f .gitignore ]; then
            cat > .gitignore <<EOF
__pycache__/
*.py[cod]
*$py.class
.env
*.log
.DS_Store
EOF
        fi
        
        # Add requirements.txt if missing and Python files exist
        if [ ! -f requirements.txt ] && [ -f *.py ]; then
            echo "flask==3.0.0" > requirements.txt
        fi
        
        git init > /dev/null 2>&1
        git add . > /dev/null 2>&1
        git commit -m "Initial commit: $repo_desc" > /dev/null 2>&1
        git branch -M main > /dev/null 2>&1
        git remote add origin "https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${repo_name}.git" > /dev/null 2>&1
        git push -u origin main > /dev/null 2>&1
        
        if [ $? -eq 0 ]; then
            echo "  ✅ Code pushed to GitHub"
        else
            echo "  ⚠️  Push may have failed"
        fi
        
        cd ..
    fi
    
    echo ""
done

echo "✅ All repositories created!"
echo ""
echo "📋 Repository list:"
for repo_info in "${REPOS[@]}"; do
    IFS=':' read -r repo_name repo_desc <<< "$repo_info"
    echo "  - https://github.com/${GITHUB_USER}/${repo_name}"
done

