#!/usr/bin/env python3
"""
Diagram Generator - Story 2 Implementation
Generates Mermaid component diagrams from identified Liberty packages.

Consumes JSON output from github_issue_analyzer.py (Story 1).
"""

import re
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class RelationType(Enum):
    """Types of relationships between packages."""
    DEPENDS_ON = "depends on"
    IMPLEMENTS = "implements"
    USES = "uses"
    CIRCULAR = "circular"


@dataclass
class Package:
    """Represents a Liberty package."""
    name: str
    confidence: float
    package_type: str  # 'LIBERTY', 'IBM', 'UNKNOWN'
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Package':
        """Create Package from dictionary."""
        return cls(
            name=data['name'],
            confidence=data['confidence'],
            package_type=data.get('package_type', 'UNKNOWN')
        )


@dataclass
class Relationship:
    """Represents a relationship between two packages."""
    source: str
    target: str
    rel_type: RelationType
    label: str


@dataclass
class DiagramResult:
    """Result of diagram generation."""
    mermaid: str
    success: bool
    additional_packages: List[Package]
    error_message: Optional[str] = None


class DiagramGenerator:
    """Generates Mermaid diagrams from package analysis."""
    
    MAX_PACKAGES = 5
    MAX_LINES = 50
    MAX_NAME_LENGTH = 30
    
    # Relationship inference patterns
    INTERNAL_SUFFIX = re.compile(r'\.internal$')
    IMPL_SUFFIX = re.compile(r'\.impl$')
    
    # Known subsystem relationships
    SUBSYSTEM_RELATIONSHIPS = {
        'security': ['authentication', 'authorization', 'token'],
        'jwt': ['security', 'token'],
        'jakartasec': ['security', 'authentication'],
        'cdi': ['injection', 'beans'],
        'jaxrs': ['servlet', 'http'],
    }
    
    def generate_diagram(self, analysis_result: dict) -> DiagramResult:
        """
        Generate Mermaid diagram from analysis result.
        
        Args:
            analysis_result: JSON output from github_issue_analyzer.py
            
        Returns:
            DiagramResult with Mermaid syntax
        """
        # Extract packages
        packages_data = analysis_result.get('packages', [])
        
        if not packages_data:
            return DiagramResult(
                mermaid="",
                success=False,
                additional_packages=[],
                error_message="No packages identified for diagram generation.\n"
                             "Please ensure the issue description mentions Liberty package names."
            )
        
        # Convert to Package objects
        packages = [Package.from_dict(p) for p in packages_data]
        
        # Sort by confidence (highest first)
        packages.sort(key=lambda p: p.confidence, reverse=True)
        
        # Split into top packages and additional
        top_packages = packages[:self.MAX_PACKAGES]
        additional_packages = packages[self.MAX_PACKAGES:]
        
        # Generate diagram
        issue = analysis_result.get('issue', {})
        mermaid = self._create_mermaid_syntax(top_packages, issue)
        
        # Validate
        if not self._validate_syntax(mermaid):
            return DiagramResult(
                mermaid="",
                success=False,
                additional_packages=[],
                error_message="Generated invalid Mermaid syntax"
            )
        
        return DiagramResult(
            mermaid=mermaid,
            success=True,
            additional_packages=additional_packages
        )
    
    def _create_mermaid_syntax(self, packages: List[Package], issue: dict) -> str:
        """Create Mermaid diagram syntax."""
        lines = []
        
        # Add title if issue info available
        if issue:
            title = self._sanitize_text(issue.get('title', ''))
            issue_num = issue.get('number', '')
            if title and issue_num:
                lines.append("```mermaid")
                lines.append("---")
                lines.append(f"title: Issue #{issue_num} - {title[:60]}")
                lines.append("---")
            else:
                lines.append("```mermaid")
        else:
            lines.append("```mermaid")
        
        # Start graph
        lines.append("graph LR")
        
        if len(packages) == 1:
            # Single package - standalone node
            node_id = "A"
            node_label = self._abbreviate_package_name(packages[0].name)
            lines.append(f"    {node_id}[{node_label}]")
            lines.append(self._get_style(node_id, packages[0]))
        else:
            # Multiple packages - infer relationships
            relationships = self._infer_relationships(packages)
            
            # Create nodes
            node_map = {}
            for idx, pkg in enumerate(packages):
                node_id = chr(65 + idx)  # A, B, C, ...
                node_label = self._abbreviate_package_name(pkg.name)
                node_map[pkg.name] = node_id
                lines.append(f"    {node_id}[{node_label}]")
            
            # Create edges
            if relationships:
                for rel in relationships:
                    source_id = node_map.get(rel.source)
                    target_id = node_map.get(rel.target)
                    if source_id and target_id:
                        if rel.rel_type == RelationType.CIRCULAR:
                            lines.append(f"    {source_id} <-->|{rel.label}| {target_id}")
                        else:
                            lines.append(f"    {source_id} -->|{rel.label}| {target_id}")
            
            # Add styling
            for pkg in packages:
                node_id = node_map.get(pkg.name)
                if node_id:
                    style = self._get_style(node_id, pkg)
                    if style:
                        lines.append(style)
        
        lines.append("```")
        
        return "\n".join(lines)
    
    def _infer_relationships(self, packages: List[Package]) -> List[Relationship]:
        """Infer relationships between packages."""
        relationships = []
        
        for i, source_pkg in enumerate(packages):
            for target_pkg in packages[i+1:]:
                rel = self._infer_relationship(source_pkg, target_pkg)
                if rel:
                    relationships.append(rel)
        
        return relationships
    
    def _infer_relationship(self, source: Package, target: Package) -> Optional[Relationship]:
        """Infer relationship between two packages."""
        source_name = source.name
        target_name = target.name
        
        # Rule 1: *.internal depends on public API
        if self.INTERNAL_SUFFIX.search(source_name):
            public_name = self.INTERNAL_SUFFIX.sub('', source_name)
            if target_name == public_name or target_name.startswith(public_name + '.'):
                return Relationship(
                    source=source_name,
                    target=target_name,
                    rel_type=RelationType.DEPENDS_ON,
                    label="depends on"
                )
        
        # Rule 2: *.impl implements interface
        if self.IMPL_SUFFIX.search(source_name):
            interface_name = self.IMPL_SUFFIX.sub('', source_name)
            if target_name == interface_name or target_name.startswith(interface_name + '.'):
                return Relationship(
                    source=source_name,
                    target=target_name,
                    rel_type=RelationType.IMPLEMENTS,
                    label="implements"
                )
        
        # Rule 3: Subsystem relationships
        source_parts = source_name.split('.')
        target_parts = target_name.split('.')
        
        for part in source_parts:
            if part in self.SUBSYSTEM_RELATIONSHIPS:
                related = self.SUBSYSTEM_RELATIONSHIPS[part]
                for target_part in target_parts:
                    if target_part in related:
                        return Relationship(
                            source=source_name,
                            target=target_name,
                            rel_type=RelationType.USES,
                            label="uses"
                        )
        
        # Rule 4: Common prefix suggests relationship
        common_prefix = self._get_common_prefix(source_name, target_name)
        if common_prefix and len(common_prefix.split('.')) >= 3:
            # Same subsystem - likely related
            return Relationship(
                source=source_name,
                target=target_name,
                rel_type=RelationType.USES,
                label="related"
            )
        
        return None
    
    def _get_common_prefix(self, name1: str, name2: str) -> str:
        """Get common prefix of two package names."""
        parts1 = name1.split('.')
        parts2 = name2.split('.')
        
        common = []
        for p1, p2 in zip(parts1, parts2):
            if p1 == p2:
                common.append(p1)
            else:
                break
        
        return '.'.join(common)
    
    def _abbreviate_package_name(self, full_name: str) -> str:
        """Abbreviate long package names while keeping clarity."""
        if len(full_name) <= self.MAX_NAME_LENGTH:
            return full_name
        
        parts = full_name.split('.')
        
        # Keep last 3 parts (most specific)
        if len(parts) > 3:
            abbreviated = '.'.join(parts[-3:])
            if len(abbreviated) <= self.MAX_NAME_LENGTH:
                return abbreviated
        
        # Keep last 2 parts
        if len(parts) > 2:
            abbreviated = '.'.join(parts[-2:])
            if len(abbreviated) <= self.MAX_NAME_LENGTH:
                return abbreviated
        
        # Just use last part
        return parts[-1]
    
    def _get_style(self, node_id: str, package: Package) -> str:
        """Get Mermaid style for package type."""
        if package.package_type == 'LIBERTY':
            color = "#e1f5ff"  # Light blue
        elif package.package_type == 'IBM':
            color = "#e8f5e9"  # Light green
        else:
            color = "#f5f5f5"  # Light gray
        
        # Add dashed border for internal packages
        if '.internal' in package.name:
            return f"    style {node_id} fill:{color},stroke:#333,stroke-width:2px,stroke-dasharray: 5 5"
        else:
            return f"    style {node_id} fill:{color},stroke:#333,stroke-width:2px"
    
    def _sanitize_text(self, text: str) -> str:
        """Sanitize text for Mermaid syntax."""
        # Remove special characters that break Mermaid
        text = re.sub(r'[<>{}[\]|]', '', text)
        # Replace quotes
        text = text.replace('"', "'")
        return text.strip()
    
    def _validate_syntax(self, mermaid: str) -> bool:
        """Validate Mermaid syntax."""
        if not mermaid:
            return False
        
        lines = mermaid.split('\n')
        
        # Check line count
        if len(lines) > self.MAX_LINES:
            return False
        
        # Check for required elements
        if '```mermaid' not in mermaid:
            return False
        
        if 'graph LR' not in mermaid and 'graph TD' not in mermaid:
            return False
        
        # Check balanced brackets
        open_brackets = mermaid.count('[')
        close_brackets = mermaid.count(']')
        if open_brackets != close_brackets:
            return False
        
        return True


