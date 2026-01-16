---
id: "001"
title: "Update Monorepo Structure"
stage: "constitution"
date_iso: "2026-01-14"
surface: "agent"
model: "Qwen"
feature: "none"
branch: "main"
user: "metachemist"
command: "/sp.constitution"
labels: ["constitution", "monorepo", "structure", "refactor"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
  - ".specify/templates/plan-template.md"
  - ".specify/templates/spec-template.md"
  - ".specify/templates/tasks-template.md"
  - "README.md"
tests_yaml: []
prompt_text: |
  I want to change the monorepo structure to evolution-of-todo-list-01/

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

  ├── core/

  ├── cli/

  └── tests/

  │

  ├── frontend/                      # STEP 4: IMPLEMENTATION (Phase II+)

  │   ├── src/

  └── ...

  │

  ├── backend/                       # STEP 4: IMPLEMENTATION (Phase II+)

  │   ├── src/

  └── ...

  │

  └── infra/                         # STEP 4: INFRASTRUCTURE (Phase IV+)

      ├── k8s/

      ├── docker/

      └── helm/
response_text: |
  I've successfully updated the project constitution and related templates to match your requested monorepo structure. Here's a summary of the changes made:

  ## Summary of Changes

  1. **Updated Constitution**:
     - Modified the project structure section to match your requested format
     - Changed from "hackathon-todo/" to "evolution-of-todo-list-01/" as the root
     - Updated the directory tree to match your specified layout
     - Incremented version from 1.4.0 to 1.5.0
     - Updated the revision history and sync impact report

  2. **Updated Templates**:
     - Modified `plan-template.md` to reflect the new project structure
     - Updated `tasks-template.md` with the new path conventions
     - Enhanced `spec-template.md` to include the project structure alignment section
     - Updated `README.md` to document the new structure

  3. **Version Update**:
     - The constitution version has been incremented from 1.4.0 to 1.5.0 to reflect the significant structural changes

  ## Suggested Commit Message

  ```
  docs: update constitution to reflect new monorepo structure

  - Updated project structure to match evolution-of-todo-list-01 layout
  - Modified templates to align with new directory conventions
  - Incremented version to 1.5.0 for structural changes
  ```

  All changes have been implemented according to your requirements, maintaining the spec-driven development approach outlined in the constitution.
outcome: "Successfully updated the constitution and related templates to reflect the new monorepo structure as requested."
evaluation: "The constitution was successfully updated with the new monorepo structure, version was incremented appropriately, and all related templates were updated to maintain consistency."
---

# Update Monorepo Structure

This prompt requested updating the project constitution to reflect a new monorepo structure for the "evolution-of-todo-list-01" project. The changes included updating the directory structure in the constitution and related templates to match the specified format.