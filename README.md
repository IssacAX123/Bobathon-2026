# GitHub Issue Analyzer for OpenLiberty

**Bobathon 2026 Project** - Automated GitHub issue analysis with MCP integration for Bob IDE

Automatically fetch GitHub issues, identify Liberty packages, generate visual diagrams, and post comprehensive analysis comments.

---

## 🚀 Quick Start

### For Bob IDE (MCP Integration)

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Bob**
   - See [BOB_MCP_SETUP.md](./BOB_MCP_SETUP.md) for complete setup

3. **Restart Bob**
   - Close Bob completely
   - Reopen Bob
   - Tools will be available

4. **Use with Bob**
   ```
   Ask Bob: "Analyze this issue: https://github.com/OpenLiberty/open-liberty/issues/12345"
   ```

### For Flask Web UI

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Web Server**
   ```bash
   # Windows
   start_web_ui.bat
   
   # Linux/Mac
   ./start_web_ui.sh
   ```

3. **Open Browser**
   - Navigate to http://localhost:5000
   - Enter issue URL and analyze

---

## 📁 Project Structure

```
Bobathon-2026/
├── src/main/python/
│   ├── mcp_server.py              # MCP server for Bob (5 granular tools)
│   ├── github_issue_analyzer.py   # Issue fetching & package analysis
│   ├── diagram_generator.py       # Mermaid diagram generation
│   ├── comment_poster.py          # GitHub comment posting
│   ├── web_app.py                 # Flask web UI
│   └── templates/
│       └── index.html             # Web UI template
├── docs/                          # Documentation
├── BOB_MCP_SETUP.md              # Bob configuration guide
├── MCP_INTEGRATION.md            # MCP architecture docs
├── MCP_USAGE_EXAMPLES.md         # Usage examples for Bob
├── VERIFY_UI.md                  # Flask UI verification
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🎯 Features

### MCP Tools for Bob (Step-by-Step Workflow)

Bob has access to 5 granular tools:

1. **fetch-github-issue** - Get issue details (title, body, labels)
2. **identify-liberty-packages** - Find Liberty packages in text
3. **generate-component-diagram** - Create Mermaid diagram
4. **format-analysis-comment** - Format comprehensive comment
5. **post-github-comment** - Post to GitHub (dry-run by default)

### Flask Web UI

- Visual interface for issue analysis
- Real-time package identification
- Interactive diagram display
- One-click analysis

### Production Pipeline

- GitHub API integration via `requests`
- YAML-based keyword mapping
- Confidence scoring
- Mermaid diagram generation
- Comprehensive GitHub comments with:
  - Package analysis
  - Component diagrams
  - Technical deep-dives
  - Code suggestions
  - Test recommendations

---

## 📚 Documentation

### Setup & Configuration
- **[BOB_MCP_SETUP.md](./BOB_MCP_SETUP.md)** - Complete Bob setup guide ⭐ START HERE
- **[VERIFY_UI.md](./VERIFY_UI.md)** - Verify Flask UI still works

### Usage & Workflow
- **[MCP_USAGE_EXAMPLES.md](./MCP_USAGE_EXAMPLES.md)** - How Bob uses the tools
- **[MCP_INTEGRATION.md](./MCP_INTEGRATION.md)** - Architecture details

### Original Hackathon Docs
- [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md) - Original plan
- [QUICK_START.md](./QUICK_START.md) - Quick start guide
- [QUICK_START_WEB_UI.md](./QUICK_START_WEB_UI.md) - Web UI guide

---

## 🔧 Tech Stack

- **Language:** Python 3.9+
- **MCP:** Model Context Protocol SDK
- **Web Framework:** Flask 3.0+
- **GitHub API:** requests library
- **Diagrams:** Mermaid
- **Config:** YAML (pyyaml)

---

## 💻 Usage Examples

### With Bob (Recommended)

```
User: "Analyze this issue: https://github.com/OpenLiberty/open-liberty/issues/12345"

Bob: [Uses fetch-github-issue]
Bob: "I fetched issue #12345 about LTPA token validation.
      Let me identify the Liberty packages..."

Bob: [Uses identify-liberty-packages]
Bob: "Found 3 packages:
      - io.openliberty.security.ltpa (95%)
      - com.ibm.ws.crypto.ltpakeyutil (90%)
      - io.openliberty.security.utility (85%)
      
      Want a diagram?"

User: "Yes"

Bob: [Uses generate-component-diagram]
Bob: "Here's the diagram showing relationships:
      [mermaid code]
      
      Should I post this to GitHub?"

