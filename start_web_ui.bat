@echo off
REM GitHub Issue Analyzer - Web UI Launcher (Windows)
REM Quick start script for the Flask web interface

echo ==================================
echo 🚀 GitHub Issue Analyzer Web UI
echo ==================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python 3 is not installed
    echo Please install Python 3.9 or higher from python.org
    pause
    exit /b 1
)

echo ✓ Python found
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment found
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✓ Virtual environment activated
echo.

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    echo.
    echo Try manually:
    echo   venv\Scripts\activate.bat
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

echo ✓ Dependencies installed
echo.

REM Check for GitHub token
if "%GITHUB_TOKEN%"=="" (
    echo ⚠️  Warning: GITHUB_TOKEN not set
    echo    You'll have lower API rate limits (60/hour vs 5000/hour^)
    echo    Set it with: set GITHUB_TOKEN=your_token
    echo.
) else (
    echo ✓ GitHub token found
    echo.
)

REM Start the server
echo 🌐 Starting Flask server...
echo.
echo ==================================
echo Open your browser to:
echo   http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ==================================
echo.

cd src\main\python
python web_app.py

@REM Made with Bob
