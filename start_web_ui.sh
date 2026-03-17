#!/bin/bash

# GitHub Issue Analyzer - Web UI Launcher
# Quick start script for the Flask web interface

echo "=================================="
echo "🚀 GitHub Issue Analyzer Web UI"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment found"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    echo ""
    echo "Try manually:"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

echo "✓ Dependencies installed"
echo ""

# Check for GitHub token
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  Warning: GITHUB_TOKEN not set"
    echo "   You'll have lower API rate limits (60/hour vs 5000/hour)"
    echo "   Set it with: export GITHUB_TOKEN='your_token'"
    echo ""
else
    echo "✓ GitHub token found"
    echo ""
fi

# Start the server
echo "🌐 Starting Flask server..."
echo ""
echo "=================================="
echo "Open your browser to:"
echo "  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================="
echo ""

cd src/main/python
python web_app.py

# Made with Bob
