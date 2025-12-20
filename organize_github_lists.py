#!/usr/bin/env python3
"""
Organize repositories into GitHub Lists automatically.
This script adds repositories to the appropriate lists based on their names.
"""

import os
import sys
import requests
import json
import time
from typing import List, Dict, Optional

GITHUB_API_BASE = "https://api.github.com"

def get_headers():
    """Get headers for GitHub API requests."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ Error: GITHUB_TOKEN environment variable not set")
        sys.exit(1)
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

def get_username():
    """Get GitHub username."""
    username = os.getenv("GITHUB_USERNAME", "yksanjo")
    return username

def get_user_lists(username: str) -> List[Dict]:
    """Get all lists for a user."""
    headers = get_headers()
    
    # Try to get lists - GitHub Lists API might be limited
    # This is an experimental endpoint
    url = f"{GITHUB_API_BASE}/user/lists"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print("⚠️  GitHub Lists API endpoint not available")
            print("   Lists may need to be managed manually via the web interface")
            return []
        else:
            print(f"⚠️  Could not fetch lists: {response.status_code}")
            return []
    except Exception as e:
        print(f"⚠️  Error fetching lists: {e}")
        return []

def get_user_repos(username: str) -> List[Dict]:
    """Get all repositories for a user."""
    headers = get_headers()
    repos = []
    page = 1
    
    print(f"📦 Fetching repositories for {username}...")
    
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

def star_repository(repo_full_name: str) -> bool:
    """Star a repository."""
    headers = get_headers()
    url = f"{GITHUB_API_BASE}/user/starred/{repo_full_name}"
    
    response = requests.put(url, headers=headers)
    
    if response.status_code == 204:
        return True
    elif response.status_code == 304:
        # Already starred
        return True
    else:
        return False

def add_repo_to_list(list_id: str, repo_full_name: str) -> bool:
    """Add a repository to a list."""
    headers = get_headers()
    
    # GitHub Lists API endpoint
    url = f"{GITHUB_API_BASE}/user/lists/{list_id}/repos/{repo_full_name}"
    
    response = requests.put(url, headers=headers)
    
    if response.status_code == 204:
        return True
    elif response.status_code == 404:
        # List or repo not found, or API not available
        return False
    else:
        return False

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
            "patterns": ["ddsp", "piano", "audio", "synthesis", "maestro", "music", "strudel", "drum"],
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
    
    return categories

def main():
    """Main function to organize repositories into lists."""
    username = get_username()
    headers = get_headers()
    
    print("=" * 70)
    print("GITHUB LISTS ORGANIZER")
    print("=" * 70)
    print()
    
    # Get user lists
    print("📋 Fetching your GitHub Lists...")
    lists = get_user_lists(username)
    
    if not lists:
        print("\n⚠️  Could not fetch lists via API.")
        print("   This might mean:")
        print("   1. Lists API is not available")
        print("   2. Lists need to be created manually first")
        print()
        print("   Creating a manual organization report instead...")
        print()
        
        # Fall back to manual organization report
        repos = get_user_repos(username)
        categories = categorize_repos(repos)
        
        print("=" * 70)
        print("REPOSITORY ORGANIZATION REPORT")
        print("=" * 70)
        print()
        print("Use this to manually organize your repositories:")
        print()
        
        for category, data in categories.items():
            repos_list = data["repos"]
            print(f"{category}: {len(repos_list)} repositories")
            print("-" * 70)
            
            for repo in sorted(repos_list, key=lambda x: x["name"]):
                print(f"  ⭐ {repo['full_name']}")
                print(f"     https://github.com/{repo['full_name']}")
            print()
        
        print("=" * 70)
        print("MANUAL STEPS")
        print("=" * 70)
        print()
        print("1. Go to: https://github.com/yksanjo?tab=stars")
        print("2. For each repository above:")
        print("   a. Make sure it's starred")
        print("   b. Click the list icon (📋) next to the star")
        print("   c. Select the appropriate list(s)")
        print()
        return
    
    # Create a mapping of list names to list IDs
    list_map = {}
    for lst in lists:
        list_map[lst.get("name", "")] = lst.get("id")
    
    print(f"✅ Found {len(lists)} lists:")
    for lst in lists:
        print(f"   - {lst.get('name', 'Unknown')} (ID: {lst.get('id')})")
    print()
    
    # Get all repositories
    repos = get_user_repos(username)
    print(f"📦 Found {len(repos)} repositories\n")
    
    # Categorize repositories
    categories = categorize_repos(repos)
    
    print("=" * 70)
    print("ORGANIZING REPOSITORIES")
    print("=" * 70)
    print()
    
    total_added = 0
    total_starred = 0
    
    for category, data in categories.items():
        repos_list = data["repos"]
        
        # Find matching list
        list_id = None
        for list_name, lid in list_map.items():
            if category in list_name or list_name in category:
                list_id = lid
                break
        
        if not list_id:
            print(f"⚠️  List '{category}' not found. Skipping...")
            print(f"   Repositories that would go here:")
            for repo in repos_list:
                print(f"     - {repo['full_name']}")
            print()
            continue
        
        print(f"📋 Processing: {category}")
        print(f"   List ID: {list_id}")
        print(f"   Repositories: {len(repos_list)}")
        print()
        
        for repo in repos_list:
            repo_full_name = repo["full_name"]
            
            # Star the repository first
            if star_repository(repo_full_name):
                total_starred += 1
                print(f"  ⭐ Starred: {repo_full_name}")
            else:
                print(f"  ⚠️  Could not star: {repo_full_name}")
            
            # Add to list
            if add_repo_to_list(list_id, repo_full_name):
                total_added += 1
                print(f"  ✅ Added to list: {repo_full_name}")
            else:
                print(f"  ⚠️  Could not add to list: {repo_full_name}")
            
            # Small delay to avoid rate limiting
            time.sleep(0.5)
        
        print()
    
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✅ Starred: {total_starred} repositories")
    print(f"✅ Added to lists: {total_added} repositories")
    print()
    print("Check your lists at: https://github.com/yksanjo?tab=stars")
    print()

if __name__ == "__main__":
    main()

