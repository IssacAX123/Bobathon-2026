# Person 2: Package Analyzer Implementation

**Your Mission:** Extract Liberty package names from issue text and score their relevance.

**Time Budget:** 50 minutes implementation + 10 minutes testing

---

## 📝 Your File: `src/package_analyzer.py`

```python
import re
from typing import List, Dict, Set
from dataclasses import dataclass

@dataclass
class Package:
    """Represents an identified Liberty package"""
    name: str
    confidence: float  # 0.0 to 1.0
    context: str       # Surrounding text
    occurrences: int   # Number of times mentioned

class PackageAnalyzer:
    """Extract and analyze Liberty packages from issue text"""
    
    # Liberty package patterns
    LIBERTY_PATTERNS = [
        r'io\.openliberty\.[a-zA-Z0-9._-]+',
        r'com\.ibm\.ws\.[a-zA-Z0-9._-]+',
        r'com\.ibm\.websphere\.[a-zA-Z0-9._-]+'
    ]
    
    # Context keywords that boost confidence
    CONFIDENCE_KEYWORDS = {
        'high': ['feature', 'bundle', 'component', 'package', 'module', 'artifact'],
        'medium': ['config', 'configuration', 'dependency', 'import', 'export'],
        'low': ['error', 'exception', 'issue', 'problem']
    }
    
    def extract_packages(self, text: str) -> List[Package]:
        """Extract Liberty package names from text
        
        Args:
            text: Issue title + body combined
            
        Returns:
            List of Package objects sorted by confidence (highest first)
        """
        if not text:
            return []
        
        packages = {}
        
        # Search for each pattern
        for pattern in self.LIBERTY_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                pkg_name = match.group(0)
                
                # Normalize package name (lowercase)
                pkg_name = pkg_name.lower()
                
                # Get context around the match
                context = self._get_context(text, match.start(), match.end())
                
                if pkg_name in packages:
                    # Increment occurrence count
                    packages[pkg_name].occurrences += 1
                    # Update confidence if this context is better
                    new_confidence = self._calculate_confidence(pkg_name, context)
                    if new_confidence > packages[pkg_name].confidence:
                        packages[pkg_name].confidence = new_confidence
                        packages[pkg_name].context = context
                else:
                    # New package found
                    packages[pkg_name] = Package(
                        name=pkg_name,
                        confidence=self._calculate_confidence(pkg_name, context),
                        context=context,
                        occurrences=1
                    )
        
        # Sort by confidence (highest first), then by occurrences
        sorted_packages = sorted(
            packages.values(),
            key=lambda p: (p.confidence, p.occurrences),
            reverse=True
        )
        
        return sorted_packages
    
    def _get_context(self, text: str, start: int, end: int, window: int = 60) -> str:
        """Extract surrounding context for a match
        
        Args:
            text: Full text
            start: Match start position
            end: Match end position
            window: Characters to include on each side
            
        Returns:
            Context string with the match highlighted
        """
        context_start = max(0, start - window)
        context_end = min(len(text), end + window)
        
        context = text[context_start:context_end].strip()
        
        # Clean up whitespace
        context = ' '.join(context.split())
        
        return context
    
    def _calculate_confidence(self, package: str, context: str) -> float:
        """Calculate confidence score (0.0-1.0) based on context
        
        Args:
            package: Package name
            context: Surrounding text
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        score = 0.5  # Base score
        context_lower = context.lower()
        
        # Boost if in code block (markdown)
        if '`' in context or '```' in context:
            score += 0.3
        
        # Boost based on keywords
        for keyword in self.CONFIDENCE_KEYWORDS['high']:
            if keyword in context_lower:
                score += 0.15
                break
        
        for keyword in self.CONFIDENCE_KEYWORDS['medium']:
            if keyword in context_lower:
                score += 0.10
                break
        
        for keyword in self.CONFIDENCE_KEYWORDS['low']:
            if keyword in context_lower:
                score += 0.05
                break
        
        # Boost if package name appears multiple times
        if context_lower.count(package.lower()) > 1:
            score += 0.1
        
        # Cap at 1.0
        return min(1.0, score)
    
    def get_top_packages(self, packages: List[Package], limit: int = 5) -> List[Package]:
        """Return top N packages by confidence
        
        Args:
            packages: List of Package objects
            limit: Maximum number to return
            
        Returns:
            Top N packages
        """
        return packages[:limit]
    
    def get_package_summary(self, packages: List[Package]) -> Dict:
        """Generate summary statistics
        
        Args:
            packages: List of Package objects
            
        Returns:
            Dict with summary stats
        """
        if not packages:
            return {
                'total': 0,
                'high_confidence': 0,
                'medium_confidence': 0,
                'low_confidence': 0
            }
        
        high = sum(1 for p in packages if p.confidence >= 0.7)
        medium = sum(1 for p in packages if 0.4 <= p.confidence < 0.7)
        low = sum(1 for p in packages if p.confidence < 0.4)
        
        return {
            'total': len(packages),
            'high_confidence': high,
            'medium_confidence': medium,
            'low_confidence': low
        }
```

---

## 🧪 Testing Your Code

Create `tests/test_package_analyzer.py`:

