# Todo Evolution - From CLI to Cloud-Native AI

This project demonstrates the evolution of a simple todo application from a command-line interface to a cloud-native AI-powered system. The progression occurs in phases, with each building upon the previous one to create a robust, scalable, and intelligent todo management platform.

## Phase I: Console Application

The first phase implements a console-based task management application with the following features:
- Add, Delete, Update, View, and Mark Complete operations
- In-memory session storage
- Console-based user interactions

## Phase II: Full-Stack Web Application

The second phase transforms the console application into a full-stack web application with user authentication, persistent storage, and RESTful API.

### Features
- User authentication (signup, signin, profile management)
- Persistent task management with PostgreSQL
- RESTful API with JWT authentication
- Rate limiting for API protection
- Health check endpoints
- Frontend with Next.js and Tailwind CSS

### Backend Setup

1. Clone the repository
2. Navigate to the backend directory: `cd backend`
3. Install dependencies with `uv sync`
4. Set up environment variables:
   - Copy `.env.example` to `.env` and update values
   - Set `DATABASE_URL` to your PostgreSQL connection string
   - Set `SECRET_KEY` for JWT signing
5. Run database migrations (if applicable)
6. Start the backend server: `uv run python -m src.main`

### Frontend Setup

1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install` or `yarn install`
3. Set up environment variables if needed
4. Start the development server: `npm run dev` or `yarn dev`
5. Visit `http://localhost:3000` in your browser

### API Endpoints

#### Authentication
- `POST /api/v1/auth/signup` - Register a new user
- `POST /api/v1/auth/login` - Authenticate user and get JWT token
- `GET /api/v1/auth/me` - Get current user profile
- `POST /api/v1/auth/signout` - Sign out user
- `PUT /api/v1/auth/profile` - Update user profile

#### Tasks
- `GET /api/v1/tasks/` - Get user's tasks
- `POST /api/v1/tasks/` - Create a new task
- `GET /api/v1/tasks/{id}` - Get specific task
- `PUT /api/v1/tasks/{id}` - Update task
- `PATCH /api/v1/tasks/{id}` - Partially update task
- `PATCH /api/v1/tasks/{id}/complete` - Toggle completion status
- `DELETE /api/v1/tasks/{id}` - Delete task

#### Health Check
- `GET /health` - Application health status
- `GET /api/health` - Alternative health check endpoint

### Rate Limits
- Authentication endpoints: 5 requests per minute per IP
- Task endpoints: 100 requests per minute per IP

## Setup

1. Clone the repository
2. Follow the Phase I or Phase II setup instructions depending on which phase you want to run

## Technologies Used

### Phase I
- Python 3.13+
- Pydantic for data validation
- Argparse for CLI parsing
- Pytest for testing

### Phase II
- **Backend**: FastAPI, Python 3.13+
- **Database**: PostgreSQL with SQLModel
- **Authentication**: JWT tokens
- **Rate Limiting**: SlowAPI
- **Frontend**: Next.js 16+, React, TypeScript, Tailwind CSS
- **Package Manager**: UV (backend), npm/yarn (frontend)