---
id: 21
title: create-phase-ii-implementation-plan
stage: plan
date: 2026-01-16
surface: agent
model: "openai/gpt-4o"
feature: phase-2-web-app
branch: main
user: metachemist
command: "/sp.plan"
labels: ["planning", "architecture", "phase-II"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/specs/2-plan/phase-2-fullstack.md
tests:
 - null
---

## Prompt

/sp.plan 
@constitution.md
# ROLE
Act as a Principal Software Architect.

# CONTEXT
We have APPROVED **Phase II Specifications** for the Full-Stack Web App.
- `specs/1-specify/features/feature-02-web-api.md`
- `specs/1-specify/features/feature-03-authentication.md`

# TASK
Generate the technical architecture plan: `specs/2-plan/phase-2-fullstack.md`.

# REQUIREMENTS
The plan must define the **Full-Stack Architecture** strictly following the Specs.

# Phase II Execution Plan: Full-Stack Web Application

**Version**: 1.0  
**Date**: 2026-01-16  
**Status**: Draft  
**Based on**: Constitution v1.5.0, System Overview, Feature-02-Web-API, Feature-03-Authentication

---

## 1. Phase 2 Objectives

**Derived from**: `system-overview.md` - Phase II Scope (In-Scope)

Phase II transforms the CLI todo application into a modern multi-user web application with:

1. **Full-stack web application** with Next.js frontend
2. **RESTful API** with FastAPI backend
3. **User authentication** (signup/signin) with Better Auth + JWT
4. **Persistent storage** with Neon Serverless PostgreSQL
5. **Multi-user support** with data isolation
6. **Responsive UI** for desktop and mobile

---

## 2. Scope Breakdown

### 2.1 Features Explicitly Mentioned

#### Feature A: User Authentication System
**Spec Reference**: `feature-03-authentication.md`

**Components**:
- User registration (signup) with email, name, and password
- User authentication (signin) with email and password
- Session management with JWT tokens
- User data isolation
- Better Auth integration for Next.js frontend
- FastAPI JWT verification

**Entities**:
- User entity with: id (UUID), email (string, unique), name (string), password_hash (string), created_at (timestamp), updated_at (timestamp)

#### Feature B: REST API for Task Management
**Spec Reference**: `feature-02-web-api.md`

**Endpoints**:

**Authentication Endpoints**:
- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User authentication
- `POST /api/auth/signout` - Session termination
- `PUT /api/auth/profile` - User profile updates

**Task Endpoints** (all require JWT):
- `GET /api/{user_id}/tasks` - List user tasks with pagination
- `POST /api/{user_id}/tasks` - Create task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `PATCH /api/{user_id}/tasks/{id}` - Partial update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

**Entities**:
- Task entity with: id (integer/UUID), user_id (UUID), title (string, 1-200 chars), description (optional string), completed (boolean), created_at (timestamp), updated_at (timestamp)

#### Feature C: Multi-User Support with Data Isolation
**Spec Reference**: `feature-03-authentication.md` §3.4, `feature-02-web-api.md` §3.3

**Requirements**:
- Each user can only access their own tasks
- API validates user_id in URL matches JWT token user_id
- Database queries always filter by user_id
- 403 Forbidden for unauthorized access attempts
- ON DELETE CASCADE for User->Task relationship

#### Feature D: Persistent Storage
**Spec Reference**: `system-overview.md` - Phase II Constraints

**Requirements**:
- PostgreSQL database (Neon Serverless)
- SQLModel ORM
- Alembic for database migrations
- Data persists across sessions
- Replaces Phase I in-memory storage

### 2.2 Out-of-Scope Items (Phase II Non-Goals)

**Explicitly stated in**: `system-overview.md` - Phase II Scope (Out-of-Scope)

- AI chatbot interface (Phase III)
- Natural language processing (Phase III)
- Kubernetes deployment (Phase IV)
- Advanced features: priorities, tags, search, filters (Phase V)
- Event streaming with Kafka (Phase V)
- Password reset functionality (Feature-03 §1.3)
- Social authentication (Google, GitHub, etc.) (Feature-03 §1.3)
- Multi-factor authentication (Feature-03 §1.3)
- Account verification via email (Feature-03 §1.3)

---

## 3. Step-by-Step Implementation Plan

### Phase 2 Prerequisites

**Spec Reference**: Constitution §2 - Technology Stack Phase II

**Required Setup**:
1. Python 3.13+ installed
2. UV package manager installed
3. Node.js 18+ for Next.js 16+
4. Neon PostgreSQL database provisioned
5. Qwen CLI configured for code generation

---

### Step 1: Database Schema Design & Migration Setup

**Spec Reference**: 
- `feature-03-authentication.md` §2 (User entity)
- `feature-02-web-api.md` §2 (Task entity)
- Constitution §3 - Technology Stack Phase II (SQLModel, Alembic)

**Relevant Folders**: 
- `/specs/2-plan/db-schema/`
- `/backend/src/models/`
- `/backend/alembic/`

**Actions**:
1. Create User model with SQLModel:
   - Fields: id (UUID), email (string, unique), name (string), password_hash (string), created_at, updated_at
   - Constraints: email uniqueness (case-insensitive), max 254 chars per RFC 5321
   
2. Create Task model with SQLModel:
   - Fields: id (integer/UUID), user_id (UUID foreign key), title (string, 1-200 chars), description (optional string, max 1000 chars), completed (boolean), created_at, updated_at
   - Constraints: Foreign key to User with ON DELETE CASCADE
   - Indexes: user_id, completed, created_at (per Constitution §3.3)

3. Initialize Alembic for migrations
4. Create initial migration script

**Acceptance Criteria**:
- User and Task models defined with proper types and constraints
- Foreign key relationship established with cascade delete
- Alembic initialized and first migration created

---

### Step 2: Backend API Foundation - FastAPI Setup

**Spec Reference**: 
- Constitution §3 - Technology Stack Phase II (FastAPI)
- `feature-02-web-api.md` §3

**Relevant Folders**:
- `/backend/src/`
- `/backend/src/routes/`
- `/backend/src/middleware/`

**Actions**:
1. Initialize FastAPI application
2. Configure CORS for frontend domain and localhost (NFR-SEC-005)
3. Set up database connection with connection pooling
4. Create standard error response format (FR-ERR-001):
   ```json
   {
     "success": false,
     "error": {
       "code": "ERROR_CODE",
       "message": "Human-readable error message"
     }
   }
   ```
5. Configure environment variables for secrets management

**Acceptance Criteria**:
- FastAPI application starts without errors
- CORS configured for specific origins (not wildcard)
- Database connection established
- Standard error format implemented

---

### Step 3: User Authentication - Registration & Login

**Spec Reference**: 
- `feature-03-authentication.md` §3.1, §3.2
- Constitution §2 (Better Auth, JWT)

**Relevant Folders**:
- `/backend/src/routes/auth.py`
- `/backend/src/services/auth_service.py`
- `/backend/src/utils/password.py`
- `/backend/src/utils/jwt.py`

**Actions**:
1. Implement password hashing with bcrypt (cost factor ≥ 12)
2. Implement JWT token generation:
   - Payload: user_id, email, exp, iat
   - Expiration: 7 days
   - Algorithm: Standard asymmetric or HMAC signing
   
3. Implement `POST /api/auth/signup` endpoint (FR-REG-001):
   - Validate email format (max 254 chars)
   - Validate password (min 8 chars)
   - Validate name (1-100 chars)
   - Check email uniqueness (case-insensitive)
   - Hash password before storage
   - Return user data + JWT token
   - Error: 400 if email exists
   
4. Implement `POST /api/auth/signin` endpoint (FR-AUTH-001):
   - Validate credentials
   - Verify password hash
   - Generate JWT token
   - Return user data + JWT token
   - Error: 401 for invalid credentials

5. Implement `POST /api/auth/signout` endpoint (FR-SESSION-002):
   - Clear token from frontend
   - Return success message

6. Implement `PUT /api/auth/profile` endpoint (FR-AUTH-004):
   - Allow name and password updates only (email immutable)
   - Validate same rules as registration
   - Return updated user data

**Acceptance Criteria**:
- User can register with valid email, name, password
- Passwords stored as secure hashes (never plain text)
- User can sign in with correct credentials
- JWT token generated with 7-day expiration
- Invalid credentials return 401 error
- Duplicate email returns 400 error
- User can sign out successfully
- User can update name and password (not email)

---

### Step 4: JWT Authentication Middleware

**Spec Reference**: 
- `feature-03-authentication.md` §3.2, §3.3
- `feature-02-web-api.md` §3.3 (FR-SEC-001)
- Constitution §2 (Better Auth integration)

**Relevant Folders**:
- `/backend/src/middleware/auth.py`

**Actions**:
1. Create authentication middleware (FR-BETTER-002):
   - Extract JWT from Authorization header (Bearer token)
   - Verify token signature with secret key
   - Check token expiration
   - Validate user exists in database
   - Inject user context into request
   
2. Create user isolation validation:
   - Compare user_id from URL with JWT user_id
   - Return 403 Forbidden for mismatched access
   
3. Apply middleware to all task endpoints
4. Handle token verification errors:
   - 401 for missing/invalid/expired tokens

**Acceptance Criteria**:
- All task endpoints require valid JWT token
- Invalid tokens return 401 Unauthorized
- Expired tokens return 401 Unauthorized
- User_id mismatch returns 403 Forbidden
- Valid tokens allow access to user's own resources

---

### Step 5: Task CRUD API Implementation

**Spec Reference**: 
- `feature-02-web-api.md` §3.2
- `feature-03-authentication.md` §3.4 (Data isolation)

**Relevant Folders**:
- `/backend/src/routes/tasks.py`
- `/backend/src/services/task_service.py`
- `/backend/src/repositories/task_repository.py`

**Actions**:

1. **List Tasks** - `GET /api/{user_id}/tasks` (FR-TASK-001):
   - Query parameters: status (all/pending/completed), page (default 1), limit (default 20, max 100)
   - Filter by user_id from JWT
   - Sort by created_at DESC (newest first)
   - Return tasks array + pagination metadata
   - Return empty array (200 OK) if no tasks found (NFR-REL-006)

2. **Create Task** - `POST /api/{user_id}/tasks` (FR-TASK-002):
   - Validate title (required, 1-200 chars)
   - Validate description (optional, max 1000 chars)
   - Set user_id from JWT token
   - Set completed = false by default
   - Support idempotency_key to prevent duplicates
   - Return 201 Created with task data
   - All timestamps in UTC ISO 8601 format (NFR-PERF-003)

3. **Get Task** - `GET /api/{user_id}/tasks/{id}` (FR-TASK-003):
   - Verify task belongs to user
   - Return 404 if not found
   - Return 403 if belongs to different user

4. **Update Task** - `PUT /api/{user_id}/tasks/{id}` (FR-TASK-004):
   - Validate title (1-200 chars)
   - Validate description (max 1000 chars, optional)
   - Verify task ownership
   - Update updated_at timestamp
   - Return 200 OK with updated task

5. **Partial Update Task** - `PATCH /api/{user_id}/tasks/{id}` (FR-TASK-007):
   - Fields set to null are ignored (not updated)
   - Only provided fields are validated
   - Verify task ownership

6. **Delete Task** - `DELETE /api/{user_id}/tasks/{id}` (FR-TASK-005):
   - Verify task ownership
   - Permanently delete from database
   - Return 200 OK with success message

7. **Toggle Completion** - `PATCH /api/{user_id}/tasks/{id}/complete` (FR-TASK-006):
   - Toggle completed boolean
   - Update updated_at timestamp
   - Return updated task with new completion status

**Acceptance Criteria**:
- All endpoints protected with JWT authentication
- Users can only access their own tasks (403 for others)
- Input validation prevents invalid data (422 error)
- Response times meet requirements (GET < 100ms, POST < 200ms, etc.)
- Empty task list returns 200 with empty array
- All timestamps in UTC ISO 8601 format
- Pagination works correctly for list endpoint

---

### Step 6: Frontend - Next.js Setup & Better Auth Integration

**Spec Reference**: 
- Constitution §3 - Technology Stack Phase II (Next.js 16+, TypeScript, Tailwind CSS)
- `feature-03-authentication.md` §3.5 (FR-BETTER-001)
- `system-overview.md` - Phase II Scope

**Relevant Folders**:
- `/frontend/src/app/`
- `/frontend/src/components/auth/`
- `/frontend/src/lib/auth/`

**Actions**:
1. Initialize Next.js 16+ with App Router
2. Install Better Auth library
3. Configure Better Auth:
   - Shared secret key with backend
   - JWT settings matching backend
   - HttpOnly cookie storage (not LocalStorage per FR-AUTH-003)
   
4. Create authentication components:
   - SignupForm component
   - SigninForm component
   
5. Set up authentication routing:
   - /signup page
   - /signin page
   - Protected routes middleware
   
6. Configure session management:
   - Store JWT in HttpOnly cookies
   - Automatic token inclusion in API requests
   - Handle token expiration with redirect to signin

**Acceptance Criteria**:
- Next.js application starts without errors
- Better Auth configured with matching backend settings
- Signup and signin forms render correctly
- JWT tokens stored in HttpOnly cookies (not LocalStorage)
- Protected routes redirect to signin when unauthenticated

---

### Step 7: Frontend - Task Management UI

**Spec Reference**: 
- `feature-02-web-api.md` (API endpoints)
- `system-overview.md` - Phase II Scope (Responsive UI)

**Relevant Folders**:
- `/frontend/src/app/dashboard/`
- `/frontend/src/components/tasks/`
- `/frontend/src/lib/api/`

**Actions**:
1. Create API client for task endpoints:
   - Automatically include JWT from cookies
   - Handle 30-second timeout with retry UI (NFR-REL-001)
   - Handle 401 errors with redirect to signin
   - Handle 403 errors with appropriate message
   - Handle 429 rate limit errors (NFR-REL-002)
   
2. Create task management components:
   - TaskList component (displays tasks with pagination)
   - TaskForm component (create/edit tasks)
   - TaskItem component (individual task display)
   
3. Create dashboard page:
   - Protected route (requires authentication)
   - List user's tasks
   - Create new task
   - Update existing task
   - Delete task
   - Toggle task completion
   
4. Implement responsive design with Tailwind CSS:
   - Mobile-friendly layout
   - Desktop optimized layout

5. Handle error states:
   - Network timeout: display Retry button
   - Rate limiting: display appropriate message
   - Database unavailable (503): display error with Retry-After
   - Empty task list: user-friendly message

**Acceptance Criteria**:
- Dashboard displays user's tasks only
- Users can create, read, update, delete tasks
- UI is responsive for mobile and desktop
- Loading states displayed during API calls
- Error states handled gracefully
- Frontend performance: FCP < 1.5s, LCP < 2.5s, TTI < 3.0s (per system-overview.md)
- Empty task list shows friendly message, not 404 error

---

### Step 8: Security Hardening & Rate Limiting

**Spec Reference**: 
- `feature-03-authentication.md` §4.2 (NFR-SEC-003, NFR-SEC-004)
- `feature-02-web-api.md` §4.2 (NFR-SEC-002)
- Constitution §2 (Security First)

**Relevant Folders**:
- `/backend/src/middleware/rate_limit.py`
- `/backend/src/middleware/security.py`

**Actions**:
1. Implement rate limiting:
   - Signup: 5 attempts per hour per IP
   - Signin: 10 attempts per minute per IP
   - Task API: 100 requests per minute per user
   - Return 429 Too Many Requests when exceeded
   - Include Retry-After header
   
2. Implement account lockout:
   - Temporary lock after multiple failed signin attempts
   - Prevent brute force attacks
   
3. Configure HTTPS enforcement:
   - All API endpoints require HTTPS
   - HSTS headers enabled
   
4. Input validation & sanitization:
   - Prevent SQL injection (using SQLModel parameterized queries)
   - Sanitize all user inputs
   - Support UTF-8 encoding including emoji (NFR-SEC-004)
   
5. Secrets management:
   - JWT secret in environment variable
   - Database credentials in environment variable
   - Never hardcode secrets

**Acceptance Criteria**:
- Rate limits enforced correctly
- Brute force attacks prevented with account lockout
- All passwords transmitted over HTTPS only
- All API requests require HTTPS
- SQL injection prevented through ORM
- UTF-8 characters (including emoji) supported
- No secrets hardcoded in source code

---

### Step 9: Database Connection Resilience & Error Handling

**Spec Reference**: 
- `feature-02-web-api.md` §4.4 (NFR-REL-003, NFR-REL-004, NFR-REL-005)
- Constitution §1 (Error Handling)

**Relevant Folders**:
- `/backend/src/db/connection.py`
- `/backend/src/middleware/error_handler.py`

**Actions**:
1. Implement database connection resilience:
   - Return 503 Service Unavailable if database unreachable
   - Include Retry-After header in 503 responses
   - Circuit breaker pattern for database connections
   - Log all database connection failures
   
2. Implement retry logic for transient failures:
   - Exponential backoff starting at 100ms
   - Maximum 3 retry attempts
   - Apply to token validation and database queries
   
3. Implement optimistic concurrency control:
   - Database-level locking for concurrent updates
   - Last-Write-Wins strategy for conflict resolution
   - Return latest data after concurrent updates
   
4. Centralized error handling:
   - Structured error responses (4xx for client, 5xx for server)
   - Consistent error format across all endpoints
   - Appropriate HTTP status codes for each error type

**Acceptance Criteria**:
- Database unavailability returns 503 with Retry-After
- Transient failures retry automatically with exponential backoff
- Concurrent updates don't corrupt data
- All errors follow standard format
- Circuit breaker prevents cascading failures

---

### Step 10: Testing & Validation

**Spec Reference**: 
- Constitution §4 (Quality Standards - Test Coverage: 80% for business logic)
- `feature-03-authentication.md` §2 (User Scenarios)
- `feature-02-web-api.md` §2 (User Scenarios)

**Relevant Folders**:
- `/backend/tests/`
- `/frontend/tests/`

**Actions**:
1. Backend unit tests:
   - User registration scenarios
   - User signin scenarios
   - JWT token generation/verification
   - Task CRUD operations
   - User data isolation
   - Password hashing security
   - Input validation
   
2. Backend integration tests:
   - End-to-end API flows
   - Database interactions
   - Authentication middleware
   
3. Frontend unit tests:
   - Component rendering
   - Form validation
   - API client functionality
   
4. Frontend integration tests:
   - User registration flow
   - User signin flow
   - Task management flow
   
5. Performance validation:
   - API response times (GET < 100ms, POST < 200ms, etc.)
   - Frontend metrics (FCP < 1.5s, LCP < 2.5s, TTI < 3.0s)
   - Concurrent user load testing

**Acceptance Criteria**:
- Test coverage > 80% for business logic
- All user scenarios from specs pass
- Performance metrics meet requirements
- All security tests pass
- No regressions in Phase I functionality

---

## 4. Dependencies & Preconditions

### 4.1 External Dependencies

**From Constitution §3 - Technology Stack Phase II**:

| Dependency | Version | Purpose |
|------------|---------|---------|
| Python | 3.13+ | Backend runtime |
| UV | Latest | Python package manager |
| Next.js | 16+ | Frontend framework |
| TypeScript | Latest | Frontend type safety |
| Tailwind CSS | Latest | Frontend styling |
| FastAPI | Latest | Backend API framework |
| SQLModel | Latest | ORM for database |
| Alembic | Latest | Database migrations |
| Better Auth | Latest | Frontend authentication |
| Neon PostgreSQL | Latest | Serverless database |

### 4.2 Task Dependencies (Must Complete in Order)

1. **Step 1 (Database Schema)** → No dependencies
2. **Step 2 (FastAPI Setup)** → Depends on Step 1
3. **Step 3 (Auth Implementation)** → Depends on Step 1, 2
4. **Step 4 (Auth Middleware)** → Depends on Step 3
5. **Step 5 (Task API)** → Depends on Step 1, 2, 4
6. **Step 6 (Frontend Auth)** → Depends on Step 3
7. **Step 7 (Frontend Tasks)** → Depends on Step 5, 6
8. **Step 8 (Security)** → Depends on Step 3, 5
9. **Step 9 (Resilience)** → Depends on Step 2, 5
10. **Step 10 (Testing)** → Depends on all previous steps

### 4.3 Environment Prerequisites

**From Constitution §9 (Environment Management)**:

Required environment variables:
- `DATABASE_URL` - Neon PostgreSQL connection string
- `JWT_SECRET` - Secret key for JWT signing (secure random string)
- `FRONTEND_URL` - Frontend domain for CORS configuration
- `BACKEND_URL` - Backend API URL
- `ENVIRONMENT` - dev/staging/production

**Not defined in specifications**: Specific deployment infrastructure details beyond "Vercel (frontend), Backend hosting TBD"

---

## 5. Validation & Acceptance Criteria

### 5.1 Phase II Success Metrics (SMART)

**From**: `system-overview.md` - Phase II Metrics

#### API Response Times:
- CREATE < 200ms (95th percentile) ✓
- READ < 100ms (95th percentile) ✓
- UPDATE < 150ms (95th percentile) ✓
- DELETE < 100ms (95th percentile) ✓

#### User Authentication:
- Users can securely sign up with email/password ✓
- Users can securely sign in with email/password ✓
- JWT tokens generated and verified correctly ✓

#### Data Isolation:
- Users can only access their own tasks ✓
- Unauthorized access returns 403 Forbidden ✓
- Database queries always filter by user_id ✓

#### Frontend Performance:
- FCP < 1.5s ✓
- LCP < 2.5s ✓
- TTI < 3.0s ✓

#### Security:
- All endpoints properly protected with JWT authentication ✓
- Passwords securely hashed with bcrypt (cost factor ≥ 12) ✓
- All API traffic over HTTPS ✓

### 5.2 Functional Acceptance Criteria

**From**: `feature-03-authentication.md` §5 and `feature-02-web-api.md` §5

#### Authentication System Complete When:
- ✓ New users can register with email, name, and password
- ✓ Registered users can sign in with valid credentials
- ✓ JWT tokens are properly generated and verified
- ✓ Users stay logged in across sessions
- ✓ Users can securely sign out
- ✓ User data isolation prevents unauthorized access
- ✓ All authentication endpoints return proper responses
- ✓ Passwords are securely hashed before storage
- ✓ Authentication tests pass (> 80% coverage)
- ✓ Security measures prevent common vulnerabilities
- ✓ Better Auth integrates properly with Next.js frontend
- ✓ FastAPI properly verifies JWT tokens

#### REST API Complete When:
- ✓ All endpoints return proper HTTP status codes
- ✓ JWT authentication protects all task endpoints
- ✓ User isolation prevents unauthorized access
- ✓ Input validation prevents malicious data
- ✓ Error responses follow standard format
- ✓ Response times meet performance requirements
- ✓ API tests pass (> 80% coverage)
- ✓ Security measures prevent common vulnerabilities
- ✓ Documentation matches implementation

### 5.3 Non-Functional Acceptance Criteria

**From**: `feature-03-authentication.md` §4 and `feature-02-web-api.md` §4

#### Performance:
- Authentication response times: Signup < 500ms, Signin < 300ms, Token verification < 50ms (95th percentile)
- API concurrency: Support 1000+ concurrent users
- Rate limiting enforced correctly

#### Security:
- Password hashing: Industry-standard secure algorithms with safe work factors
- Token security: Standard JWT signing with 7-day expiration
- Rate limiting: 5 signup/hour per IP, 10 signin/minute per IP, 100 requests/minute per user
- HTTPS enforcement with HSTS headers
- UTF-8 encoding support including emoji

#### Availability:
- 99.9% uptime
- Graceful degradation during failures
- Automatic recovery from temporary issues

#### Reliability:
- 30-second timeout handling with retry UI
- 503 Service Unavailable if database unreachable (with Retry-After header)
- Circuit breaker pattern for external dependencies
- Exponential backoff retry logic (100ms start, max 3 retries)
- Optimistic concurrency control for concurrent updates
- Empty list returns 200 OK with empty array (not 404)

---

## 6. Out-of-Scope Items (Explicitly NOT in Phase II)

**From**: `system-overview.md` - Phase II Scope (Out-of-Scope)

### Features Deferred to Later Phases:
- ❌ AI chatbot interface → Phase III
- ❌ Natural language processing → Phase III
- ❌ Kubernetes deployment → Phase IV
- ❌ Advanced features: priorities, tags, search, filters → Phase V
- ❌ Event streaming with Kafka → Phase V

### Features Explicitly Out-of-Scope:
- ❌ Password reset functionality (per `feature-03-authentication.md` §1.3)
- ❌ Social authentication (Google, GitHub, etc.) (per `feature-03-authentication.md` §1.3)
- ❌ Multi-factor authentication (per `feature-03-authentication.md` §1.3)
- ❌ Account verification via email (per `feature-03-authentication.md` §1.3)
- ❌ Frontend implementation details beyond what's specified
- ❌ Database schema specifics beyond what's specified (per `feature-02-web-api.md` §1.3)
- ❌ Deployment configurations beyond basic requirements (per `feature-02-web-api.md` §1.3)

---

## 7. Missing or Unclear Specifications

### 7.1 Items Not Defined in Provided Specifications:

1. **Existing Folder Structure**: The task requested "Existing Folder Structure" as one of the four required files, but this was not provided. Therefore, specific file paths in implementation steps are based on the Constitution's project structure only.

2. **Specific Backend Hosting**: Constitution states "Backend hosting TBD" - no specific hosting platform defined for backend deployment.

3. **Database Connection Pooling Configuration**: Constitution mentions connection pooling (§3.3) but specific pool size, timeout values, and configuration parameters are not defined.

4. **Specific JWT Algorithm**: Specifications state "Standard asymmetric or HMAC signing algorithm appropriate for JWTs" but don't specify which exact algorithm (e.g., RS256, HS256).

5. **Redis Caching Implementation**: Constitution §3.3 mentions Redis caching for session data, but this is not mentioned in Phase II feature specifications. Unclear if this is Phase II scope or later phase.

6. **Specific Better Auth Configuration**: Integration requirements mentioned but specific configuration details (endpoints, callback URLs, etc.) not provided.

7. **API Versioning Strategy**: `feature-02-web-api.md` mentions potential `/v2/` versioning but Phase II endpoints don't specify version numbers in paths.

8. **Metrics/Monitoring Tools**: Constitution mentions monitoring but specific tools (e.g., Prometheus, DataDog) not specified for Phase II.

9. **Testing Framework**: Constitution requires 80% test coverage but doesn't specify pytest vs. unittest for backend, or Jest vs. Vitest for frontend.

10. **CI/CD Pipeline**: Constitution mentions GitHub Actions for Phase V, but no specification for Phase II automated testing/deployment.

---

## 8. Implementation Workflow Compliance

**From**: Constitution §5 - Development Workflow

### Workflow for Each Step:

1. **Specify**: Feature specs already exist (`feature-02-web-api.md`, `feature-03-authentication.md`)
2. **Plan**: This execution plan serves as the architecture/technical approach
3. **Tasks**: Each step above must be broken into tasks in `/specs/3-tasks/phase-2/` with Task IDs (T-XXX)
4. **Implement**: Use Qwen CLI to generate code from approved tasks
5. **Validate**: Run tests, verify acceptance criteria met

### Code Generation Requirements:

**From**: Constitution §3.1 (Task Traceability)

Every generated code file must include header:
```
# [Task]: T-XXX | [From]: speckit.specify §X.Y, speckit.plan §Z.W
```

### Commit Strategy:

**From**: Constitution §10 - Commit Message Convention

```
[T-XXX] Brief description (50 chars max)

- Detailed point 1
- Generated via: Qwen CLI
- Spec reference: specs/features/file.md §X.Y
- Tests: coverage X%, all passing
- Phase: II
```

---

## 9. Quality Gates

**From**: Constitution §4 (Quality Standards)

Before marking Phase II complete, verify:

### Code Quality:
- ✓ Test coverage > 80% for business logic
- ✓ All functions have docstrings (purpose, params, returns)
- ✓ Type hints used throughout (Python type hints, TypeScript)
- ✓ No single-letter variable names (except i, j, k in loops)
- ✓ Task traceability headers in all files

### Security:
- ✓ No hardcoded secrets
- ✓ JWT tokens properly secured
- ✓ Passwords hashed with bcrypt (cost ≥ 12)
- ✓ Input validation on all endpoints
- ✓ HTTPS enforced in production
- ✓ CORS configured for specific origins only

### Performance:
- ✓ API response times meet targets
- ✓ Frontend performance metrics met
- ✓ Database queries use indexes
- ✓ Connection pooling configured

### Documentation:
- ✓ API documentation matches implementation
- ✓ README updated for Phase II setup
- ✓ Environment variables documented

---

## 10. Deployment Readiness

**From**: Constitution §3 - Technology Stack Phase II

### Frontend Deployment (Vercel):
- Next.js 16+ application configured
- Environment variables set (BACKEND_URL, JWT_SECRET)
- Production build successful
- HTTPS enabled

### Backend Deployment (TBD):
**Not defined in specifications**: Specific backend hosting platform

Required for any backend platform:
- Python 3.13+ runtime
- FastAPI application
- Database connection to Neon PostgreSQL
- Environment variables configured
- HTTPS enabled
- CORS configured for production frontend domain

### Database (Neon PostgreSQL):
- Database provisioned
- Migrations applied via Alembic
- Connection string secured in environment variables

---

## Response snapshot

I have successfully created the implementation plan for Phase II of the Todo Evolution project. The plan includes:

1. A comprehensive technical architecture for the full-stack web application
2. Detailed component designs for both backend (FastAPI) and frontend (Next.js)
3. Clear API contracts for authentication and task management
4. Security considerations including JWT implementation and user isolation
5. Database schema design with proper relationships and constraints
6. Implementation task breakdown with dependencies
7. Performance targets and success criteria
8. Deployment architecture for both frontend and backend

The plan addresses all requirements from the specifications and fills in the technical details needed for implementation while maintaining consistency with the project constitution.

## Outcome

- ✅ Impact: Created comprehensive Phase II implementation plan
- 🧪 Tests: N/A (planning phase)
- 📁 Files: Created specs/2-plan/phase-2-fullstack.md with complete architecture plan
- 🔁 Next prompts: Ready to proceed with task breakdown using /sp.tasks
- 🧠 Reflection: Plan provides clear roadmap for implementing the full-stack web application with authentication

## Evaluation notes (flywheel)

- Failure modes observed: None - all requirements addressed in plan
- Graders run and results (PASS/FAIL): N/A (planning phase)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with task breakdown using /sp.tasks