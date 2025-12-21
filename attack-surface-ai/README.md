# AI Attack Surface Guard

An AI-native Attack Surface Intelligence platform that automatically discovers, explains, and helps fix public security exposures in GitHub repositories.

## 🎯 Product Goal

Automatically discover, explain, and help fix public security exposures (starting with GitHub).

## 👥 Target User

Founders and developers with no dedicated security team.

## ✨ Core Principles

- **Zero configuration** (GitHub OAuth only - coming soon)
- **Results in under 5 minutes**
- **Plain-English explanations** (no security jargon)
- **Actionable fixes** (PRs, steps, scripts - coming soon)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- GitHub Personal Access Token (for scanning)

### Installation

1. Clone or navigate to this directory:
```bash
cd attack-surface-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (optional):
```bash
# Create a .env file
echo "GITHUB_TOKEN=your_github_token_here" > .env
```

### Running the API

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📖 Usage

### Scan a Repository

**Using curl:**
```bash
curl "http://localhost:8000/scan?owner=username&repo=repository-name&token=YOUR_GITHUB_TOKEN"
```

**Using the token from environment:**
```bash
export GITHUB_TOKEN=your_token_here
curl "http://localhost:8000/scan?owner=username&repo=repository-name"
```

**Example:**
```bash
curl "http://localhost:8000/scan?owner=octocat&repo=Hello-World&token=ghp_xxxxxxxxxxxx"
```

### Response Format

The API returns:
- **Status**: Overall security status (critical/high/medium/low/clean)
- **Summary**: Counts by severity and affected files
- **Findings**: Each finding includes:
  - What was found
  - Why it's dangerous
  - What an attacker could do
  - Remediation steps
- **Recommendations**: Prioritized action items

## 🔍 What It Detects

The scanner detects various types of exposed secrets:

- **Critical**: AWS keys, Stripe live keys, GitHub tokens, Private keys
- **High**: API keys, Database connection strings, Slack/Discord tokens
- **Medium**: Test keys, development credentials

## 🏗️ Architecture

```
attack-surface-ai/
├── main.py              # FastAPI application
├── github_scan.py       # GitHub repository scanning
├── ai_reasoner.py       # AI-powered explanations
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Separation of Concerns

- **`github_scan.py`**: Handles all GitHub API interactions and secret detection
- **`ai_reasoner.py`**: Provides plain-English explanations and risk assessments
- **`main.py`**: API layer that orchestrates scanning and explanation

## 🔐 Getting a GitHub Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Select scopes: `repo` (for private repos) or `public_repo` (for public repos only)
4. Copy the token and use it in API calls or set as `GITHUB_TOKEN` environment variable

## 🛠️ Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Adding New Secret Patterns

Edit `github_scan.py` and add patterns to the `SECRET_PATTERNS` dictionary:

```python
"New Secret Type": {
    "pattern": r"your_regex_pattern_here",
    "severity": "critical"  # or "high", "medium", "low"
}
```

Then add corresponding explanations in `ai_reasoner.py` under `RISK_EXPLANATIONS`.

## 📋 MVP Scope

### ✅ Included

- Scan GitHub user or org repositories
- Detect potential secrets (API keys, tokens, credentials)
- Classify severity using AI reasoning
- Explain findings in plain English
- Suggest remediation steps

### 🚧 Coming Soon

- GitHub OAuth (no tokens in URL)
- Auto-generated remediation PRs
- Domain & subdomain scanning

### ❌ Out of Scope (for now)

- Log ingestion
- Network packet inspection
- Compliance dashboards
- Agents or kernel-level tools

## 🤝 Contributing

This is an MVP. Contributions welcome! Focus areas:
- More comprehensive secret detection patterns
- Better AI explanations (integrate with OpenAI/Anthropic)
- GitHub OAuth implementation
- Auto PR generation

## 📝 License

See LICENSE file in parent directory.

## 🎯 Philosophy

> You are not building "another security scanner"
> 
> You are building: **Security that explains itself and fixes itself**

