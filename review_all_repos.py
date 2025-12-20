#!/usr/bin/env python3
"""
Comprehensive GitHub Repository Reviewer
Reviews all repositories and suggests/makes improvements.
"""

import os
import sys
import json
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime
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


class RepoReviewer:
    """Review and improve GitHub repositories."""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None, username: Optional[str] = None):
        """Initialize reviewer."""
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.username = username or os.getenv("GITHUB_USERNAME")
        
        if not self.token:
            print("❌ Error: GITHUB_TOKEN environment variable is required")
            print("   Get one at: https://github.com/settings/tokens")
            sys.exit(1)
        
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.token}"
        }
        
        # Get username if not provided
        if not self.username:
            try:
                user_data = self._make_request("GET", "/user")
                self.username = user_data.get("login")
                print(f"✅ Authenticated as: {self.username}")
            except Exception as e:
                print(f"❌ Failed to authenticate: {e}")
                sys.exit(1)
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a request to GitHub API."""
        url = f"{self.BASE_URL}{endpoint}"
        custom_headers = kwargs.pop('headers', {})
        merged_headers = {**self.headers, **custom_headers}
        response = requests.request(method, url, headers=merged_headers, **kwargs)
        
        if response.status_code == 401:
            raise Exception("Authentication failed. Check your GitHub token.")
        elif response.status_code == 403:
            raise Exception("Forbidden. Check token permissions or rate limit.")
        
        response.raise_for_status()
        return response.json() if response.content else {}
    
    def list_all_repos(self, include_forks: bool = False) -> List[Dict[str, Any]]:
        """List all repositories for the user."""
        repos = []
        page = 1
        per_page = 100
        
        print(f"📡 Fetching repositories for {self.username}...")
        
        while True:
            params = {
                "per_page": per_page,
                "page": page,
                "type": "all" if include_forks else "owner",
                "sort": "updated",
                "direction": "desc"
            }
            
            try:
                response = requests.get(
                    f"{self.BASE_URL}/user/repos",
                    headers=self.headers,
                    params=params
                )
                response.raise_for_status()
                page_repos = response.json()
                
                if not page_repos:
                    break
                
                repos.extend(page_repos)
                print(f"   Fetched {len(repos)} repositories so far...")
                
                if len(page_repos) < per_page:
                    break
                
                page += 1
            except Exception as e:
                print(f"❌ Error fetching repositories: {e}")
                break
        
        print(f"✅ Found {len(repos)} repositories\n")
        return repos
    
    def analyze_repo(self, repo: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a repository and identify improvements."""
        full_name = repo["full_name"]
        name = repo["name"]
        
        analysis = {
            "full_name": full_name,
            "name": name,
            "issues": [],
            "suggestions": [],
            "needs_update": False,
            "last_updated": repo.get("updated_at"),
            "has_readme": False,
            "has_description": bool(repo.get("description")),
            "has_topics": len(repo.get("topics", [])) > 0,
            "has_license": bool(repo.get("license")),
            "has_badges": False,
            "language": repo.get("language", "Unknown"),
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "open_issues": repo.get("open_issues_count", 0),
            "archived": repo.get("archived", False),
            "private": repo.get("private", False)
        }
        
        # Skip archived repos
        if analysis["archived"]:
            analysis["issues"].append("Repository is archived")
            return analysis
        
        # Check for README
        try:
            readme_data = self._make_request("GET", f"/repos/{full_name}/readme")
            analysis["has_readme"] = True
            readme_content = readme_data.get("content", "")
            if readme_content:
                import base64
                decoded = base64.b64decode(readme_content).decode("utf-8")
                analysis["has_badges"] = "img.shields.io" in decoded or "badge" in decoded.lower()
        except:
            analysis["issues"].append("No README.md found")
            analysis["suggestions"].append("Add a README.md file")
        
        # Check description
        if not analysis["has_description"]:
            analysis["issues"].append("No repository description")
            analysis["suggestions"].append("Add a repository description")
        
        # Check topics
        if not analysis["has_topics"]:
            analysis["issues"].append("No repository topics/tags")
            analysis["suggestions"].append("Add repository topics for better discoverability")
        
        # Check for badges in README
        if analysis["has_readme"] and not analysis["has_badges"]:
            analysis["suggestions"].append("Add badges to README for better presentation")
        
        # Check for license
        if not analysis["has_license"]:
            analysis["suggestions"].append("Consider adding a LICENSE file")
        
        # Check last update (if older than 6 months, suggest update)
        if analysis["last_updated"]:
            last_update = datetime.fromisoformat(analysis["last_updated"].replace("Z", "+00:00"))
            days_since_update = (datetime.now(last_update.tzinfo) - last_update).days
            if days_since_update > 180:
                analysis["issues"].append(f"Last updated {days_since_update} days ago")
                analysis["suggestions"].append("Consider updating dependencies and documentation")
        
        # Determine if needs update
        analysis["needs_update"] = (
            not analysis["has_readme"] or
            not analysis["has_description"] or
            not analysis["has_topics"] or
            (analysis["has_readme"] and not analysis["has_badges"])
        )
        
        return analysis
    
    def improve_repo(self, repo_name: str, auto_apply: bool = False) -> bool:
        """Improve a repository using the automation tool."""
        try:
            github = GitHubRepoAutomation(token=self.token)
            
            # Get repo info
            owner, repo = repo_name.split("/")
            repo_info = github.get_repo_info(owner, repo)
            
            # Skip if archived
            if repo_info.get("archived"):
                print(f"   ⏭️  Skipping archived repository")
                return False
            
            improvements_made = []
            
            # Update description if missing
            if not repo_info.get("description"):
                suggested_desc = self._suggest_description(repo_info)
                if auto_apply and suggested_desc:
                    if github.update_description(owner, repo, suggested_desc):
                        improvements_made.append("description")
                else:
                    print(f"   💡 Suggested description: {suggested_desc}")
            
            # Update topics if missing
            if not repo_info.get("topics"):
                suggested_topics = self._suggest_topics(repo_info)
                if auto_apply and suggested_topics:
                    if github.update_topics(owner, repo, suggested_topics):
                        improvements_made.append("topics")
                else:
                    print(f"   💡 Suggested topics: {', '.join(suggested_topics)}")
            
            # Add badges to README
            readme_content = github.get_readme(owner, repo)
            if readme_content and "img.shields.io" not in readme_content:
                badge_gen = BadgeGenerator(owner, repo, repo_info)
                badges = badge_gen.generate_badges()
                
                if auto_apply:
                    updated_readme = ReadmeUpdater.add_badges_to_readme(readme_content, badges)
                    if updated_readme != readme_content:
                        if github.update_readme(owner, repo, updated_readme):
                            improvements_made.append("badges")
                else:
                    print(f"   💡 Would add {len(badges)} badges to README")
            
            if improvements_made:
                print(f"   ✅ Applied improvements: {', '.join(improvements_made)}")
                return True
            else:
                print(f"   ✓ Repository is up to date")
                return False
                
        except Exception as e:
            print(f"   ❌ Error improving repository: {e}")
            return False
    
    def _suggest_description(self, repo_info: Dict[str, Any]) -> str:
        """Suggest a description based on repo info."""
        name = repo_info.get("name", "")
        language = repo_info.get("language", "")
        topics = repo_info.get("topics", [])
        
        # Try to infer from name and topics
        if "cli" in topics or "command-line" in topics:
            return f"A command-line tool for {name.replace('-', ' ').replace('_', ' ')}"
        elif "api" in topics:
            return f"API for {name.replace('-', ' ').replace('_', ' ')}"
        elif "web" in topics or "frontend" in topics:
            return f"Web application: {name.replace('-', ' ').replace('_', ' ')}"
        else:
            return f"{name.replace('-', ' ').replace('_', ' ').title()} - {language or 'A'} project"
    
    def _suggest_topics(self, repo_info: Dict[str, Any]) -> List[str]:
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
        
        # Add common topics
        if not topics:
            topics = ["open-source"]
        
        return topics[:5]  # Limit to 5 topics
    
    def generate_report(self, analyses: List[Dict[str, Any]]) -> str:
        """Generate a summary report."""
        total = len(analyses)
        needs_update = sum(1 for a in analyses if a["needs_update"] and not a["archived"])
        archived = sum(1 for a in analyses if a["archived"])
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║           GitHub Repository Review Report                    ║
╚══════════════════════════════════════════════════════════════╝

