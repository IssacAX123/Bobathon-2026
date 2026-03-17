# MCP Integration for GitHub Issue Analyzer

This document explains how the GitHub Issue Analyzer integrates with Bob via MCP (Model Context Protocol).

## Overview

The MCP server (`src/main/python/mcp_server.py`) wraps the production pipeline as tools that Bob can use:

1. **analyze-github-issue** - Analyzes issues to identify Liberty packages
2. **generate-component-diagram** - Creates Mermaid diagrams from analysis
3. **post-analysis-comment** - Posts comprehensive analysis to GitHub
4. **full-pipeline** - Runs complete analysis workflow

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Bob IDE                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              MCP Client (Built-in)                    │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │ stdio
                           │
┌──────────────────────────▼──────────────────────────────────┐
│              MCP Server (mcp_server.py)                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Tool 1: analyze-github-issue                         │  │
│  │  Tool 2: generate-component-diagram                   │  │
│  │  Tool 3: post-analysis-comment                        │  │
│  │  Tool 4: full-pipeline                                │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌───────────────┐  ┌──────────────┐  ┌──────────────┐
│   Analyzer    │  │   Diagram    │  │   Comment    │
│  (Story 1)    │  │  Generator   │  │   Poster     │
│               │  │  (Story 2)   │  │  (Story 3)   │
└───────────────┘  └──────────────┘  └──────────────┘
```

## Production Code Integration

The MCP server **wraps** existing production code without modifying it:

- **github_issue_analyzer.py** - Unchanged, used as-is
- **diagram_generator.py** - Unchanged, used as-is  
- **comment_poster.py** - Unchanged, used as-is
- **web_app.py** - Unchanged, Flask UI still works

This means:
- ✅ Flask web UI continues to work
- ✅ CLI tools continue to work
- ✅ Bob can now use the same functionality via MCP
- ✅ No code duplication

## Tools Available to Bob

### 1. analyze-github-issue

Analyzes a GitHub issue to identify Liberty packages.

**Input:**
```json
{
  "issue_url": "https://github.com/owner/repo/issues/123"
}
```

**Output:**
- Package list with confidence scores
- Full JSON for downstream tools
- Analysis time

**Example:**
```
Bob: "Analyze this issue: https://github.com/OpenLiberty/open-liberty/issues/12345"
```

### 2. generate-component-diagram

Generates Mermaid diagram from analysis results.

**Input:**
```json
{
  "analysis_json": "{...JSON from analyze-github-issue...}"
}
```

**Output:**
- Mermaid diagram code
- Additional packages (if any)

**Example:**
```
Bob: "Generate a diagram from this analysis: {...}"
```

### 3. post-analysis-comment

Posts comprehensive analysis to GitHub issue.

**Input:**
```json
{
  "issue_url": "https://github.com/owner/repo/issues/123",
  "analysis_json": "{...}",
  "diagram": "```mermaid\n...\n```",
  "dry_run": false
}
```

**Output:**
- Success/failure status
- Comment URL (if posted)

**Example:**
```
Bob: "Post this analysis to the issue with dry_run=true"
```

### 4. full-pipeline

Runs complete workflow: analyze → diagram → post.

**Input:**
```json
{
  "issue_url": "https://github.com/owner/repo/issues/123",
  "post_comment": true,
  "dry_run": false
}
```

**Output:**
- Complete analysis summary
- Diagram
- Comment status

**Example:**
```
Bob: "Run full analysis on https://github.com/OpenLiberty/open-liberty/issues/12345"
```

## Configuration

Bob's MCP configuration is at: `C:/Users/IssacAbraham/.bob/settings/mcp_settings.json`

```json
{
  "mcpServers": {
    "github-issue-analyzer": {
      "command": "py",
      "args": ["c:/Users/IssacAbraham/Documents/misc/2026/Bobathon/Bobathon-2026/src/main/python/mcp_server.py"],
      "env": {
        "GITHUB_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Usage Examples

### Example 1: Quick Analysis

```
User: "Analyze issue #12345 in OpenLiberty/open-liberty"

Bob uses: analyze-github-issue
Result: Package list with confidence scores
```

### Example 2: Full Pipeline

```
User: "Analyze and post analysis for https://github.com/OpenLiberty/open-liberty/issues/12345"

Bob uses: full-pipeline
Result: Analysis posted to GitHub with diagram and recommendations
```

### Example 3: Step-by-Step

```
User: "Analyze this issue: https://github.com/OpenLiberty/open-liberty/issues/12345"
Bob uses: analyze-github-issue
Bob: "Found 3 packages: io.openliberty.security.ltpa, ..."

User: "Generate a diagram"
Bob uses: generate-component-diagram
Bob: "Here's the diagram: [mermaid code]"

User: "Post it to GitHub"
Bob uses: post-analysis-comment
Bob: "Posted! URL: https://github.com/..."
```

## Benefits

1. **No Code Duplication** - Reuses production code
2. **Consistent Results** - Same logic as Flask UI
3. **Flexible Workflow** - Bob can use tools individually or together
4. **Async Execution** - No timeouts with proper async handling
5. **Dry Run Support** - Preview before posting

## Testing

### Test MCP Server Standalone

```bash
cd src/main/python
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

### Test with Bob

1. Restart Bob completely
2. Check MCP settings for errors (red dot)
3. Ask Bob: "What tools do you have available?"
4. Should see: analyze-github-issue, generate-component-diagram, etc.
5. Test: "Analyze issue https://github.com/OpenLiberty/open-liberty/issues/12345"

## Troubleshooting

### MCP Server Not Starting

- Check Python path: `py --version`
- Check MCP package: `pip show mcp`
- Check file path in mcp_settings.json
- Check Bob's logs for errors

### Tools Not Appearing

- Restart Bob completely
- Check mcp_settings.json syntax
- Verify GITHUB_TOKEN is set
- Check server stderr output

### Timeouts

- All subprocess calls use `run_in_executor`
- Async operations don't block event loop
- If still timing out, check network/GitHub API

## Future Enhancements

- Add caching for repeated analyses
- Support batch processing multiple issues
- Add webhook integration for automatic analysis
- Integrate with CI/CD pipelines