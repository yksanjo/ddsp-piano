# Contributing to DDSP-Piano

Thank you for your interest in contributing to DDSP-Piano! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

Before creating a bug report, please check if the issue has already been reported:
1. Check existing [Issues](https://github.com/yksanjo/ddsp-piano/issues)
2. If it doesn't exist, create a new issue using the bug report template

When reporting bugs, please include:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs. actual behavior
- Environment details (OS, Python version, etc.)
- Relevant error messages or logs
- Any relevant code snippets

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:
1. Check existing issues to avoid duplicates
2. Use the feature request template
3. Clearly describe the enhancement and its benefits
4. Provide examples of how it would be used

### Pull Requests

1. **Fork the repository** and create a branch from `main` or `master`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the code style guidelines (see below)
   - Add tests if applicable
   - Update documentation as needed

3. **Test your changes**
   - Run existing tests: `pytest` (if available)
   - Test manually with sample data
   - Ensure no new warnings or errors

4. **Commit your changes**
   - Write clear, descriptive commit messages
   - Reference related issues: `Fixes #123` or `Closes #456`

5. **Push and create a Pull Request**
   - Push to your fork
   - Create a PR with a clear description
   - Reference any related issues

## Development Setup

### For DDSP-Piano (Main Project)

```bash
# Clone the repository
git clone https://github.com/yksanjo/ddsp-piano.git
cd ddsp-piano

# Install dependencies
pip install --upgrade ddsp==3.7.0

# Install development dependencies
pip install pytest black flake8 isort mypy
```

### For TypeScript/Node.js Projects

```bash
# Navigate to project directory
cd <project-name>/backend  # or frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## Code Style Guidelines

### Python

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints where appropriate
- Maximum line length: 127 characters
- Use `black` for code formatting
- Use `isort` for import sorting
- Run `flake8` before committing

```bash
# Format code
black .

# Sort imports
isort .

# Check style
flake8 .
```

### TypeScript/JavaScript

- Follow the existing code style in each project
- Use TypeScript for new code
- Run `npm run lint` before committing
- Use meaningful variable and function names

## Project Structure

This repository contains the DDSP-Piano project:

- **`ddsp_piano/`** - Main DDSP-Piano Python package
- **`audio_visualizer/`** - Web-based audio visualizer for DDSP-Piano
- **`assets/`** - Project assets (diagrams, images, CSV files)
- **`ddsp_piano/configs/`** - Model configuration files
- **`ddsp_piano/model_weights/`** - Pre-trained model weights
- **`ddsp_piano/modules/`** - Core synthesis modules

The project includes:
- `README.md` - Project-specific documentation
- `requirements.txt` or `package.json` - Dependencies
- `.gitignore` - Project-specific ignore rules

## Testing

### Python Projects

```bash
# Run tests (if available)
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

### TypeScript Projects

```bash
# Run tests
npm test

# Type check
npm run build
```

## Documentation

- Update README.md if you add new features
- Add docstrings to new functions/classes
- Update API documentation if applicable
- Include examples in your PR description

## Commit Message Guidelines

Write clear, descriptive commit messages:

```
Short summary (50 chars or less)

More detailed explanation if needed. Wrap at 72 characters.
Explain what and why vs. how.

- Bullet points are okay too
- Reference issues: Fixes #123
```

## Review Process

1. All PRs require at least one review
2. Maintainers will review for:
   - Code quality and style
   - Test coverage
   - Documentation updates
   - Backward compatibility
3. Address review comments promptly
4. Once approved, maintainers will merge

## Questions?

- Open an issue for questions or discussions
- Check existing documentation first
- Be respectful and patient with maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (Apache 2.0).

Thank you for contributing! 🎉
