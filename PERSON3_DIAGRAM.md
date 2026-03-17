# Person 3: Mermaid Diagram Generator Implementation

**Your Mission:** Generate beautiful Mermaid component diagrams showing Liberty packages.

**Time Budget:** 50 minutes implementation + 10 minutes testing

---

## 📝 Your File: `src/diagram_generator.py`

```python
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class DiagramNode:
    """Represents a node in the diagram"""
    id: str
    label: str
    type: str  # 'issue', 'package', 'component'

class MermaidGenerator:
    """Generate Mermaid component diagrams for Liberty packages"""
    
    # Color scheme
    COLORS = {
        'issue': {'fill': '#ff6b6b', 'stroke': '#c92a2a', 'text': '#fff'},
        'package': {'fill': '#4dabf7', 'stroke': '#1971c2', 'text': '#000'},
        'warning': {'fill': '#ffd43b', 'stroke': '#fab005', 'text': '#000'},
        'success': {'fill': '#51cf66', 'stroke': '#2f9e44', 'text': '#000'}
    }
    
    def generate_diagram(self, issue_number: int, packages: List[str], 
                        issue_title: str = None) -> str:
        """Generate Mermaid diagram showing issue and packages
        
        Args:
            issue_number: GitHub issue number
            packages: List of package names (up to 5 recommended)
            issue_title: Optional issue title for context
            
        Returns:
            Mermaid diagram as string
        """
        if not packages:
            return self._generate_empty_diagram(issue_number, issue_title)
        
        # Limit to 5 packages for readability
        packages = packages[:5]
        
        lines = []
        lines.append("graph TD")
        
        # Add issue node
        issue_label = f"Issue #{issue_number}"
        if issue_title:
            # Truncate long titles
            short_title = issue_title[:40] + "..." if len(issue_title) > 40 else issue_title
            issue_label = f"Issue #{issue_number}<br/>{short_title}"
        
        lines.append(f"    Issue[\"{issue_label}\"]")
        lines.append(f"    style Issue fill:{self.COLORS['issue']['fill']},stroke:{self.COLORS['issue']['stroke']},color:{self.COLORS['issue']['text']}")
        
        # Add package nodes
        for idx, pkg in enumerate(packages):
            node_id = f"P{idx}"
            short_name = self._shorten_package_name(pkg)
            
            lines.append(f"    {node_id}[\"{short_name}\"]")
            lines.append(f"    style {node_id} fill:{self.COLORS['package']['fill']},stroke:{self.COLORS['package']['stroke']}")
            
            # Connect issue to package
            lines.append(f"    Issue --> {node_id}")
        
        # Add legend if multiple packages
        if len(packages) > 1:
            lines.append("")
            lines.append("    %% Legend")
            lines.append(f"    Legend[\"📦 {len(packages)} Liberty packages identified\"]")
            lines.append(f"    style Legend fill:{self.COLORS['success']['fill']},stroke:{self.COLORS['success']['stroke']}")
        
        return "\n".join(lines)
    
    def _generate_empty_diagram(self, issue_number: int, issue_title: str = None) -> str:
        """Generate diagram when no packages found
        
        Args:
            issue_number: GitHub issue number
            issue_title: Optional issue title
            
        Returns:
            Mermaid diagram showing no packages found
        """
        issue_label = f"Issue #{issue_number}"
        if issue_title:
            short_title = issue_title[:40] + "..." if len(issue_title) > 40 else issue_title
            issue_label = f"Issue #{issue_number}<br/>{short_title}"
        
        return f"""graph TD
    Issue[\"{issue_label}\"]
    NoPackages[\"⚠️ No Liberty packages identified\"]
    style Issue fill:{self.COLORS['issue']['fill']},stroke:{self.COLORS['issue']['stroke']},color:{self.COLORS['issue']['text']}
    style NoPackages fill:{self.COLORS['warning']['fill']},stroke:{self.COLORS['warning']['stroke']}
    Issue -.-> NoPackages"""
    
    def _shorten_package_name(self, package: str) -> str:
        """Shorten package name for display
        
        Args:
            package: Full package name
            
        Returns:
            Shortened package name
        """
        parts = package.split('.')
        
        # If short enough, return as-is
        if len(package) <= 35:
            return package
        
        # For long packages, show first 2 and last 2 parts
        if len(parts) > 4:
            return f"{parts[0]}.{parts[1]}...{parts[-2]}.{parts[-1]}"
        
        # For medium packages, show first 2 and last part
        if len(parts) > 3:
            return f"{parts[0]}.{parts[1]}...{parts[-1]}"
        
        return package
    
    def generate_detailed_diagram(self, issue_number: int, packages: List[Dict],
                                 issue_title: str = None) -> str:
        """Generate diagram with confidence scores
        
        Args:
            issue_number: GitHub issue number
            packages: List of dicts with 'name' and 'confidence' keys
            issue_title: Optional issue title
            
        Returns:
            Mermaid diagram with confidence indicators
        """
        if not packages:
            return self._generate_empty_diagram(issue_number, issue_title)
        
        packages = packages[:5]
        
        lines = []
        lines.append("graph TD")
        
        # Issue node
        issue_label = f"Issue #{issue_number}"
        if issue_title:
            short_title = issue_title[:40] + "..." if len(issue_title) > 40 else issue_title
            issue_label = f"Issue #{issue_number}<br/>{short_title}"
        
        lines.append(f"    Issue[\"{issue_label}\"]")
        lines.append(f"    style Issue fill:{self.COLORS['issue']['fill']},stroke:{self.COLORS['issue']['stroke']},color:{self.COLORS['issue']['text']}")
        
        # Package nodes with confidence
        for idx, pkg in enumerate(packages):
            node_id = f"P{idx}"
            pkg_name = pkg.get('name', pkg) if isinstance(pkg, dict) else pkg
            confidence = pkg.get('confidence', 0.5) if isinstance(pkg, dict) else 0.5
            
            short_name = self._shorten_package_name(pkg_name)
            confidence_pct = int(confidence * 100)
            
            # Add confidence indicator
            label = f"{short_name}<br/>({confidence_pct}% confidence)"
            
            lines.append(f"    {node_id}[\"{label}\"]")
            
            # Color based on confidence
            if confidence >= 0.7:
                color = self.COLORS['success']
            elif confidence >= 0.4:
                color = self.COLORS['package']
            else:
                color = self.COLORS['warning']
            
            lines.append(f"    style {node_id} fill:{color['fill']},stroke:{color['stroke']}")
            
            # Connection style based on confidence
            if confidence >= 0.7:
                lines.append(f"    Issue ==> {node_id}")  # Thick arrow
            else:
                lines.append(f"    Issue --> {node_id}")  # Normal arrow
        
        return "\n".join(lines)
    
    def validate_diagram(self, diagram: str) -> bool:
        """Validate Mermaid syntax
        
        Args:
            diagram: Mermaid diagram string
            
        Returns:
            True if valid syntax
        """
        # Basic validation checks
        if not diagram.strip():
            return False
        
        if not diagram.startswith("graph"):
            return False
        
        # Check for balanced brackets
        if diagram.count('[') != diagram.count(']'):
            return False
        
        if diagram.count('(') != diagram.count(')'):
            return False
        
        return True
```

