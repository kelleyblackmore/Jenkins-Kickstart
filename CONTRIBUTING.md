# Contributing to Jenkins-Kickstart

Thank you for considering contributing to Jenkins-Kickstart! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:

1. **Clear title and description**
2. **Steps to reproduce** the issue
3. **Expected behavior** vs. **actual behavior**
4. **Configuration file** (if relevant, sanitize credentials)
5. **Environment information** (Python version, Jenkins version, OS)
6. **Error messages or logs**

### Suggesting Enhancements

Enhancement suggestions are welcome! Please open an issue with:

1. **Clear description** of the feature
2. **Use case** - why this feature would be useful
3. **Proposed implementation** (if you have ideas)
4. **Examples** of how it would work

### Pull Requests

We welcome pull requests! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Test your changes** thoroughly
5. **Commit your changes** (`git commit -m 'Add amazing feature'`)
6. **Push to the branch** (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

## Development Setup

### Prerequisites

- Python 3.7 or higher
- pip
- Git
- (Optional) Jenkins instance for testing

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/kelleyblackmore/Jenkins-Kickstart.git
cd Jenkins-Kickstart

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies (if any)
pip install pytest black flake8
```

### Running Tests

```bash
# Run Python syntax check
python3 -m py_compile jenkins_kickstart/*.py

# Test the CLI
jenkins-kickstart examples/minimal-config.yaml --dry-run

# Test imports
python3 -c "from jenkins_kickstart import JenkinsKickstart, ConfigParser"
```

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose
- Add comments for complex logic

### Project Structure

```
Jenkins-Kickstart/
├── jenkins_kickstart/       # Main package
│   ├── __init__.py         # Package initialization
│   ├── client.py           # Jenkins API client
│   ├── config.py           # Configuration parser
│   └── cli.py              # Command-line interface
├── examples/               # Example configurations
│   ├── minimal-config.yaml
│   ├── example-config.yaml
│   ├── example-config.json
│   └── advanced-config.yaml
├── setup.py               # Package setup
├── pyproject.toml         # Modern package setup
├── requirements.txt       # Dependencies
├── README.md             # Main documentation
├── USAGE.md              # Usage guide
├── CONTRIBUTING.md       # This file
└── LICENSE               # MIT License
```

## Making Changes

### Adding a New Feature

1. **Identify where the feature belongs:**
   - Configuration parsing → `config.py`
   - Jenkins API interaction → `client.py`
   - CLI functionality → `cli.py`

2. **Implement the feature:**
   - Write clean, documented code
   - Follow existing patterns
   - Add error handling

3. **Add examples:**
   - Update or add example configs
   - Document in README or USAGE.md

4. **Test the feature:**
   - Test with dry-run mode
   - Test with real Jenkins (if possible)
   - Test error cases

### Updating Documentation

- **README.md** - Overview and quick start
- **USAGE.md** - Detailed usage instructions
- **Examples** - Configuration examples
- **Docstrings** - In-code documentation

### Backward Compatibility

Please maintain backward compatibility when possible. If breaking changes are necessary:

1. Document the breaking change clearly
2. Provide migration instructions
3. Update version number appropriately (major version bump)

## Code Review Process

All contributions go through code review:

1. **Automated checks** run on pull requests
2. **Maintainers review** the code
3. **Feedback** is provided if changes are needed
4. **Approval** and merge once ready

## Release Process

Maintainers handle releases:

1. Update version in `setup.py` and `pyproject.toml`
2. Update `__version__` in `__init__.py`
3. Update CHANGELOG (if exists)
4. Create a git tag
5. Build and publish to PyPI

## Questions?

If you have questions about contributing:

- Open a GitHub issue with your question
- Label it as "question"
- We'll respond as soon as possible

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the project
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing others' private information
- Other unprofessional conduct

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Every contribution helps make Jenkins-Kickstart better. Thank you for your time and effort!
