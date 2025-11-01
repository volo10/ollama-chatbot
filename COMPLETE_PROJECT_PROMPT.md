# 🤖 Complete Ollama Chatbot Project - Reconstruction Prompt

## Project Specification

Build a professional desktop chatbot application using Python and Tkinter that interfaces with Ollama for local LLM interactions. The application should have a modern ChatGPT-inspired interface with comprehensive features.

---

## 🎯 Core Requirements

### **Application Name**: Ollama AI Assistant
### **Version**: 3.0
### **Platform**: Desktop (macOS, Linux, Windows)
### **Framework**: Python 3.8+ with Tkinter
### **Architecture**: MVC pattern with threading for async operations

---

## 🎨 UI/UX Requirements

### **Design Philosophy**
- Modern, clean ChatGPT-inspired interface
- Light theme with professional color scheme
- Intuitive layout with clear visual hierarchy
- Responsive and non-blocking user experience
- Window size: 1400x900 (minimum 1200x800)

### **Color Scheme**
```python
colors = {
    'bg_primary': '#ffffff',        # Main background
    'bg_secondary': '#f7f7f8',      # Secondary areas
    'bg_tertiary': '#ececf1',       # Tertiary elements
    'sidebar': '#202123',           # Dark sidebar
    'sidebar_hover': '#2a2b32',     # Sidebar hover
    'accent': '#10a37f',            # Primary accent (green)
    'accent_hover': '#1a7f64',      # Accent hover
    'text_primary': '#353740',      # Main text
    'text_secondary': '#6e6e80',    # Secondary text
    'text_white': '#ffffff',        # White text
    'border': '#d9d9e3',            # Borders
    'user_msg': '#f7f7f8',          # User message bg
    'bot_msg': '#ffffff',           # Bot message bg
    'ticker_bg': '#10a37f',         # Ticker background
    'ticker_text': '#ffffff'        # Ticker text
}
```

### **Layout Structure**
```
┌─────────────────────────────────────────────────────────────┐
│  Fun Facts Ticker (rotating facts every 5 seconds)          │
├──────────────┬──────────────────────────────────────────────┤
│  SIDEBAR     │  MAIN CHAT AREA                              │
│  (280px)     │                                              │
│              │  [Messages displayed here]                   │
│  + New Chat  │  You: Hello                                  │
│  ────────    │  AI: Hi there!                               │
│  Recent:     │                                              │
│  ● Chat 1    │                                              │
│  ○ Chat 2    │                                              │
│  ○ Chat 3    │                                              │
│              ├──────────────────────────────────────────────┤
│              │  Settings: Model [▼] Temp [slider] [Export] │
│              ├──────────────────────────────────────────────┤
│  v3.0        │  📁 File  🖼 Image                           │
│              │  ┌─────────────────────────────────┐  ┌──┐  │
│              │  │ Type message...                │  │→ │  │
│              │  └─────────────────────────────────┘  └──┘  │
└──────────────┴──────────────────────────────────────────────┘
```

---

## ⚙️ Core Features

### **1. Chat Management**
- Create new chats with "+ New Chat" button
- Save chat history persistently (pickle format)
- Auto-name chats from first message (max 40 chars)
- Display chat list in sidebar (most recent first)
- Click to switch between chats instantly
- Delete chats with confirmation dialog
- Export individual chats to text files
- Store: chat ID, name, messages, timestamps

### **2. Message Handling**
- Text input area (4 lines, expandable)
- Send button (→ symbol)
- Keyboard shortcuts: Enter to send, Shift+Enter for new line
- Display messages with timestamps
- User messages: left-aligned, light gray background
- AI messages: left-aligned, white background
- System messages: centered, italic
- Auto-scroll to latest message
- Thread-safe message display

### **3. File Upload**
- Button: "📁 File"
- Support: .txt, .py, .js, .md, .json, .java, .cpp, etc.
- Read with UTF-8 encoding
- Truncate to 5000 chars per file
- Show file name and size in preview
- Support multiple files
- Embed content in message context

### **4. Image Upload**
- Button: "🖼 Image"
- Support: PNG, JPG, JPEG, GIF, BMP
- Base64 encode for API
- Show image name in preview
- Support multiple images
- Auto-suggest llava model for images
- Send with vision model support

