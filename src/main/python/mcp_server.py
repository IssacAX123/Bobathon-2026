#!/usr/bin/env python3
"""
MCP Server for GitHub Issue Analyzer
Provides granular tools for Bob to orchestrate the analysis workflow step-by-step.
Each tool does ONE thing, giving Bob full control and visibility.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Optional, Dict, List

from mcp.server import Server
from mcp.types import Tool, TextContent

# Import production modules
from github_issue_analyzer import GitHubIssueAnalyzer, AnalysisResult
from diagram_generator import DiagramGenerator, DiagramResult
from comment_poster import GitHubCommentPoster, CommentResult


# Initialize MCP server
app = Server("github-issue-analyzer")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Register granular tools for Bob's step-by-step workflow."""
    return [
        Tool(
            name="fetch-github-issue",
            description="Fetch a GitHub issue's details (title, body, labels, author). First step in analysis.",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_url": {
                        "type": "string",
                        "description": "GitHub issue URL (e.g., https://github.com/owner/repo/issues/123)"
                    }
                },
                "required": ["issue_url"]
            }
        ),
        Tool(
            name="identify-liberty-packages",
            description="Analyze issue text to identify Liberty packages with confidence scores. Use after fetching issue.",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_text": {
                        "type": "string",
                        "description": "Combined issue title and body text to analyze"
                    }
                },
                "required": ["issue_text"]
            }
        ),
        Tool(
            name="generate-component-diagram",
            description="Generate a Mermaid diagram showing package relationships. Use after identifying packages.",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_number": {
                        "type": "integer",
                        "description": "GitHub issue number"
                    },
                    "issue_title": {
                        "type": "string",
                        "description": "GitHub issue title"
                    },
                    "packages": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "confidence": {"type": "number"}
                            }
                        },
                        "description": "List of identified packages"
                    }
                },
                "required": ["issue_number", "issue_title", "packages"]
            }
        ),
        Tool(
            name="format-analysis-comment",
            description="Format a comprehensive analysis comment with packages, diagram, and recommendations. Use before posting.",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_number": {
                        "type": "integer",
                        "description": "GitHub issue number"
                    },
                    "issue_title": {
                        "type": "string",
                        "description": "GitHub issue title"
                    },
                    "packages": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "List of identified packages"
                    },
                    "diagram": {
                        "type": "string",
                        "description": "Mermaid diagram code"
                    }
                },
                "required": ["issue_number", "issue_title", "packages", "diagram"]
            }
        ),
        Tool(
            name="post-github-comment",
            description="Post a comment to a GitHub issue. Use dry_run=true first to preview!",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_url": {
                        "type": "string",
                        "description": "GitHub issue URL"
                    },
                    "comment_text": {
                        "type": "string",
                        "description": "The formatted comment text to post"
                    },
                    "dry_run": {
                        "type": "boolean",
                        "description": "If true, preview only without posting (default: true for safety)",
                        "default": True
                    }
                },
                "required": ["issue_url", "comment_text"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute the requested tool."""
    
    if name == "fetch-github-issue":
        return await fetch_github_issue(arguments)
    elif name == "identify-liberty-packages":
        return await identify_packages(arguments)
    elif name == "generate-component-diagram":
        return await generate_diagram(arguments)
    elif name == "format-analysis-comment":
        return await format_comment(arguments)
    elif name == "post-github-comment":
        return await post_comment(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


async def fetch_github_issue(arguments: dict) -> list[TextContent]:
    """Fetch GitHub issue details."""
    issue_url = arguments["issue_url"]
    
    def _fetch():
        analyzer = GitHubIssueAnalyzer()
        result = analyzer.analyze_issue(issue_url)
        
        if not result.success:
            return {"success": False, "error": result.error_message}
        
        return {
            "success": True,
            "issue": {
                "number": result.issue.number,
                "title": result.issue.title,
                "body": result.issue.body,
                "labels": result.issue.labels,
                "author": result.issue.author,
                "url": result.issue.url
            }
        }
    
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, _fetch)
        
        if not result["success"]:
            return [TextContent(type="text", text=f"❌ Error: {result['error']}")]
        
        issue = result["issue"]
        response = f"""✅ **Issue Fetched**

**#{issue['number']}: {issue['title']}**

**Author**: {issue['author']}
**Labels**: {', '.join(issue['labels']) if issue['labels'] else 'None'}

**Body** (first 500 chars):
{issue['body'][:500]}{'...' if len(issue['body']) > 500 else ''}

**Full text for analysis**:
```json
{json.dumps({"title": issue['title'], "body": issue['body']}, indent=2)}
```
"""
        
        return [TextContent(type="text", text=response)]
    
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


async def identify_packages(arguments: dict) -> list[TextContent]:
    """Identify Liberty packages in issue text."""
    issue_text = arguments["issue_text"]
    
    def _identify():
        analyzer = GitHubIssueAnalyzer()
        # Create a minimal issue object for analysis
        from github_issue_analyzer import Issue
        issue = Issue(
            number=0,
            title="",
            body=issue_text,
            labels=[],
            url="",
            created_at="",
            author=""
        )
        packages = analyzer._analyze_packages(issue)
        return packages
    
    try:
        loop = asyncio.get_event_loop()
        packages = await loop.run_in_executor(None, _identify)
        
        if not packages:
            return [TextContent(type="text", text="ℹ️ No Liberty packages identified in the text.")]
        
        response = f"""✅ **Identified {len(packages)} Liberty Package(s)**

"""
        for i, pkg in enumerate(packages, 1):
            response += f"""{i}. **{pkg.name}**
   - Confidence: {pkg.confidence:.0%}
   - Type: {pkg.package_type}
   - Location: {pkg.location}
   - Context: {pkg.context[:100]}...

"""
        
        response += f"""
**Packages JSON** (for next steps):
```json
{json.dumps([{"name": p.name, "confidence": p.confidence, "package_type": p.package_type} for p in packages], indent=2)}
```
"""
        
        return [TextContent(type="text", text=response)]
    
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


async def generate_diagram(arguments: dict) -> list[TextContent]:
    """Generate Mermaid diagram."""
    issue_number = arguments["issue_number"]
    issue_title = arguments["issue_title"]
    packages_data = arguments["packages"]
    
    def _generate():
        # Convert to format expected by diagram generator
        analysis_dict = {
            "issue": {
                "number": issue_number,
                "title": issue_title
            },
            "packages": packages_data
        }
        
        generator = DiagramGenerator()
        result = generator.generate_diagram(analysis_dict)
        return result
    
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, _generate)
        
        if not result.success:
            return [TextContent(type="text", text=f"❌ Error: {result.error_message}")]
        
        response = f"""✅ **Diagram Generated**

{result.mermaid}

{f"**Note**: Showing top {DiagramGenerator.MAX_PACKAGES} packages." if result.additional_packages else ""}
"""
        
        return [TextContent(type="text", text=response)]
    
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


async def format_comment(arguments: dict) -> list[TextContent]:
    """Format analysis comment."""
    issue_number = arguments["issue_number"]
    issue_title = arguments["issue_title"]
    packages = arguments["packages"]
    diagram = arguments["diagram"]
    
    def _format():
        # Create analysis dict for comment poster
        analysis_dict = {
            "issue": {
                "number": issue_number,
                "title": issue_title
            },
            "packages": packages,
            "success": True
        }
        
        poster = GitHubCommentPoster(dry_run=True)
        comment_body = poster._format_comprehensive_comment(
            analysis_dict,
            diagram,
            str(issue_number)
        )
        return comment_body
    
    try:
        loop = asyncio.get_event_loop()
        comment_body = await loop.run_in_executor(None, _format)
        
        response = f"""✅ **Comment Formatted**

**Preview** (first 1000 chars):
{comment_body[:1000]}...

**Full comment** (for posting):
```
{comment_body}
```
"""
        
        return [TextContent(type="text", text=response)]
    
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


async def post_comment(arguments: dict) -> list[TextContent]:
    """Post comment to GitHub."""
    issue_url = arguments["issue_url"]
    comment_text = arguments["comment_text"]
    dry_run = arguments.get("dry_run", True)  # Default to dry-run for safety
    
    def _post():
        poster = GitHubCommentPoster(dry_run=dry_run)
        
        # Parse URL to get API endpoint
        from urllib.parse import urlparse
        parsed = urlparse(issue_url)
        path_parts = parsed.path.strip('/').split('/')
        owner, repo, _, issue_number = path_parts
        
        if dry_run:
            return {
                "success": True,
                "dry_run": True,
                "message": "Dry run - comment not posted"
            }
        
        # Actually post
        api_url = f'https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}'
        result = poster._create_comment(api_url, comment_text)
        
        return {
            "success": result.success,
            "dry_run": False,
            "comment_url": result.comment_url,
            "error": result.error_message
        }
    
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, _post)
        
        if result["dry_run"]:
            return [TextContent(type="text", text="✅ **Dry Run** - Comment preview generated (not posted to GitHub)")]
        
        if result["success"]:
            return [TextContent(type="text", text=f"✅ **Posted Successfully!**\n\nView at: {result['comment_url']}")]
        else:
            return [TextContent(type="text", text=f"❌ **Failed to post**: {result['error']}")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server
    
    print("Starting GitHub Issue Analyzer MCP Server...", file=sys.stderr)
    print("Tools available (step-by-step workflow):", file=sys.stderr)
    print("  1. fetch-github-issue", file=sys.stderr)
    print("  2. identify-liberty-packages", file=sys.stderr)
    print("  3. generate-component-diagram", file=sys.stderr)
    print("  4. format-analysis-comment", file=sys.stderr)
    print("  5. post-github-comment", file=sys.stderr)
    print("Ready!", file=sys.stderr)
    
    async def run_server():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    
    asyncio.run(run_server())


if __name__ == "__main__":
    main()

# Made with Bob
