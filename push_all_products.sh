#!/bin/bash

# Script to push all 10 products to GitHub repositories

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Array of products and their GitHub URLs
declare -A products=(
    ["api-rate-limit-monitor"]="https://github.com/yksanjo/RateGuard.git"
    ["code-review-time-tracker"]="https://github.com/yksanjo/ReviewClock.git"
    ["saas-churn-predictor"]="https://github.com/yksanjo/ChurnGuard.git"
    ["email-warmup-service"]="https://github.com/yksanjo/WarmUp.git"
    ["github-star-notifier"]="https://github.com/yksanjo/StarAlert-.git"
    ["invoice-reminder-bot"]="https://github.com/yksanjo/InvoiceBot.git"
    ["domain-expiration-monitor"]="https://github.com/yksanjo/DomainWatch.git"
    ["competitor-price-tracker"]="https://github.com/yksanjo/PriceWatch.git"
    ["social-media-scheduler"]="https://github.com/yksanjo/SocialQueue.git"
    ["dead-link-checker"]="https://github.com/yksanjo/LinkCheck.git"
)

echo -e "${BLUE}🚀 Pushing all 10 products to GitHub...${NC}\n"

# Function to push a single product
push_product() {
    local dir=$1
    local repo_url=$2
    
    echo -e "${BLUE}📦 Processing: ${dir}${NC}"
    
    if [ ! -d "$dir" ]; then
        echo -e "${RED}❌ Directory ${dir} not found, skipping...${NC}\n"
        return 1
    fi
    
    cd "$dir" || return 1
    
    # Initialize git if not already initialized
    if [ ! -d ".git" ]; then
        echo "  Initializing git repository..."
        git init
    fi
    
    # Add all files
    git add .
    
    # Check if there are changes to commit
    if git diff --staged --quiet && git diff --quiet; then
        echo -e "  ${BLUE}⚠️  No changes to commit${NC}"
    else
        # Commit changes
        git commit -m "Initial commit: $(basename $dir)"
        echo -e "  ${GREEN}✅ Committed changes${NC}"
    fi
    
    # Add remote if not exists, or update it
    if git remote | grep -q "^origin$"; then
        git remote set-url origin "$repo_url"
    else
        git remote add origin "$repo_url"
    fi
    
    # Push to GitHub
    echo "  Pushing to GitHub..."
    if git push -u origin main 2>/dev/null || git push -u origin master 2>/dev/null; then
        echo -e "  ${GREEN}✅ Successfully pushed to GitHub${NC}\n"
    else
        echo -e "  ${RED}❌ Failed to push. You may need to set the default branch:${NC}"
        echo -e "     ${BLUE}git branch -M main${NC}"
        echo -e "     ${BLUE}git push -u origin main${NC}\n"
    fi
    
    cd ..
}

# Push each product
for dir in "${!products[@]}"; do
    push_product "$dir" "${products[$dir]}"
done

echo -e "${GREEN}✨ Done! All products processed.${NC}"
echo -e "\n${BLUE}📝 Note: If any pushes failed, you may need to:${NC}"
echo -e "   1. Set the default branch: ${BLUE}git branch -M main${NC}"
echo -e "   2. Push manually: ${BLUE}git push -u origin main${NC}"







