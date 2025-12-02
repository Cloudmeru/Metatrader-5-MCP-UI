# Contributing to MT5 Trading Assistant

Thank you for your interest in contributing to MT5 Trading Assistant! This guide will help you get started.

## 🚀 Quick Start

1. **Fork the repository**
   ```bash
   git clone https://github.com/Cloudmeru/mt5-mcp-ui.git
   cd mt5-mcp-ui
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Copy environment template**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the application**
   ```bash
   python -m mt5_mcp_ui
   ```

## 🧪 Development

### Code Style

We use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
# Format code
ruff format .

# Check for issues
ruff check .

# Auto-fix issues
ruff check --fix .
```

### Project Structure

```
mt5-mcp-ui/
├── src/mt5_mcp_ui/
│   ├── __init__.py
│   ├── __main__.py       # CLI entry point
│   └── app.py            # Main Gradio application
├── docs/                 # Documentation
├── .env.example          # Environment template
├── pyproject.toml        # Project configuration
└── README.md
```

### Running Tests

Currently, the project focuses on integration testing with real MT5 connections. If you add unit tests:

```bash
pytest tests/
```

## 🐛 Reporting Bugs

Found a bug? Please [open an issue](https://github.com/Cloudmeru/mt5-mcp-ui/issues/new) with:

- **Description**: What happened vs. what you expected
- **Steps to reproduce**: Minimal steps to trigger the bug
- **Environment**: OS, Python version, MT5 version
- **Logs**: Any error messages or stack traces

## 💡 Feature Requests

Have an idea? [Open a feature request](https://github.com/Cloudmeru/mt5-mcp-ui/issues/new) describing:

- **Use case**: What problem does it solve?
- **Proposed solution**: How should it work?
- **Alternatives**: Other approaches you considered

## 🔧 Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow existing code style
   - Add docstrings for new functions
   - Update documentation if needed

3. **Test your changes**
   ```bash
   # Run the app locally
   python -m mt5_mcp_ui
   
   # Test with different LLM providers
   # Test MCP connection
   ```

4. **Commit with clear messages**
   ```bash
   git commit -m "feat: add support for new indicator"
   git commit -m "fix: resolve chart rendering issue"
   git commit -m "docs: update README with new examples"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a PR on GitHub with:
   - Clear description of changes
   - Link to related issues
   - Screenshots/videos if UI changes

## 📝 Commit Convention

We loosely follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style/formatting
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Maintenance tasks

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

## 📚 Resources

- [MCP Protocol Docs](https://modelcontextprotocol.io)
- [Gradio Documentation](https://gradio.app)
- [mt5-mcp Package](https://pypi.org/project/mt5-mcp/)

## 📧 Questions?

- Open a [GitHub Discussion](https://github.com/Cloudmeru/mt5-mcp-ui/discussions)
- Check existing [Issues](https://github.com/Cloudmeru/mt5-mcp-ui/issues)

---

Thank you for contributing! 🎉
