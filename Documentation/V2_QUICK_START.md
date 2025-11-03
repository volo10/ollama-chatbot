# 🚀 Quick Start - Version 2.0

## What is v2.0?

Your chatbot now supports **file and image uploads**! You can:
- 📁 Upload text files, code, PDFs
- 🖼️ Upload and analyze images
- 👁️ Use AI vision to understand pictures

---

## ⚡ Quick Setup (5 minutes)

### 1. Install New Dependency

```bash
cd /Users/bvolovelsky/Desktop/LLM
pip3 install Pillow
```

### 2. Download Vision Model (Optional)

```bash
# For image analysis
ollama pull llava
```

### 3. Run v2.0

```bash
python3 chatbot_v2.py
```

That's it! 🎉

---

## 🎮 How to Use

### Upload a File:
1. Click **"📁 Attach File"**
2. Select your file
3. Type: "Summarize this file"
4. Click **Send**

### Upload an Image:
1. Click **"🖼️ Attach Image"**
2. Select your image
3. Switch model to **"llava"** (app will suggest this)
4. Type: "What's in this image?"
5. Click **Send**

---

## 💡 Cool Things to Try

### Code Review:
```
1. Attach: my_script.py
2. Ask: "Review this code and find bugs"
```

### Image Description:
```
1. Switch to: llava model
2. Attach: photo.jpg
3. Ask: "Describe this image in detail"
```

### Document Analysis:
```
1. Attach: document.txt
2. Ask: "Summarize the key points"
```

### Extract Text from Screenshot:
```
1. Switch to: llava
2. Attach: screenshot.png
3. Ask: "Extract all text from this image"
```

---

## 🆚 v1.0 vs v2.0

**v1.0** (`chatbot.py`):
- ✅ Text chat only
- ✅ Lighter and simpler

**v2.0** (`chatbot_v2.py`):
- ✅ Everything in v1.0
- ✅ File uploads
- ✅ Image uploads
- ✅ Vision AI

**Both work!** Keep both files and use whichever you need.

---

## 🐛 Troubleshooting

**Error: "llava not found"**
```bash
ollama pull llava
```

**Error: "No module named 'PIL'"**
```bash
pip3 install Pillow
```

**Slow image responses?**
- Normal! Vision models are slower
- llava needs more processing time

---

## 📸 Ready to Upload to GitHub?

See **V2_GITHUB_PUSH.md** for instructions!

---

**Happy chatting! 🎉**

