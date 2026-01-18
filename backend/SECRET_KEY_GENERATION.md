# SECRET_KEY Generation Guide

This guide explains how to generate a secure SECRET_KEY for the Todo Evolution backend application.

## Why is SECRET_KEY Important?

The SECRET_KEY is used for signing JWT tokens in the authentication system. Using a strong, random key is crucial for security to prevent token forgery attacks.

## Current SECRET_KEY

The current SECRET_KEY is stored in the `.env` file in the backend directory and is also configured in `docker-compose.yml`.

## How to Generate a New SECRET_KEY

### Method 1: Using Python (Recommended)

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Method 2: Using OpenSSL

```bash
openssl rand -base64 32
```

### Method 3: Online Generator (Not Recommended for Production)

Use only trusted cryptographic random generators. Never use predictable values like dictionary words or personal information.

## Updating the SECRET_KEY

1. Generate a new key using one of the methods above
2. Update the `.env` file in the backend directory:
   ```
   SECRET_KEY=your-new-generated-key-here
   ```
3. Update the `SECRET_KEY` in `docker-compose.yml` if deploying with Docker
4. Restart the application to load the new key

## Security Best Practices

- Keep the SECRET_KEY confidential and never commit it to version control
- Use different keys for development, testing, and production environments
- Rotate the key periodically, especially if there's any suspicion of compromise
- Ensure the key is at least 32 characters long and randomly generated
- Don't reuse keys across different applications