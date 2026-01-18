---
id: 25
title: implement-missing-patch-endpoints-t006
stage: green
date: 2026-01-16
surface: agent
model: "openai/gpt-4o"
feature: phase-2-web-app
branch: main
user: metachemist
command: "/sp.implement"
labels: ["implementation", "api", "endpoints", "task-T-006"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/api/v1/endpoints/tasks.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/repositories/task_repository.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/scripts/test_task_endpoints.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/specs/3-tasks/phase-2-tasks.md
tests:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/scripts/test_task_endpoints.py
---

## Prompt

/sp.implement @constitution.md
# ROLE
Act as a Principal Backend Architect.

# CONTEXT
We are re-implementing **Task T-006**.
The current `tasks.py` router implements GET, POST, PUT, and DELETE.
However, it is **missing** the PATCH endpoints required by the specification.

# TASK
Update `backend/src/api/v1/endpoints/tasks.py` to implement the missing functionality.

# SPECIFICATIONS

## 1. PATCH Endpoint (Partial Update)
- **Path**: `PATCH /{task_id}`
- **Input**: `TaskUpdate` (SQLModel)
- **Logic**:
  - Fetch task by ID (ensure ownership).
  - Update *only* the fields provided in the request body (exclude unset fields).
  - Save to DB.
  - Return `TaskPublic`.

## 2. Toggle Complete Endpoint
- **Path**: `PATCH /{task_id}/complete`
- **Input**: None (Action-based).
- **Logic**:
  - Fetch task by ID (ensure ownership).
  - Flip the `.completed` boolean (True -> False, False -> True).
  - Save to DB.
  - Return `TaskPublic`.

# VERIFICATION
Update the test script `backend/scripts/test_task_endpoints.py` to include:
1.  Test Case: `test_patch_update` (Edit title only).
2.  Test Case: `test_toggle_complete` (Flip status).

# OUTPUT
Regenerate the code for:
1. `backend/src/api/v1/endpoints/tasks.py`
2. `backend/scripts/test_task_endpoints.py`

## Response snapshot

I have successfully implemented the missing PATCH endpoints for Task T-006:

1. **Added PATCH endpoint for partial updates** (`PATCH /{task_id}`):
   - Implemented `patch_update_task` function that accepts TaskUpdate model
   - Validates user ownership of the task
   - Updates only the fields provided in the request
   - Returns TaskPublic model

2. **Added PATCH endpoint for toggling completion** (`PATCH /{task_id}/complete`):
   - Implemented `toggle_task_completion` function
   - Validates user ownership of the task
   - Flips the completion status (True ↔ False)
   - Updates the updated_at timestamp
   - Returns TaskPublic model

3. **Updated repository layer** in `task_repository.py`:
   - Added `toggle_completion` method that handles the completion status toggle
   - Updated the method to return the appropriate model type

4. **Enhanced test coverage** in `test_task_endpoints.py`:
   - Added test for partial update (PATCH) endpoint
   - Added test for completion toggle endpoint
   - Updated all test numbering to reflect the new endpoints
   - Verified all endpoints work correctly with mocked data

The implementation now includes all required endpoints for the task management API as specified in the requirements. The endpoints properly validate user ownership of tasks and return the appropriate response models.

## Outcome

- ✅ Impact: Successfully implemented missing PATCH endpoints for task management
- 🧪 Tests: Added comprehensive tests for both new endpoints
- 📁 Files: Updated tasks endpoint, repository, and test files
- 🔁 Next prompts: Ready to proceed with remaining tasks
- 🧠 Reflection: API now fully compliant with specification requirements

## Evaluation notes (flywheel)

- Failure modes observed: Previously missing PATCH endpoints for partial updates and completion toggling
- Graders run and results (PASS/FAIL): All tests pass successfully
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test with actual database integration