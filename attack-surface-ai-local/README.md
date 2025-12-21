# AI Attack Surface Guard

> **Your security team, before you can afford one.**

An AI-native Attack Surface Intelligence platform that prevents the security disaster that kills your startup. Get a complete security audit in 5 minutes, with plain-English explanations that actually make sense.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 🎯 Why This Exists

**The Problem:** Most security tools are built for security teams. They're complex, jargon-heavy, and require weeks of setup. Founders and small teams get left behind, making them easy targets.

**The Solution:** Security that explains itself in plain English. No security expertise required. Results in 5 minutes. Fixes that actually work.

**The Outcome:** Sleep-at-night peace of mind, not compliance checkboxes.

---

## 🚀 What Makes Us Different

### ❌ What Competitors Say:
- "We detect 800+ secret types"
- "Enterprise-grade secret scanning"
- "CI/CD integration required"

### ✅ What We Deliver:
- **"We prevent the security disaster that kills your startup"**
- **"Your security team, before you can afford one"**
- **"5-minute security audit, zero setup"**

### Our Competitive Edge

| Feature | Competitors | Attack Surface AI |
|---------|------------|-------------------|
| **Time to Value** | Days/weeks of setup | 5 minutes |
| **Explanations** | Technical jargon | Plain English with business impact |
| **Target User** | Security teams | Founders & developers |
| **Pricing** | $18-50/dev/month | Simple flat pricing |
| **Setup** | Complex CI/CD integration | Zero configuration |
| **Remediation** | Generic fixes | Guided, contextual fixes |
| **Attack Scenarios** | Severity labels | "Here's what a hacker would do" |

---

## 💡 Core Value Propositions

### 1. **AI-Native Explanation Layer** (Our Secret Weapon)

Most tools just detect and report. We explain **why it matters** in founder language:

- ✅ **Business impact narratives**, not just technical details
- ✅ **Attack scenarios**: "Here's exactly what a hacker would do with this AWS key"
- ✅ **Role-based explanations**: Different for founders vs developers
- ✅ **Exploitability-based prioritization**, not just severity labels

### 2. **Time-to-Value Speed**

While competitors require complex CI/CD integration, policy configuration, and team onboarding, we deliver:

- ✅ **Instant security audit** - like running a credit report for your codebase
- ✅ **Zero configuration** - just connect your GitHub
- ✅ **Results in 5 minutes** - not 5 weeks

### 3. **Built for Founders, Not Security Teams**

Most tools assume you know what SAST, DAST, and CVE mean. We assume you don't, and **that's our moat**.

- ✅ **No security jargon** - we speak founder language
- ✅ **"Sleep-at-night" peace of mind** - not compliance checkboxes
- ✅ **Positioned as "security advisor"** - not "vulnerability scanner"

### 4. **Automated Remediation with Context**

Where competitors provide generic fixes, we provide:

- ✅ **Pull requests that fix issues AND explain the fix** in comments
- ✅ **Step-by-step guided remediation**: "First, rotate this key in AWS, then..."
- ✅ **Runbooks customized to your tech stack**
- ✅ **"Fix-it-for-me" service** for critical issues (coming soon)

### 5. **Continuous Intelligence**

Most tools scan once or on commit. We provide:

- ✅ **Weekly monitoring** for new attack patterns
- ✅ **Automatic re-scanning** when issues become critical
- ✅ **Progress tracking** with simple dashboards
- ✅ **Weekly "security health" reports** in plain English

---

## 👥 Who This Is For

### ✅ Perfect For:
- **Founders** who can't afford a security team yet
- **Small teams** (1-20 people) without dedicated security
- **Developers** who want security without the complexity
- **Startups** that need to pass investor security audits

