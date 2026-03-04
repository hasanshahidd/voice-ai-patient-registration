# Contributing to Voice AI Agent

Thank you for your interest in contributing! This document provides guidelines for contributing to the Voice AI Patient Registration System.

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/voice-ai-patient-registration.git
   cd voice-ai-patient-registration
   ```
3. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes**
5. **Test thoroughly**
6. **Commit with clear messages**
7. **Push and create a Pull Request**

## 📋 Development Setup

### Backend Development

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Configure your environment
uvicorn app:app --reload
```

### Frontend Development

```bash
cd frontend
python server.py
# Visit http://localhost:3000
```

### Database Setup

```bash
createdb patient_registration
psql patient_registration < database/schema.sql
psql patient_registration < database/seed.sql  # Optional test data
```

## 🎯 Contribution Guidelines

### Code Style

**Python (Backend):**
- Follow PEP 8 style guide
- Use type hints where appropriate
- Use `black` for formatting: `black app.py`
- Use `flake8` for linting: `flake8 app.py`

**JavaScript (Frontend):**
- Use consistent indentation (2 spaces)
- Use `const`/`let` instead of `var`
- Add comments for complex logic
- Keep functions small and focused

**SQL:**
- Use uppercase for SQL keywords
- Use snake_case for table and column names
- Add comments for complex queries

### Commit Messages

Follow the conventional commits format:

```
type(scope): brief description

- Detailed bullet points if needed
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(api): add patient search by date of birth
fix(webhook): handle missing phone number in Vapi payload
docs(readme): update deployment instructions
```

### Testing

- **Backend:** Write tests using pytest
  ```bash
  pytest
  ```
- **Frontend:** Test manually in browser
  - Chrome DevTools for debugging
  - Test on mobile viewport
- **Integration:** Test full flow (call → webhook → database → dashboard)

### Pull Request Process

1. **Update documentation** if adding new features
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** with your changes
5. **Write a clear PR description:**
   - What problem does this solve?
   - How was it tested?
   - Any breaking changes?
   - Screenshots (if UI changes)

## 🐛 Bug Reports

Use GitHub Issues and include:
- **Description:** Clear summary of the bug
- **Steps to Reproduce:** Numbered list
- **Expected Behavior:** What should happen
- **Actual Behavior:** What actually happens
- **Environment:** OS, Python version, browser, etc.
- **Logs:** Relevant error messages or stack traces

## 💡 Feature Requests

Use GitHub Issues and include:
- **Problem:** What problem would this solve?
- **Proposed Solution:** Your suggested approach
- **Alternatives:** Other solutions you considered
- **Use Case:** Real-world scenario where this helps

## 📁 Project Structure

```
voice-ai-agent/
├── backend/              # FastAPI server
│   ├── config/          # Database and settings
│   ├── models/          # SQLAlchemy models
│   ├── routers/         # API endpoints
│   └── schemas/         # Pydantic schemas
├── frontend/            # Static web interface
│   └── public/          # HTML/CSS/JS files
├── database/            # SQL schema and seeds
├── docs/                # Additional documentation
└── *.md                 # Project documentation
```

## 🔒 Security

If you discover a security vulnerability:
- **DO NOT** open a public issue
- Email the maintainer directly (add your email in README)
- Provide detailed steps to reproduce
- Allow time for a fix before public disclosure

## 📝 Documentation

- Add JSDoc comments for JavaScript functions
- Add docstrings (Google style) for Python functions
- Update README.md if changing setup process
- Update VAPI_SETUP.md if changing voice integration
- Keep CHANGELOG.md current

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License (or whatever license this project uses).

## 🙏 Thank You!

Every contribution, big or small, is appreciated. Whether it's:
- Fixing typos in documentation
- Reporting bugs
- Suggesting features
- Writing code
- Improving tests

You're helping make this project better! 🎉
