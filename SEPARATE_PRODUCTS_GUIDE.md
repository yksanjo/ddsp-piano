# Guide: Separating Products into Individual Repositories

This guide explains how to separate each product from the SMB Security Suite into its own GitHub repository.

## Products to Separate

1. ✅ **SurfaceAI** - Attack Surface Monitor (`surfaceai/`)
2. **LogCopilot** - Log Intelligence Platform (`logcopilot/`)
3. **VPC Guardian** - Cloud Network Monitor (`vpc-guardian/`)
4. **PentestGPT** - Continuous Pentest Assistant (`pentestgpt/`)
5. **SMB Security Suite** - Unified Dashboard (`smb-security-suite/`)

## Repository Structure

Each product should have:

```
product-name/
├── README.md              # Comprehensive product README
├── .gitignore
├── docker-compose.yml
├── SETUP_GITHUB.md        # Instructions for GitHub setup
├── screenshots/
│   ├── README.md
│   └── .gitkeep
├── backend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── Dockerfile
│   ├── .env.example
│   └── src/
│       ├── index.ts
│       ├── routes/
│       ├── services/
│       ├── db/
│       └── ...
└── frontend/
    ├── package.json
    ├── tsconfig.json
    ├── next.config.js
    ├── tailwind.config.js
    ├── Dockerfile
    └── app/
        └── ...
```

## Steps for Each Product

### 1. Create Product Directory

```bash
cd /Users/yoshikondo/ddsp-piano
mkdir -p product-name/{backend/src,frontend/app,docker,screenshots}
```

### 2. Copy Relevant Files

From `smb-security-suite/`, copy:
- Product-specific routes
- Product-specific services
- Product-specific database tables
- Product-specific frontend pages
- Shared utilities (auth, db, etc.)

### 3. Create Comprehensive README

Each README should include:
- Product overview and value proposition
- Features list
- Quick start guide
- Screenshots section
- API documentation
- Pricing information
- Architecture overview
- Roadmap

### 4. Improve UI/UX

- Modern, thoughtful design
- Consistent color scheme
- Responsive layout
- Accessible components
- Loading states
- Error handling
- Empty states

### 5. Add Screenshots

- Dashboard view
- Main feature views
- Settings/configuration
- Use placeholder images initially
- Document in screenshots/README.md

### 6. Set Up Git Repository

```bash
cd product-name
git init
git add .
git commit -m "Initial commit: [Product Name]"
git remote add origin https://github.com/YOUR_USERNAME/product-name.git
git push -u origin main
```

## Product-Specific Details

### SurfaceAI (Attack Surface Monitor)

**Files to Copy:**
- `backend/src/routes/attackSurface.ts`
- `backend/src/services/attackSurface/githubScanner.ts`
- `backend/src/services/ai/openai.ts` (shared)
- `frontend/app/attack-surface/page.tsx`
- Database tables: `github_repos`, `attack_surface_findings`

**Dependencies:**
- `@octokit/rest` (GitHub API)
- `openai` (AI explanations)

### LogCopilot (Log Intelligence)

**Files to Copy:**
- `backend/src/routes/logIntelligence.ts`
- `backend/src/services/ai/openai.ts` (shared)
- `frontend/app/logs/page.tsx`
- Database tables: `log_sources`, `log_anomalies`

**Dependencies:**
- `openai` (AI analysis)
- `@opentelemetry/api` (optional)

### VPC Guardian (Cloud Monitor)

**Files to Copy:**
- `backend/src/routes/cloudMonitor.ts`
- `backend/src/services/ai/openai.ts` (shared)
- `frontend/app/cloud/page.tsx`
- Database tables: `cloud_accounts`, `cloud_network_findings`

**Dependencies:**
- `@aws-sdk/client-*` (AWS integration)
- `openai` (AI explanations)

### PentestGPT (Pentest Assistant)

**Files to Copy:**
- `backend/src/routes/pentest.ts`
- `backend/src/services/ai/openai.ts` (shared)
- `frontend/app/pentest/page.tsx`
- Database tables: `pentest_sessions`, `pentest_findings`

**Dependencies:**
- `openai` (AI copilot)

### SMB Security Suite (Unified Dashboard)

**Files to Copy:**
- All routes (aggregates all products)
- `backend/src/routes/dashboard.ts`
- `frontend/app/dashboard/page.tsx`
- All database tables

**Dependencies:**
- All product dependencies

## Shared Components

Each product needs these shared components:

### Backend
- `src/db/index.ts` - Database connection
- `src/db/migrate.ts` - Migration runner
- `src/middleware/auth.ts` - Authentication
- `src/utils/logger.ts` - Logging
- `src/routes/auth.ts` - Auth routes
- `src/routes/organizations.ts` - Org management

### Frontend
- `lib/api.ts` - API client
- `stores/authStore.ts` - Auth state
- `components/Layout.tsx` - Layout wrapper
- `app/login/page.tsx` - Login page
- `app/organizations/page.tsx` - Org selection

## UI/UX Improvements

### Design Principles

1. **Modern Aesthetics**
   - Gradient backgrounds
   - Rounded corners (xl, 2xl)
   - Subtle shadows
   - Smooth transitions

2. **Color Coding**
   - Critical: Red
   - High: Orange
   - Medium: Yellow
   - Low: Blue
   - Success: Green

3. **Typography**
   - Clear hierarchy
   - Readable font sizes
   - Proper spacing

4. **Interactions**
   - Hover states
   - Loading indicators
   - Error messages
   - Success feedback

5. **Responsive Design**
   - Mobile-first approach
   - Breakpoints: sm, md, lg, xl
   - Flexible grids

## Screenshot Requirements

Each product needs:

1. **Dashboard/Overview** - Main landing page
2. **Feature Views** - Product-specific pages
3. **Settings** - Configuration pages
4. **Empty States** - When no data exists
5. **Loading States** - During operations

### Screenshot Specs
- Format: PNG
- Resolution: 1920x1080 minimum
- Optimize: < 500KB
- Style: Consistent across products

## GitHub Setup Script

Use the provided `setup-github.sh` script:

```bash
./setup-github.sh product-name "Product Description"
```

This will:
1. Initialize git repository
2. Create initial commit
3. Set up remote (you'll need to create repo on GitHub first)
4. Push to GitHub

## Next Steps

1. ✅ SurfaceAI - Complete
2. Create LogCopilot repository
3. Create VPC Guardian repository
4. Create PentestGPT repository
5. Update SMB Security Suite (unified dashboard)

## Checklist for Each Product

- [ ] Directory structure created
- [ ] Backend files copied and adapted
- [ ] Frontend files copied and improved
- [ ] Database schema extracted
- [ ] README.md comprehensive
- [ ] Screenshots directory with README
- [ ] .gitignore configured
- [ ] docker-compose.yml set up
- [ ] SETUP_GITHUB.md created
- [ ] UI/UX improvements applied
- [ ] Git repository initialized
- [ ] Pushed to GitHub

## Notes

- Each product is independently deployable
- Shared code is duplicated (not ideal, but necessary for separation)
- Consider creating a shared package later
- Each product has its own pricing and branding

