# ADR-003: Authentication and Session Management Approach

**Status**: Proposed
**Date**: 2026-01-16

## Context

For Phase II, we need to implement secure user authentication and session management for a multi-user system. Users must be able to register, sign in, and have their data properly isolated from other users. The approach must be secure against common threats like XSS and CSRF.

## Decision

We will implement authentication using:

- **Frontend Authentication**: Better Auth library for Next.js
- **Token Type**: JWT (JSON Web Tokens) with 7-day expiration
- **Token Storage**: HttpOnly cookies (not localStorage)
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Password Hashing**: bcrypt with cost factor ≥ 12
- **Session Management**: Stateless JWT tokens with automatic renewal

## Alternatives Considered

### Alternative 1: Traditional Session-Based Authentication
- **Pros**: Server-side session control, easier to invalidate sessions
- **Cons**: Requires server-side session storage, doesn't scale statelessly, more complex deployment

### Alternative 2: OAuth2 with Third-Party Providers Only
- **Pros**: Leverages trusted identity providers, reduces password management burden
- **Cons**: Doesn't meet requirement for email/password authentication, limits user control

### Alternative 3: Custom Authentication with Session Tokens
- **Pros**: Full control over implementation, potentially lighter weight
- **Cons**: More security considerations to handle, reinventing proven solutions

## Consequences

### Positive
- Stateless authentication scales horizontally without session storage
- HttpOnly cookies protect against XSS attacks
- JWT tokens contain all necessary user information without server-side lookup
- Better Auth provides comprehensive authentication features out of the box
- Standard JWT implementation allows for easy integration with other services

### Negative
- JWT tokens cannot be invalidated before expiration (without additional complexity)
- Larger payload size compared to session IDs
- Need to handle token refresh/rotation for extended sessions
- More complex error handling for expired tokens

## References

- specs/2-plan/phase-2-fullstack.md
- specs/1-specify/features/feature-03-authentication.md
- specs/1-specify/features/feature-02-web-api.md