User: "Preview first"

Bob: [Uses format-analysis-comment]
Bob: "Here's what would be posted:
      [shows preview]
      
      Ready to post?"

User: "Yes"

Bob: [Uses post-github-comment with dry_run=true]
Bob: "Dry run successful. Post for real?"

User: "Yes"

Bob: [Uses post-github-comment with dry_run=false]
Bob: "✅ Posted! https://github.com/.../issues/12345#comment-456"
```

### With Flask UI

1. Open http://localhost:5000
2. Enter issue URL
3. Click "Analyze Issue"
4. View results with diagram
5. Optionally post to GitHub

---

## 🧪 Testing

### Test MCP Server

```bash
cd src/main/python
python mcp_server.py
```

Should output:
```
Starting GitHub Issue Analyzer MCP Server...
Tools available (step-by-step workflow):
  1. fetch-github-issue
  2. identify-liberty-packages
  3. generate-component-diagram
  4. format-analysis-comment
  5. post-github-comment
Ready!
```

### Test Flask UI

```bash
start_web_ui.bat  # Windows
./start_web_ui.sh # Linux/Mac
```

Open http://localhost:5000 and test with a real issue.

### Test Production Modules

```bash
cd src/main/python

# Test analyzer
python github_issue_analyzer.py https://github.com/OpenLiberty/open-liberty/issues/12345

# Test diagram generator
python github_issue_analyzer.py --json-only https://github.com/OpenLiberty/open-liberty/issues/12345 > analysis.json
python diagram_generator.py analysis.json

# Test comment poster (dry-run)
python comment_poster.py --dry-run https://github.com/OpenLiberty/open-liberty/issues/12345 analysis.json diagram.md
```

---

## 🚨 Troubleshooting

### "ModuleNotFoundError: No module named 'yaml'"

```bash
pip install -r requirements.txt
```

### "MCP error -32000: Connection closed"

1. Install dependencies: `pip install -r requirements.txt`
2. Restart Bob completely
3. Check Bob's MCP settings for errors

### Flask UI won't start

```bash
pip install Flask requests pyyaml
```

### Bob doesn't see tools

1. Verify Bob config at `C:/Users/[username]/.bob/settings/mcp_settings.json`
2. Check file paths are correct
3. Restart Bob completely
4. Check Bob's error logs

See [BOB_MCP_SETUP.md](./BOB_MCP_SETUP.md) for detailed troubleshooting.

---

## 📈 Architecture

### MCP Integration (Bob)

```
Bob IDE
  ↓ (uses MCP tools)
MCP Server (mcp_server.py)
  ↓ (imports)
Production Modules
  ├─ github_issue_analyzer.py
  ├─ diagram_generator.py
  └─ comment_poster.py
```

### Flask UI

```
Browser
  ↓ (HTTP)
Flask App (web_app.py)
  ↓ (imports)
Production Modules
  ├─ github_issue_analyzer.py
  ├─ diagram_generator.py
  └─ comment_poster.py
```

**Key Point**: Both Bob and Flask UI use the **same production code**!

---

## 🎯 Success Metrics

- ✅ **Bob Integration**: 5 granular tools for step-by-step workflow
- ✅ **Flask UI**: Web interface for visual analysis
- ✅ **No Code Duplication**: Both use same production modules
- ✅ **Comprehensive Comments**: Detailed technical analysis
- ✅ **Safety**: Dry-run by default before posting
- ✅ **Documentation**: Complete setup and usage guides

---

## 👥 Team

- **Dave** - GitHub Integration
- **Deval** - Package Analysis  
- **Hannah** - Visualization
- **Issac** - MCP Server & Integration

---

## 📝 License

Bobathon 2026 Hackathon Project

---

## 🆘 Need Help?

1. **Setup Issues**: See [BOB_MCP_SETUP.md](./BOB_MCP_SETUP.md)
2. **Usage Questions**: See [MCP_USAGE_EXAMPLES.md](./MCP_USAGE_EXAMPLES.md)
3. **Architecture**: See [MCP_INTEGRATION.md](./MCP_INTEGRATION.md)
4. **UI Issues**: See [VERIFY_UI.md](./VERIFY_UI.md)

---

**Built for Bobathon 2026** 🤖

**Key Features:**
- 🔧 MCP integration for Bob IDE
- 🌐 Flask web UI
- 📊 Mermaid diagrams
- 📝 Comprehensive analysis
- 🔒 Safe (dry-run by default)
