# ADR-004: Data Architecture and Persistence Strategy

**Status**: Proposed
**Date**: 2026-01-16

## Context

For Phase II, we need to transition from the in-memory storage of Phase I to a persistent database solution. The data architecture must support multi-user functionality with proper data isolation, handle the required data models (User and Task), and provide good performance for the expected operations.

## Decision

We will implement the following data architecture:

- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel (combining SQLAlchemy and Pydantic)
- **Connection Pooling**: Built-in Neon connection pooling
- **Migration Tool**: Alembic for schema versioning
- **Relationships**: Foreign key from Task to User with CASCADE delete
- **Indexes**: On user_id, completed, created_at for performance
- **Data Isolation**: Row-level filtering by user_id in all queries

## Alternatives Considered

### Alternative 1: MongoDB with Pydantic
- **Pros**: Flexible schema, good integration with Pydantic models
- **Cons**: Less ACID guarantees, not ideal for relational data like user-task relationships

### Alternative 2: SQLite with SQLAlchemy
- **Pros**: Lightweight, file-based storage
- **Cons**: Limited scalability, not suitable for multi-user web application

### Alternative 3: Redis for Primary Storage
- **Pros**: Very fast, good for caching
- **Cons**: Not ideal for relational data, lacks ACID properties for critical operations

## Consequences

### Positive
- PostgreSQL provides strong ACID guarantees
- Neon Serverless offers automatic scaling and connection management
- SQLModel provides excellent type safety with Pydantic validation
- Foreign key constraints ensure data integrity
- Proper indexing strategy for performance
- Alembic provides reliable migration management
- Clear data isolation strategy prevents cross-user data access

### Negative
- PostgreSQL has a steeper learning curve than document databases
- More complex setup than in-memory storage
- Potential costs associated with Neon Serverless as usage grows
- Need to handle database connection management properly

## References

- specs/2-plan/phase-2-fullstack.md
- specs/1-specify/features/feature-02-web-api.md
- specs/1-specify/features/feature-03-authentication.md