# Bob MCP Setup Guide

This guide shows you how to configure Bob to use the GitHub Issue Analyzer MCP server.

## Quick Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `requests` - HTTP requests
- `pyyaml` - YAML parsing (required by analyzer)
- `Flask` - Web UI
- `mcp` - MCP SDK

### Step 2: Update Bob Configuration

Your Bob configuration file is at:
```
C:/Users/IssacAbraham/.bob/settings/mcp_settings.json
```

**Current Configuration:**
```json
{
  "mcpServers": {
    "github-issue-analyzer": {
      "command": "py",
      "args": [
        "c:/Users/IssacAbraham/Documents/misc/2026/Bobathon/Bobathon-2026/src/main/python/mcp_server.py"
      ],
      "env": {
        "GITHUB_TOKEN": "your_token_here"
      }
    }
  }
}
```

**Important**: Replace `your_token_here` with your actual GitHub token!

### Step 3: Restart Bob

**Complete restart required:**
1. Close Bob completely (not just the window)
2. Reopen Bob
3. Wait for MCP server to initialize

### Step 4: Verify Tools Available

Ask Bob:
```
What tools do you have available?
```

You should see:
- ✅ `analyze-github-issue`
- ✅ `generate-component-diagram`
- ✅ `post-analysis-comment`
- ✅ `full-pipeline`

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'yaml'"

**Solution:**
```bash
pip install pyyaml
```

Then restart Bob.

### Error: "MCP error -32000: Connection closed"

**Possible causes:**

1. **Missing dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Wrong Python path**
   
   Check which Python Bob is using:
   ```bash
   py --version
   ```
   
   If you have multiple Python installations, specify the full path:
   ```json
   {
     "mcpServers": {
       "github-issue-analyzer": {
         "command": "C:/Python312/python.exe",
         "args": ["c:/Users/IssacAbraham/Documents/misc/2026/Bobathon/Bobathon-2026/src/main/python/mcp_server.py"],
         "env": {
           "GITHUB_TOKEN": "your_token_here"
         }
       }
     }
   }
   ```

3. **File path incorrect**
   
   Verify the path exists:
   ```bash
   dir "c:/Users/IssacAbraham/Documents/misc/2026/Bobathon/Bobathon-2026/src/main/python/mcp_server.py"
   ```

4. **Import errors in MCP server**
   
   Test the server manually:
   ```bash
   cd c:/Users/IssacAbraham/Documents/misc/2026/Bobathon/Bobathon-2026/src/main/python
   python mcp_server.py
   ```
   
   Should output:
   ```
   Starting GitHub Issue Analyzer MCP Server...
   Tools available:
     - analyze-github-issue
     - generate-component-diagram
     - post-analysis-comment
     - full-pipeline
   Ready!
   ```

### Error: "No tools available"

**Solution:**

1. Check Bob's MCP settings for red dot/error indicator
2. Check Bob's logs for error messages
3. Verify configuration syntax is correct (valid JSON)
4. Restart Bob completely

### Error: "Request timed out"

This should be fixed with the async implementation, but if it still occurs:

1. Check network connectivity
2. Verify GitHub token is valid
3. Check GitHub API rate limits: https://api.github.com/rate_limit

## Testing the Setup

### Test 1: Check Tools

Ask Bob:
```
What tools do you have available?
```

Expected: List of 4 tools

### Test 2: Analyze an Issue

Ask Bob:
```
Analyze this issue: https://github.com/OpenLiberty/open-liberty/issues/12345
```

Expected: Package analysis with confidence scores

### Test 3: Full Pipeline

Ask Bob:
```
Run full analysis on https://github.com/OpenLiberty/open-liberty/issues/12345 with dry_run=true
```

Expected: Complete analysis with diagram (preview mode, not posted)

## Configuration Options

### Basic Configuration (Current)

```json
{
  "mcpServers": {
    "github-issue-analyzer": {
      "command": "py",
      "args": ["path/to/mcp_server.py"],
      "env": {
        "GITHUB_TOKEN": "your_token"
      }
    }
  }
}
```

### Advanced Configuration

```json
{
  "mcpServers": {
    "github-issue-analyzer": {
      "command": "C:/Python312/python.exe",
      "args": [
        "c:/Users/IssacAbraham/Documents/misc/2026/Bobathon/Bobathon-2026/src/main/python/mcp_server.py"
      ],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here",
        "PYTHONPATH": "c:/Users/IssacAbraham/Documents/misc/2026/Bobathon/Bobathon-2026/src/main/python"
      },
      "timeout": 30000
    }
  }
}
```

## Security Notes

⚠️ **Important**: The `.bob/` directory is in `.gitignore` to prevent committing your GitHub token!

**Never commit:**
- `C:/Users/IssacAbraham/.bob/settings/mcp_settings.json`
- Any file containing your GitHub token

**Safe to commit:**
- `src/main/python/mcp_server.py`
- `MCP_INTEGRATION.md`
- `requirements.txt`

## Next Steps

Once Bob is configured and working:

1. **Test individual tools** - Try each tool separately
2. **Test full pipeline** - Run complete analysis workflow
3. **Verify Flask UI** - Ensure web UI still works (see VERIFY_UI.md)
4. **Create issues** - Use Bob to analyze real issues

## Getting Help

If you encounter issues:

1. Check this guide's troubleshooting section
2. Review `MCP_INTEGRATION.md` for architecture details
3. Test MCP server manually (see troubleshooting)
4. Check Bob's error logs
5. Verify all dependencies are installed

## Summary

✅ Install dependencies: `pip install -r requirements.txt`
✅ Update Bob config with correct path and token
✅ Restart Bob completely
✅ Verify tools available
✅ Test with an issue

Your Bob is now ready to analyze GitHub issues! 🚀