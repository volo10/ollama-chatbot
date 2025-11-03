# 🚀 Version 2.0 Upgrade Guide

## What's New in v2.0?

### 🎉 Major Features

#### 1. **📁 File Upload Support**
- Upload text files, code files, PDFs, and more
- AI can read and analyze file content
- Support for multiple file formats: `.txt`, `.py`, `.md`, `.json`, etc.
- Files are automatically parsed and sent to the AI

#### 2. **🖼️ Image Upload & Analysis**
- Upload images (PNG, JPG, JPEG, GIF)
- AI can "see" and analyze images using vision models
- Automatic model suggestion (llava) when uploading images
- Image preview in attachment area

#### 3. **👁️ Vision Model Integration**
- Added `llava` model support for image understanding
- AI can describe images, extract text, answer questions about visuals
- Seamless switching between text and vision models

#### 4. **📎 Attachment System**
- Visual attachment preview
- Shows all attached files and images before sending
- Easy "Clear All" to remove attachments
- File size display

---

## 🔄 How to Upgrade

### Step 1: Install New Dependencies

```bash
cd /Users/bvolovelsky/Desktop/LLM

# Install Pillow for image handling
pip install Pillow==10.1.0

# Or install all requirements
pip install -r requirements.txt
```

### Step 2: Download the Vision Model (Optional but Recommended)

```bash
# Download llava for image analysis
ollama pull llava
```

This will take 3-5 minutes (downloads ~4.5GB).

### Step 3: Run the New Version

```bash
# Run v2.0
python3 chatbot_v2.py
```

---

## 📚 How to Use New Features

### Using File Upload

1. **Click "📁 Attach File" button**
2. **Select your file** (text, code, PDF, etc.)
3. **File appears in attachment preview**
4. **Type your message** (e.g., "Summarize this file" or "Find bugs in this code")
5. **Click Send**

**Example Uses:**
- "Summarize this document"
- "Review this code for bugs"
- "Explain what this file does"
- "Convert this JSON to a table"

### Using Image Upload

1. **Click "🖼️ Attach Image" button**
2. **Select your image** (PNG, JPG, etc.)
3. **Switch to 'llava' model** (app will suggest this)
4. **Type your question** (e.g., "What's in this image?")
5. **Click Send**

**Example Uses:**
- "What do you see in this image?"
- "Describe this photo in detail"
- "Extract text from this screenshot"
- "What objects are in this picture?"
- "Explain this diagram"

### Multiple Attachments

You can attach **multiple files at once**:
- Multiple text files
- Multiple images
- Mix of files and images

Just click the attach buttons multiple times before sending.

---

## 🎯 Comparison: v1.0 vs v2.0

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Text Chat | ✅ | ✅ |
| Multiple Models | ✅ | ✅ |
| Temperature Control | ✅ | ✅ |
| System Prompts | ✅ | ✅ |
| Chat Export | ✅ | ✅ |
| **File Upload** | ❌ | ✅ **NEW** |
| **Image Upload** | ❌ | ✅ **NEW** |
| **Vision AI (llava)** | ❌ | ✅ **NEW** |
| **Attachment Preview** | ❌ | ✅ **NEW** |
| Window Size | 1000x700 | 1200x800 (larger) |

---

## 💡 Usage Examples

### Example 1: Code Review

```
1. Attach file: your_script.py
2. Message: "Review this code and suggest improvements"
3. Send
```

The AI will read your code and provide feedback!

### Example 2: Image Analysis

```
1. Switch model to: llava
2. Attach image: photo.jpg
3. Message: "Describe everything you see in this image"
4. Send
```

The AI will analyze and describe the image!

### Example 3: Document Summarization

```
1. Attach file: long_document.txt
2. Message: "Summarize the key points in bullet format"
3. Send
```

The AI will summarize your document!

### Example 4: Multiple Files

```
1. Attach file: config.json
2. Attach file: readme.md
3. Message: "Are these configuration settings correct based on the readme?"
4. Send
```

The AI will analyze both files together!

---

## 🔧 Technical Details

### New Dependencies

- **Pillow (PIL)**: For image processing
  - Used to read and encode images
  - Converts images to base64 for API

### File Handling

- Files are read with UTF-8 encoding
- Content is limited to 5000 characters per file (to prevent token limits)
- Binary files are handled with error ignore

### Image Handling

- Images are base64 encoded
- Sent directly to vision models (llava)
- No preprocessing required

### API Changes

- Messages now support `images` field for vision models
- File content is embedded in message text
- Compatible with Ollama v0.1.0+

---

## 🆚 Which Version Should I Use?

### Use v1.0 (`chatbot.py`) if:
- You only need text conversations
- You want a lighter application
- You don't need file/image analysis

### Use v2.0 (`chatbot_v2.py`) if:
- You want to analyze files and images
- You need code review capabilities
- You want image understanding
- You want the latest features

**Both versions work side-by-side!** You can keep both files and use whichever you need.

---

## 🐛 Troubleshooting

### "llava model not found"

**Solution:**
```bash
ollama pull llava
```

### "Image upload failed"

**Solution:**
- Make sure Pillow is installed: `pip install Pillow`
- Check file is a valid image format
- Try a smaller image (< 5MB)

### "File too large" or slow responses

**Solution:**
- Large files are truncated to 5000 characters
- For very large files, summarize them first
- Consider splitting large files

### PIL/Pillow import error

**Solution:**
```bash
pip uninstall PIL Pillow
pip install Pillow==10.1.0
```

---

## 📊 Performance Notes

- **File Upload**: Instant (reads files locally)
- **Image Analysis**: Slower than text (vision models are larger)
- **Model Switching**: Instant
- **Memory**: Vision models use more RAM (~8GB for llava)

---

## 🎓 Tips & Best Practices

### For File Analysis:
- Be specific in your questions
- Large files are truncated - ask for specific sections
- Works best with text-based files

### For Image Analysis:
- Use high-quality, clear images
- Ask specific questions about the image
- llava works best with natural images and screenshots
- Can extract text from images (OCR-like capability)

### For Best Results:
- Use llama2/mistral for text and code
- Use llava for images
- Adjust temperature: lower for factual, higher for creative
- Clear attachments between different topics

---

## 🔄 Rollback to v1.0

If you want to go back to v1.0:

```bash
# Just run the original file
python3 chatbot.py
```

Both versions can coexist!

---

## 🚀 Future Enhancements (Coming Soon)

Potential v3.0 features:
- [ ] PDF preview and page selection
- [ ] Video file support
- [ ] Audio file transcription
- [ ] Drag & drop file upload
- [ ] File history/library
- [ ] Batch file processing
- [ ] Export with attachments
- [ ] Cloud storage integration

---

## 📝 Changelog

### v2.0.0 (2025-10-29)
- ✅ Added file upload functionality
- ✅ Added image upload and analysis
- ✅ Added llava vision model support
- ✅ Added attachment preview system
- ✅ Enhanced UI with larger window
- ✅ Updated status bar with version info
- ✅ Added Pillow dependency for image handling
- ✅ Improved error handling for files

### v1.0.0 (2025-10-29)
- Initial release with text chat
- Multiple model support
- Temperature control
- System prompts
- Chat export

---

## 📞 Need Help?

- Check the main **README.md** for general help
- Check **DOCUMENTATION.md** for technical details
- For v2.0 specific issues, see troubleshooting above

---

**Enjoy the new features! 🎉**

*Version 2.0 | October 29, 2025*

