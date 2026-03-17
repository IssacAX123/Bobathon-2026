#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimal Viable MCP Server for GitHub Issue Analysis
Reads GitHub issues, analyzes codebase, generates explanations with diagrams, and posts back to issue.
"""

import os
import sys
import json
import subprocess
from typing import Optional, Dict, List
from dataclasses import dataclass
import re

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


@dataclass
class IssueAnalysis:
    """Result of analyzing a GitHub issue."""
    issue_number: int
    issue_title: str
    explanation: str
    diagram: str
    relevant_files: List[str]


class MinimalMCPServer:
    """Minimal MCP server for GitHub issue analysis."""
    
    def __init__(self, repo_path: str = ".", github_token: Optional[str] = None):
        """Initialize the server.
        
        Args:
            repo_path: Path to the repository to analyze
            github_token: GitHub personal access token (optional, will check env var if not provided)
        """
        self.repo_path = repo_path
        # Priority: 1. Provided token, 2. Environment variable, 3. gh CLI auth
        self.github_token = github_token or os.getenv('GITHUB_TOKEN') or os.getenv('GH_TOKEN')
    
    def analyze_issue(self, issue_url: str) -> IssueAnalysis:
        """Main workflow: Fetch issue → Analyze codebase → Generate explanation → Create diagram.
        
        Args:
            issue_url: GitHub issue URL (e.g., https://github.com/owner/repo/issues/123)
            
        Returns:
            IssueAnalysis with explanation and diagram
        """
        print(f"🔍 Fetching issue: {issue_url}")
        issue_data = self._fetch_issue(issue_url)
        
        print(f"📂 Analyzing codebase for relevant files...")
        relevant_files = self._find_relevant_files(issue_data['title'], issue_data['body'])
        
        print(f"💡 Generating explanation...")
        explanation = self._generate_explanation(issue_data, relevant_files)
        
        print(f"📊 Creating diagram...")
        diagram = self._create_diagram(issue_data, relevant_files)
        
        return IssueAnalysis(
            issue_number=issue_data['number'],
            issue_title=issue_data['title'],
            explanation=explanation,
            diagram=diagram,
            relevant_files=relevant_files
        )
    
    def post_analysis_to_issue(self, issue_url: str, analysis: IssueAnalysis) -> bool:
        """Post the analysis back to the GitHub issue.
        
        Args:
            issue_url: GitHub issue URL
            analysis: The analysis to post
            
        Returns:
            True if successful
        """
        print(f"💬 Posting analysis to issue...")
        
        comment = self._format_comment(analysis)
        
        # Use gh CLI to post comment
        try:
            # Set up environment with token if provided
            env = os.environ.copy()
            if self.github_token:
                env['GH_TOKEN'] = self.github_token
            
            result = subprocess.run(
                ['gh', 'issue', 'comment', issue_url, '--body', comment],
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8',
                errors='replace',
                env=env
            )
            print(f"✅ Analysis posted successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to post comment: {e.stderr}")
            return False
    
    def _fetch_issue(self, issue_url: str) -> Dict:
        """Fetch issue from GitHub using gh CLI.
        
        Args:
            issue_url: GitHub issue URL
            
        Returns:
            Dict with issue data
        """
        try:
            # Set up environment with token if provided
            env = os.environ.copy()
            if self.github_token:
                env['GH_TOKEN'] = self.github_token
            
            result = subprocess.run(
                ['gh', 'issue', 'view', issue_url, '--json', 'number,title,body'],
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8',
                errors='replace',
                env=env
            )
            if not result.stdout or result.stdout.strip() == '':
                raise Exception(f"No data returned from GitHub CLI. Error: {result.stderr}")
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to fetch issue: {e.stderr}")
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse GitHub response: {e}")
    
    def _find_relevant_files(self, title: str, body: str) -> List[str]:
        """Find relevant files in the codebase based on issue content.
        
        Args:
            title: Issue title
            body: Issue body
            
        Returns:
            List of relevant file paths
        """
        # Combine title and body for analysis
        text = f"{title} {body or ''}"
        
        # Extract keywords (simple approach: words longer than 3 chars)
        keywords = set(re.findall(r'\b[a-zA-Z]{4,}\b', text.lower()))
        
        # Search for files containing these keywords
        relevant_files = []
        
        # List all files in repo
        try:
            result = subprocess.run(
                ['git', 'ls-files'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8',
                errors='replace'
            )
            all_files = result.stdout.strip().split('\n')
            
            # Filter to code files and docs
            code_files = [f for f in all_files if f.endswith(('.py', '.java', '.js', '.ts', '.md', '.txt'))]
            
            # Search for keywords in file names and content
            for filepath in code_files[:50]:  # Limit to first 50 files for performance
                full_path = os.path.join(self.repo_path, filepath)
                
                # Check filename
                if any(keyword in filepath.lower() for keyword in keywords):
                    relevant_files.append(filepath)
                    continue
                
                # Check file content (first 1000 chars)
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(1000).lower()
                        if any(keyword in content for keyword in keywords):
                            relevant_files.append(filepath)
                except:
                    pass
                
                if len(relevant_files) >= 5:  # Limit to 5 most relevant files
                    break
        
        except subprocess.CalledProcessError:
            # If not a git repo, just list files in directory
            for root, dirs, files in os.walk(self.repo_path):
                for file in files:
                    if file.endswith(('.py', '.java', '.js', '.ts', '.md')):
                        filepath = os.path.relpath(os.path.join(root, file), self.repo_path)
                        if any(keyword in filepath.lower() for keyword in keywords):
                            relevant_files.append(filepath)
                        if len(relevant_files) >= 5:
                            break
                if len(relevant_files) >= 5:
                    break
        
        return relevant_files[:5]  # Return top 5
    
    def _generate_explanation(self, issue_data: Dict, relevant_files: List[str]) -> str:
        """Generate explanation for what needs to be done.
        
        Args:
            issue_data: Issue data from GitHub
            relevant_files: List of relevant files
            
        Returns:
            Explanation text
        """
        title = issue_data['title']
        body = issue_data['body'] or "No description provided"
        
        # Simple explanation generation
        explanation = f"""## Analysis of Issue #{issue_data['number']}

### Issue Summary
**Title:** {title}

**Description:** {body[:200]}{'...' if len(body) > 200 else ''}

### Relevant Files Identified
"""
        
        if relevant_files:
            for i, file in enumerate(relevant_files, 1):
                explanation += f"{i}. `{file}`\n"
        else:
            explanation += "*No specific files identified - this may be a general issue*\n"
        
        explanation += """
### Recommended Actions

1. **Review the relevant files** listed above
2. **Understand the context** by reading the issue description
3. **Identify the root cause** in the codebase
4. **Implement a fix** addressing the issue
5. **Test thoroughly** before submitting changes
6. **Update documentation** if needed

### Next Steps

- Assign this issue to a team member familiar with the affected files
- Create a branch for the fix
- Reference this issue in your commit messages
- Submit a pull request when ready
"""
        
        return explanation
    
    def _create_diagram(self, issue_data: Dict, relevant_files: List[str]) -> str:
        """Create a Mermaid diagram showing the issue and affected files.
        
        Args:
            issue_data: Issue data from GitHub
            relevant_files: List of relevant files
            
        Returns:
            Mermaid diagram as string
        """
        if not relevant_files:
            return f"""graph TD
    Issue["Issue #{issue_data['number']}<br/>{issue_data['title'][:40]}..."]
    NoFiles["⚠️ No specific files identified"]
    Issue -.-> NoFiles
    
    style Issue fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style NoFiles fill:#ffd43b,stroke:#fab005"""
        
        diagram = "graph TD\n"
        diagram += f"    Issue[\"Issue #{issue_data['number']}<br/>{issue_data['title'][:40]}...\"]\n"
        
        # Add file nodes
        for i, file in enumerate(relevant_files):
            node_id = f"F{i}"
            # Shorten file path if too long
            display_name = file if len(file) <= 30 else f"...{file[-27:]}"
            diagram += f"    {node_id}[\"{display_name}\"]\n"
            diagram += f"    Issue --> {node_id}\n"
        
        # Add styling
        diagram += "\n    style Issue fill:#ff6b6b,stroke:#c92a2a,color:#fff\n"
        for i in range(len(relevant_files)):
            diagram += f"    style F{i} fill:#4dabf7,stroke:#1971c2\n"
        
        return diagram
    
    def _format_comment(self, analysis: IssueAnalysis) -> str:
        """Format the analysis as a GitHub comment.
        
        Args:
            analysis: The analysis to format
            
        Returns:
            Formatted markdown comment
        """
        from datetime import datetime, timezone
        
        comment = f"""## 🤖 Automated Analysis by Bob

**Analyzed:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}

{analysis.explanation}

### 📊 Visual Overview

```mermaid
{analysis.diagram}
```

---
*This analysis was automatically generated. Please review and adjust as needed.*
"""
        return comment


def main():
    """CLI entry point for testing."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python mcp_server.py <issue_url>")
        print("Example: python mcp_server.py https://github.com/owner/repo/issues/123")
        sys.exit(1)
    
    issue_url = sys.argv[1]
    
    # Initialize server
    server = MinimalMCPServer()
    
    # Analyze issue
    print("\n" + "="*60)
    print("GitHub Issue Analyzer - Minimal MVP")
    print("="*60 + "\n")
    
    try:
        analysis = server.analyze_issue(issue_url)
        
        print("\n" + "="*60)
        print("Analysis Complete!")
        print("="*60 + "\n")
        
        print(f"Issue: #{analysis.issue_number} - {analysis.issue_title}")
        print(f"Relevant Files: {len(analysis.relevant_files)}")
        print()
        
        # Ask if user wants to post
        response = input("Post this analysis to GitHub? (y/n): ").strip().lower()
        
        if response == 'y':
            success = server.post_analysis_to_issue(issue_url, analysis)
            if success:
                print("\n✅ Done! Check the issue on GitHub.")
            else:
                print("\n❌ Failed to post. Check your GitHub CLI authentication.")
        else:
            print("\n📄 Analysis preview:")
            print(server._format_comment(analysis))
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

# Made with Bob
