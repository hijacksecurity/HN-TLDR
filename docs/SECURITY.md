# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of HackerNews TLDR seriously. If you believe you have found a security vulnerability, please report it to us as described below.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please send an email to security@yourproject.com. You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the requested information listed below (as much as you can provide) to help us better understand the nature and scope of the possible issue:

- Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit the issue

This information will help us triage your report more quickly.

## Security Best Practices

### For Users

1. **Environment Variables**: Never commit `.env` files or expose API keys
2. **Updates**: Keep your deployment up to date with the latest releases
3. **Network Security**: Use HTTPS in production deployments
4. **Access Control**: Implement proper access controls for your Kubernetes cluster

### For Contributors

1. **No Secrets in Code**: Never hardcode API keys, passwords, or other secrets
2. **Input Validation**: Always validate and sanitize user inputs
3. **Dependencies**: Keep dependencies up to date and scan for vulnerabilities
4. **Least Privilege**: Follow the principle of least privilege in configurations

## Security Features

### Current Implementation

- **Environment-based Configuration**: Secrets are managed through environment variables
- **Input Validation**: API inputs are validated using Pydantic models
- **CORS Configuration**: Proper CORS headers are set for frontend-backend communication
- **Container Security**: Services run as non-root users where possible

### Planned Enhancements

- **Rate Limiting**: Implement rate limiting for API endpoints
- **Authentication**: Add optional authentication for API access
- **Audit Logging**: Implement comprehensive audit logging
- **Network Policies**: Kubernetes network policies for service isolation

## Disclosure Policy

When we receive a security bug report, we will assign it to a primary handler. This person will coordinate the fix and release process, involving the following steps:

1. Confirm the problem and determine the affected versions
2. Audit code to find any potential similar problems
3. Prepare fixes for all releases still under maintenance
4. Release new versions as soon as possible

## Comments on this Policy

If you have suggestions on how this process could be improved, please submit a pull request or file an issue to discuss.