### ❌ Not For:
- Enterprise security teams (we're building something better for you later)
- Compliance-focused organizations (we focus on actual risk, not checkboxes)
- Teams that already have dedicated security staff

---

## 📸 See It In Action

### API Documentation (Swagger UI)

The interactive API documentation provides a clean interface to explore and test all endpoints:

![Swagger UI Main](screenshots/swagger-main.png)

### Scan Endpoint

The `/scan` endpoint allows you to scan any GitHub repository for exposed secrets:

![Scan Endpoint](screenshots/swagger-scan-endpoint.png)

### API Root Response

The root endpoint provides an overview of available endpoints:

![API Root](screenshots/api-root-response.png)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- GitHub Personal Access Token (for scanning)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yksanjo/attack-surface-ai.git
cd attack-surface-ai
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables (optional):**
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
- **Swagger UI**: `http://localhost:8000/docs` (Interactive API explorer)
- **ReDoc**: `http://localhost:8000/redoc` (Beautiful documentation)

---

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

The API returns comprehensive, founder-friendly results:

- **Status**: Overall security status (critical/high/medium/low/clean)
- **Message**: Plain-English summary (e.g., "🚨 CRITICAL: 3 critical security exposure(s) found. Immediate action required.")
- **Summary**: Counts by severity and affected files
- **Findings**: Each finding includes:
  - **What was found**: Clear description
  - **Why it's dangerous**: Business impact explanation
  - **What an attacker could do**: Specific attack scenarios
  - **Remediation steps**: Step-by-step fix instructions
- **Recommendations**: Prioritized action items

---

## 🔍 What We Detect

### Critical Severity
- AWS Access Keys & Secret Keys
- Stripe Live API Keys
- GitHub Personal Access Tokens
- Private Cryptographic Keys
- Database Connection Strings (MongoDB, PostgreSQL)

### High Severity
- Generic API Keys
- Slack & Discord Bot Tokens
- OAuth Tokens
- Service Account Credentials

### Medium Severity
- Test/Development Keys
- Stripe Test Keys
- Non-production Credentials

---

## 🏗️ Architecture

```
attack-surface-ai/
├── main.py              # FastAPI application
├── github_scan.py       # GitHub repository scanning (recursive)
├── ai_reasoner.py       # AI-powered plain-English explanations
├── requirements.txt     # Python dependencies
├── screenshots/         # UI/UX screenshots
└── README.md           # This file
```

### Separation of Concerns

- **`github_scan.py`**: Handles all GitHub API interactions and secret detection
- **`ai_reasoner.py`**: Provides plain-English explanations and risk assessments
- **`main.py`**: API layer that orchestrates scanning and explanation

---

## 🔐 Getting a GitHub Token

1. Go to [GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select scopes:
   - `repo` (for private repos) 
   - OR `public_repo` (for public repos only)
4. Copy the token and use it in API calls or set as `GITHUB_TOKEN` environment variable

---

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

---

## 📋 Current Status (MVP)

### ✅ What's Included

- ✅ Scan GitHub user or org repositories (recursive file scanning)
- ✅ Detect 12+ types of exposed secrets (AWS, Stripe, GitHub, databases, etc.)
- ✅ AI-powered severity classification
- ✅ Plain-English explanations with business impact
- ✅ Attack scenario descriptions
- ✅ Step-by-step remediation guidance
- ✅ FastAPI REST API with Swagger documentation

### 🚧 Coming Soon

- 🔄 GitHub OAuth (no tokens in URL)
- 🔄 Auto-generated remediation PRs
- 🔄 Domain & subdomain scanning
- 🔄 Continuous monitoring and alerts
- 🔄 Slack/Linear/Notion integrations
- 🔄 "Security Copilot" conversational interface
- 🔄 Proof of exploitability (verify keys actually work)
- 🔄 Beyond GitHub: S3 buckets, Docker images, npm/PyPI packages

### ❌ Out of Scope (For Now)

- Log ingestion
- Network packet inspection
- Compliance dashboards
- Agents or kernel-level tools

---

## 💰 Pricing Strategy (Future)

We're building the only security tool founders **want** to use, not one they're forced to use.

### Planned Tiers:

- **Free**: Scan public repos, limit 1 scan/week
- **Starter ($29/month)**: Unlimited scans, private repos, email alerts
- **Pro ($99/month)**: Auto-remediation PRs, Slack integration, weekly monitoring
- **Enterprise ($499/month)**: API access, team features, custom patterns

**Compare to:** GitGuardian ($18-50/developer/month) or GitHub Advanced Security (requires Enterprise plan)

---

## 🎯 Strategic Positioning

### We Don't Compete on Features

We compete on **outcome**:

| ❌ What Others Say | ✅ What We Say |
|-------------------|----------------|
| "We detect 800+ secret types" | "We prevent the security disaster that kills your startup" |
| "Enterprise-grade secret scanning" | "Your security team, before you can afford one" |
| "CI/CD integration" | "5-minute security audit, zero setup" |

### Our Moat

**Every other tool assumes the user knows security jargon. We assume they don't, and that's our competitive advantage.**

We're building the **Grammarly for security** - helpful, not annoying. The only security tool founders actually **want** to use.

---

## 🤝 Contributing

This is an MVP. Contributions welcome! Focus areas:

- More comprehensive secret detection patterns
- Better AI explanations (integrate with OpenAI/Anthropic)
- GitHub OAuth implementation
- Auto PR generation
- Integration with modern dev tools (Slack, Linear, Notion)
- Proof of exploitability features

---

## 📝 License

See LICENSE file in parent directory.

---

## 🎯 Philosophy

> **You are not building "another security scanner"**
> 
> **You are building: Security that explains itself and fixes itself**

### The Vision

Become the only security tool that:
- Founders **want** to use (not forced by investors/compliance)
- Explains security in **founder language** (not security jargon)
- Delivers value in **5 minutes** (not 5 weeks)
- Focuses on **actual risk** (not compliance checkboxes)
- Helps you **sleep at night** (not just pass audits)

---

## 🌟 Quick Wins & Momentum Builders

Coming soon:
- Launch on Product Hunt: "Security for founders who can't hire security"
- Scan top YC companies publicly and email founders with free report
- "Security Speedrun" - scan repo and generate report in 60 seconds
- Partner with VC firms to offer free scans to portfolio companies
- Create viral tool: "Check if your personal GitHub has leaks" (like Have I Been Pwned)

---

## 📚 Additional Resources

- [GitHub Repository](https://github.com/yksanjo/attack-surface-ai)
- [API Documentation](http://localhost:8000/docs) (when running locally)
- [Issues & Feature Requests](https://github.com/yksanjo/attack-surface-ai/issues)

---

**Built with ❤️ for founders who can't afford a security team yet.**
