# How to Integrate with Bob (Roo-Cline)

This guide shows you how to integrate the GitHub Issue Analyzer MCP server with Bob (Roo-Cline) so you can analyze issues with simple commands.

## 📍 Step 1: Locate Bob's Configuration File

Bob's MCP configuration is stored in a JSON file. The location depends on your setup:

### Windows
```
C:\Users\YourUsername\AppData\Roaming\Code\User\globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json
```

Or check in VS Code settings:
1. Open VS Code
2. Press `Ctrl+Shift+P`
3. Type "Preferences: Open User Settings (JSON)"
4. Look for MCP configuration

### Linux/Mac
```
~/.config/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json
```

## 📝 Step 2: Add MCP Server Configuration

Open the configuration file and add this MCP server:

```json
{
  "mcpServers": {
    "github-issue-analyzer": {
      "command": "py",
      "args": [
        "c:/Users/IssacAbraham/Documents/misc/2026/Bobathon/Bobathon-2026/src/mcp_tool.py"
      ],
      "env": {
        "GITHUB_TOKEN": "your_github_token_here"
      }
    }
  }
}
```

**Important:** Replace the path with your actual path to `mcp_tool.py`

### If You Already Have Other MCP Servers

Add the new server to the existing configuration:

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "...",
      "args": ["..."]
    },
    "github-issue-analyzer": {
      "command": "py",
      "args": [
        "c:/Users/IssacAbraham/Documents/misc/2026/Bobathon/Bobathon-2026/src/mcp_tool.py"
      ],
      "env": {
        "GITHUB_TOKEN": "your_github_token_here"
      }
    }
  }
}
```

## 🔑 Step 3: Set Your GitHub Token

### Option A: In Configuration File (Shown Above)
Replace `"your_github_token_here"` with your actual GitHub token.

### Option B: Use System Environment Variable
Remove the `"env"` section and set the token in your system:

**Windows PowerShell:**
```powershell
[System.Environment]::SetEnvironmentVariable('GITHUB_TOKEN', 'ghp_your_token_here', 'User')
```

**Windows Command Prompt:**
```cmd
setx GITHUB_TOKEN "ghp_your_token_here"
```

Then your config becomes:
```json
{
  "mcpServers": {
    "github-issue-analyzer": {
      "command": "py",
      "args": [
        "c:/Users/IssacAbraham/Documents/misc/2026/Bobathon/Bobathon-2026/src/mcp_tool.py"
      ]
    }
  }
}
```

### Option C: Use GitHub CLI Authentication
If you've already run `gh auth login`, you can omit the token entirely:

```json
{
  "mcpServers": {
    "github-issue-analyzer": {
      "command": "py",
      "args": [
        "c:/Users/IssacAbraham/Documents/misc/2026/Bobathon/Bobathon-2026/src/mcp_tool.py"
      ]
    }
  }
}
```

## 🔄 Step 4: Restart Bob

After adding the configuration:
1. Close VS Code completely
2. Reopen VS Code
3. Open Bob/Roo-Cline extension

Or use the command palette:
1. Press `Ctrl+Shift+P`
2. Type "Developer: Reload Window"

## ✅ Step 5: Verify Integration

### Check Available Tools

In Bob's chat, type:
```
What tools do you have available?
```

Bob should list `analyze-github-issue` among the available tools.

### Test the Tool

Try analyzing an issue:
```
Analyze this GitHub issue: https://github.com/IssacAX123/Bobathon-2026/issues/1
```

Bob will:
1. Use the `analyze-github-issue` tool
2. Fetch the issue
3. Analyze your codebase
4. Generate explanation and diagram
5. Post the analysis to GitHub
6. Show you a summary

## 💬 How to Use with Bob

Once integrated, you can use natural language commands:

### Basic Analysis
```
You: "Analyze issue #1 in my repository"
You: "What files are affected by issue 123?"
You: "Help me understand this issue: https://github.com/owner/repo/issues/42"
```

### With Options
```
You: "Analyze this issue but don't post to GitHub: https://github.com/owner/repo/issues/5"
```

### Bob's Response
```
Bob: 🔍 Analyzing issue...
     
     ✅ Analysis Complete and Posted!
     
     Issue: #1 - Story 1: Implement GitHub Issue Fetching
     Relevant Files: 5
     - src/main/python/github_issue_analyzer.py
     - docs/user-stories/story-1-fetch-analyze.md
     - PERSON1_GITHUB.md
     - PERSON2_ANALYZER.md
     - PERSON3_DIAGRAM.md
     
     The analysis has been posted to GitHub!
     View at: https://github.com/IssacAX123/Bobathon-2026/issues/1