```python
import sys
sys.path.insert(0, 'src')

from package_analyzer import PackageAnalyzer

def test_basic_extraction():
    """Test basic package extraction"""
    analyzer = PackageAnalyzer()
    
    text = """
    Issue with io.openliberty.microprofile.config feature.
    The com.ibm.ws.security bundle is also affected.
    """
    
    packages = analyzer.extract_packages(text)
    
    print(f"Found {len(packages)} packages:")
    for pkg in packages:
        print(f"  - {pkg.name} (confidence: {pkg.confidence:.2f})")
    
    assert len(packages) == 2
    assert any('microprofile.config' in p.name for p in packages)
    assert any('security' in p.name for p in packages)
    print("✓ Basic extraction works")

def test_confidence_scoring():
    """Test confidence scoring with different contexts"""
    analyzer = PackageAnalyzer()
    
    # High confidence: in code block with feature keyword
    high_text = "`io.openliberty.microprofile.config` feature is broken"
    high_packages = analyzer.extract_packages(high_text)
    
    # Low confidence: just mentioned
    low_text = "io.openliberty.microprofile.config"
    low_packages = analyzer.extract_packages(low_text)
    
    print(f"High confidence context: {high_packages[0].confidence:.2f}")
    print(f"Low confidence context: {low_packages[0].confidence:.2f}")
    
    assert high_packages[0].confidence > low_packages[0].confidence
    print("✓ Confidence scoring works")

def test_multiple_occurrences():
    """Test handling of repeated package mentions"""
    analyzer = PackageAnalyzer()
    
    text = """
    The io.openliberty.microprofile.config feature has issues.
    When using io.openliberty.microprofile.config, errors occur.
    The io.openliberty.microprofile.config bundle needs fixing.
    """
    
    packages = analyzer.extract_packages(text)
    
    print(f"Package mentioned {packages[0].occurrences} times")
    assert packages[0].occurrences == 3
    print("✓ Multiple occurrences tracked")

def test_real_issue():
    """Test with realistic issue text"""
    analyzer = PackageAnalyzer()
    
    text = """
    # MicroProfile Config Issue
    
    When using the `io.openliberty.microprofile.config-3.0` feature,
    the application fails to start. The error mentions:
    
    ```
    com.ibm.ws.config.ConfigException: Unable to load configuration
    ```
    
    This affects the io.openliberty.microprofile.config component.
    Related to com.ibm.ws.microprofile.config.impl bundle.
    """
    
    packages = analyzer.extract_packages(text)
    top_5 = analyzer.get_top_packages(packages, limit=5)
    
    print(f"\nReal issue analysis:")
    print(f"Total packages found: {len(packages)}")
    print(f"Top 5 packages:")
    for i, pkg in enumerate(top_5, 1):
        print(f"  {i}. {pkg.name}")
        print(f"     Confidence: {pkg.confidence:.2f}")
        print(f"     Occurrences: {pkg.occurrences}")
        print(f"     Context: {pkg.context[:60]}...")
    
    summary = analyzer.get_package_summary(packages)
    print(f"\nSummary: {summary}")
    
    assert len(packages) > 0
    print("✓ Real issue analysis works")

def test_no_packages():
    """Test with text containing no packages"""
    analyzer = PackageAnalyzer()
    
    text = "This is a general issue with no specific packages mentioned."
    packages = analyzer.extract_packages(text)
    
    assert len(packages) == 0
    print("✓ Handles no packages gracefully")

if __name__ == "__main__":
    print("=== Testing Package Analyzer ===\n")
    
    test_basic_extraction()
    print()
    
    test_confidence_scoring()
    print()
    
    test_multiple_occurrences()
    print()
    
    test_no_packages()
    print()
    
    test_real_issue()
    print()
    
    print("=== All tests passed! ===")
```

Run your tests:
```bash
python tests/test_package_analyzer.py
```

---

## ⚠️ Common Issues & Solutions

### Issue: Regex not matching packages
**Solution:** Test patterns individually with `re.findall()` to debug

### Issue: Confidence scores all the same
**Solution:** Check that context extraction is working, print context to debug

### Issue: Duplicate packages with different cases
**Solution:** Normalize to lowercase: `pkg_name.lower()`

### Issue: Context too short/long
**Solution:** Adjust `window` parameter in `_get_context()`

---

## 📋 Checklist

- [ ] Extracts `io.openliberty.*` packages
- [ ] Extracts `com.ibm.ws.*` packages
- [ ] Extracts `com.ibm.websphere.*` packages
- [ ] Confidence scoring works (0.0-1.0 range)
- [ ] Handles multiple occurrences correctly
- [ ] Returns empty list when no packages found
- [ ] Top N selection works
- [ ] All tests pass

---

## 🤝 Integration Points

**Your module will be used by:**
- `server.py` (Person 4) - Main workflow
- `diagram_generator.py` (Person 3) - Needs package list

**You need from others:**
- Nothing! Your module is independent.

---

## 💡 Tips

1. **Test with real Liberty issues** - Copy actual issue text for testing
2. **Print debug info** - Use `print()` to see what's being extracted
3. **Start simple** - Get basic extraction working first, then add confidence scoring
4. **Handle edge cases** - Empty text, no packages, malformed packages
5. **Keep regex simple** - Don't over-complicate patterns

---

## 🆘 Need Help?

**Regex not working?** Test at [regex101.com](https://regex101.com)  
**Confidence scoring confusing?** Start with fixed scores, refine later  
**Context extraction issues?** Print the context to see what you're getting

**Estimated completion time:** 50 minutes  
**If blocked:** Post in team channel immediately!