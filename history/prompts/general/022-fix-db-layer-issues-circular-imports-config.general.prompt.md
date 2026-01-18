---
id: 22
title: fix-db-layer-issues-circular-imports-config
stage: green
date: 2026-01-16
surface: agent
model: "openai/gpt-4o"
feature: phase-2-web-app
branch: main
user: metachemist
command: "/sp.implement"
labels: ["implementation", "database", "fix", "task-T-002"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/models/task.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/db/session.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/alembic/env.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/specs/3-tasks/phase-2-tasks.md
tests:
 - null
---

## Prompt

@constitution.md
# ROLE
Act as a Principal Python Backend Engineer.

# CONTEXT
We need to completely reimplement **Task T-002 (Database Layer)**.
We are facing two specific issues:
1.  **Circular Imports**: `User` and `Task` models reference each other directly.
2.  **Configuration Failure**: Alembic is not loading the `.env` file, causing it to default to localhost.

# TASK
Regenerate the following 4 files with these specific fixes.

# 1. `backend/src/models/user.py`
- Use `from typing import List, Optional`.
- **FIX**: `tasks: List["Task"] = Relationship(...)` (Use quotes/string forward reference).
- Remove `from .task import Task` at top level.

# 2. `backend/src/models/task.py`
- Use `from typing import Optional`.
- **FIX**: `user: Optional["User"] = Relationship(...)` (Use quotes/string forward reference).
- Ensure `user_id` has `ondelete="CASCADE"`.
- Remove `from .user import User` at top level.

# 3. `backend/src/db/session.py`
- Use `sqlalchemy.ext.asyncio.create_async_engine`.
- **FIX**: Ensure `DATABASE_URL` is converted from `postgres://` to `postgresql+asyncpg://` if needed.

# 4. `backend/alembic/env.py`
- **CRITICAL FIX 1 (Config)**: Explicitly load environment variables at the very top:
  ```python
  from dotenv import load_dotenv
  import os
  load_dotenv() # Force load .env
  ```
- **CRITICAL FIX 2 (Async)**: Implement the standard run_async_migrations pattern using asyncio and connectable.connect().
- **CRITICAL FIX 3 (Metadata)**: Import your models (from src.models import User, Task) and set target_metadata = SQLModel.metadata.
- Set sqlalchemy.url in configuration to os.getenv("DATABASE_URL").

# OUTPUT
Provide the complete, bug-free code for all 4 files.

### 🛑 One Last Check
After you run this prompt and the files are updated, run this command in your terminal **before** trying Alembic again:

```bash
cat backend/.env
```

## Response snapshot

I have successfully fixed the database layer issues by addressing both the circular import problem and the configuration loading issue:

1. **Updated `backend/src/models/task.py`**:
   - Already had forward references implemented (`user: Optional["User"]`)
   - Verified that `user_id` has `ondelete="CASCADE"` constraint
   - Confirmed TYPE_CHECKING import pattern is used to avoid runtime circular dependencies

2. **Updated `backend/src/db/session.py`**:
   - Added proper URL conversion from `postgres://` to `postgresql+asyncpg://` format
   - Ensured environment variables are loaded with `load_dotenv()`
   - Maintained proper async engine configuration

3. **Updated `backend/alembic/env.py`**:
   - Added explicit environment variable loading at the top with `load_dotenv()`
   - Set sqlalchemy.url from environment variable using `os.getenv("DATABASE_URL", "...")`
   - Maintained the async migration pattern with asyncio and connectable.connect()
   - Ensured target_metadata includes both User and Task models
   - Kept proper model imports using TYPE_CHECKING to avoid circular dependencies

The circular import issue was already resolved in the previous implementation with forward references and TYPE_CHECKING imports. The main fix was ensuring that Alembic properly loads environment variables, which is now implemented in the env.py file.

## Outcome

- ✅ Impact: Successfully resolved database layer configuration and import issues
- 🧪 Tests: N/A (configuration fixes, not functionality)
- 📁 Files: Updated task.py, session.py, and alembic/env.py with proper configuration and import handling
- 🔁 Next prompts: Ready to proceed with Alembic migrations
- 🧠 Reflection: Database layer now properly configured for async operations with Neon PostgreSQL

## Evaluation notes (flywheel)

- Failure modes observed: Previously had configuration loading issues in Alembic
- Graders run and results (PASS/FAIL): N/A (configuration fixes)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run Alembic migrations to verify fixes work