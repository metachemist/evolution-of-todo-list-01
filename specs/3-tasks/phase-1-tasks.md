# Task Breakdown: Phase I Console App

**Feature**: Task CRUD Operations | **Phase**: 3-tasks | **Branch**: `3-phase-1-tasks`
**Input**: specs/2-plan/phase-1-console.md and specs/1-specify/features/feature-01-task-crud.md

## Summary

This task breakdown implements the Phase I Console App with Task CRUD functionality following the layered architecture plan. Tasks are organized by user story priority to enable incremental development and testing.

## Dependencies Overview

- **User Story 1 (Add Tasks)**: Foundation for all other stories
- **User Story 2 (View Tasks)**: Depends on US1 (needs tasks to view)
- **User Story 3 (Update Tasks)**: Depends on US1 (needs tasks to update)
- **User Story 4 (Complete/Delete Tasks)**: Depends on US1 (needs tasks to complete/delete)

## Implementation Strategy

- **MVP Scope**: User Story 1 (Add Tasks) with minimal supporting infrastructure
- **Incremental Delivery**: Complete each user story with all its components before moving to the next
- **Parallel Opportunities**: Repository, Service, and CLI components can be developed in parallel once the Domain layer is complete

## Phase 1: Project Setup

### Task [T-001]: Initialize Project Structure
- **Objective**: Set up the project directory structure and configuration files
- **Source Reference**: [Link to Plan §File Structure] and [Link to Constitution §Technology Stack]
- **Dependencies**: None
- **Estimated Time**: 15m
- **Files to Create/Modify**:
  - `pyproject.toml`
  - `uv.lock`
  - `README.md`
  - `src/__init__.py`
  - `src/models/__init__.py`
  - `src/repositories/__init__.py`
  - `src/services/__init__.py`
  - `src/cli/__init__.py`
- **Step-by-Step Instructions**:
  1. Create the project directory structure as specified in the plan
  2. Initialize pyproject.toml with Python 3.13, Pydantic, argparse, and pytest dependencies
  3. Create __init__.py files in each package directory
  4. Create basic README.md with project overview
- **Definition of Done (Acceptance Criteria)**:
  - [x] Project directory structure matches plan specification
  - [x] pyproject.toml includes all required dependencies
  - [x] All __init__.py files created in appropriate directories

## Phase 2: Foundational Components

### Task [T-002]: Implement Custom Exception Classes
- **Objective**: Create custom exception classes for domain-specific error handling
- **Source Reference**: [Link to Spec §Functional Requirements] and [Link to Plan §Custom Exceptions]
- **Dependencies**: T-001
- **Estimated Time**: 15m
- **Files to Create/Modify**:
  - `src/models/task.py`
- **Step-by-Step Instructions**:
  1. Add TaskException base class
  2. Add TaskNotFoundException with constructor taking task_id
  3. Add InvalidTaskDataException with constructor taking message
  4. Ensure all exceptions inherit from base Exception class
- **Definition of Done (Acceptance Criteria)**:
  - [x] TaskException base class created
  - [x] TaskNotFoundException class created with proper constructor
  - [x] InvalidTaskDataException class created with proper constructor

## Phase 3: User Story 1 - Add Tasks (P1)

### Task [T-003]: Implement Task Model with Validation
- **Objective**: Create the Task Pydantic model with all required fields and validation rules
- **Source Reference**: [Link to Spec §Core Domain Entities] and [Link to Plan §Data Model]
- **Dependencies**: T-002
- **Estimated Time**: 15m
- **Files to Create/Modify**:
  - `src/models/task.py`
- **Step-by-Step Instructions**:
  1. Create Task class inheriting from Pydantic BaseModel
  2. Add id (int), title (str), description (Optional[str]), completed (bool), created_at (datetime) fields
  3. Add field_validator for title (1-200 characters)
  4. Add field_validator for description (0-500 characters)
  5. Set created_at default to datetime.utcnow()
- **Definition of Done (Acceptance Criteria)**:
  - [x] Task model created with all required fields
  - [x] Title validation (1-200 characters) implemented
  - [x] Description validation (0-500 characters) implemented
  - [x] Created_at defaults to UTC timestamp

### Task [T-004]: Implement InMemoryTaskRepository
- **Objective**: Create repository with CRUD operations for task storage
- **Source Reference**: [Link to Spec §Functional Requirements] and [Link to Plan §Repository]
- **Dependencies**: T-003
- **Estimated Time**: 30m
- **Files to Create/Modify**:
  - `src/repositories/task_repository.py`
