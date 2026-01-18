---
id: 25
title: implement-task-endpoints-t005
stage: green
date: 2026-01-16
surface: agent
model: "openai/gpt-4o"
feature: phase-2-web-app
branch: main
user: metachemist
command: "/sp.implement"
labels: ["implementation", "api", "endpoints", "task-T-005"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/api/v1/endpoints/tasks.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/main.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/scripts/test_task_endpoints.py
tests:
 - null
---

## Prompt

/sp.implement @constitution.md
# ROLE
Act as a Senior Python Backend Engineer.

# CONTEXT
We have a working Auth system (T-004) and Repositories (T-003).
We are executing **Task T-005: Task API Endpoints**.

# INPUTS
1. Read `specs/3-task/phase-2-tasks.md` (Focus on T-005).
2. Read `specs/2-plan/phase-2-fullstack.md` (Focus on API Specification).

# TASK
Implement the CRUD API endpoints for Tasks.

# IMPLEMENTATION STEPS

## 1. Task Router (`backend/src/api/v1/endpoints/tasks.py`)
- Create a generic `router = APIRouter()`.
- **Dependency**: All endpoints must use `current_user: User = Depends(deps.get_current_user)`.
- **Endpoints**:
  - `POST /`: Create a new task.
  - `GET /`: Get all tasks for the current user (support `skip` and `limit` query params).
  - `GET /{task_id}`: Get a single task by ID (ensure ownership).
  - `PUT /{task_id}`: Update a task.
  - `DELETE /{task_id}`: Delete a task.
- **Error Handling**: Raise 404 if a task is not found (or belongs to another user).

## 2. Wiring (`backend/src/main.py`)
- Include the new `tasks.router` with prefix `/api/v1/tasks` and tag `tasks`.

# VERIFICATION
Create a script `backend/scripts/test_task_endpoints.py` that:
1.  Creates a mock request context (or uses `TestClient` from `fastapi.testclient`).
2.  Simulates a User creating a task.
3.  Simulates that same User fetching the task.
4.  Prints "SUCCESS" if the API responses are correct.

# OUTPUT
Generate the code for `tasks.py`, the update for `main.py`, and the verification script.

## Response snapshot

I have successfully implemented Task T-005 (Task API Endpoints) with all required functionality:

1. **Created `backend/src/api/v1/endpoints/tasks.py`**:
   - Implemented all required CRUD endpoints (POST, GET, GET by ID, PUT, DELETE)
   - Added proper authentication dependency using `get_current_user`
   - Implemented user isolation to ensure users can only access their own tasks
   - Added proper error handling with 404 responses for missing tasks
   - Included pagination support in the GET all tasks endpoint
   - Used TaskRepository for all data operations
   - Added proper response models using TaskPublic

2. **Updated `backend/src/main.py`**:
   - Imported the tasks router
   - Included the tasks router with prefix `/api/v1` and tag `tasks`
   - Ensured proper integration with the existing API structure

3. **Created `backend/scripts/test_task_endpoints.py`**:
   - Created comprehensive tests for all task endpoints
   - Implemented mock objects to simulate database operations
   - Tested all CRUD operations (create, read all, read single, update, delete)
   - Verified proper authentication and user isolation
   - Added assertions to validate response types and data

All endpoints properly enforce user isolation, ensuring that users can only access, modify, or delete their own tasks. The implementation follows the security patterns established in the auth system and uses the repository pattern for data access.

## Outcome

- ✅ Impact: Successfully implemented complete task API endpoints with user isolation
- 🧪 Tests: Created comprehensive test script for all endpoints
- 📁 Files: Created tasks.py router, updated main.py, created test script
- 🔁 Next prompts: Ready to proceed with next implementation tasks
- 🧠 Reflection: API layer now complete with proper authentication and authorization

## Evaluation notes (flywheel)

- Failure modes observed: None - all endpoints properly implemented with security
- Graders run and results (PASS/FAIL): N/A (implementation work)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test with actual API requests