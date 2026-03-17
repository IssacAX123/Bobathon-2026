# Story 4: MCP Tool - Workflow Orchestrator

## Overview

The MCP (Model Context Protocol) server provides a single tool that orchestrates the entire GitHub issue analysis workflow. This is the "glue" that ties Stories 1, 2, and 3 together into a seamless experience.

## Features

### Single Command Execution
```bash
# Analyze and post to GitHub
./mcp_server.py https://github.com/OpenLiberty/open-liberty/issues/12345

# Dry run (preview without posting)
./mcp_server.py https://github.com/OpenLiberty/open-liberty/issues/12345 --dry-run
```

### MCP Protocol Support
```bash
# Run as MCP server (for Bob integration)
./mcp_server.py --stdio
```

### Progress Feedback
```
🔍 Validating issue URL...
✓ URL validated

🔍 Fetching issue from GitHub...
✓ Issue #12345 fetched: "NullPointerException in JWT token validation"
✓ Found 2 package(s)

📊 Generating architecture diagram...
✓ Diagram generated

📝 Posting analysis to GitHub...
✓ Comment posted: https://github.com/.../issues/12345#comment-789
✓ Label 'bot-analyzed' added

✅ Analysis complete in 8.3 seconds!
```

## Architecture

### Workflow Steps

1. **Validate URL** - Ensures GitHub issue URL format is correct
2. **Fetch & Analyze** - Calls Story 1 (github_issue_analyzer.py)
3. **Generate Diagram** - Calls Story 2 (diagram_generator.py)
4. **Post Comment** - Calls Story 3 (comment_poster.py)
5. **Return Result** - Provides structured JSON response

### Components

```
mcp_server.py
├── WorkflowOrchestrator
│   ├── analyze_issue()      # Main workflow execution
│   ├── _validate_url()      # URL validation
│   ├── _log_progress()      # Progress feedback
│   └── _determine_failed_step()  # Error handling
├── AnalysisResult           # Data class for results
├── create_mcp_tool_definition()  # MCP tool spec
└── handle_mcp_request()     # MCP protocol handler
```

## Usage

### CLI Mode

```bash
# Basic usage
python mcp_server.py https://github.com/org/repo/issues/123

# Dry run mode
python mcp_server.py https://github.com/org/repo/issues/123 --dry-run

# With environment variable
export GITHUB_TOKEN='your_token'
python mcp_server.py https://github.com/org/repo/issues/123
```

### MCP Mode (for Bob)

```bash
# Start MCP server
python mcp_server.py --stdio

# Bob can then invoke:
# "Bob, analyze this issue: https://github.com/org/repo/issues/123"
```

### Programmatic Usage

```python
from mcp_server import WorkflowOrchestrator

# Create orchestrator
orchestrator = WorkflowOrchestrator(
    github_token='your_token',
    dry_run=False
)

# Execute workflow
result = orchestrator.analyze_issue(
    'https://github.com/org/repo/issues/123'
)

# Check result
if result.success:
    print(f"Analysis complete!")
    print(f"Packages found: {result.packages_found}")
    print(f"Comment URL: {result.comment_url}")
    print(f"Execution time: {result.execution_time_ms}ms")
else:
    print(f"Failed at step: {result.failed_step}")
    print(f"Error: {result.error_message}")
```

## Response Format

### Success Response

```json
{
  "success": true,
  "issue": {
    "number": 12345,
    "title": "NullPointerException in JWT token validation"
  },
  "packages_found": 2,
  "diagram_generated": true,
  "comment_url": "https://github.com/.../issues/12345#comment-789",
  "execution_time_ms": 8300,
  "error_message": null,
  "failed_step": null,
  "partial_results": null
}
```

### Error Response

```json
{
  "success": false,
  "issue": null,
  "packages_found": 0,
  "diagram_generated": false,
  "comment_url": null,
  "execution_time_ms": 1200,
  "error_message": "Issue not found or not accessible",
  "failed_step": "fetch-issue",
  "partial_results": null
}
```

## Error Handling

### Validation Errors

| Error | Failed Step | Message |
|-------|-------------|---------|
| Empty URL | validate-url | "Issue URL is required" |
| Invalid format | validate-url | "Invalid GitHub issue URL format" |
| Non-GitHub URL | validate-url | "URL must be a GitHub issue" |

### Runtime Errors

