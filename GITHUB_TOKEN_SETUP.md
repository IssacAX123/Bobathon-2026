# 🔐 GitHub Token Setup Guide

You're getting a **401 error** because you're accessing GitHub Enterprise (github.ibm.com) which requires authentication.

## 🚀 Quick Fix (2 minutes)

### Step 1: Create a GitHub Token

1. Go to your GitHub Enterprise settings:
   ```
   https://github.ibm.com/settings/tokens
   ```

2. Click **"Generate new token"** → **"Generate new token (classic)"**

3. Give it a name: `Issue Analyzer`

4. Select these scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `read:org` (Read org and team membership)

5. Click **"Generate token"**

6. **Copy the token** (starts with `ghp_...`) - you won't see it again!

### Step 2: Set the Token

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

### Step 3: Restart the Web UI

Stop the server (Ctrl+C) and restart:

**macOS/Linux:**
```bash
./start_web_ui.sh
```

**Windows:**
```cmd
start_web_ui.bat
```

### Step 4: Try Again!

Now try your issue again:
```
https://github.ibm.com/David-Webster1/jakarta_security/issues/1
```

It should work! ✅

---

## 🔒 Make It Permanent (Optional)

To avoid setting the token every time:

### macOS/Linux

Add to your `~/.bashrc` or `~/.zshrc`:
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

Then reload:
```bash
source ~/.bashrc  # or ~/.zshrc
```

### Windows

**Command Prompt (Permanent):**
```cmd
setx GITHUB_TOKEN "ghp_your_token_here"
```
(Restart terminal after this)

**PowerShell (Permanent):**
Add to your PowerShell profile:
```powershell
notepad $PROFILE
```
Add this line:
```powershell
$env:GITHUB_TOKEN="ghp_your_token_here"
```

---

## 🧪 Verify It's Working

Run this in your terminal:

**macOS/Linux:**
```bash
echo $GITHUB_TOKEN
```

**Windows (Command Prompt):**
```cmd
echo %GITHUB_TOKEN%
```

**Windows (PowerShell):**
```powershell
echo $env:GITHUB_TOKEN
```

You should see your token (starting with `ghp_...`)

---

## 🎯 Why Do I Need This?

- **GitHub Enterprise** (github.ibm.com) requires authentication for all API calls
- **Public GitHub** (github.com) allows 60 requests/hour without a token
- **With a token**: You get 5000 requests/hour + access to private repos

---

## 🐛 Still Not Working?

### Check Token Permissions
Make sure your token has:
- ✅ `repo` scope (for private repos)
- ✅ Access to the organization (github.ibm.com)

### Check Token Format
Token should look like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Check Organization Access
You might need to authorize the token for your organization:
1. Go to: https://github.ibm.com/settings/tokens
2. Click on your token
3. Under "Organization access", click "Grant" for your org

### Test with curl
```bash
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://github.ibm.com/api/v3/repos/David-Webster1/jakarta_security/issues/1
```

If this works, the web UI should work too!

---

## 🎉 Success!

Once you see the token in the startup message:
```
✓ GitHub token found
```

You're all set! Try analyzing your issue again. 🚀