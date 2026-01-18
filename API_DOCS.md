# Todo Evolution API Documentation

## Overview
The Todo Evolution API provides endpoints for managing user accounts and tasks. All endpoints require authentication using JWT tokens, except for the authentication endpoints.

## Authentication
Most endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

## Base URL
All API endpoints are prefixed with `/api/v1/`

## Endpoints

### Authentication

#### POST /api/v1/auth/signup
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "securePassword123"
}
```

**Response:**
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### POST /api/v1/auth/login
Authenticate a user and obtain a JWT token.

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "securePassword123"
}
```

**Response:**
```json
{
  "access_token": "jwt-token-string",
  "token_type": "bearer"
}
```

#### GET /api/v1/auth/me
Get the current user's profile information.

**Response:**
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### POST /api/v1/auth/signout
Sign out the current user (placeholder endpoint).

**Response:**
```json
{
  "message": "Successfully signed out"
}
```

#### PUT /api/v1/auth/profile
Update the current user's profile information.

**Request Body:**
```json
{
  "email": "newemail@example.com",
  "name": "John Smith",
  "password_hash": "new-hashed-password"
}
```

**Response:**
```json
{
  "id": "uuid-string",
  "email": "newemail@example.com",
  "name": "John Smith",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

### Tasks

#### GET /api/v1/tasks/
Get all tasks for the current user.

**Query Parameters:**
- `skip` (optional): Number of tasks to skip (default: 0)
- `limit` (optional): Maximum number of tasks to return (max: 100, default: 20)

**Response:**
```json
[
  {
    "id": 1,
    "title": "Sample Task",
    "description": "A sample task description",
    "completed": false,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
]
```

#### POST /api/v1/tasks/
Create a new task for the current user.

**Request Body:**
```json
{
  "title": "New Task",
  "description": "Task description",
  "completed": false
}
```

**Response:**
```json
{
  "id": 1,
  "title": "New Task",
  "description": "Task description",
  "completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### GET /api/v1/tasks/{id}
Get a specific task by ID.

**Response:**
```json
{
  "id": 1,
  "title": "Sample Task",
  "description": "A sample task description",
  "completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### PUT /api/v1/tasks/{id}
Update a specific task by ID.

**Request Body:**
```json
{
  "title": "Updated Task",
  "description": "Updated description",
  "completed": true
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Updated Task",
  "description": "Updated description",
  "completed": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### PATCH /api/v1/tasks/{id}
Partially update a specific task by ID.

**Request Body:**
```json
{
  "title": "Partially Updated Task"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Partially Updated Task",
  "description": "A sample task description",
  "completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### PATCH /api/v1/tasks/{id}/complete
Toggle the completion status of a specific task by ID.

**Response:**
```json
{
  "id": 1,
  "title": "Sample Task",
  "description": "A sample task description",
  "completed": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### DELETE /api/v1/tasks/{id}
Delete a specific task by ID.

**Response:**
```json
Status: 204 No Content
```

### Health Check

#### GET /health
Check the health status of the application.

**Response:**
```json
{
  "status": "ok",
  "database": "connected",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

#### GET /api/health
Alternative health check endpoint.

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "service": "todo-api",
    "database": "connected",
    "timestamp": "2023-01-01T00:00:00Z"
  }
}
```

## Rate Limits
- Authentication endpoints: 5 requests per minute per IP
- Task endpoints: 100 requests per minute per IP

## Error Responses
All error responses follow this format:
```json
{
  "detail": "Error message"
}
```

## Security Headers
All responses include security headers:
- Strict-Transport-Security
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection
- Referrer-Policy
- Permissions-Policy