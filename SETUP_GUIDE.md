# Setup Guide - GitHub Issue Analyzer

Complete guide for setting up and using the GitHub Issue Analyzer MCP server.

## 📋 Prerequisites

1. **Python 3.9+** - Check with: `py --version` or `python --version`
2. **GitHub CLI** - Install from https://cli.github.com/
3. **Git** - For codebase analysis

## 🔑 GitHub Authentication

You have **3 options** for GitHub authentication:

### Option 1: GitHub CLI (Easiest)
```bash
gh auth login
```
Follow the prompts to authenticate. This is the simplest method.

### Option 2: Environment Variable
Set your GitHub token as an environment variable:

**Windows (PowerShell):**
```powershell
$env:GITHUB_TOKEN = "ghp_your_token_here"
```

**Windows (Command Prompt):**
```cmd
set GITHUB_TOKEN=ghp_your_token_here
```

**Linux/Mac:**
```bash
export GITHUB_TOKEN=ghp_your_token_here
```

**Permanent (add to your profile):**
- Windows: Add to PowerShell profile or System Environment Variables
- Linux/Mac: Add to `~/.bashrc` or `~/.zshrc`

### Option 3: Pass Token Directly (When using with Bob)
You can pass the token as a parameter when calling the tool (see Bob integration below).

## 🎫 Creating a GitHub Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name (e.g., "Issue Analyzer")
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `public_repo` (if only analyzing public repos)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)

## 🚀 Installation

### 1. Install Python Dependencies
```bash
pip install mcp
```

That's it! The tool only needs the MCP package.

### 2. Verify GitHub CLI
```bash
gh --version
```

Should show: `gh version 2.x.x`

### 3. Test Authentication
```bash
gh auth status
```

Should show: `✓ Logged in to github.com`

## 💻 Usage

### Bob Integration (MCP Mode) - Recommended

See **BOB_MCP_SETUP.md** for complete setup instructions.

#### Quick Configuration

Add to Bob's MCP configuration file:

**Windows:**
```json
{
  "mcpServers": {
    "github-issue-analyzer": {
      "command": "py",
      "args": ["/path/to/project/src/main/python/mcp_server.py"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

**Linux/Mac:**
```json
{
  "mcpServers": {
    "github-issue-analyzer": {
      "command": "python3",
      "args": ["/path/to/project/src/main/python/mcp_server.py"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

#### Use with Bob

Bob now has 5 granular tools for step-by-step analysis:

```
You: "Analyze this issue: https://github.com/OpenLiberty/open-liberty/issues/12345"

Bob: [Uses fetch-github-issue]
     Shows issue details...
     
Bob: [Uses identify-liberty-packages]
     Found 3 packages with confidence scores...
     
Bob: "Would you like me to generate a diagram?"
You: "Yes"

Bob: [Uses generate-component-diagram]
     Shows Mermaid diagram...
     
Bob: "Would you like me to post this to GitHub?"
You: "Preview first"

Bob: [Uses format-analysis-comment with dry_run=true]
     Shows formatted comment preview...
     
You: "Post it"
Bob: [Uses post-github-comment]
     ✅ Posted to GitHub!
```

See **MCP_USAGE_EXAMPLES.md** for more examples.

## 🔒 Security Best Practices

### DO ✅
- Store tokens in environment variables
- Use tokens with minimal required scopes
- Rotate tokens regularly
- Use different tokens for different projects

### DON'T ❌
- Commit tokens to git repositories
- Share tokens in chat or email
- Use tokens with excessive permissions
- Store tokens in plain text files

## 🧪 Testing Your Setup

### Test 1: Check Authentication
```bash
gh auth status
```
Expected: `✓ Logged in to github.com`

### Test 2: Test Issue Fetching
```bash
gh issue view https://github.com/owner/repo/issues/1 --json number,title
```
Expected: JSON output with issue data

### Test 3: Test with Bob

Ask Bob:
```
What tools do you have available?
```

You should see 5 tools:
- fetch-github-issue
- identify-liberty-packages
- generate-component-diagram
- format-analysis-comment
- post-github-comment

### Test 4: Analyze an Issue

```
Analyze this issue: https://github.com/OpenLiberty/open-liberty/issues/12345
```

Bob will guide you through the step-by-step analysis.

## 🐛 Troubleshooting

### "gh: command not found"
**Solution:** Install GitHub CLI from https://cli.github.com/

### "authentication required"
**Solution:** Run `gh auth login` or set GITHUB_TOKEN environment variable

### "Failed to fetch issue"
**Possible causes:**
- Issue doesn't exist
- No access to private repository
- Invalid token
- Network issues

**Solution:** 
1. Verify issue URL is correct
2. Check authentication: `gh auth status`
3. Try accessing the issue in browser
4. Check token has `repo` scope

### "No relevant files found"
**This is normal if:**
- Issue doesn't mention specific technical terms
- Running from wrong directory
- Repository has no code files

**Solution:**
- Add more technical details to issue description
- Run from repository root directory
- Check that git repository is initialized

### "UnicodeEncodeError" on Windows
**Solution:** Already fixed in the code! UTF-8 encoding is automatically set.

### "Failed to post comment"
**Possible causes:**
- No write access to repository
- Issue is locked
- Token lacks permissions

**Solution:**
1. Check token has `repo` scope
2. Verify you have write access
3. Check if issue is locked

## 📊 What Gets Posted to GitHub

The analyzer posts a comment with:

```markdown
## 🤖 Automated Analysis by Bob

**Analyzed:** 2026-03-17 14:00 UTC

## Analysis of Issue #123

### Issue Summary
**Title:** Fix login bug
**Description:** Users cannot login...

### Relevant Files Identified
1. `src/auth/login.py`
2. `src/utils/validation.py`
3. `tests/test_login.py`

### Recommended Actions
1. Review the relevant files listed above
2. Understand the context by reading the issue description
3. Identify the root cause in the codebase
4. Implement a fix addressing the issue
5. Test thoroughly before submitting changes
6. Update documentation if needed

### Next Steps
- Assign this issue to a team member
- Create a branch for the fix
- Reference this issue in commits
- Submit a pull request when ready

### 📊 Visual Overview
[Mermaid diagram showing issue and affected files]

---
*This analysis was automatically generated.*
```

## 🎯 Use Cases

### For Individual Developers
Ask Bob to analyze issues step-by-step, giving you full control over each stage.

### For Teams Using Bob
```
Team Member: "Bob, analyze issue #42"
Bob: [Guides through analysis step-by-step]
Team: [Reviews each step before posting]
```

### For OpenLiberty Contributors
Bob can identify which Liberty packages are affected by an issue, helping with:
- Package ownership assignment
- Impact analysis
- Technical documentation

## 🔄 Updating

To get the latest version:
```bash
cd Bobathon-2026
git pull origin main
pip install --upgrade mcp
```

## 📞 Support

If you encounter issues:
1. Check this guide's troubleshooting section
2. Verify all prerequisites are installed
3. Test with a public repository first
4. Check GitHub CLI authentication

## 🎉 You're Ready!

Your setup is complete when:
- ✅ Python is installed
- ✅ GitHub CLI is installed and authenticated
- ✅ MCP package is installed
- ✅ Test run completes successfully

Now you can analyze any GitHub issue with a single command!