### **5. Model Management**
- Dropdown selector with models:
  - llama2 (default)
  - llava (vision)
  - mistral
  - codellama
  - llama3
  - phi
  - gemma
- Change model anytime
- Model persists per chat

### **6. Temperature Control**
- Slider: 0.0 to 2.0 (resolution 0.1)
- Default: 0.7
- Live value display
- Tooltips: 0-0.3 focused, 0.4-0.7 balanced, 0.8-1.5 creative, 1.6-2.0 very creative

### **7. Fun Facts Ticker**
- Top banner (35px height)
- Green background (#10a37f)
- White text
- Auto-rotate every 5 seconds
- 20 diverse facts covering:
  - Animals (sharks, octopuses, bees, giraffes, lizards, snails)
  - Science (brain, stars, moon, diamonds, waves)
  - History (library, war, Leonardo da Vinci, Eiffel Tower)
  - Nature (ocean, rainbow, trees)
  - Food (honey, coffee, bananas)
  - Random interesting facts

Example facts:
- "🦈 Sharks have been around longer than trees - about 400 million years!"
- "🍯 Honey never spoils - archaeologists found 3,000 year old honey that's still edible!"
- "🌍 There are more stars in the universe than grains of sand on all Earth's beaches!"

### **8. Connection Management**
- Check Ollama connection on startup
- Display status indicator: ● Connected (green), ● Disconnected (red)
- API endpoint: http://localhost:11434
- Timeout: 2 seconds for checks, 120 seconds for generation
- Graceful error handling

---

## 🔧 Technical Specifications

### **Dependencies**
```python
requests==2.31.0   # API calls
Pillow==10.1.0     # Image processing
# Built-in: tkinter, threading, pickle, datetime, base64
```

### **File Structure**
```python
chatbot.py              # Main application
test_chatbot.py         # Unit tests
chat_sessions.pkl       # Persistent storage (auto-created)
requirements.txt        # Dependencies
README.md              # Documentation
TESTING.md             # Testing guide
```

### **Main Classes**

#### **ChatSession Class**
```python
class ChatSession:
    - id: str (timestamp or custom)
    - name: str (chat title)
    - messages: list (conversation history)
    - created_at: datetime
    - updated_at: datetime
    - to_dict() method for serialization
```

#### **Main App Class**
```python
class OllamaChatbot:
    # Initialization
    - __init__(root): Setup window, colors, variables
    
    # GUI Creation
    - setup_gui(): Main layout
    - create_ticker(): Fun facts banner
    - create_sidebar(): Chat list and navigation
    - create_chat_display(): Message area
    - create_input_area(): Text input and buttons
    - create_compact_settings(): Model/temp controls
    
    # Chat Management
    - new_chat(): Create new conversation
    - load_chat(id): Switch to existing chat
    - delete_chat(id): Remove chat
    - save_sessions(): Persist to disk
    - load_sessions(): Load from disk
    - refresh_chat_list(): Update sidebar
    
    # Messaging
    - send_message(): Process user input
    - get_bot_response(): API call in thread
    - display_message(text, sender): Show in UI
    - display_chat_history(): Load previous messages
    
    # File/Image Handling
    - attach_file(): File dialog and read
    - attach_image(): Image dialog and encode
    - clear_attachments(): Remove all
    - update_attachment_display(): Show preview
    
    # Utilities
    - animate_ticker(): Rotate fun facts
    - check_ollama_connection(): Test API
    - export_chat(): Save to text file
    - on_enter_key(): Handle keyboard input
```

### **API Integration**
```python
# Ollama Chat API
POST http://localhost:11434/api/chat

Request:
{
    "model": "llama2",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi!"}
    ],
    "images": ["base64_encoded_image"],  # Optional, for llava
    "stream": false,
    "options": {
        "temperature": 0.7
    }
}

Response:
{
    "message": {
        "role": "assistant",
        "content": "Response text"
    },
    "done": true
}
```

### **Threading Model**
- Main thread: GUI event loop
- Worker threads: API calls, file operations
- Use `root.after()` for thread-safe GUI updates
- Disable send button during generation
- Show loading indicator ("...")

### **Error Handling**
```python
# Connection errors
try:
    response = requests.post(...)
except requests.ConnectionError:
    display_message("Ollama not running", "system")
except requests.Timeout:
    display_message("Request timed out", "system")
except Exception as e:
    display_message(f"Error: {str(e)}", "system")

# File errors
try:
    with open(file, 'r') as f:
        content = f.read()
except PermissionError:
    messagebox.showerror("Error", "Permission denied")
except UnicodeDecodeError:
    # Fallback to binary read
```

---

## 🧪 Testing Requirements

### **Test Coverage**
- Minimum 75% code coverage
- Test all major features
- Use unittest framework
- Mock external dependencies

### **Test Categories**
```python
# Unit Tests
- Initialization and configuration
- GUI component creation
- Model/temperature controls
- Message display
- Chat session management

# Integration Tests
- Full message flow
- File/image attachment
- Chat switching
- Export functionality

# Mock Requirements
- requests.get/post for API calls
- filedialog for file selection
- messagebox for dialogs
- open() for file operations
```

### **Test File**
```python
test_chatbot.py
- TestChatSession: Session class tests
- TestChatbot: Main app tests
- TestFileHandling: File/image tests
- TestChatHistory: History management tests
- TestFunFacts: Ticker tests
```

---

## 📚 Documentation Requirements

### **README.md**
- Project overview
- Features list with screenshots placeholders
- Installation instructions (uv preferred)
- Quick start guide
- Usage examples
- Configuration options
- Troubleshooting section
- License (MIT)

### **TESTING.md**
- How to run tests
- Test coverage explanation
- Adding new tests
- CI/CD integration

### **Code Documentation**
- Docstrings for all classes and methods
- Inline comments for complex logic
- Type hints where appropriate

---

## 🎯 Key Implementation Details

### **Sidebar Chat List**
```python
# Each chat item:
- Frame with chat name (truncated to 30 chars)
- Highlight active chat with different background
- Hover effect on non-active chats
- Delete button (🗑) appears on hover
- Click to switch, confirm before delete
```

### **Message Display**
```python
# Format:
[HH:MM] Sender:
Message content with proper wrapping

# Tags:
user: Light gray bg, dark text
bot: White bg, dark text
system: Center-aligned, italic
timestamp: Small, gray text
```

### **Persistent Storage**
```python
# chat_sessions.pkl structure:
[
    {
        'id': '20251101_120000',
        'name': 'Hello world conversation',
        'messages': [
            {'role': 'user', 'content': 'Hello'},
            {'role': 'assistant', 'content': 'Hi!'}
        ],
        'created_at': '2025-11-01T12:00:00',
        'updated_at': '2025-11-01T12:05:00'
    },
    # ... more sessions
]
```

### **File Attachment Flow**
```python
1. User clicks "📁 File"
2. File dialog opens
3. Read file (max 5000 chars)
4. Add to attached_files list
5. Update preview display
6. On send:
   - Embed content in message
   - Clear attachments
   - Send to AI
```

### **Image Attachment Flow**
```python
1. User clicks "🖼 Image"
2. Image dialog opens
3. Read file as binary
4. Base64 encode
5. Add to attached_images list
6. Suggest llava model if not active
7. On send:
   - Add images to API payload
   - Clear attachments
   - Send to vision model
```

---

## 🚀 Startup Sequence

```python
1. Initialize Tkinter window
2. Set colors and configuration
3. Initialize empty chat sessions list
4. Create GUI components:
   - Ticker
   - Sidebar
   - Chat display
   - Input area
   - Settings
5. Load saved sessions from disk
6. Create new chat if none exist
7. Start ticker animation
8. Check Ollama connection
9. Enter main event loop
```

---

## ⚡ Performance Requirements

- Startup time: < 3 seconds
- Chat switching: < 500ms
- Message display: < 100ms
- File loading: < 2 seconds
- Image encoding: < 3 seconds
- Memory usage: < 100MB (without Ollama)

---

## 🔒 Security & Privacy

- All processing is local
- No external API calls except localhost
- No telemetry or tracking
- Chat data stored locally only
- File permissions respected
- No cloud dependencies

---

## 📦 Deliverables

### **Required Files**
1. `chatbot.py` - Main application (~850 lines)
2. `test_chatbot.py` - Unit tests (~300 lines)
3. `requirements.txt` - Dependencies
4. `README.md` - User documentation
5. `TESTING.md` - Testing guide
6. `.gitignore` - Git exclusions
7. `LICENSE` - MIT License
8. `pyproject.toml` - Package metadata

### **Generated Files**
- `chat_sessions.pkl` - Auto-created on first run
- `chat_export_*.txt` - Created when exporting
- Screenshots for README (user-provided)

---

## 🎨 Advanced Features (Optional Enhancements)

If time permits, add:
- Streaming responses (word-by-word)
- Dark/light theme toggle
- Search across chats
- Chat folders/categories
- Keyboard shortcuts panel
- System tray integration
- Auto-save drafts
- Message editing
- Conversation branching

---

## ✅ Acceptance Criteria

### **Functional**
- [ ] App starts without errors
- [ ] Can create and switch between chats
- [ ] Can send messages and receive responses
- [ ] Can attach files and images
- [ ] Can change models and temperature
- [ ] Chats persist between sessions
- [ ] Fun facts rotate every 5 seconds
- [ ] Can export chats
- [ ] Connection status displays correctly

### **Technical**
- [ ] No linter errors
- [ ] 75%+ test coverage
- [ ] All tests pass
- [ ] Thread-safe operations
- [ ] Proper error handling
- [ ] Clean code structure

### **UX**
- [ ] Responsive interface
- [ ] No UI blocking
- [ ] Clear visual feedback
- [ ] Intuitive navigation
- [ ] Professional appearance

---

## 🎯 Success Metrics

- Window opens in < 3 seconds
- Tests run in < 10 seconds
- All tests pass (60+ tests)
- Code is under 1000 lines
- Documentation is comprehensive
- Users can start chatting immediately
- No crashes during normal operation

---

## 📖 Example Usage Scenarios

### **Scenario 1: Simple Chat**
```
1. User opens app
2. Types "What is Python?"
3. Presses Enter
4. AI responds with explanation
5. Chat auto-named "What is Python?"
```

### **Scenario 2: Code Review**
```
1. User clicks "+ New Chat"
2. Clicks "📁 File"
3. Selects script.py
4. Types "Review this code"
5. Sends message
6. AI analyzes and provides feedback
```

### **Scenario 3: Image Analysis**
```
1. User switches model to "llava"
2. Clicks "🖼 Image"
3. Selects photo.jpg
4. Types "What's in this image?"
5. AI describes the image
```

### **Scenario 4: Multiple Chats**
```
1. User has 5 active chats
2. Clicks "Python Help" in sidebar
3. Previous Python conversation loads
4. Continues discussion
5. Switches to "Travel Plans" chat
6. Different context loaded instantly
```

---

## 🎓 Implementation Tips

1. **Start with GUI** - Get layout working first
2. **Mock API initially** - Don't need Ollama to build UI
3. **Test incrementally** - Add tests as you build
4. **Use threading carefully** - Always use root.after()
5. **Handle errors gracefully** - Show user-friendly messages
6. **Keep it simple** - Don't over-engineer
7. **Follow conventions** - PEP 8 style guide
8. **Document as you go** - Docstrings and comments

---

## 🏆 Final Notes

This specification represents a complete, production-ready desktop chatbot application. The implementation should prioritize:

1. **User Experience** - Clean, intuitive, responsive
2. **Reliability** - Proper error handling, testing
3. **Performance** - Fast startup, smooth interactions
4. **Maintainability** - Clean code, good documentation
5. **Extensibility** - Easy to add features

The result should be a professional application that rivals commercial chatbot interfaces while maintaining complete local privacy and control.

---

**Target Stats:**
- Lines of Code: ~850
- Lines of Tests: ~300
- Lines of Docs: ~500
- Total Tests: 60+
- Test Coverage: 75-80%
- Window Size: 1400x900
- Startup Time: < 3 seconds
- Dependencies: 2 (requests, Pillow)

**End Result:** A professional, ChatGPT-inspired chatbot with full chat history, file/image support, and engaging fun facts ticker - all running locally with Ollama!

---

*This prompt contains everything needed to rebuild the entire project from scratch.*

**Version**: 3.0.0  
**Last Updated**: November 1, 2025  
**License**: MIT

