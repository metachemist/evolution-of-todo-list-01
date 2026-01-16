# evolution-of-todo-list-01

This project follows a spec-driven development approach with a well-defined monorepo structure:

```
evolution-of-todo-list-01/
├── constitution.md                 # The Supreme Law (Principles & Constraints)
├── AGENTS.md                      # AI Agent Instructions (The "How-To")
├── QWEN.md                        # CLI entry point (Shim to AGENTS.md)
├── README.md                      # Project onboarding
│
├── .specify/                      # SpecifyPlus Tool Configuration
│   ├── config.yaml               # Tool settings
│   └── templates/                # Templates for Spec/Plan/Task generation
│       ├── spec-template.md
│       ├── plan-template.md
│       └── tasks-template.md
│
├── specs/                         # The Source of Truth (Lifecycle Stages)
│   │
│   ├── 1-specify/                # STEP 1: WHAT (Requirements & Context)
│   │   ├── system-overview.md    # High-level goals
│   │   ├── features/             # Feature Requirements
│   │   │   ├── feature-01-task-crud.md
│   │   │   ├── feature-02-auth.md
│   │   │   └── ...
│   │   ├── domain/               # Domain Rules & Entities
│   │   └── user-journeys/        # User Stories
│   │
│   ├── 2-plan/                   # STEP 2: HOW (Architecture & Design)
│   │   ├── phase-1-console.md
│   │   ├── phase-2-fullstack.md
│   │   ├── api-specs/            # API Contracts (OpenAPI/MCP)
│   │   ├── db-schema/            # Data Models (SQLModel)
│   │   └── ui-design/            # Component Architecture
│   │
│   └── 3-tasks/                  # STEP 3: EXECUTE (Atomic Units)
│       ├── phase-1/
│       │   ├── T-001-setup.md
│       │   ├── T-002-core-logic.md
│       │   └── ...
│       └── phase-2/
│           └── ...
│
├── src/                           # STEP 4: IMPLEMENTATION (Phase I)
│   ├── core/
│   ├── cli/
│   └── tests/
│
├── frontend/                      # STEP 4: IMPLEMENTATION (Phase II+)
│   ├── src/
│   └── ...
│
├── backend/                       # STEP 4: IMPLEMENTATION (Phase II+)
│   ├── src/
│   └── ...
│
├── infra/                         # STEP 4: INFRASTRUCTURE (Phase IV+)
    ├── k8s/
    ├── docker/
    └── helm/
```

## Getting Started

This project uses a spec-driven development approach where all code is generated from specifications. To get started:

1. Review the `constitution.md` to understand the project principles
2. Examine the `specs/` directory to understand feature requirements
3. Follow the development workflow as outlined in the constitution