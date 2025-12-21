# How to Prevent Unrelated Projects in Cursor AI

## The Problem
When working with Cursor AI, it can sometimes create or add files from other projects if:
- You have multiple projects open in the same workspace
- Cursor AI references files from your file history
- You accidentally include unrelated directories

## Solutions

### 1. Use `.cursorrules` File (Already Created)
I've created a `.cursorrules` file in this repository that tells Cursor AI:
- What belongs in this repository (DDSP-Piano only)
- What doesn't belong (security projects, SaaS products, etc.)
- Patterns to watch for

**This file is automatically read by Cursor AI** and helps prevent accidental additions.

### 2. Use Separate Workspaces
**Best Practice:** Open each project in its own Cursor workspace:
- `/path/to/ddsp-piano` - Only DDSP-Piano files
- `/path/to/other-project` - Separate workspace

**How to do this:**
1. In Cursor: `File > Open Folder`
2. Select ONLY the project directory you want to work on
3. Don't open parent directories that contain multiple projects

### 3. Check Repository Before Committing
Before committing, always check:
```bash
git status
git diff
```

Look for:
- Unexpected directories
- Files that don't match the project domain
- TypeScript/JavaScript files in a Python-only project

### 4. Use `.gitignore` Strategically
The `.gitignore` file already excludes common unrelated file patterns. Keep it updated.

### 5. Set Clear Context in Cursor
When starting a new task in Cursor AI:
- **Be explicit:** "I'm working on DDSP-Piano music synthesis"
- **Mention scope:** "Only create files related to piano/MIDI/audio"
- **Set boundaries:** "Don't create any security or web app projects"

### 6. Review File Structure Regularly
Run this command to see what's in your repository:
```bash
find . -maxdepth 2 -type d ! -name ".git" ! -name "__pycache__" | sort
```

### 7. Use Git Hooks (Optional)
Create a pre-commit hook to check for unrelated files:
```bash
#!/bin/sh
# .git/hooks/pre-commit

# Check for unrelated project directories
for dir in attack-surface flowboard workos saas-products; do
  if [ -d "$dir" ]; then
    echo "ERROR: Unrelated project directory found: $dir"
    echo "This repository is for DDSP-Piano only!"
    exit 1
  fi
done
```

## Quick Checklist Before Committing

- [ ] Only DDSP-Piano related files?
- [ ] No TypeScript/JavaScript projects?
- [ ] No security/cybersecurity projects?
- [ ] No SaaS product documentation?
- [ ] No unrelated markdown files?
- [ ] Python files only (except config files)?

## What This Repository Should Contain

✅ **Keep:**
- `ddsp_piano/` - Core package
- `assets/` - Project assets
- Python scripts (synthesize, evaluate, train, preprocess)
- Configuration files (requirements.txt, pyproject.toml, .gin files)
- README.md, LICENSE

❌ **Remove:**
- Any directory that's not `ddsp_piano/` or `assets/`
- TypeScript/JavaScript projects
- Security/cybersecurity tools
- SaaS product documentation
- Business/product management tools

## If You Accidentally Add Unrelated Files

1. **Don't commit yet!**
2. Remove the files: `git rm -r <unrelated-directory>`
3. Check again: `git status`
4. Commit only DDSP-Piano files

## Summary

The `.cursorrules` file I created will help, but the best practice is:
1. **One project per workspace** in Cursor
2. **Check `git status`** before committing
3. **Be explicit** with Cursor AI about project scope
4. **Review changes** before pushing to GitHub