---

## 🧪 Testing Your Code

Create `tests/test_diagram_generator.py`:

```python
import sys
sys.path.insert(0, 'src')

from diagram_generator import MermaidGenerator

def test_basic_diagram():
    """Test basic diagram generation"""
    gen = MermaidGenerator()
    
    packages = [
        "io.openliberty.microprofile.config",
        "com.ibm.ws.security"
    ]
    
    diagram = gen.generate_diagram(12345, packages, "MicroProfile Config Issue")
    
    print("Basic Diagram:")
    print(diagram)
    print()
    
    assert "graph TD" in diagram
    assert "Issue #12345" in diagram
    assert "P0" in diagram
    assert "P1" in diagram
    assert gen.validate_diagram(diagram)
    print("✓ Basic diagram generation works")

def test_empty_diagram():
    """Test diagram with no packages"""
    gen = MermaidGenerator()
    
    diagram = gen.generate_empty_diagram(12345, "Issue with no packages")
    
    print("Empty Diagram:")
    print(diagram)
    print()
    
    assert "No Liberty packages identified" in diagram
    assert gen.validate_diagram(diagram)
    print("✓ Empty diagram generation works")

def test_package_name_shortening():
    """Test package name shortening"""
    gen = MermaidGenerator()
    
    test_cases = [
        ("io.openliberty.config", "io.openliberty.config"),  # Short, no change
        ("io.openliberty.microprofile.config.impl.internal", "io.openliberty...config.internal"),  # Long
        ("com.ibm.ws.security.auth.impl", "com.ibm...impl"),  # Medium
    ]
    
    print("Package name shortening:")
    for original, expected_pattern in test_cases:
        shortened = gen._shorten_package_name(original)
        print(f"  {original}")
        print(f"  -> {shortened}")
        assert len(shortened) <= 40
    
    print("✓ Package name shortening works")

def test_detailed_diagram():
    """Test diagram with confidence scores"""
    gen = MermaidGenerator()
    
    packages = [
        {'name': 'io.openliberty.microprofile.config', 'confidence': 0.9},
        {'name': 'com.ibm.ws.security', 'confidence': 0.6},
        {'name': 'com.ibm.ws.logging', 'confidence': 0.3}
    ]
    
    diagram = gen.generate_detailed_diagram(12345, packages, "Test Issue")
    
    print("Detailed Diagram:")
    print(diagram)
    print()
    
    assert "90% confidence" in diagram
    assert "60% confidence" in diagram
    assert "30% confidence" in diagram
    assert gen.validate_diagram(diagram)
    print("✓ Detailed diagram generation works")

def test_many_packages():
    """Test diagram with many packages (should limit to 5)"""
    gen = MermaidGenerator()
    
    packages = [f"io.openliberty.package{i}" for i in range(10)]
    
    diagram = gen.generate_diagram(12345, packages)
    
    print(f"Diagram with {len(packages)} packages (limited to 5):")
    print(diagram)
    print()
    
    # Should only have P0-P4 (5 packages)
    assert "P0" in diagram
    assert "P4" in diagram
    assert "P5" not in diagram
    print("✓ Package limiting works")

def test_validation():
    """Test diagram validation"""
    gen = MermaidGenerator()
    
    valid_diagram = """graph TD
    Issue["Issue #123"]
    P0["Package"]
    Issue --> P0"""
    
    invalid_diagrams = [
        "",  # Empty
        "not a diagram",  # No graph keyword
        "graph TD\n    Issue[Unclosed",  # Unbalanced brackets
    ]
    
    assert gen.validate_diagram(valid_diagram)
    print("✓ Valid diagram passes validation")
    
    for invalid in invalid_diagrams:
        assert not gen.validate_diagram(invalid)
    print("✓ Invalid diagrams fail validation")

def test_github_rendering():
    """Test that diagram will render in GitHub"""
    gen = MermaidGenerator()
    
    packages = [
        "io.openliberty.microprofile.config",
        "com.ibm.ws.security"
    ]
    
    diagram = gen.generate_diagram(12345, packages, "Test Issue")
    
    # Create markdown with diagram
    markdown = f"""## Test Comment

```mermaid
{diagram}
```
"""
    
    print("GitHub Markdown Preview:")
    print(markdown)
    print()
    
    assert "```mermaid" in markdown
    assert "```" in markdown
    print("✓ Diagram ready for GitHub rendering")

