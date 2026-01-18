# [Task]: T-002 | [From]: specs/2-plan/phase-2-fullstack.md

"""
Module initialization for the models package.
Exports the core domain models for easy import.
"""

from .user import User
from .task import Task, TaskUpdate

__all__ = ["User", "Task", "TaskUpdate"]