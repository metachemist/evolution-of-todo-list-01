---
id: 19
title: implement-tasks-t011-t012-update-functionality-and-testing
stage: green
date: 2026-01-16
surface: agent
model: "openai/gpt-4o"
feature: phase-1-console
branch: 3-phase-1-tasks
user: metachemist
command: "/sp.implement"
labels: ["implementation", "update", "testing", "task-T-011", "task-T-012"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/tests/unit/test_update_task.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/specs/3-tasks/phase-1-tasks.md
tests:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/tests/unit/test_update_task.py
---

## Prompt

/sp.implement @constitution.md
# ROLE
Act as a Full-Stack Python Developer.

# CONTEXT
Current Tasks: **T-011 (Implement Update) & T-012 (Test Update)**.

# INPUTS
1. `specs/3-tasks/phase-1-tasks.md` (Read T-011 & T-012).

# TASK: IMPLEMENT T-011 & T-012
Enable modifying existing tasks.

# REQUIREMENTS
1. **Service Layer**: Ensure `update_task` in `src/services/task_service.py` allows partial updates (e.g., passing `None` for description keeps the old one).
2. **CLI Layer**: Update `src/cli/interface.py` to handle the `update <id> <title> [desc]` command.
3. **Testing**: Create `tests/unit/test_update_task.py`.
   - Test updating just the title.
   - Test updating a non-existent ID (assert Error).
   - Test validation (updating to empty title should fail).

# OUTPUT
1. Updated code for Service and CLI.
2. Code for `tests/unit/test_update_task.py`.
3. Command to run tests.

## Response snapshot

I have successfully implemented both Task T-011 (Implement Task Update Functionality) and Task T-012 (Test Update Task Functionality) by:

1. Verifying the existing implementation in src/services/task_service.py:
   - Confirmed that update_task method allows partial updates (passing None keeps old values)
   - Verified validation logic for empty titles
   - Confirmed proper error handling for non-existent IDs

2. Verifying the existing implementation in src/cli/interface.py:
   - Confirmed that CLI properly handles the update command with ID, title, and optional description
   - Verified success and error message formatting

3. Creating comprehensive tests in tests/unit/test_update_task.py covering:
   - Updating just the title while preserving other fields
   - Updating just the description while preserving other fields
   - Updating both title and description
   - Attempting to update a non-existent task (properly raises exception)
   - Attempting to update to an empty title (properly raises validation error)
   - Preservation of completion status during updates
   - Preservation of creation timestamp during updates
   - Partial updates with None values preserving original values

4. Running the tests successfully to verify all functionality works as expected

5. Updating both task entries in the tasks file to mark them as completed

## Outcome

- ✅ Impact: Successfully completed Tasks T-011 and T-012 - Update functionality and testing implemented
- 🧪 Tests: All 8 tests in test_update_task.py pass successfully
- 📁 Files: Created tests/unit/test_update_task.py with comprehensive test coverage
- 🔁 Next prompts: Ready to proceed with Task T-013 - Implement Complete and Delete Functionality
- 🧠 Reflection: The update functionality was already properly implemented with partial updates and validation.

## Evaluation notes (flywheel)

- Failure modes observed: None - all tests pass
- Graders run and results (PASS/FAIL): PASS - All 8 tests pass successfully
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with Task T-013 implementation