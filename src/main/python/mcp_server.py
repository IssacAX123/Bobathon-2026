#!/usr/bin/env python3
"""
MCP Server for GitHub Issue Analysis
Implements Story 4: Single MCP tool that orchestrates the entire workflow
"""

import json
import sys
import time
import re
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import subprocess
import os

from github_issue_analyzer import GitHubIssueAnalyzer
from diagram_generator import DiagramGenerator
from comment_poster import GitHubCommentPoster


@dataclass
class AnalysisResult:
    """Result of the complete analysis workflow."""
    success: bool
    issue: Optional[Dict[str, Any]] = None
    packages_found: int = 0
    diagram_generated: bool = False
    comment_url: Optional[str] = None
    execution_time_ms: int = 0
    error_message: Optional[str] = None
    failed_step: Optional[str] = None
    partial_results: Optional[Dict[str, Any]] = None


class WorkflowOrchestrator:
    """Orchestrates the complete GitHub issue analysis workflow."""
    
    def __init__(self, github_token: Optional[str] = None, dry_run: bool = False):
        """
        Initialize the orchestrator.
        
        Args:
            github_token: GitHub personal access token
            dry_run: If True, performs analysis but doesn't post to GitHub
        """
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.dry_run = dry_run
        self.start_time = None
        
    def analyze_issue(self, issue_url: str) -> AnalysisResult:
        """
        Execute the complete workflow for analyzing a GitHub issue.
        
        Args:
            issue_url: Full URL of the GitHub issue
            
        Returns:
            AnalysisResult with success status and details
        """
        self.start_time = time.time()
        
        try:
            # Step 1: Validate URL
            self._log_progress("🔍 Validating issue URL...")
            self._validate_url(issue_url)
            self._log_progress("✓ URL validated\n")
            
            # Step 2: Fetch and analyze issue
            self._log_progress("🔍 Fetching issue from GitHub...")
            analyzer = GitHubIssueAnalyzer(self.github_token)
            analysis_result = analyzer.analyze_issue(issue_url)
            
            # Convert AnalysisResult to dict if needed
            if hasattr(analysis_result, '__dict__'):
                analysis = asdict(analysis_result)
            else:
                analysis = analysis_result
            
            issue = analysis.get('issue', {})
            if hasattr(issue, '__dict__'):
                issue = asdict(issue)
            
            packages = analysis.get('packages', [])
            if packages and hasattr(packages[0], '__dict__'):
                packages = [asdict(p) for p in packages]
            
            self._log_progress(f"✓ Issue #{issue.get('number')} fetched: \"{issue.get('title', 'Unknown')}\"")
            self._log_progress(f"✓ Found {len(packages)} package(s)\n")
            
            # Step 3: Generate diagram
            self._log_progress("📊 Generating architecture diagram...")
            generator = DiagramGenerator()
            # Pass the dict version to diagram generator
            diagram = generator.generate_diagram(analysis)
            self._log_progress("✓ Diagram generated\n")
            
            # Step 4: Post comment (or skip if dry-run)
            comment_url = None
            if self.dry_run:
                self._log_progress("🔍 Dry run mode - skipping GitHub post\n")
            else:
                self._log_progress("📝 Posting analysis to GitHub...")
                poster = GitHubCommentPoster(self.github_token, dry_run=False)
                # Pass the dict version to comment poster
                result = poster.post_analysis(issue_url, analysis, diagram)
                
                if result.success:
                    comment_url = result.comment_url
                    self._log_progress(f"✓ Comment posted: {comment_url}")
                    self._log_progress("✓ Label 'bot-analyzed' added\n")
                else:
                    raise Exception(f"Failed to post comment: {result.error_message}")
            
            # Calculate execution time
            execution_time_ms = int((time.time() - self.start_time) * 1000)
            
            self._log_progress(f"✅ Analysis complete in {execution_time_ms/1000:.1f} seconds!")
            
            return AnalysisResult(
                success=True,
                issue={
                    'number': issue.get('number'),
                    'title': issue.get('title')
                },
                packages_found=len(packages),
                diagram_generated=True,
                comment_url=comment_url,
                execution_time_ms=execution_time_ms
            )
            
        except Exception as e:
            execution_time_ms = int((time.time() - self.start_time) * 1000)
            error_step = self._determine_failed_step(str(e))
            
            self._log_progress(f"\n❌ Error in step '{error_step}': {str(e)}")
            
            return AnalysisResult(
                success=False,
                error_message=str(e),
                failed_step=error_step,
                execution_time_ms=execution_time_ms
            )
    
    def _validate_url(self, url: str):
        """Validate GitHub issue URL format."""
        if not url:
            raise ValueError("Issue URL is required")
        
        # Support both github.com and GitHub Enterprise
        pattern = r'^https://github\.com/[^/]+/[^/]+/issues/\d+$'
        if not re.match(pattern, url):
            raise ValueError("Invalid GitHub issue URL format. Expected: https://github.com/owner/repo/issues/123")
    
    def _determine_failed_step(self, error_message: str) -> str:
        """Determine which step failed based on error message."""
        error_lower = error_message.lower()
        
        if 'url' in error_lower or 'format' in error_lower:
            return 'validate-url'
        elif 'fetch' in error_lower or '404' in error_lower or 'not found' in error_lower:
            return 'fetch-issue'
        elif 'package' in error_lower or 'analyz' in error_lower:
            return 'analyze-packages'
        elif 'diagram' in error_lower or 'mermaid' in error_lower:
            return 'generate-diagram'
        elif 'post' in error_lower or 'comment' in error_lower:
            return 'post-comment'
        else:
            return 'unknown'
    
    def _log_progress(self, message: str):
        """Log progress message to stderr."""
        print(message, file=sys.stderr)


