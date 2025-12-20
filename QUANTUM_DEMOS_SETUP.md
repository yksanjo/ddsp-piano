# Quantum Demos - GitHub Repository Setup Guide

This guide will help you create separate GitHub repositories for each quantum computing demo and push them to GitHub.

## 📋 Prerequisites

1. **GitHub Account** - You need a GitHub account
2. **GitHub Token** - Personal access token with `repo` scope
3. **GitHub Username** - Your GitHub username

### Setup GitHub Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scope: `repo` (full control)
4. Generate and copy the token
5. Set environment variables:

```bash
export GITHUB_TOKEN=ghp_your_token_here
export GITHUB_USERNAME=your-username
```

## 🚀 Quick Start

### Step 1: Create GitHub Repositories

This will create all the repositories on GitHub:

```bash
./create_quantum_demo_repos.sh
```

This creates:
- `quantum-coin-demo` - Superposition demonstration
- `quantum-twins-demo` - Entanglement visualization
- `grover-search-demo` - Quantum search algorithm
- `quantum-randomness-demo` - True randomness generation
- `quantum-teleportation-demo` - Quantum teleportation
- `quantum-noise-demo` - Simulator vs real hardware
- `quantum-art-generator` - Art/music from quantum measurements

### Step 2: Create Standalone Projects

Each demo needs to be extracted into its own project. The first demo (`quantum-coin-demo`) is already created as an example.

For the remaining demos, you can:
1. Copy the structure from `quantum-coin-demo`
2. Replace the component with the specific demo component
3. Update the README and package.json

### Step 3: Push to GitHub

Once all projects are ready:

```bash
./push_quantum_demos.sh
```

This will:
- Initialize git in each project
- Add GitHub remote
- Commit and push to GitHub

## 📁 Project Structure

Each demo follows this structure:

```
quantum-[name]-demo/
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── index.html
├── .gitignore
├── README.md
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── index.css
    └── utils/
        └── quantumSimulator.js
```

## 🎯 Demo Descriptions

### 1. Quantum Coin Demo
**Repository:** `quantum-coin-demo`  
**Description:** Interactive superposition demonstration - heads AND tails simultaneously  
**Status:** ✅ Complete

### 2. Quantum Twins Demo
**Repository:** `quantum-twins-demo`  
**Description:** Entanglement visualization - instant correlation across any distance  
**Status:** ⏳ Needs component extraction

### 3. Grover Search Demo
**Repository:** `grover-search-demo`  
**Description:** Quantum search algorithm - faster than classical search  
**Status:** ⏳ Needs component extraction

### 4. Quantum Randomness Demo
**Repository:** `quantum-randomness-demo`  
**Description:** True randomness generation for security applications  
**Status:** ⏳ Needs component extraction

### 5. Quantum Teleportation Demo
**Repository:** `quantum-teleportation-demo`  
**Description:** Teleport quantum information without physical transfer  
**Status:** ⏳ Needs to be created

### 6. Quantum Noise Demo
**Repository:** `quantum-noise-demo`  
**Description:** Compare perfect simulator vs noisy real quantum hardware  
**Status:** ⏳ Needs to be created

### 7. Quantum Art Generator
**Repository:** `quantum-art-generator`  
**Description:** Generate unique art and music from quantum measurements  
**Status:** ⏳ Needs to be created

## 🔧 Manual Setup (Alternative)

If you prefer to set up manually:

### For Each Demo:

1. **Create repository on GitHub:**
   - Go to https://github.com/new
   - Name: `quantum-[name]-demo`
   - Description: [from descriptions above]
   - Public
   - Don't initialize with README

2. **Initialize local project:**
   ```bash
   cd quantum-demos/quantum-[name]-demo
   git init
   git branch -M main
   git add .
   git commit -m "Initial commit: quantum-[name]-demo"
   git remote add origin https://github.com/YOUR_USERNAME/quantum-[name]-demo.git
   git push -u origin main
   ```

## 📝 Adding Topics to Repositories

After creating repos, add these topics to each:

- `quantum-computing`
- `education`
- `demo`
- `interactive`
- `react`
- `quantum-mechanics`
- `visualization`
- `teaching`
- `stem`

You can do this via GitHub UI or use the automation script.

## 🌐 Deployment

Each demo can be deployed independently:

### Vercel
```bash
cd quantum-demos/quantum-[name]-demo
vercel
```

### Netlify
```bash
cd quantum-demos/quantum-[name]-demo
netlify deploy --prod
```

## ✅ Checklist

- [ ] Set `GITHUB_TOKEN` and `GITHUB_USERNAME`
- [ ] Run `./create_quantum_demo_repos.sh`
- [ ] Create standalone projects for each demo
- [ ] Test each demo locally (`npm run dev`)
- [ ] Run `./push_quantum_demos.sh`
- [ ] Verify all repos on GitHub
- [ ] Deploy demos (optional)

## 🆘 Troubleshooting

**Repository already exists:**
- The script will skip existing repos
- Delete on GitHub if you want to recreate

**Push fails:**
- Make sure repository exists on GitHub
- Check your GitHub token has `repo` scope
- Verify remote URL is correct

**Component not found:**
- Make sure you've extracted components from main `quantum-demo` project
- Check file paths in imports

## 📚 Next Steps

1. Complete remaining demo projects
2. Add deployment badges to READMEs
3. Create demo video/gif for each
4. Add to portfolio/showcase
5. Share on social media!

---

**Made with ⚛️ for curious minds**



