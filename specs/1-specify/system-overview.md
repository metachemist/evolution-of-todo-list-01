# System Overview: Evolution of Todo

**Branch**: `1-evolution-of-todo` | **Date**: 2026-01-16 | **Spec**: specs/1-specify/system-overview.md

## Vision: "Evolution of Todo" from CLI to Cloud

The "Evolution of Todo" project represents a progressive journey from a simple console-based task management application to a sophisticated, cloud-native AI-powered system. This evolution follows a phased approach, with each phase building upon the previous one to create a robust, scalable, and intelligent todo management platform.

## Phase I Scope (Completed)

### In-Scope
- CLI Interface for task management
- CRUD operations (Add, Delete, Update, View, Mark Complete)
- In-memory session storage
- Console-based user interactions

### Out-of-Scope (Non-Goals)
- Persistent database storage
- Web UI or graphical interface
- User authentication
- Multi-user support
- Network connectivity

## Phase II Scope (Current)

### In-Scope
- Full-stack web application with Next.js frontend
- RESTful API with FastAPI backend
- User authentication (signup/signin) with Better Auth + JWT
- Persistent storage with Neon Serverless PostgreSQL
- Multi-user support with data isolation
- Responsive UI for desktop and mobile

### Out-of-Scope (Non-Goals)
- AI chatbot interface (Phase III)
- Natural language processing (Phase III)
- Kubernetes deployment (Phase IV)
- Advanced features: priorities, tags, search, filters (Phase V)
- Event streaming with Kafka (Phase V)

## Success Metrics (SMART)

### Phase I Metrics (Completed)
- **Startup time < 1 second**: The application must initialize and be ready for user input within 1 second
- **Zero crashes on invalid input**: The system must handle incorrect input types (integers vs strings) gracefully without crashing
- **100% test coverage for business logic**: All core functionality must be covered by automated tests

### Phase II Metrics (Current)
- **API response times**: CREATE < 200ms, READ < 100ms, UPDATE < 150ms, DELETE < 100ms (95th percentile)
- **User authentication**: Users can securely sign up and sign in with email/password
- **Data isolation**: Users can only access their own tasks
- **Frontend performance**: FCP < 1.5s, LCP < 2.5s, TTI < 3.0s
- **Security**: All endpoints properly protected with JWT authentication

## Core Domain Entities

### `User` Entity (Phase II Addition)
The identity entity for multi-user support with the following attributes:
- `id`: Unique identifier for the user (UUID)
- `email`: Unique email address for login (string)
- `name`: User's display name (string)
- `password_hash`: Securely hashed password (string)
- `created_at`: Timestamp when the user account was created
- `updated_at`: Timestamp when the user account was last updated

### `Task` Entity
The central entity of the system with the following attributes:
- `id`: Unique identifier for the task (integer or UUID)
- `user_id`: Foreign key linking to the owning user (string/UUID)
- `title`: Required string representing the task name (1-200 characters)
- `description`: Optional string providing additional details about the task
- `completed`: Boolean indicating whether the task is completed (true) or pending (false)
- `created_at`: Timestamp indicating when the task was created
- `updated_at`: Timestamp indicating when the task was last updated

## Global Constraints

### Phase I Constraints (Legacy)
- **No Persistence**: The application will use in-memory storage only, with data reset on exit
- **Strictly Typed Python**: Implementation will use Python 3.13+ with type hints for all functions and variables
- **CLI Interface**: All user interactions will occur through command-line interface
- **UV Package Manager**: Dependencies will be managed using the UV package manager
- **Spec-Driven Development**: All code must be generated from specifications following the project constitution

### Phase II Constraints (Current)
- **Persistent Storage**: Data must persist across sessions using PostgreSQL database
- **Multi-User Support**: System must support multiple users with data isolation
- **Authentication Required**: All task operations require valid JWT token
- **Web-First Interface**: Primary interface is web-based with responsive design
- **Security First**: All endpoints protected with JWT authentication
- **Stateless Backend**: No server-side session storage, all state in JWT or database
- **Database Migration**: Use Alembic for schema versioning and migration
- **Type Safety**: Strict typing for both frontend (TypeScript) and backend (Python)
- **Spec-Driven Development**: All code must be generated from specifications following the project constitution

### Transition Note
Phase II replaces the in-memory repository with a PostgreSQL-based repository, transitioning from single-user console application to multi-user web application. The core task business logic remains consistent between phases.