- **Step-by-Step Instructions**:
  1. Create InMemoryTaskRepository class
  2. Initialize internal storage as empty list
  3. Implement create(task: Task) -> Task method
  4. Implement find_all() -> List[Task] method
  5. Implement find_by_id(id: int) -> Task method (raises TaskNotFoundException if not found)
  6. Implement update(id: int, task: Task) -> Task method (raises TaskNotFoundException if not found)
  7. Implement delete(id: int) -> bool method (raises TaskNotFoundException if not found)
  8. Implement ID auto-generation starting from 1
- **Definition of Done (Acceptance Criteria)**:
  - [x] InMemoryTaskRepository class created with all required methods
  - [x] Create method adds task and returns it with assigned ID
  - [x] Find_all method returns all tasks
  - [x] Find_by_id returns task or raises exception
  - [x] Update modifies existing task or raises exception
  - [x] Delete removes task and returns boolean or raises exception
  - [x] ID auto-generation implemented

### Task [T-005]: Implement TaskService
- **Objective**: Create service layer with business logic for task operations
- **Source Reference**: [Link to Spec §Functional Requirements] and [Link to Plan §Service]
- **Dependencies**: T-004
- **Estimated Time**: 30m
- **Files to Create/Modify**:
  - `src/services/task_service.py`
- **Step-by-Step Instructions**:
  1. Create TaskService class with InMemoryTaskRepository dependency
  2. Implement add_task(title: str, description: str) -> Task method
  3. Implement get_all_tasks() -> List[Task] method
  4. Implement update_task(id: int, title: str, description: str) -> Task method
  5. Implement delete_task(id: int) -> bool method
  6. Implement toggle_complete(id: int) -> Task method
  7. Add validation for title/description length requirements
  8. Ensure datetime handling uses UTC timezone
- **Definition of Done (Acceptance Criteria)**:
  - [x] TaskService class created with repository dependency
  - [x] Add_task method creates and returns task with validation
  - [x] Get_all_tasks method returns all tasks
  - [x] Update_task method updates task with validation
  - [x] Delete_task method deletes task and returns boolean
  - [x] Toggle_complete method toggles completion status
  - [x] All validation requirements implemented

### Task [T-006]: Implement CLI Interface
- **Objective**: Create CLI class with command parsing and execution
- **Source Reference**: [Link to Spec §CLI Interface Design] and [Link to Plan §Interface]
- **Dependencies**: T-005
- **Estimated Time**: 30m
- **Files to Create/Modify**:
  - `src/cli/interface.py`
- **Step-by-Step Instructions**:
  1. Create CLI class with TaskService dependency
  2. Implement parse_args() method using argparse for all required commands
  3. Implement execute_command(command: str, args: dict) -> Any method
  4. Implement display_result(result: Any) -> None method
  5. Implement handle_exception(exception: Exception) -> None method
  6. Implement main_loop() -> None method for interactive command processing
  7. Ensure all CLI commands from spec are supported (add, view, update, delete, complete, exit)
- **Definition of Done (Acceptance Criteria)**:
  - [x] CLI class created with service dependency
  - [x] Parse_args method handles all required commands
  - [x] Execute_command routes commands to service methods
  - [x] Display_result formats output appropriately
  - [x] Handle_exception catches and formats errors
  - [x] Main_loop handles interactive command processing
  - [x] All required CLI commands are supported

### Task [T-007]: Implement Main Application Entry Point
- **Objective**: Create main.py that initializes components and starts CLI
- **Source Reference**: [Link to Spec §CLI Interface Design] and [Link to Plan §Main Application]
- **Dependencies**: T-006
- **Estimated Time**: 15m
- **Files to Create/Modify**:
  - `src/main.py`
- **Step-by-Step Instructions**:
  1. Import all necessary components (repository, service, CLI)
  2. Initialize InMemoryTaskRepository instance
  3. Initialize TaskService instance with repository
  4. Initialize CLI instance with service
  5. Call CLI's main_loop() method
  6. Add proper error handling
- **Definition of Done (Acceptance Criteria)**:
  - [x] Main.py creates all component instances
  - [x] Components are properly wired together
  - [x] CLI main loop is called to start application
  - [x] Proper error handling implemented

### Task [T-008]: Test Add Task Functionality
- **Objective**: Verify that users can add new tasks with valid titles and descriptions
- **Source Reference**: [Link to Spec §User Story 1] and [Link to Plan §API Contracts]
- **Dependencies**: T-007
- **Estimated Time**: 15m
- **Files to Create/Modify**:
  - `tests/unit/test_add_task.py`
- **Step-by-Step Instructions**:
  1. Create test file for add task functionality
  2. Test adding task with valid title only
  3. Test adding task with title and description
  4. Test adding task with empty title (should fail)
  5. Test adding task with title exceeding 200 characters (should fail)
  6. Test adding task with description exceeding 500 characters (should fail)
  7. Verify success messages match spec format
