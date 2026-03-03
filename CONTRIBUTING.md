# Contributing to iTerm2-Tabs

Thank you for your interest in contributing to iTerm2-Tabs! This document provides guidelines for contributing.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/iterm2-Tabs.git
   cd iterm2-Tabs
   ```
3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install development dependencies:
   ```bash
   make install-dev
   ```

## Code Style

This project uses:
- **Black** for code formatting
- **Ruff** for linting
- **mypy** for type checking
- **pytest** for testing

Before submitting a PR, please run:
```bash
make format  # Format code
make lint    # Check for issues
make test    # Run tests
```

## Commit Messages

Follow conventional commit format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Example: `feat: add support for custom themes`

## Pull Request Process

1. Create a branch from `main`: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Write tests for new functionality
4. Ensure all tests pass: `make test`
5. Commit your changes with descriptive messages
6. Push to your fork
7. Open a pull request with a clear description

## Testing

- Write unit tests for new features in `tests/`
- Run tests with `make test`
- Maintain test coverage above 80%

## Questions?

Feel free to open an issue for questions or discussion!
