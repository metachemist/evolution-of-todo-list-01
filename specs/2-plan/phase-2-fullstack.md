# Implementation Plan: Phase II Full-Stack Web Application

**Version**: 1.0
**Phase**: II - Full-Stack Web Application
**Status**: Draft
**Date**: 2026-01-16

## 1. Overview

### 1.1 Purpose
Transform the Phase I console application into a modern full-stack web application with persistent storage, RESTful API, and user authentication.

### 1.2 Scope
This plan defines the technical architecture for:
- Next.js 16+ frontend with App Router
- FastAPI backend with SQLModel ORM
- Better Auth integration for authentication
- Neon Serverless PostgreSQL for persistent storage
- JWT-based user session management
- Multi-user support with data isolation

### 1.3 Out of Scope
- AI chatbot interface (Phase III)
- Natural language processing (Phase III)
- Kubernetes deployment (Phase IV)
- Advanced features: priorities, tags, search, filters (Phase V)
- Event streaming with Kafka (Phase V)

### 1.4 Dependencies
- Phase I task business logic completed
- All Phase I specifications and tasks implemented
- Python 3.13+ environment
- Node.js 18+ for frontend
- UV package manager
- Neon PostgreSQL database provisioned

## 2. Technical Context

### 2.1 Architecture Pattern
**Layered Architecture** with clear separation of concerns:
- **Presentation Layer**: Next.js frontend with React components
- **API Layer**: FastAPI backend with REST endpoints
- **Service Layer**: Business logic and validation
- **Repository Layer**: Data access and persistence
- **Database Layer**: Neon Serverless PostgreSQL

### 2.2 Tech Stack
- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.13+, SQLModel
- **Authentication**: Better Auth with JWT
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel (combines SQLAlchemy and Pydantic)
- **Package Manager**: UV (Python), npm/pnpm (Node.js)
- **Testing**: pytest (backend), vitest/jest (frontend)

### 2.3 Data Flow
1. **User Interaction**: Next.js frontend handles user input
2. **Authentication**: Better Auth manages session, stores JWT in HttpOnly cookie
3. **API Request**: Frontend sends authenticated requests to FastAPI backend
4. **Business Logic**: Service layer processes requests with validation
5. **Data Access**: Repository layer handles database operations
6. **Response**: Data flows back through layers to frontend for display

### 2.4 Security Model
- **Transport**: All communication over HTTPS
- **Authentication**: JWT tokens with 7-day expiration
- **Storage**: Tokens in HttpOnly cookies (not LocalStorage)
- **Authorization**: User ID validation in API endpoints
- **Data Isolation**: All queries filtered by user_id
- **Password Security**: bcrypt hashing with cost factor ≥ 12

## 3. Constitution Check

*GATE: Must pass before implementation starts. Re-check after design completion.*

- [x] Spec-Driven Development: All code will be generated from specifications
- [x] Traceability: Every implementation will map back to specification requirements
- [x] No Manual Coding: Code will be generated via Qwen CLI based on approved tasks
- [x] Task ID Referencing: Every file will include header comment with Task ID
- [x] Clean Architecture: Following layered architecture pattern (Presentation → API → Service → Repository → Database)
- [x] Technology Stack: Using Next.js, FastAPI, SQLModel, Neon DB, Better Auth as specified
- [x] Performance: Meeting response time requirements (< 200ms for operations)

## 4. Phase 0: Research & Unknown Resolution

### 4.1 Research Tasks Identified
- **RT-001**: Determine optimal JWT algorithm (HS256 vs RS256) for Phase II
- **RT-002**: Research Better Auth configuration best practices for Next.js 16+ App Router
- **RT-003**: Investigate SQLModel relationship patterns for user-task associations
- **RT-004**: Evaluate Next.js API route patterns for FastAPI backend integration

### 4.2 Decision Log

#### Decision: JWT Algorithm Selection
- **Chosen**: HS256 (HMAC with SHA-256)
- **Rationale**: Simpler implementation with shared secret, sufficient security for this application size
- **Alternative Considered**: RS256 (RSA with SHA-256) - more complex key management
- **Impact**: Affects both frontend and backend JWT configuration

