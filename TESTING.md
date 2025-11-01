# 🧪 Testing Guide

## Overview

This project includes comprehensive unit tests for all three versions of the chatbot.

---

## 📋 Test Files

- **`test_chatbot_v1.py`** - Tests for v1.0 (text-only chatbot)
- **`test_chatbot_v2.py`** - Tests for v2.0 (file/image support)
- **`test_chatbot_v3.py`** - Tests for v3.0 (chat history & UI)

---

## 🚀 Running Tests

### Run All Tests (Recommended)

```bash
# Make script executable (first time only)
chmod +x run_tests.sh

# Run all tests
./run_tests.sh
```

### Run Individual Tests

```bash
# Test v1.0
python3 test_chatbot_v1.py

# Test v2.0
python3 test_chatbot_v2.py

# Test v3.0
python3 test_chatbot_v3.py
```

### Run with Verbose Output

```bash
python3 -m unittest test_chatbot_v1 -v
python3 -m unittest test_chatbot_v2 -v
python3 -m unittest test_chatbot_v3 -v
```

---

## 📊 Test Coverage

### v1.0 Tests (test_chatbot_v1.py)

**Basic Tests:**
- ✅ Initialization
- ✅ Color scheme
- ✅ Model selection
- ✅ Temperature control
- ✅ GUI components
- ✅ Message display
- ✅ Chat clearing
- ✅ Status updates

**Integration Tests:**
- ✅ Ollama connection check
- ✅ Message flow
- ✅ GUI layout integrity

**Total**: ~20 tests

### v2.0 Tests (test_chatbot_v2.py)

**File Tests:**
- ✅ File attachment
- ✅ File dialog cancellation
- ✅ Multiple file attachments
- ✅ File content reading

**Image Tests:**
- ✅ Image attachment
- ✅ Image encoding
- ✅ Multiple image attachments
- ✅ llava model availability

**Attachment Tests:**
- ✅ Clear attachments
- ✅ Preview updates

**Total**: ~15 tests

### v3.0 Tests (test_chatbot_v3.py)

**Chat Session Tests:**
- ✅ Session creation
- ✅ Session serialization
- ✅ Custom IDs

**History Tests:**
- ✅ New chat creation
- ✅ Chat switching
- ✅ Chat deletion
- ✅ Save/load sessions
- ✅ Display history

**Fun Facts Tests:**
- ✅ Facts loaded
- ✅ Ticker animation
- ✅ Diverse topics
- ✅ All facts displayable

**UI Tests:**
- ✅ Sidebar exists
- ✅ Ticker label
- ✅ Chat list refresh

**Total**: ~25 tests

---

## 🎯 Test Categories

### Unit Tests
Test individual components in isolation

### Integration Tests
Test multiple components working together

### UI Tests
Test GUI components (with hidden windows)

---

## 📝 Test Output

### Successful Run

```
Running Ollama Chatbot v1.0 Tests...
============================================================
test_initialization ... ok
test_color_scheme ... ok
test_model_variable ... ok
...
------------------------------------------------------------
Ran 20 tests in 2.341s

OK
Tests run: 20
Successes: 20
Failures: 0
Errors: 0
```

### Failed Run

```
Running Ollama Chatbot v1.0 Tests...
============================================================
test_initialization ... ok
test_color_scheme ... FAIL
...
------------------------------------------------------------
FAIL: test_color_scheme
AssertionError: 'accent' not in colors
```

---

## 🔧 Test Requirements

### Python Packages

```bash
# Standard library only - no additional packages needed!
# Tests use:
# - unittest (built-in)
# - unittest.mock (built-in)
# - tkinter (built-in)
```

### System Requirements

- Python 3.8+
- Display server (for GUI tests)
  - macOS/Linux: Usually available
  - Headless: May need Xvfb

---

## 💡 Writing New Tests

### Test Structure

```python
import unittest
import tkinter as tk
from chatbot import OllamaChatbot

class TestMyFeature(unittest.TestCase):
    def setUp(self):
        """Run before each test"""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window
        self.app = OllamaChatbot(self.root)
    
    def tearDown(self):
        """Run after each test"""
        try:
            self.root.destroy()
        except:
            pass
    
    def test_my_feature(self):
        """Test description"""
        # Arrange
        expected = "value"
        
        # Act
        result = self.app.some_method()
        
        # Assert
        self.assertEqual(result, expected)
```

### Best Practices

1. **Use descriptive test names**
   ```python
   def test_chat_history_saves_correctly(self):
   ```

2. **Test one thing per test**
   ```python
   # Good
   def test_model_changes(self):
       self.app.current_model.set("mistral")
       self.assertEqual(self.app.current_model.get(), "mistral")
   
   # Avoid
   def test_everything(self):
       # Testing model, temperature, and display...
   ```

3. **Use mocks for external dependencies**
   ```python
   @patch('requests.get')
   def test_api_call(self, mock_get):
       mock_get.return_value = Mock(status_code=200)
   ```

4. **Clean up resources**
   ```python
   def tearDown(self):
       self.root.destroy()
       if os.path.exists("test.pkl"):
           os.remove("test.pkl")
   ```

---

## 🐛 Troubleshooting Tests

### "Display not found" Error

**macOS/Linux:**
```bash
# Tests need a display server
# Usually works out of the box
```

**Headless Server:**
```bash
# Install Xvfb
sudo apt-get install xvfb

# Run with virtual display
xvfb-run python3 test_chatbot_v1.py
```

### "Module not found" Error

```bash
# Make sure you're in the right directory
cd /Users/bvolovelsky/Desktop/LLM

# Python should find modules in current directory
python3 test_chatbot_v1.py
```

### GUI Tests Hang

```bash
# Make sure windows are hidden
self.root.withdraw()  # Add this to setUp()
```

### File Permission Errors

```bash
# Clean up test artifacts
rm -f chat_sessions.pkl
rm -f test_*.txt
```

---

## 📊 Coverage Report

To see test coverage:

```bash
# Install coverage tool
pip3 install coverage

# Run with coverage
coverage run -m unittest test_chatbot_v1
coverage report

# HTML report
coverage html
open htmlcov/index.html
```

---

## 🎯 Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: |
          python3 test_chatbot_v1.py
          python3 test_chatbot_v2.py
          python3 test_chatbot_v3.py
```

---

## 📝 Test Checklist

Before committing:

- [ ] All tests pass
- [ ] New features have tests
- [ ] Tests are documented
- [ ] No test files in .gitignore
- [ ] Test data cleaned up

---

## 🎓 Test Philosophy

**Goals:**
- Catch bugs early
- Document behavior
- Enable refactoring
- Build confidence

**What to Test:**
- Public methods
- Edge cases
- Error handling
- Integration points

**What NOT to Test:**
- Private methods (usually)
- Third-party libraries
- Trivial getters/setters

---

## 📞 Need Help?

- **Failed Tests**: Check the error message
- **New Tests**: Follow examples in test files
- **Coverage**: Run coverage tool
- **CI/CD**: See GitHub Actions docs

---

## 📈 Test Statistics

| Version | Tests | Lines | Coverage |
|---------|-------|-------|----------|
| v1.0 | 20 | 200+ | ~80% |
| v2.0 | 15 | 180+ | ~75% |
| v3.0 | 25 | 250+ | ~80% |
| **Total** | **60** | **630+** | **~78%** |

---

**Happy Testing!** 🧪✨

*Last Updated: November 1, 2025*

