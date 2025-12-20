#!/usr/bin/env python3
"""
Create GitHub Lists for organizing repositories by category.

GitHub Lists are used to organize starred repositories on your profile.
This script creates lists and adds your repositories to them.
"""

import os
import sys
import requests
import json
from typing import List, Dict

# GitHub API base URL
GITHUB_API_BASE = "https://api.github.com"

def get_headers():
    """Get headers for GitHub API requests."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ Error: GITHUB_TOKEN environment variable not set")
        print("Set it with: export GITHUB_TOKEN=ghp_your_token_here")
        sys.exit(1)
    
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

def get_username():
    """Get GitHub username from environment or API."""
    username = os.getenv("GITHUB_USERNAME")
    if not username:
        # Try to get from API
        headers = get_headers()
        response = requests.get(f"{GITHUB_API_BASE}/user", headers=headers)
        if response.status_code == 200:
            return response.json()["login"]
        else:
            print("❌ Error: Could not determine GitHub username")
            print("Set it with: export GITHUB_USERNAME=your-username")
            sys.exit(1)
    return username

def get_user_repos(username: str) -> List[Dict]:
    """Get all repositories for a user."""
    headers = get_headers()
    repos = []
    page = 1
    per_page = 100
    
    print(f"📦 Fetching repositories for {username}...")
    
    while True:
        url = f"{GITHUB_API_BASE}/users/{username}/repos"
        params = {"page": page, "per_page": per_page, "sort": "updated"}
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"❌ Error fetching repos: {response.status_code}")
            print(response.text)
            break
        
        page_repos = response.json()
        if not page_repos:
            break
        
        repos.extend(page_repos)
        print(f"  Found {len(page_repos)} repos (total: {len(repos)})")
        
        if len(page_repos) < per_page:
            break
        page += 1
    
    return repos

def create_list(name: str, description: str = "") -> Dict:
    """
    Create a GitHub List.
    Note: GitHub Lists API might be limited. This attempts to create via API.
    """
    headers = get_headers()
    username = get_username()
    
    # GitHub Lists API endpoint (if available)
    # Note: GitHub Lists might need to be created manually via UI
    # This is an attempt to use the API
    
    url = f"{GITHUB_API_BASE}/user/lists"
    data = {
        "name": name,
        "description": description
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"✅ Created list: {name}")
        return response.json()
    elif response.status_code == 404:
        print(f"⚠️  GitHub Lists API might not be available")
        print(f"   You may need to create lists manually at:")
        print(f"   https://github.com/{username}?tab=stars")
        return None
    else:
        print(f"⚠️  Could not create list via API: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def add_repo_to_list(list_id: str, repo_full_name: str):
    """Add a repository to a list."""
    headers = get_headers()
    url = f"{GITHUB_API_BASE}/user/lists/{list_id}/repos/{repo_full_name}"
    
    response = requests.put(url, headers=headers)
    
    if response.status_code == 204:
        print(f"  ✅ Added {repo_full_name} to list")
        return True
    else:
        print(f"  ⚠️  Could not add {repo_full_name}: {response.status_code}")
        return False

def main():
    """Main function to create lists and organize repositories."""
    username = get_username()
    print(f"🚀 Creating GitHub Lists for {username}\n")
    
    # Get all repositories
    repos = get_user_repos(username)
    print(f"\n📊 Found {len(repos)} total repositories\n")
    
    # Define lists and their repository patterns
    lists_config = {
        "⚛️ Quantum Fun": {
            "description": "Interactive quantum computing demos",
            "patterns": [
                "quantum-coin-demo",
                "quantum-twins-demo",
                "grover-search-demo",
                "quantum-randomness-demo",
                "quantum-teleportation-demo",
                "quantum-noise-demo",
                "quantum-art-generator"
            ]
        },
        "💰 Financial Toolbox": {
            "description": "Enterprise AI security products for financial institutions",
            "patterns": [
                "agentguard",
                "codeshield-ai",
                "paymentsentinel",
                "legacybridge",
                "modelwatch",
                "fleetcommand",
                "promptshield",
                "identityvault",
                "supplychainguard",
                "complianceiq"
            ]
        },
        "🎵 Music & Audio": {
            "description": "DDSP-Piano and audio synthesis projects",
            "patterns": [
                "ddsp-piano",
                "ddsp",
                "piano",
                "audio",
                "synthesis",
                "maestro"
            ]
        },
        "🛠️ Community Tools": {
            "description": "Open-source engineering and DevOps tools",
            "patterns": [
                "pr-summarizer",
                "meeting-action",
                "postmortem",
                "feature-flag",
                "roadmap",
                "dead-link",
                "api-rate-limit",
                "github-star",
                "env-manager",
                "git-hook",
                "quick-scaffold",
                "mock-api",
                "task-run"
            ]
        },
        "🚀 Other Projects": {
            "description": "Other specialized projects and tools",
            "patterns": [
                "strategyforge",
                "identity-studio",
                "sap-whisper",
                "calypso"
            ]
        }
    }
    
    # Create lists and organize repos
    print("=" * 70)
    print("CREATING LISTS AND ORGANIZING REPOSITORIES")
    print("=" * 70)
    print()
    
    for list_name, config in lists_config.items():
        print(f"\n📋 Processing: {list_name}")
        print(f"   Description: {config['description']}")
        
        # Try to create list (might need manual creation)
        list_obj = create_list(list_name, config['description'])
        
        # Find matching repositories
        matching_repos = []
        for repo in repos:
            repo_name_lower = repo["name"].lower()
            for pattern in config["patterns"]:
                if pattern.lower() in repo_name_lower:
                    matching_repos.append(repo)
                    break
        
        print(f"   Found {len(matching_repos)} matching repositories:")
        for repo in matching_repos:
            print(f"     - {repo['full_name']}")
        
        # If list was created, add repos to it
        if list_obj and "id" in list_obj:
            for repo in matching_repos:
                add_repo_to_list(list_obj["id"], repo["full_name"])
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("\n⚠️  NOTE: GitHub Lists API might be limited.")
    print("   If lists were not created automatically, you can:")
    print("   1. Go to: https://github.com/{username}?tab=stars")
    print("   2. Click 'New list' to create lists manually")
    print("   3. Add repositories to lists by starring them and selecting the list")
    print()
    print("📝 Repository organization:")
    for list_name, config in lists_config.items():
        matching_count = sum(
            1 for repo in repos
            if any(pattern.lower() in repo["name"].lower() for pattern in config["patterns"])
        )
        print(f"   {list_name}: {matching_count} repositories")

if __name__ == "__main__":
    main()

