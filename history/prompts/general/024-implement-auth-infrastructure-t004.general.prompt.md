---
id: 24
title: implement-auth-infrastructure-t004
stage: green
date: 2026-01-16
surface: agent
model: "openai/gpt-4o"
feature: phase-2-web-app
branch: main
user: metachemist
command: "/sp.implement"
labels: ["implementation", "authentication", "security", "api", "task-T-004"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/core/security.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/api/deps.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/api/v1/endpoints/auth.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/api/v1/endpoints/users.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/main.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/models/token.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/models/user.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/models/task.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/models/__init__.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/db/session.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/alembic/env.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/scripts/test_auth_flow.py
tests:
 - null
---

## Prompt

/sp.implement @constitution.md
# ROLE
Act as a Principal Backend Architect.

# CONTEXT
We are re-implementing **Task T-004** (Authentication & API Infrastructure) from scratch to ensure perfect alignment with the Specs and to resolve configuration issues.
Current State: The app is mistakenly trying to connect to `localhost` instead of the `DATABASE_URL` environment variable.

# TASK
Regenerate the 4 critical components of the Authentication Infrastructure.

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

## 4. Security Utilities (`backend/src/core/security.py`)
- Implement `verify_password(plain, hashed)` and `get_password_hash(password)`.
- Implement `create_access_token(subject: Union[str, Any], expires_delta: timedelta)`.
- Ensure it uses `python-jose` and `passlib`.

## 5. API Dependencies (`backend/src/api/deps.py`)
- Implement `get_current_user`.
    - It must decode the JWT token from the `Authorization` header.
    - It must use `UserRepository` to fetch the user from the DB.
    - **CRITICAL**: Raise `HTTPException(status_code=401)` if token is invalid or user not found.

## 6. Auth Router (`backend/src/api/v1/endpoints/auth.py`)
- `POST /signup`: Accepts `UserCreate`, creates user via Repo, returns `UserPublic`.
- `POST /login`: Accepts `OAuth2PasswordRequestForm`, verifies credentials, returns `Token` (access_token).

## 7. User Router (`backend/src/api/v1/endpoints/users.py`)
- `GET /me`: Uses `get_current_user` dependency to return the currently logged-in user.

## 8. Main API Wiring (`backend/src/main.py`)
- Include the routers (`auth_router` and `users_router`) into the main FastAPI app.
- Prefix them correctly (e.g., `/api/v1/auth`, `/api/v1/users`).

# VERIFICATION
Create a script `backend/scripts/test_auth_flow.py` that:
1.  Registers a new user via the API function (simulated).
2.  Logs in to get a Token.
3.  Decodes the token to verify it contains the correct User ID.
4.  Prints "SUCCESS" if the flow works.

# OUTPUT
Generate the code for `security.py`, `deps.py`, the routers, `main.py` updates, and the verification script.

## Response snapshot

I have successfully implemented Task T-004 (Authentication & API Infrastructure) with all required components:

1. **Security Utilities (`backend/src/core/security.py`)**:
   - Implemented `verify_password()` and `get_password_hash()` functions using passlib
   - Implemented `create_access_token()` with proper JWT handling
   - Added proper environment variable loading for SECRET_KEY
   - Removed the problematic get_current_user function that was causing circular imports

2. **API Dependencies (`backend/src/api/deps.py`)**:
   - Implemented `get_current_user()` dependency with proper JWT token decoding
   - Added proper error handling with HTTPException(401) for invalid tokens or missing users
   - Used UserRepository to fetch user from database based on token

3. **Auth Router (`backend/src/api/v1/endpoints/auth.py`)**:
   - Implemented `POST /signup` endpoint that accepts UserCreate and returns UserPublic
   - Implemented `POST /login` endpoint that accepts OAuth2PasswordRequestForm and returns Token
   - Added proper validation for existing emails during signup
   - Added proper credential verification during login

4. **User Router (`backend/src/api/v1/endpoints/users.py`)**:
   - Implemented `GET /me` endpoint that uses get_current_user dependency
   - Returns the currently authenticated user's public information

5. **Main API Wiring (`backend/src/main.py`)**:
   - Included auth_router and users_router with proper prefixes
   - Set up routing at `/api/v1/auth` and `/api/v1/users`

6. **Database Session (`backend/src/db/session.py`)**:
   - Added critical check for DATABASE_URL environment variable
   - Raises ValueError if DATABASE_URL is missing
   - Properly configured async engine with environment URL

7. **Alembic Configuration (`backend/alembic/env.py`)**:
   - Forced configuration to use DATABASE_URL from environment variables
   - Implemented async migration pattern to prevent MissingGreenlet errors

8. **Token Model (`backend/src/models/token.py`)**:
   - Created Token model for authentication responses
   - Created TokenData model for holding user information from JWT

9. **Test Script (`backend/scripts/test_auth_flow.py`)**:
   - Created verification script that tests the complete auth flow
   - Simulates user registration, login, and token verification

All components are now properly configured to use the DATABASE_URL environment variable instead of defaulting to localhost. The authentication infrastructure is complete and ready for use.

## Outcome

- ✅ Impact: Successfully implemented complete authentication infrastructure (T-004)
- 🧪 Tests: Created auth flow verification script
- 📁 Files: Created/updated 11 files across models, security, API endpoints, and configuration
- 🔁 Next prompts: Ready to proceed with next task in implementation sequence
- 🧠 Reflection: Authentication layer now properly configured with security best practices

## Evaluation notes (flywheel)

- Failure modes observed: Previously had configuration loading issues causing localhost connection
- Graders run and results (PASS/FAIL): N/A (implementation work)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test the authentication endpoints with actual requests