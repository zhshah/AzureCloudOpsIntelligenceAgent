# Contributing to Azure CloudOps Intelligence Agent

Thank you for considering contributing to the Azure CloudOps Intelligence Agent! This document outlines the process for contributing to this project.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Your environment (OS, Python version, Azure region, etc.)
- Screenshots if applicable

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:
- A clear description of the enhancement
- Why this enhancement would be useful
- Potential implementation approach

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the coding standards below
3. **Test your changes** thoroughly
4. **Update documentation** if needed (README.md, code comments)
5. **Submit a pull request** with a clear description of your changes

## 💻 Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused on a single responsibility

### Commit Messages

- Use clear and descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove, etc.)
- Keep the first line under 72 characters
- Add detailed description if needed in the commit body

Example:
```
Add support for Azure Government Cloud

- Added environment variable for cloud type
- Updated authentication to support sovereign clouds
- Added documentation for government cloud deployment
```

### Testing

- Test your changes locally before submitting
- Verify deployment to Azure Container Apps works
- Test with different Azure subscription configurations
- Ensure no secrets or credentials are committed

## 🔐 Security

- Never commit API keys, credentials, or sensitive data
- Always use environment variables for configuration
- Test with Managed Identity when possible
- Report security vulnerabilities privately to the maintainer

## 📋 Pull Request Checklist

Before submitting your PR, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] Documentation is updated (if applicable)
- [ ] Commit messages are clear and descriptive
- [ ] No secrets or credentials in code
- [ ] `.gitignore` updated for new files (if needed)
- [ ] PR description clearly explains the changes

## 🎯 Areas for Contribution

We especially welcome contributions in these areas:

### High Priority
- [ ] Multi-language support (Arabic, French, Spanish)
- [ ] Export functionality (PDF, Excel reports)
- [ ] Cost alerting and notifications
- [ ] Additional Azure service integrations
- [ ] Performance optimization

### Medium Priority
- [ ] Custom dashboard with visualizations
- [ ] Reserved Instance recommendations
- [ ] Anomaly detection for cost spikes
- [ ] Integration with ticketing systems (ServiceNow, Jira)

### Documentation
- [ ] Video tutorials
- [ ] Architecture diagrams
- [ ] Deployment scenarios and use cases
- [ ] Troubleshooting guides

## 📝 Code Review Process

1. Maintainers will review your PR within 5 business days
2. Feedback will be provided as comments on the PR
3. Make requested changes and push updates to your branch
4. Once approved, maintainers will merge your PR
5. Your contribution will be acknowledged in the project

## 🏆 Recognition

All contributors will be:
- Listed in the project's contributors section
- Acknowledged in release notes
- Credited in documentation (with permission)

## ❓ Questions?

If you have questions about contributing:
- Check existing issues and pull requests
- Create a new issue with the "question" label
- Contact the maintainer directly

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Examples of behavior that contributes to a positive environment:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Examples of unacceptable behavior:**
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project maintainer. All complaints will be reviewed and investigated promptly and fairly.

## 📞 Contact

**Zahir Hussain Shah**  
Solution Architect - Azure AI & Cloud Optimization

- GitHub: [@zhshah](https://github.com/zhshah)
- Email: [Your Email]

---

Thank you for contributing to Azure CloudOps Intelligence Agent! 🚀
