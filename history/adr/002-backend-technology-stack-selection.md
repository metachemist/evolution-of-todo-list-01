# ADR-002: Backend Technology Stack Selection

**Status**: Proposed
**Date**: 2026-01-16

## Context

For Phase II of the Todo Evolution project, we need to select a backend technology stack that will provide a robust API for the frontend, handle authentication, and interact with the database. The backend must be efficient, secure, and follow modern API design principles.

## Decision

We will use the following integrated backend technology stack:

- **Framework**: FastAPI
- **Language**: Python 3.13+
- **ORM**: SQLModel (combining SQLAlchemy and Pydantic)
- **Authentication**: Better Auth with JWT tokens
- **Database**: Neon Serverless PostgreSQL

## Alternatives Considered

### Alternative 1: Django REST Framework + PostgreSQL
- **Pros**: Mature ecosystem, built-in admin interface, comprehensive authentication
- **Cons**: Heavier framework, less async-native, potentially slower development

### Alternative 2: Flask + SQLAlchemy + JWT
- **Pros**: Lightweight, familiar to many Python developers
- **Cons**: Less automatic documentation, fewer built-in features than FastAPI

### Alternative 3: Node.js + Express + Prisma
- **Pros**: Strong async capabilities, large ecosystem
- **Cons**: Would introduce inconsistency with Python backend, different language paradigm

## Consequences

### Positive
- FastAPI provides automatic API documentation (OpenAPI/Swagger)
- Pydantic models offer excellent data validation and serialization
- SQLModel combines the power of SQLAlchemy with Pydantic benefits
- Neon Serverless PostgreSQL offers automatic scaling and connection pooling
- Better Auth provides comprehensive authentication solution

### Negative
- Team may need to learn FastAPI-specific patterns
- SQLModel is newer than pure SQLAlchemy, potentially fewer resources for troubleshooting
- Neon pricing model may change as usage scales

## References

- specs/2-plan/phase-2-fullstack.md
- specs/1-specify/features/feature-02-web-api.md
- specs/1-specify/features/feature-03-authentication.md