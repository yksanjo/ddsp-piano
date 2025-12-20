#!/usr/bin/env python3
"""
List repositories by category to help organize GitHub Lists.
This script shows which repositories belong in which list.
"""

import os
import sys
import requests
from typing import List, Dict

GITHUB_API_BASE = "https://api.github.com"

def get_headers():
    """Get headers for GitHub API requests."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ Error: GITHUB_TOKEN environment variable not set")
        sys.exit(1)
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

def get_user_repos(username: str) -> List[Dict]:
    """Get all repositories for a user."""
    headers = get_headers()
    repos = []
    page = 1
    
    print(f"📦 Fetching repositories for {username}...\n")
    
    while True:
        url = f"{GITHUB_API_BASE}/users/{username}/repos"
        params = {"page": page, "per_page": 100, "sort": "updated"}
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            break
        
        page_repos = response.json()
        if not page_repos:
            break
        
        repos.extend(page_repos)
        if len(page_repos) < 100:
            break
        page += 1
    
    return repos

def categorize_repos(repos: List[Dict]) -> Dict[str, List[Dict]]:
    """Categorize repositories by patterns."""
    
    categories = {
        "⚛️ Quantum Fun": {
            "patterns": ["quantum"],
            "repos": []
        },
        "💰 Financial Toolbox": {
            "patterns": [
                "agentguard", "codeshield", "paymentsentinel", "legacybridge",
                "modelwatch", "fleetcommand", "promptshield", "identityvault",
                "supplychainguard", "complianceiq", "financial"
            ],
            "repos": []
        },
        "🎵 Music & Audio": {
            "patterns": ["ddsp", "piano", "audio", "synthesis", "maestro", "music"],
            "repos": []
        },
        "🛠️ Community Tools": {
            "patterns": [
                "pr-summarizer", "meeting-action", "postmortem", "feature-flag",
                "roadmap", "dead-link", "api-rate", "github-star", "env-manager",
                "git-hook", "scaffold", "mock-api", "task-run", "code-review"
            ],
            "repos": []
        },
        "🚀 Other Projects": {
            "patterns": ["strategyforge", "identity-studio", "sap-whisper", "calypso"],
            "repos": []
        }
    }
    
    for repo in repos:
        repo_name_lower = repo["name"].lower()
        added = False
        
        for category, data in categories.items():
            if not added:
                for pattern in data["patterns"]:
                    if pattern.lower() in repo_name_lower:
                        data["repos"].append(repo)
                        added = True
                        break
        
        # If not categorized, add to "Other"
        if not added:
            if "other" not in categories:
                categories["📦 Uncategorized"] = {"patterns": [], "repos": []}
            categories["📦 Uncategorized"]["repos"].append(repo)
    
    return categories

def main():
    """Main function."""
    username = os.getenv("GITHUB_USERNAME", "yksanjo")
    
    print("=" * 70)
    print("GITHUB REPOSITORY CATEGORIZATION")
    print("=" * 70)
    print()
    
    repos = get_user_repos(username)
    print(f"Found {len(repos)} total repositories\n")
    
    categories = categorize_repos(repos)
    
    print("=" * 70)
    print("REPOSITORIES BY CATEGORY")
    print("=" * 70)
    print()
    
    for category, data in categories.items():
        repos_list = data["repos"]
        print(f"{category}: {len(repos_list)} repositories")
        print("-" * 70)
        
        if repos_list:
            for repo in sorted(repos_list, key=lambda x: x["name"]):
                print(f"  ⭐ {repo['full_name']}")
                print(f"     {repo.get('description', 'No description') or 'No description'}")
                print(f"     🔗 https://github.com/{repo['full_name']}")
                print()
        else:
            print("  (No repositories found)")
        
        print()
    
    print("=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print()
    print("1. Go to: https://github.com/yksanjo?tab=stars")
    print("2. Create new lists for each category above")
    print("3. Star each repository and add it to the appropriate list(s)")
    print("4. See GITHUB_LISTS_GUIDE.md for detailed instructions")
    print()

if __name__ == "__main__":
    main()

