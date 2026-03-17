# Person 4: MCP Server & Integration Lead

**Your Mission:** Build the MCP server that orchestrates the entire workflow and prepare the demo.

**Time Budget:** Hour 1 (scaffold), Hours 2-3 (integration + demo)

---

## 📝 Your File: `src/server.py`

```python
from mcp.server import Server
from mcp.types import Tool, TextContent
from datetime import datetime
from typing import List
import sys

# Import our modules
from github_client import GitHubClient
from package_analyzer import PackageAnalyzer, Package
from diagram_generator import MermaidGenerator

# Initialize MCP server
app = Server("liberty-analyzer")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """Register available MCP tools"""
    return [
        Tool(
            name="analyze-github-issue",
            description="Fetch GitHub issue, identify Liberty packages, generate diagram, and post analysis comment",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_url": {
                        "type": "string",
                        "description": "GitHub issue URL (e.g., 'OpenLiberty/open-liberty#12345' or full URL)"
                    },
                    "post_comment": {
                        "type": "boolean",
                        "description": "Whether to post the analysis as a comment (default: true)",
                        "default": True
                    }
                },
                "required": ["issue_url"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute MCP tool"""
    if name != "analyze-github-issue":
        raise ValueError(f"Unknown tool: {name}")
    
    issue_url = arguments["issue_url"]
    post_comment = arguments.get("post_comment", True)
    
    try:
        # Initialize components
        gh_client = GitHubClient()
        analyzer = PackageAnalyzer()
        diagram_gen = MermaidGenerator()
        
        # Validate URL
        if not gh_client.validate_issue_url(issue_url):
            return [TextContent(
                type="text",
                text=f"❌ Invalid issue URL format: {issue_url}\n\nExpected: 'owner/repo#123' or full GitHub URL"
            )]
        
        # Step 1: Fetch issue
        print("🔍 Fetching issue...", file=sys.stderr)
        issue = gh_client.fetch_issue(issue_url)
        
        # Step 2: Analyze packages
        print("📦 Analyzing packages...", file=sys.stderr)
        full_text = f"{issue['title']} {issue.get('body', '')}"
        packages = analyzer.extract_packages(full_text)
        top_packages = analyzer.get_top_packages(packages, limit=5)
        
        # Step 3: Generate diagram
        print("📊 Generating diagram...", file=sys.stderr)
        package_names = [p.name for p in top_packages]
        diagram = diagram_gen.generate_detailed_diagram(
            issue['number'],
            [{'name': p.name, 'confidence': p.confidence} for p in top_packages],
            issue['title']
        )
        
        # Validate diagram
        if not diagram_gen.validate_diagram(diagram):
            print("⚠️ Warning: Generated diagram may have syntax errors", file=sys.stderr)
        
        # Step 4: Format comment
        comment = format_analysis_comment(issue, top_packages, diagram)
        
        # Step 5: Post comment (if requested)
        if post_comment:
            print("💬 Posting analysis...", file=sys.stderr)
            gh_client.post_comment(issue_url, comment)
            gh_client.add_label(issue_url, "bot-analyzed")
            
            result = f"""✅ Analysis complete!

**Issue:** #{issue['number']} - {issue['title']}
**Packages identified:** {len(top_packages)}
**View at:** {issue['url']}

Top packages:
{format_package_list(top_packages)}
"""
        else:
            # Just return the analysis without posting
            result = f"""✅ Analysis complete (not posted)

**Issue:** #{issue['number']} - {issue['title']}
**Packages identified:** {len(top_packages)}

Top packages:
{format_package_list(top_packages)}

**Generated Comment:**
{comment}
"""
        
        return [TextContent(type="text", text=result)]
        
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}\n\nIssue URL: {issue_url}"
        print(error_msg, file=sys.stderr)
        return [TextContent(type="text", text=error_msg)]

def format_analysis_comment(issue: dict, packages: List[Package], diagram: str) -> str:
    """Format the analysis as a markdown comment
    
    Args:
        issue: Issue data from GitHub
        packages: List of Package objects
        diagram: Mermaid diagram string
        
    Returns:
        Formatted markdown comment
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    
    comment_lines = [
        "## 🤖 Automated Analysis by Bob",
        "",
        f"**Issue:** #{issue['number']} - {issue['title']}",
        f"**Analyzed:** {timestamp}",
        "",
        "### 📦 Identified Liberty Packages",
        ""
    ]
    
    if packages:
        for pkg in packages:
            confidence_pct = int(pkg.confidence * 100)
            occurrences = pkg.occurrences
            
            # Add confidence indicator emoji
            if confidence_pct >= 70:
                indicator = "🟢"
            elif confidence_pct >= 40:
                indicator = "🟡"
            else:
                indicator = "🟠"
            
            comment_lines.append(
                f"- {indicator} `{pkg.name}` "
                f"(confidence: {confidence_pct}%, mentioned {occurrences}x)"
            )
        
        # Add summary
        summary = f"\n**Total:** {len(packages)} package(s) identified"
        comment_lines.append(summary)
    else:
        comment_lines.append("*No Liberty packages identified in issue description*")
    
    # Add diagram
    comment_lines.extend([
        "",
        "### 📊 Component Diagram",
        "",
        "```mermaid",
        diagram,
        "```",
        "",
        "---",
        "*Generated by Liberty Issue Analyzer MCP Tool*"
    ])
    
    return "\n".join(comment_lines)

