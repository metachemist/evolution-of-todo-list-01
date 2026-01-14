---
id: 2
title: Update Constitution With New Sections
stage: constitution
date: 2026-01-14
surface: agent
model: Qwen
feature: none
branch: main
user: metachemist
command: /sp.constitution
labels: [constitution,spec-driven-development,todo-evolution,error-handling,quality-metrics,risk-management]
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


/sp.constitution add these into constitution file ```---

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

---

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

---

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

---

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

---

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

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Jan 14, 2026 | Initial constitution for Qwen CLI-based hackathon |
| 1.1 | Jan 14, 2026 | Added error handling, metrics, oversight, risk management, and version control sections per Qwen CLI feedback |

---

```

## Response snapshot

I have successfully updated the constitution file with the new sections you provided. The updated constitution now includes:

1. Error Handling and Recovery Procedures
2. Quality Metrics and Measurement
3. Human Oversight and Approval
4. Risk Management and Contingency Plans
5. Version Control and Change Management

The version has been updated from 1.0.0 to 1.1.0 to reflect these additions. The sync impact report at the top of the file has been updated to reflect the changes made. The constitution now has a more comprehensive governance structure that addresses operational realities while maintaining the spec-driven development principles.

## Outcome

- ✅ Impact: Enhanced constitution with detailed procedures for error handling, quality metrics, oversight, risk management, and version control
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: Proceed with creating feature specifications based on the enhanced constitution
- 🧠 Reflection: The updated constitution provides more practical guidance for handling real-world challenges while maintaining the spec-driven approach.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): Constitution update with additional sections
- Next experiment (smallest change to try): Begin creating feature specifications based on the enhanced principles