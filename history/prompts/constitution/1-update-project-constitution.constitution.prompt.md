---
id: 1
title: Update Project Constitution
stage: constitution
date: 2026-01-14
surface: agent
model: Qwen
feature: none
branch: main
user: metachemist
command: /sp.constitution
labels: [constitution,spec-driven-development,todo-evolution]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. Load the existing constitution template at `.specify/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read each command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
   - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.


/sp.constitution # Project Constitution: Todo Evolution - Spec-Driven Development with Qwen CLI

## Project Identity
**Name:** Todo Evolution - From CLI to Cloud-Native AI  
**Framework:** Spec-Driven Development (SDD)  
**AI Agent:** Qwen CLI (replacing Claude Code)  
**Methodology:** Agentic Dev Stack (Specify → Plan → Tasks → Implement)  
**Version:** 1.0  
**Last Updated:** January 14, 2026

---

## Core Principles

### 1. Spec-Driven Development (Non-Negotiable)
- **NO MANUAL CODING**: All code must be generated through Qwen CLI based on specifications
- **Spec-First**: Every feature begins with a markdown specification before any implementation
- **Iterative Refinement**: Refine specs until Qwen CLI generates correct output
- **Traceable**: Every line of code must map back to a specification document with Task ID
- **Constitution → Specify → Plan → Tasks → Implement**: This hierarchy is absolute

### 2. Documentation Hierarchy (Source of Truth Order)
1. **Constitution** (this document) - The "WHY" - Principles & constraints
2. **Specifications** (`/specs/features/`) - The "WHAT" - Requirements & acceptance criteria  
3. **Plans** (`/specs/plans/`) - The "HOW" - Architecture & technical approach
4. **Tasks** (`/specs/tasks/`) - The "BREAKDOWN" - Atomic, testable work units
5. **Implementation** (`/src`, `/frontend`, `/backend`) - The "CODE" - Generated only from approved tasks

### 3. Agent Behavior Rules
Qwen CLI (and any AI agent) working on this project MUST:
- ✅ Read constitution before every major action
- ✅ Reference Task IDs in all code comments (e.g., `# [Task]: T-001`)
- ✅ Stop and request clarification when specs are unclear
- ✅ Update specs when requirements change
- ✅ Link every implementation to Specify + Plan sections
- ❌ NEVER freestyle code or invent features not in specs
- ❌ NEVER modify architecture without updating `speckit.plan`
- ❌ NEVER propose features without updating `speckit.specify`
- ❌ NEVER generate code without a referenced Task ID
- ❌ NEVER ignore acceptance criteria

**Golden Rule**: No task = No code. No spec = No task.

---

## Technology Stack (Non-Negotiable)

### Phase I: Console App
- **Runtime**: Python 3.13+
- **Package Manager**: UV
- **AI Agent**: Qwen CLI
- **Spec Management**: Spec-Kit Plus workflow (manual until MCP server ready)
- **Storage**: In-memory (Python data structures)

### Phase II: Full-Stack Web Application
- **Frontend**: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.13+
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT
- **Deployment**: Vercel (frontend), Backend hosting TBD

### Phase III: AI Chatbot
- **Chat UI**: OpenAI ChatKit
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK (Python)
- **Architecture**: Stateless server, database-persisted conversation state

### Phase IV: Kubernetes Deployment
- **Containerization**: Docker, Docker Desktop
- **Orchestration**: Kubernetes (Minikube for local)
- **Package Manager**: Helm Charts
- **AIOps**: kubectl-ai, kagent

### Phase V: Cloud Production
- **Cloud**: Azure (AKS) / Google Cloud (GKE) / Oracle Cloud (OKE)
- **Event Streaming**: Kafka (Strimzi self-hosted or Redpanda Cloud)
- **Distributed Runtime**: Dapr (Pub/Sub, State, Bindings, Secrets, Service Invocation)
- **CI/CD**: GitHub Actions

---

## Architecture Principles

### 1. Clean Code Standards
- **Naming**: Descriptive variable/function names (no single letters except loop indices)
- **Structure**: Separate concerns - models, routes, services, utilities
- **DRY**: Don't Repeat Yourself - extract common patterns
- **Error Handling**: Always handle exceptions gracefully with user-friendly messages
- **Type Safety**: Use type hints in Python, TypeScript in frontend
- **Comments**: Every function/class must have docstrings explaining purpose, params, returns
- **Task Traceability**: Every file must have header comment: `# [Task]: T-XXX | [From]: speckit.specify §X.Y`

### 2. Security First
- **Authentication**: JWT tokens for API security, verify on every request
- **User Isolation**: Users can only access their own data
- **Input Validation**: Validate all user inputs before processing
- **SQL Injection Prevention**: Use ORM (SQLModel) parameterized queries only
- **Secrets Management**: Environment variables, never hardcode credentials
- **HTTPS**: All production deployments must use HTTPS

### 3. Performance Expectations
- **API Response Time**: < 200ms for CRUD operations
- **Database Queries**: Use indexes on user_id, completed, created_at
- **Frontend**: Server-side rendering by default, client components only when needed
- **Caching**: Implement where appropriate (e.g., user session data)
- **Async/Await**: Use async patterns for I/O operations in Python and TypeScript

### 4. Scalability Mindset
- **Stateless Design**: Backend servers hold no state (Phase III+)
- **Horizontal Scaling**: Application must support multiple instances
- **Database Connection Pooling**: Efficient connection management
- **Event-Driven**: Use Kafka for decoupled microservices (Phase V)
- **Cloud-Native**: Design for container orchestration from Phase IV onwards

---

## Project Structure (Monorepo)

```
hackathon-todo/
├── constitution.md                 # This file
├── AGENTS.md                      # AI agent instructions (Qwen CLI + future agents)
├── QWEN.md                        # Qwen CLI-specific configuration (shim to AGENTS.md)
├── README.md                      # Project overview and setup
├── .spec-kit/
│   └── config.yaml               # Spec-Kit configuration
├── specs/
│   ├── overview.md               # Project overview
│   ├── architecture.md           # System architecture diagrams
│   ├── features/                 # Feature specifications (WHAT)
│   │   ├── task-crud.md
│   │   ├── authentication.md
│   │   └── chatbot.md
│   ├── api/                      # API specifications
│   │   ├── rest-endpoints.md
│   │   └── mcp-tools.md
│   ├── database/                 # Database specifications
│   │   └── schema.md
│   ├── ui/                       # UI specifications
│   │   ├── components.md
│   │   └── pages.md
│   ├── plans/                    # Technical plans (HOW)
│   │   ├── phase1-plan.md
│   │   ├── phase2-plan.md
│   │   └── ...
│   └── tasks/                    # Task breakdowns (BREAKDOWN)
│       ├── phase1-tasks.md
│       ├── phase2-tasks.md
│       └── ...
├── phase1-console/               # Phase I: Console app
│   ├── src/
│   ├── tests/
│   └── README.md
├── frontend/                      # Phase II+: Next.js app
│   ├── QWEN.md                   # Frontend-specific instructions
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── README.md
├── backend/                       # Phase II+: FastAPI app
│   ├── QWEN.md                   # Backend-specific instructions
│   ├── main.py
│   ├── models.py
│   ├── routes/
│   ├── services/
│   └── README.md
├── k8s/                          # Phase IV+: Kubernetes manifests
│   ├── helm-charts/
│   └── deployments/
├── docker-compose.yml            # Local development
└── .github/
    └── workflows/                # CI/CD pipelines
```

---

## Development Workflow (Agentic Dev Stack)

### Step 1: Specify (WHAT to Build)
- Create/update `/specs/features/[feature-name].md`
- Define user stories, acceptance criteria, business rules
- Get human approval before proceeding

### Step 2: Plan (HOW to Build)
- Create/update `/specs/plans/[phase-name]-plan.md`
- Define architecture, components, APIs, database schema
- Specify technology choices and integration points
- Reference corresponding Specify sections

### Step 3: Tasks (BREAKDOWN)
- Create/update `/specs/tasks/[phase-name]-tasks.md`
- Break plan into atomic, testable units
- Each task must include:
  - Task ID (e.g., T-001)
  - Clear description
  - Preconditions
  - Expected outputs
  - Files to modify
  - Links to Specify + Plan sections

### Step 4: Implement (CODE)
- Qwen CLI generates code based on approved tasks
- Every code file includes header: `# [Task]: T-XXX | [From]: speckit.specify §X.Y, speckit.plan §Z.W`
- Run tests after implementation
- Refine spec if implementation reveals issues

### Step 5: Validate & Iterate
- Test generated code
- If issues found, update spec (not code manually)
- Re-run Qwen CLI with refined spec
- Repeat until acceptance criteria met

---

## Quality Standards

### Code Quality
- **Test Coverage**: Minimum 80% for business logic
- **Linting**: All code must pass linter (Ruff for Python, ESLint for TypeScript)
- **Formatting**: Consistent formatting (Black for Python, Prettier for TypeScript)
- **No Dead Code**: Remove unused imports, functions, variables
- **Documentation**: README in every major folder

### Deliverables per Phase
1. **Specifications**: Complete and approved specs in `/specs`
2. **Source Code**: Generated by Qwen CLI, properly structured
3. **Tests**: Unit tests for core functionality
4. **Documentation**: README with setup instructions, architecture diagrams
5. **Demo Video**: 90 seconds max, shows features + spec-driven workflow
6. **GitHub Repo**: Public, with clear commit history showing spec → code flow

---

## Phase-Specific Requirements

### Phase I: Console App 
**Features**: Add, Delete, Update, View, Mark Complete  
**Storage**: In-memory Python data structures  
**Deliverable**: Single Python application with clean CLI interface

### Phase II: Web Application 
**Features**: All Phase I features as web UI  
**New**: User authentication, persistent storage, REST API  
**Deliverable**: Deployed frontend (Vercel) + backend

### Phase III: AI Chatbot 
**Features**: Natural language task management  
**New**: OpenAI Agents SDK, MCP server, stateless architecture  
**Deliverable**: ChatKit UI managing todos via conversation

### Phase IV: Kubernetes 
**Features**: All Phase III features  
**New**: Docker containers, Helm charts, Minikube deployment  
**Deliverable**: Local K8s deployment with AIOps tools

### Phase V: Cloud Production 
**Features**: All previous + Advanced features  
**New**: Recurring tasks, due dates, priorities, tags, search, filter, sort  
**New**: Kafka event streaming, Dapr runtime, cloud K8s deployment  
**Deliverable**: Production deployment on Azure/GCP/Oracle

---

## Constraints & Guardrails

### What We DON'T Do
- ❌ Write code manually (except for fixing critical bugs after spec exhaustion)
- ❌ Skip phases or merge requirements
- ❌ Use technologies outside approved stack without justification
- ❌ Commit code without corresponding spec + task
- ❌ Deploy without testing
- ❌ Store secrets in code or version control

### What We ALWAYS Do
- ✅ Start with spec, end with validated implementation
- ✅ Reference Task IDs in commits: `git commit -m "[T-001] Implement add task feature"`
- ✅ Update specs when requirements change
- ✅ Test before committing
- ✅ Document setup steps
- ✅ Keep constitution as single source of truth for principles

---

## Success Criteria

### Technical Excellence
- All phases completed according to specs
- Test coverage > 80%
- No manual code (all generated via Qwen CLI)
- Clean git history showing spec-driven workflow

### Spec-Driven Mastery
- Every feature has corresponding spec
- Every code file references Task ID
- Constitution → Specify → Plan → Tasks → Implement hierarchy maintained
- Iterative refinement demonstrated

### Bonus Achievements (Optional)
- **Reusable Intelligence**: Create Qwen CLI subagents/skills (+200 points)
- **Cloud-Native Blueprints**: Agent skills for infrastructure (+200 points)
- **Urdu Support**: Multi-language chatbot (+100 points)
- **Voice Commands**: Voice input for todos (+200 points)

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Jan 14, 2026 | Initial constitution for Qwen CLI-based hackathon |

---

## Response snapshot

I have successfully updated the project constitution file at `.specify/memory/constitution.md` with the comprehensive content you provided. The new constitution includes:

1. Core principles for Spec-Driven Development
2. Technology stack definitions for all five phases
3. Architecture principles for clean code, security, performance, and scalability
4. Detailed project structure
5. Development workflow (Specify → Plan → Tasks → Implement)
6. Quality standards and phase-specific requirements
7. Constraints and guardrails
8. Success criteria

The constitution now serves as the authoritative guide for the Todo Evolution project, establishing the non-negotiable rules and guidelines that all development activities must follow. The file includes an HTML comment at the top with a sync impact report detailing the changes made.

## Outcome

- ✅ Impact: Created comprehensive project constitution establishing development principles and guidelines
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: Proceed with creating feature specifications based on this constitution
- 🧠 Reflection: The constitution establishes a strong foundation for the Spec-Driven Development approach, ensuring all future work follows the prescribed methodology.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): Standard constitution update
- Next experiment (smallest change to try): Begin creating feature specifications based on the established principles