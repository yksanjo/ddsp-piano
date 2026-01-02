# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < Latest | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability, please follow these steps:

### 1. **Do NOT** open a public issue

Security vulnerabilities should be reported privately to protect users.

### 2. Report the vulnerability

Please create a private security advisory on GitHub:
1. Go to the repository's "Security" tab
2. Click "Advisories"
3. Click "New draft security advisory"
4. Fill out the form with details about the vulnerability

### 3. Include the following information

- **Type of vulnerability** (e.g., XSS, SQL injection, authentication bypass)
- **Affected component** (which part of the codebase)
- **Steps to reproduce** (if possible)
- **Potential impact** (what could an attacker do)
- **Suggested fix** (if you have one)

### 4. Response timeline

- **Initial response**: Within 48 hours
- **Status update**: Within 7 days
- **Resolution**: Depends on severity and complexity

## Security Best Practices

### For Contributors

- Never commit secrets, API keys, or credentials
- Use environment variables for sensitive configuration
- Keep dependencies up to date
- Review code changes for security implications
- Follow secure coding practices

### For Users

- Keep your installation up to date
- Use strong, unique passwords
- Don't expose sensitive endpoints publicly
- Review and understand permissions before granting access
- Report suspicious activity immediately

## Security Considerations

### Python Projects

- Validate and sanitize all user inputs
- Use parameterized queries for database operations
- Keep dependencies updated (check with `pip list --outdated`)
- Use virtual environments to isolate dependencies
- Never commit `.env` files or credentials

### TypeScript/Node.js Projects

- Validate input with libraries like `zod` or `joi`
- Use parameterized queries for database operations
- Keep `package.json` dependencies updated
- Use environment variables for secrets
- Enable CORS only for trusted origins
- Use HTTPS in production

### General

- Review third-party dependencies regularly
- Use dependency scanning tools
- Implement rate limiting where appropriate
- Use secure authentication methods (JWT, OAuth)
- Log security events appropriately
- Follow principle of least privilege

## Known Security Issues

We maintain a list of known security issues and their resolutions. Check the [Security Advisories](https://github.com/yksanjo/ddsp-piano/security/advisories) page.

## Security Updates

Security updates will be:
- Released as patches to supported versions
- Documented in release notes
- Announced via GitHub releases
- Tagged with security labels

## Acknowledgments

We appreciate responsible disclosure. Contributors who report security vulnerabilities will be:
- Acknowledged (if desired) in security advisories
- Credited in release notes
- Thanked for helping improve the project's security

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)

Thank you for helping keep this project secure! 🔒
