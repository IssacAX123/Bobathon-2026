#!/usr/bin/env python3
"""
MCP Server for GitHub Issue Analyzer
Wraps the production pipeline (analyzer, diagram generator, comment poster)
as MCP tools that Bob can use, while keeping Flask UI functional.
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
    """Register tools for Bob to use."""
    return [
        Tool(
            name="analyze-github-issue",
            description="Analyze a GitHub issue to identify Liberty packages with confidence scores",
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
            name="generate-component-diagram",
            description="Generate a Mermaid component diagram from analysis results",
            inputSchema={
                "type": "object",
                "properties": {
                    "analysis_json": {
                        "type": "string",
                        "description": "JSON string from analyze-github-issue tool"
                    }
                },
                "required": ["analysis_json"]
            }
        ),
        Tool(
            name="post-analysis-comment",
            description="Post comprehensive analysis as a GitHub comment with diagrams and recommendations",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_url": {
                        "type": "string",
                        "description": "GitHub issue URL"
                    },
                    "analysis_json": {
                        "type": "string",
                        "description": "JSON string from analyze-github-issue tool"
                    },
                    "diagram": {
                        "type": "string",
                        "description": "Mermaid diagram from generate-component-diagram tool"
                    },
                    "dry_run": {
                        "type": "boolean",
                        "description": "If true, preview comment without posting (default: false)",
                        "default": False
                    }
                },
                "required": ["issue_url", "analysis_json", "diagram"]
            }
        ),
        Tool(
            name="full-pipeline",
            description="Run complete analysis pipeline: analyze issue, generate diagram, and post comment",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_url": {
                        "type": "string",
                        "description": "GitHub issue URL"
                    },
                    "post_comment": {
                        "type": "boolean",
                        "description": "Whether to post comment to GitHub (default: true)",
                        "default": True
                    },
                    "dry_run": {
                        "type": "boolean",
                        "description": "If true, preview comment without posting (default: false)",
                        "default": False
                    }
                },
                "required": ["issue_url"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute the requested tool."""
    
    if name == "analyze-github-issue":
        return await analyze_issue(arguments)
    elif name == "generate-component-diagram":
        return await generate_diagram(arguments)
    elif name == "post-analysis-comment":
        return await post_comment(arguments)
    elif name == "full-pipeline":
        return await run_full_pipeline(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


async def analyze_issue(arguments: dict) -> list[TextContent]:
    """Analyze a GitHub issue to identify packages."""
    issue_url = arguments["issue_url"]
    
    def _analyze():
        analyzer = GitHubIssueAnalyzer()
        result = analyzer.analyze_issue(issue_url)
        return analyzer.to_json(result)
    
    try:
        loop = asyncio.get_event_loop()
        json_result = await loop.run_in_executor(None, _analyze)
        
        # Parse to provide human-readable summary
        result_dict = json.loads(json_result)
        
        if not result_dict['success']:
            return [TextContent(
                type="text",
                text=f"❌ Analysis failed: {result_dict['error_message']}"
            )]
        
        packages = result_dict.get('packages', [])
        issue = result_dict.get('issue', {})
        
        summary = f"""✅ **Analysis Complete**

**Issue**: #{issue.get('number')} - {issue.get('title')}
**Packages Found**: {len(packages)}
**Analysis Time**: {result_dict['analysis_time_ms']}ms

**Top Packages**:
{chr(10).join(f"- `{pkg['name']}` (confidence: {pkg['confidence']:.0%})" for pkg in packages[:5])}

**Full JSON** (use this for generate-component-diagram):
```json
{json_result}
```
"""
        
        return [TextContent(type="text", text=summary)]
    
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


async def generate_diagram(arguments: dict) -> list[TextContent]:
    """Generate Mermaid diagram from analysis results."""
    analysis_json = arguments["analysis_json"]
    
    def _generate():
        analysis_dict = json.loads(analysis_json)
        generator = DiagramGenerator()
        result = generator.generate_diagram(analysis_dict)
        return result
    
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, _generate)
        
        if not result.success:
            return [TextContent(
                type="text",
                text=f"❌ Diagram generation failed: {result.error_message}"
            )]
        
        response = f"""✅ **Diagram Generated**

{result.mermaid}

{f"**Note**: Showing top {DiagramGenerator.MAX_PACKAGES} packages." if result.additional_packages else ""}
{chr(10).join(f"- `{pkg.name}` (confidence: {pkg.confidence:.0%})" for pkg in result.additional_packages) if result.additional_packages else ""}
"""
        
        return [TextContent(type="text", text=response)]
    
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