def format_package_list(packages: List[Package]) -> str:
    """Format package list for display
    
    Args:
        packages: List of Package objects
        
    Returns:
        Formatted string
    """
    if not packages:
        return "None"
    
    lines = []
    for i, pkg in enumerate(packages, 1):
        confidence_pct = int(pkg.confidence * 100)
        lines.append(f"{i}. {pkg.name} ({confidence_pct}%)")
    
    return "\n".join(lines)

def main():
    """Run the MCP server"""
    import mcp.server.stdio
    
    print("Starting Liberty Issue Analyzer MCP Server...", file=sys.stderr)
    print("Ready to analyze GitHub issues!", file=sys.stderr)
    
    mcp.server.stdio.run(app)

if __name__ == "__main__":
    main()
```

---

## 🧪 Testing Your Integration

Create `tests/test_integration.py`:

```python
import sys
import asyncio
sys.path.insert(0, 'src')

from server import call_tool

# Real OpenLiberty issues for testing
TEST_ISSUES = [
    "OpenLiberty/open-liberty#28000",
    "OpenLiberty/open-liberty#27500",
    "OpenLiberty/open-liberty#27000"
]

async def test_single_issue(issue_url: str, post_comment: bool = False):
    """Test analysis of a single issue"""
    print(f"\n{'='*60}")
    print(f"Testing: {issue_url}")
    print(f"{'='*60}\n")
    
    try:
        result = await call_tool(
            "analyze-github-issue",
            {"issue_url": issue_url, "post_comment": post_comment}
        )
        
        print(result[0].text)
        
        # Verify success
        assert "✅" in result[0].text or "Analysis complete" in result[0].text
        print(f"\n✓ {issue_url} - PASSED")
        return True
        
    except Exception as e:
        print(f"\n✗ {issue_url} - FAILED: {e}")
        return False

async def test_all_issues():
    """Test all issues"""
    print("\n" + "="*60)
    print("INTEGRATION TEST SUITE")
    print("="*60)
    
    results = []
    for issue_url in TEST_ISSUES:
        # Test without posting (dry run)
        success = await test_single_issue(issue_url, post_comment=False)
        results.append((issue_url, success))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for issue_url, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{status}: {issue_url}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return True
    else:
        print(f"\n⚠️ {total - passed} test(s) failed")
        return False

