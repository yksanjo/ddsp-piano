# Projects in this Repository

This repository is a monorepo containing multiple projects. Each project is independent and can be used separately.

## Main Project

### 🎹 DDSP-Piano
**Location:** `/ddsp_piano/`  
**Type:** Python package  
**Description:** Differentiable Piano model for MIDI-to-Audio Performance Synthesis  
**Documentation:** See [README.md](README.md)  
**Dependencies:** `ddsp>=3.2.0`, TensorFlow

## Security & AI Tools

### 🔍 Attack Surface AI
**Location:** `/attack-surface-ai/`  
**Type:** Python (FastAPI)  
**Description:** AI-powered attack surface monitoring and scanning  
**Tech Stack:** FastAPI, Python  
**Documentation:** [attack-surface-ai/README.md](attack-surface-ai/README.md)

### 📊 LogCopilot
**Location:** `/logcopilot/`  
**Type:** Full-stack (TypeScript/Next.js + Node.js)  
**Description:** AI-Powered Log Analysis for Non-Security Experts  
**Tech Stack:** Next.js, TypeScript, Express, PostgreSQL  
**Documentation:** [logcopilot/README.md](logcopilot/README.md)

### 🛡️ PentestGPT
**Location:** `/pentestgpt/`  
**Type:** Full-stack (TypeScript/Next.js + Node.js)  
**Description:** AI-Powered Security Testing Copilot  
**Tech Stack:** Next.js, TypeScript, Express, PostgreSQL  
**Documentation:** [pentestgpt/README.md](pentestgpt/README.md)

### 🌐 SurfaceAI
**Location:** `/surfaceai/`  
**Type:** Full-stack (TypeScript/Next.js + Node.js)  
**Description:** AI-Powered Attack Surface Monitor for GitHub Repositories  
**Tech Stack:** Next.js, TypeScript, Express, PostgreSQL  
**Documentation:** [surfaceai/README.md](surfaceai/README.md)

### ☁️ VPC Guardian
**Location:** `/vpc-guardian/`  
**Type:** Full-stack (TypeScript/Next.js + Node.js)  
**Description:** AI-Powered Cloud Network Security Monitoring  
**Tech Stack:** Next.js, TypeScript, Express, PostgreSQL  
**Documentation:** [vpc-guardian/README.md](vpc-guardian/README.md)

### 🔐 SMB Security Suite
**Location:** `/smb-security-suite/`  
**Type:** Full-stack (TypeScript/Next.js + Node.js)  
**Description:** Complete AI-Native Security Platform for SMBs (Unified Dashboard)  
**Tech Stack:** Next.js, TypeScript, Express, PostgreSQL  
**Documentation:** [smb-security-suite/README.md](smb-security-suite/README.md)

### 🔐 SMB Security Suite (Unified)
**Location:** `/smb-security-suite-unified/`  
**Type:** Full-stack (TypeScript/Next.js + Node.js)  
**Description:** Alternative unified version of SMB Security Suite  
**Tech Stack:** Next.js, TypeScript, Express, PostgreSQL  
**Documentation:** [smb-security-suite-unified/README.md](smb-security-suite-unified/README.md)

## Other Projects

### 💼 WorkOS
**Location:** `/workos/`  
**Type:** Full-stack (TypeScript/Next.js + Node.js + Python ML)  
**Description:** Work management platform with AI/ML capabilities  
**Tech Stack:** Next.js, TypeScript, Express, PostgreSQL, Python/Flask  
**Documentation:** [workos/README.md](workos/README.md)

### 📝 SaaS Products Documentation
**Location:** `/saas-products/`  
**Type:** Documentation  
**Description:** Product documentation and alternatives  
**Contents:**
- Form builders & surveys
- Scheduling & booking tools

## Quick Start by Project Type

### Python Projects
```bash
# DDSP-Piano
pip install -r requirements.txt

# Attack Surface AI
cd attack-surface-ai
pip install -r requirements.txt
```

### TypeScript/Node.js Projects
```bash
# Example: LogCopilot
cd logcopilot/backend
npm install
npm run dev

cd ../frontend
npm install
npm run dev
```

### Docker Projects
Most projects include Docker Compose files:
```bash
cd <project-name>
docker-compose up -d
```

## Project Status

| Project | Status | Last Updated |
|---------|--------|--------------|
| DDSP-Piano | ✅ Active | - |
| Attack Surface AI | ✅ Active | - |
| LogCopilot | ✅ Active | - |
| PentestGPT | ✅ Active | - |
| SurfaceAI | ✅ Active | - |
| VPC Guardian | ✅ Active | - |
| SMB Security Suite | ✅ Active | - |
| WorkOS | ✅ Active | - |

## Contributing

Each project may have its own contribution guidelines. See:
- [CONTRIBUTING.md](CONTRIBUTING.md) for general guidelines
- Individual project READMEs for project-specific instructions

## License

All projects in this repository are licensed under the Apache 2.0 License unless otherwise specified. See [LICENSE](LICENSE) for details.
