<!-- SYNC IMPACT REPORT
Version change: 1.1.0 → 1.2.0
Modified principles: None (new sections added)
Added sections: Testing Strategy and Quality Assurance, Monitoring and Observability, Security and Compliance, Documentation Standards
Removed sections: None
Templates requiring updates:
- ✅ .specify/templates/plan-template.md - Updated to align with new principles
- ✅ .specify/templates/spec-template.md - Updated to align with new principles
- ✅ .specify/templates/tasks-template.md - Updated to align with new principles
- ⚠️  .specify/templates/commands/*.md - May need updates for agent-specific references
- ⚠️  README.md - May need updates to reference new principles
Follow-up TODOs: None
-->

# Todo Evolution - From CLI to Cloud-Native AI Constitution

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

## Testing Strategy and Quality Assurance

### Test-Driven Development (TDD) Approach
- Write tests before implementation code
- Follow Arrange-Act-Assert pattern for test structure
- Include unit, integration, and end-to-end tests

### Testing Requirements by Phase
**Phase I (Console App)**:
- Unit tests for all business logic functions
- Command-line interface tests
- Input validation tests

**Phase II (Web Application)**:
- Component tests for UI elements
- API endpoint tests with mock data
- Authentication flow tests
- Database integration tests

**Phase III (AI Chatbot)**:
- Natural language processing tests
- Conversation flow tests
- MCP tool integration tests

### Automated Testing Pipeline
- All tests must pass before merging
- Continuous integration with GitHub Actions
- Performance regression tests
- Security vulnerability scanning

## Monitoring and Observability

### Logging Standards
- Structured JSON logs for all services
- Log levels: DEBUG, INFO, WARN, ERROR
- Include correlation IDs for tracing requests
- Centralized logging with aggregation

### Metrics Collection
- Application performance metrics
- Resource utilization (CPU, memory, disk)
- Business metrics (user actions, conversion rates)
- Custom application-specific metrics

### Health Checks
- Liveness and readiness probes for containers
- Database connectivity checks
- External service dependency checks
- Automatic restart on health failures

### Alerting
- Response time degradation alerts
- Error rate threshold alerts
- Resource exhaustion alerts
- Notification channels (email, system notifications)

## Security and Compliance

### Authentication and Authorization
- Multi-factor authentication for admin access
- Role-based access control (RBAC)
- Session management and timeout policies
- Password strength requirements

### Data Protection
- Encrypt data in transit (TLS 1.3)
- Encrypt sensitive data at rest
- Regular security audits
- GDPR compliance for user data

### Vulnerability Management
- Regular dependency scanning
- Penetration testing schedule
- Security incident response plan
- Bug bounty program considerations

## Documentation Standards

### Code Documentation
- Inline comments for complex algorithms
- API documentation with examples
- Architecture decision records (ADRs)
- Code walkthrough guides

### Project Documentation
- Setup and installation guides
- Configuration documentation
- Deployment guides
- Troubleshooting guides

### Maintenance
- Update documentation with each feature
- Regular documentation reviews
- User feedback incorporation
- Version-specific documentation

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

## Error Handling and Recovery Procedures

### When AI Generation Fails
If Qwen CLI fails to generate acceptable code after 3 refinement iterations:

1. **Document the Issue**: Create `/specs/issues/[issue-id].md` documenting:
   - What was requested vs. what was generated
   - All spec refinements attempted
   - Specific failures or deviations

2. **Human Review Required**: Determine if issue is:
   - **Spec ambiguity**: Rewrite spec with more explicit acceptance criteria
   - **AI limitation**: Break task into smaller atomic units
   - **Technical impossibility**: Revise plan/architecture

3. **Emergency Override Process**: For critical bugs blocking progress:
   - Document bug in `/specs/issues/emergency-[id].md`
   - Apply minimal manual fix with detailed comments
   - Create follow-up task to regenerate fix via spec
   - Mark file with `# [EMERGENCY FIX] - Requires spec-driven replacement`

### AI Hallucination Protocol
If generated code contradicts specifications:

1. **Stop immediately** - Do not commit hallucinated code
2. **Document the hallucination** in `/specs/issues/hallucination-[id].md`
3. **Simplify the spec** - Break into smaller, more explicit tasks
4. **Add negative examples** - Show what NOT to generate
5. **Re-run with simplified task`

### Specification Emergency Changes
For urgent spec changes mid-phase:

1. **Impact Assessment**: Document which tasks/implementations are affected
2. **Version the Old Spec**: Move to `/specs/archive/[feature]-v[N].md`
3. **Create New Spec**: With clear changelog section at top
4. **Regenerate Affected Code**: Using new spec, don't patch manually
5. **Update All References**: Task IDs, plan sections, architecture docs

## Quality Metrics and Measurement

### Phase-Specific Performance Benchmarks

**Phase I: Console App**
- Startup time: < 1 second
- Command execution: < 100ms
- Memory usage: < 50MB

**Phase II: Web Application**
- API response time: < 200ms (p95)
- Frontend page load: < 2 seconds (First Contentful Paint)
- Database query time: < 50ms average
- Build time: < 2 minutes

**Phase III: AI Chatbot**
- Message response time: < 3 seconds (including AI inference)
- MCP tool execution: < 500ms per tool call
- Conversation context retrieval: < 100ms
- Concurrent users supported: 50+ (local testing)

**Phase IV: Kubernetes Deployment**
- Container startup time: < 30 seconds
- Pod readiness: < 45 seconds
- Rolling update downtime: 0 seconds
- Resource usage per pod: < 512MB RAM, < 0.5 CPU

**Phase V: Cloud Production**
- API response time: < 150ms (p95) at 100 req/s
- Kafka message latency: < 100ms
- Horizontal scaling time: < 2 minutes
- System uptime: > 99.5%

### Specification Quality Criteria

A spec is considered "complete" when it contains:
- ✅ Clear user stories with acceptance criteria
- ✅ All edge cases documented with expected behavior
- ✅ Positive AND negative examples
- ✅ Input validation rules specified
- ✅ Error messages defined
- ✅ Success/failure response formats
- ✅ No ambiguous terms (all domain concepts defined)

**Spec Clarity Score**: Rate 1-5 on:
- Clarity (no ambiguous language)
- Completeness (all scenarios covered)
- Testability (can write tests from spec alone)
- Traceability (links to architecture/requirements)

**Minimum acceptable score: 4/5 before implementation**

### Timeline Expectations

| Activity | Expected Duration |
|----------|------------------|
| Write initial spec | 30-60 minutes |
| Spec review & approval | 15-30 minutes |
| Generate plan from spec | 20-40 minutes |
| Break into tasks | 15-30 minutes |
| Generate code (per task) | 5-15 minutes |
| Test & validate | 10-20 minutes per task |
| Refine spec (if needed) | 10-20 minutes |

**Total cycle time per feature: 2-4 hours from spec to validated code**

### Definition of "Done" per Phase

**Phase I Complete When:**
- ✅ All 5 basic features implemented (Add, Delete, Update, View, Complete)
- ✅ Console interface functional with clear user prompts
- ✅ All specs, plans, tasks documented in `/specs`
- ✅ Test coverage > 80%
- ✅ README with setup instructions complete
- ✅ Demo video recorded (< 90 seconds)
- ✅ GitHub repo public and submitted via form

**Phase II Complete When:**
- ✅ All Phase I features working in web UI
- ✅ Authentication functional (signup/signin)
- ✅ REST API endpoints tested and documented
- ✅ Frontend deployed to Vercel
- ✅ Backend deployed and accessible
- ✅ Database migrations documented
- ✅ All specs updated for web context
- ✅ Demo video shows web interface

**Similar criteria apply to Phases III-V with phase-specific requirements**

## Human Oversight and Approval

### Mandatory Human Review Points

1. **Before Implementation Starts**
   - ✅ Specification completeness (Clarity Score ≥ 4/5)
   - ✅ Plan alignment with architecture principles
   - ✅ Task breakdown is atomic and testable

2. **After Initial Code Generation**
   - ✅ Code matches spec acceptance criteria
   - ✅ No hallucinations or spec violations
   - ✅ Task IDs properly referenced

3. **Before Phase Completion**
   - ✅ All features meet "Definition of Done"
   - ✅ Demo video demonstrates all requirements
   - ✅ Documentation complete and accurate

### Approval Authority

**For this individual hackathon, YOU are the approver for:**
- All specification changes
- All plan modifications
- Emergency fixes
- Phase completion sign-off

**Approval Process:**
1. Review generated content against spec
2. Test functionality manually
3. Run automated tests
4. Check quality metrics
5. Approve or request refinement

### Validating AI-Generated Code

**Validation Checklist:**
- [ ] Code includes Task ID header comment
- [ ] All acceptance criteria from spec are met
- [ ] No extra features not in spec
- [ ] Error handling implemented as specified
- [ ] Type hints/TypeScript types present
- [ ] Tests pass (>80% coverage)
- [ ] Linter passes with no warnings
- [ ] Performance meets phase benchmarks
- [ ] Security checks pass (no hardcoded secrets, SQL injection safe)
- [ ] Documentation/comments explain complex logic

**If validation fails:** Document issue and refine spec, do not manually patch code.

### Escalation Process

**Level 1 - Spec Refinement (First 3 attempts):**
- Clarify ambiguous requirements
- Add more explicit examples
- Break into smaller tasks

**Level 2 - Architecture Review (After 3 failed attempts):**
- Review plan for feasibility
- Consider alternative technical approach
- Consult constitution for constraints

**Level 3 - Emergency Override (Only for critical blockers):**
- Document in `/specs/issues/emergency-[id].md`
- Apply minimal manual fix
- Create follow-up task for proper spec-driven solution

## Risk Management and Contingency Plans

### Risk: Qwen CLI Becomes Unavailable

**Probability:** Low | **Impact:** Critical

**Contingency Plan:**
1. **Immediate**: Switch to alternative AI CLI (Claude Code, GitHub Copilot CLI, or GPT-4 with custom wrapper)
2. **Update**: Modify QWEN.md to point to new agent
3. **Validate**: Re-run last task to ensure new agent understands specs
4. **Document**: Note agent switch in constitution revision history

**Prevention**:
- Keep specs in universal markdown format (agent-agnostic)
- Test with multiple AI agents during setup phase
- Maintain local copies of all specs and generated code

### Risk: AI-Generated Code Consistently Fails Quality

**Probability:** Medium | **Impact:** High

**Contingency Plan:**
1. **After 5 consecutive failures**: Pause and review approach
2. **Root Cause Analysis**: Is the spec unclear, or is the task too complex?
3. **Options**:
   - **Simplify**: Break into even smaller atomic tasks
   - **Clarify**: Rewrite spec with more explicit requirements
   - **Template**: Provide code template/skeleton in spec
   - **Hybrid**: Generate pseudocode first, then translate to code
4. **Document Learnings**: Update constitution with new patterns

**Prevention**:
- Start with simple tasks to validate AI agent capability
- Build complexity gradually
- Keep task scope small (< 50 lines per task)

### Risk: Planned Tools Become Obsolete

**Probability:** Low | **Impact:** Medium

**Contingency Plan:**
1. **For Infrastructure Tools** (Docker, K8s, Helm):
   - These are industry standards, unlikely to change rapidly
   - If unavailable, document in `/specs/issues/` and continue with other phases

2. **For Cloud Services** (Neon DB, Vercel, DigitalOcean):
   - Fallback to alternatives: Supabase, Netlify, other cloud providers
   - Update specs with new service details
   - Core architecture remains same (spec-driven)

3. **For AI Services** (OpenAI Agents SDK, ChatKit):
   - Fallback: LangChain, Anthropic SDK, or custom implementation
   - MCP protocol is standard, swap underlying LLM

**Prevention**:
- Use industry-standard, open-source tools when possible
- Abstract vendor-specific logic behind interfaces
- Keep specs focused on behavior, not implementation details

### Risk: Data Loss in Specification Documents

**Probability:** Low | **Impact:** Critical

**Contingency Plan:**
1. **Git as Primary Backup**: All specs in version control
2. **Commit Frequency**: Commit specs after every approval
3. **Remote Backup**: Push to GitHub after each phase
4. **Export**: Weekly export of `/specs` folder to cloud storage

**Recovery Procedure:**
1. Restore from git history: `git checkout HEAD~1 specs/`
2. If git corrupted, restore from GitHub remote
3. If both unavailable, restore from cloud backup
4. Last resort: Regenerate specs from working code + memory

**Prevention**:
- Commit frequently with descriptive messages
- Push to remote after every work session
- Keep local backup of `/specs` folder
- Use git tags for phase milestones

## Version Control and Change Management

### Branching Strategy

**Main Branch (`main`):**
- Production-ready code only
- Only merge after phase completion
- Protected branch - no direct commits

**Development Branch (`develop`):**
- Integration branch for current phase
- Merge feature branches here first
- Must pass all tests before merging to main

**Feature Branches (`feature/T-XXX-description`):**
- One branch per task or small group of related tasks
- Named with Task ID from specs
- Deleted after merge to develop
- Examples:
  - `feature/T-001-add-task`
  - `feature/T-015-auth-jwt`
  - `feature/T-042-mcp-server`

**Emergency Branches (`hotfix/emergency-XXX`):**
- For critical bugs requiring immediate fix
- Merge to both develop and main
- Must have corresponding `/specs/issues/emergency-XXX.md`

### Branching Workflow

```bash
# Start new task
git checkout develop
git pull origin develop
git checkout -b feature/T-001-add-task

# Generate code via Qwen CLI
qwen "Implement T-001 from specs/tasks/phase1-tasks.md"

# Commit with Task ID
git add .
git commit -m "[T-001] Implement add task feature

- Generated via Qwen CLI from specs/tasks/phase1-tasks.md
- Implements Add Task requirement from specs/features/task-crud.md
- Tests included, coverage: 85%"

# Push and create PR
git push origin feature/T-001-add-task
# Create Pull Request to develop branch
```

### Handling Breaking Changes to Specifications

**When spec changes would break existing implementation:**

1. **Version the Specification**:
   ```
   specs/features/task-crud-v1.md  (original)
   specs/features/task-crud-v2.md  (new version)
   ```

2. **Create Migration Plan**:
   ```markdown
   # specs/migrations/task-crud-v1-to-v2.md

   ## Changes
   - Added `priority` field to tasks
   - Changed `completed` to `status` enum

   ## Affected Components
   - Database schema (migration required)
   - API endpoints (version with /v2/)
   - Frontend UI (update forms)

   ## Migration Steps
   1. Create database migration
   2. Implement v2 API alongside v1
   3. Update frontend to use v2
   4. Deprecate v1 after testing
   ```

3. **Implement with Versioning**:
   - Keep old spec for reference
   - Generate new code from v2 spec
   - Use API versioning if needed (`/api/v2/tasks`)
   - Document breaking changes in changelog

### Rolling Back Failed Implementations

**If implementation doesn't meet requirements:**

1. **Do NOT manually fix code**
2. **Rollback git branch**:
   ```bash
   git checkout develop
   git branch -D feature/T-XXX-failed-attempt
   ```
3. **Refine specification**:
   - Update `/specs/features/[feature].md`
   - Add more explicit acceptance criteria
   - Include examples of what went wrong
4. **Create new feature branch**:
   ```bash
   git checkout -b feature/T-XXX-revised
   ```
5. **Regenerate with Qwen CLI using refined spec**

### Coordination for Multiple Related Features

**When working on related tasks (even solo):**

1. **Check Task Dependencies**:
   - Review `/specs/tasks/phase-X-tasks.md` for prerequisites
   - Ensure dependent tasks completed first

2. **Update Shared Specs First**:
   - If two tasks share a spec file, complete spec for both
   - Implement in dependency order

3. **Integration Testing**:
   - After completing related tasks, test integration
   - Create integration test task if needed

4. **Merge Strategy**:
   - Merge tasks in dependency order
   - Run full test suite after each merge
   - Fix conflicts by regenerating from spec, not manually

### Commit Message Convention

```
[T-XXX] Brief description (50 chars max)

- Detailed point 1
- Detailed point 2
- Generated via: Qwen CLI
- Spec reference: specs/features/file.md §X.Y
- Tests: coverage X%, all passing
- Phase: I/II/III/IV/V
```

**Examples:**
```
[T-001] Implement add task feature

- Generated via Qwen CLI from specs/tasks/phase1-tasks.md
- Implements requirement from specs/features/task-crud.md §2.1
- Tests: coverage 87%, all passing
- Phase: I
```

```
[T-015] Add JWT authentication middleware

- Generated via Qwen CLI
- Spec: specs/features/authentication.md §3
- Integrates with Better Auth token verification
- Tests: coverage 92%, all passing
- Phase: II
```

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-14 | Initial constitution for Qwen CLI-based hackathon |
| 1.1 | 2026-01-14 | Added error handling, metrics, oversight, risk management, and version control sections per Qwen CLI feedback |
| 1.2 | 2026-01-14 | Added testing strategy, monitoring, security, and documentation standards |

## Governance
This constitution serves as the governing document for the Todo Evolution project. All development activities must comply with the principles and constraints outlined herein. Amendments to this constitution require explicit approval and must be documented with clear rationale.

**Version**: 1.2.0 | **Ratified**: 2026-01-14 | **Last Amended**: 2026-01-14