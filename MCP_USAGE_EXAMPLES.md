# MCP Usage Examples

This guide shows how Bob can use the GitHub Issue Analyzer MCP tools.

## Two Approaches

### Approach 1: Step-by-Step (Recommended for Bob)

Bob orchestrates the workflow, using individual tools and making decisions at each step.

**Benefits:**
- ✅ Bob can see results at each stage
- ✅ Bob can adjust based on findings
- ✅ Bob can explain what's happening
- ✅ More flexible and interactive

**Example conversation:**

```
User: "Analyze this issue: https://github.com/OpenLiberty/open-liberty/issues/12345"

Bob: [Uses analyze-github-issue tool]
Bob: "I found 3 Liberty packages:
      - io.openliberty.security.ltpa (95% confidence)
      - com.ibm.ws.crypto.ltpakeyutil (90% confidence)
      - io.openliberty.security.utility (85% confidence)
      
      Would you like me to generate a diagram?"

User: "Yes, create a diagram"

Bob: [Uses generate-component-diagram tool]
Bob: "Here's the component diagram showing the relationships:
      [Mermaid diagram displayed]
      
      Should I post this analysis to the GitHub issue?"

User: "Yes, but use dry-run first"

Bob: [Uses post-analysis-comment with dry_run=true]
Bob: "Here's a preview of what would be posted:
      [Shows formatted comment]
      
      Looks good?"

User: "Perfect, post it for real"

Bob: [Uses post-analysis-comment with dry_run=false]
Bob: "✅ Posted! https://github.com/OpenLiberty/open-liberty/issues/12345#comment-123"
```

### Approach 2: Full Pipeline (Quick but Less Interactive)

One tool does everything automatically.

**Benefits:**
- ✅ Fast - one command
- ✅ Consistent workflow
- ✅ Good for batch processing

**Drawbacks:**
- ❌ Less interactive
- ❌ Bob can't adjust mid-workflow
- ❌ All-or-nothing approach

**Example conversation:**

```
User: "Run full analysis on https://github.com/OpenLiberty/open-liberty/issues/12345"

Bob: [Uses full-pipeline tool]
Bob: "✅ Complete analysis done!
      - Found 3 packages
      - Generated diagram
      - Posted to GitHub
      
      View at: https://github.com/OpenLiberty/open-liberty/issues/12345#comment-123"
```

## Recommended Workflow for Bob

**Bob should use the step-by-step approach** because:

1. **Better user experience** - User sees progress
2. **More control** - Bob can explain findings
3. **Flexible** - Can adjust based on results
4. **Educational** - User learns what's happening

## Tool Descriptions

### 1. analyze-github-issue

**Purpose**: Analyze issue to identify Liberty packages

**Input:**
```json
{
  "issue_url": "https://github.com/owner/repo/issues/123"
}
```

**Output:**
- Package list with confidence scores
- Issue metadata
- Full JSON for next steps

**When to use:**
- First step in any analysis
- User asks to "analyze an issue"
- Need to identify packages

**Example Bob usage:**
```
User: "What packages are mentioned in issue #12345?"
Bob: [Uses analyze-github-issue]
Bob: "Found 3 packages: ..."
```

### 2. generate-component-diagram

**Purpose**: Create Mermaid diagram from analysis

**Input:**
```json
{
  "analysis_json": "{...from analyze-github-issue...}"
}
```

**Output:**
- Mermaid diagram code
- Additional packages (if >5 found)

**When to use:**
- After analyzing an issue
- User asks for "diagram" or "visualization"
- Want to show package relationships

**Example Bob usage:**
```
User: "Show me a diagram of the affected components"
Bob: [Uses generate-component-diagram with previous analysis]
Bob: "Here's the component diagram: [mermaid code]"
```

### 3. post-analysis-comment

**Purpose**: Post comprehensive analysis to GitHub

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

**When to use:**
- After analysis and diagram generation
- User asks to "post to GitHub"
- Want to share findings

**Example Bob usage:**
```
User: "Post this analysis to the issue"
Bob: [Uses post-analysis-comment]
Bob: "✅ Posted! URL: ..."
```

### 4. full-pipeline

**Purpose**: Run complete workflow automatically

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

**When to use:**
- User explicitly asks for "full analysis"
- Batch processing multiple issues
- Quick one-shot analysis

**Example Bob usage:**
```
User: "Do a complete analysis of issue #12345"
Bob: [Uses full-pipeline]
Bob: "✅ Complete! Found 3 packages, posted analysis."
```

