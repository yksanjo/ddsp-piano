# Update Product Repositories - Instructions

## Quick Start

1. **Get your GitHub Personal Access Token:**
   - Go to: https://github.com/settings/tokens
   - Generate a new token with `repo` scope (full control)
   - Copy the token

2. **Set the token:**
   ```bash
   export GITHUB_TOKEN=ghp_your_token_here
   ```

3. **Run the update script:**
   ```bash
   # Dry run (see what will change)
   python3 update_product_repos.py --dry-run
   
   # Apply changes
   python3 update_product_repos.py
   ```

## What It Does

The script will update all 10 product repositories with:

### 1. Repository Descriptions
- RateGuard: "🛡️ API Rate Limit Monitor - Never get caught off guard by rate limit errors..."
- ReviewClock: "⏱️ Code Review Time Tracker - Track how long pull requests sit in review..."
- ChurnGuard: "🔮 SaaS Churn Predictor - Analyze your Stripe data to predict churn..."
- WarmUp: "📧 Email Warm-up Service - Automated email domain warm-up tool..."
- StarAlert: "⭐ GitHub Star Notifier - Get notified when someone stars your repository..."
- InvoiceBot: "💰 Invoice Reminder Bot - Automated follow-up bot for unpaid invoices..."
- DomainWatch: "🌐 Domain Expiration Monitor - Monitor multiple domains and get alerts..."
- PriceWatch: "💵 Competitor Price Tracker - Track competitor pricing changes..."
- SocialQueue: "📱 Social Media Post Scheduler - Schedule and post to multiple platforms..."
- LinkCheck: "🔗 Dead Link Checker - Scan websites for broken links..."

### 2. Repository Topics/Tags
Each repo gets relevant topics for better discoverability:
- Language tags (python, javascript)
- Category tags (automation, monitoring, developer-tools)
- Platform tags (github, slack, stripe)
- Use-case tags (saas, ecommerce, marketing)

### 3. README Badges
Automatically adds badges to README files:
- License badge
- Python version badge
- Status badge
- GitHub stars badge
- Language-specific badges

## Update Single Product

To update just one product:
```bash
python3 update_product_repos.py --product RateGuard
```

## Alternative: Use review_all_repos.py

You can also use the general repository reviewer:
```bash
# Review all repos (dry run)
python3 review_all_repos.py

# Apply improvements to all repos
python3 review_all_repos.py --auto-apply

# Review specific repo
python3 review_all_repos.py --repo yksanjo/RateGuard --auto-apply
```

## Manual Update

If you prefer to update manually, use the github-repo-automation tool:
```bash
cd github-repo-automation
python3 github-repo-automation.py \
  --repo yksanjo/RateGuard \
  --description "🛡️ API Rate Limit Monitor - Never get caught off guard..." \
  --topics "api,monitoring,rate-limit,slack,discord,automation,python,devops"
```







