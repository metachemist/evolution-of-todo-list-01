---
id: 18
title: implement-tasks-t009-t010-enhance-display-and-test-view
stage: green
date: 2026-01-16
surface: agent
model: "openai/gpt-4o"
feature: phase-1-console
branch: 3-phase-1-tasks
user: metachemist
command: "/sp.implement"
labels: ["implementation", "ui", "testing", "task-T-009", "task-T-010"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/src/cli/interface.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/tests/unit/test_view_tasks.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/specs/3-tasks/phase-1-tasks.md
tests:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/tests/unit/test_view_tasks.py
---

## Prompt

/sp.implement @constitution.md
# ROLE
Act as a Python Frontend Developer (CLI Specialist).

# CONTEXT
We are improving the UX.
Current Tasks: **T-009 (Enhance Display) & T-010 (Test View)**.

# INPUTS
1. `specs/3-tasks/phase-1-tasks.md` (Read T-009 & T-010).
2. `specs/1-specify/features/feature-01-task-crud.md` (Reference the "CLI Interaction Examples" for the exact table format).

# TASK: IMPLEMENT T-009 & T-010
1. Modify `src/cli/interface.py` to format the task list beautifully.
2. Verify it with tests.

# REQUIREMENTS
1. **Formatting Logic (T-009)**:
   - Pending: `1 | [ ] | Buy Milk`
   - Completed: `2 | [x] | Walk Dog`
   - With Desc: `3 | [ ] | Code - Write Python`
   - Empty: Print "No tasks in your list".
2. **Testing (T-010)**:
   - Create `tests/unit/test_view_tasks.py`.
   - Mock the service to return a list of tasks.
   - Capture stdout and assert the string formatting matches exactly.

# OUTPUT
1. Updated code for `src/cli/interface.py`.
2. Code for `tests/unit/test_view_tasks.py`.
3. Command to run tests.

## Response snapshot

I have successfully implemented both Task T-009 (Enhance Task Display Format) and Task T-010 (Test View Task Functionality) by:

1. Updating src/cli/interface.py to enhance the display format:
   - Modified the _handle_view method to properly format tasks
   - Implemented the format: 'ID | [ ] | Title' for pending tasks
   - Implemented the format: 'ID | [x] | Title' for completed tasks
   - Added support for descriptions: 'ID | [ ] | Title - Description'
   - Maintained the "No tasks in your list" message for empty lists
   - Ensured proper spacing and alignment in the table format

2. Creating comprehensive tests in tests/unit/test_view_tasks.py covering:
   - Proper formatting of tasks with mixed completion statuses
   - Display of tasks with and without descriptions
   - Handling of empty task lists
   - Verification that the display format matches spec requirements
   - All tests use mocking to isolate the CLI display functionality

3. Running the tests successfully to verify all functionality works as expected

4. Updating both task entries in the tasks file to mark them as completed

## Outcome

- ✅ Impact: Successfully completed Tasks T-009 and T-010 - Enhanced display and testing implemented
- 🧪 Tests: All 6 tests in test_view_tasks.py pass successfully
- 📁 Files: Updated src/cli/interface.py and created tests/unit/test_view_tasks.py with complete functionality
- 🔁 Next prompts: Ready to proceed with Task T-011 - Implement Task Update Functionality
- 🧠 Reflection: The task display is now properly formatted according to the specification with comprehensive test coverage.

## Evaluation notes (flywheel)

- Failure modes observed: Initially missing 'capsys' parameter in test functions, but fixed quickly
- Graders run and results (PASS/FAIL): PASS - All 6 tests pass successfully after fixes
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with Task T-011 implementation