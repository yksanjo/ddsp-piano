# Repository Improvement Guide

This guide explains how to review and improve all your GitHub repositories.

## Quick Start

### 1. Review All Repositories (Dry Run)

First, review all repositories to see what needs improvement:

```bash
python3 review_all_repos.py
```

This will:
- List all your repositories
- Analyze each one for missing elements
- Show suggestions without making changes
- Generate a report saved to `repo_review_report.txt`

### 2. Review with Auto-Apply

To automatically apply improvements:

```bash
python3 review_all_repos.py --auto-apply
```

**⚠️ Warning:** This will make changes to your repositories. Review the dry-run output first!

### 3. Batch Improve All Repositories

For systematic batch processing with better control:

```bash
# Dry run first (recommended)
python3 batch_improve_all_repos.py --dry-run

# Apply improvements
python3 batch_improve_all_repos.py
```

## What Gets Improved

### Repository Descriptions
- Intelligent descriptions based on repository name and patterns
- Known patterns for:
  - Financial products (AgentGuard, CodeShield AI, etc.)
  - Quantum demos (quantum-coin-demo, quantum-twins-demo, etc.)
  - Music & audio projects (ddsp-piano, audio2strudel, etc.)
  - Community tools (pr-summarizer, code-review-time-tracker, etc.)

### Repository Topics
- Comprehensive topic suggestions based on repository type
- Financial products get: `financial-services`, `ai-security`, `banking`, etc.
- Quantum demos get: `quantum-computing`, `qiskit`, `education`, etc.
- Community tools get: `github`, `automation`, `developer-tools`, etc.

### README Badges
- License badges (if license detected)
- Language badges (Python, JavaScript, TypeScript, Rust, Go, Java)
- GitHub stats (stars, forks, issues)
- CI/CD badges (if GitHub Actions detected)
- Docker badges (if Docker detected)
- Last commit badge

### README Quality Checks
- Checks for proper title (H1 heading)
- Checks for project description
- Checks for installation/setup instructions
- Checks for usage examples
- Identifies placeholder/short READMEs

## Prerequisites

1. **GitHub Personal Access Token**
   - Go to: https://github.com/settings/tokens
   - Generate a new token with `repo` scope (full control of private repositories)
   - Set it as an environment variable:
     ```bash
     export GITHUB_TOKEN=ghp_your_token_here
     ```

2. **Python Dependencies**
   ```bash
   pip install requests
   ```

## Command Options

### review_all_repos.py

```bash
# Review all repos (dry run)
python3 review_all_repos.py

# Review all repos and apply improvements
python3 review_all_repos.py --auto-apply

# Review specific repository
python3 review_all_repos.py --repo owner/repo-name

# Include forked repositories
python3 review_all_repos.py --include-forks

# Specify username
python3 review_all_repos.py --username yourusername
```

### batch_improve_all_repos.py

```bash
# Dry run (recommended first)
python3 batch_improve_all_repos.py --dry-run

# Apply improvements
python3 batch_improve_all_repos.py

# Include forked repositories
python3 batch_improve_all_repos.py --include-forks

# Adjust delay between updates (default: 1.0 seconds)
python3 batch_improve_all_repos.py --delay 2.0

# Specify token
python3 batch_improve_all_repos.py --token ghp_your_token
```

## Example Output

```
🚀 GitHub Repository Reviewer
============================================================

✅ Authenticated as: yksanjo
📡 Fetching repositories for yksanjo...
   Fetched 25 repositories so far...
✅ Found 25 repositories

🔍 Analyzing repositories...

[1/25] yksanjo/task-run
   ⚠️  No repository description
   ⚠️  No repository topics/tags
   💡 Add a repository description
   💡 Add repository topics for better discoverability
   💡 Add badges to README for better presentation
   ⚠️  Needs updates (run with --auto-apply to fix)

[2/25] yksanjo/env-manager
   ✓ Repository is up to date

...

╔══════════════════════════════════════════════════════════════╗
║           GitHub Repository Review Report                    ║
╚══════════════════════════════════════════════════════════════╝

📊 Summary:
   Total repositories: 25
   Need updates: 8
   Archived: 2
   Up to date: 15
```

## Best Practices

1. **Always run dry-run first**: Review what will be changed before applying
2. **Review generated descriptions**: Auto-generated descriptions may need manual refinement
3. **Customize topics**: Add more specific topics manually on GitHub for better discoverability
4. **Check badges**: Ensure badges are appropriate for your project
5. **Update regularly**: Run the review script periodically to keep repositories up to date
6. **Rate limiting**: Use `--delay` option if you hit rate limits

## Troubleshooting

### Authentication Failed
- Verify your GitHub token is valid
- Ensure token has `repo` scope
- Check token hasn't expired

### Repository Not Found
- Verify repository name format: `owner/repo-name`
- Check you have access to the repository
- Ensure repository isn't archived

### README Update Failed
- The script will show badges to add manually
- Copy and paste them into your README.md
- Ensure you have write access to the repository

### Rate Limit Exceeded
- GitHub API has rate limits (5000 requests/hour for authenticated users)
- Use `--delay` option to slow down requests
- Wait and retry, or process repositories in smaller batches

## Reports Generated

- `repo_review_report.txt` - Text report from review_all_repos.py
- `batch_improvement_report.json` - JSON report from batch_improve_all_repos.py

## Next Steps

1. Set up your GitHub token
2. Run the review script in dry-run mode
3. Review the generated report
4. Apply improvements selectively or use `--auto-apply` for all
5. Manually refine descriptions and topics as needed

