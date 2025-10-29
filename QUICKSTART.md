# 🚀 Quick Start Guide - Ollama AI Assistant

Get up and running in 5 minutes!

## Prerequisites Check

Before starting, verify you have:
- [ ] Python 3.8 or higher installed
- [ ] Terminal/Command Prompt access
- [ ] Internet connection (for downloading Ollama and models)

## Step-by-Step Setup

### 1️⃣ Clone & Setup Environment (1 minute)

```bash
# Clone the repository (after you upload it)
git clone https://github.com/volo10/ollama-chatbot.git
cd ollama-chatbot

# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows
```

### 2️⃣ Install Dependencies (30 seconds)

```bash
# Using uv (much faster!)
uv pip install -r requirements.txt
```

### 3️⃣ Install Ollama (2 minutes)

**macOS/Linux:**
```bash
curl https://ollama.ai/install.sh | sh
```

**Windows:**
Download and install from: https://ollama.ai/download

### 4️⃣ Download a Model (2-5 minutes)

Open a terminal and run:
```bash
ollama pull llama2
```

Wait for the download to complete. You'll see a progress bar.

### 5️⃣ Start Ollama Service (10 seconds)

```bash
ollama serve
```

**Keep this terminal window open!** You should see:
```
Listening on http://localhost:11434
```

### 6️⃣ Run the Chatbot (5 seconds)

```bash
python chatbot.py
```

**That's it!** The application window should open.

## First Steps in the App

1. **Check Connection**: Look at the bottom right of the settings panel. It should show "● Connected" in green.

2. **Type a Message**: Click in the text box at the bottom and type: "Hello, who are you?"

3. **Send**: Press `Enter` or click the "Send →" button

4. **Wait for Response**: The bot will think for a few seconds and respond.

## Quick Tips

### Keyboard Shortcuts
- `Enter` - Send message
- `Shift + Enter` - New line in message

### Adjusting Response Style
- **More Creative**: Move temperature slider to the right (1.0-1.5)
- **More Focused**: Move temperature slider to the left (0.3-0.5)

### Changing the AI's Personality
Edit the "System Prompt" box in the settings panel:

**Examples:**
```
"You are a friendly pirate. Respond in pirate speak."
"You are a professional code reviewer."
"You are a creative storyteller."
```

### Try Different Models
Click the Model dropdown and select:
- `llama2` - General purpose (default)
- `mistral` - High quality responses
- `codellama` - Best for programming

*Note: You need to download models first with `ollama pull model-name`*

## Troubleshooting

### ❌ "Ollama not running" message

**Solution:**
1. Open a terminal
2. Run: `ollama serve`
3. Keep it running
4. Restart the chatbot app

### ❌ "Model not found" error

**Solution:**
```bash
# List downloaded models
ollama list

# Download the missing model
ollama pull llama2
```

### ❌ Slow responses

**Solutions:**
- Use a smaller model: `ollama pull phi`
- Lower temperature setting
- Close other programs to free RAM

### ❌ App won't start

**Solution:**
```bash
# Check Python version (need 3.8+)
python --version

# Or try
python3 chatbot.py
```

## Example Conversations

### General Chat
```
You: What's the capital of France?
AI: The capital of France is Paris.
```

### Code Help
```
You: Write a Python function to reverse a string
AI: Here's a function that reverses a string:

def reverse_string(s):
    return s[::-1]

# Example usage:
result = reverse_string("hello")
print(result)  # Output: "olleh"
```

### Creative Writing
*(Set temperature to 1.2 first)*
```
You: Write a short poem about coding
AI: In the realm of bits and bytes so bright,
Where logic weaves through day and night,
The coder sits with focused mind,
Creating worlds of every kind...
```

## Next Steps

- **Read the full README.md** for detailed features
- **Check DOCUMENTATION.md** for technical details
- **Experiment with settings** to find your perfect configuration
- **Try different models** to compare responses
- **Export your chats** to keep interesting conversations

## Need More Help?

1. Check the full **README.md** file
2. Review **DOCUMENTATION.md** for technical details
3. Visit Ollama docs: https://ollama.ai/docs
4. Check Ollama Discord community

---

**Enjoy your new AI assistant!** 🎉

*Setup time: ~5-10 minutes*
*Start chatting: Immediately after setup*