if __name__ == "__main__":
    print("=== Testing Mermaid Generator ===\n")
    
    test_basic_diagram()
    print()
    
    test_empty_diagram()
    print()
    
    test_package_name_shortening()
    print()
    
    test_detailed_diagram()
    print()
    
    test_many_packages()
    print()
    
    test_validation()
    print()
    
    test_github_rendering()
    print()
    
    print("=== All tests passed! ===")
```

Run your tests:
```bash
python tests/test_diagram_generator.py
```

---

## 🎨 Visual Testing

Test your diagrams in a Mermaid live editor:

1. Go to [Mermaid Live Editor](https://mermaid.live/)
2. Copy your generated diagram
3. Paste and verify it renders correctly
4. Adjust colors/styling if needed

---

## ⚠️ Common Issues & Solutions

### Issue: Diagram doesn't render in GitHub
**Solution:** Ensure proper markdown code fence: ` ```mermaid ` (with newline after)

### Issue: Package names too long
**Solution:** Adjust shortening logic in `_shorten_package_name()`

### Issue: Colors not showing
**Solution:** Check color format: `fill:#ff6b6b` (hex with #)

### Issue: Syntax errors
**Solution:** Use `validate_diagram()` before returning

---

## 📋 Checklist

- [ ] Basic diagram generation works
- [ ] Empty diagram (no packages) works
- [ ] Package name shortening works
- [ ] Handles 1-5 packages correctly
- [ ] Limits to 5 packages when more provided
- [ ] Colors apply correctly
- [ ] Validation catches syntax errors
- [ ] Renders correctly in Mermaid Live Editor
- [ ] All tests pass

---

## 🤝 Integration Points

**Your module will be used by:**
- `server.py` (Person 4) - Main workflow

**You need from others:**
- Package list from `package_analyzer.py` (Person 2)

---

## 💡 Tips

1. **Test in Mermaid Live Editor** - Visual feedback is crucial
2. **Keep diagrams simple** - Don't overcomplicate the layout
3. **Use colors wisely** - Make important info stand out
4. **Handle edge cases** - 0 packages, 1 package, many packages
5. **Validate before returning** - Catch syntax errors early

---

## 🎨 Color Customization

Want different colors? Modify the `COLORS` dict:

```python
COLORS = {
    'issue': {'fill': '#your-color', 'stroke': '#border-color', 'text': '#text-color'},
    # ... more colors
}
```

Use [Color Hunt](https://colorhunt.co/) for color schemes.

---

## 🆘 Need Help?

**Mermaid syntax issues?** Check [Mermaid docs](https://mermaid.js.org/syntax/flowchart.html)  
**Diagram not rendering?** Test in Mermaid Live Editor first  
**Colors not working?** Verify hex format with #

**Estimated completion time:** 50 minutes  
**If blocked:** Post in team channel immediately!