# ADR-001: Layered Architecture Pattern for Phase I Console App

## Status
Proposed

## Date
2026-01-14

## Context
We need to design the architecture for the Phase I Console App that implements Task CRUD functionality. The architecture must follow Clean Architecture principles to ensure modularity and maintainability. We also need to ensure that the architecture makes it easier to transition to a web-based interface in Phase II.

## Decision
We will implement a layered architecture pattern with the following layers:
- Presentation Layer (CLI): Handles user input/output and command parsing
- Service Layer (TaskService): Contains business logic and validation
- Repository Layer (InMemoryTaskRepository): Manages data operations
- Model Layer (Task): Defines the core data structure

This follows the pattern: Presentation -> Service -> Repository, which decouples the CLI from the business logic.

## Alternatives
- Monolithic approach: All functionality in a single file/module
- MVC (Model-View-Controller) pattern: More complex for a console application
- Event-driven architecture: Over-engineered for this simple application
- Microservices: Inappropriate for a single console application

## Consequences
### Positive
- Clear separation of concerns between different aspects of the application
- Each layer can be tested independently
- Changes in one layer have minimal impact on others
- Easy to swap implementations (e.g., CLI for web interface in Phase II)
- Code is more maintainable and understandable
- Enables parallel development on different layers

### Negative
- More complex initial setup compared to monolithic approach
- Additional overhead from multiple layers
- Potential over-engineering for a simple application

## References
- Plan: specs/2-plan/phase-1-console.md
- Research: specs/2-plan/research.md
- Data Model: specs/2-plan/data-model.md