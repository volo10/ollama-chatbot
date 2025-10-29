#!/bin/bash

# Ollama Chatbot Setup Script
# This script automates the setup process

set -e  # Exit on error

echo "🤖 Ollama AI Assistant - Setup Script"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION found"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
    echo "✅ uv installed successfully"
else
    UV_VERSION=$(uv --version)
    echo "✅ uv found: $UV_VERSION"
fi

# Create virtual environment
if [ -d ".venv" ]; then
    echo "📁 Virtual environment already exists"
    read -p "Do you want to recreate it? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing existing virtual environment..."
        rm -rf .venv
        echo "📦 Creating new virtual environment with uv..."
        uv venv
    fi
else
    echo "📦 Creating virtual environment with uv..."
    uv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
uv pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source .venv/bin/activate"
echo ""
echo "2. Make sure Ollama is installed and running:"
echo "   ollama serve"
echo ""
echo "3. Download a model if you haven't:"
echo "   ollama pull llama2"
echo ""
echo "4. Run the chatbot:"
echo "   python chatbot.py"
echo ""
echo "For more help, see QUICKSTART.md or README.md"

