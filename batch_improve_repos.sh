#!/bin/bash
# Batch improvement script for GitHub repositories
# This script uses the github-repo-automation tool to improve multiple repositories

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if GITHUB_TOKEN is set
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}❌ Error: GITHUB_TOKEN environment variable is not set${NC}"
    echo "   Set it with: export GITHUB_TOKEN=ghp_your_token_here"
    exit 1
fi

# Check if github-repo-automation.py exists
AUTOMATION_SCRIPT="github-repo-automation/github-repo-automation.py"
if [ ! -f "$AUTOMATION_SCRIPT" ]; then
    echo -e "${RED}❌ Error: $AUTOMATION_SCRIPT not found${NC}"
    exit 1
fi

# List of repositories to improve
# Add your repositories here
REPOS=(
    "yksanjo/task-run"
    "yksanjo/env-manager"
    "yksanjo/mock-api-gen"
    "yksanjo/quick-scaffold"
    "yksanjo/git-hook-setup"
    "yksanjo/github-repo-automation"
    "yksanjo/meeting-action-extractor"
    "yksanjo/postmortem-generator"
    "yksanjo/pr-summarizer"
    "yksanjo/feature-flag-auditor"
    "yksanjo/roadmap-dashboard"
)

# Check if --dry-run flag is passed
DRY_RUN=false
if [ "$1" == "--dry-run" ]; then
    DRY_RUN=true
    echo -e "${YELLOW}🔍 DRY RUN MODE - No changes will be made${NC}\n"
fi

echo -e "${GREEN}🚀 Batch Repository Improvement Tool${NC}"
echo "=========================================="
echo ""

TOTAL=${#REPOS[@]}
SUCCESS=0
FAILED=0
SKIPPED=0

for i in "${!REPOS[@]}"; do
    REPO="${REPOS[$i]}"
    NUM=$((i + 1))
    
    echo -e "${YELLOW}[$NUM/$TOTAL] Processing: $REPO${NC}"
    
    if [ "$DRY_RUN" = true ]; then
        python3 "$AUTOMATION_SCRIPT" --repo "$REPO" --dry-run || {
            echo -e "${RED}   ❌ Failed${NC}"
            FAILED=$((FAILED + 1))
            continue
        }
    else
        python3 "$AUTOMATION_SCRIPT" --repo "$REPO" || {
            echo -e "${RED}   ❌ Failed${NC}"
            FAILED=$((FAILED + 1))
            continue
        }
        SUCCESS=$((SUCCESS + 1))
    fi
    
    echo ""
done

echo "=========================================="
echo -e "${GREEN}✅ Summary:${NC}"
echo "   Total: $TOTAL"
if [ "$DRY_RUN" = false ]; then
    echo -e "   ${GREEN}Success: $SUCCESS${NC}"
    echo -e "   ${RED}Failed: $FAILED${NC}"
else
    echo -e "   ${YELLOW}Dry-run completed${NC}"
fi
echo ""








