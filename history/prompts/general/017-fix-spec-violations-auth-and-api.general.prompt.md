---
id: 17
title: fix-spec-violations-auth-and-api
stage: green
date: 2026-01-16
surface: agent
model: "openai/gpt-4o"
feature: phase-2-web-app
branch: 2-phase-2-web-app
user: metachemist
command: "/sp.implement"
labels: ["specification", "refinement", "quality-audit", "task-T-007"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/specs/1-specify/features/feature-03-authentication.md
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/specs/1-specify/features/feature-02-web-api.md
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/specs/3-tasks/phase-1-tasks.md
tests:
 - /home/metachemist/projects/myprograms/gen_ai/evolution-of-todo-list-01/tests/unit/test_main.py
---

## Prompt

@constitution.md # ROLE Act as a Senior Product Owner refining specifications to pass a Quality Audit. # CONTEXT Our specifications were **REJECTED** due to "Implementation Leakage" (describing code instead of requirements) and "Missing Edge Cases". We are refining two files: 1. `specs/1-specify/features/feature-02-web-api.md` 2. `specs/1-specify/features/feature-03-authentication.md` # TASK Rewrite both files to fix the specific violations found in the Audit Report. # REFINEMENT INSTRUCTIONS ## 1. Fix `feature-03-authentication.md` (Purge Leakage) - **Violation**: "Use bcrypt with minimum cost factor 12" - **Fix**: Change to "Passwords must be hashed using industry-standard secure algorithms (e.g., bcrypt, argon2) with safe work factors." - **Violation**: "Use Better Auth hooks" - **Fix**: Change to "Frontend must manage session state and persistence." (Do not name specific React functions). - **Violation**: "HS256 algorithm" - **Fix**: Change to "Secure signing algorithm". ## 2. Fix `feature-02-web-api.md` (Add Edge Cases) The Audit found missing reliability scenarios. Add a new section **"4. Reliability & Error Handling"** covering: - **Network Timeouts**: Requirements for client handling of requests > 30s. - **Rate Limiting**: Define limits (e.g., "API must reject requests > 100/min per user with 429 Too Many Requests"). - **Database Downtime**: "System must return 503 Service Unavailable if storage is unreachable." - **Concurrent Updates**: "System must handle race conditions (e.g., Last-Write-Wins strategy)." # OUTPUT Regenerate the full valid Markdown for both files. - Ensure NO raw SQL or specific library function calls remain. - Ensure all "Success Criteria" are SMART (Specific, Measurable, Achievable, Relevant, Time-bound).

## Response snapshot

I have successfully updated both specification files to address the violations identified in the quality audit:

1. Fixed `feature-03-authentication.md` by:
   - Changed "Use bcrypt with minimum cost factor 12" to "Use industry-standard secure algorithms (e.g., bcrypt, argon2) with safe work factors"
   - Changed "Use Better Auth hooks" to "Frontend must manage session state and persistence"
   - Changed "HS256 algorithm" to "Secure signing algorithm"
   - Updated related sections to remove specific implementation details

2. Fixed `feature-02-web-api.md` by:
   - Added new section "4.4 Reliability & Error Handling" with subsections for:
     - Network Timeouts (handling requests > 30s)
     - Rate Limiting (limits and responses)
     - Database Downtime (503 responses)
     - Concurrent Updates (race condition handling)

The specifications now properly focus on functional and non-functional requirements without implementation leakage, and include the missing edge cases for reliability and error handling.

## Outcome

- ✅ Impact: Successfully fixed specification violations identified in quality audit
- 🧪 Tests: N/A (specification work, not implementation)
- 📁 Files: Updated feature-03-authentication.md and feature-02-web-api.md with corrected specifications
- 🔁 Next prompts: Ready to proceed with implementation tasks
- 🧠 Reflection: Specifications now properly balance requirements with abstraction of implementation details.

## Evaluation notes (flywheel)

- Failure modes observed: None - all violations have been addressed
- Graders run and results (PASS/FAIL): N/A (specification work)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with implementation of the corrected specifications