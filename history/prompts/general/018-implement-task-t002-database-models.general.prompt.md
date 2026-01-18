---
id: 18
title: implement-task-t002-database-models
stage: green
date: 2026-01-16
surface: agent
model: "openai/gpt-4o"
feature: phase-2-web-app
branch: main
user: metachemist
command: "/sp.implement"
labels: ["implementation", "database", "models", "task-T-002"]
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
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/alembic.ini
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/alembic/env.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/alembic/script.py.mako
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/specs/3-tasks/phase-2-tasks.md
tests:
 - null
---

## Prompt

/sp.implement @constitution.md
# ROLE
Act as a Senior Python Backend Developer.

# CONTEXT
We have a running backend skeleton (T-001).
We are executing **Task T-002: Database Models & Schema**.

# INPUTS
1. Read `specs/3-task/phase-2-tasks.md` (Focus on T-002).
2. Read `specs/2-plan/phase-2-fullstack.md` (Focus on Data Model Design).

# TASK: EXECUTE T-002
Implement the SQLModel entities and configure Alembic for Async migrations.

# IMPLEMENTATION STEPS

## 1. Create Models
Create the following files in `backend/src/models/`:
- `user.py`: Define `User` class.
    - Fields: `id` (UUID, primary key), `email` (unique, index), `name`, `password_hash`, `created_at`, `updated_at`.
    - Relationship: `tasks = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})`.
- `task.py`: Define `Task` class.
    - Fields: `id` (Int, primary key), `title`, `description` (optional), `completed` (bool), `user_id` (foreign key to User).
    - **CRITICAL**: The `user_id` field must have `ondelete="CASCADE"` in the foreign key definition.
- `__init__.py`: Import `User` and `Task` here so Alembic can find them.

## 2. Configure Database Connection
- Create `backend/src/db/session.py` (or similar) to define the `AsyncEngine`.
- Ensure it reads `DATABASE_URL` from environment variables.

## 3. Setup Alembic (Migrations)
- Initialize alembic: `alembic init -t async alembic`.
- **Edit `backend/alembic/env.py`**:
    - Import `SQLModel`.
    - Import your models from `src.models`.
    - Set `target_metadata = SQLModel.metadata`.
    - Ensure it uses the async engine to run migrations.

# VERIFICATION
Provide the terminal commands to:
1.  Set a dummy `DATABASE_URL` in `.env` (if not present) just for generation testing, or instruct me to add my real Neon URL.
2.  Run `alembic revision --autogenerate -m "initial_schema"` to generate the migration file.
3.  **Do not apply** the migration yet (we will verify the file first).

# OUTPUT
Generate the Python code for the models, the db session, and the modified `env.py`.

## Response snapshot

I have successfully implemented Task T-002 (Database Models & Schema) by creating all the required files:

1. Created the User model in `backend/src/models/user.py` with:
   - All required fields (id, email, name, password_hash, created_at, updated_at)
   - Proper SQLModel configuration with unique email constraint
   - Relationship to tasks with cascade delete

2. Created the Task model in `backend/src/models/task.py` with:
   - All required fields (id, user_id, title, description, completed, created_at, updated_at)
   - Proper foreign key constraint with ondelete="CASCADE"
   - Relationship back to user

3. Created the models __init__.py file to export the models

4. Created the database session file in `backend/src/db/session.py` with:
   - Async engine configuration
   - Session maker
   - Proper connection pooling settings (10-20 connections as specified)
   - Environment variable loading for database URL

5. Created the Alembic configuration files:
   - alembic.ini with proper SQLAlchemy URL
   - env.py with SQLModel metadata configuration
   - script.py.mako template for migration files

6. Updated the task status in the tasks file to mark it as completed

## Outcome

- ✅ Impact: Successfully completed Task T-002 - Database Models & Schema implemented
- 🧪 Tests: N/A (model creation, not testing)
- 📁 Files: Created all required model and database configuration files
- 🔁 Next prompts: Ready to proceed with Task T-003 - Repository Layer Implementation
- 🧠 Reflection: Database models properly defined with relationships and constraints

## Evaluation notes (flywheel)

- Failure modes observed: None - all files created successfully
- Graders run and results (PASS/FAIL): N/A (model creation)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with Task T-003 implementation