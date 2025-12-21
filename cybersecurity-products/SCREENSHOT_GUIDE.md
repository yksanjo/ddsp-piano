# UI/UX Screenshot Creation Guide

## Overview
This guide provides detailed specifications for creating screenshots for all 4 AI Agent Security Platform products.

## Design System

### Color Palette
- **Primary Blue**: #0066FF - Trust, security, primary actions
- **Success Green**: #00C853 - Safe, compliant, positive states
- **Warning Yellow**: #FFB300 - Caution, review needed
- **Critical Red**: #E53935 - Threats, violations, errors
- **Background Dark**: #1E1E1E - Main background
- **Background Light**: #2D2D2D - Cards, panels
- **Text Primary**: #FFFFFF - Main text
- **Text Secondary**: #B0B0B0 - Secondary text
- **Border**: #404040 - Dividers, borders

### Typography
- **Font Family**: Inter (primary), JetBrains Mono (code)
- **Headers**: 24-32px, Bold
- **Body**: 14-16px, Regular
- **Metrics**: 18-24px, Semi-Bold
- **Code**: 13px, Regular

### Spacing
- **Unit**: 8px base unit
- **Card Padding**: 16px
- **Section Spacing**: 24px
- **Page Margin**: 32px

### Components
- **Cards**: 8px border radius, subtle shadow
- **Buttons**: 6px border radius, hover states
- **Inputs**: 4px border radius, focus states
- **Badges**: 12px border radius, pill shape

## Product 1: Autonomous Threat-Hunter

### Screenshot 1: Main Dashboard
**File**: `assets/screenshots/dashboard-main.png`
**Size**: 2880x1800px
**Elements**:
- Header with logo and navigation
- 4 metric cards (Active Threats, MTTD, MTTR, Detection Rate)
- Threat timeline chart (last 24 hours)
- Agent inventory panel (right side)
- Active investigations list (bottom)

### Screenshot 2: Investigation Workspace
**File**: `assets/screenshots/investigation-workspace.png`
**Elements**:
- Left: Investigation timeline
- Center: Evidence collection area
- Right: Playbook steps checklist
- Threat details panel

### Screenshot 3: Agent Inventory
**File**: `assets/screenshots/agent-inventory.png`
**Elements**:
- Table of all agents
- Health status indicators
- Risk scores with color coding
- Filter and search controls

## Product 2: AI Agent WAF

### Screenshot 1: Security Dashboard
**File**: `assets/screenshots/dashboard-main.png`
**Elements**:
- Attack statistics (blocked, prevented)
- Attack volume chart
- Attack type distribution
- Recent blocks table

### Screenshot 2: Input Analysis
**File**: `assets/screenshots/input-analysis.png`
**Elements**:
- Real-time input stream
- Risk scoring display
- Pattern detection highlights
- Block/Allow decision panel

## Product 3: Cross-Cloud Policy Manager

### Screenshot 1: Policy Dashboard
**File**: `assets/screenshots/dashboard-main.png`
**Elements**:
- Multi-cloud tabs (AWS, Azure, GCP)
- Policy compliance cards
- Violations panel
- Compliance score display

### Screenshot 2: Policy Definition
**File**: `assets/screenshots/policy-definition.png`
**Elements**:
- Code editor (left)
- Visual policy builder (right)
- Policy test results (bottom)

## Product 4: Zero-Trust AI Access

### Screenshot 1: Access Dashboard
**File**: `assets/screenshots/dashboard-main.png`
**Elements**:
- Machine identity metrics
- Agent inventory table
- Risk panel
- Active sessions list

### Screenshot 2: Authentication Flow
**File**: `assets/screenshots/auth-flow.png`
**Elements**:
- Flowchart diagram
- Step-by-step process
- Decision points
- Context indicators

## Export Specifications

### Resolution
- **Primary**: 2880x1800px (MacBook Pro Retina)
- **Thumbnail**: 1280x800px (for README)
- **Format**: PNG with transparency

### Quality
- **DPI**: 144 (Retina display)
- **Compression**: Optimized for web
- **File Size**: <500KB per image

### Naming Convention
- Use kebab-case: `dashboard-main.png`
- Include product prefix if needed
- Version numbers optional: `v1-dashboard-main.png`

## Tools & Resources

### Design Tools
- **Figma** (Recommended) - Collaborative design
- **Sketch** - Mac-only design tool
- **Adobe XD** - Alternative option

### Templates
- Use provided mockup specifications in `docs/mockups/`
- Follow design system guidelines
- Maintain consistency across products

### Icons & Assets
- Use consistent icon library (Material Icons, Feather Icons)
- Maintain icon size consistency (24px, 32px)
- Use SVG for scalability

## Checklist

Before exporting screenshots:
- [ ] Follow color palette exactly
- [ ] Use correct typography
- [ ] Maintain consistent spacing
- [ ] Include realistic data (not lorem ipsum)
- [ ] Show actual UI states (hover, active, etc.)
- [ ] Export at correct resolution
- [ ] Optimize file size
- [ ] Test on different displays
- [ ] Update README.md with image references

## Next Steps

1. Create mockups in Figma based on specifications
2. Review with team/stakeholders
3. Export screenshots at specified resolution
4. Add to `assets/screenshots/` directories
5. Update product README.md files
6. Test image loading and display
