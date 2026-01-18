# Feature Specification: REST API for Task Management (Phase II)

**Version**: 1.0
**Phase**: II - Full-Stack Web Application
**Status**: Draft
**Last Updated**: 2026-01-16

## 1. Overview

### 1.1 Purpose
Expose Task CRUD operations via a secure, RESTful API that integrates with the Next.js frontend and FastAPI backend.

### 1.2 Scope
This specification covers the API endpoints for:
- Task management (Create, Read, Update, Delete, Complete)
- User authentication (Signup, Signin, Signout)
- All endpoints protected with JWT authentication

### 1.3 Out of Scope
- Frontend implementation details
- Database schema specifics
- Deployment configurations

### 1.4 Dependencies
- Phase I task business logic
- Better Auth integration
- JWT authentication system

## 2. User Scenarios & Testing

### 2.1 Task Creation Scenario
**Scenario**: Authenticated user creates a new task
- **Given**: User has valid JWT token
- **When**: User sends POST request to `/api/{user_id}/tasks` with task data
- **Then**: Task is created and returned with user association
- **Test**: Verify task exists in database with correct user_id

### 2.2 Task Retrieval Scenario
**Scenario**: Authenticated user retrieves their tasks
- **Given**: User has valid JWT token and tasks exist
- **When**: User sends GET request to `/api/{user_id}/tasks`
- **Then**: Only user's tasks are returned
- **Test**: Verify user isolation (no other users' tasks returned)

### 2.3 Task Update Scenario
**Scenario**: Authenticated user updates their task
- **Given**: User has valid JWT token and owns the task
- **When**: User sends PUT request to `/api/{user_id}/tasks/{id}`
- **Then**: Task is updated if user owns it
- **Test**: Verify only task owner can update

### 2.4 Task Deletion Scenario
**Scenario**: Authenticated user deletes their task
- **Given**: User has valid JWT token and owns the task
- **When**: User sends DELETE request to `/api/{user_id}/tasks/{id}`
- **Then**: Task is deleted if user owns it
- **Test**: Verify only task owner can delete

### 2.5 Authentication Scenario
**Scenario**: User authenticates to access protected endpoints
- **Given**: User has valid credentials
- **When**: User sends POST request to `/api/auth/signin`
- **Then**: JWT token is returned
- **Test**: Verify token can be used for protected endpoints

## 3. Functional Requirements

### 3.1 Authentication Endpoints

#### FR-AUTH-001: User Registration
- **Endpoint**: `POST /api/auth/signup`
- **Purpose**: Create new user account
- **Request Body**:
  ```json
  {
    "name": "string (required)",
    "email": "string (required, unique)",
    "password": "string (required, min 8 chars)"
  }
  ```
- **Success Response (201)**:
  ```json
  {
    "success": true,
    "data": {
      "user": {
        "id": "uuid-string",
        "email": "string",
        "name": "string",
        "created_at": "timestamp"
      },
      "token": "jwt-token"
    }
  }
  ```
- **Error Response (400)**:
  ```json
  {
    "success": false,
    "error": {
      "code": "EMAIL_EXISTS",
      "message": "Email already registered"
    }
  }
  ```

#### FR-AUTH-002: User Signin
- **Endpoint**: `POST /api/auth/signin`
- **Purpose**: Authenticate user and return JWT token
- **Request Body**:
  ```json
  {
    "email": "string (required)",
    "password": "string (required)"
  }
  ```
- **Success Response (200)**:
  ```json
  {
    "success": true,
    "data": {
      "user": {
        "id": "uuid-string",
        "email": "string",
        "name": "string"
      },
      "token": "jwt-token"
    }
  }
  ```
- **Error Response (401)**:
  ```json
  {
    "success": false,
    "error": {
      "code": "INVALID_CREDENTIALS",
      "message": "Invalid email or password"
    }
  }
  ```

#### FR-AUTH-003: User Signout
- **Endpoint**: `POST /api/auth/signout`
- **Purpose**: Invalidate user session
- **Headers Required**: `Authorization: Bearer {token}`
- **Success Response (200)**:
  ```json
  {
    "success": true,
    "data": {
      "message": "Successfully signed out"
    }
  }
  ```

### 3.2 Task Management Endpoints

#### FR-TASK-001: List User Tasks
- **Endpoint**: `GET /api/{user_id}/tasks`
- **Purpose**: Retrieve tasks for authenticated user with pagination support
- **Headers Required**: `Authorization: Bearer {token}`
- **Query Parameters** (Optional):
  - `status`: "all" | "pending" | "completed"
  - `page`: Integer (default: 1) - Page number for pagination
  - `limit`: Integer (default: 20, max: 100) - Number of tasks per page
- **Default Sorting**: Results are sorted by `created_at` DESC (Newest first)
- **Success Response (200)**:
  ```json
  {
    "success": true,
    "data": {
      "tasks": [
        {
          "id": "integer",
          "user_id": "uuid-string",
          "title": "string",
          "description": "string or null",
          "completed": "boolean",
          "created_at": "timestamp",
          "updated_at": "timestamp"
        }
      ],
      "pagination": {
        "page": "integer",
        "limit": "integer",
        "total": "integer",
        "pages": "integer"
      }
    }
  }
  ```

#### FR-TASK-002: Create Task
- **Endpoint**: `POST /api/{user_id}/tasks`
- **Purpose**: Create a new task for authenticated user
- **Headers Required**: `Authorization: Bearer {token}`, `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "title": "string (required, 1-200 chars)",
    "description": "string (optional, max 1000 chars)",
    "idempotency_key": "string (optional, for preventing duplicate requests)"
  }
  ```
- **Idempotency**: System implements idempotency using request identifiers to prevent accidental duplicate task creation
- **Success Response (201)**:
  ```json
  {
    "success": true,
    "data": {
      "task": {
        "id": "integer",
        "user_id": "uuid-string",
        "title": "string",
        "description": "string or null",
        "completed": "false",
        "created_at": "timestamp",
        "updated_at": "timestamp"
      }
    }
  }
  ```

#### FR-TASK-003: Get Specific Task
- **Endpoint**: `GET /api/{user_id}/tasks/{id}`
- **Purpose**: Retrieve a specific task by ID
- **Headers Required**: `Authorization: Bearer {token}`
- **Success Response (200)**:
  ```json
  {
    "success": true,
    "data": {
      "task": {
        "id": "integer",
        "user_id": "uuid-string",
        "title": "string",
        "description": "string or null",
        "completed": "boolean",
        "created_at": "timestamp",
        "updated_at": "timestamp"
      }
    }
  }
  ```

#### FR-TASK-004: Update Task
- **Endpoint**: `PUT /api/{user_id}/tasks/{id}`
- **Purpose**: Update an existing task
- **Headers Required**: `Authorization: Bearer {token}`, `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "title": "string (1-200 chars)",
    "description": "string (max 1000 chars, optional)"
  }
  ```
- **Success Response (200)**:
  ```json
  {
    "success": true,
    "data": {
      "task": {
        "id": "integer",
        "user_id": "uuid-string",
        "title": "string",
        "description": "string or null",
        "completed": "boolean",
        "created_at": "timestamp",
        "updated_at": "timestamp"
      }
    }
  }
  ```

#### FR-TASK-007: Partial Update Behavior
- **Endpoint**: `PATCH /api/{user_id}/tasks/{id}`
- **Purpose**: Update specific fields of an existing task
- **Behavior**: For `PATCH` requests, fields set to `null` are ignored (do not un-set the value). Only fields with valid new values are updated.
- **Example**: If a request contains `{"title": "New Title", "description": null}`, only the title is updated, the description remains unchanged.
- **Validation**: Only provided fields are validated, missing fields are left as-is.

#### FR-TASK-005: Delete Task
- **Endpoint**: `DELETE /api/{user_id}/tasks/{id}`
- **Purpose**: Delete a task by ID
- **Headers Required**: `Authorization: Bearer {token}`
- **Success Response (200)**:
  ```json
  {
    "success": true,
    "data": {
      "message": "Task deleted successfully"
    }
  }
  ```

#### FR-TASK-006: Toggle Task Completion
- **Endpoint**: `PATCH /api/{user_id}/tasks/{id}/complete`
- **Purpose**: Toggle the completion status of a task
- **Headers Required**: `Authorization: Bearer {token}`
- **Success Response (200)**:
  ```json
  {
    "success": true,
    "data": {
      "task": {
        "id": "integer",
        "completed": "boolean",
        "updated_at": "timestamp"
      }
    }
  }
  ```

### 3.3 Security Requirements

#### FR-SEC-001: JWT Authentication
- All task endpoints require valid JWT token in Authorization header
- Token must be included as `Authorization: Bearer {token}`
- Invalid or missing tokens return 401 Unauthorized
- Token expiry handled automatically

#### FR-SEC-002: User Isolation
- API validates that user_id in URL matches JWT token user_id
- Users can only access their own tasks
- Requests for other users' tasks return 403 Forbidden
- Database queries always filter by user_id

#### FR-SEC-003: Input Validation
- All request bodies validated for required fields and data types
- String lengths validated according to specifications
- Malicious input sanitized to prevent injection attacks
- Invalid requests return 422 Validation Error

### 3.4 Error Handling

#### FR-ERR-001: Standard Error Format
All error responses follow the standard format consistently across all endpoints (both auth and task endpoints):
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

#### FR-ERR-002: Error Codes
| Code | HTTP Status | Description |
|------|-------------|-------------|
| EMAIL_EXISTS | 400 | Email already registered |
| INVALID_CREDENTIALS | 401 | Invalid email/password |
| UNAUTHORIZED | 401 | Missing or invalid JWT token |
| FORBIDDEN | 403 | User cannot access resource |
| NOT_FOUND | 404 | Resource not found |
| VALIDATION_ERROR | 422 | Invalid input data |
| SERVER_ERROR | 500 | Internal server error |

## 4. Non-Functional Requirements

### 4.1 Deployment & Runtime

#### NFR-DEPLOY-001: Hugging Face Spaces Deployment
- Backend must be deployable to Hugging Face Spaces using Docker
- Application must listen on port **7860** (Hugging Face default) to receive traffic
- File system is read-only at runtime (except `/tmp`) - no writes to application directories
- All database migrations must run during the build phase or via a separate command (not implicit on startup)
- Application must load sensitive config (DB_URL, JWT_SECRET) from `HF_SPACE_SECRETS` environment variables

### 4.2 Performance

#### NFR-PERF-001: Response Times
- GET requests: < 100ms (95th percentile)
- POST/PUT/PATCH requests: < 200ms (95th percentile)
- DELETE requests: < 100ms (95th percentile)
- Authentication requests: < 300ms (95th percentile)

#### NFR-PERF-003: Date Format
- All timestamps must be returned in UTC ISO 8601 format (e.g., `2026-01-16T10:30:00Z`)
- All timestamp fields in API responses use this format consistently
- Database stores all timestamps in UTC timezone

#### NFR-PERF-004: Concurrency
- Support 1000+ concurrent users
- Handle 100+ requests per second per user
- Maintain response times under load

### 4.3 Security

#### NFR-SEC-001: Transport Security
- All API endpoints require HTTPS
- Automatic redirect from HTTP to HTTPS
- HSTS headers enabled

#### NFR-SEC-005: CORS Policy
- API must allow CORS from the frontend domain (Vercel deployment) and `localhost` only
- Do NOT allow all origins (`*`) for security reasons
- Configure specific allowed origins in environment variables
- Include credentials in allowed headers if using cookie-based auth

#### NFR-SEC-002: Secrets Management
- Application must load sensitive config (DB_URL, JWT_SECRET) from `HF_SPACE_SECRETS` environment variables
- No hardcoded secrets in source code
- Secrets validation: check for presence of required secrets at startup
- Secure handling of secrets in memory (avoid logging, etc.)

#### NFR-SEC-003: Rate Limiting
- Authentication endpoints: 5 requests per minute per IP
- Task API endpoints: 100 requests per minute per user
- Exponential backoff for repeated failures

### 4.4 Availability

#### NFR-AVAIL-001: Uptime
- 99.9% uptime during business hours
- Planned maintenance windows announced 48 hours in advance
- Automatic failover to backup systems

### 4.5 Reliability & Error Handling

#### NFR-REL-001: Network Timeouts
- API clients must handle requests that take longer than 30 seconds
- UI should display a "Retry" button for timed-out requests
- Backend should return appropriate timeout responses when possible
- Default timeout for API requests: 30 seconds

#### NFR-REL-002: Rate Limiting
- API must reject requests > 100/min per user with 429 Too Many Requests
- Authentication endpoints limited to 5 requests per minute per IP
- Rate limit headers should be included in responses when approaching limits
- Exponential backoff recommended for client retries

#### NFR-REL-003: Database Downtime
- System must return 503 Service Unavailable if storage is unreachable
- Response must include Retry-After header for client retry scheduling
- Backend should implement circuit breaker pattern for database connections
- Error logs must capture database connection failures for monitoring
- Graceful degradation: cache responses when possible during partial outages

#### NFR-REL-004: Network Partitions
- System must handle transient network failures during token validation by retrying internal calls before failing
- Default retry policy: exponential backoff starting at 100ms, max 3 retries
- Circuit breaker pattern should be implemented for external service dependencies
- Fallback mechanisms should be in place for critical operations

#### NFR-REL-005: Concurrent Updates
- System must handle concurrent requests to the same resource using database-level locking or optimistic concurrency control to prevent data corruption
- API should return the most recent version of data after concurrent updates
- UI should show latest data after update operations
- Conflict resolution strategy: Last-Write-Wins with appropriate user notification

#### NFR-REL-006: Empty List Handling
- If no resources are found for a list endpoint (e.g., `GET /api/{user_id}/tasks`), return `200 OK` with an empty array `[]` (Do NOT return 404)
- This applies to all list endpoints across the API
- Frontend should handle empty arrays appropriately with user-friendly messaging

## 5. Success Criteria

API is complete when:
- ✓ All endpoints return proper HTTP status codes
- ✓ JWT authentication protects all task endpoints
- ✓ User isolation prevents unauthorized access
- ✓ Input validation prevents malicious data
- ✓ Error responses follow standard format
- ✓ Response times meet performance requirements
- ✓ API tests pass (> 80% coverage)
- ✓ Security measures prevent common vulnerabilities
- ✓ Documentation matches implementation

## 6. Assumptions

- Clients can handle JSON requests/responses
- Clients properly include JWT tokens in headers
- Network connectivity is available for API communication
- Database is accessible and responsive
- Authentication service is available

## 7. Key Entities

- **API Endpoint**: RESTful interface for client-server communication
- **JWT Token**: Authentication token for securing endpoints
- **User**: Identity context for task ownership and access control
- **Task**: Core data entity managed through the API