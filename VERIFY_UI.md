# Verify Flask Web UI Still Works

This guide verifies that the Flask web UI continues to work after adding MCP integration.

## Quick Verification

### Step 1: Start the Web UI

**Windows:**
```bash
start_web_ui.bat
```

**Linux/Mac:**
```bash
./start_web_ui.sh
```

### Step 2: Open Browser

Navigate to: **http://localhost:5000**

You should see the GitHub Issue Analyzer web interface.

### Step 3: Test Analysis

1. Enter a GitHub issue URL (e.g., `https://github.com/OpenLiberty/open-liberty/issues/12345`)
2. Optionally enter your GitHub token
3. Click "Analyze Issue"
4. Verify you see:
   - ✅ Package list with confidence scores
   - ✅ Component diagram (Mermaid)
   - ✅ Analysis time

### Step 4: Verify No Errors

Check the terminal where you started the server:
- ✅ No error messages
- ✅ Server responds to requests
- ✅ Analysis completes successfully

## What We're Verifying

The MCP integration (`src/main/python/mcp_server.py`) **wraps** the existing production code without modifying it:

```
Flask Web UI (web_app.py)
    ↓
    Uses directly:
    ├── github_issue_analyzer.py  ← UNCHANGED
    ├── diagram_generator.py      ← UNCHANGED
    └── comment_poster.py         ← UNCHANGED

MCP Server (mcp_server.py)
    ↓
    Also uses (via imports):
    ├── github_issue_analyzer.py  ← SAME CODE
    ├── diagram_generator.py      ← SAME CODE
    └── comment_poster.py         ← SAME CODE
```

**Result**: Both Flask UI and MCP tools use the exact same production code!

## Detailed Verification Steps

### 1. Check Dependencies

```bash
cd src/main/python
pip list | grep -E "Flask|requests|mcp"
```

Expected output:
```
Flask           3.0.0
mcp             0.9.0
requests        2.31.0
```

### 2. Test Analyzer Module

```bash
cd src/main/python
python github_issue_analyzer.py https://github.com/OpenLiberty/open-liberty/issues/12345
```

Expected: Package analysis output (same as before MCP integration)

### 3. Test Diagram Generator

```bash
cd src/main/python
python github_issue_analyzer.py --json-only https://github.com/OpenLiberty/open-liberty/issues/12345 > analysis.json
python diagram_generator.py analysis.json
```

Expected: Mermaid diagram output (same as before MCP integration)

### 4. Test Web UI Endpoints

**Start server:**
```bash
cd src/main/python
python web_app.py
```

**Test API (in another terminal):**
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"issue_url": "https://github.com/OpenLiberty/open-liberty/issues/12345"}'
```

Expected: JSON response with packages and analysis

### 5. Test MCP Server (Separate Process)

**In a new terminal:**
```bash
cd src/main/python
python mcp_server.py
```

Expected output:
```
Starting GitHub Issue Analyzer MCP Server...
Tools available:
  - analyze-github-issue
  - generate-component-diagram
  - post-analysis-comment
  - full-pipeline
Ready!
```

**Important**: MCP server and Flask UI can run **simultaneously** because they use the same underlying code modules.

## Verification Checklist

- [ ] Flask UI starts without errors
- [ ] Can access http://localhost:5000
- [ ] Can analyze an issue via web UI
- [ ] Package list displays correctly
- [ ] Diagram renders correctly
- [ ] No import errors in terminal
- [ ] MCP server can start separately
- [ ] Both can run at the same time

## Troubleshooting

### Issue: Import Error in MCP Server

**Error:**
```
ModuleNotFoundError: No module named 'github_issue_analyzer'
```

**Solution:**
```bash
cd src/main/python
python mcp_server.py
```

MCP server must be run from `src/main/python` directory to import production modules.

### Issue: Flask UI Not Starting

**Error:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Both Use Same Port

MCP server uses **stdio** (standard input/output), not HTTP ports.
Flask UI uses **port 5000**.

They **do not conflict** and can run simultaneously!

## Success Criteria

✅ **Flask UI works exactly as before**
✅ **No changes to production code**
✅ **MCP server provides same functionality via tools**
✅ **Both can run simultaneously**
✅ **No code duplication**

## Conclusion

The MCP integration is a **wrapper layer** that:
- ✅ Adds Bob integration without modifying production code
- ✅ Keeps Flask UI fully functional
- ✅ Reuses all existing logic
- ✅ Provides flexible tool-based access for Bob

**Result**: Best of both worlds! 🎉