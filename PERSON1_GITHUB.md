# Person 1: GitHub Integration Implementation

**Your Mission:** Build the GitHub CLI wrapper that fetches issues and posts comments.

**Time Budget:** 50 minutes implementation + 10 minutes testing

---

## 📝 Your File: `src/github_client.py`

```python
import subprocess
import json
from typing import Dict, Optional

class GitHubClient:
    """Wrapper for gh CLI operations"""
    
    def fetch_issue(self, issue_url: str) -> Dict:
        """Fetch issue details using gh CLI
        
        Args:
            issue_url: Full GitHub issue URL or owner/repo#number
            
        Returns:
            Dict with title, body, number, labels, url
            
        Raises:
            Exception: If gh CLI fails or issue not found
        """
        try:
            cmd = [
                "gh", "issue", "view", issue_url,
                "--json", "title,body,number,labels,url"
            ]
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=True,
                timeout=10
            )
            return json.loads(result.stdout)
        except subprocess.TimeoutExpired:
            raise Exception(f"Timeout fetching issue: {issue_url}")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to fetch issue: {e.stderr}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {e}")
    
    def post_comment(self, issue_url: str, comment: str) -> bool:
        """Post comment to GitHub issue
        
        Args:
            issue_url: Full GitHub issue URL or owner/repo#number
            comment: Markdown-formatted comment text
            
        Returns:
            True if successful
            
        Raises:
            Exception: If posting fails
        """
        try:
            cmd = ["gh", "issue", "comment", issue_url, "--body", comment]
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=True,
                timeout=10
            )
            return True
        except subprocess.TimeoutExpired:
            raise Exception(f"Timeout posting comment to: {issue_url}")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to post comment: {e.stderr}")
    
    def add_label(self, issue_url: str, label: str) -> bool:
        """Add label to issue
        
        Args:
            issue_url: Full GitHub issue URL or owner/repo#number
            label: Label name to add
            
        Returns:
            True if successful, False if label already exists or permission denied
        """
        try:
            cmd = ["gh", "issue", "edit", issue_url, "--add-label", label]
            subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=True,
                timeout=10
            )
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            # Non-critical operation, don't crash
            return False
    
    def validate_issue_url(self, issue_url: str) -> bool:
        """Validate issue URL format
        
        Args:
            issue_url: Issue URL to validate
            
        Returns:
            True if valid format
        """
        # Accept formats: owner/repo#123 or full URL
        import re
        patterns = [
            r'^[\w-]+/[\w-]+#\d+$',  # owner/repo#123
            r'^https://github\.com/[\w-]+/[\w-]+/issues/\d+$'  # Full URL
        ]
        return any(re.match(pattern, issue_url) for pattern in patterns)
```

---

## 🧪 Testing Your Code

Create `tests/test_github_client.py`:

```python
import sys
sys.path.insert(0, 'src')

from github_client import GitHubClient

def test_fetch_issue():
    """Test fetching a real OpenLiberty issue"""
    client = GitHubClient()
    
    # Use a known issue
    issue_url = "OpenLiberty/open-liberty#28000"
    
    print(f"Testing fetch_issue with {issue_url}...")
    issue = client.fetch_issue(issue_url)
    
    assert 'title' in issue
    assert 'body' in issue
    assert 'number' in issue
    assert issue['number'] == 28000
    
    print(f"✓ Fetched: {issue['title'][:50]}...")
    print(f"✓ Body length: {len(issue['body'])} chars")
    return issue

def test_validate_url():
    """Test URL validation"""
    client = GitHubClient()
    
    valid_urls = [
        "OpenLiberty/open-liberty#28000",
        "https://github.com/OpenLiberty/open-liberty/issues/28000"
    ]
    
    invalid_urls = [
        "not-a-url",
        "github.com/repo",
        "#123"
    ]
    
    for url in valid_urls:
        assert client.validate_issue_url(url), f"Should be valid: {url}"
        print(f"✓ Valid: {url}")
    
    for url in invalid_urls:
        assert not client.validate_issue_url(url), f"Should be invalid: {url}"
        print(f"✓ Invalid: {url}")

def test_error_handling():
    """Test error handling"""
    client = GitHubClient()
    
    # Test with non-existent issue
    try:
        client.fetch_issue("OpenLiberty/open-liberty#999999999")
        assert False, "Should have raised exception"
    except Exception as e:
        print(f"✓ Caught error: {str(e)[:50]}...")

if __name__ == "__main__":
    print("=== Testing GitHub Client ===\n")
    
    # Test 1: Fetch issue
    issue = test_fetch_issue()
    print()
    
    # Test 2: Validate URLs
    test_validate_url()
    print()
    
    # Test 3: Error handling
    test_error_handling()
    print()
    
    print("=== All tests passed! ===")
```

Run your tests:
```bash
python tests/test_github_client.py
```

---

## ⚠️ Common Issues & Solutions

### Issue: "gh: command not found"
**Solution:** Install gh CLI: `brew install gh` (macOS) or see [gh installation](https://cli.github.com/)

### Issue: "authentication required"
**Solution:** Run `gh auth login` and follow prompts

### Issue: "rate limit exceeded"
**Solution:** Authenticated requests have 5000/hour limit. Check with `gh api rate_limit`

### Issue: "permission denied" when posting comment
**Solution:** Verify you have write access to the repository

---

## 📋 Checklist

- [ ] `fetch_issue()` works with real OpenLiberty issue
- [ ] `post_comment()` successfully posts (test on your own repo first!)
- [ ] `add_label()` handles errors gracefully
- [ ] `validate_issue_url()` accepts both formats
- [ ] All error cases have clear error messages
- [ ] Timeouts are set (10 seconds)
- [ ] Tests pass successfully

---

## 🤝 Integration Points

**Your module will be used by:**
- `server.py` (Person 4) - Main workflow orchestration

**You need from others:**
- Nothing! Your module is independent.

---

## 💡 Tips

1. **Test with real issues** - Use actual OpenLiberty issues, not fake data
2. **Handle errors gracefully** - Don't crash on network issues
3. **Add timeouts** - Prevent hanging on slow connections
4. **Validate inputs** - Check URL format before calling gh CLI
5. **Keep it simple** - Don't over-engineer, MVP first

---

## 🆘 Need Help?

**Stuck on gh CLI?** Check: `gh issue view --help`  
**JSON parsing issues?** Print `result.stdout` to debug  
**Permission errors?** Test on your own repo first

**Estimated completion time:** 50 minutes  
**If blocked:** Post in team channel immediately!