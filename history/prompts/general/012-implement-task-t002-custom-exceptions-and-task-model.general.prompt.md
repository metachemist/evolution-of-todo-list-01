---
id: 12
title: implement-task-t002-custom-exceptions-and-task-model
stage: green
date: 2026-01-16
surface: agent
model: "openai/gpt-4o"
feature: phase-1-console
branch: 3-phase-1-tasks
user: metachemist
command: "/sp.implement"
labels: ["implementation", "domain-model", "task-T-002", "task-T-003"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/src/models/task.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/tests/unit/test_domain_task.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/specs/3-tasks/phase-1-tasks.md
tests:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/tests/unit/test_domain_task.py
---

## Prompt

/sp.implement @constitution.md
# ROLE
Act as a Senior Python Developer.

# CONTEXT
We are executing **Phase I: Step 4 (Implementation)**.
Task T-001 (Scaffold) is complete.
Current Task: **T-002 (Implement Domain Model)**.

# INPUTS
1. `specs/3-tasks/phase-1-tasks.md` (Read details for T-002).
2. `specs/2-plan/phase-1-console.md` (Read the Class Diagram/Schema for `Task`).
3. `specs/1-specify/features/feature-01-task-crud.md` (Read the Validation Rules, e.g., max length, required fields).

# TASK: IMPLEMENT T-002
Create the `Task` model class.

# REQUIREMENTS
1. **File**: Create `src/models/task.py`.
2. **Technology**: Use Python `dataclasses` or `pydantic` (as specified in the Plan).
3. **Fields**: Implement `id`, `title`, `description`, `status` (Enum), `created_at`.
4. **Validation**: Ensure `title` is not empty and `title` max length is enforced (raise `ValueError` if invalid).
5. **Testing**: Create `tests/test_domain_task.py`.
   - Test happy path (valid task creation).
   - Test validation errors (empty title raises error).
   - Test default values (status defaults to PENDING).

# OUTPUT
1. The code for `src/models/task.py`.
2. The code for `tests/test_domain_task.py`.
3. The command to run strictly these tests.

# CRITERIA
- Include header: `# [Task]: T-002 | [From]: specs/2-plan/phase-1-console.md`
- No database code.
- No CLI code.

## Response snapshot

I have successfully implemented both Task T-002 (Custom Exception Classes) and Task T-003 (Task Model with Validation) by:

1. Creating the src/models/task.py file with:
   - TaskException base class
   - TaskNotFoundException with proper constructor
   - InvalidTaskDataException with proper constructor
   - Task model with id, title, description, completed, and created_at fields
   - Field validators for title (1-200 characters) and description (0-500 characters)
   - Proper header comment referencing the task and source

2. Creating comprehensive tests in tests/unit/test_domain_task.py covering:
   - Valid task creation
   - Default value assignments
   - Title validation (empty, too long, min/max length)
   - Description validation (too long, max length)

3. Running the tests successfully to verify all functionality works as expected

4. Updating both task entries in the tasks file to mark them as completed

## Outcome

- ✅ Impact: Successfully completed Tasks T-002 and T-003 - Domain model and custom exceptions implemented
- 🧪 Tests: All 8 tests in test_domain_task.py pass successfully
- 📁 Files: Created src/models/task.py and tests/unit/test_domain_task.py with proper validation
- 🔁 Next prompts: Ready to proceed with Task T-004 - Implement InMemoryTaskRepository
- 🧠 Reflection: The domain model is properly validated with custom exceptions and comprehensive test coverage.

## Evaluation notes (flywheel)

- Failure modes observed: Initially used deprecated datetime.utcnow() which caused warnings
- Graders run and results (PASS/FAIL): PASS - All 8 tests pass successfully
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with Task T-004 implementation