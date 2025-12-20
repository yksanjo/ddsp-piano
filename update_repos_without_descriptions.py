#!/usr/bin/env python3
"""
Update GitHub repositories that don't have descriptions.
Uses the github-repo-automation tool to add descriptions, topics, and badges.
"""

import os
import sys
import requests
from typing import List, Dict, Any, Optional
from pathlib import Path

# Import from github-repo-automation
automation_path = Path(__file__).parent / "github-repo-automation" / "github-repo-automation.py"
sys.path.insert(0, str(automation_path.parent))
import importlib.util
spec = importlib.util.spec_from_file_location("github_repo_automation", automation_path)
github_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(github_module)
GitHubRepoAutomation = github_module.GitHubRepoAutomation
BadgeGenerator = github_module.BadgeGenerator
ReadmeUpdater = github_module.ReadmeUpdater


def list_repos_without_descriptions(token: Optional[str] = None, username: Optional[str] = None, include_forks: bool = False) -> List[Dict[str, Any]]:
    """List all repositories that don't have descriptions."""
    BASE_URL = "https://api.github.com"
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    if token:
        headers["Authorization"] = f"token {token}"
    
    repos = []
    page = 1
    per_page = 100
    
    print("📡 Fetching repositories...")
    
    # Determine endpoint
    if token:
        endpoint = f"{BASE_URL}/user/repos"
        params = {
            "per_page": per_page,
            "page": page,
            "type": "all" if include_forks else "owner",
            "sort": "updated",
            "direction": "desc"
        }
    elif username:
        endpoint = f"{BASE_URL}/users/{username}/repos"
        params = {
            "per_page": per_page,
            "page": page,
            "type": "all" if include_forks else "owner",
            "sort": "updated",
            "direction": "desc"
        }
    else:
        raise ValueError("Either token or username must be provided")
    
    while True:
        try:
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            page_repos = response.json()
            
            if not page_repos:
                break
            
            # Filter repos without descriptions
            for repo in page_repos:
                if not repo.get("description") and not repo.get("archived"):
                    repos.append(repo)
            
            print(f"   Checked {len(page_repos)} repositories, found {len(repos)} without descriptions...")
            
            if len(page_repos) < per_page:
                break
            
            page += 1
            params["page"] = page
        except Exception as e:
            print(f"❌ Error fetching repositories: {e}")
            break
    
    print(f"✅ Found {len(repos)} repositories without descriptions\n")
    return repos


def suggest_description(repo_info: Dict[str, Any]) -> str:
    """Suggest a description based on repo info."""
    name = repo_info.get("name", "")
    language = repo_info.get("language", "")
    topics = repo_info.get("topics", [])
    
    # Clean up name
    clean_name = name.replace("-", " ").replace("_", " ").title()
    name_lower = name.lower()
    
    # Specific descriptions for known repo patterns
    descriptions = {
        "linkcheck": "🔍 Check and monitor broken links in your projects, websites, or documentation. Automated link validation tool.",
        "socialqueue": "📱 Social media content scheduler and queue management tool. Plan and automate your social media posts.",
        "pricewatch": "💰 Price monitoring and tracking tool. Get alerts when prices change for products you're watching.",
        "domainwatch": "🌐 Domain expiration monitor. Track domain expiration dates and receive alerts before domains expire.",
        "invoicebot": "🧾 Automated invoice reminder bot. Send payment reminders and track invoice status.",
        "staralert": "⭐ GitHub star notification bot. Get notified when your repositories receive new stars.",
        "warmup": "📧 Email warmup service. Gradually increase email sending volume to improve deliverability.",
        "churnguard": "📊 SaaS churn prediction and monitoring tool. Identify at-risk customers and prevent churn.",
        "reviewclock": "⏱️ Code review time tracker. Monitor and analyze code review turnaround times.",
        "rateguard": "🛡️ API rate limit monitor. Track and alert on API rate limit usage across services.",
        "diff-focus": "🎯 Focus on what matters in code reviews. Highlight important changes and filter noise in diffs.",
        "fastpass-review": "⚡ FastPass code review optimizer. Streamline and accelerate your code review process.",
    }
    
    # Check for exact matches first
    for key, desc in descriptions.items():
        if key in name_lower:
            return desc
    
    # Try to infer from name and topics
    if "cli" in topics or "command-line" in topics or "cli" in name_lower:
        return f"🚀 A command-line tool for {clean_name.lower()}"
    elif "api" in topics or "api" in name_lower:
        return f"🌐 API for {clean_name.lower()}"
    elif "web" in topics or "frontend" in topics or "web" in name_lower:
        return f"💻 Web application: {clean_name.lower()}"
    elif "automation" in topics or "automation" in name_lower:
        return f"⚙️ Automation tool for {clean_name.lower()}"
    elif "monitor" in name_lower or "tracker" in name_lower or "watch" in name_lower:
        return f"📊 Monitoring and tracking tool: {clean_name.lower()}"
    elif "bot" in name_lower:
        return f"🤖 Bot for {clean_name.lower()}"
    elif "check" in name_lower:
        return f"🔍 {clean_name} - Validation and checking tool"
    elif language:
        return f"🔧 {clean_name} - {language} project"
    else:
        return f"📦 {clean_name} - Open source project"


def suggest_topics(repo_info: Dict[str, Any]) -> List[str]:
    """Suggest topics based on repo info."""
    topics = []
    language = repo_info.get("language", "").lower()
    name = repo_info.get("name", "").lower()
    
    # Add language
    if language:
        topics.append(language)
    
    # Infer from name
    if "cli" in name or "command" in name:
        topics.append("cli")
    if "api" in name:
        topics.append("api")
    if "web" in name or "frontend" in name:
        topics.append("web")
    if "automation" in name:
        topics.append("automation")
    if "tool" in name:
        topics.append("tools")
    if "monitor" in name or "tracker" in name:
        topics.append("monitoring")
    if "bot" in name:
        topics.append("bot")
    if "github" in name:
        topics.append("github")
    
    # Add common topics
    if not topics:
        topics = ["open-source"]
    
    return topics[:8]  # Limit to 8 topics


def update_repo(repo: Dict[str, Any], token: Optional[str], dry_run: bool = False) -> bool:
    """Update a repository with description, topics, and badges."""
    full_name = repo["full_name"]
    owner, repo_name = full_name.split("/")
    
    print(f"\n📦 Processing: {full_name}")
    
    if not token and not dry_run:
        print(f"   ⚠️  Skipping: Token required for updates")
        return False
    
    try:
        github = GitHubRepoAutomation(token=token)
        
        # Get current repo info
        repo_info = github.get_repo_info(owner, repo_name)
        
        improvements = []
        
        # Update description
        suggested_desc = suggest_description(repo_info)
        if dry_run:
            print(f"   💡 Would add description: {suggested_desc}")
        else:
            if github.update_description(owner, repo_name, suggested_desc):
                improvements.append("description")
        
        # Update topics
        suggested_topics = suggest_topics(repo_info)
        if dry_run:
            print(f"   💡 Would add topics: {', '.join(suggested_topics)}")
        else:
            if github.update_topics(owner, repo_name, suggested_topics):
                improvements.append("topics")
        
        # Add badges to README
        readme_content = github.get_readme(owner, repo_name)
        if readme_content:
            if "img.shields.io" not in readme_content:
                badge_gen = BadgeGenerator(owner, repo_name, repo_info)
                badges = badge_gen.generate_badges()
                
                if dry_run:
                    print(f"   💡 Would add {len(badges)} badges to README")
                else:
                    updated_readme = ReadmeUpdater.add_badges_to_readme(readme_content, badges)
                    if updated_readme != readme_content:
                        if github.update_readme(owner, repo_name, updated_readme):
                            improvements.append("badges")
            else:
                print(f"   ✓ README already has badges")
        else:
            print(f"   ℹ️  No README found (badges will be added when README is created)")
        
        if improvements:
            print(f"   ✅ Applied improvements: {', '.join(improvements)}")
            return True
        else:
            print(f"   ✓ Repository updated")
            return True
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Update GitHub repositories without descriptions",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    parser.add_argument(
        "--include-forks",
        action="store_true",
        help="Include forked repositories"
    )
    parser.add_argument(
        "--token",
        help="GitHub personal access token (or set GITHUB_TOKEN env var)"
    )
    parser.add_argument(
        "--username",
        help="GitHub username (for listing public repos without token)"
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip confirmation prompt and proceed automatically"
    )
    
    args = parser.parse_args()
    
    token = args.token or os.getenv("GITHUB_TOKEN")
    username = args.username or os.getenv("GITHUB_USERNAME", "yksanjo")
    
    # For updates, token is required
    if not args.dry_run and not token:
        print("❌ Error: GITHUB_TOKEN environment variable is required for updates")
        print("   Get one at: https://github.com/settings/tokens")
        print("   Then run: export GITHUB_TOKEN=ghp_your_token_here")
        print("\n   Note: You can use --dry-run with --username to preview changes")
        sys.exit(1)
    
    print("🚀 GitHub Repository Updater")
    print("=" * 60)
    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made\n")
    else:
        if not token:
            print("❌ Error: Token required for updates")
            sys.exit(1)
        print("⚠️  LIVE MODE - Changes will be applied\n")
    
    # List repos without descriptions
    repos = list_repos_without_descriptions(token=token, username=username, include_forks=args.include_forks)
    
    if not repos:
        print("✨ All repositories have descriptions! Nothing to update.")
        return
    
    print(f"Found {len(repos)} repositories without descriptions:\n")
    for repo in repos:
        print(f"  - {repo['full_name']}")
    
    if args.dry_run:
        print(f"\n🔍 Preview mode - showing what would be updated:\n")
    else:
        if args.yes:
            print(f"\n✅ Proceeding with updating {len(repos)} repositories...\n")
        else:
            try:
                response = input(f"\n⚠️  Proceed with updating {len(repos)} repositories? (yes/no): ")
                if response.lower() not in ["yes", "y"]:
                    print("Cancelled.")
                    return
            except EOFError:
                # Non-interactive mode, proceed if --yes flag is set
                if not args.yes:
                    print("\n⚠️  Non-interactive mode detected. Use --yes flag to proceed without confirmation.")
                    return
                print(f"\n✅ Proceeding with updating {len(repos)} repositories...\n")
    
    # Update each repo
    print("\n" + "=" * 60)
    print("🔄 Updating repositories...\n")
    
    updated = 0
    failed = 0
    
    for i, repo in enumerate(repos, 1):
        print(f"[{i}/{len(repos)}]")
        if update_repo(repo, token, dry_run=args.dry_run):
            updated += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"✨ Done!")
    print(f"   Updated: {updated}")
    print(f"   Failed: {failed}")
    print(f"   Total: {len(repos)}")


if __name__ == "__main__":
    main()