#### Decision: Frontend State Management
- **Chosen**: Better Auth hooks for session management + React state for UI interactions
- **Rationale**: Better Auth provides comprehensive session management, React handles UI state
- **Alternative Considered**: Custom JWT management in localStorage - less secure
- **Impact**: Security posture and session handling consistency

#### Decision: Database Connection Pooling
- **Chosen**: SQLModel with connection pooling via SQLAlchemy engine settings
- **Rationale**: Standard approach for FastAPI+SQLModel applications
- **Settings**: Pool size 10-20, max overflow 30, pool timeout 30s
- **Impact**: Performance under load and resource efficiency

## 5. Phase 1: Design Artifacts

### 5.1 Data Model Design

#### Entity: User
```python
class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(sa_column=Column(String(254), unique=True, nullable=False))
    name: str = Field(sa_column=Column(String(100), nullable=False))
    password_hash: str = Field(sa_column=Column(String, nullable=False))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")
```

#### Entity: Task
```python
class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    title: str = Field(sa_column=Column(String(200), nullable=False))
    description: Optional[str] = Field(sa_column=Column(String(1000)))
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: User = Relationship(back_populates="tasks")
```

#### Entity: TaskUpdate (for partial updates)
```python
class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, sa_column=Column(String(200)))
    description: Optional[str] = Field(default=None, sa_column=Column(String(1000)))
    completed: Optional[bool] = None
```

#### Entity: PaginatedResponse (Generic model for pagination)
```python
from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    pagination: dict = {
        "page": int,
        "limit": int,
        "total": int,
        "pages": int
    }
```

### 5.2 Database Migration Strategy

#### Initial Setup
- Command: `alembic init -t async backend/src/migrations`
- Configure alembic.ini with async PostgreSQL driver
- Set up migration directory structure

#### First Migration
- Generate initial schema: `alembic revision --autogenerate -m "initial_schema"`
- Verify generated migration before applying
- Apply migration: `alembic upgrade head`

#### Phase I Transition
- Since Phase I used in-memory storage, no data migration is required
- This is a fresh schema with no legacy data to migrate
- All users and tasks start from empty database

### 5.3 API Contract Design

#### Authentication Endpoints
- `POST /api/auth/signup` - Create user account
- `POST /api/auth/signin` - Authenticate user
- `POST /api/auth/signout` - Invalidate session
- `PUT /api/auth/profile` - Update user profile

#### Task Management Endpoints
- `GET /api/tasks` - List user's tasks with pagination
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PATCH /api/tasks/{id}/complete` - Toggle completion status

#### Health Check Endpoint
- `GET /health` - Public endpoint to check system health
- **Purpose**: Verify backend service and database connectivity
- **Authentication**: No JWT required (public endpoint)
- **Logic**: Check database connectivity by performing a simple query (e.g., SELECT 1)
- **Success Response (200)**:
  ```json
  {
    "status": "ok",
    "database": "connected",
    "timestamp": "ISO 8601 UTC timestamp"
  }
  ```
- **Failure Response (503)**:
  ```json
  {
    "status": "error",
    "database": "disconnected",
    "timestamp": "ISO 8601 UTC timestamp"
  }
  ```

### 5.3 Component Architecture

#### Backend Structure
```
backend/
├── Dockerfile (Multi-stage build for FastAPI)
├── .dockerignore
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   └── task_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── task_service.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth_router.py
│   │   └── task_router.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth_middleware.py
│   └── main.py
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── alembic.ini
└── requirements.txt
```

#### Frontend Structure
```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── signin/
│   │   │   └── page.tsx
│   │   ├── signup/
│   │   │   └── page.tsx
│   │   └── dashboard/
│   │       └── page.tsx
│   ├── components/
│   │   ├── auth/
│   │   │   ├── SigninForm.tsx
│   │   │   └── SignupForm.tsx
│   │   ├── tasks/
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskItem.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   └── DeleteConfirm.tsx
│   │   └── ui/
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       └── Card.tsx
│   ├── lib/
│   │   ├── api.ts
│   │   └── auth.ts
│   └── types/
│       ├── user.ts
│       └── task.ts
├── public/
├── package.json
└── tsconfig.json
```

### 5.4 Security Architecture

#### JWT Token Structure
```json
{
  "user_id": "uuid-string",
  "email": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567890
}
```

#### Authentication Flow
1. User submits credentials to `/api/auth/signin`
2. Backend verifies credentials against database
3. Backend generates JWT with user_id and email
4. Frontend stores JWT in HttpOnly cookie
5. All subsequent requests include JWT in Authorization header
6. Backend middleware validates JWT and extracts user context

#### Rate Limiting Strategy
- Authentication endpoints: 5 requests per minute per IP
- Task API endpoints: 100 requests per minute per user
- Implemented with custom middleware tracking request counts

### 5.5 Error Handling Standard

#### FR-ERR-001: Standard Error Format
All HTTP 4xx/5xx error responses must follow this exact JSON structure:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE_STRING",
    "message": "Human readable description",
    "details": { "optional": "field_errors" }
  }
}
```

