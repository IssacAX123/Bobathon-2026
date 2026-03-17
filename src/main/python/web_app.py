#!/usr/bin/env python3
"""
Flask Web UI for GitHub Issue Analyzer
Simple web interface to analyze GitHub issues and display results.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from github_issue_analyzer import GitHubIssueAnalyzer, AnalysisResult
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Initialize analyzer
analyzer = GitHubIssueAnalyzer()


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
    Generate a Mermaid diagram from packages.
    
    Request JSON:
        {
            "packages": [...],
            "issue_title": "Issue title"
        }
    
    Response JSON:
        {
            "diagram": "mermaid syntax..."
        }
    """
    try:
        data = request.get_json()
        packages = data.get('packages', [])
        issue_title = data.get('issue_title', 'GitHub Issue')
        
        if not packages:
            return jsonify({
                'diagram': None,
                'message': 'No packages to visualize'
            })
        
        # Generate simple Mermaid diagram
        diagram = generate_mermaid_diagram(packages, issue_title)
        
        return jsonify({
            'diagram': diagram
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


def generate_mermaid_diagram(packages, issue_title):
    """Generate a simple Mermaid diagram from packages."""
    lines = [
        "graph TD",
        f'    Issue["📋 {issue_title[:50]}..."]'
    ]
    
    # Add top 5 packages
    for i, pkg in enumerate(packages[:5]):
        pkg_name = pkg['name'].split('.')[-1]  # Get last part of package name
        confidence = int(pkg['confidence'] * 100)
        
        # Choose emoji based on confidence
        if confidence >= 90:
            emoji = "🟢"
        elif confidence >= 70:
            emoji = "🟡"
        else:
            emoji = "🟠"
        
        lines.append(f'    P{i}["{emoji} {pkg_name}<br/>{confidence}% confidence"]')
        
        # Add connection from issue
        if confidence >= 80:
            lines.append(f'    Issue ==> P{i}')
        else:
            lines.append(f'    Issue --> P{i}')
    
    return '\n'.join(lines)


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