📊 Summary:
   Total repositories: {total}
   Need updates: {needs_update}
   Archived: {archived}
   Up to date: {total - needs_update - archived}

📋 Repositories needing attention:
"""
        
        for analysis in analyses:
            if analysis["archived"]:
                continue
            
            if analysis["needs_update"]:
                report += f"\n   📦 {analysis['full_name']}\n"
                if analysis["issues"]:
                    for issue in analysis["issues"]:
                        report += f"      ⚠️  {issue}\n"
                if analysis["suggestions"]:
                    for suggestion in analysis["suggestions"]:
                        report += f"      💡 {suggestion}\n"
        
        return report


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Review and improve all GitHub repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--auto-apply",
        action="store_true",
        help="Automatically apply improvements (default: dry-run)"
    )
    parser.add_argument(
        "--username",
        help="GitHub username (default: auto-detect from token)"
    )
    parser.add_argument(
        "--include-forks",
        action="store_true",
        help="Include forked repositories"
    )
    parser.add_argument(
        "--repo",
        help="Review only a specific repository (format: owner/repo)"
    )
    
    args = parser.parse_args()
    
    print("🚀 GitHub Repository Reviewer")
    print("=" * 60 + "\n")
    
    reviewer = RepoReviewer(username=args.username)
    
    if args.repo:
        # Review single repo
        print(f"📦 Reviewing repository: {args.repo}\n")
        repo_info = reviewer._make_request("GET", f"/repos/{args.repo}")
        analysis = reviewer.analyze_repo(repo_info)
        
        print(f"Repository: {analysis['full_name']}")
        print(f"Language: {analysis['language']}")
        print(f"Stars: {analysis['stars']}, Forks: {analysis['forks']}")
        print(f"Last updated: {analysis['last_updated']}\n")
        
        if analysis["issues"]:
            print("Issues found:")
            for issue in analysis["issues"]:
                print(f"  ⚠️  {issue}")
        
        if analysis["suggestions"]:
            print("\nSuggestions:")
            for suggestion in analysis["suggestions"]:
                print(f"  💡 {suggestion}")
        
        if analysis["needs_update"]:
            print(f"\n{'🔧 Applying improvements...' if args.auto_apply else '💡 Run with --auto-apply to apply improvements'}")
            if args.auto_apply:
                reviewer.improve_repo(args.repo, auto_apply=True)
    else:
        # Review all repos
        repos = reviewer.list_all_repos(include_forks=args.include_forks)
        
        if not repos:
            print("No repositories found.")
            return
        
        print("🔍 Analyzing repositories...\n")
        analyses = []
        
        for i, repo in enumerate(repos, 1):
            full_name = repo["full_name"]
            print(f"[{i}/{len(repos)}] {full_name}")
            
            analysis = reviewer.analyze_repo(repo)
            analyses.append(analysis)
            
            if analysis["needs_update"] and not analysis["archived"]:
                if args.auto_apply:
                    reviewer.improve_repo(full_name, auto_apply=True)
                else:
                    print(f"   ⚠️  Needs updates (run with --auto-apply to fix)")
            
            print()
        
        # Generate report
        report = reviewer.generate_report(analyses)
        print(report)
        
        # Save report to file
        report_file = "repo_review_report.txt"
        with open(report_file, "w") as f:
            f.write(report)
        print(f"\n📄 Full report saved to: {report_file}")


if __name__ == "__main__":
    main()

