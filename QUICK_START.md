# ⚡ QUICK START - Liberty Issue Analyzer

**Time Remaining:** 3 hours | **Team Size:** 4 people

---

## 🎯 Your Role (Find Yourself)

### 👤 Person 1: GitHub Integration
**File:** `src/github_client.py`  
**Guide:** [PERSON1_GITHUB.md](./PERSON1_GITHUB.md)  
**Time:** 50 minutes  
**Task:** Build gh CLI wrapper for fetching issues and posting comments

### 👤 Person 2: Package Analysis
**File:** `src/package_analyzer.py`  
**Guide:** [PERSON2_ANALYZER.md](./PERSON2_ANALYZER.md)  
**Time:** 50 minutes  
**Task:** Extract Liberty packages from issue text with confidence scoring

### 👤 Person 3: Diagram Generation
**File:** `src/diagram_generator.py`  
**Guide:** [PERSON3_DIAGRAM.md](./PERSON3_DIAGRAM.md)  
**Time:** 50 minutes  
**Task:** Generate Mermaid component diagrams

### 👤 Person 4: MCP Server & Demo
**File:** `src/server.py`  
**Guide:** [PERSON4_SERVER.md](./PERSON4_SERVER.md)  
**Time:** 3 hours (scaffold → integrate → demo)  
**Task:** Build MCP server, integrate modules, prepare demo

---

## 🚀 Setup (Everyone - 5 minutes)

```bash
# 1. Navigate to project
cd liberty-analyzer

# 2. Create structure
mkdir -p src tests docs

# 3. Install dependencies
pip install mcp

# 4. Verify gh CLI
gh auth status

# 5. Open your guide
# Person 1: open PERSON1_GITHUB.md
# Person 2: open PERSON2_ANALYZER.md
# Person 3: open PERSON3_DIAGRAM.md
# Person 4: open PERSON4_SERVER.md
```

---

## ⏰ Timeline

| Time | Activity | Who |
|------|----------|-----|
| **0:00-0:50** | Build core modules | Persons 1, 2, 3 |
| **0:50-1:00** | Check-in: "Module done?" | Everyone |
| **1:00-1:30** | Integration | Person 4 (lead) |
| **1:30-2:00** | Testing with real issues | Everyone |
| **2:00-2:10** | Code cleanup | Everyone |
| **2:10-2:40** | Demo rehearsal (2x) | Everyone |
| **2:40-3:00** | Backup materials | Person 4 (lead) |

---

## ✅ Your Checklist

### Person 1 (GitHub Integration)
- [ ] `fetch_issue()` works
- [ ] `post_comment()` works
- [ ] `add_label()` works
- [ ] Error handling complete
- [ ] Tests pass

### Person 2 (Package Analysis)
- [ ] Regex extracts packages
- [ ] Confidence scoring works
- [ ] Handles multiple occurrences
- [ ] Returns top N packages
- [ ] Tests pass

### Person 3 (Diagram Generation)
- [ ] Basic diagram generates
- [ ] Empty state handled
- [ ] Package names shortened
- [ ] Colors applied
- [ ] Validates syntax
- [ ] Tests pass

### Person 4 (MCP Server)
- [ ] Tool registered
- [ ] Workflow orchestrated
- [ ] Error handling complete
- [ ] Integration tests pass
- [ ] Demo script ready
- [ ] Backup materials prepared

---

## 🧪 Test Commands

```bash
# Test your module
python tests/test_github_client.py      # Person 1
python tests/test_package_analyzer.py   # Person 2
python tests/test_diagram_generator.py  # Person 3

# Test integration (Hour 2)
python tests/test_integration.py        # Everyone

# Run MCP server (Hour 3)
python src/server.py                    # Person 4
```

---

## 🆘 Emergency Contacts

**Blocker?** Post immediately:
```
🚨 BLOCKER: [Your name] stuck on [issue]
File: [filename]
Error: [error message]
Need: [what you need]
```

**Check-ins:**
- 0:50 - "Module complete?"
- 1:30 - "Integration working?"
- 2:40 - "Demo ready?"

---

## 📊 Success Criteria

- [ ] Analysis completes in <15 seconds
- [ ] Identifies packages correctly (test with 3 issues)
- [ ] Diagram renders in GitHub
- [ ] Comment looks professional
- [ ] Demo runs smoothly (5 minutes)

---

## 🎬 Demo Preview

**What we'll show:**
1. GitHub issue (complex, multiple packages)
2. Run: `Bob, analyze this issue: OpenLiberty/open-liberty#28000`
3. Show progress messages
4. Navigate to GitHub comment
5. Highlight: packages identified, diagram, automation

**Wow factor:** All automated in <10 seconds!

---

## 💡 Pro Tips

1. **Test early** - Don't wait until Hour 3
2. **Use real issues** - Test with actual OpenLiberty issues
3. **Communicate** - Post updates and blockers immediately
4. **Keep it simple** - MVP first, polish later
5. **Prepare backups** - Screenshots and video save demos

---

## 📁 Key Files

| File | Purpose | Owner |
|------|---------|-------|
| `src/github_client.py` | GitHub API wrapper | Person 1 |
| `src/package_analyzer.py` | Package extraction | Person 2 |
| `src/diagram_generator.py` | M diagram generation | Person 3 |
| `src/server.py` | MCP server | Person 4 |
| `tests/test_integration.py` | End-to-end tests | Person 4 |
| `docs/DEMO.md` | Demo script | Person 4 |

---

## 🔗 Resources

- [MCP Docs](https://modelcontextprotocol.io/docs)
- [gh CLI Manual](https://cli.github.com/manual/)
- [Mermaid Live Editor](https://mermaid.live/)
- [OpenLiberty Issues](https://github.com/OpenLiberty/open-liberty/issues)

---

## 🎯 Final Goal

**Demo this workflow:**
```
User: "Bob, analyze this issue: OpenLiberty/open-liberty#28000"

Bob: 🔍 Fetching issue...
     📦 Analyzing packages...
     📊 Generating diagram...
     💬 Posting analysis...
     ✅ Analysis complete!

[Show formatted GitHub comment with diagram]
```

---

**START NOW! ⏰**

Time is ticking. Read your guide and begin coding immediately.

**You've got this! 🚀**