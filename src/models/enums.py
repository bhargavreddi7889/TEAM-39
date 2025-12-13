from enum import Enum


class Role(str, Enum):
    """User roles for access control."""
    ADMIN = "admin"
    STUDENT = "student"
    # Future: FACULTY = "faculty"
