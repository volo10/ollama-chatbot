@echo off
REM Ollama Chatbot Setup Script for Windows
REM This script automates the setup process

echo.
echo 🤖 Ollama AI Assistant - Setup Script (Windows)
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% found

REM Check if uv is installed
uv --version >nul 2>&1
if errorlevel 1 (
    echo 📦 uv not found. Please install uv manually:
    echo Run: pip install uv
    echo Or visit: https://github.com/astral-sh/uv
    pause
    exit /b 1
)

echo ✅ uv found

REM Create virtual environment
if exist ".venv" (
    echo 📁 Virtual environment already exists
    set /p RECREATE="Do you want to recreate it? (y/n): "
    if /i "%RECREATE%"=="y" (
        echo 🗑️  Removing existing virtual environment...
        rmdir /s /q .venv
        echo 📦 Creating new virtual environment with uv...
        uv venv
    )
) else (
    echo 📦 Creating virtual environment with uv...
    uv venv
)

REM Activate virtual environment and install dependencies
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

echo 📥 Installing dependencies...
uv pip install -r requirements.txt

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Activate the virtual environment:
echo    .venv\Scripts\activate
echo.
echo 2. Make sure Ollama is installed and running
echo    Download from: https://ollama.ai/download
echo    Run: ollama serve
echo.
echo 3. Download a model if you haven't:
echo    ollama pull llama2
echo.
echo 4. Run the chatbot:
echo    python chatbot.py
echo.
echo For more help, see QUICKSTART.md or README.md
echo.
pause

