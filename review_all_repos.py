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
                
                # Check README quality
                readme_lower = decoded.lower()
                has_title = "# " in decoded or "## " in decoded
                has_description = len(decoded.split("\n")) > 5  # Has some content
                has_installation = "install" in readme_lower or "setup" in readme_lower or "getting started" in readme_lower
                has_usage = "usage" in readme_lower or "example" in readme_lower or "how to" in readme_lower
                
                if not has_title:
                    analysis["suggestions"].append("README should have a clear title (H1 heading)")
                if not has_description:
                    analysis["suggestions"].append("README should have a project description")
                if not has_installation:
                    analysis["suggestions"].append("README should include installation/setup instructions")
                if not has_usage:
                    analysis["suggestions"].append("README should include usage examples")
                    
                # Check for very short READMEs (likely placeholder)
                if len(decoded.strip()) < 200:
                    analysis["issues"].append("README is very short (likely a placeholder)")
                    analysis["suggestions"].append("Expand README with proper documentation")
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
            (analysis["has_readme"] and not analysis["has_badges"]) or
            len(analysis["suggestions"]) > 0
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
        """Suggest a description based on repo info with enhanced intelligence."""
        name = repo_info.get("name", "").lower()
        language = repo_info.get("language", "")
        topics = repo_info.get("topics", [])
        name_clean = name.replace('-', ' ').replace('_', ' ')
        
        # Known repository patterns and descriptions
        repo_patterns = {
            # Financial Products
            "agentguard": "Enterprise AI Agent Security & Governance Platform for Financial Institutions",
            "codeshield-ai": "Secure Development Gateway for AI-Generated Code in Banking Systems",
            "paymentsentinel": "Real-Time Transaction Defense System for Payment Processing",
            "legacybridge-ai-gateway": "Secure Integration Layer for Legacy Core Banking Systems",
            "modelwatch": "AI Integrity Monitoring Platform for Financial Services",
            "fleetcommand": "Multi-Agent Orchestration Platform for Enterprise AI Systems",
            "promptshield": "AI Agent Input Validation System for Secure Banking Applications",
            "identityvault-agents": "Non-Human Identity & Access Management for AI Agents",
            "supplychainguard": "AI Development Tool Security & Supply Chain Protection",
            "complianceiq": "AI Governance & Regulatory Reporting Suite for Financial Institutions",
            
            # Quantum Demos
            "quantum-coin-demo": "Quantum Superposition Demonstration - Flipping a Quantum Coin",
            "quantum-twins-demo": "Quantum Entanglement Visualization - The Quantum Twins Experiment",
            "grover-search-demo": "Grover's Quantum Search Algorithm Implementation",
            "quantum-randomness-demo": "True Quantum Randomness Generation from Quantum Measurements",
            "quantum-teleportation-demo": "Quantum Teleportation Protocol Demonstration",
            "quantum-noise-demo": "Quantum Noise Comparison: Simulator vs Real Hardware",
            "quantum-art-generator": "Quantum Art & Music Generator from Quantum Measurements",
            
            # Music & Audio
            "ddsp-piano": "Differentiable Piano Model for MIDI-to-Audio Performance Synthesis",
            "audio2strudel": "Convert audio files to Strudel music patterns",
            "drum2strudel": "Convert drum patterns to Strudel music notation",
            "strudel-music-lab": "Interactive music lab using Strudel patterns",
            "music-agreement-analysis": "Music agreement and pattern analysis tools",
            
            # Community Tools
            "pr-summarizer": "AI-powered Pull Request Summarization Tool",
            "code-review-time-tracker": "Browser extension to track code review time and efficiency",
            "meeting-action-extractor": "Extract action items from meeting transcripts using AI",
            "postmortem-generator": "Automated incident post-mortem report generator",
            "feature-flag-auditor": "Feature flag auditing and management tool",
            "roadmap-dashboard": "Interactive roadmap visualization dashboard",
            "dead-link-checker": "Automated broken link detection and reporting",
            "api-rate-limit-monitor": "Monitor and alert on API rate limit usage",
            "github-star-notifier": "Get notified when your repositories receive stars",
            "github-repo-automation": "Automate GitHub repository setup: descriptions, topics, and badges",
            "env-manager": "Environment variable management tool",
            "git-hook-setup": "Automated git hooks setup and management",
            "quick-scaffold": "Quick project scaffolding tool",
            "mock-api-gen": "Mock API generator for testing and development",
            "task-run": "Task runner utility for development workflows",
            "saas-churn-predictor": "SaaS customer churn prediction using machine learning",
            "competitor-price-tracker": "Track competitor pricing changes over time",
            "social-media-scheduler": "Social media content scheduling and management",
            "email-warmup-service": "Email deliverability warmup service",
            "invoice-reminder-bot": "Automated invoice reminder bot",
            "domain-expiration-monitor": "Monitor domain expiration dates and send alerts",
            
            # Other Projects
            "strategyforge-ai": "Strategic planning and analysis AI platform",
            "identity-studio": "Identity management and authentication studio",
            "sap-whisper": "SAP system utilities and automation tools",
        }
        
        # Check for exact match
        if name in repo_patterns:
            return repo_patterns[name]
        
        # Check for partial matches
        for pattern, desc in repo_patterns.items():
            if pattern in name or name in pattern:
                return desc
        
        # Infer from name patterns
        if "quantum" in name:
            if "coin" in name:
                return "Quantum Superposition Demonstration"
            elif "twin" in name:
                return "Quantum Entanglement Visualization"
            elif "random" in name:
                return "Quantum Randomness Generation"
            elif "teleport" in name:
                return "Quantum Teleportation Protocol"
            elif "noise" in name:
                return "Quantum Noise Analysis"
            elif "art" in name or "generator" in name:
                return "Quantum Art & Music Generator"
            elif "grover" in name or "search" in name:
                return "Grover's Quantum Search Algorithm"
            else:
                return f"Quantum Computing Demonstration: {name_clean.title()}"
        
        if "ddsp" in name or "piano" in name:
            return "DDSP-Piano: Differentiable Piano Model for Audio Synthesis"
        
        if "strudel" in name:
            return f"Strudel Music Pattern Tool: {name_clean.title()}"
        
        if "financial" in name or any(t in topics for t in ["banking", "fintech", "financial-services"]):
            return f"Financial Services Tool: {name_clean.title()}"
        
        # Generic patterns
        if "cli" in name or "command" in name:
            return f"Command-line tool for {name_clean}"
        elif "api" in name:
            return f"API for {name_clean}"
        elif "web" in name or "frontend" in name:
            return f"Web application: {name_clean.title()}"
        elif "automation" in name:
            return f"Automation tool for {name_clean}"
        elif "monitor" in name or "tracker" in name:
            return f"Monitoring and tracking tool: {name_clean.title()}"
        elif "generator" in name:
            return f"Generator tool: {name_clean.title()}"
        elif "manager" in name:
            return f"Management tool: {name_clean.title()}"
        else:
            return f"{name_clean.title()} - {language or 'A'} project"
    
    def _suggest_topics(self, repo_info: Dict[str, Any]) -> List[str]:
        """Suggest topics based on repo info with enhanced intelligence."""
        topics = []
        language = repo_info.get("language", "").lower()
        name = repo_info.get("name", "").lower()
        
        # Known repository topic mappings
        repo_topics = {
            # Financial Products
            "agentguard": ["financial-services", "ai-security", "banking", "regulatory-compliance", 
                          "enterprise-software", "ai-governance", "cybersecurity", "fintech", 
                          "g-sib", "agentic-ai", "security-monitoring", "siem", "compliance"],
            "codeshield-ai": ["financial-services", "ai-security", "banking", "devsecops", 
                             "code-security", "static-analysis", "enterprise-software", "fintech"],
            "paymentsentinel": ["financial-services", "ai-security", "banking", "fraud-prevention", 
                               "payment-security", "transaction-monitoring", "fintech", "cybersecurity"],
            "legacybridge-ai-gateway": ["financial-services", "ai-security", "banking", "core-banking", 
                                       "legacy-systems", "api-gateway", "enterprise-software", "fintech"],
            "modelwatch": ["financial-services", "ai-security", "banking", "ml-ops", "model-validation", 
                          "model-risk", "ai-governance", "fintech"],
            "fleetcommand": ["financial-services", "ai-security", "banking", "orchestration", 
                            "multi-agent", "coordination", "enterprise-software", "agentic-ai"],
            "promptshield": ["financial-services", "ai-security", "banking", "prompt-injection", 
                            "input-validation", "waf", "cybersecurity", "fintech"],
            "identityvault-agents": ["financial-services", "ai-security", "banking", "iam", 
                                     "identity-management", "access-control", "enterprise-software"],
            "supplychainguard": ["financial-services", "ai-security", "banking", "supply-chain-security", 
                                "sbom", "dependency-scanning", "devsecops", "cybersecurity"],
            "complianceiq": ["financial-services", "ai-security", "banking", "regulatory-reporting", 
                            "compliance", "governance", "g-sib", "enterprise-software"],
            
            # Quantum Demos
            "quantum-coin-demo": ["quantum-computing", "superposition", "qiskit", "quantum-mechanics", 
                                 "education", "demo"],
            "quantum-twins-demo": ["quantum-computing", "entanglement", "qiskit", "quantum-mechanics", 
                                  "education", "demo"],
            "grover-search-demo": ["quantum-computing", "grover-algorithm", "qiskit", "quantum-algorithms", 
                                  "education", "demo"],
            "quantum-randomness-demo": ["quantum-computing", "randomness", "qiskit", "quantum-mechanics", 
                                       "cryptography", "education"],
            "quantum-teleportation-demo": ["quantum-computing", "teleportation", "qiskit", "quantum-mechanics", 
                                          "education", "demo"],
            "quantum-noise-demo": ["quantum-computing", "noise", "qiskit", "quantum-hardware", 
                                  "education", "demo"],
            "quantum-art-generator": ["quantum-computing", "art", "music", "qiskit", "creative", 
                                      "generator", "demo"],
            
            # Music & Audio
            "ddsp-piano": ["audio-synthesis", "ddsp", "piano", "music", "machine-learning", 
                          "tensorflow", "maestro"],
            "audio2strudel": ["audio", "strudel", "music", "conversion", "pattern"],
            "drum2strudel": ["drums", "strudel", "music", "conversion", "pattern"],
            "strudel-music-lab": ["strudel", "music", "interactive", "lab", "pattern"],
            "music-agreement-analysis": ["music", "analysis", "pattern", "agreement"],
            
            # Community Tools
            "pr-summarizer": ["github", "pull-requests", "ai", "automation", "developer-tools"],
            "code-review-time-tracker": ["github", "code-review", "productivity", "browser-extension", 
                                        "developer-tools"],
            "meeting-action-extractor": ["ai", "meetings", "automation", "nlp", "productivity"],
            "postmortem-generator": ["incident-management", "automation", "devops", "documentation"],
            "feature-flag-auditor": ["feature-flags", "audit", "devops", "developer-tools"],
            "roadmap-dashboard": ["roadmap", "visualization", "project-management", "streamlit"],
            "dead-link-checker": ["automation", "testing", "quality-assurance", "seo"],
            "api-rate-limit-monitor": ["api", "monitoring", "devops", "observability"],
            "github-star-notifier": ["github", "notifications", "automation", "developer-tools"],
            "github-repo-automation": ["github", "automation", "developer-tools", "ci-cd"],
            "env-manager": ["environment-variables", "devops", "configuration", "developer-tools"],
            "git-hook-setup": ["git", "hooks", "automation", "developer-tools"],
            "quick-scaffold": ["scaffolding", "templates", "developer-tools", "productivity"],
            "mock-api-gen": ["api", "mocking", "testing", "developer-tools"],
            "task-run": ["task-runner", "automation", "developer-tools", "productivity"],
        }
        
        # Check for exact match
        if name in repo_topics:
            topics.extend(repo_topics[name])
        else:
            # Add language
            if language:
                topics.append(language)
            
            # Infer from name patterns
            if "quantum" in name:
                topics.extend(["quantum-computing", "qiskit", "education"])
            elif "ddsp" in name or "piano" in name or "audio" in name or "music" in name:
                topics.extend(["audio", "music", "machine-learning"])
            elif "financial" in name or "banking" in name or "payment" in name:
                topics.extend(["financial-services", "fintech", "banking"])
            elif "ai" in name or "agent" in name:
                topics.extend(["ai", "machine-learning", "automation"])
            
            # Generic patterns
            if "cli" in name or "command" in name:
                topics.append("cli")
            if "api" in name:
                topics.append("api")
            if "web" in name or "frontend" in name:
                topics.append("web")
            if "automation" in name:
                topics.append("automation")
            if "tool" in name or "manager" in name or "generator" in name:
                topics.append("tools")
            if "monitor" in name or "tracker" in name:
                topics.append("monitoring")
            if "github" in name:
                topics.append("github")
            if "docker" in name:
                topics.append("docker")
            
            # Add common topics if none found
            if not topics:
                topics = ["open-source"]
        
        # Remove duplicates and limit
        topics = list(dict.fromkeys(topics))  # Preserve order, remove duplicates
        return topics[:10]  # Limit to 10 topics (GitHub allows up to 20)
    
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

