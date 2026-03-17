# 🚀 Flask Web UI for GitHub Issue Analyzer

A beautiful, modern web interface for analyzing GitHub issues and identifying Liberty packages.

![Modern UI](https://img.shields.io/badge/UI-Modern%20%26%20Smooth-blueviolet)
![Flask](https://img.shields.io/badge/Flask-3.0+-green)
![Python](https://img.shields.io/badge/Python-3.9+-blue)

---

## ✨ Features

- 🎨 **Modern, Smooth UI** - Glassmorphism effects, smooth animations, gradient backgrounds
- ⚡ **Real-time Analysis** - Instant feedback with loading animations
- 📊 **Visual Diagrams** - Auto-generated Mermaid diagrams
- 📦 **Package Detection** - Identifies Liberty packages with confidence scores
- 🎯 **Responsive Design** - Works on desktop, tablet, and mobile
- 🔍 **Example Issues** - Pre-loaded examples to try instantly

---

## 🚀 Quick Start (2 minutes)

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. Set GitHub Token (Optional but Recommended)

```bash
# For higher API rate limits (5000/hour vs 60/hour)
export GITHUB_TOKEN="your_github_token_here"
```

### 3. Run the Web Server

```bash
cd src/main/python
python web_app.py
```

### 4. Open in Browser

```
http://localhost:5000
```

That's it! 🎉

---

## 📸 Screenshots

### Main Interface
- Beautiful gradient background with animated particles
- Clean, modern input form
- Example issues for quick testing

### Analysis Results
- Issue information card
- Statistics dashboard (packages found, analysis time, confidence)
- Detailed package list with confidence scores
- Interactive Mermaid diagram

### Smooth Animations
- Fade-in effects on page load
- Slide-in animations for package items
- Hover effects on cards and buttons
- Loading spinner with pulse animation

---

## 🎯 How to Use

1. **Paste a GitHub Issue URL**
   ```
   https://github.com/OpenLiberty/open-liberty/issues/12345
   ```

2. **Click "Analyze Issue"**
   - The analyzer will fetch the issue
   - Identify Liberty packages
   - Calculate confidence scores
   - Generate a visual diagram

3. **View Results**
   - See identified packages with confidence levels
   - View the component diagram
   - Check analysis statistics

---

## 🏗️ Architecture

```
src/main/python/
├── web_app.py              # Flask application
├── github_issue_analyzer.py # Analysis engine
├── templates/
│   └── index.html          # Modern UI template
└── static/                 # (Future: CSS/JS files)
```

### API Endpoints

#### `POST /api/analyze`
Analyzes a GitHub issue and returns identified packages.

**Request:**
```json
{
  "issue_url": "https://github.com/owner/repo/issues/123"
}
```

**Response:**
```json
{
  "success": true,
  "issue": {
    "number": 123,
    "title": "Issue title",
    "author": "username",
    ...
  },
  "packages": [
    {
      "name": "io.openliberty.security.jwt",
      "confidence": 0.95,
      "package_type": "LIBERTY",
      "location": "code_block"
    }
  ],
  "analysis_time_ms": 1234
}
```

#### `POST /api/generate-diagram`
Generates a Mermaid diagram from packages.

**Request:**
```json
{
  "packages": [...],
  "issue_title": "Issue title"
}
```

**Response:**
```json
{
  "diagram": "graph TD\n    Issue[...]\n    ..."
}
```

#### `GET /health`
Health check endpoint.

---

## 🎨 Design Features

### Modern UI Elements
- **Glassmorphism** - Frosted glass effect on cards
- **Gradient Backgrounds** - Purple to violet gradient
- **Smooth Animations** - Fade-in, slide-in, hover effects
- **Inter Font** - Modern, clean typography
- **Responsive Grid** - Adapts to any screen size

### Color Palette
- Primary: `#667eea` (Purple)
- Secondary: `#764ba2` (Violet)
- Success: `#28a745` (Green)
- Warning: `#ffc107` (Yellow)
- Danger: `#dc3545` (Red)

### Animations
- Page load: Fade-in down (header), fade-in up (cards)
- Package items: Staggered slide-in
- Buttons: Hover lift, shine effect
- Loading: Spinning gradient border
- Errors: Shake animation

---

## 🔧 Configuration

### Port Configuration
Default port is `5000`. To change:

```python
# In web_app.py
app.run(debug=True, host='0.0.0.0', port=8080)  # Change to 8080
```

### Debug Mode
For production, disable debug mode:

```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

### GitHub Token
Set via environment variable:

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

Or pass directly:

```python
analyzer = GitHubIssueAnalyzer(github_token="your_token")
```

---

## 🚀 Deployment Options

### Option 1: Local Development
```bash
python web_app.py
```

### Option 2: Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

### Option 3: Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/main/python/ .
CMD ["python", "web_app.py"]
```

### Option 4: Deploy to Cloud
- **Heroku**: `heroku create && git push heroku main`
- **Railway**: Connect GitHub repo
- **Render**: Deploy from GitHub
- **AWS/Azure/GCP**: Use container services

---

## 🎯 Example Issues to Try

1. **MicroProfile Config Issue**
   ```
   https://github.com/OpenLiberty/open-liberty/issues/28000
   ```

2. **Security Feature Issue**
   ```
   https://github.com/OpenLiberty/open-liberty/issues/27500
   ```

3. **Configuration Issue**
   ```
   https://github.com/OpenLiberty/open-liberty/issues/27000
   ```

---

## 🐛 Troubleshooting

### "Module 'flask' not found"
```bash
pip install Flask
```

### "Connection refused"
- Check if the server is running
- Verify the port (default: 5000)
- Try `http://127.0.0.1:5000` instead of `localhost`

### "GitHub API rate limit exceeded"
- Set a GitHub token: `export GITHUB_TOKEN="your_token"`
- Wait for rate limit reset (shown in error message)

### "Issue not found"
- Verify the URL is correct
- Check if the issue is public
- Ensure you have access to the repository

---

## 🎨 Customization

### Change Colors
Edit the CSS in `templates/index.html`:

```css
/* Primary gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Change to blue gradient */
background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
```

### Add Your Logo
```html
<div class="header">
    <img src="/static/logo.png" alt="Logo" style="width: 60px; margin-bottom: 20px;">
    <h1>🤖 GitHub Issue Analyzer</h1>
</div>
```

### Modify Animations
```css
/* Faster animations */
.card {
    animation: fadeInUp 0.4s ease-out;  /* Changed from 0.8s */
}
```

---

## 📊 Performance

- **Analysis Time**: < 3 seconds (typical)
- **Page Load**: < 1 second
- **API Response**: < 2 seconds
- **Diagram Generation**: < 500ms

---

## 🔮 Future Enhancements

- [ ] Dark mode toggle
- [ ] Save analysis history
- [ ] Export results as PDF
- [ ] Batch analysis (multiple issues)
- [ ] Custom package patterns
- [ ] Integration with CI/CD
- [ ] User authentication
- [ ] Real-time collaboration

---

## 🤝 Contributing

This is a hackathon project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

Hackathon project - 2026

---

## 🆘 Need Help?

- Check the main [README.md](../../../README.md)
- Review the [IMPLEMENTATION_GUIDE.md](../../../IMPLEMENTATION_GUIDE.md)
- Open an issue on GitHub

---

## 🎉 Credits

Built for **Bobathon 2026** 🤖

**Team:** dave, deval, hannah, issac

**Tech Stack:**
- Flask (Python web framework)
- Mermaid.js (Diagrams)
- Inter Font (Typography)
- GitHub API (Data source)

---

**Enjoy analyzing GitHub issues with style! 🚀✨**