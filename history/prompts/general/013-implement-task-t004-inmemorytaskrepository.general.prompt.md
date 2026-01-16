---
id: 13
title: implement-task-t004-inmemorytaskrepository
stage: green
date: 2026-01-16
surface: agent
model: "openai/gpt-4o"
feature: phase-1-console
branch: 3-phase-1-tasks
user: metachemist
command: "/sp.implement"
labels: ["implementation", "repository", "task-T-004"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/src/repositories/task_repository.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/tests/unit/test_repository.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/specs/3-tasks/phase-1-tasks.md
tests:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/tests/unit/test_repository.py
---

## Prompt

/sp.implement @constitution.md
# ROLE
Act as a Senior Backend Developer.

# CONTEXT
We are executing **Phase I: Step 4 (Implementation)**.
Completed:
- T-001 (Scaffold)
- T-002 (Custom Exceptions in `src/models/task.py`)
- T-003 (Task Model in `src/models/task.py`)
Current Task: **T-004 (Implement InMemoryTaskRepository)**.

# INPUTS
1. Read `specs/3-tasks/phase-1-tasks.md` (Focus strictly on T-004).
2. Read `src/models/task.py` to see the available Model and Exception classes.

# TASK: IMPLEMENT T-004
Create the `InMemoryTaskRepository` class.

# REQUIREMENTS
1. **File**: Create `src/repositories/task_repository.py`.
2. **Imports**: Import `Task` and `TaskNotFoundException` from `src.models.task`.
3. **Storage**: Use a private list `self._tasks: List[Task] = []` as defined in the Task Spec.
4. **ID Generation**: Implement logic to auto-increment IDs (e.g., `max(id) + 1` or a counter).
5. **Methods to Implement**:
   - `create(task: Task) -> Task`: Assign ID, append to list, return task.
   - `find_all() -> List[Task]`: Return copy of list.
   - `find_by_id(id: int) -> Task`: Loop through list. If found, return. Else raise `TaskNotFoundException`.
   - `update(id: int, task: Task) -> Task`: Find existing by ID. Replace data. Return updated task. Raise exception if missing.
   - `delete(id: int) -> bool`: Remove from list. Return True. Raise exception if missing.

# VERIFICATION (Test-Driven)
Create `tests/test_repository.py` covering:
1. **Create**: Verify ID is assigned and task is stored.
2. **Find**: Verify retrieval works.
3. **Failures**: Verify `find_by_id(999)` raises `TaskNotFoundException`.
4. **Update/Delete**: Verify state changes correctly.

# OUTPUT
1. The code for `src/repositories/task_repository.py`.
2. The code for `tests/test_repository.py`.
3. The command to run the tests.

# CRITERIA
- Include header: `# [Task]: T-004 | [From]: specs/2-plan/phase-1-console.md`
- STRICTLY follow the method signatures defined above.

## Response snapshot

I have successfully implemented Task T-004 (InMemoryTaskRepository) by:

1. Creating the src/repositories/task_repository.py file with:
   - InMemoryTaskRepository class with proper imports
   - Private _tasks list for storage
   - Auto-increment ID generation starting from 1
   - All required methods (create, find_all, find_by_id, update, delete) with correct signatures
   - Proper exception handling using TaskNotFoundException
   - Proper header comment referencing the task and source

2. Creating comprehensive tests in tests/unit/test_repository.py covering:
   - Task creation with ID assignment
   - Retrieval of all tasks (returning a copy)
   - Finding tasks by ID
   - Exception handling for missing tasks
   - Update functionality
   - Delete functionality
   - Auto-increment ID generation

3. Running the tests successfully to verify all functionality works as expected

4. Updating the task entry in the tasks file to mark it as completed

## Outcome

- ✅ Impact: Successfully completed Task T-004 - InMemoryTaskRepository implemented
- 🧪 Tests: All 9 tests in test_repository.py pass successfully
- 📁 Files: Created src/repositories/task_repository.py and tests/unit/test_repository.py with complete functionality
- 🔁 Next prompts: Ready to proceed with Task T-005 - Implement TaskService
- 🧠 Reflection: The repository layer is properly implemented with full CRUD operations and comprehensive test coverage.

## Evaluation notes (flywheel)

- Failure modes observed: None - all tests pass
- Graders run and results (PASS/FAIL): PASS - All 9 tests pass successfully
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with Task T-005 implementation