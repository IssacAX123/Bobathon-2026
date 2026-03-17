# 🚀 Liberty Issue Analyzer - 3-Hour Implementation Guide

**Team Size:** 4 people  
**Time Budget:** 3 hours  
**Tech Stack:** Python MCP + gh CLI  
**Goal:** Demo-ready GitHub issue analyzer with automated commenting

---

## 📋 Quick Start (5 minutes - Everyone)

```bash
# 1. Clone and setup
git clone <your-repo-url>
cd liberty-analyzer

# 2. Install dependencies
pip install mcp anthropic-mcp

# 3. Verify gh CLI
gh auth status

# 4. Create project structure
mkdir -p src tests docs
touch src/{__init__.py,server.py,github_client.py,package_analyzer.py,diagram_generator.py}
touch tests/test_integration.py
touch docs/DEMO.md
```

---

## 👥 Team Assignments

### Person 1: GitHub Integration Lead
**Files:** `src/github_client.py`  
**Time:** Hour 1-2 (implementation), Hour 3 (testing)  
**Tasks:**
- Implement `fetch_issue()` using gh CLI
- Implement `post_comment()` 
- Implement `add_label()`
- Error handling for API failures

### Person 2: Analysis Engine Lead
**Files:** `src/package_analyzer.py`  
**Time:** Hour 1-2 (implementation), Hour 3 (polish)  
**Tasks:**
- Regex patterns for Liberty packages
- Confidence scoring algorithm
- Context extraction
- Top-N package selection

### Person 3: Visualization Lead
**Files:** `src/diagram_generator.py`  
**Time:** Hour 1-2 (implementation), Hour 3 (refinement)  
**Tasks:**
- Mermaid diagram templates
- Package name shortening
- Styling and colors
- Empty state handling

### Person 4: MCP & Demo Lead
**Files:** `src/server.py`, `docs/DEMO.md`  
**Time:** Hour 1 (scaffold), Hour 2-3 (integration + demo)  
**Tasks:**
- MCP server setup
- Tool registration
- Workflow orchestration
- Demo script preparation

---

## ⏱️ Hour-by-Hour Timeline

### Hour 1: Core Components (Parallel Work)

**0:00-0:50** - Everyone implements their assigned module  
**0:50-1:00** - Quick sync: "Does your module work standalone?"

### Hour 2: Integration

**1:00-1:30** - Person 4 integrates all modules in `server.py`  
**1:30-2:00** - Everyone: Integration testing with real issues

### Hour 3: Demo Prep

**2:00-2:10** - Code cleanup and documentation  
**2:10-2:40** - Demo rehearsal (2 runs)  
**2:40-3:00** - Backup materials (screenshots, video)

---

## 📁 File Structure

```
liberty-analyzer/
├── src/
│   ├── __init__.py
│   ├── server.py              # Person 4 - MCP server
│   ├── github_client.py       # Person 1 - gh CLI wrapper
│   ├── package_analyzer.py    # Person 2 - Package extraction
│   └── diagram_generator.py   # Person 3 - Mermaid generation
├── tests/
│   └── test_integration.py    # Everyone - Integration tests
├── docs/
│   └── DEMO.md               # Person 4 - Demo script
├── README.md                 # Project overview
└── requirements.txt          # Dependencies
```

---

## 🔧 Implementation Details

See individual files for complete code:
- [Person 1: GitHub Client](./PERSON1_GITHUB.md)
- [Person 2: Package Analyzer](./PERSON2_ANALYZER.md)
- [Person 3: Diagram Generator](./PERSON3_DIAGRAM.md)
- [Person 4: MCP Server](./PERSON4_SERVER.md)

---

## ✅ Testing Checklist

Use these real OpenLiberty issues for testing:

```python
TEST_ISSUES = [
    "OpenLiberty/open-liberty#28000",  # MicroProfile issue
    "OpenLiberty/open-liberty#27500",  # Security feature
    "OpenLiberty/open-liberty#27000",  # Config issue
]
```

**Test each:**
- [ ] Issue fetches successfully
- [ ] Packages are identified
- [ ] Diagram generates correctly
- [ ] Comment posts to GitHub
- [ ] Label is added
- [ ] Completes in <15 seconds

---

## 🎬 Demo Flow (5 minutes)

1. **Setup** (30 sec): Show GitHub issue in browser
2. **Execute** (30 sec): Run MCP tool command
3. **Progress** (1 min): Show real-time progress messages
4. **Result** (2 min): Navigate to GitHub, show formatted comment
5. **Wow** (1 min): Highlight automated features

---

## 🚨 Emergency Backup Plan

If live demo fails:
1. Show pre-recorded video (prepare in Hour 3)
2. Walk through screenshots
3. Explain architecture with diagram

**Prepare these in Hour 3:**
- [ ] 1-minute demo video
- [ ] 5 screenshots of successful run
- [ ] Architecture diagram slide

---

## 📞 Communication Protocol

**Slack/Discord Channel:** #liberty-analyzer  
**Check-ins:**
- 0:50 - "Module complete?" status
- 1:30 - "Integration working?" status
- 2:10 - "Demo ready?" status

**Blockers:** Post immediately in channel with `@team` mention

---

## 🎯 Success Criteria

- [ ] Tool executes end-to-end without errors
- [ ] Identifies packages with >80% accuracy
- [ ] Diagram renders in GitHub
- [ ] Comment formatting looks professional
- [ ] Demo runs smoothly (2 successful rehearsals)
- [ ] Backup materials ready

---

## 📦 Dependencies

```txt
# requirements.txt
mcp>=0.9.0
anthropic-mcp>=0.1.0
```

**System Requirements:**
- Python 3.9+
- gh CLI (authenticated)
- Git

---

## 🔗 Quick Links

- [MCP Documentation](https://modelcontextprotocol.io/docs)
- [gh CLI Reference](https://cli.github.com/manual/)
- [Mermaid Syntax](https://mermaid.js.org/syntax/flowchart.html)
- [OpenLiberty Issues](https://github.com/OpenLiberty/open-liberty/issues)

---

## 💡 Tips for Success

1. **Test early, test often** - Don't wait until Hour 3
2. **Use real issues** - Test with actual OpenLiberty issues
3. **Keep it simple** - MVP first, polish later
4. **Communicate blockers** - Don't struggle alone
5. **Prepare backups** - Screenshots save demos

---

**Last Updated:** 2026-03-17  
**Version:** 1.0  
**Contact:** Team lead for questions