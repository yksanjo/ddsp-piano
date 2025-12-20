#!/usr/bin/env python3
"""
Batch improvement script for all GitHub repositories.
This script reviews and improves all repositories systematically.
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import List, Dict, Any

# Import the review script
sys.path.insert(0, str(Path(__file__).parent))
from review_all_repos import RepoReviewer


class BatchRepoImprover:
    """Batch improve all repositories."""
    
    def __init__(self, token: str = None, username: str = None, dry_run: bool = False):
        """Initialize batch improver."""
        self.reviewer = RepoReviewer(token=token, username=username)
        self.dry_run = dry_run
        self.improvements_made = []
        self.errors = []
    
    def improve_all_repos(self, include_forks: bool = False, delay: float = 1.0):
        """Improve all repositories."""
        print("🚀 Batch Repository Improvement")
        print("=" * 70)
        print(f"Mode: {'DRY RUN (no changes will be made)' if self.dry_run else 'LIVE (changes will be applied)'}")
        print()
        
        # Get all repositories
        repos = self.reviewer.list_all_repos(include_forks=include_forks)
        
        if not repos:
            print("No repositories found.")
            return
        
        print(f"\n🔍 Analyzing {len(repos)} repositories...\n")
        
        # Filter out archived repos
        active_repos = [r for r in repos if not r.get("archived", False)]
        print(f"📦 Found {len(active_repos)} active repositories (excluding {len(repos) - len(active_repos)} archived)\n")
        
        improvements_summary = {
            "descriptions_added": 0,
            "topics_added": 0,
            "badges_added": 0,
            "readmes_updated": 0,
            "total_improved": 0
        }
        
        for i, repo in enumerate(active_repos, 1):
            full_name = repo["full_name"]
            print(f"[{i}/{len(active_repos)}] Processing: {full_name}")
            
            try:
                # Analyze repository
                analysis = self.reviewer.analyze_repo(repo)
                
                if not analysis["needs_update"]:
                    print(f"   ✓ Repository is up to date")
                    print()
                    continue
                
                # Show what needs improvement
                if analysis["issues"]:
                    print(f"   Issues found:")
                    for issue in analysis["issues"]:
                        print(f"     ⚠️  {issue}")
                
                if analysis["suggestions"]:
                    print(f"   Suggestions:")
                    for suggestion in analysis["suggestions"]:
                        print(f"     💡 {suggestion}")
                
                # Apply improvements
                if not self.dry_run:
                    print(f"   🔧 Applying improvements...")
                    success = self.reviewer.improve_repo(full_name, auto_apply=True)
                    
                    if success:
                        improvements_summary["total_improved"] += 1
                        self.improvements_made.append({
                            "repo": full_name,
                            "improvements": analysis["suggestions"]
                        })
                        print(f"   ✅ Improvements applied")
                    else:
                        self.errors.append({
                            "repo": full_name,
                            "error": "Failed to apply improvements"
                        })
                        print(f"   ❌ Failed to apply improvements")
                else:
                    print(f"   🔍 [DRY RUN] Would apply improvements")
                    improvements_summary["total_improved"] += 1
                
                print()
                
                # Rate limiting delay
                if delay > 0:
                    time.sleep(delay)
                    
            except Exception as e:
                error_msg = f"Error processing {full_name}: {e}"
                print(f"   ❌ {error_msg}")
                self.errors.append({
                    "repo": full_name,
                    "error": str(e)
                })
                print()
                continue
        
        # Print summary
        self._print_summary(improvements_summary, len(active_repos))
        
        # Save report
        self._save_report(improvements_summary, len(active_repos))
    
    def _print_summary(self, summary: Dict[str, int], total: int):
        """Print improvement summary."""
        print("\n" + "=" * 70)
        print("📊 IMPROVEMENT SUMMARY")
        print("=" * 70)
        print(f"Total repositories processed: {total}")
        print(f"Repositories improved: {summary['total_improved']}")
        print(f"Repositories up to date: {total - summary['total_improved']}")
        
        if self.errors:
            print(f"\n⚠️  Errors encountered: {len(self.errors)}")
            for error in self.errors[:5]:  # Show first 5 errors
                print(f"   - {error['repo']}: {error['error']}")
            if len(self.errors) > 5:
                print(f"   ... and {len(self.errors) - 5} more")
        
        print()
    
    def _save_report(self, summary: Dict[str, int], total: int):
        """Save improvement report to file."""
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "mode": "dry_run" if self.dry_run else "live",
            "summary": summary,
            "total_repos": total,
            "improvements_made": self.improvements_made,
            "errors": self.errors
        }
        
        report_file = "batch_improvement_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Detailed report saved to: {report_file}")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Batch improve all GitHub repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run mode - show what would be done without making changes"
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
        "--delay",
        type=float,
        default=1.0,
        help="Delay between repository updates in seconds (default: 1.0)"
    )
    parser.add_argument(
        "--token",
        help="GitHub personal access token (or set GITHUB_TOKEN env var)"
    )
    
    args = parser.parse_args()
    
    # Get token
    token = args.token or os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ Error: GITHUB_TOKEN environment variable is required")
        print("   Get one at: https://github.com/settings/tokens")
        sys.exit(1)
    
    # Create improver
    improver = BatchRepoImprover(
        token=token,
        username=args.username,
        dry_run=args.dry_run
    )
    
    # Run improvements
    improver.improve_all_repos(
        include_forks=args.include_forks,
        delay=args.delay
    )


if __name__ == "__main__":
    main()