## Example Conversations

### Example 1: Detailed Analysis

```
User: "I need help understanding issue #12345 in OpenLiberty/open-liberty"

Bob: "I'll analyze that issue for you."
     [Uses analyze-github-issue]
     
Bob: "I found 3 Liberty packages mentioned:
      
      1. io.openliberty.security.ltpa (95% confidence)
         - Found in stack trace
         - Related to LTPA token validation
      
      2. com.ibm.ws.crypto.ltpakeyutil (90% confidence)
         - Found in error message
         - Handles LTPA key encryption
      
      3. io.openliberty.security.utility (85% confidence)
         - Mentioned in description
         - CLI tool for key generation
      
      This appears to be a security/LTPA issue. Would you like me to create
      a diagram showing how these components relate?"

User: "Yes please"

Bob: [Uses generate-component-diagram]
     "Here's the component diagram:
     
     [Mermaid diagram showing Issue -> 3 packages with relationships]
     
     The diagram shows that the LTPA utility depends on the crypto package,
     which is used by the main LTPA implementation. Should I post this
     analysis to the GitHub issue?"

User: "Let me see a preview first"

Bob: [Uses post-analysis-comment with dry_run=true]
     "Here's what would be posted:
     
     [Shows formatted comment with:
      - Package list
      - Diagram
      - Integration points
      - Code suggestions
      - Test recommendations]
     
     This includes detailed technical information about LTPA tokens,
     encryption, and suggested fixes. Ready to post?"

User: "Looks great, post it!"

Bob: [Uses post-analysis-comment with dry_run=false]
     "✅ Posted successfully!
     
     View at: https://github.com/OpenLiberty/open-liberty/issues/12345#comment-789
     
     The team can now see the detailed analysis with diagrams and
     recommendations."
```

### Example 2: Quick Analysis

```
User: "Quick analysis of https://github.com/OpenLiberty/open-liberty/issues/12345"

Bob: [Uses full-pipeline with dry_run=true]
     "✅ Analysis complete!
     
     Found 3 packages:
     - io.openliberty.security.ltpa (95%)
     - com.ibm.ws.crypto.ltpakeyutil (90%)
     - io.openliberty.security.utility (85%)
     
     [Shows diagram]
     
     This is a preview (dry-run mode). Post to GitHub?"

User: "Yes"

Bob: [Uses full-pipeline with dry_run=false]
     "✅ Posted! https://github.com/OpenLiberty/open-liberty/issues/12345#comment-789"
```

### Example 3: Just Identification

```
User: "What Liberty packages are affected by issue #12345?"

Bob: [Uses analyze-github-issue]
     "I found 3 Liberty packages:
     
     1. io.openliberty.security.ltpa (95% confidence)
     2. com.ibm.ws.crypto.ltpakeyutil (90% confidence)
     3. io.openliberty.security.utility (85% confidence)
     
     All are related to LTPA security and token management."

User: "Thanks, that's all I needed"

Bob: "You're welcome! Let me know if you need more details or want me
      to generate a diagram."
```

## Best Practices for Bob

1. **Start with analysis** - Always use `analyze-github-issue` first
2. **Explain findings** - Don't just show data, interpret it
3. **Offer next steps** - Suggest diagram or posting
4. **Use dry-run** - Preview before posting to GitHub
5. **Be conversational** - Explain what you're doing and why

## Common User Requests

| User Says | Bob Should Use | Notes |
|-----------|---------------|-------|
| "Analyze issue #123" | `analyze-github-issue` | Start here |
| "Show me a diagram" | `generate-component-diagram` | After analysis |
| "Post to GitHub" | `post-analysis-comment` | Use dry-run first |
| "Full analysis" | `full-pipeline` | Quick option |
| "What packages?" | `analyze-github-issue` | Just identification |
| "Preview comment" | `post-analysis-comment` with `dry_run=true` | Safe preview |

## Summary

**For Bob:**
- ✅ Use step-by-step approach (individual tools)
- ✅ Explain what you're doing at each step
- ✅ Offer choices to the user
- ✅ Use dry-run before posting

**For Users:**
- ✅ You can ask for step-by-step or full analysis
- ✅ Bob will guide you through the process
- ✅ You can preview before posting to GitHub
- ✅ Flexible workflow based on your needs

The MCP integration gives Bob powerful tools while keeping the user in control! 🚀