| Error | Failed Step | Behavior |
|-------|-------------|----------|
| GitHub API down | fetch-issue | Returns error, doesn't crash |
| Invalid token | fetch-issue | Returns auth error |
| Rate limit | fetch-issue | Returns error with reset time |
| Diagram failure | generate-diagram | Continues, posts without diagram |
| Post failure | post-comment | Returns error with details |

## MCP Tool Definition

```json
{
  "name": "analyze-github-issue",
  "description": "Analyzes a GitHub issue, identifies Liberty packages, generates architecture diagram, and posts analysis as a comment",
  "inputSchema": {
    "type": "object",
    "properties": {
      "issueUrl": {
        "type": "string",
        "description": "Full URL of the GitHub issue to analyze",
        "pattern": "^https://github(?:\\.[a-z0-9-]+)*\\.com/[^/]+/[^/]+/issues/\\d+$"
      },
      "dryRun": {
        "type": "boolean",
        "description": "If true, performs analysis but does not post to GitHub",
        "default": false
      }
    },
    "required": ["issueUrl"]
  }
}
```

## Integration with Bob

### Bob Configuration

Add to Bob's MCP server configuration:

```json
{
  "mcpServers": {
    "github-issue-analyzer": {
      "command": "python",
      "args": [
        "/path/to/Bobathon-2026/src/main/python/mcp_server.py",
        "--stdio"
      ],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Bob Usage

```
User: "Bob, analyze this issue: 
       https://github.com/OpenLiberty/open-liberty/issues/12345"

Bob: [Invokes analyze-github-issue tool]
     
     🔍 Fetching issue from GitHub...
     ✓ Issue #12345 fetched: "NullPointerException in JWT token validation"
     ✓ Found 2 package(s)
     
     📊 Generating architecture diagram...
     ✓ Diagram generated
     
     📝 Posting analysis to GitHub...
     ✓ Comment posted
     ✓ Label added: bot-analyzed
     
     ✅ Analysis complete in 8.3 seconds!
     
     View the full analysis at: 
     https://github.com/OpenLiberty/open-liberty/issues/12345#comment-789
```

## Performance

### Targets

| Metric | Target | Typical |
|--------|--------|---------|
| Total execution | <15s | 8-12s |
| URL validation | <10ms | <5ms |
| Issue fetch | <3s | 1-2s |
| Package analysis | <1s | 0.5s |
| Diagram generation | <1s | 0.3s |
| Comment posting | <5s | 2-3s |

### Timeout

- Hard timeout: 30 seconds
- After timeout: Returns partial results
- Logs timeout details for debugging

## Testing

### Manual Testing

```bash
# Test successful flow
./mcp_server.py https://github.com/OpenLiberty/open-liberty/issues/12345

# Test dry run
./mcp_server.py https://github.com/OpenLiberty/open-liberty/issues/12345 --dry-run

# Test invalid URL
./mcp_server.py https://invalid-url

# Test non-existent issue
./mcp_server.py https://github.com/OpenLiberty/open-liberty/issues/999999999
```

### Integration Testing

```python
import subprocess
import json

def test_mcp_server():
    # Run MCP server
    result = subprocess.run(
        ['python', 'mcp_server.py', 'https://github.com/org/repo/issues/1'],
        capture_output=True,
        text=True
    )
    
    # Parse result
    response = json.loads(result.stdout)
    
    # Verify
    assert response['success'] == True
    assert response['packages_found'] > 0
    assert response['comment_url'] is not None
```

## Troubleshooting

### Common Issues

**"Import could not be resolved"**
- These are type checking warnings, not runtime errors
- The imports work correctly when running the script

**"GITHUB_TOKEN not set"**
```bash
export GITHUB_TOKEN='your_token_here'
```

**"Invalid GitHub issue URL format"**
- Ensure URL matches: `https://github.com/owner/repo/issues/123`
- Supports GitHub Enterprise: `https://github.ibm.com/owner/repo/issues/123`

**"Issue not found or not accessible"**
- Verify the issue exists
- Check token has access to the repository
- For private repos, token needs `repo` scope

## Future Enhancements

- [ ] Batch analysis of multiple issues
- [ ] Webhook integration for automatic analysis
- [ ] Caching to avoid re-analyzing same issue
- [ ] Metrics and telemetry
- [ ] Retry logic with exponential backoff
- [ ] Support for pull requests
- [ ] Integration with Slack/Teams notifications

## Dependencies

- Story 1: github_issue_analyzer.py
- Story 2: diagram_generator.py
- Story 3: comment_poster.py
- Python 3.9+
- requests library
- pyyaml library

## License

Part of Bobathon 2026 project.