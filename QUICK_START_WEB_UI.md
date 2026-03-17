# 🚀 Quick Start - Web UI

## Super Fast Setup (2 minutes)

### Option 1: Automated Script (Recommended)

**macOS/Linux:**
```bash
./start_web_ui.sh
```

**Windows:**
```cmd
start_web_ui.bat
```

That's it! The script will:
- ✅ Create a virtual environment
- ✅ Install all dependencies
- ✅ Start the Flask server
- ✅ Open at http://localhost:5000

### Option 2: Manual Setup

**macOS/Linux:**
```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
cd src/main/python
python web_app.py

# 5. Open browser to http://localhost:5000
```

**Windows:**
```cmd
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
venv\Scripts\activate.bat

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
cd src\main\python
python web_app.py

# 5. Open browser to http://localhost:5000
```

## 🎯 First Time Use

1. **Open your browser** to `http://localhost:5000`
2. **Try an example issue** - Click one of the pre-loaded examples
3. **Click "Analyze Issue"** - Watch the magic happen!
4. **View results** - See packages, confidence scores, and diagram

## 🔧 Optional: Set GitHub Token

For higher API rate limits (5000/hour instead of 60/hour):

**macOS/Linux:**
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

**Windows (Command Prompt):**
```cmd
set GITHUB_TOKEN=ghp_your_token_here
```

**Windows (PowerShell):**
```powershell
$env:GITHUB_TOKEN="ghp_your_token_here"
```

Get a token at: https://github.com/settings/tokens

## 🐛 Troubleshooting

### "Command not found: python3"
Install Python 3.9+:
```bash
brew install python3
```

### "Permission denied: ./start_web_ui.sh"
Make it executable:
```bash
chmod +x start_web_ui.sh
```

### "Port 5000 already in use"
Kill the process or change the port in `web_app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Use port 8080
```

### Virtual Environment Issues
If you have issues with the venv:
```bash
# Remove old venv
rm -rf venv

# Create fresh one
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🎉 You're Ready!

The web UI should now be running at **http://localhost:5000**

Enjoy the modern, smooth interface! ✨