def format_output(result: DiagramResult) -> str:
    """Format diagram result for display."""
    if not result.success:
        return f"❌ Error: {result.error_message}"
    
    output = []
    output.append("## 📊 Component Diagram\n")
    output.append(result.mermaid)
    
    if result.additional_packages:
        output.append(f"\n**Note**: Showing top {DiagramGenerator.MAX_PACKAGES} packages.")
        output.append("\n### Additional Packages Identified:\n")
        for pkg in result.additional_packages:
            output.append(f"- `{pkg.name}` (confidence: {pkg.confidence:.0%})")
    
    return "\n".join(output)


def main():
    """CLI entry point."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python diagram_generator.py <analysis_json_file>")
        print("   or: python diagram_generator.py <analysis_json_string>")
        sys.exit(1)
    
    # Read input
    input_arg = sys.argv[1]
    
    try:
        # Try as file first
        with open(input_arg, 'r') as f:
            analysis_result = json.load(f)
    except FileNotFoundError:
        # Try as JSON string
        try:
            analysis_result = json.loads(input_arg)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON input: {e}")
            sys.exit(1)
    
    # Generate diagram
    generator = DiagramGenerator()
    result = generator.generate_diagram(analysis_result)
    
    # Output
    print(format_output(result))
    
    # Exit code
    sys.exit(0 if result.success else 1)


if __name__ == '__main__':
    main()

# Made with Bob