#### FR-ERR-002: Required Error Codes
The system must implement these specific error codes:
- `VALIDATION_ERROR`: For input validation failures
- `AUTH_INVALID`: For authentication/authorization failures
- `NOT_FOUND`: For resource not found scenarios
- `DB_ERROR`: For database connectivity or operation failures
- `EMAIL_EXISTS`: For duplicate email registration attempts
- `INVALID_CREDENTIALS`: For invalid email/password combinations
- `UNAUTHORIZED`: For missing or invalid JWT tokens
- `FORBIDDEN`: For unauthorized access attempts
- `SERVER_ERROR`: For internal server errors

| Code | HTTP Status | Description |
|------|-------------|-------------|
| EMAIL_EXISTS | 400 | Email already registered |
| INVALID_CREDENTIALS | 401 | Invalid email/password |
| UNAUTHORIZED | 401 | Missing or invalid JWT token |
| FORBIDDEN | 403 | User cannot access resource |
| NOT_FOUND | 404 | Resource not found |
| VALIDATION_ERROR | 422 | Invalid input data |
| DB_ERROR | 500 | Database connectivity or operation error |
| SERVER_ERROR | 500 | Internal server error |

## 6. Phase 2: Implementation Tasks Breakdown

### 6.1 Task Dependencies & Execution Order

```
T-001 Setup & Configuration
  ↓
T-002 Database Models & Schema
  ↓
T-003 Repository Layer Implementation
  ↓
T-004 Service Layer Implementation
  ↓
T-005 API Endpoints (Auth)
  ↓
T-006 API Endpoints (Tasks)
  ↓
T-007 Authentication Middleware
  ↓
T-008 Health Check & System Monitoring
  ↓
T-009 Rate Limiting & Resilience Patterns
  ↓
T-010 Frontend Setup & Auth Integration
  ↓
T-011 Frontend Task Management UI
  ↓
T-012 Security Hardening & Testing
```

### 6.2 Implementation Milestones

#### Milestone 1: Backend Foundation (T-001-T-004)
- Project scaffolding and dependencies
- Database models and relationships
- Repository layer with CRUD operations
- Service layer with business logic

#### Milestone 2: API Layer (T-005-T-007)
- Authentication endpoints
- Task management endpoints
- JWT middleware implementation

#### Milestone 3: Infrastructure & Resilience (T-008-T-009)
- Health check endpoint implementation
- Rate limiting middleware
- Circuit breaker pattern for database resilience
- Database connection pooling configuration

#### Milestone 4: Frontend Implementation (T-010-T-011)
- Next.js app setup with App Router
- Better Auth integration
- Task management UI components

#### Milestone 5: Integration & Validation (T-012)
- Security hardening
- End-to-end testing
- Performance validation

### 6.3 New Task Definitions

#### Task [T-008]: Health Check & System Monitoring
- **Objective**: Implement health check endpoint and system monitoring capabilities
- **Source Reference**: Plan §5.3 - API Contract Design (Health Check Endpoint), Plan §9.2 - Backend Deployment (Health Check)
- **Dependencies**: T-007
- **Estimated Time**: 15m
- **Files to Create/Modify**:
  - `backend/src/main.py` (add health check route)
  - `backend/src/api/health_router.py`
