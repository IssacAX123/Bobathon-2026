#!/usr/bin/env python3
"""
Flask Web UI for GitHub Issue Analyzer
Simple web interface to analyze GitHub issues and display results.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from github_issue_analyzer import GitHubIssueAnalyzer, AnalysisResult
from diagram_generator import DiagramGenerator, Package as DiagramPackage
import os
import requests
from datetime import datetime
from typing import Optional

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Initialize analyzer and diagram generator
analyzer = GitHubIssueAnalyzer()
diagram_generator = DiagramGenerator()


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_issue():
    """
    API endpoint to analyze a GitHub issue.
    
    Request JSON:
        {
            "issue_url": "https://github.com/owner/repo/issues/123",
            "github_token": "ghp_..." (optional)
        }
    
    Response JSON:
        {
            "success": true,
            "issue": {...},
            "packages": [...],
            "analysis_time_ms": 1234
        }
    """
    try:
        data = request.get_json()
        issue_url = data.get('issue_url', '').strip()
        github_token = data.get('github_token', '').strip()
        
        if not issue_url:
            return jsonify({
                'success': False,
                'error': 'Issue URL is required'
            }), 400
        
        # Create analyzer with token if provided
        if github_token:
            temp_analyzer = GitHubIssueAnalyzer(github_token=github_token)
            result = temp_analyzer.analyze_issue(issue_url)
        else:
            # Use default analyzer (with env token if set)
            result = analyzer.analyze_issue(issue_url)
        
        # Convert to JSON-serializable format
        response = {
            'success': result.success,
            'analysis_time_ms': result.analysis_time_ms,
            'error_message': result.error_message
        }
        
        if result.issue:
            response['issue'] = {
                'number': result.issue.number,
                'title': result.issue.title,
                'body': result.issue.body,
                'labels': result.issue.labels,
                'url': result.issue.url,
                'created_at': result.issue.created_at,
                'author': result.issue.author
            }
        
        if result.packages:
            response['packages'] = [
                {
                    'name': pkg.name,
                    'confidence': pkg.confidence,
                    'context': pkg.context,
                    'package_type': pkg.package_type,
                    'location': pkg.location
                }
                for pkg in result.packages
            ]
        else:
            response['packages'] = []
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/generate-diagram', methods=['POST'])
def generate_diagram():
    """
    Generate a Mermaid diagram from packages using the enhanced DiagramGenerator.
    
    Request JSON:
        {
            "packages": [...],
            "issue": {...}
        }
    
    Response JSON:
        {
            "diagram": "mermaid syntax...",
            "success": true,
            "additional_packages": [...]
        }
    """
    try:
        data = request.get_json()
        
        # Use the enhanced diagram generator
        result = diagram_generator.generate_diagram(data)
        
        # Strip markdown code fences for frontend rendering
        diagram_content = result.mermaid
        if diagram_content:
            # Remove ```mermaid and ``` wrappers
            diagram_content = diagram_content.replace('```mermaid', '').replace('```', '').strip()
        
        return jsonify({
            'success': result.success,
            'diagram': diagram_content,
            'additional_packages': [
                {
                    'name': pkg.name,
                    'confidence': pkg.confidence,
                    'package_type': pkg.package_type
                }
                for pkg in result.additional_packages
            ],
            'error_message': result.error_message
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/post-comment', methods=['POST'])
def post_comment():
    """
    Post analysis as a comment to the GitHub issue.
    
    Request JSON:
        {
            "issue_url": "https://github.com/owner/repo/issues/123",
            "github_token": "ghp_...",
            "analysis_result": {...}
        }
    
    Response JSON:
        {
            "success": true,
            "comment_url": "https://github.com/.../issues/123#comment-456",
            "message": "Comment posted successfully"
        }
    """
    try:
        data = request.get_json()
        issue_url = data.get('issue_url', '').strip()
        github_token = data.get('github_token', '').strip()
        analysis_result = data.get('analysis_result', {})
        
        if not issue_url:
            return jsonify({
                'success': False,
                'error': 'Issue URL is required'
            }), 400
        
        if not github_token:
            return jsonify({
                'success': False,
                'error': 'GitHub token is required to post comments'
            }), 400
        
        # Format the comment
        comment_body = format_analysis_comment(analysis_result)
        
        # Post the comment
        comment_url = post_github_comment(issue_url, github_token, comment_body)
        
        # Try to add label (non-blocking)
        try:
            add_github_label(issue_url, github_token, 'bot-analyzed')
        except Exception as label_error:
            print(f"Warning: Could not add label: {label_error}")
        
        return jsonify({
            'success': True,
            'comment_url': comment_url,
            'message': 'Comment posted successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def format_analysis_comment(analysis_result: dict) -> str:
    """Format the analysis result as a GitHub comment."""
    issue = analysis_result.get('issue', {})
    packages = analysis_result.get('packages', [])
    diagram = analysis_result.get('diagram', '')
    
    lines = [
        "## 🤖 Automated Analysis by Bob",
        "",
        f"**Issue**: #{issue.get('number', 'N/A')} - {issue.get('title', 'N/A')}",
        ""
    ]
    
    if packages:
        lines.append(f"### Identified Packages ({len(packages)})")
        for pkg in packages:
            confidence = int(pkg['confidence'] * 100)
            emoji = "🟢" if confidence >= 80 else "🟡" if confidence >= 60 else "🟠"
            lines.append(f"- {emoji} `{pkg['name']}` (confidence: {confidence}%)")
        lines.append("")
    else:
        lines.append("### Analysis Result")
        lines.append("No Liberty packages were identified in the issue description.")
        lines.append("")
        lines.append("### Suggestions")
        lines.append("- If this is a code issue, please mention the affected package names")
        lines.append("- Use format: `io.openliberty.package.name` or `com.ibm.ws.package.name`")
        lines.append("- Re-run analysis after updating the description")
        lines.append("")
    
    if diagram and packages:
        lines.append("### Architecture Diagram")
        # Add markdown code fences for GitHub rendering
        if not diagram.startswith('```'):
            lines.append("```mermaid")
            lines.append(diagram)
            lines.append("```")
        else:
            lines.append(diagram)
        lines.append("")
    
    lines.append("---")
    lines.append(f"*Analysis generated at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*")
    lines.append("*Version: 1.0.0*")
    
    return "\n".join(lines)


def post_github_comment(issue_url: str, github_token: str, comment_body: str) -> str:
    """Post a comment to a GitHub issue and return the comment URL."""
    from urllib.parse import urlparse
    
    # Parse the issue URL to get API endpoint
    parsed = urlparse(issue_url)
    path_parts = parsed.path.strip('/').split('/')
    
    if len(path_parts) != 4 or path_parts[2] != 'issues':
        raise ValueError("Invalid GitHub issue URL")
    
    owner, repo, _, issue_number = path_parts
    
    # Construct API URL
    if parsed.hostname == 'github.com':
        api_url = f'https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments'
    else:
        api_url = f'https://{parsed.hostname}/api/v3/repos/{owner}/{repo}/issues/{issue_number}/comments'
    
    # Post the comment
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        api_url,
        headers=headers,
        json={'body': comment_body},
        timeout=10
    )
    
    if response.status_code == 403:
        raise ValueError("Permission denied: Cannot post comments to this issue")
    elif response.status_code == 404:
        raise ValueError("Issue not found or not accessible")
    elif response.status_code not in (200, 201):
        raise ValueError(f"GitHub API error: {response.status_code} - {response.text}")
    
    comment_data = response.json()
    return comment_data.get('html_url', issue_url)


def add_github_label(issue_url: str, github_token: str, label: str) -> None:
    """Add a label to a GitHub issue."""
    from urllib.parse import urlparse
    
    parsed = urlparse(issue_url)
    path_parts = parsed.path.strip('/').split('/')
    owner, repo, _, issue_number = path_parts
    
    # Construct API URL
    if parsed.hostname == 'github.com':
        api_url = f'https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/labels'
    else:
        api_url = f'https://{parsed.hostname}/api/v3/repos/{owner}/{repo}/issues/{issue_number}/labels'
    
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        api_url,
        headers=headers,
        json={'labels': [label]},
        timeout=10
    )
    
    if response.status_code not in (200, 201):
        raise ValueError(f"Failed to add label: {response.status_code}")


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    print("=" * 80)
    print("🚀 GitHub Issue Analyzer Web UI")
    print("=" * 80)
    print()
    print("Starting Flask server...")
    print("Open your browser to: http://localhost:5000")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 80)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob
