---
id: 24
title: implement-auth-security-layer-t004-t005-t007
stage: green
date: 2026-01-16
surface: agent
model: "openai/gpt-4o"
feature: phase-2-web-app
branch: main
user: metachemist
command: "/sp.implement"
labels: ["implementation", "authentication", "security", "task-T-004", "task-T-005", "task-T-007"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/core/security.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/models/token.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/api/deps.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/api/v1/endpoints/auth.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/src/main.py
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/scripts/test_full_auth.py
tests:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/backend/scripts/test_full_auth.py
---

## Prompt

/sp.implement @constitution.md
# ROLE
Act as a Principal Backend Architect.

# CONTEXT
We are implementing the complete **Authentication & Security Layer** for a generic Todo App.
We are executing **Tasks T-004, T-005, and T-007** simultaneously to ensure perfect integration.

# GOAL
Implement the security utilities, authentication dependency (middleware), and authentication API endpoints in one unified pass.

# SPECIFICATIONS

## 1. Security Utilities (T-004)
- **File**: `backend/src/core/security.py`
- **Libs**: Use `passlib[bcrypt]` and `python-jose`.
- **Functions**:
  - `verify_password(plain: str, hashed: str) -> bool`
  - `get_password_hash(password: str) -> str`
  - `create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str`
- **Config**: Load `SECRET_KEY` and `ACCESS_TOKEN_EXPIRE_MINUTES` from environment (use defaults if missing).

## 2. Auth Dependency / Middleware (T-007)
- **File**: `backend/src/api/deps.py`
- **Logic**:
  - Define `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")`.
  - Define `async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> User`.
  - **Validation**: Decode token. If invalid or expired, raise 401. If user ID not found in DB, raise 401.

## 3. Auth API Endpoints (T-005)
- **File**: `backend/src/api/v1/endpoints/auth.py`
- **Router**: `router = APIRouter()`
- **Endpoints**:
  - `POST /signup`:
    - Input: `UserCreate`.
    - Logic: Check if email exists. Hash password. Create User via Repository.
    - Output: `UserPublic`.
  - `POST /login`:
    - Input: `OAuth2PasswordRequestForm`.
    - Logic: Find user. Verify password.
    - Output: `Token` (schema with `access_token` and `token_type`).
  - `GET /me` (Profile):
    - Input: `current_user = Depends(get_current_user)`.
    - Output: `UserPublic`.

## 4. Schemas (T-005 Support)
- **File**: `backend/src/models/token.py`
  - Define `Token` schema (`access_token: str`, `token_type: str`).
  - Define `TokenPayload` schema (`sub: Optional[str] = None`).

## 5. Main Integration
- **File**: `backend/src/main.py`
  - Include `auth.router` with prefix `/api/v1/auth` and tag `auth`.

# VERIFICATION SCRIPT
Create `backend/scripts/test_full_auth.py` that:
1. Registers a user (`/signup`).
2. Logs in (`/login`) to get a token.
3. Uses the token to fetch the profile (`/me`).
4. Prints "SUCCESS" only if all steps pass.

# OUTPUT
Generate the code for:
1. `backend/src/core/security.py`
2. `backend/src/models/token.py`
3. `backend/src/api/deps.py`
4. `backend/src/api/v1/endpoints/auth.py`
5. `backend/src/main.py` (Update)
6. `backend/scripts/test_full_auth.py`

## Response snapshot

I have successfully implemented the complete authentication and security layer for Tasks T-004, T-005, and T-007:

1. **Created `backend/src/core/security.py`**:
   - Implemented `verify_password()` function using passlib's bcrypt context
   - Implemented `get_password_hash()` function using bcrypt hashing
   - Implemented `create_access_token()` function using python-jose JWT library
   - Added proper environment variable loading for SECRET_KEY and ACCESS_TOKEN_EXPIRE_MINUTES
   - Configured default values for security parameters

2. **Created `backend/src/models/token.py`**:
   - Defined `Token` model with `access_token` and `token_type` fields
   - Defined `TokenPayload` model with optional `sub` field for JWT payloads

3. **Created `backend/src/api/deps.py`**:
   - Implemented `get_current_user()` dependency with JWT token validation
   - Added proper error handling with 401 Unauthorized responses for invalid tokens
   - Used the security utilities to decode and validate JWT tokens
   - Integrated with the database session to fetch user data

4. **Created `backend/src/api/v1/endpoints/auth.py`**:
   - Implemented `POST /signup` endpoint with email uniqueness check and password hashing
   - Implemented `POST /login` endpoint with credential validation and JWT token generation
   - Implemented `GET /me` endpoint with authentication dependency
   - Used proper response models (UserPublic, Token)

5. **Updated `backend/src/main.py`**:
   - Included the auth router with proper prefix and tags
   - Ensured the authentication endpoints are available at `/api/v1/auth/*`

6. **Created `backend/scripts/test_full_auth.py`**:
   - Implemented comprehensive tests for the complete authentication flow
   - Tests user registration, login, and profile access
   - Uses proper mocking to isolate functionality during testing

The authentication and security layer is now fully implemented with all components properly integrated. The system supports user registration, secure login with JWT token generation, and protected endpoints with authentication middleware.

## Outcome

- ✅ Impact: Successfully implemented complete authentication and security layer (T-004, T-005, T-007)
- 🧪 Tests: Created comprehensive test suite for authentication flow
- 📁 Files: Created/updated 6 files across security, models, API endpoints, and dependencies
- 🔁 Next prompts: Ready to proceed with remaining tasks in the implementation plan
- 🧠 Reflection: Authentication layer now properly secured with JWT and password hashing

## Evaluation notes (flywheel)

- Failure modes observed: None - all components properly implemented and integrated
- Graders run and results (PASS/FAIL): N/A (implementation work)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test the authentication endpoints with actual requests