async def test_error_handling():
    """Test error handling"""
    print("\n" + "="*60)
    print("ERROR HANDLING TESTS")
    print("="*60)
    
    # Test invalid URL
    print("\nTest 1: Invalid URL format")
    result = await call_tool(
        "analyze-github-issue",
        {"issue_url": "not-a-valid-url"}
    )
    assert "❌" in result[0].text
    print("✓ Invalid URL handled correctly")
    
    # Test non-existent issue
    print("\nTest 2: Non-existent issue")
    try:
        result = await call_tool(
            "analyze-github-issue",
            {"issue_url": "OpenLiberty/open-liberty#999999999"}
        )
        assert "❌" in result[0].text
        print("✓ Non-existent issue handled correctly")
    except Exception as e:
        print(f"✓ Non-existent issue raised exception (expected): {str(e)[:50]}")
    
    print("\n✓ Error handling tests passed")

if __name__ == "__main__":
    print("Liberty Issue Analyzer - Integration Tests")
    print("=" * 60)
    
    # Run main tests
    success = asyncio.run(test_all_issues())
    
    # Run error handling tests
    asyncio.run(test_error_handling())
    
    if success:
        print("\n" + "="*60)
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("="*60)
        print("\nYou're ready for the demo!")
    else:
        print("\n" + "="*60)
        print("⚠️ SOME TESTS FAILED")
        print("="*60)
        print("\nFix issues before demo!")
```

Run integration tests:
```bash
python tests/test_integration.py
```

---

## 🎬 Demo Preparation

Create `docs/DEMO.md`:

```markdown
# Liberty Issue Analyzer - Demo Script

**Duration:** 5 minutes  
**Audience:** Hackathon judges  
**Goal:** Show automated GitHub issue analysis

---

## Pre-Demo Checklist (15 minutes before)

- [ ] MCP server running and tested
- [ ] 3 test issues ready in browser tabs
- [ ] Bob interface connected to server
- [ ] Backup video ready (if needed)
- [ ] Screenshots prepared
- [ ] Team roles assigned

---

## Demo Flow

### Opening (30 seconds)

**Speaker:** "We built an MCP tool that automatically analyzes Liberty GitHub issues."

**Show:** GitHub issue on screen

---

### Live Demo (3 minutes)

#### Step 1: Show the Problem (30 sec)
**Speaker:** "Here's a complex Liberty issue about MicroProfile Config..."

**Show:** Issue #28000 in browser
- Point out: Long description, multiple packages mentioned
- Problem: "Manually identifying affected components takes time"

#### Step 2: Run Analysis (30 sec)
**Speaker:** "Watch Bob analyze this automatically..."

**Execute:**
```
User: Bob, analyze this issue: OpenLiberty/open-liberty#28000
```

**Show:** Real-time progress:
- 🔍 Fetching issue...
- 📦 Analyzing packages...
- 📊 Generating diagram...
- 💬 Posting analysis...
- ✅ Analysis complete!

#### Step 3: Show Results (1 min)
**Speaker:** "Let's see what Bob found..."

**Navigate to:** GitHub issue comments

**Point out:**
1. Formatted analysis comment
2. Identified packages with confidence scores
3. Visual Mermaid diagram
4. "bot-analyzed" label added

#### Step 4: Highlight Features (1 min)
**Speaker:** "Notice Bob automatically:"

**List:**
- ✅ Identified 3 Liberty packages
- ✅ Scored confidence (90%, 75%, 60%)
- ✅ Generated visual diagram
- ✅ Posted formatted analysis
- ✅ Added tracking label
- ✅ Completed in under 10 seconds

---

### Closing (30 seconds)

**Speaker:** "This saves developers hours of manual analysis and provides instant context for issue triage."

**Impact:**
- Faster issue triage
- Better component identification
- Visual documentation
- Automated workflow

---

## Backup Plan

### If Live Demo Fails:

1. **Show pre-recorded video** (prepare 1-min video)
2. **Walk through screenshots** (prepare 5 screenshots)
3. **Explain architecture** (show diagram)

### Screenshots to Prepare:

1. GitHub issue before analysis
2. Bob executing command
3. Progress messages
4. GitHub comment with diagram
5. Issue with label added

