# Testing Guide for Ollama Chatbot

Complete guide for running and understanding tests for all versions of the Ollama Chatbot.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Test Files](#test-files)
3. [Running Tests](#running-tests)
4. [Test Coverage](#test-coverage)
5. [Writing New Tests](#writing-new-tests)
6. [Troubleshooting](#troubleshooting)

---

## Overview

This project includes comprehensive unit tests for all three versions:
- **v1.0**: Basic chatbot functionality
- **v2.0**: File and image upload features
- **v3.2**: Multiple chat sessions and persistence

All tests use Python's built-in `unittest` framework and require no additional dependencies.

---

## Test Files

### Test Structure

```
ollama-chatbot/
├── test_chatbot_v1.py      # Tests for version 1.0
├── test_chatbot_v2.py      # Tests for version 2.0
├── test_chatbot_v3.py      # Tests for version 3.2
├── run_all_tests.py        # Test runner script
└── requirements-dev.txt    # Development dependencies
```

### Test Coverage Summary

#### Version 1.0 Tests (`test_chatbot_v1.py`)
- **Initialization**: App setup, color schemes, default values
- **UI Components**: Chat display, input box, buttons
- **Message Handling**: Display messages, clear chat
- **Ollama Connection**: Connection checking (mocked)
- **Temperature Control**: Temperature slider updates
- **Status Bar**: Status updates

**Total Tests**: ~20 test cases

#### Version 2.0 Tests (`test_chatbot_v2.py`)
- **All v1.0 Features**: Inherits v1 functionality
- **File Attachments**: Upload, clear, multiple files
- **Image Attachments**: Upload, clear, multiple images
- **Attachment Preview**: UI updates for attachments
- **Model Support**: llava model for vision
- **File Handling**: Dialog cancellation, error handling

**Total Tests**: ~15 test cases

#### Version 3.2 Tests (`test_chatbot_v3.py`)
- **All v2.0 Features**: Inherits v1 and v2 functionality
- **ChatSession Class**: Creation, naming, timestamps
- **Multiple Sessions**: Create, switch, load sessions
- **Persistence**: Save/load from pickle file
- **Chat History**: Display history, message flow
- **Fun Facts Ticker**: Display, updates
- **Blue Theme UI**: Colors, components
- **Session Management**: Non-existent chat handling

**Total Tests**: ~40 test cases

---

## Running Tests

### Prerequisites

```bash
# Install Python dependencies
pip install -r requirements.txt

# Optional: Install development dependencies
pip install -r requirements-dev.txt
```

### Quick Start

#### Run All Tests (All Versions)

```bash
python run_all_tests.py
```

#### Run Tests for Specific Version

```bash
# Version 1.0 tests only
python run_all_tests.py --version 1

# Version 2.0 tests only
python run_all_tests.py --version 2

# Version 3.2 tests only
python run_all_tests.py --version 3
```

### Individual Test Files

You can also run individual test files directly:

```bash
# Run v1 tests
python test_chatbot_v1.py

# Run v2 tests
python test_chatbot_v2.py

# Run v3 tests
python test_chatbot_v3.py
```

### Using Python's unittest Module

```bash
# Run all tests in a file with verbose output
python -m unittest test_chatbot_v3 -v

# Run specific test class
python -m unittest test_chatbot_v3.TestChatbotV3Sessions -v

# Run specific test method
python -m unittest test_chatbot_v3.TestChatbotV3Sessions.test_new_chat_creation -v

# Discover and run all tests
python -m unittest discover -v
```

---

## Test Coverage

### What's Tested

✅ **Initialization & Setup**
- App creation and configuration
- Default values and settings
- Color schemes and themes

✅ **UI Components**
- Widget creation and placement
- Button functionality
- Text input/output areas

✅ **Session Management** (v3.2)
- Creating new chat sessions
- Switching between sessions
- Loading existing sessions
- Session persistence

✅ **Message Handling**
- User message display
- Assistant message display
- Empty message handling
- Message history

✅ **File Operations** (v2.0+)
- File upload and attachment
- Image upload and attachment
- Attachment clearing
- Multiple attachments

✅ **Persistence** (v3.2)
- Saving sessions to pickle
- Loading sessions from pickle
- Handling corrupted files
- Missing file scenarios

✅ **External Connections**
- Ollama API connection checking
- Error handling for disconnection

✅ **UI Features** (v3.2)
- Fun facts ticker
- Ticker updates
- Status bar updates

---

## Writing New Tests

### Test Template

```python
import unittest
import tkinter as tk
from unittest.mock import Mock, patch
from chatbot_v3 import OllamaChatbotBlue

class TestNewFeature(unittest.TestCase):
    """Test description"""

    def setUp(self):
        """Set up test fixtures"""
        self.app = OllamaChatbotBlue()
        self.app.withdraw()  # Hide window during tests

    def tearDown(self):
        """Clean up after tests"""
        try:
            self.app.destroy()
        except:
            pass

    def test_feature_name(self):
        """Test specific functionality"""
        # Arrange
        expected = "expected_value"

        # Act
        result = self.app.some_method()

        # Assert
        self.assertEqual(result, expected)
```

### Best Practices

1. **Use setUp and tearDown**: Initialize fixtures and clean up
2. **Mock External Dependencies**: Use `@patch` for API calls
3. **Test One Thing Per Test**: Keep tests focused
4. **Use Descriptive Names**: Test names should explain what they test
5. **Handle File Cleanup**: Remove test files in tearDown

---

## Troubleshooting

### Common Issues

#### Test Hangs

**Problem**: Tkinter window blocks test execution

**Solution**: Always call `withdraw()` on Tkinter apps
```python
self.app = OllamaChatbotBlue()
self.app.withdraw()
```

#### Import Errors

**Problem**: Cannot find module

**Solution**: Run tests from project root directory
```bash
cd /path/to/ollama-chatbot
python test_chatbot_v3.py
```

---

## Quick Reference

```bash
# Run all tests
python run_all_tests.py

# Run specific version
python run_all_tests.py --version 3

# Run individual file
python test_chatbot_v3.py

# Run with verbose output
python -m unittest test_chatbot_v3 -v
```

---

**Last Updated**: November 1, 2025
