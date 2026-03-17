#!/usr/bin/env python3
"""
GitHub Issue Analyzer - Story 1 Implementation
Fetches and analyzes GitHub issues to identify Liberty packages.

This implementation uses flexible pattern matching and AI-assisted analysis
to handle unstructured issue descriptions.
"""

import re
import os
import json
import requests
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from urllib.parse import urlparse


@dataclass
class Package:
    """Represents an identified Liberty package."""
    name: str
    confidence: float
    context: str
    package_type: str  # 'LIBERTY', 'IBM', 'UNKNOWN'
    location: str  # Where in the issue it was found


@dataclass
class Issue:
    """Represents a GitHub issue."""
    number: int
    title: str
    body: str
    labels: List[str]
    url: str
    created_at: str
    author: str


@dataclass
class AnalysisResult:
    """Complete analysis result."""
    issue: Optional[Issue]
    packages: List[Package]
    analysis_time_ms: int
    success: bool
    error_message: Optional[str] = None


class GitHubIssueAnalyzer:
    """Analyzes GitHub issues to identify Liberty packages."""
    
    # Regex patterns for package identification
    LIBERTY_PATTERN = re.compile(r'io\.openliberty\.[a-z0-9._]+', re.IGNORECASE)
    IBM_PATTERN = re.compile(r'com\.ibm\.ws\.[a-z0-9._]+', re.IGNORECASE)
    
    # Keyword-to-package mappings for natural language issues
    KEYWORD_MAPPINGS = {
        'ltpa': [
            ('com.ibm.ws.security.token.ltpa', 0.90, 'LTPA token processing'),
            ('com.ibm.ws.crypto.ltpakeyutil', 0.95, 'LTPA key generation and encryption'),
            ('com.ibm.ws.security.token.ltpa.internal', 0.85, 'Internal LTPA implementation')
        ],
        'ltpa.keys': [
            ('com.ibm.ws.crypto.ltpakeyutil', 0.95, 'LTPA key file operations'),
        ],
        'securityutility': [
            ('com.ibm.ws.security.utility', 0.90, 'securityUtility command'),
        ],
        'security utility': [
            ('com.ibm.ws.security.utility', 0.90, 'securityUtility command'),
        ],
        'pqc': [
            ('com.ibm.ws.crypto.ltpakeyutil', 0.85, 'Post-quantum cryptography support'),
        ],
        'fips': [
            ('com.ibm.ws.crypto.ltpakeyutil', 0.80, 'FIPS compliance'),
        ],
        'jwt': [
            ('io.openliberty.security.jwt', 0.90, 'JWT token processing'),
            ('io.openliberty.security.jwt.internal', 0.85, 'Internal JWT implementation'),
        ],
        'jakartasec': [
            ('io.openliberty.security.jakartasec.3.0.internal', 0.85, 'Jakarta Security 3.0'),
            ('io.openliberty.security.jakartasec.4.0.internal', 0.85, 'Jakarta Security 4.0'),
        ],
        'jakarta security': [
            ('io.openliberty.security.jakartasec.3.0.internal', 0.85, 'Jakarta Security 3.0'),
            ('io.openliberty.security.jakartasec.4.0.internal', 0.85, 'Jakarta Security 4.0'),
        ],
    }
    
    # Context keywords that increase confidence
    CONTEXT_KEYWORDS = {
        'error': 1.1,
        'exception': 1.15,
        'fails': 1.1,
        'issue': 1.05,
        'problem': 1.1,
        'bug': 1.1,
        'crash': 1.15,
        'stacktrace': 1.2,
        'trace': 1.15,
    }
    
    # Package relationship patterns
    INTERNAL_SUFFIX = re.compile(r'\.internal$')
    IMPL_SUFFIX = re.compile(r'\.impl$')
    
    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize the analyzer.
        
        Args:
            github_token: GitHub personal access token (optional, but recommended)
        """
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.session = requests.Session()
        if self.github_token:
            self.session.headers.update({
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            })
    
    def analyze_issue(self, issue_url: str) -> AnalysisResult:
        """
        Main entry point: Analyze a GitHub issue.
        
        Args:
            issue_url: Full URL of the GitHub issue
            
        Returns:
            AnalysisResult with identified packages
        """
        start_time = datetime.now()
        
        try:
            # Validate URL
            if not self._validate_url(issue_url):
                return AnalysisResult(
                    issue=None,
                    packages=[],
                    analysis_time_ms=0,
                    success=False,
                    error_message="Invalid GitHub issue URL format"
                )
            
            # Fetch issue
            issue = self._fetch_issue(issue_url)
            
            # Analyze packages
            packages = self._analyze_packages(issue)
            
            # Calculate execution time
            elapsed = (datetime.now() - start_time).total_seconds() * 1000
            
            return AnalysisResult(
                issue=issue,
                packages=packages,
                analysis_time_ms=int(elapsed),
                success=True
            )
            
        except Exception as e:
            elapsed = (datetime.now() - start_time).total_seconds() * 1000
            return AnalysisResult(
                issue=None,
                packages=[],
                analysis_time_ms=int(elapsed),
                success=False,
                error_message=str(e)
            )
    
    def _validate_url(self, url: str) -> bool:
        """Validate GitHub issue URL format (supports github.com and GitHub Enterprise)."""
        # Support both github.com and GitHub Enterprise (e.g., github.ibm.com)
        pattern = r'^https://github(?:\.[a-z0-9-]+)*\.com/[^/]+/[^/]+/issues/\d+$'
        return bool(re.match(pattern, url))
    
    def _fetch_issue(self, issue_url: str) -> Issue:
        """
        Fetch issue from GitHub API.
        
        Args:
            issue_url: GitHub issue URL
            
        Returns:
            Issue object
        """
        # Parse URL to get API endpoint
        # https://github.com/owner/repo/issues/123 -> https://api.github.com/repos/owner/repo/issues/123
        # https://github.ibm.com/owner/repo/issues/123 -> https://github.ibm.com/api/v3/repos/owner/repo/issues/123
        
        parsed = urlparse(issue_url)
        path_parts = parsed.path.strip('/').split('/')
        
        if len(path_parts) != 4 or path_parts[2] != 'issues':
            raise ValueError("Invalid GitHub issue URL")
        
        owner, repo, _, issue_number = path_parts
        
        # Construct API URL based on hostname
        if parsed.hostname == 'github.com':
            # Public GitHub
            api_url = f'https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}'
        else:
            # GitHub Enterprise (e.g., github.ibm.com)
            api_url = f'https://{parsed.hostname}/api/v3/repos/{owner}/{repo}/issues/{issue_number}'
        
        response = self.session.get(api_url, timeout=10)
        
        if response.status_code == 404:
            raise ValueError("Issue not found or not accessible")
        elif response.status_code == 403:
            raise ValueError("GitHub API rate limit exceeded")
        elif response.status_code != 200:
            raise ValueError(f"GitHub API error: {response.status_code}")
        
        data = response.json()
        
        return Issue(
            number=data['number'],
            title=data['title'],
            body=data.get('body', ''),
            labels=[label['name'] for label in data.get('labels', [])],
            url=data['html_url'],
            created_at=data['created_at'],
            author=data['user']['login']
        )
    
    def _analyze_packages(self, issue: Issue) -> List[Package]:
        """
        Analyze issue text to identify packages.
        
        This uses multiple strategies:
        1. Direct regex matching
        2. Keyword-to-package mapping (for natural language)
        3. Context-aware confidence scoring
        4. Code block detection
        5. Stack trace parsing
        """
        packages = []
        text = f"{issue.title}\n\n{issue.body}"
        
        # Strategy 1: Find all Liberty packages
        liberty_matches = self._find_packages_with_context(
            text, self.LIBERTY_PATTERN, 'LIBERTY'
        )
        packages.extend(liberty_matches)
        
        # Strategy 2: Find all IBM packages
        ibm_matches = self._find_packages_with_context(
            text, self.IBM_PATTERN, 'IBM'
        )
        packages.extend(ibm_matches)
        
        # Strategy 3: Parse stack traces for additional packages
        stack_trace_packages = self._parse_stack_traces(text)
        packages.extend(stack_trace_packages)
        
        # Strategy 4: Keyword-to-package mapping (for natural language issues)
        keyword_packages = self._find_packages_by_keywords(text)
        packages.extend(keyword_packages)
        
        # Deduplicate and sort by confidence
        packages = self._deduplicate_packages(packages)
        packages.sort(key=lambda p: p.confidence, reverse=True)
        
        return packages
    
    def _find_packages_with_context(
        self, 
        text: str, 
        pattern: re.Pattern, 
        pkg_type: str
    ) -> List[Package]:
        """Find packages and calculate confidence based on context."""
        packages = []
        
        for match in pattern.finditer(text):
            package_name = match.group(0)
            start, end = match.span()
            
            # Get surrounding context (50 chars before and after)
            context_start = max(0, start - 50)
            context_end = min(len(text), end + 50)
            context = text[context_start:context_end]
            
            # Determine location
            location = self._determine_location(text, start)
            
            # Calculate confidence
            confidence = self._calculate_confidence(
                package_name, context, location
            )
            
            packages.append(Package(
                name=package_name,
                confidence=confidence,
                context=context.strip(),
                package_type=pkg_type,
                location=location
            ))
        
        return packages
    
    def _parse_stack_traces(self, text: str) -> List[Package]:
        """Parse stack traces to find additional packages."""
        packages = []
        
        # Look for common stack trace patterns
        # Example: at io.openliberty.security.jwt.JwtTokenValidator.validate(...)
        stack_pattern = re.compile(
            r'at\s+(io\.openliberty\.[a-z0-9.]+|com\.ibm\.ws\.[a-z0-9.]+)\.',
            re.IGNORECASE
        )
        
        for match in stack_pattern.finditer(text):
            package_name = match.group(1)
            
            # High confidence for stack traces
            packages.append(Package(
                name=package_name,
                confidence=0.95,
                context=match.group(0),
                package_type='LIBERTY' if 'openliberty' in package_name else 'IBM',
                location='stack_trace'
            ))
        
        return packages
    def _find_packages_by_keywords(self, text: str) -> List[Package]:
        """
        Find packages based on keyword mappings for natural language issues.
        
        This helps identify packages when issues use terms like "LTPA" or 
        "securityUtility" instead of explicit package names.
        """
        packages = []
        text_lower = text.lower()
        
        for keyword, mappings in self.KEYWORD_MAPPINGS.items():
            if keyword in text_lower:
                for package_name, confidence, context in mappings:
                    # Determine package type
                    if package_name.startswith('io.openliberty'):
                        pkg_type = 'LIBERTY'
                    elif package_name.startswith('com.ibm.ws'):
                        pkg_type = 'IBM'
                    else:
                        pkg_type = 'UNKNOWN'
                    
                    packages.append(Package(
                        name=package_name,
                        confidence=confidence,
                        context=context,
                        package_type=pkg_type,
                        location='inferred'
                    ))
        
        return packages
    
    
    def _determine_location(self, text: str, position: int) -> str:
        """Determine where in the issue the package was found."""
        # Check if in code block
        before_text = text[:position]
        
        if '```' in before_text:
            # Count code block markers
            code_blocks = before_text.count('```')
            if code_blocks % 2 == 1:  # Odd number means we're inside a code block
                return 'code_block'
        
        # Check if in title (first 200 chars)
        if position < 200:
            return 'title'
        
        return 'description'
    
    def _calculate_confidence(
        self, 
        package_name: str, 
        context: str, 
        location: str
    ) -> float:
        """
        Calculate confidence score for a package identification.
        
        Factors:
        - Base confidence: 0.70
        - Location bonus: code_block (+0.20), title (+0.10), stack_trace (+0.25)
        - Context keywords: +5-20% per keyword
        - Package completeness: full package name (+0.10)
        """
        confidence = 0.70  # Base confidence
        
        # Location bonus
        if location == 'code_block':
            confidence += 0.20
        elif location == 'title':
            confidence += 0.10
        elif location == 'stack_trace':
            confidence += 0.25
        
        # Context keyword bonus
        context_lower = context.lower()
        for keyword, multiplier in self.CONTEXT_KEYWORDS.items():
            if keyword in context_lower:
                confidence *= multiplier
        
        # Package completeness bonus
        # More dots = more specific package
        dot_count = package_name.count('.')
        if dot_count >= 4:  # e.g., io.openliberty.security.jwt.internal
            confidence += 0.10
        elif dot_count >= 3:  # e.g., io.openliberty.security.jwt
            confidence += 0.05
        
        # Cap at 1.0
        return min(confidence, 1.0)
    
    def _deduplicate_packages(self, packages: List[Package]) -> List[Package]:
        """Remove duplicate packages, keeping the one with highest confidence."""
        seen = {}
        
        for pkg in packages:
            if pkg.name not in seen or pkg.confidence > seen[pkg.name].confidence:
                seen[pkg.name] = pkg
        
        return list(seen.values())
    
    def to_json(self, result: AnalysisResult) -> str:
        """Convert analysis result to JSON."""
        return json.dumps({
            'success': result.success,
            'analysis_time_ms': result.analysis_time_ms,
            'error_message': result.error_message,
            'issue': asdict(result.issue) if result.issue else None,
            'packages': [asdict(pkg) for pkg in result.packages]
        }, indent=2)


def main():
    """CLI entry point for testing."""
    import sys
    
    # Check for --json-only flag
    json_only = '--json-only' in sys.argv
    if json_only:
        sys.argv.remove('--json-only')
    
    if len(sys.argv) < 2:
        print("Usage: python github_issue_analyzer.py [--json-only] <issue_url>")
        print("Example: python github_issue_analyzer.py https://github.com/OpenLiberty/open-liberty/issues/12345")
        print("  --json-only: Output only JSON (for piping to diagram_generator.py)")
        sys.exit(1)
    
    issue_url = sys.argv[1]
    
    # Initialize analyzer
    analyzer = GitHubIssueAnalyzer()
    
    # Analyze issue
    if not json_only:
        print(f"Analyzing issue: {issue_url}")
        print()
    
    result = analyzer.analyze_issue(issue_url)
    
    if not result.success:
        if json_only:
            # Output error as JSON for downstream tools
            print(analyzer.to_json(result))
        else:
            print(f"❌ Error: {result.error_message}")
        sys.exit(1)
    
    # JSON-only mode: just output JSON and exit
    if json_only:
        print(analyzer.to_json(result))
        sys.exit(0)
    
    # Human-readable output
    print(f"✅ Analysis complete in {result.analysis_time_ms}ms")
    print()
    
    if result.issue:
        print(f"Issue #{result.issue.number}: {result.issue.title}")
        print(f"Author: {result.issue.author}")
        print(f"Created: {result.issue.created_at}")
        print()
    
    if result.packages:
        print(f"Identified {len(result.packages)} package(s):")
        print()
        for i, pkg in enumerate(result.packages, 1):
            print(f"{i}. {pkg.name}")
            print(f"   Confidence: {pkg.confidence:.0%}")
            print(f"   Type: {pkg.package_type}")
            print(f"   Location: {pkg.location}")
            print(f"   Context: ...{pkg.context[:60]}...")
            print()
    else:
        print("No Liberty packages identified in issue description.")
        print()
        print("Suggestions:")
        print("- Ensure the issue mentions package names")
        print("- Use format: io.openliberty.package.name or com.ibm.ws.package.name")
    
    # Print JSON output
    print("\n" + "="*80)
    print("JSON Output:")
    print("="*80)
    print(analyzer.to_json(result))


if __name__ == '__main__':
    main()

# Made with Bob