- **Step-by-Step Instructions**:
  1. Create health check endpoint GET /health (public, no auth required)
  2. Implement database connectivity check (perform simple SELECT 1 query)
  3. Return 200 OK with status: "ok" and database: "connected" when healthy
  4. Return 503 Service Unavailable with status: "error" and database: "disconnected" when unhealthy
  5. Include timestamp in both success and failure responses
  6. Register health check endpoint in main application
- **Definition of Done (Acceptance Criteria)**:
  - [ ] GET /health endpoint exists and is publicly accessible
  - [ ] Endpoint checks database connectivity
  - [ ] Healthy response returns 200 with status: "ok"
  - [ ] Unhealthy response returns 503 with status: "error"
  - [ ] Both responses include timestamp in ISO 8601 UTC format
  - [ ] Health check endpoint registered in main application

#### Task [T-009]: Rate Limiting & Resilience Patterns
- **Objective**: Implement rate limiting and resilience patterns for system stability
- **Source Reference**: Plan §5.4 - Security Architecture (Rate Limiting Strategy), Plan §8.2 - Data Protection (Database resilience), Plan §9.3 - Database (Connection Pooling)
- **Dependencies**: T-008
- **Estimated Time**: 30m
- **Files to Create/Modify**:
  - `backend/src/middleware/rate_limit.py`
  - `backend/src/db/connection.py`
  - `backend/src/middleware/circuit_breaker.py`
- **Step-by-Step Instructions**:
  1. Create rate limiting middleware with specific thresholds (5/min for auth, 100/min for tasks)
  2. Implement database connection pooling with 10-20 connections, max overflow 30, timeout 30s
  3. Implement circuit breaker pattern for database connections to handle failures gracefully
  4. Configure rate limiting on appropriate endpoints
  5. Add retry logic with exponential backoff for transient failures
  6. Log all rate limiting and circuit breaker events for monitoring
- **Definition of Done (Acceptance Criteria)**:
  - [ ] Rate limiting middleware implemented with specific thresholds
  - [ ] Database connection pooling configured with specified parameters
  - [ ] Circuit breaker pattern implemented for database connections
  - [ ] Rate limiting applied to authentication and task endpoints
  - [ ] Retry logic with exponential backoff implemented
  - [ ] Events properly logged for monitoring

## 7. Performance Targets

### 7.1 Backend Performance
- **API Response Times**: 
  - GET requests: < 100ms (95th percentile)
  - POST/PUT/PATCH requests: < 200ms (95th percentile)
  - DELETE requests: < 100ms (95th percentile)
  - Authentication requests: < 300ms (95th percentile)

### 7.2 Frontend Performance
- **Core Web Vitals**:
  - First Contentful Paint (FCP): < 1.5s
  - Largest Contentful Paint (LCP): < 2.5s
  - Time to Interactive (TTI): < 3.0s
  - Cumulative Layout Shift (CLS): < 0.1

### 7.3 Database Performance
- **Query Execution**: < 50ms average
- **Connection Pool**: 10-20 connections
- **Connection Timeout**: 30 seconds

## 8. Security Considerations

### 8.1 Authentication Security
- Passwords hashed with bcrypt (cost factor ≥ 12)
- JWT tokens with 7-day expiration
- HttpOnly cookies for token storage
- Rate limiting on auth endpoints

### 8.2 Data Protection
- User isolation: users only access their own data
- Parameterized queries to prevent SQL injection
- Input validation on all endpoints
- HTTPS enforcement in production

### 8.3 Infrastructure Security
- Environment variables for all secrets
- No hardcoded credentials
- Regular security updates
- Vulnerability scanning

## 9. Deployment Architecture

### 9.1 Frontend Deployment (Vercel)
- Automatic deployments from main branch
- Environment variables for API URLs
- HTTPS enabled by default
- CDN for static assets

