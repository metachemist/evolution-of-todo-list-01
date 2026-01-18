import os

def check_feature(name, path, search_term=None):
    exists = os.path.exists(path)
    found_term = False
    if exists and search_term:
        with open(path, 'r') as f:
            if search_term in f.read():
                found_term = True
    
    # Logic: If looking for file, existence is enough. If looking for term inside, need both.
    result = "✅ FOUND" if (exists and (not search_term or found_term)) else "❌ MISSING"
    print(f"{name.ljust(40)}: {result}")

print("--- 🔍 PHASE 2 REALITY AUDIT ---")

# T-003: Repositories
check_feature("UserRepository Class", "backend/src/repositories/user_repository.py", "class UserRepository")
check_feature("TaskRepository Class", "backend/src/repositories/task_repository.py", "class TaskRepository")

# T-004: Auth & Services (The tricky part)
check_feature("Auth Router", "backend/src/api/v1/endpoints/auth.py")
check_feature("Task Service Class", "backend/src/services/task_service.py", "class TaskService")
check_feature("Idempotency Logic", "backend/src/api/v1/endpoints/tasks.py", "idempotency_key")

# T-005: API
check_feature("Task Router", "backend/src/api/v1/endpoints/tasks.py")

# T-006: Docker (Should be missing)
check_feature("Docker Compose", "docker-compose.yml")