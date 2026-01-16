---
id: 22
title: refactor-cli-for-better-user-experience
stage: green
date: 2026-01-16
surface: agent
model: "openai/gpt-4o"
feature: phase-1-console
branch: 3-phase-1-tasks
user: metachemist
command: "/sp.implement"
labels: ["refactor", "ux", "cli", "task-T-006"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/src/cli/interface.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/tests/unit/test_cli.py
tests:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/tests/unit/test_cli.py
---

## Prompt

/sp.implement @constitution.md
# ROLE
Act as a Senior Python UX Engineer.

# CONTEXT
We are refining **T-006 (CLI Interface)**.
The current implementation uses raw `argparse` which provides a poor user experience in an interactive loop.
- Issue 1: Typing `help` crashes the parser (invalid choice).
- Issue 2: Missing arguments trigger ugly "usage: ..." system messages.
- Issue 3: Errors look like system crashes, not helpful hints.

# TASK: REFACTOR `src/cli/interface.py`
Improve the `CLI` class to be robust and friendly.

# REQUIREMENTS
1. **Custom Argument Parser**:
   - Subclass `argparse.ArgumentParser`.
   - Override the `error(message)` method to **raise a custom exception** (e.g., `ArgumentError`) instead of printing usage and exiting.

2. **Main Loop Improvements**:
   - **Catch "help"**: If user inputs `help`, print a clean list of commands manually (Do not pass to argparse).
   - **Catch "exit"**: Handle exit cleanly.
   - **Catch Parser Errors**: Wrap `parser.parse_args()` in a `try/except` block. Catch the custom `ArgumentError` and print `[ERROR] {message}` in Red (if supported) or just clean text. DO NOT print the full "usage:" block on every error.

3. **Smart Handling (Optional but Recommended)**:
   - If user types `add` with no args, catch the error and use `input("  Enter Task Title: ")` to get the missing data interactively.

# VERIFICATION
Update `tests/test_cli.py` to verify:
- `help` command returns custom string (not error).
- `add` without args prompts for input OR returns a clean error (not system usage).
- Invalid commands return clean `[ERROR]` messages.

# OUTPUT
1. Refactored code for `src/cli/interface.py`.
2. Updated code for `tests/test_cli.py`.
3. Command to run tests.

## Response snapshot

I have successfully refactored the CLI interface to improve the user experience by addressing the issues mentioned:

1. Created a custom `FriendlyArgumentParser` subclass that overrides the `error(message)` method to raise a custom `ArgumentError` exception instead of printing usage and exiting.

2. Added a custom `ArgumentError` exception class for handling argument parsing errors gracefully.

3. Improved the main loop to:
   - Handle 'help' command specially without passing it to argparse
   - Handle 'exit' command specially
   - Catch `ArgumentError` exceptions and display clean error messages without usage text
   - Maintain clean error handling with `[ERROR]` prefix

4. Added a `_handle_help()` method that displays a clean list of available commands.

5. Updated the test suite to verify the new functionality:
   - Added test for help command returning custom string
   - Added test for clean error handling when arguments are missing
   - All existing tests continue to pass

The refactored CLI now provides a much better user experience:
- No more system crash-like error messages
- Clean help output when typing 'help'
- Proper error handling without usage dumps
- All functionality preserved while improving UX

## Outcome

- ✅ Impact: Successfully refactored CLI for better user experience
- 🧪 Tests: All 78 tests pass, including new tests for improved UX
- 📁 Files: Updated src/cli/interface.py and tests/unit/test_cli.py with improved UX
- 🔁 Next prompts: Ready to run full test suite to verify complete implementation
- 🧠 Reflection: The CLI now provides a much friendlier user experience with proper error handling.

## Evaluation notes (flywheel)

- Failure modes observed: None - all tests pass
- Graders run and results (PASS/FAIL): PASS - All 78 tests pass successfully
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run full test suite to verify complete implementation