```

## 🔧 Advanced Configuration

### Custom Working Directory

If you want to analyze a different repository:

```json
{
  "mcpServers": {
    "github-issue-analyzer": {
      "command": "py",
      "args": [
        "c:/path/to/mcp_tool.py"
      ],
      "cwd": "c:/path/to/repository/to/analyze",
      "env": {
        "GITHUB_TOKEN": "your_token_here"
      }
    }
  }
}
```

### Multiple Analyzers for Different Repos

```json
{
  "mcpServers": {
    "analyzer-repo1": {
      "command": "py",
      "args": ["c:/path/to/mcp_tool.py"],
      "cwd": "c:/repos/project1",
      "env": {"GITHUB_TOKEN": "token1"}
    },
    "analyzer-repo2": {
      "command": "py",
      "args": ["c:/path/to/mcp_tool.py"],
      "cwd": "c:/repos/project2",
      "env": {"GITHUB_TOKEN": "token2"}
    }
  }
}
```

## 🐛 Troubleshooting

### "Tool not found" or "Unknown tool"

**Problem:** Bob doesn't see the tool

**Solutions:**
1. Check the path to `mcp_tool.py` is correct
2. Verify the JSON syntax is valid (use a JSON validator)
3. Restart VS Code completely
4. Check Bob's logs for errors

### "Failed to start MCP server"

**Problem:** The server won't start

**Solutions:**
1. Verify Python is installed: `py --version`
2. Install MCP package: `pip install mcp`
3. Check the command is correct (`py` vs `python` vs `python3`)
4. Look at the full path - use absolute paths, not relative

### "Authentication failed"

**Problem:** Can't access GitHub

**Solutions:**
1. Verify your GitHub token is correct
2. Check token has `repo` scope
3. Try `gh auth login` as alternative
4. Set GITHUB_TOKEN environment variable

### "No relevant files found"

**Problem:** Analyzer doesn't find files

**Solutions:**
1. Check you're in the correct repository directory
2. Verify `cwd` in config points to your repo
3. Make sure the repository has code files
4. Add more technical terms to the issue description

## 📊 What Bob Can Do With This Tool

Once integrated, Bob can:

✅ **Analyze any GitHub issue** you give it
✅ **Find relevant files** in your codebase automatically
✅ **Generate explanations** of what needs to be done
✅ **Create visual diagrams** showing affected components
✅ **Post analysis to GitHub** as a formatted comment
✅ **Help you understand** complex issues quickly

## 🎯 Example Workflow

```
You: "I need help with issue #42 in my repo"

Bob: "Let me analyze that issue for you."
     [Uses analyze-github-issue tool]
     
     "I've analyzed issue #42. It affects 3 files:
     - src/auth/login.py
     - src/utils/validation.py  
     - tests/test_login.py
     
     The issue is about login validation failing with special characters.
     I've posted a detailed analysis with a diagram to the issue.
     
     Would you like me to help you fix it?"

You: "Yes, let's start with login.py"

Bob: [Reads the file and helps you fix it]
```

## 🎉 You're Ready!

Your integration is complete when:
- ✅ Configuration file is updated
- ✅ GitHub token is set
- ✅ Bob is restarted
- ✅ Tool appears in Bob's available tools
- ✅ Test analysis works

Now you can analyze GitHub issues just by talking to Bob! 🚀

---

**Need Help?** Check SETUP_GUIDE.md for more details on authentication and troubleshooting.