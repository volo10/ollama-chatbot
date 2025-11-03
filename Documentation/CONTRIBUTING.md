# Contributing to Ollama AI Assistant

First off, thank you for considering contributing to Ollama AI Assistant! 🎉

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Adding Screenshots](#adding-screenshots)

## Code of Conduct

This project and everyone participating in it is governed by our commitment to providing a welcoming and inspiring community for all.

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Screenshots** if applicable
- **System information** (OS, Python version, Ollama version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear description** of the proposed feature
- **Use cases** - why would this be useful?
- **Possible implementation** approach (if you have ideas)

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:
- `good-first-issue` - Simple issues perfect for beginners
- `help-wanted` - Issues that need assistance

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/ollama-chatbot.git
cd ollama-chatbot
```

### 2. Set Up Environment

```bash
# Install uv if you haven't
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate it
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Install dependencies
uv pip install -r requirements.txt
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 4. Make Your Changes

- Write clear, commented code
- Follow the existing code style
- Test your changes thoroughly

### 5. Test Your Changes

```bash
# Make sure Ollama is running
ollama serve

# Run the application
python chatbot.py

# Test your changes:
# - Does the GUI work correctly?
# - Are there any errors in the console?
# - Does it work with different models?
# - Does it handle errors gracefully?
```

## Pull Request Process

### Before Submitting

1. **Update documentation** if needed
2. **Test thoroughly** on your system
3. **Update README.md** if you added features
4. **Add screenshots** for UI changes
5. **Check for linting errors**

### Submitting

1. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Open a Pull Request on GitHub

3. Fill out the PR template with:
   - Description of changes
   - Related issue number
   - Type of change (bug fix, feature, docs, etc.)
   - Screenshots (for UI changes)
   - Testing performed

4. Wait for review and address any feedback

### After Submission

- Be responsive to feedback
- Make requested changes promptly
- Be patient - reviews may take a few days
- Don't force-push after review starts (unless requested)

## Style Guidelines

### Python Code Style

Follow PEP 8 with these specifics:

```python
# Use 4 spaces for indentation (no tabs)
def example_function(param1, param2):
    """Docstring describing what the function does."""
    result = param1 + param2
    return result

# Use descriptive variable names
user_message = "Hello"  # Good
msg = "Hello"          # Avoid

# Keep lines under 100 characters when possible
# Add blank lines between logical sections
```

### Commit Messages

Write clear, descriptive commit messages:

```bash
# Good
git commit -m "Add temperature slider to settings panel"
git commit -m "Fix: Connection indicator not updating"
git commit -m "Docs: Update installation instructions"

# Less good
git commit -m "Update"
git commit -m "Fix bug"
git commit -m "Changes"
```

### Documentation

- Use clear, simple language
- Include code examples where helpful
- Keep formatting consistent
- Update relevant .md files

## Adding Screenshots

### For Documentation

If you're adding screenshots to documentation:

1. **Take high-quality screenshots**
   - Use the application at default size
   - Ensure good lighting/contrast
   - Capture relevant UI elements

2. **Name files descriptively**
   ```
   main-interface.png
   settings-panel.png
   chat-example.png
   model-selection.png
   ```

3. **Save in screenshots/ directory**
   ```bash
   screenshots/
   ├── main-interface.png
   ├── chat-example.png
   └── settings-panel.png
   ```

4. **Optimize file sizes**
   - PNG for UI screenshots
   - Keep under 1MB if possible
   - Use compression tools if needed

5. **Update README.md**
   ```markdown
   ![Description](screenshots/filename.png)
   *Caption explaining the screenshot*
   ```

### Screenshot Checklist

For UI-related PRs, include screenshots showing:
- [ ] Before (if changing existing feature)
- [ ] After (your changes)
- [ ] Different states (hover, active, etc.)
- [ ] Error states (if applicable)

## Feature Additions

### GUI Features

When adding GUI features:

1. **Follow existing color scheme**
   - Use colors from `self.colors` dictionary
   - Maintain dark theme aesthetic
   - Add hover effects for interactive elements

2. **Ensure thread safety**
   - Use `root.after()` for GUI updates from threads
   - Never block the main thread

3. **Add status indicators**
   - Show when operations are in progress
   - Provide user feedback

4. **Handle errors gracefully**
   - Show user-friendly error messages
   - Log technical details to console

### API Features

When working with Ollama API:

1. **Add timeout handling**
2. **Handle connection errors**
3. **Validate responses**
4. **Update documentation**

## Testing Guidelines

### Manual Testing Checklist

- [ ] Application starts without errors
- [ ] All buttons work correctly
- [ ] Settings persist during session
- [ ] Error messages display properly
- [ ] Chat export works
- [ ] Connection indicator updates
- [ ] Different models can be selected
- [ ] Temperature changes affect responses
- [ ] System prompt customization works

### System Testing

Test on different systems if possible:
- macOS
- Linux
- Windows

## Questions?

Feel free to:
- Open an issue for questions
- Join discussions in existing issues
- Reach out to maintainers

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes (for significant contributions)
- Project documentation

---

**Thank you for contributing! 🙏**

Every contribution, no matter how small, helps make this project better for everyone.

