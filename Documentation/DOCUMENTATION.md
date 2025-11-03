# 📚 Ollama AI Assistant - Technical Documentation

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Code Structure](#code-structure)
3. [Class and Method Reference](#class-and-method-reference)
4. [API Integration](#api-integration)
5. [GUI Components](#gui-components)
6. [Threading Model](#threading-model)
7. [Customization Guide](#customization-guide)
8. [Best Practices](#best-practices)

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────┐
│          GUI Layer (Tkinter)            │
│  ┌────────────┐  ┌──────────────────┐  │
│  │  Top Bar   │  │   Side Panel     │  │
│  │            │  │   (Settings)     │  │
│  ├────────────┤  └──────────────────┘  │
│  │ Chat       │                         │
│  │ Display    │                         │
│  │            │                         │
│  ├────────────┤                         │
│  │ Input Area │                         │
│  └────────────┘                         │
└─────────────────────────────────────────┘
              ↓↑
┌─────────────────────────────────────────┐
│      Application Logic Layer            │
│  ┌────────────────────────────────────┐ │
│  │    OllamaChatbot Class             │ │
│  │  • Message handling                │ │
│  │  • State management                │ │
│  │  • Threading coordination          │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
              ↓↑
┌─────────────────────────────────────────┐
│         API Layer (requests)            │
│  ┌────────────────────────────────────┐ │
│  │    HTTP Communication              │ │
│  │    http://localhost:11434          │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
              ↓↑
┌─────────────────────────────────────────┐
│          Ollama Service                 │
│      (Local LLM Processing)             │
└─────────────────────────────────────────┘
```

### Design Patterns

1. **Model-View-Controller (MVC)**
   - **Model**: Chat history, settings, API communication
   - **View**: Tkinter GUI components
   - **Controller**: OllamaChatbot class methods

2. **Observer Pattern**: Event-driven GUI updates using Tkinter's event system

3. **Thread-Safe Operations**: Using `root.after()` for cross-thread GUI updates

---

## Code Structure

### File Organization

```python
chatbot.py
├── Imports
├── OllamaChatbot Class
│   ├── __init__              # Initialization
│   ├── GUI Setup Methods     # UI construction
│   ├── Event Handlers        # User interaction
│   ├── API Methods           # Ollama communication
│   └── Utility Methods       # Helper functions
└── main()                    # Entry point
```

### Module Dependencies

```python
import tkinter as tk           # GUI framework
from tkinter import ttk        # Themed widgets
from tkinter import scrolledtext  # (unused, can be removed)
from tkinter import messagebox    # Dialog boxes
import requests                # HTTP client for Ollama API
import json                    # JSON handling
import threading               # Async operations
from datetime import datetime  # Timestamps
import os                      # File operations
```

---

## Class and Method Reference

### OllamaChatbot Class

```python
class OllamaChatbot:
    """
    Main application class that manages the GUI and API communication.
    
    Attributes:
        root (tk.Tk): Main window instance
        colors (dict): Color scheme definitions
        ollama_url (str): Ollama API endpoint
        current_model (tk.StringVar): Selected model name
        temperature (tk.DoubleVar): Temperature parameter
        system_prompt (str): System prompt text
        chat_history (list): Conversation history
        is_generating (bool): Response generation flag
    """
```

### Initialization Methods

#### `__init__(self, root)`

**Purpose**: Initialize the application and create the main window.

**Parameters**:
- `root` (tk.Tk): The main Tkinter window instance

**Process**:
1. Sets up window properties (title, size, colors)
2. Initializes configuration variables
3. Calls GUI setup methods
4. Schedules connection check

**Example**:
```python
root = tk.Tk()
app = OllamaChatbot(root)
root.mainloop()
```

---

### GUI Setup Methods

#### `setup_gui(self)`

**Purpose**: Orchestrates the creation of all GUI components.

**Flow**:
```
setup_gui()
    ├── create_top_bar()
    ├── create_chat_display()
    ├── create_input_area()
    ├── create_side_panel()
    └── create_status_bar()
```

#### `create_top_bar(self)`

**Purpose**: Creates the header with logo and control buttons.

**Components**:
- Logo emoji (🤖)
- Application title
- Clear Chat button
- Export Chat button

**Layout**: Horizontal bar at the top

#### `create_chat_display(self, parent)`

**Purpose**: Creates the main chat display area.

**Components**:
- Canvas with custom styling
- Scrollbar for navigation
- Text widget with custom tags

**Tags for Styling**:
```python
"user"      # User message styling
"bot"       # Bot message styling
"timestamp" # Timestamp styling
"system"    # System message styling
```

**Features**:
- Disabled editing (read-only)
- Auto-scroll to bottom
- Word wrapping
- Custom backgrounds per message type

#### `create_input_area(self, parent)`

**Purpose**: Creates the message input section.

**Components**:
- Multi-line text input
- Send button
- Key bindings (Enter, Shift+Enter)

**Key Bindings**:
```python
<Return>        # Send message
<Shift-Return>  # New line
```

#### `create_side_panel(self, parent)`

**Purpose**: Creates the settings panel.

**Sections**:
1. Model selection dropdown
2. Temperature slider
3. System prompt text area
4. Connection status indicator

**Width**: Fixed at 250 pixels

#### `create_status_bar(self)`

**Purpose**: Creates the bottom status bar.

**Features**:
- Shows current application state
- Updates during operations
- Left-aligned text

---

### Setting Components

#### `create_model_selector(self, parent)`

**Purpose**: Creates dropdown for model selection.

**Available Models**:
```python
["llama2", "mistral", "codellama", "llama3", "phi", "gemma"]
```

**Styling**: Uses ttk.Combobox with custom theme

#### `create_temperature_slider(self, parent)`

**Purpose**: Creates temperature adjustment slider.

**Range**: 0.0 to 2.0
**Resolution**: 0.1
**Default**: 0.7

**Features**:
- Live value display
- Custom colors
- Smooth sliding

#### `create_system_prompt_input(self, parent)`

**Purpose**: Creates text area for system prompt.

**Features**:
- Multi-line editing
- Custom styling
- Default prompt included

---

### Event Handlers

#### `on_enter_key(self, event)`

**Purpose**: Handles Enter key press in input field.

**Behavior**:
- `Enter`: Send message
- `Shift+Enter`: New line

**Implementation**:
```python
def on_enter_key(self, event):
    if not event.state & 0x1:  # Shift not pressed
        self.send_message()
        return "break"  # Prevent default behavior
```

#### `send_message(self)`

**Purpose**: Processes and sends user message.

**Flow**:
```
1. Get message text
2. Validate message
3. Check if generating
4. Clear input
5. Display user message
6. Add to history
7. Start generation thread
```

**Thread Safety**: Uses threading to prevent UI blocking

---

### API Communication

#### `get_bot_response(self)`

**Purpose**: Communicates with Ollama API to get response.

**Process**:
```python
1. Prepare payload with:
   - Model name
   - System prompt
   - Conversation history
   - Temperature setting

2. Send POST request to Ollama

3. Parse response

4. Update GUI using root.after()

5. Handle errors gracefully
```

**API Endpoint**:
```
POST http://localhost:11434/api/chat
```

**Payload Structure**:
```json
{
  "model": "llama2",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"},
    {"role": "user", "content": "How are you?"}
  ],
  "stream": false,
  "options": {
    "temperature": 0.7
  }
}
```

**Response Structure**:
```json
{
  "message": {
    "role": "assistant",
    "content": "I'm doing well, thank you for asking!"
  },
  "done": true
}
```

**Error Handling**:
- HTTP errors (status codes)
- Connection timeouts
- JSON parsing errors
- General exceptions

#### `check_ollama_connection(self)`

**Purpose**: Verifies Ollama service is running.

**Endpoint**: `GET http://localhost:11434/api/tags`

**Updates**:
- Connection indicator color
- Connection indicator text
- Status bar message

**States**:
- ● Connected (Green)
- ● Disconnected (Red)
- ● Checking... (Orange)
- ● Error (Red)

---

### Display Methods

#### `display_message(self, message, sender)`

**Purpose**: Displays a message in the chat area.

**Parameters**:
- `message` (str): Message text
- `sender` (str): One of "user", "bot", "system"

**Format**:
```
[HH:MM] Sender:
Message text

```

**Process**:
1. Enable text widget
2. Generate timestamp
3. Insert header with timestamp
4. Insert message with appropriate tag
5. Disable text widget
6. Scroll to bottom

**Tags Applied**:
- "user": Blue background
- "bot": Dark background
- "system": Centered, italic, accent color

---

### Utility Methods

#### `clear_chat(self)`

**Purpose**: Clears all chat history.

**Features**:
- Confirmation dialog
- Resets chat_history list
- Clears display
- Shows system message

**Implementation**:
```python
def clear_chat(self):
    if messagebox.askyesno("Clear Chat", "Are you sure?"):
        self.chat_history = []
        # Clear display
        # Show confirmation
```

#### `export_chat(self)`

**Purpose**: Exports conversation to text file.

**File Format**:
```
Ollama Chat Export - YYYY-MM-DD HH:MM:SS
Model: llama2
Temperature: 0.7
================================================================================

USER:
Hello there!

ASSISTANT:
Hi! How can I help you today?

USER:
Tell me a joke.

ASSISTANT:
Why did the programmer quit his job?
Because he didn't get arrays!
```

**Filename**: `chat_export_YYYYMMDD_HHMMSS.txt`

**Error Handling**: Shows error dialog if export fails

#### `update_status(self, message)`

**Purpose**: Updates the status bar text.

**Usage**:
```python
self.update_status("Generating response...")
self.update_status("Ready")
self.update_status("Error occurred")
```

#### `update_temp_label(self, value)`

**Purpose**: Updates temperature display label.

**Format**: Shows value with 1 decimal place (e.g., "0.7")

#### `create_styled_button(self, parent, text, command, width, height)`

**Purpose**: Creates a button with custom styling.

**Features**:
- Custom colors
- Hover effects
- Flat design
- Hand cursor

**Hover Behavior**:
```python
Normal:  accent color (#e94560)
Hover:   accent_hover color (#ff6b81)
```

---

## API Integration

### Ollama API Reference

#### Chat Endpoint

**URL**: `http://localhost:11434/api/chat`

**Method**: POST

**Headers**: 
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "model": string,           // Model name (required)
  "messages": array,         // Message history (required)
  "stream": boolean,         // Stream response (optional)
  "options": {              // Generation options (optional)
    "temperature": float,   // 0.0 to 2.0
    "top_p": float,        // Nucleus sampling
    "top_k": int,          // Top-k sampling
    "num_predict": int     // Max tokens to generate
  }
}
```

**Response**: 
```json
{
  "model": string,
  "created_at": string,
  "message": {
    "role": "assistant",
    "content": string
  },
  "done": true
}
```

#### Tags Endpoint (Connection Check)

**URL**: `http://localhost:11434/api/tags`

**Method**: GET

**Response**:
```json
{
  "models": [
    {
      "name": "llama2:latest",
      "modified_at": "2024-01-01T00:00:00Z",
      "size": 3826793677
    }
  ]
}
```

### Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response |
| 400 | Bad Request | Check payload format |
| 404 | Model Not Found | Download model |
| 500 | Server Error | Check Ollama logs |
| Timeout | No Response | Check if Ollama is running |

---

## Threading Model

### Thread Architecture

```
Main Thread (GUI)
    │
    ├── User Events (Button clicks, key presses)
    │
    └── Creates Worker Threads
            │
            ├── get_bot_response()
            │       │
            │       ├── HTTP Request to Ollama
            │       └── root.after() → GUI Update
            │
            └── check_ollama_connection()
                    │
                    ├── HTTP Request
                    └── root.after() → GUI Update
```

### Thread Safety

**Problem**: Tkinter is not thread-safe. GUI updates must occur on the main thread.

**Solution**: Use `root.after(0, callback)` to schedule GUI updates.

**Example**:
```python
# In worker thread
def get_bot_response(self):
    response = requests.post(...)
    
    # Schedule GUI update on main thread
    self.root.after(0, lambda: self.display_message(msg, "bot"))
```

### Blocking Prevention

To keep the UI responsive:
1. Long operations run in separate threads
2. Disable controls during operations
3. Show status indicators
4. Use timeout for API calls

**Example**:
```python
self.is_generating = True
self.send_button.config(state=tk.DISABLED)
threading.Thread(target=self.get_bot_response, daemon=True).start()
```

---

## Customization Guide

### Adding New Models

**Step 1**: Download model with Ollama
```bash
ollama pull model-name
```

**Step 2**: Add to model list
```python
def create_model_selector(self, parent):
    models = ["llama2", "mistral", "your-new-model"]
    # ...
```

### Custom Color Schemes

**Light Theme Example**:
```python
self.colors = {
    'bg_primary': '#f5f5f5',
    'bg_secondary': '#ffffff',
    'bg_tertiary': '#e0e0e0',
    'accent': '#2196f3',
    'accent_hover': '#1976d2',
    'text_primary': '#000000',
    'text_secondary': '#666666',
    'success': '#4caf50',
    'warning': '#ff9800',
    'user_msg': '#e3f2fd',
    'bot_msg': '#f5f5f5',
}
```

### Adding Custom Options

**Example: Adding Max Tokens Setting**

**Step 1**: Add variable
```python
def __init__(self, root):
    # ... other initializations
    self.max_tokens = tk.IntVar(value=512)
```

**Step 2**: Add UI component
```python
def create_max_tokens_slider(self, parent):
    slider = tk.Scale(
        parent,
        from_=128,
        to=2048,
        orient=tk.HORIZONTAL,
        variable=self.max_tokens,
        # ... styling
    )
    slider.pack()
```

**Step 3**: Use in API call
```python
payload = {
    "model": self.current_model.get(),
    "messages": [...],
    "options": {
        "temperature": self.temperature.get(),
        "num_predict": self.max_tokens.get()  # New option
    }
}
```

### Custom Message Formatting

**Example: Add Message Icons**

```python
def display_message(self, message, sender):
    # ... existing code
    
    if sender == "user":
        prefix = "👤 You"
    elif sender == "bot":
        prefix = "🤖 AI"
    else:
        prefix = "⚙️ System"
    
    # ... rest of the method
```

---

## Best Practices

### Code Organization

1. **Keep methods focused**: Each method should do one thing
2. **Use descriptive names**: `create_chat_display` not `make_chat`
3. **Comment complex logic**: Explain why, not what
4. **Group related methods**: All GUI creation methods together

### Performance

1. **Use threading**: Never block the main thread
2. **Lazy loading**: Load resources when needed
3. **Limit history**: Consider trimming old messages
4. **Optimize redraws**: Minimize display updates

### Error Handling

1. **Always use try-except** for API calls
2. **Provide user feedback** for errors
3. **Log errors** for debugging
4. **Graceful degradation**: App should work even if Ollama is down

**Example**:
```python
try:
    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()
except requests.Timeout:
    self.display_message("Request timed out", "system")
except requests.ConnectionError:
    self.display_message("Cannot connect to Ollama", "system")
except Exception as e:
    self.display_message(f"Error: {str(e)}", "system")
```

### Security

1. **Validate user input**: Sanitize before sending to API
2. **Handle malicious responses**: Escape special characters if needed
3. **Secure file operations**: Check permissions before writing
4. **Local only**: Never expose Ollama to internet without authentication

### User Experience

1. **Provide feedback**: Show status during operations
2. **Confirm destructive actions**: Ask before clearing chat
3. **Keyboard shortcuts**: Make common actions quick
4. **Responsive design**: Never freeze the UI
5. **Helpful errors**: Tell users how to fix problems

---

## Advanced Topics

### Implementing Streaming Responses

To show responses word-by-word:

```python
def get_bot_response_streaming(self):
    payload = {
        "model": self.current_model.get(),
        "messages": [...],
        "stream": True  # Enable streaming
    }
    
    response = requests.post(
        self.ollama_url,
        json=payload,
        stream=True
    )
    
    full_response = ""
    for line in response.iter_lines():
        if line:
            chunk = json.loads(line)
            content = chunk.get("message", {}).get("content", "")
            full_response += content
            
            # Update display in real-time
            self.root.after(0, lambda: self.update_partial_message(full_response))
```

### Adding Conversation Context Management

```python
def manage_context(self, max_tokens=4096):
    """Trim conversation history to fit within context window"""
    
    # Simple approach: Keep last N messages
    if len(self.chat_history) > 20:
        self.chat_history = self.chat_history[-20:]
    
    # Advanced: Count tokens and trim intelligently
    # (requires tokenizer library)
```

### Implementing RAG (Retrieval Augmented Generation)

```python
def add_document_context(self, user_query):
    """Add relevant document context to the query"""
    
    # 1. Search documents for relevant content
    relevant_docs = self.search_documents(user_query)
    
    # 2. Add to system prompt or user message
    context = "\n".join(relevant_docs)
    enhanced_query = f"Context:\n{context}\n\nQuery: {user_query}"
    
    return enhanced_query
```

---

## Debugging Tips

### Enable Debug Mode

Add logging:
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# In methods:
logging.debug(f"Sending request: {payload}")
logging.debug(f"Received response: {response.json()}")
```

### Common Issues

**Issue**: GUI freezes during response
**Solution**: Check that API calls are in separate threads

**Issue**: Messages don't display
**Solution**: Verify `display_message` is called on main thread

**Issue**: Connection always fails
**Solution**: Check Ollama is running: `ollama serve`

**Issue**: Wrong model error
**Solution**: Verify model is downloaded: `ollama list`

---

## Testing

### Manual Testing Checklist

- [ ] Application starts without errors
- [ ] Connection indicator shows correct status
- [ ] Can send messages and receive responses
- [ ] Model selection changes behavior
- [ ] Temperature adjustment works
- [ ] System prompt customization works
- [ ] Chat can be cleared
- [ ] Chat can be exported
- [ ] Keyboard shortcuts work
- [ ] Window can be resized
- [ ] Status bar updates correctly

### Automated Testing (Future Enhancement)

```python
import unittest

class TestOllamaChatbot(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = OllamaChatbot(self.root)
    
    def test_message_display(self):
        self.app.display_message("Test", "user")
        content = self.app.chat_display.get("1.0", tk.END)
        self.assertIn("Test", content)
    
    def tearDown(self):
        self.root.destroy()
```

---

## API Alternatives

If you want to support other LLM APIs:

### OpenAI API
```python
def get_openai_response(self, messages):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "gpt-3.5-turbo",
            "messages": messages
        }
    )
    return response.json()
```

### Anthropic Claude
```python
def get_claude_response(self, messages):
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        },
        json={
            "model": "claude-3-sonnet-20240229",
            "messages": messages
        }
    )
    return response.json()
```

---

## Conclusion

This documentation covers the complete technical implementation of the Ollama AI Assistant. For questions or issues:

1. Review this documentation
2. Check the README.md for usage instructions
3. Consult Ollama documentation: https://ollama.ai/docs
4. Review the source code comments

**Remember**: The code is designed to be readable and modifiable. Don't hesitate to customize it for your needs!

---

*Documentation Version: 1.0*
*Last Updated: October 2025*
*Compatible with: Python 3.8+, Ollama 0.1.0+*