async def post_comment(arguments: dict) -> list[TextContent]:
    """Post analysis comment to GitHub issue."""
    issue_url = arguments["issue_url"]
    analysis_json = arguments["analysis_json"]
    diagram = arguments["diagram"]
    dry_run = arguments.get("dry_run", False)
    
    def _post():
        analysis_dict = json.loads(analysis_json)
        poster = GitHubCommentPoster(dry_run=dry_run)
        result = poster.post_analysis(issue_url, analysis_dict, diagram)
        return result
    
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, _post)
        
        if result.success:
            if dry_run:
                return [TextContent(
                    type="text",
                    text="✅ **Dry Run Complete** - Comment preview generated (not posted)"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"✅ **Comment Posted Successfully**\n\nURL: {result.comment_url}"
                )]
        else:
            return [TextContent(
                type="text",
                text=f"❌ Failed to post comment: {result.error_message}"
            )]
    
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


async def run_full_pipeline(arguments: dict) -> list[TextContent]:
    """Run complete analysis pipeline."""
    issue_url = arguments["issue_url"]
    post_comment_flag = arguments.get("post_comment", True)
    dry_run = arguments.get("dry_run", False)
    
    def _pipeline():
        # Step 1: Analyze issue
        analyzer = GitHubIssueAnalyzer()
        analysis_result = analyzer.analyze_issue(issue_url)
        
        if not analysis_result.success:
            return {
                'success': False,
                'error': analysis_result.error_message
            }
        
        analysis_dict = json.loads(analyzer.to_json(analysis_result))
        
        # Step 2: Generate diagram
        generator = DiagramGenerator()
        diagram_result = generator.generate_diagram(analysis_dict)
        
        if not diagram_result.success:
            return {
                'success': False,
                'error': diagram_result.error_message
            }
        
        # Step 3: Post comment (if requested)
        comment_result = None
        if post_comment_flag:
            poster = GitHubCommentPoster(dry_run=dry_run)
            comment_result = poster.post_analysis(
                issue_url,
                analysis_dict,
                diagram_result.mermaid
            )
        
        return {
            'success': True,
            'analysis': analysis_dict,
            'diagram': diagram_result.mermaid,
            'comment': comment_result
        }
    
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, _pipeline)
        
        if not result['success']:
            return [TextContent(
                type="text",
                text=f"❌ Pipeline failed: {result['error']}"
            )]
        
        analysis = result['analysis']
        packages = analysis.get('packages', [])
        issue = analysis.get('issue', {})
        
        response = f"""✅ **Full Pipeline Complete**

**Issue**: #{issue.get('number')} - {issue.get('title')}
**Packages Found**: {len(packages)}
**Analysis Time**: {analysis['analysis_time_ms']}ms

**Top Packages**:
{chr(10).join(f"- `{pkg['name']}` (confidence: {pkg['confidence']:.0%})" for pkg in packages[:5])}

**Diagram**:
{result['diagram']}
"""
        
        if post_comment_flag and result['comment']:
            if result['comment'].success:
                if dry_run:
                    response += "\n\n✅ **Comment Preview Generated** (dry run mode)"
                else:
                    response += f"\n\n✅ **Comment Posted**: {result['comment'].comment_url}"
            else:
                response += f"\n\n⚠️ **Comment Failed**: {result['comment'].error_message}"
        
        return [TextContent(type="text", text=response)]
    
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server
    
    print("Starting GitHub Issue Analyzer MCP Server...", file=sys.stderr)
    print("Tools available:", file=sys.stderr)
    print("  - analyze-github-issue", file=sys.stderr)
    print("  - generate-component-diagram", file=sys.stderr)
    print("  - post-analysis-comment", file=sys.stderr)
    print("  - full-pipeline", file=sys.stderr)
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
