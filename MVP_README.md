# GitHub Issue Analyzer - Minimal MVP

A minimal MCP server that reads GitHub issues, analyzes your codebase, generates explanations with diagrams, and posts the analysis back to the issue.

## 🎯 What It Does

1. **Reads GitHub Issues** - Fetches issue title and description
2. **Analyzes Codebase** - Finds relevant files based on issue content
3. **Generates Explanation** - Creates actionable steps to resolve the issue
4. **Creates Diagram** - Visual Mermaid diagram showing affected files
5. **Posts to GitHub** - Adds analysis as a comment on the issue

## 🚀 Quick Start

### Prerequisites

1. **Python 3.9+**
2. **GitHub CLI** - Install from https://cli.github.com/
3. **GitHub Authentication**
   ```bash
   gh auth login
   ```

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or just install MCP
pip install mcp
```

### Usage

#### As MCP Tool (With Bob) - Recommended

1. **Configure Bob** to use this MCP server (add to Bob's config):

```json
{
  "mcpServers": {
    "github-issue-analyzer": {
      "command": "python",
      "args": ["src/main/python/mcp_server.py"],
      "cwd": "/path/to/this/repo",
      "env": {
        "GITHUB_TOKEN": "your_token_here"
      }
    }
  }
}
```

2. **Use with Bob** - Step-by-step workflow:

```
You: "Analyze this issue: https://github.com/OpenLiberty/open-liberty/issues/12345"

Bob: [Uses fetch-github-issue]
     Shows issue details...
     
Bob: [Uses identify-liberty-packages]
     Found packages: io.openliberty.security.ltpa (95% confidence)
     
Bob: "Would you like a diagram?"
You: "Yes"

Bob: [Uses generate-component-diagram]
     Shows Mermaid diagram...
     
Bob: "Post to GitHub?"
You: "Preview first"

Bob: [Uses format-analysis-comment]
     Shows formatted preview...
     
You: "Post it"
Bob: [Uses post-github-comment]
     ✅ Posted!
```

See **BOB_MCP_SETUP.md** for complete setup instructions.

## 📊 Example Output

When you run the analyzer, it posts a comment like this to the GitHub issue:

```markdown
## 🤖 Automated Analysis by Bob

**Analyzed:** 2026-03-17 12:00 UTC

## Analysis of Issue #123

### Issue Summary
**Title:** Fix login bug

**Description:** Users cannot login when using special characters...

### Relevant Files Identified
1. `src/auth/login.py`
2. `src/utils/validation.py`
3. `tests/test_login.py`

### Recommended Actions

1. **Review the relevant files** listed above
2. **Understand the context** by reading the issue description
3. **Identify the root cause** in the codebase
4. **Implement a fix** addressing the issue
5. **Test thoroughly** before submitting changes
6. **Update documentation** if needed

### Next Steps

- Assign this issue to a team member familiar with the affected files
- Create a branch for the fix
- Reference this issue in your commit messages
- Submit a pull request when ready

### 📊 Visual Overview

```mermaid
graph TD
    Issue["Issue #123<br/>Fix login bug"]
    F0["src/auth/login.py"]
    F1["src/utils/validation.py"]
    F2["tests/test_login.py"]
    Issue --> F0
    Issue --> F1
    Issue --> F2
    
    style Issue fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style F0 fill:#4dabf7,stroke:#1971c2
    style F1 fill:#4dabf7,stroke:#1971c2
    style F2 fill:#4dabf7,stroke:#1971c2
```

---
*This analysis was automatically generated. Please review and adjust as needed.*
```

## 🔧 How It Works

### 1. Fetch Issue
Uses GitHub CLI (`gh issue view`) to fetch issue data:
- Issue number
- Title
- Description

### 2. Find Relevant Files
Analyzes the codebase to find files related to the issue:
- Extracts keywords from issue title and description
- Searches file names and content for matches
- Returns top 5 most relevant files

### 3. Generate Explanation
Creates a structured explanation including:
- Issue summary
- List of relevant files
- Recommended action steps
- Next steps for the team

### 4. Create Diagram
Generates a Mermaid diagram showing:
- The issue as the central node
- Connected relevant files
- Color-coded for clarity

### 5. Post to GitHub
Uses GitHub CLI (`gh issue comment`) to post the analysis as a comment on the issue.

## 🎯 Use Cases

### For Developers
- **Quick Context**: Instantly see which files are related to an issue
- **Save Time**: No manual searching through the codebase
- **Visual Understanding**: Diagram shows relationships at a glance

### For Team Leads
- **Faster Triage**: Quickly assign issues to the right people
- **Better Planning**: Understand scope immediately
- **Consistent Analysis**: Same quality every time

### For New Team Members
- **Learn Codebase**: See how files relate to issues
- **Understand Structure**: Visual diagrams help onboarding
- **Get Context**: Clear explanations of what needs to be done

## 🛠️ Configuration

### Environment Variables

- `GITHUB_TOKEN` (optional): GitHub personal access token for private repos
  ```bash
  export GITHUB_TOKEN=ghp_your_token_here
  ```

### Customization

Edit `src/main/python/mcp_server.py` to customize tool behavior.

Edit `config/package_keywords.yaml` to add more Liberty package mappings.

## 📝 MCP Tools Available

Bob has 5 granular tools:

1. **fetch-github-issue** - Get issue details
2. **identify-liberty-packages** - Find affected packages
3. **generate-component-diagram** - Create Mermaid diagram
4. **format-analysis-comment** - Format comprehensive comment
5. **post-github-comment** - Post to GitHub (dry-run by default)

See **MCP_USAGE_EXAMPLES.md** for detailed examples.

## 🧪 Testing

Test with Bob:

```
You: "What tools do you have available?"
Bob: Lists 5 tools...

You: "Analyze this issue: https://github.com/OpenLiberty/open-liberty/issues/12345"
Bob: Guides you through step-by-step analysis...
```

## 🚨 Troubleshooting

### "gh: command not found"
Install GitHub CLI: https://cli.github.com/

### "authentication required"
Run: `gh auth login`

### "Failed to post comment"
Check permissions: `gh auth status`

### "No relevant files found"
- Issue may not contain specific technical terms
- Try adding more keywords to the issue description
- Check that you're running from the correct repository directory

## 📈 Success Metrics

- ⚡ Analysis completes in <10 seconds
- 📂 Finds relevant files 80%+ of the time
- 📊 Diagrams render correctly in GitHub
- 💬 Comments are well-formatted and helpful

## 🎉 What Makes This Implementation Special

✅ **Granular Tools** - Bob orchestrates 5 focused tools
✅ **Step-by-Step** - Full visibility and control at each stage
✅ **OpenLiberty Focus** - Specialized for Liberty package analysis
✅ **Async Execution** - No timeouts with proper async handling
✅ **Dry-Run Support** - Preview before posting
✅ **Comprehensive Output** - Detailed technical documentation

## 🚀 Current Features

- ✅ GitHub issue fetching
- ✅ Liberty package identification with confidence scores
- ✅ Mermaid diagram generation
- ✅ Comprehensive technical documentation
- ✅ LTPA security explanations
- ✅ Configuration examples
- ✅ Troubleshooting guides

## 📄 License

Hackathon project - 2026

---

**Built for Bobathon 2026** 🤖