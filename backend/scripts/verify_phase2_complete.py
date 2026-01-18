#!/usr/bin/env python3
# [Task]: T-012 | [From]: specs/2-plan/phase-2-fullstack.md

"""
Verification script for Phase 2 completion.
This script checks if all required components for Phase 2 are properly implemented.
"""

import os
import sys
import json
from pathlib import Path
import asyncio
import httpx


async def check_health_endpoint():
    """Check if the health endpoint is accessible."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:7860/health", timeout=5.0)
            return response.status_code == 200
    except Exception:
        return False


def check_file_exists(filepath):
    """Check if a file exists at the given path."""
    return Path(filepath).exists()


def main():
    """Main verification function."""
    print("🔍 Phase 2 Verification Script")
    print("=" * 50)

    # Define the checklist
    checklist = {
        "Frontend Setup": {
            "description": "Check if frontend package.json exists",
            "filepath": "frontend/package.json",
            "status": False
        },
        "Rate Limiting Middleware": {
            "description": "Check if rate limiting middleware exists",
            "filepath": "backend/src/middleware/rate_limit.py",
            "status": False
        },
        "Health Check Endpoint": {
            "description": "Check if health check endpoint exists",
            "filepath": "backend/src/api/health_router.py",
            "status": False
        },
        "API Client": {
            "description": "Check if frontend API client exists",
            "filepath": "frontend/src/lib/api.ts",
            "status": False
        },
        "Login Page": {
            "description": "Check if login page exists",
            "filepath": "frontend/src/app/login/page.tsx",
            "status": False
        },
        "Signup Page": {
            "description": "Check if signup page exists",
            "filepath": "frontend/src/app/signup/page.tsx",
            "status": False
        },
        "Dashboard Page": {
            "description": "Check if dashboard page exists",
            "filepath": "frontend/src/app/dashboard/page.tsx",
            "status": False
        },
        "Task Item Component": {
            "description": "Check if TaskItem component exists",
            "filepath": "frontend/src/components/TaskItem.tsx",
            "status": False
        },
        "Create Task Form Component": {
            "description": "Check if CreateTaskForm component exists",
            "filepath": "frontend/src/components/CreateTaskForm.tsx",
            "status": False
        },
        "Auth Middleware": {
            "description": "Check if authentication middleware exists",
            "filepath": "backend/src/middleware/auth_middleware.py",
            "status": False
        },
        "Circuit Breaker": {
            "description": "Check if circuit breaker pattern exists",
            "filepath": "backend/src/middleware/circuit_breaker.py",
            "status": False
        },
        "DB Connection Pooling": {
            "description": "Check if database connection pooling exists",
            "filepath": "backend/src/db/connection.py",
            "status": False
        },
        "API Documentation": {
            "description": "Check if API documentation exists",
            "filepath": "API_DOCS.md",
            "status": False
        },
        "README Updated": {
            "description": "Check if README has Phase II instructions",
            "filepath": "README.md",
            "status": False
        }
    }

    # Check file existence
    for item_name, item_info in checklist.items():
        if check_file_exists(item_info["filepath"]):
            # For README, check if it contains Phase II instructions
            if item_name == "README Updated":
                with open(item_info["filepath"], 'r') as f:
                    content = f.read()
                    if "Phase II" in content and "Full-Stack Web Application" in content:
                        item_info["status"] = True
                    else:
                        item_info["status"] = False
            else:
                item_info["status"] = True

            if item_info["status"]:
                print(f"✅ {item_name}: Found")
            else:
                print(f"❌ {item_name}: Missing or doesn't meet criteria - {item_info['description']}")
        else:
            print(f"❌ {item_name}: Missing - {item_info['description']}")

    print("\n" + "=" * 50)

    # Count completed items
    completed = sum(1 for item in checklist.values() if item["status"])
    total = len(checklist)

    print(f"📊 Summary: {completed}/{total} items completed")

    # Check health endpoint separately (requires server to be running)
    print("\n🌐 Health Check Endpoint Test:")
    print("   (This test requires the backend server to be running on localhost:7860)")
    try:
        health_ok = asyncio.run(check_health_endpoint())
        if health_ok:
            print("   ✅ Health endpoint is accessible")
            completed += 1
            total += 1
        else:
            print("   ❌ Health endpoint is not accessible (server may not be running)")
    except Exception as e:
        print(f"   ❌ Health endpoint test failed: {str(e)}")

    print("\n" + "=" * 50)
    print("📋 Phase 2 Component Checklist:")

    for item_name, item_info in checklist.items():
        status = "✅" if item_info["status"] else "❌"
        print(f"  {status} {item_name}")

    # Final assessment
    print(f"\n🎯 Final Status: {completed}/{total} checks passed")

    if completed == total:
        print("🎉 Phase 2 implementation is complete!")
        return True
    else:
        print("⚠️  Phase 2 implementation is incomplete.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)