### 9.2 Backend Deployment (Hugging Face Spaces)
- Platform: Hugging Face Spaces with Docker runtime
- Docker image: Multi-stage build using python:3.13-slim as base
- Runtime user: Must run as non-root user (user ID 1000) for Hugging Face security compliance
- Port configuration: Application must listen on port 7860 (Hugging Face default)
- Network binding: Bind to 0.0.0.0 (not localhost) to receive external traffic
- Environment variables for database URL and secrets
- Health check endpoint: `GET /health`
- Auto-scaling configuration

### 9.3 Database (Neon Serverless PostgreSQL)
- Connection pooling enabled
- SSL/TLS encryption required
- Automatic backups
- Connection string in environment variables

### 9.4 Docker Configuration for Hugging Face Spaces
- Base Image: Use python:3.13-slim (or similar lightweight image) for optimized builds
- Multi-stage build: Separate build and runtime stages to minimize image size
- Security: Run as non-root user (UID 1000) as required by Hugging Face Spaces
- CMD instruction: Define startup command to launch uvicorn on host 0.0.0.0 and port 7860
- Dependencies: Install with UV package manager for faster dependency resolution
- Environment: Configure to load secrets from HF_SPACE_SECRETS environment variables
- Health check: Include health check endpoint for container monitoring

### 9.5 Deployment Strategy
- Build: GitHub Actions builds the Docker image and pushes to Hugging Face Hub
- Secrets: GitHub Actions Secrets → Hugging Face Space Secrets
- Environment Variables: Map required environment variables from Hugging Face Space configuration
- CI/CD: Automated deployment from main branch to Hugging Face Spaces
- Rollback: Ability to rollback to previous versions if needed

## 10. Testing Strategy

### 10.1 Backend Testing
- Unit tests for services (>80% coverage)
- Integration tests for API endpoints
- Security tests for authentication
- Performance tests for API endpoints

### 10.2 Frontend Testing
- Component tests for UI elements (>70% coverage)
- Integration tests for API interactions
- End-to-end tests for critical user flows
- Accessibility tests

### 10.3 Testing Matrix

#### Authentication Test Scenarios
- `test_register_duplicate_email`: Verify system rejects duplicate email registration (Expect 400 response)
- `test_login_wrong_password`: Verify system rejects incorrect credentials (Expect 401 response)
- `test_login_valid_credentials`: Verify valid credentials grant access (Expect 200 response with token)
- `test_unauthorized_access`: Verify protected endpoints reject requests without valid JWT (Expect 401 response)

#### Task Management Test Scenarios
- `test_create_task_happy_path`: Verify task creation works correctly (Expect 201 response + DB verification)
- `test_get_tasks_pagination`: Create 25 tasks, request with limit=10, verify 10 returned per page
- `test_update_other_user_task`: Verify user cannot update another user's task (Expect 403 Forbidden)
- `test_delete_other_user_task`: Verify user cannot delete another user's task (Expect 403 Forbidden)
- `test_toggle_completion_valid`: Verify user can toggle completion status of their own task (Expect 200 response)
- `test_view_own_tasks_only`: Verify user only sees their own tasks (Expect 200 with user's tasks only)

### 10.4 Test Scenarios
- User registration and authentication
- Task CRUD operations
- Data isolation between users
- Error handling and edge cases
- Performance under load

## 11. Success Criteria

Phase II is complete when:
- [ ] All Phase I features working in web UI
- [ ] User signup/signin functional with Better Auth
- [ ] JWT authentication protecting all task endpoints
- [ ] Health check endpoint available at GET /health
- [ ] Rate limiting implemented with specified thresholds (5/min for auth, 100/min for tasks)
- [ ] Circuit breaker pattern protecting database connections
- [ ] Database connection pooling configured (10-20 connections)
- [ ] Frontend deployed to Vercel
- [ ] Backend deployed to Hugging Face Spaces and accessible
- [ ] Docker image properly configured for Hugging Face Spaces (port 7860, non-root user)
- [ ] Neon database configured and migrated
- [ ] All acceptance criteria met
- [ ] Test coverage > 80% for backend, > 70% for frontend
- [ ] All quality checks pass (linting, formatting)
- [ ] User isolation verified (cannot access other users' data)
- [ ] Demo video recorded (< 90 seconds)
- [ ] All code generated via Qwen CLI with proper task references
- [ ] README updated with Phase II setup instructions