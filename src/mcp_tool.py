#!/usr/bin/env python3
"""
MCP Tool Wrapper for GitHub Issue Analyzer
Provides individual tools that Bob can use to analyze GitHub issues step by step.
"""

import asyncio
import sys
import os
import subprocess
import json
from mcp.server import Server
from mcp.types import Tool, TextContent


# Initialize MCP server
app = Server("github-issue-analyzer")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Register tools for Bob to use."""
    return [
        Tool(
            name="fetch-github-issue",
            description="Fetch a GitHub issue's details including title, body, and labels",
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
            name="search-codebase-files",
            description="Search for files in the codebase that match given keywords",
            inputSchema={
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Keywords to search for in filenames and paths"
                    },
                    "max_files": {
                        "type": "integer",
                        "description": "Maximum number of files to return (default: 10)",
                        "default": 10
                    }
                },
                "required": ["keywords"]
            }
        ),
        Tool(
            name="create-mermaid-diagram",
            description="Create a Mermaid diagram showing relationships between an issue and files",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_title": {
                        "type": "string",
                        "description": "The GitHub issue title"
                    },
                    "issue_number": {
                        "type": "integer",
                        "description": "The GitHub issue number"
                    },
                    "files": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of file paths related to the issue"
                    }
                },
                "required": ["issue_title", "issue_number", "files"]
            }
        ),
        Tool(
            name="post-github-comment",
            description="Post a comment to a GitHub issue",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_url": {
                        "type": "string",
                        "description": "GitHub issue URL"
                    },
                    "comment": {
                        "type": "string",
                        "description": "The comment text to post (supports Markdown)"
                    }
                },
                "required": ["issue_url", "comment"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute the requested tool."""
    
    if name == "fetch-github-issue":
        return await fetch_github_issue(arguments)
    elif name == "search-codebase-files":
        return await search_codebase_files(arguments)
    elif name == "create-mermaid-diagram":
        return await create_mermaid_diagram(arguments)
    elif name == "post-github-comment":
        return await post_github_comment(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


async def fetch_github_issue(arguments: dict) -> list[TextContent]:
    """Fetch GitHub issue details using gh CLI."""
    issue_url = arguments["issue_url"]
    
    def _fetch():
        # Extract owner, repo, and issue number from URL
        parts = issue_url.rstrip('/').split('/')
        owner, repo, issue_num = parts[-4], parts[-3], parts[-1]
        
        # Get GitHub token from environment
        token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
        env = os.environ.copy()
        if token:
            env['GITHUB_TOKEN'] = token
        
        # Fetch issue using gh CLI
        cmd = ['gh', 'issue', 'view', issue_num, '--repo', f'{owner}/{repo}', '--json', 'title,body,number,labels']
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', env=env)
        
        if result.returncode != 0:
            return f"Error fetching issue: {result.stderr}"
        
        issue_data = json.loads(result.stdout)
        
        return f"""**Issue #{issue_data['number']}: {issue_data['title']}**

**Body:**
{issue_data['body']}

**Labels:** {', '.join(label['name'] for label in issue_data.get('labels', []))}
"""
    
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, _fetch)
        return [TextContent(type="text", text=response)]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def search_codebase_files(arguments: dict) -> list[TextContent]:
    """Search for files matching keywords."""
    keywords = arguments["keywords"]
    max_files = arguments.get("max_files", 10)
    
    try:
        # Use asyncio.create_subprocess_exec for truly async subprocess
        process = await asyncio.create_subprocess_exec(
            'git', 'ls-files',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=os.getcwd()
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            return [TextContent(type="text", text=f"Error listing files: {stderr.decode('utf-8')}")]
        
        all_files = stdout.decode('utf-8').strip().split('\n')
        
        # Score files based on keyword matches (fast in-memory operation)
        scored_files = []
        for filepath in all_files:
            score = sum(filepath.lower().count(kw.lower()) for kw in keywords)
            if score > 0:
                scored_files.append((score, filepath))
        
        # Sort and take top N
        scored_files.sort(reverse=True, key=lambda x: x[0])
        top_files = [f for _, f in scored_files[:max_files]]
        
        if not top_files:
            response = f"No files found matching keywords: {', '.join(keywords)}"
        else:
            response = f"**Found {len(top_files)} relevant files:**\n\n"
            response += '\n'.join(f"- {f}" for f in top_files)
        
        return [TextContent(type="text", text=response)]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def create_mermaid_diagram(arguments: dict) -> list[TextContent]:
    """Create a Mermaid diagram."""
    issue_title = arguments["issue_title"]
    issue_number = arguments["issue_number"]
    files = arguments["files"]
    
    try:
        diagram = f"""graph TD
    Issue[\"Issue #{issue_number}: {issue_title}\"]
"""
        
        for i, filepath in enumerate(files, 1):
            file_id = f"File{i}"
            diagram += f"    {file_id}[\"{filepath}\"]\n"
            diagram += f"    Issue --> {file_id}\n"
        
        response = f"""**Mermaid Diagram:**

```mermaid
{diagram}```
"""
        
        return [TextContent(type="text", text=response)]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def post_github_comment(arguments: dict) -> list[TextContent]:
    """Post a comment to a GitHub issue."""
    issue_url = arguments["issue_url"]
    comment = arguments["comment"]
    
    def _post():
        # Extract owner, repo, and issue number from URL
        parts = issue_url.rstrip('/').split('/')
        owner, repo, issue_num = parts[-4], parts[-3], parts[-1]
        
        # Get GitHub token from environment
        token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
        env = os.environ.copy()
        if token:
            env['GITHUB_TOKEN'] = token
        
        # Post comment using gh CLI
        cmd = ['gh', 'issue', 'comment', issue_num, '--repo', f'{owner}/{repo}', '--body', comment]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', env=env)
        
        if result.returncode != 0:
            return f"Error posting comment: {result.stderr}"
        
        return f"✅ Successfully posted comment to issue #{issue_num}"
    
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, _post)
        return [TextContent(type="text", text=response)]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server
    
    print("Starting GitHub Issue Analyzer MCP Server...", file=sys.stderr)
    print("Providing tools: fetch-github-issue, search-codebase-files, create-mermaid-diagram, post-github-comment", file=sys.stderr)
    
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
