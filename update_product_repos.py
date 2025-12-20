#!/usr/bin/env python3
"""
Update descriptions and badges for the 10 distribution-driven products
"""

import os
import sys
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

# Product descriptions and topics
PRODUCTS = {
    "RateGuard": {
        "repo": "yksanjo/RateGuard",
        "description": "🛡️ API Rate Limit Monitor - Never get caught off guard by rate limit errors. Monitor multiple APIs simultaneously and get real-time alerts via Slack or Discord.",
        "topics": ["api", "monitoring", "rate-limit", "slack", "discord", "automation", "python", "devops"]
    },
    "ReviewClock": {
        "repo": "yksanjo/ReviewClock",
        "description": "⏱️ Code Review Time Tracker - Track how long pull requests sit in review. Get insights into your team's code review velocity and identify bottlenecks.",
        "topics": ["github", "code-review", "chrome-extension", "productivity", "developer-tools", "javascript"]
    },
    "ChurnGuard": {
        "repo": "yksanjo/ChurnGuard",
        "description": "🔮 SaaS Churn Predictor - Analyze your Stripe data to predict which customers are at risk of churning. Get actionable insights to reduce churn and improve retention.",
        "topics": ["saas", "churn", "stripe", "analytics", "machine-learning", "python", "business"]
    },
    "WarmUp": {
        "repo": "yksanjo/WarmUp",
        "description": "📧 Email Warm-up Service - Automated email domain warm-up tool that gradually increases sending volume to improve deliverability and avoid spam filters.",
        "topics": ["email", "warmup", "deliverability", "smtp", "automation", "python", "marketing"]
    },
    "StarAlert": {
        "repo": "yksanjo/StarAlert-",
        "description": "⭐ GitHub Star Notifier - Get notified when someone stars your repository, with context about who starred and why. Never miss a potential contributor or user.",
        "topics": ["github", "notifications", "open-source", "automation", "python", "developer-tools"]
    },
    "InvoiceBot": {
        "repo": "yksanjo/InvoiceBot",
        "description": "💰 Invoice Reminder Bot - Automated follow-up bot for unpaid invoices. Integrates with Stripe and PayPal to track unpaid invoices and send reminder emails.",
        "topics": ["invoice", "stripe", "paypal", "automation", "python", "business", "finance"]
    },
    "DomainWatch": {
        "repo": "yksanjo/DomainWatch",
        "description": "🌐 Domain Expiration Monitor - Monitor multiple domains and get alerts before they expire. Never lose a domain due to expiration again.",
        "topics": ["domain", "monitoring", "whois", "automation", "python", "devops", "infrastructure"]
    },
    "PriceWatch": {
        "repo": "yksanjo/PriceWatch",
        "description": "💵 Competitor Price Tracker - Track competitor pricing changes and get alerts when prices change. Perfect for e-commerce and SaaS businesses.",
        "topics": ["price-tracking", "competitor-analysis", "ecommerce", "saas", "automation", "python", "business"]
    },
    "SocialQueue": {
        "repo": "yksanjo/SocialQueue",
        "description": "📱 Social Media Post Scheduler - Schedule and post to multiple social media platforms (Twitter, LinkedIn, Mastodon) from one place. Perfect for content creators and marketers.",
        "topics": ["social-media", "scheduler", "twitter", "linkedin", "mastodon", "automation", "python", "marketing"]
    },
    "LinkCheck": {
        "repo": "yksanjo/LinkCheck",
        "description": "🔗 Dead Link Checker - Scan websites for broken links and generate comprehensive reports. Perfect for SEO audits and website maintenance.",
        "topics": ["seo", "link-checker", "web-crawler", "automation", "python", "developer-tools", "website"]
    }
}

def update_repo(product_name: str, product_info: dict, github: GitHubRepoAutomation, auto_apply: bool = True):
    """Update a single repository."""
    print(f"\n{'='*60}")
    print(f"📦 {product_name}")
    print(f"{'='*60}")
    
    owner, repo = product_info["repo"].split("/")
    
    try:
        # Get repo info
        repo_info = github.get_repo_info(owner, repo)
        print(f"✅ Found repository: {repo_info.get('full_name')}")
        
        improvements = []
        
        # Update description
        current_desc = repo_info.get("description", "")
        new_desc = product_info["description"]
        if current_desc != new_desc:
            if auto_apply:
                if github.update_description(owner, repo, new_desc):
                    improvements.append("description")
            else:
                print(f"💡 Would update description: {new_desc}")
        else:
            print(f"✓ Description already set")
        
        # Update topics
        current_topics = set(repo_info.get("topics", []))
        new_topics = set(product_info["topics"])
        if current_topics != new_topics:
            if auto_apply:
                # Merge topics (keep existing + add new)
                merged_topics = list(current_topics | new_topics)
                if github.update_topics(owner, repo, merged_topics):
                    improvements.append("topics")
            else:
                print(f"💡 Would update topics: {', '.join(product_info['topics'])}")
        else:
            print(f"✓ Topics already set")
        
        # Check and update badges in README
        readme_content = github.get_readme(owner, repo)
        if readme_content:
            # Check if badges already exist
            if "img.shields.io" in readme_content or "badge" in readme_content.lower():
                print(f"✓ Badges already present in README")
            else:
                if auto_apply:
                    badge_gen = BadgeGenerator(owner, repo, repo_info)
                    badges = badge_gen.generate_badges()
                    updated_readme = ReadmeUpdater.add_badges_to_readme(readme_content, badges)
                    if updated_readme != readme_content:
                        if github.update_readme(owner, repo, updated_readme):
                            improvements.append("badges")
                            print(f"✅ Added {len(badges)} badges to README")
                else:
                    print(f"💡 Would add badges to README")
        else:
            print(f"⚠️  No README found")
        
        if improvements:
            print(f"✅ Applied improvements: {', '.join(improvements)}")
        else:
            print(f"✓ Repository is up to date")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Update descriptions and badges for product repositories")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be updated without making changes")
    parser.add_argument("--product", help="Update only a specific product (e.g., RateGuard)")
    
    args = parser.parse_args()
    
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ Error: GITHUB_TOKEN environment variable is required")
        print("   Get one at: https://github.com/settings/tokens")
        sys.exit(1)
    
    github = GitHubRepoAutomation(token=token)
    
    print("🚀 Updating Product Repositories")
    print("=" * 60)
    
    products_to_update = {}
    if args.product:
        if args.product in PRODUCTS:
            products_to_update[args.product] = PRODUCTS[args.product]
        else:
            print(f"❌ Product '{args.product}' not found")
            print(f"   Available products: {', '.join(PRODUCTS.keys())}")
            sys.exit(1)
    else:
        products_to_update = PRODUCTS
    
    for product_name, product_info in products_to_update.items():
        update_repo(product_name, product_info, github, auto_apply=not args.dry_run)
    
    print(f"\n{'='*60}")
    print("✨ Done!")
    if args.dry_run:
        print("💡 Run without --dry-run to apply changes")
    print("=" * 60)

if __name__ == "__main__":
    main()







