# ADR-003: In-Memory Storage Strategy for Phase I

## Status
Proposed

## Date
2026-01-14

## Context
We need to determine the storage approach for the Phase I Console App. The application requires a simple way to store and manage tasks during a session. The storage solution must be appropriate for a console application and align with the constraint that data does not persist across application sessions.

## Decision
We will use in-memory storage using Python Lists/Dictionaries for the Phase I Console App. This approach stores all task data in the application's memory during the session and loses all data when the application exits.

## Alternatives
- File-based storage: JSON, CSV, or pickle files for persistence
- SQLite database: Lightweight database for local storage
- External database: PostgreSQL, MySQL for more complex storage
- Cloud storage: Remote API for data persistence

## Consequences
### Positive
- Simple implementation without complex database setup
- Fast read/write operations
- No external dependencies for storage
- Aligns with the constraint of no persistence across sessions
- Appropriate for a console application prototype
- Easy to implement and test

### Negative
- Data is lost when the application exits
- Limited scalability for large datasets
- Memory usage increases with the number of tasks
- Not suitable for production applications
- Single-user only, no concurrency support

## References
- Plan: specs/2-plan/phase-1-console.md
- Research: specs/2-plan/research.md
- Data Model: specs/2-plan/data-model.md