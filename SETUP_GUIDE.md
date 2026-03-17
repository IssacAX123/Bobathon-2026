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

### Standalone Mode (Testing)

```bash
# Basic usage (uses gh CLI auth or environment variable)
py src/mcp_server.py https://github.com/owner/repo/issues/123

# With explicit token
set GITHUB_TOKEN=ghp_your_token_here
py src/mcp_server.py https://github.com/owner/repo/issues/123
```

The script will:
1. Fetch the issue
2. Analyze your codebase
3. Generate explanation and diagram
4. Ask if you want to post to GitHub

### Bob Integration (MCP Mode)

#### Step 1: Configure Bob

Add to Bob's MCP configuration file:

**Windows:**
```json
{
  "mcpServers": {
    "github-issue-analyzer": {
      "command": "py",
      "args": ["C:/path/to/Bobathon-2026/src/mcp_tool.py"],
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
      "args": ["/path/to/Bobathon-2026/src/mcp_tool.py"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

**Alternative (using system environment variable):**
```json
{
  "mcpServers": {
    "github-issue-analyzer": {
      "command": "py",
      "args": ["C:/path/to/Bobathon-2026/src/mcp_tool.py"]
    }
  }
}
```
(Token will be read from system GITHUB_TOKEN or GH_TOKEN environment variable)

#### Step 2: Use with Bob

```
You: "Bob, analyze this issue: https://github.com/owner/repo/issues/123"

Bob: [Uses analyze-github-issue tool]
     ✅ Analysis Complete and Posted!
     
     Issue: #123 - Fix login bug
     Relevant Files: 3
     - src/auth/login.py
     - src/utils/validation.py
     - tests/test_login.py
```

**With explicit token in command:**
```
You: "Bob, analyze this issue with my token: https://github.com/owner/repo/issues/123"
     Token: ghp_your_token_here
```

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

### Test 3: Run Analyzer (Dry Run)
```bash
py src/mcp_server.py https://github.com/owner/repo/issues/1
```
When prompted, type `n` to skip posting. You should see the analysis preview.

### Test 4: Full Run (Posts to GitHub)
```bash
py src/mcp_server.py https://github.com/owner/repo/issues/1
```
When prompted, type `y` to post. Check the issue on GitHub for the comment.

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
```bash
# Quick analysis of any issue
py src/mcp_server.py https://github.com/myorg/myrepo/issues/42
```

### For Teams Using Bob
```
Team Member: "Bob, analyze issue #42"
Bob: [Analyzes and posts to GitHub]
Team: [Sees analysis comment on issue]
```

### For CI/CD Pipelines
```bash
# Analyze new issues automatically
gh issue list --state open --limit 10 | while read issue; do
  py src/mcp_server.py $issue
done
```

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