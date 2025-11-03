# 🤖 Ollama AI Assistant - Version 2.0

**Professional Desktop Chatbot with File & Image Upload**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Ollama](https://img.shields.io/badge/Ollama-Required-orange.svg)
![Version](https://img.shields.io/badge/Version-2.0-brightgreen.svg)

---

## 🆕 What's New in v2.0?

### Major Features Added:

#### 📁 **File Upload Support**
- Upload text files, code files, PDFs, and more
- AI can read and analyze file content
- Support for `.txt`, `.py`, `.md`, `.json`, `.java`, `.cpp`, and many more
- Automatic file content parsing

#### 🖼️ **Image Upload & Analysis**
- Upload images (PNG, JPG, JPEG, GIF, BMP)
- AI can "see" and analyze images using vision models
- Automatic model suggestion (llava) when uploading images
- Image preview in attachment area

#### 👁️ **Vision Model Integration**
- New `llava` model support for image understanding
- AI can describe images, extract text (OCR), answer questions about visuals
- Seamless switching between text and vision models

#### 📎 **Attachment System**
- Visual attachment preview before sending
- Shows all attached files and images
- File size display
- Easy "Clear All" button to remove attachments
- Support for multiple attachments at once

---

## 🎯 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running
3. **llama2** model downloaded (for text)
4. **llava** model downloaded (for images, optional)

### Installation

```bash
# 1. Clone repository (if you haven't)
git clone https://github.com/volo10/ollama-chatbot.git
cd ollama-chatbot

# 2. Install dependencies
pip3 install requests Pillow

# 3. Download models
ollama pull llama2  # For text chat
ollama pull llava   # For image analysis (optional)

# 4. Start Ollama (if not running)
ollama serve

# 5. Run v2.0
python3 chatbot_v2.py
```

---

## 📚 Usage Examples

### Example 1: Code Review

```
1. Click "📁 Attach File"
2. Select your Python/JavaScript/Java file
3. Type: "Review this code and suggest improvements"
4. Click Send
```

The AI will read your code and provide detailed feedback!

### Example 2: Image Analysis

```
1. Switch model to "llava"
2. Click "🖼️ Attach Image"
3. Select your image file
4. Type: "Describe what you see in this image"
5. Click Send
```

The AI will analyze and describe the image!

### Example 3: Extract Text from Screenshot

```
1. Switch model to "llava"
2. Attach a screenshot with text
3. Type: "Extract all text from this image"
4. Send
```

The AI will perform OCR and extract the text!

### Example 4: Document Summarization

```
1. Attach a .txt or .md file
2. Type: "Summarize the key points in bullet format"
3. Send
```

The AI will read and summarize your document!

---

## 🆚 Version Comparison

| Feature | v1.0 | v2.0 |
|---------|:----:|:----:|
| Text Chat | ✅ | ✅ |
| Multiple Models | ✅ | ✅ |
| Temperature Control | ✅ | ✅ |
| System Prompts | ✅ | ✅ |
| Chat Export | ✅ | ✅ |
| **File Upload** | ❌ | ✅ |
| **Image Upload** | ❌ | ✅ |
| **Vision AI (llava)** | ❌ | ✅ |
| **Attachment Preview** | ❌ | ✅ |
| Window Size | 1000x700 | 1200x800 |

---

## 🎨 Features

### Core Features (v1.0)
- ✅ Beautiful dark-themed GUI
- ✅ Multiple AI models (llama2, mistral, codellama, etc.)
- ✅ Temperature control for creativity
- ✅ Custom system prompts
- ✅ Chat history management
- ✅ Export conversations
- ✅ Real-time connection status
- ✅ Thread-safe, non-blocking interface

### New Features (v2.0)
- ✅ File upload functionality
- ✅ Image upload and preview
- ✅ Vision model integration (llava)
- ✅ Attachment management system
- ✅ Enhanced UI with larger window
- ✅ Support for multiple file types
- ✅ Base64 image encoding for API

---

## 💻 System Requirements

- **OS**: macOS, Linux, or Windows
- **Python**: 3.8 or higher
- **RAM**: 8GB minimum (16GB recommended for vision models)
- **Disk**: 10GB free (for models)
- **Ollama**: Latest version

---

## 📖 Documentation

- **V2_QUICK_START.md** - Quick setup guide
- **V2_UPGRADE_GUIDE.md** - Detailed upgrade information
- **V2_GITHUB_PUSH.md** - How to push v2 to GitHub
- **V2_SUMMARY.md** - Complete v2 overview
- **DOCUMENTATION.md** - Technical documentation
- **README.md** - Original v1.0 documentation

---

## 🔧 Configuration

### Supported Models

**Text Models**:
- `llama2` - General purpose (default)
- `mistral` - High-quality responses
- `codellama` - Code generation and review
- `llama3` - Latest version
- `phi` - Smaller, faster model
- `gemma` - Google's model

**Vision Models**:
- `llava` - Image understanding and analysis

### Supported File Types

**Text Files**:
- `.txt` - Plain text
- `.md` - Markdown
- `.py` - Python
- `.js` - JavaScript
- `.java` - Java
- `.cpp` / `.c` - C/C++
- `.json` - JSON data
- `.xml` - XML data
- And many more!

**Image Files**:
- `.png` - PNG images
- `.jpg` / `.jpeg` - JPEG images
- `.gif` - GIF images
- `.bmp` - Bitmap images

---

## 🐛 Troubleshooting

### "llava model not found"
```bash
ollama pull llava
```

### "No module named 'PIL'"
```bash
pip3 install Pillow
```

### "Ollama not running"
```bash
ollama serve
```

### Slow image responses
- Normal behavior - vision models are slower than text models
- llava typically takes 10-30 seconds per image
- Be patient and wait for the response

### File upload failed
- Check file encoding (UTF-8 recommended)
- Try a smaller file
- Some binary files may not be readable

---

## 🎓 Tips & Best Practices

### For File Analysis:
- Be specific in your questions
- Large files are truncated to 5000 characters
- Works best with text-based files
- For code review, include specific concerns

### For Image Analysis:
- Use high-quality, clear images
- Ask specific questions about the image
- llava works best with natural images and screenshots
- Can extract text from images (OCR capability)
- Switch to llava model before uploading images

### For Best Results:
- Use llama2/mistral for text and code
- Use llava for images
- Adjust temperature: lower (0.3-0.5) for factual, higher (0.8-1.2) for creative
- Clear attachments between different topics
- Keep file sizes reasonable (< 5MB recommended)

---

## 🔒 Privacy & Security

- **100% Local Processing**: All AI runs on your machine
- **No Cloud Dependencies**: No data sent to external servers
- **No Tracking**: No analytics or user tracking
- **Open Source**: Full source code available
- **File Privacy**: Files are only read locally, never uploaded

---

## 📝 License

MIT License - See LICENSE file for details.

---

## 🤝 Contributing

Contributions welcome! See CONTRIBUTING.md for guidelines.

---

## 🙏 Acknowledgments

- **Ollama** - Local LLM platform
- **Python Community** - Amazing libraries
- **Meta AI** - Llama models
- **Mistral AI** - Mistral models
- **LLaVA Team** - Vision model

---

## 📞 Support

- **Documentation**: See docs folder
- **Ollama Docs**: https://ollama.ai/docs
- **GitHub Issues**: Report bugs and request features

---

## 🎯 Roadmap

### Planned Features (v3.0):
- [ ] Drag & drop file upload
- [ ] PDF page selection and preview
- [ ] Video file support
- [ ] Audio transcription
- [ ] File history library
- [ ] Batch file processing
- [ ] Cloud storage integration (optional)
- [ ] More vision models
- [ ] Real-time streaming responses

---

## 📊 Project Stats

- **Lines of Code**: 850+
- **Documentation**: 5000+ lines
- **Total Files**: 24
- **Dependencies**: 2 (requests, Pillow)
- **Models Supported**: 7+
- **File Formats**: 20+
- **License**: MIT

---

**GitHub**: https://github.com/volo10/ollama-chatbot
**Version**: 2.0.0
**Last Updated**: October 29, 2025

---

**Made with ❤️ for the AI community**

*Try v2.0 today and experience the power of file and image analysis!* 🚀

