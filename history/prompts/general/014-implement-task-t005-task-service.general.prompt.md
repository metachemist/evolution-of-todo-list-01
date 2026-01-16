---
id: 14
title: implement-task-t005-task-service
stage: green
date: 2026-01-16
surface: agent
model: "openai/gpt-4o"
feature: phase-1-console
branch: 3-phase-1-tasks
user: metachemist
command: "/sp.implement"
labels: ["implementation", "service-layer", "task-T-005"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/src/services/task_service.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/tests/unit/test_service.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/specs/3-tasks/phase-1-tasks.md
tests:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/tests/unit/test_service.py
---

## Prompt

/sp.implement @constitution.md
# ROLE
Act as a Senior Python Developer.

# CONTEXT
We are executing **Phase I: Step 4 (Implementation)**.
Completed: T-001 through T-004 (Repository is ready).
Current Task: **T-005 (Implement TaskService)**.

# INPUTS
1. `specs/3-tasks/phase-1-tasks.md` (Read T-005).
2. `specs/2-plan/phase-1-console.md` (Read Service Layer architecture).
3. `src/repositories/task_repository.py` (To understand the dependency).
4. `src/models/task.py` (To understand the data).

# TASK: IMPLEMENT T-005
Create the `TaskService` class.

# REQUIREMENTS
1. **File**: `src/services/task_service.py`.
2. **Dependency**: Constructor must accept an instance of `InMemoryTaskRepository`.
3. **Methods**:
   - `add_task(title, description)`: Create `Task` object, validate inputs, call repo.create.
   - `get_all_tasks()`: Call repo.find_all.
   - `update_task(id, title, description)`: Call repo.update. Handle partial updates (keep existing values if new ones are None).
   - `delete_task(id)`: Call repo.delete.
   - `toggle_complete(id)`: Get task, flip `completed` status, save back to repo.
4. **Validation**: Ensure `title` is not empty (redundant check alongside Model is good practice).
5. **Error Handling**: Allow `TaskNotFoundException` to bubble up (do not catch it here; the CLI handles it).

# VERIFICATION
Create `tests/test_service.py`:
- Test `add_task` success.
- Test `toggle_complete` flips status True <-> False.
- Test `update_task` preserves old description if only title is changed.

# OUTPUT
1. Code for `src/services/task_service.py`.
2. Code for `tests/test_service.py`.
3. Command to run tests.

# CRITERIA
- Use header: `# [Task]: T-005 | [From]: specs/2-plan/phase-1-console.md`

## Response snapshot

I have successfully implemented Task T-005 (TaskService) by:

1. Creating the src/services/task_service.py file with:
   - TaskService class with InMemoryTaskRepository dependency
   - All required methods (add_task, get_all_tasks, update_task, delete_task, toggle_complete)
   - Proper input validation including checking for empty titles
   - Partial update handling in update_task method
   - Proper exception handling allowing TaskNotFoundException to bubble up
   - Proper header comment referencing the task and source

2. Creating comprehensive tests in tests/unit/test_service.py covering:
   - Successful task addition
   - Task addition without description
   - Validation of empty titles
   - Retrieval of all tasks
   - Partial updates preserving old values
   - Full updates of both title and description
   - Validation in updates
   - Toggle complete functionality flipping status
   - Task deletion
   - Error handling for non-existent tasks

3. Running the tests successfully to verify all functionality works as expected

4. Updating the task entry in the tasks file to mark it as completed

## Outcome

- ✅ Impact: Successfully completed Task T-005 - TaskService implemented
- 🧪 Tests: All 12 tests in test_service.py pass successfully
- 📁 Files: Created src/services/task_service.py and tests/unit/test_service.py with complete functionality
- 🔁 Next prompts: Ready to proceed with Task T-006 - Implement CLI Interface
- 🧠 Reflection: The service layer is properly implemented with full business logic and comprehensive test coverage.

## Evaluation notes (flywheel)

- Failure modes observed: None - all tests pass
- Graders run and results (PASS/FAIL): PASS - All 12 tests pass successfully
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with Task T-006 implementation