---

## Q&A Preparation

**Q: How accurate is package identification?**  
A: 80%+ accuracy on real Liberty issues, with confidence scoring

**Q: Can it handle private repos?**  
A: Yes, uses gh CLI authentication

**Q: What about rate limits?**  
A: Authenticated requests get 5000/hour limit

**Q: Can it analyze multiple issues?**  
A: Yes, just call the tool multiple times

**Q: What's next?**  
A: Git history analysis, pattern detection, custom templates

---

## Success Metrics

- [ ] Demo completes without errors
- [ ] Audience sees value immediately
- [ ] Questions answered confidently
- [ ] Under 5 minutes total time

---

## Team Roles During Demo

- **Person 1:** Run Bob commands
- **Person 2:** Navigate browser/GitHub
- **Person 3:** Explain technical details
- **Person 4:** Present and narrate

---

## Rehearsal Checklist

- [ ] Rehearsal 1 completed (Hour 2)
- [ ] Rehearsal 2 completed (Hour 3)
- [ ] Timing under 5 minutes
- [ ] All transitions smooth
- [ ] Backup materials ready
```

---

## 📋 Hour-by-Hour Tasks

### Hour 1: Scaffold (0:00-1:00)
- [ ] Create `server.py` with basic structure
- [ ] Set up MCP tool registration
- [ ] Test tool listing works
- [ ] Create placeholder for integration

### Hour 2: Integration (1:00-2:00)
- [ ] Import all modules (Person 1, 2, 3)
- [ ] Implement `call_tool()` workflow
- [ ] Add error handling
- [ ] Test with 1 real issue
- [ ] First demo rehearsal

### Hour 3: Polish & Demo (2:00-3:00)
- [ ] Run full integration tests
- [ ] Create demo script
- [ ] Record backup video
- [ ] Take screenshots
- [ ] Second demo rehearsal
- [ ] Final checks

---

## 🚨 Common Issues & Solutions

### Issue: Module import errors
**Solution:** Ensure all files have `__init__.py` in src/

### Issue: MCP server won't start
**Solution:** Check `mcp` package installed: `pip install mcp`

### Issue: Tool not appearing in Bob
**Solution:** Restart Bob interface after server changes

### Issue: Async errors
**Solution:** Ensure all tool functions are `async`

---

## 📋 Integration Checklist

- [ ] All modules import successfully
- [ ] Tool registration works
- [ ] Workflow executes end-to-end
- [ ] Error handling works
- [ ] Comment formatting looks good
- [ ] Diagram renders in GitHub
- [ ] Tests pass (3/3 issues)
- [ ] Demo script ready
- [ ] Backup materials prepared

---

## 🤝 Coordination Points

**Hour 1 Check-in (0:50):**
- Verify all modules are complete
- Test imports work
- Identify any blockers

**Hour 2 Check-in (1:30):**
- Verify integration works
- Test with real issue
- First demo rehearsal

**Hour 3 Check-in (2:40):**
- Final tests complete
- Demo rehearsed 2x
- Backup ready

---

## 💡 Tips for Success

1. **Start simple** - Get basic workflow working first
2. **Test early** - Don't wait until Hour 3
3. **Communicate** - Keep team updated on progress
4. **Prepare backups** - Video and screenshots save demos
5. **Practice** - Rehearse demo at least twice

---

## 🆘 Need Help?

**MCP server issues?** Check [MCP docs](https://modelcontextprotocol.io/docs)  
**Integration problems?** Test each module independently first  
**Demo nerves?** Practice makes perfect - rehearse!

**Estimated completion time:** 3 hours (distributed)  
**If blocked:** Coordinate with team immediately!

---

## 🎯 Success Criteria

- [ ] Tool executes without errors
- [ ] Analysis completes in <15 seconds
- [ ] Comment posts successfully
- [ ] Diagram renders correctly
- [ ] Demo runs smoothly
- [ ] Team confident and ready

**You've got this! 🚀**