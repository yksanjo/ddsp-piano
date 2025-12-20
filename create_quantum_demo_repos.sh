#!/bin/bash

# Script to create GitHub repositories for quantum demo projects
# Requires: GITHUB_TOKEN and GITHUB_USERNAME environment variables

set -e

# Check for GitHub token
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: GITHUB_TOKEN environment variable not set"
    echo ""
    echo "To get a token:"
    echo "1. Go to: https://github.com/settings/tokens"
    echo "2. Generate new token (classic)"
    echo "3. Select scope: repo (full control)"
    echo "4. Set token: export GITHUB_TOKEN=ghp_your_token_here"
    exit 1
fi

# Get GitHub username
if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ Error: GITHUB_USERNAME environment variable not set"
    echo "Set it with: export GITHUB_USERNAME=your-username"
    exit 1
fi

echo "🚀 Creating Quantum Demo GitHub Repositories..."
echo "GitHub User: $GITHUB_USERNAME"
echo ""

# Quantum demo configurations
declare -A DEMOS=(
    ["quantum-coin-demo"]="Quantum Coin Demo|Interactive superposition demonstration - heads AND tails simultaneously"
    ["quantum-twins-demo"]="Quantum Twins Demo|Entanglement visualization - instant correlation across any distance"
    ["grover-search-demo"]="Grover Search Demo|Quantum search algorithm - faster than classical search"
    ["quantum-randomness-demo"]="Quantum Randomness Demo|True randomness generation for security applications"
    ["quantum-teleportation-demo"]="Quantum Teleportation Demo|Teleport quantum information without physical transfer"
    ["quantum-noise-demo"]="Quantum Noise Demo|Compare perfect simulator vs noisy real quantum hardware"
    ["quantum-art-generator"]="Quantum Art Generator|Generate unique art and music from quantum measurements"
)

# Topics for all repos
TOPICS="quantum-computing,education,demo,interactive,react,quantum-mechanics,quantum-physics,visualization,teaching,stem"

# Function to create a GitHub repo
create_repo() {
    local repo_name=$1
    local demo_name=$2
    local description=$3
    
    echo "📦 Creating: $repo_name"
    
    # Check if repo already exists
    response=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        "https://api.github.com/repos/$GITHUB_USERNAME/$repo_name")
    
    if [ "$response" = "200" ]; then
        echo "  ⚠️  Repository already exists, skipping..."
        return
    fi
    
    # Create repository
    response=$(curl -s -w "\n%{http_code}" \
        -X POST \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        -H "Content-Type: application/json" \
        -d "{
            \"name\": \"$repo_name\",
            \"description\": \"$description\",
            \"private\": false,
            \"has_issues\": true,
            \"has_projects\": false,
            \"has_wiki\": false,
            \"auto_init\": false
        }" \
        "https://api.github.com/user/repos")
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "201" ]; then
        echo "  ✅ Repository created successfully"
        
        # Add topics
        echo "  📌 Adding topics..."
        curl -s -X PUT \
            -H "Authorization: token $GITHUB_TOKEN" \
            -H "Accept: application/vnd.github.mercy-preview+json" \
            -H "Content-Type: application/json" \
            -d "{\"names\": [$(echo $TOPICS | sed 's/,/","/g' | sed 's/^/"/' | sed 's/$/"/')]}" \
            "https://api.github.com/repos/$GITHUB_USERNAME/$repo_name/topics" > /dev/null
        
        echo "  ✅ Topics added"
        echo "  🔗 https://github.com/$GITHUB_USERNAME/$repo_name"
    else
        echo "  ❌ Failed to create repository"
        echo "  Response: $body"
    fi
    echo ""
}

# Create all repositories
for repo_name in "${!DEMOS[@]}"; do
    IFS='|' read -r demo_name description <<< "${DEMOS[$repo_name]}"
    create_repo "$repo_name" "$demo_name" "$description"
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ All quantum demo repositories created!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Create standalone projects for each demo:"
echo "   ./setup_quantum_demos.sh"
echo ""
echo "2. Push code to each repository:"
echo "   ./push_quantum_demos.sh"
echo ""



