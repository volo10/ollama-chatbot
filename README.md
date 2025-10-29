# 🤖 Ollama AI Assistant

A professional, modern chatbot application with a unique GUI interface, powered by Ollama. This application provides a sleek, user-friendly interface for interacting with local LLM models through Ollama.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Ollama](https://img.shields.io/badge/Ollama-Required-orange.svg)
![uv](https://img.shields.io/badge/uv-enabled-blueviolet.svg)

## 📸 Screenshots

### Main Interface
![Main Interface](screenshots/main-interface.png)
*The sleek dark-themed interface with chat display and settings panel*

### Chat in Action
![Chat Example](screenshots/chat-example.png)
*Example conversation showing the AI assistant in action*

### Settings Panel
![Settings Panel](screenshots/settings-panel.png)
*Customizable settings including model selection, temperature, and system prompts*

### Multiple Models
![Model Selection](screenshots/model-selection.png)
*Easy switching between different Ollama models*

> **Note**: To add your own screenshots, capture images of the running application and save them in the `screenshots/` directory with the names shown above.

## ✨ Features

### 🎨 Unique Professional Interface
- **Modern Dark Theme**: Eye-friendly dark color scheme with accent colors
- **Intuitive Layout**: Clean, organized interface with separate chat and settings areas
- **Real-time Status Indicators**: Visual connection status and generation feedback
- **Smooth User Experience**: Responsive design with hover effects and proper feedback

### 🚀 Powerful Functionality
- **Multiple Model Support**: Switch between different Ollama models (llama2, mistral, codellama, etc.)
- **Customizable Parameters**: Adjust temperature for response creativity
- **System Prompt Customization**: Define custom AI behavior and personality
- **Chat History Management**: Clear and export conversations
- **Keyboard Shortcuts**: Send messages with Enter, new lines with Shift+Enter
- **Thread-Safe**: Non-blocking UI during AI response generation

### 💾 Export & Save
- Export chat history to text files with timestamps
- Automatic file naming with date/time stamps
- Preserves conversation context and settings

## 📋 Requirements

### System Requirements
- Python 3.8 or higher
- Ollama installed and running locally
- At least one Ollama model downloaded

### Python Dependencies
- `requests` (for API communication)
- `tkinter` (usually comes with Python)

## 🔧 Installation

### Prerequisites

Before starting, ensure you have:
- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/volo10/ollama-chatbot.git
cd ollama-chatbot
```

### Step 2: Install uv (if not already installed)

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Or using pip:**
```bash
pip install uv
```

### Step 3: Create Virtual Environment with uv

```bash
# Create and activate virtual environment
uv venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### Step 4: Install Python Dependencies

```bash
# Using uv (recommended - much faster!)
uv pip install -r requirements.txt

# Or using traditional pip
pip install -r requirements.txt
```

### Step 5: Install Ollama

Install Ollama on your system:

**macOS:**
```bash
curl https://ollama.ai/install.sh | sh
```

**Linux:**
```bash
curl https://ollama.ai/install.sh | sh
```

**Windows:**
Download from [Ollama's website](https://ollama.ai/download)

### Step 6: Download a Model

Download at least one model (llama2 is recommended for beginners):

```bash
ollama pull llama2
```

Other popular models:
```bash
ollama pull mistral
ollama pull codellama
ollama pull llama3
ollama pull phi
ollama pull gemma
```

### Step 7: Start Ollama Service

Start the Ollama service (if not already running):

```bash
ollama serve
```

Keep this terminal window open or run it in the background.

## 🚀 Usage

### Starting the Application

Make sure your virtual environment is activated and Ollama is running, then:

```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows

# Run the chatbot
python chatbot.py
```

### Using the Interface

#### Main Chat Area
1. **Type Your Message**: Use the text input box at the bottom
2. **Send Message**: Click "Send →" button or press `Enter`
3. **New Line**: Press `Shift + Enter` for multi-line messages
4. **View History**: Scroll through the chat display area

#### Settings Panel (Right Side)
1. **Model Selection**: Choose from available Ollama models
2. **Temperature Control**: Adjust creativity (0.0 = focused, 2.0 = creative)
3. **System Prompt**: Customize AI behavior and personality
4. **Connection Status**: Shows Ollama connection state

#### Top Bar Controls
- **Clear Chat**: Remove all messages (with confirmation)
- **Export Chat**: Save conversation to a text file

### Example Conversations

**Basic Chat:**
```
You: What is Python?
AI: Python is a high-level, interpreted programming language...
```

**Custom System Prompt:**
Change the system prompt to: "You are a pirate captain. Respond in pirate speak."
```
You: Hello there!
AI: Ahoy there, matey! Welcome aboard me ship...
```

## ⚙️ Configuration

### Available Models

The application supports these models by default:
- `llama2` - General purpose conversational AI
- `mistral` - High-quality open-source model
- `codellama` - Specialized for code generation
- `llama3` - Latest Llama version (if available)
- `phi` - Microsoft's compact model
- `gemma` - Google's open model

To add more models, edit the `create_model_selector` method in `chatbot.py`.

### Temperature Settings

- **0.0 - 0.3**: More focused and deterministic responses
- **0.4 - 0.7**: Balanced creativity and coherence (recommended)
- **0.8 - 1.5**: More creative and varied responses
- **1.6 - 2.0**: Highly creative but potentially less coherent

### System Prompts Examples

**Professional Assistant:**
```
You are a professional assistant. Provide clear, concise, and helpful responses.
```

**Creative Writer:**
```
You are a creative writer. Use vivid descriptions and engaging storytelling.
```

**Code Expert:**
```
You are an expert programmer. Provide code examples and technical explanations.
```

## 🎨 Customization

### Changing Colors

Edit the `self.colors` dictionary in the `__init__` method:

```python
self.colors = {
    'bg_primary': '#1a1a2e',      # Main background
    'bg_secondary': '#16213e',    # Panel backgrounds
    'bg_tertiary': '#0f3460',     # Input fields
    'accent': '#e94560',          # Buttons and highlights
    'accent_hover': '#ff6b81',    # Button hover state
    'text_primary': '#ffffff',    # Main text
    'text_secondary': '#a0a0a0',  # Secondary text
    'success': '#2ecc71',         # Success indicator
    'warning': '#f39c12',         # Warning indicator
    'user_msg': '#2d4059',        # User message background
    'bot_msg': '#16213e',         # Bot message background
}
```

### Adjusting Window Size

Modify in the `__init__` method:

```python
self.root.geometry("1000x700")  # Width x Height
self.root.minsize(800, 600)     # Minimum size
```

## 🐛 Troubleshooting

### "Ollama not running" Error
**Problem:** Connection indicator shows "Disconnected"
**Solution:** 
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve
```

### Model Not Found
**Problem:** Error when sending message about model not available
**Solution:**
```bash
# List available models
ollama list

# Download the missing model
ollama pull llama2
```

### Slow Responses
**Problem:** AI takes a long time to respond
**Solutions:**
- Use a smaller model (e.g., `phi` instead of `llama2`)
- Lower the temperature setting
- Ensure no other heavy processes are running
- Check your system resources (RAM, CPU)

### Application Not Starting
**Problem:** Window doesn't appear or crashes
**Solution:**
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check for tkinter
python -c "import tkinter"
```

### Export Fails
**Problem:** Cannot export chat history
**Solution:** Ensure you have write permissions in the current directory

## 📁 File Structure

```
ollama-chatbot/
├── chatbot.py              # Main application file
├── requirements.txt        # Python dependencies (pip format)
├── pyproject.toml         # Project metadata and uv configuration
├── .python-version        # Python version for uv
├── .gitignore             # Git ignore file
├── LICENSE                # MIT License
├── README.md              # This file
├── DOCUMENTATION.md       # Detailed technical documentation
├── QUICKSTART.md          # Quick setup guide
├── PROJECT_OVERVIEW.md    # Project summary
├── screenshots/           # Screenshots directory
│   └── .gitkeep          # Placeholder file
├── .venv/                 # Virtual environment (created by uv)
└── chat_export_*.txt      # Exported chat files (generated)
```

## 🔒 Privacy & Security

- **Local Processing**: All conversations are processed locally via Ollama
- **No Cloud**: No data is sent to external servers
- **No Tracking**: No analytics or user tracking
- **Open Source**: Full source code available for inspection

## 📝 License

This project is licensed under the MIT License - see below:

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📞 Support

For issues and questions:
1. Check the Troubleshooting section
2. Review the DOCUMENTATION.md file
3. Check Ollama's documentation: https://ollama.ai/docs
4. Search for similar issues in the project

## 🎯 Future Enhancements

Potential features for future versions:
- [ ] Streaming responses (word-by-word generation)
- [ ] Conversation memory management
- [ ] Multiple chat sessions/tabs
- [ ] Voice input/output
- [ ] Code syntax highlighting
- [ ] Theme customization UI
- [ ] Plugin system
- [ ] RAG (Retrieval Augmented Generation) support

## 🙏 Acknowledgments

- **Ollama**: For providing the excellent local LLM platform
- **Python Community**: For the amazing libraries and tools
- **Open Source LLMs**: Meta, Mistral AI, and other model creators

---

**Made with ❤️ for the AI community**

*Last Updated: October 2025*