- **Definition of Done (Acceptance Criteria)**:
  - [x] Test for adding task with valid title passes
  - [x] Test for adding task with title and description passes
  - [x] Test for empty title rejection passes
  - [x] Test for title length validation passes
  - [x] Test for description length validation passes
  - [x] Success messages match spec format

## Phase 4: User Story 2 - View Tasks (P2)

### Task [T-009]: Enhance Task Display Format
- **Objective**: Implement proper display format for viewing tasks with ID, status, and title
- **Source Reference**: [Link to Spec §User Story 2] and [Link to Plan §Success and Error Message Formats]
- **Dependencies**: T-008
- **Estimated Time**: 15m
- **Files to Create/Modify**:
  - `src/cli/interface.py`
- **Step-by-Step Instructions**:
  1. Modify display_result method to handle task list display
  2. Format tasks as 'ID | [ ] | Title' for pending tasks
  3. Format tasks as 'ID | [x] | Title' for completed tasks
  4. Include description when space permits: 'ID | [ ] | Title - Description'
  5. Handle case when no tasks exist ('No tasks in your list')
- **Definition of Done (Acceptance Criteria)**:
  - [x] Pending tasks display as 'ID | [ ] | Title'
  - [x] Completed tasks display as 'ID | [x] | Title'
  - [x] Descriptions included when space permits
  - [x] Empty list displays 'No tasks in your list'

### Task [T-010]: Test View Task Functionality
- **Objective**: Verify that users can view all tasks in the specified format
- **Source Reference**: [Link to Spec §User Story 2] and [Link to Plan §API Contracts]
- **Dependencies**: T-009
- **Estimated Time**: 15m
- **Files to Create/Modify**:
  - `tests/unit/test_view_tasks.py`
- **Step-by-Step Instructions**:
  1. Create test file for view task functionality
  2. Test viewing tasks with mixed completion statuses
  3. Test viewing tasks with descriptions
  4. Test viewing empty task list
  5. Verify display format matches spec requirements
- **Definition of Done (Acceptance Criteria)**:
  - [x] Test for viewing tasks with mixed statuses passes
  - [x] Test for viewing tasks with descriptions passes
  - [x] Test for viewing empty list passes
  - [x] Display format matches spec requirements

## Phase 5: User Story 3 - Update Tasks (P3)

### Task [T-011]: Implement Task Update Functionality
- **Objective**: Enable users to update existing task details with validation
- **Source Reference**: [Link to Spec §User Story 3] and [Link to Plan §Service]
- **Dependencies**: T-010
- **Estimated Time**: 15m
- **Files to Create/Modify**:
  - `src/services/task_service.py`
  - `src/cli/interface.py`
- **Step-by-Step Instructions**:
  1. Ensure update_task method properly validates new title/description
  2. Update CLI to handle update command with ID and new details
  3. Ensure error handling for invalid task IDs
  4. Verify success message format matches spec
- **Definition of Done (Acceptance Criteria)**:
  - [x] Update functionality properly validates new details
  - [x] CLI handles update command with ID and new details
  - [x] Error handling for invalid IDs implemented
  - [x] Success message format matches spec

### Task [T-012]: Test Update Task Functionality
- **Objective**: Verify that users can update existing task details with proper validation
- **Source Reference**: [Link to Spec §User Story 3] and [Link to Plan §API Contracts]
- **Dependencies**: T-011
- **Estimated Time**: 15m
- **Files to Create/Modify**:
  - `tests/unit/test_update_task.py`
- **Step-by-Step Instructions**:
  1. Create test file for update task functionality
  2. Test updating task with valid details
  3. Test updating task with invalid ID (should fail)
  4. Test updating task with empty title (should fail)
  5. Test updating task with title exceeding 200 characters (should fail)
  6. Test updating task with description exceeding 500 characters (should fail)
  7. Verify success/error messages match spec format
- **Definition of Done (Acceptance Criteria)**:
  - [x] Test for updating task with valid details passes
  - [x] Test for invalid ID rejection passes
  - [x] Test for empty title rejection passes
  - [x] Test for title length validation passes
  - [x] Test for description length validation passes
  - [x] Success/error messages match spec format

## Phase 6: User Story 4 - Complete/Delete Tasks (P4)

### Task [T-013]: Implement Complete and Delete Functionality
- **Objective**: Enable users to mark tasks as complete/incomplete and delete tasks
- **Source Reference**: [Link to Spec §User Story 4] and [Link to Plan §Service]
- **Dependencies**: T-012
- **Estimated Time**: 15m
- **Files to Create/Modify**:
  - `src/services/task_service.py`
  - `src/cli/interface.py`
