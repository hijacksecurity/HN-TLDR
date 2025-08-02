# Contributing to HackerNews TLDR 🤝

We love your input! We want to make contributing to HackerNews TLDR as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, track issues and feature requests, and accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. **Fork the repo** and create your branch from `main`.
2. **Add tests** if you've added code that should be tested.
3. **Update documentation** if you've changed APIs.
4. **Ensure the test suite passes** by running `./test_all.sh`.
5. **Make sure your code lints** (we use standard linting tools).
6. **Issue that pull request!**

## Local Development Setup

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- OpenAI API Key

### Quick Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/hn-tldr.git
cd hn-tldr

# Set up environment
cp .env.example .env
# Add your OpenAI API key to .env

# Start all services
docker-compose up --build
```

### Running Tests

```bash
# Run all tests
./test_all.sh

# Run specific service tests
cd hn-api-service && python -m pytest -v
cd summarization-service && python -m pytest -v
cd backend-api && python -m pytest -v
cd frontend && npm test
```

### Code Structure

```
hn-tldr/
├── hn-api-service/      # HackerNews API fetching
├── summarization-service/ # OpenAI integration
├── backend-api/         # Main orchestration
├── frontend/           # React web app
└── k8s/               # Kubernetes manifests
```

## Coding Standards

### Python Services

- **Code Style**: We follow PEP 8
- **Type Hints**: Use type hints where possible
- **Async/Await**: Use async patterns for I/O operations
- **Error Handling**: Comprehensive error handling with meaningful messages
- **Testing**: Write tests for new functionality

Example:
```python
async def fetch_stories() -> List[Story]:
    """Fetch stories from HackerNews API with proper error handling."""
    try:
        # Implementation
        pass
    except Exception as e:
        logger.error(f"Failed to fetch stories: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

### Frontend (React)

- **Components**: Functional components with hooks
- **Styling**: Material-UI components and sx prop
- **State Management**: React hooks (useState, useEffect)
- **Error Handling**: User-friendly error messages
- **Testing**: React Testing Library

Example:
```jsx
function StoryCard({ story }) {
  const [loading, setLoading] = useState(false);

  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Typography variant="h6">{story.title}</Typography>
        <Typography variant="body2">{story.summary}</Typography>
      </CardContent>
    </Card>
  );
}
```

### Kubernetes

- **Resource Names**: Use kebab-case
- **Labels**: Consistent labeling strategy
- **Security**: No hardcoded secrets
- **Documentation**: Comment complex configurations

## Issue and Bug Reports

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/yourusername/hn-tldr/issues).

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Feature Requests

We welcome feature requests! Please:

1. **Check existing issues** to avoid duplicates
2. **Provide context** about the problem you're trying to solve
3. **Describe the solution** you'd like to see
4. **Consider the scope** - start with smaller, focused features

## Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add OpenAI streaming responses
fix: handle missing story URLs gracefully
docs: update deployment instructions
test: add integration tests for summarization
```

Types:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `style`: Code style changes
- `chore`: Build process or auxiliary tool changes

## Security

### Reporting Security Issues

Please DO NOT file a public issue. Instead, send your report privately to [security@yourproject.com](mailto:security@yourproject.com).

### Security Guidelines

- Never commit API keys or secrets
- Use environment variables for configuration
- Validate all inputs
- Use HTTPS in production
- Regular dependency updates

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Getting Help

- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/hn-tldr/discussions)
- 📧 **Email**: [contributors@yourproject.com](mailto:contributors@yourproject.com)
- 📖 **Documentation**: Check our comprehensive README

## Recognition

Contributors will be recognized in our README and release notes. We appreciate every contribution, no matter how small!

## Code of Conduct

### Our Pledge

We pledge to make participation in our community a harassment-free experience for everyone.

### Our Standards

- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

### Enforcement

Report any behavior that violates this code of conduct to [conduct@yourproject.com](mailto:conduct@yourproject.com).

---

Thank you for contributing to HackerNews TLDR! 🎉
