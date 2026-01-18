---
id: 23
title: reimpl-db-layer-with-env-var-fixes
stage: green
date: 2026-01-16
surface: agent
model: "openai/gpt-4o"
feature: phase-2-web-app
branch: main
user: metachemist
command: "/sp.implement"
labels: ["implementation", "database", "environment", "task-T-002"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/models/user.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/models/task.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/models/__init__.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/db/session.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/alembic/env.py
tests:
 - null
---

## Prompt

/sp.implement @constitution.md
# ROLE
Act as a Principal Backend Architect.

# CONTEXT
We are re-implementing **Task T-002** (Database Layer) from scratch to ensure perfect alignment with the Specs and to resolve configuration issues.
Current State: The app is mistakenly trying to connect to `localhost` instead of the `DATABASE_URL` environment variable.

# TASK
Regenerate the 4 critical components of the Database Layer.

# SPECIFICATIONS & REQUIREMENTS

## 1. The Models (`src/models/`)
- **File**: `backend/src/models/user.py`
  - Class `User`: `id` (UUID), `email` (unique), `password_hash`.
  - **Fix**: Use Forward Reference `tasks: List["Task"]` to prevent circular imports.
- **File**: `backend/src/models/task.py`
  - Class `Task`: `id`, `user_id` (Foreign Key), `title`, `completed`.
  - **Fix**: Use Forward Reference `user: Optional["User"]` to prevent circular imports.
  - **Constraint**: `user_id` must have `ondelete="CASCADE"`.
- **File**: `backend/src/models/__init__.py`
  - Export both `User` and `Task`.

## 2. The Database Session (`src/db/session.py`)
- **Logic**:
  - Load `DATABASE_URL` from `os.getenv`.
  - **Critical Check**: If `DATABASE_URL` is missing, raise a clear `ValueError`.
  - Create `AsyncEngine` using `create_async_engine(url, echo=True)`.
  - Create `AsyncSession` factory.

## 3. The Migrations (`alembic/env.py`)
- **Logic**: Use the **Async Pattern** to prevent `MissingGreenlet` errors.
- **Config**:
  - `config.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])` <-- **Force overwrite config from Env Var**.
  - Run migrations using `asyncio.run(run_async_migrations())`.
  - Import models from `src.models`.

# OUTPUT
Generate the full code for:
1. `backend/src/models/user.py`
2. `backend/src/models/task.py`
3. `backend/src/models/__init__.py`
4. `backend/src/db/session.py`
5. `backend/alembic/env.py`.

## Response snapshot

I have successfully re-implemented the database layer components with all critical fixes:

1. **Updated `backend/src/models/user.py`**:
   - Implemented forward reference for tasks relationship: `tasks: List["Task"]`
   - Used TYPE_CHECKING to prevent circular imports
   - Maintained all required fields and constraints
   - Added proper cascade settings for task deletion

2. **Updated `backend/src/models/task.py`**:
   - Implemented forward reference for user relationship: `user: Optional["User"]`
   - Used TYPE_CHECKING to prevent circular imports
   - Added `ondelete="CASCADE"` to the user_id foreign key
   - Maintained all required fields and validation constraints

3. **Created `backend/src/models/__init__.py`**:
   - Properly exports both User and Task models
   - Includes clear module documentation
   - Uses standard __all__ convention

4. **Updated `backend/src/db/session.py`**:
   - Added critical check for DATABASE_URL environment variable
   - Raises clear ValueError if DATABASE_URL is missing
   - Properly loads environment variables with load_dotenv()
   - Uses the correct async engine configuration

5. **Updated `backend/alembic/env.py`**:
   - Added critical check for DATABASE_URL environment variable
   - Force overwrite config from environment variable using `config.set_main_option`
   - Maintains the async migration pattern with asyncio and connectable.connect()
   - Ensures target_metadata includes both User and Task models
   - Uses proper model imports to avoid circular dependencies

All components now properly handle environment variables and prevent circular imports while maintaining all functionality.

## Outcome

- ✅ Impact: Successfully resolved database layer configuration and import issues
- 🧪 Tests: N/A (refactoring work, not testing)
- 📁 Files: Updated all 5 database layer files with proper environment handling and forward references
- 🔁 Next prompts: Ready to proceed with Alembic migrations and database setup
- 🧠 Reflection: Database layer now properly configured to use environment variables instead of localhost

## Evaluation notes (flywheel)

- Failure modes observed: Previously had localhost connection instead of environment variable
- Graders run and results (PASS/FAIL): N/A (refactoring work)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run Alembic migrations to verify environment variable handling works