def create_mcp_tool_definition() -> Dict[str, Any]:
    """Create the MCP tool definition for Bob."""
    return {
        "name": "analyze-github-issue",
        "description": "Analyzes a GitHub issue, identifies Liberty packages, generates architecture diagram, and posts analysis as a comment",
        "inputSchema": {
            "type": "object",
            "properties": {
                "issueUrl": {
                    "type": "string",
                    "description": "Full URL of the GitHub issue to analyze",
                    "pattern": "^https://github\\.com/[^/]+/[^/]+/issues/\\d+$"
                },
                "dryRun": {
                    "type": "boolean",
                    "description": "If true, performs analysis but does not post to GitHub",
                    "default": False
                }
            },
            "required": ["issueUrl"]
        }
    }


def handle_mcp_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle an MCP tool invocation request.
    
    Args:
        request: MCP request with method and params
        
    Returns:
        MCP response with result or error
    """
    try:
        method = request.get('method')
        params = request.get('params', {})
        
        if method == 'tools/list':
            # Return list of available tools
            return {
                "tools": [create_mcp_tool_definition()]
            }
        
        elif method == 'tools/call':
            # Execute the tool
            tool_name = params.get('name')
            arguments = params.get('arguments', {})
            
            if tool_name != 'analyze-github-issue':
                return {
                    "error": {
                        "code": -32601,
                        "message": f"Unknown tool: {tool_name}"
                    }
                }
            
            # Extract parameters
            issue_url = arguments.get('issueUrl')
            dry_run = arguments.get('dryRun', False)
            
            if not issue_url:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: issueUrl"
                    }
                }
            
            # Execute workflow
            orchestrator = WorkflowOrchestrator(dry_run=dry_run)
            result = orchestrator.analyze_issue(issue_url)
            
            # Return result
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(asdict(result), indent=2)
                    }
                ]
            }
        
        else:
            return {
                "error": {
                    "code": -32601,
                    "message": f"Unknown method: {method}"
                }
            }
    
    except Exception as e:
        return {
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        }


def main():
    """Main entry point for MCP server."""
    if len(sys.argv) > 1 and sys.argv[1] == '--stdio':
        # MCP stdio mode - read JSON-RPC requests from stdin
        print("MCP Server started in stdio mode", file=sys.stderr)
        
        for line in sys.stdin:
            try:
                request = json.loads(line)
                response = handle_mcp_request(request)
                print(json.dumps(response))
                sys.stdout.flush()
            except json.JSONDecodeError as e:
                error_response = {
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {str(e)}"
                    }
                }
                print(json.dumps(error_response))
                sys.stdout.flush()
    
    else:
        # CLI mode - direct invocation
        if len(sys.argv) < 2:
            print("Usage: python mcp_server.py <issue_url> [--dry-run]", file=sys.stderr)
            print("   or: python mcp_server.py --stdio  (for MCP mode)", file=sys.stderr)
            sys.exit(1)
        
        # Parse arguments
        dry_run = '--dry-run' in sys.argv
        args = [arg for arg in sys.argv[1:] if arg != '--dry-run']
        
        if not args:
            print("Error: Issue URL is required", file=sys.stderr)
            sys.exit(1)
        
        issue_url = args[0]
        
        orchestrator = WorkflowOrchestrator(dry_run=dry_run)
        result = orchestrator.analyze_issue(issue_url)
        
        # Print result as JSON to stdout
        print(json.dumps(asdict(result), indent=2))
        
        # Exit with appropriate code
        sys.exit(0 if result.success else 1)


if __name__ == '__main__':
    main()

# Made with Bob