- **Step-by-Step Instructions**:
  1. Ensure toggle_complete method properly toggles task status
  2. Ensure delete_task method properly removes task
  3. Update CLI to handle complete and delete commands with ID
  4. Ensure error handling for invalid task IDs
  5. Verify success message formats match spec
- **Definition of Done (Acceptance Criteria)**:
  - [x] Toggle complete functionality properly toggles status
  - [x] Delete functionality properly removes task
  - [x] CLI handles complete and delete commands with ID
  - [x] Error handling for invalid IDs implemented
  - [x] Success message formats match spec

### Task [T-014]: Test Complete and Delete Functionality
- **Objective**: Verify that users can mark tasks as complete/incomplete and delete tasks
- **Source Reference**: [Link to Spec §User Story 4] and [Link to Plan §API Contracts]
- **Dependencies**: T-013
- **Estimated Time**: 15m
- **Files to Create/Modify**:
  - `tests/unit/test_complete_delete_task.py`
- **Step-by-Step Instructions**:
  1. Create test file for complete and delete functionality
  2. Test marking pending task as complete
  3. Test marking completed task as pending
  4. Test deleting existing task
  5. Test complete/delete with invalid ID (should fail)
  6. Verify success/error messages match spec format
- **Definition of Done (Acceptance Criteria)**:
  - [x] Test for marking pending task as complete passes
  - [x] Test for marking completed task as pending passes
  - [x] Test for deleting existing task passes
  - [x] Test for invalid ID rejection passes
  - [x] Success/error messages match spec format

## Phase 7: Polish & Cross-Cutting Concerns

### Task [T-015]: Integrate All Components and Perform End-to-End Testing
- **Objective**: Test complete user workflow from adding to deleting tasks
- **Source Reference**: [Link to Spec §CLI Interface Design] and [Link to Plan §Data Flow]
- **Dependencies**: T-014
- **Estimated Time**: 30m
- **Files to Create/Modify**:
  - `tests/integration/test_end_to_end.py`
- **Step-by-Step Instructions**:
  1. Create end-to-end test following the example session from spec
  2. Test the complete workflow: add, view, complete, update, view, delete, view
  3. Verify all success messages match the spec format
  4. Test error conditions and verify error messages
  5. Verify performance requirements (response times)
- **Definition of Done (Acceptance Criteria)**:
  - [x] End-to-end workflow test passes
  - [x] All success messages match spec format
  - [x] Error handling works correctly
  - [x] Performance requirements met

### Task [T-016]: Final Integration and Documentation
- **Objective**: Complete final integration, update documentation, and prepare for deployment
- **Source Reference**: [Link to Spec §Success Criteria] and [Link to Plan §Quickstart Guide]
- **Dependencies**: T-015
- **Estimated Time**: 15m
- **Files to Create/Modify**:
  - `README.md`
  - `src/main.py`
- **Step-by-Step Instructions**:
  1. Update README.md with setup instructions from plan
  2. Verify all CLI commands work as specified in the spec
  3. Test the happy path scenario from the spec
  4. Ensure all error handling works as specified
  5. Verify all functional requirements (REQ-01 through REQ-11) are met
- **Definition of Done (Acceptance Criteria)**:
  - [x] README.md updated with setup instructions
  - [x] All CLI commands work as specified
  - [x] Happy path scenario works correctly
  - [x] All functional requirements met
  - [x] All error handling works as specified

## Task Execution Order

1. **Setup Phase**: T-001
2. **Foundation Phase**: T-002
3. **User Story 1**: T-003 → T-004 → T-005 → T-006 → T-007 → T-008
4. **User Story 2**: T-009 → T-010
5. **User Story 3**: T-011 → T-012
6. **User Story 4**: T-013 → T-014
7. **Polish Phase**: T-015 → T-016

## Parallel Execution Opportunities

- [P] T-002, T-003 can be developed in parallel after T-001
- [P] T-004, T-005 can be developed in parallel after T-003
- [P] T-006 can be developed in parallel with T-004, T-005 after T-003
- [P] T-008, T-009, T-010 can be developed in parallel after T-007
- [P] T-012, T-013, T-014 can be developed in parallel after T-011

## Independent Test Criteria

- **User Story 1 Complete**: T-008 passes (add task functionality verified)
- **User Story 2 Complete**: T-010 passes (view task functionality verified)
- **User Story 3 Complete**: T-012 passes (update task functionality verified)
- **User Story 4 Complete**: T-014 passes (complete/delete functionality verified)
- **Phase Complete**: T-016 passes (full integration and requirements verified)