# GitHub Issue Analyzer - Python Implementation

## Overview

This is a flexible, production-ready implementation of User Story 1 (Fetch and Analyze GitHub Issue) that can handle **unstructured** GitHub issues and intelligently extract Liberty package information.

## Key Features

### 🎯 Intelligent Package Detection
- **Multiple Detection Strategies**:
  - Direct regex pattern matching for `io.openliberty.*` and `com.ibm.ws.*`
  - Stack trace parsing for high-confidence identification
  - Code block detection for context-aware analysis
  - Context keyword analysis (error, exception, fails, etc.)

### 📊 Confidence Scoring
- **Base confidence**: 70%
- **Location bonuses**:
  - Stack trace: +25%
  - Code block: +20%
  - Title: +10%
- **Context keywords**: +5-20% per keyword
- **Package completeness**: +5-10% for fully qualified names

### 🔍 Flexible Analysis
- Handles unstructured issue descriptions
- Works with various issue formats
- Parses stack traces automatically
- Identifies packages in code blocks
- No strict formatting requirements

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set GitHub token (optional but recommended for higher rate limits)
export GITHUB_TOKEN="your_github_personal_access_token"
```

## Usage

### Command Line

```bash
# Basic usage
python github_issue_analyzer.py https://github.com/OpenLiberty/open-liberty/issues/12345

# With GitHub token
GITHUB_TOKEN="ghp_xxx" python github_issue_analyzer.py <issue_url>
```

### As a Library

```python
from github_issue_analyzer import GitHubIssueAnalyzer

# Initialize
analyzer = GitHubIssueAnalyzer(github_token="ghp_xxx")

# Analyze an issue
result = analyzer.analyze_issue("https://github.com/OpenLiberty/open-liberty/issues/12345")

# Check results
if result.success:
    print(f"Found {len(result.packages)} packages")
    for pkg in result.packages:
        print(f"  - {pkg.name} (confidence: {pkg.confidence:.0%})")
else:
    print(f"Error: {result.error_message}")

# Get JSON output
json_output = analyzer.to_json(result)
```

## Example Output

### Successful Analysis

```
Analyzing issue: https://github.com/OpenLiberty/open-liberty/issues/12345

✅ Analysis complete in 1234ms

Issue #12345: NullPointerException in JWT token validation
Author: developer123
Created: 2026-03-15T10:30:00Z

Identified 3 package(s):

1. io.openliberty.security.jwt
   Confidence: 95%
   Type: LIBERTY
   Location: stack_trace
   Context: ...at io.openliberty.security.jwt.JwtTokenValidator.va...

2. com.ibm.ws.security.token
   Confidence: 87%
   Type: IBM
   Location: code_block
   Context: ...when calling com.ibm.ws.security.token.TokenManage...

3. io.openliberty.security.common
   Confidence: 82%
   Type: LIBERTY
   Location: description
   Context: ...issue in io.openliberty.security.common during aut...
```

### JSON Output

```json
{
  "success": true,
  "analysis_time_ms": 1234,
  "error_message": null,
  "issue": {
    "number": 12345,
    "title": "NullPointerException in JWT token validation",
    "body": "...",
    "labels": ["bug", "security"],
    "url": "https://github.com/OpenLiberty/open-liberty/issues/12345",
    "created_at": "2026-03-15T10:30:00Z",
    "author": "developer123"
  },
  "packages": [
    {
      "name": "io.openliberty.security.jwt",
      "confidence": 0.95,
      "context": "at io.openliberty.security.jwt.JwtTokenValidator.validate(...)",
      "package_type": "LIBERTY",
      "location": "stack_trace"
    }
  ]
}
```

## Detection Strategies

### 1. Direct Pattern Matching
Finds packages mentioned anywhere in the issue:
```
"Issue in io.openliberty.security.jwt when validating tokens"
→ Detected: io.openliberty.security.jwt (confidence: 75%)
```

### 2. Stack Trace Parsing
High-confidence detection from stack traces:
```
at io.openliberty.security.jwt.JwtTokenValidator.validate(JwtTokenValidator.java:123)
→ Detected: io.openliberty.security.jwt (confidence: 95%)
```

### 3. Code Block Detection
Enhanced confidence for packages in code blocks:
```markdown
```java
import io.openliberty.security.jwt.JwtToken;
```
→ Detected: io.openliberty.security.jwt (confidence: 90%)
```

### 4. Context-Aware Scoring
Keywords increase confidence:
```
"NullPointerException in io.openliberty.security.jwt"
→ Base: 70% + Exception keyword: +15% = 85%
```

## Integration with Other Stories

This implementation provides the foundation for the other user stories:

### Story 2: Diagram Generation
```python
# Get packages from Story 1
result = analyzer.analyze_issue(issue_url)

# Pass to diagram generator (Story 2)
from diagram_generator import DiagramGenerator
generator = DiagramGenerator()
diagram = generator.generate_diagram(result.packages, result.issue)
```

### Story 3: Comment Posting
```python
# Get analysis from Story 1
result = analyzer.analyze_issue(issue_url)

# Format and post (Story 3)
from comment_poster import CommentPoster
poster = CommentPoster()
poster.post_analysis(issue_url, result)
```

### Story 4: MCP Tool
```python
# Orchestrate all stories
from mcp_tool import MCPTool
tool = MCPTool()
final_result = tool.analyze_issue(issue_url)
```

## Error Handling

The analyzer handles various error conditions gracefully:

```python
# Invalid URL
result = analyzer.analyze_issue("not-a-url")
# Returns: success=False, error_message="Invalid GitHub issue URL format"

# Issue not found
result = analyzer.analyze_issue("https://github.com/owner/repo/issues/999999")
# Returns: success=False, error_message="Issue not found or not accessible"

# Rate limit exceeded
result = analyzer.analyze_issue(issue_url)  # Without token, after 60 requests
# Returns: success=False, error_message="GitHub API rate limit exceeded"

# Network error
result = analyzer.analyze_issue(issue_url)  # When GitHub is down
# Returns: success=False, error_message="GitHub API error: 503"
```

## Performance

- **Target**: < 10 seconds per analysis
- **Typical**: 1-3 seconds
- **Factors**:
  - GitHub API latency: 500-2000ms
  - Package analysis: 100-500ms
  - Network conditions

## Testing

```bash
# Run unit tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=github_issue_analyzer tests/

# Test with real issue
python github_issue_analyzer.py https://github.com/OpenLiberty/open-liberty/issues/12345
```

## Configuration

### Environment Variables

- `GITHUB_TOKEN`: GitHub personal access token (optional)
  - Without token: 60 requests/hour
  - With token: 5000 requests/hour

### Customization

```python
# Custom confidence thresholds
analyzer = GitHubIssueAnalyzer()
analyzer.CONTEXT_KEYWORDS['critical'] = 1.25  # Add custom keyword

# Custom patterns
analyzer.LIBERTY_PATTERN = re.compile(r'your\.custom\.pattern')
```

## Limitations

- Requires internet connection to GitHub API
- Rate limited without authentication token
- Cannot access private repositories without proper token
- Package detection depends on issue content quality

## Future Enhancements

1. **Machine Learning**: Train model on historical issues for better detection
2. **Caching**: Cache issue data to reduce API calls
3. **Batch Processing**: Analyze multiple issues simultaneously
4. **Advanced Relationships**: Detect package dependencies from issue content
5. **Confidence Tuning**: Learn optimal confidence weights from feedback

## Contributing

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for guidelines.

## License

[Your License Here]