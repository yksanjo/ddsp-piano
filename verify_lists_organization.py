#!/usr/bin/env python3
"""
Verify and provide quick links for organizing GitHub Lists.
Generates clickable links and verification checklist.
"""

import os
import sys
import requests
from typing import List, Dict

GITHUB_API_BASE = "https://api.github.com"
USERNAME = "yksanjo"

def get_headers():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return None
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

def get_user_repos(username: str) -> List[Dict]:
    """Get all repositories for a user."""
    headers = get_headers()
    if not headers:
        return []
    
    repos = []
    page = 1
    
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
                "supplychainguard", "complianceiq"
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
            "patterns": ["strategyforge", "identity-studio", "sap-whisper"],
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
    """Generate organization report with clickable links."""
    print("=" * 80)
    print("GITHUB LISTS ORGANIZATION VERIFICATION")
    print("=" * 80)
    print()
    
    repos = get_user_repos(USERNAME)
    if not repos:
        print("⚠️  Could not fetch repositories. Make sure GITHUB_TOKEN is set.")
        return
    
    categories = categorize_repos(repos)
    
    print(f"📊 Found {len(repos)} total repositories")
    print()
    print("=" * 80)
    print("ORGANIZATION BY LIST")
    print("=" * 80)
    print()
    
    total_repos = 0
    
    for category, data in categories.items():
        repos_list = data["repos"]
        total_repos += len(repos_list)
        
        print(f"{category}")
        print("─" * 80)
        print(f"Total: {len(repos_list)} repositories")
        print()
        print("Quick Actions:")
        print(f"  1. Go to: https://github.com/{USERNAME}?tab=stars")
        print(f"  2. Find or create list: {category}")
        print(f"  3. Add these repositories:")
        print()
        
        for i, repo in enumerate(sorted(repos_list, key=lambda x: x["name"]), 1):
            repo_name = repo["name"]
            repo_full_name = repo["full_name"]
            repo_url = f"https://github.com/{repo_full_name}"
            
            print(f"  {i:2d}. {repo_name}")
            print(f"      🔗 {repo_url}")
            print(f"      ⭐ Star & add to list: {repo_url}")
            print()
        
        print()
    
    print("=" * 80)
    print("VERIFICATION CHECKLIST")
    print("=" * 80)
    print()
    print("After organizing, verify:")
    print()
    print(f"  ✅ ⚛️ Quantum Fun: {len(categories['⚛️ Quantum Fun']['repos'])} repos")
    print(f"  ✅ 💰 Financial Toolbox: {len(categories['💰 Financial Toolbox']['repos'])} repos")
    print(f"  ✅ 🎵 Music & Audio: {len(categories['🎵 Music & Audio']['repos'])} repos")
    print(f"  ✅ 🛠️ Community Tools: {len(categories['🛠️ Community Tools']['repos'])} repos")
    print(f"  ✅ 🚀 Other Projects: {len(categories['🚀 Other Projects']['repos'])} repos")
    print()
    print(f"Total organized: {total_repos} repositories")
    print()
    print("=" * 80)
    print("QUICK LINKS")
    print("=" * 80)
    print()
    print(f"📋 Your Lists: https://github.com/{USERNAME}?tab=stars")
    print(f"👤 Your Profile: https://github.com/{USERNAME}")
    print()
    
    # Generate a summary file
    summary_file = "LISTS_ORGANIZATION_SUMMARY.txt"
    with open(summary_file, "w") as f:
        f.write("=" * 80 + "\n")
        f.write("GITHUB LISTS ORGANIZATION SUMMARY\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Generated for: {USERNAME}\n")
        f.write(f"Total repositories: {len(repos)}\n")
        f.write(f"Total to organize: {total_repos}\n\n")
        
        for category, data in categories.items():
            repos_list = data["repos"]
            f.write(f"{category}: {len(repos_list)} repositories\n")
            f.write("-" * 80 + "\n")
            for repo in sorted(repos_list, key=lambda x: x["name"]):
                f.write(f"  - {repo['full_name']}\n")
            f.write("\n")
    
    print(f"✅ Summary saved to: {summary_file}")
    print()

if __name__ == "__main__":
    main()

